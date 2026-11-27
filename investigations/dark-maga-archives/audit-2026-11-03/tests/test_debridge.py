"""Regression checks for source units, decoded makers and bridge-report scope."""
import csv
import json
from datetime import datetime, timedelta, timezone
from decimal import Decimal
from pathlib import Path

import pytest

from dmaga.debridge import case_bridge_paragraph, read_decoded_orders, select_makers, source_usdc
from dmaga.frfmt import fr


ROOT = Path(__file__).resolve().parents[1]
TABLE = ROOT / "audits/2026-11-03/work_I/i14_orders.csv"
MINT = datetime(2024, 7, 14, 2, 5, 25, tzinfo=timezone.utc)


@pytest.fixture
def orders():
    return read_decoded_orders(TABLE)


@pytest.fixture
def members():
    return set(json.loads((ROOT / "data/prevent_groups.json").read_text())[0]["members"])


@pytest.fixture
def row():
    with TABLE.open(newline="", encoding="utf-8") as handle:
        return next(csv.DictReader(handle))


def write_table(tmp_path, rows, *, fields=None):
    path = tmp_path / "orders.csv"
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields or list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    return path


def test_decoded_archive_amounts_are_reconciled_at_micro_usdc_precision(orders, members):
    assert len(orders) == 76
    assert source_usdc(orders) == Decimal("1018687.178289")
    group = select_makers(orders, members)
    assert len(members) == 33
    assert len(group) == 68
    assert source_usdc(group) == Decimal("974077.946152")
    outside = [order for order in orders if order.maker not in members]
    assert len(outside) == 8
    assert source_usdc(outside) == Decimal("44609.232137")
    assert source_usdc(group) + source_usdc(outside) == source_usdc(orders)
    early = select_makers(orders, members, before=MINT)
    assert len(early) == 15
    assert source_usdc(early) == Decimal("1610.177867")


def test_c73_receiver_subtotal_is_not_its_complete_wallet_total(orders):
    c73 = select_makers(orders, {"C73Yv9iHmTaf8SU2XFnGLt7QXUDqbeWNtUYza9WJhkae"})
    receiver = [o for o in c73 if o.take_chain == 1
                and o.receiver == "0x2d86499a410a9ac2139833ba8d6942b8a8700a7b"]
    assert (len(c73), source_usdc(c73)) == (29, Decimal("527600.400084"))
    assert (len(receiver), source_usdc(receiver)) == (27, Decimal("496371.589492"))


def test_four_orders_cached_under_other_wallets_remain_in_the_maker_cohort(orders, members):
    with TABLE.open(newline="", encoding="utf-8") as handle:
        other_cache_signatures = {
            r["sig"] for r in csv.DictReader(handle)
            if r["maker"] in members and r["wallet_file"] not in members
        }
    retained = [o for o in select_makers(orders, members) if o.signature in other_cache_signatures]
    assert len(retained) == 4
    assert source_usdc(retained) == Decimal("175439.743465")


def test_native_sol_fees_are_not_added_to_usdc(tmp_path, row):
    row.update(give_amount="1000000", fee_pct="500", fee_fix_lamports="15000000")
    result = read_decoded_orders(write_table(tmp_path, [row]))
    assert source_usdc(result) == Decimal("1.0005")


def test_rounding_is_applied_after_aggregation(tmp_path, row):
    row.update(give_amount="1005000", fee_pct="0")
    second = dict(row, sig="another-source-signature", nonce=str(int(row["nonce"]) + 1))
    total = source_usdc(read_decoded_orders(write_table(tmp_path, [row, second])))
    assert total == Decimal("2.010000")
    assert f"{total:.2f}" == "2.01"


def test_pre_mint_cutoff_is_strict_and_normalized_to_utc(tmp_path, row):
    rows = [
        dict(row, sig="before", utc=(MINT - timedelta(seconds=1)).isoformat()),
        dict(row, sig="at", utc="2024-07-14T03:05:25+01:00"),
        dict(row, sig="after", utc=(MINT + timedelta(seconds=1)).isoformat()),
    ]
    result = read_decoded_orders(write_table(tmp_path, rows))
    before = select_makers(result, {row["maker"]}, before=MINT)
    assert [o.signature for o in before] == ["before"]
    assert result[1].utc == MINT
    with pytest.raises(ValueError, match="timezone"):
        select_makers(result, {row["maker"]}, before=MINT.replace(tzinfo=None))


@pytest.mark.parametrize("field,value,message", [
    ("give_token", "another-token", "source USDC"),
    ("give_chain", "1", "source USDC"),
    ("give_amount", "1.5", "non-negative integer"),
    ("give_amount", "NaN", "non-negative integer"),
    ("fee_pct", "-1", "non-negative integer"),
    ("fee_pct", "", "non-negative integer"),
    ("fee_fix_lamports", "inf", "non-negative integer"),
    ("utc", "2024-07-14 02:05:25", "timezone"),
    ("utc", "not a time", "source timestamp"),
    ("maker", "", "missing signature, maker or receiver"),
    ("receiver", " ", "missing signature, maker or receiver"),
])
def test_invalid_source_inputs_fail_instead_of_producing_plausible_totals(tmp_path, row, field, value, message):
    row[field] = value
    with pytest.raises(ValueError, match=message):
        read_decoded_orders(write_table(tmp_path, [row]))


def test_duplicate_cached_event_fails_instead_of_double_counting(tmp_path, row):
    copy = dict(row, wallet_file="another-cache-wallet")
    with pytest.raises(ValueError, match="repeated source order"):
        read_decoded_orders(write_table(tmp_path, [row, copy]))


def test_missing_required_column_fails(tmp_path, row):
    del row["fee_pct"]
    with pytest.raises(ValueError, match="missing or duplicate columns"):
        read_decoded_orders(write_table(tmp_path, [row]))


def test_empty_table_fails(tmp_path, row):
    path = write_table(tmp_path, [], fields=list(row))
    with pytest.raises(ValueError, match="empty"):
        read_decoded_orders(path)


def test_published_bridge_paragraph_matches_the_targeted_recalculation(orders, members):
    lines = (ROOT / "docs/CASE_REPORT.md").read_text().splitlines()
    published = next(line for line in lines if line.startswith("9. **Ponts :"))
    assert published == "9. " + fr(case_bridge_paragraph(orders, members, MINT))
