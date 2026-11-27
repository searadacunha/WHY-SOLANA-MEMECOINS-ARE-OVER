"""Tests du parseur sur des cas synthétiques minimaux. Les vraies transactions sont testées par
tests/test_real_txs.py, qui a besoin du réseau ou du cache brut."""
import pytest

from dmaga.config import BONDING_CURVE, MINT, WSOL
from dmaga.normalize import RAYDIUM_AUTH as AUTH, parse_tx

VD, VS = "vaultDmaga", "vaultSol"


def tx(pre, post, keys=("trader", BONDING_CURVE), pre_l=(0, 0), post_l=(0, 0), err=None):
    return {
        "slot": 1, "blockTime": 2, "transactionIndex": 3,
        "transaction": {"signatures": ["sig"],
                        "message": {"accountKeys": [{"pubkey": k, "signer": i == 0} for i, k in enumerate(keys)]}},
        "meta": {"err": err, "fee": 5000, "preBalances": list(pre_l), "postBalances": list(post_l),
                 "preTokenBalances": pre, "postTokenBalances": post},
    }


def bal(i, mint, owner, amount, dec=6):
    return {"accountIndex": i, "mint": mint, "owner": owner, "uiTokenAmount": {"amount": str(amount), "decimals": dec}}


KEYS = ("trader", VD, VS, "traderAta", "traderWsol")


def test_raydium_buy():
    pre = [bal(1, MINT, AUTH, 1000), bal(2, WSOL, AUTH, 500, 9), bal(3, MINT, "trader", 0)]
    post = [bal(1, MINT, AUTH, 900), bal(2, WSOL, AUTH, 600, 9), bal(3, MINT, "trader", 100)]
    rows = parse_tx(tx(pre, post, KEYS, (0,) * 5, (0,) * 5), {VD}, {VS}, "t")
    assert [r["kind"] for r in rows] == ["swap"]
    r = rows[0]
    assert (r["owner"], r["token_delta"], r["sol_lamports"]) == ("trader", 100, -100)


def test_raydium_sell():
    pre = [bal(1, MINT, AUTH, 1000), bal(2, WSOL, AUTH, 500, 9), bal(3, MINT, "trader", 100)]
    post = [bal(1, MINT, AUTH, 1100), bal(2, WSOL, AUTH, 450, 9), bal(3, MINT, "trader", 0)]
    r = parse_tx(tx(pre, post, KEYS, (0,) * 5, (0,) * 5), {VD}, {VS}, "t")[0]
    assert (r["kind"], r["token_delta"], r["sol_lamports"]) == ("swap", -100, 50)


def test_failed_tx_gives_nothing():
    assert parse_tx(tx([], [], err={"x": 1}), {VD}, {VS}, "t") == []


def test_pure_transfer():
    pre = [bal(1, MINT, "a", 100), bal(2, MINT, "b", 0)]
    post = [bal(1, MINT, "a", 40), bal(2, MINT, "b", 60)]
    rows = parse_tx(tx(pre, post, ("a", "ata1", "ata2"), (0,) * 3, (0,) * 3), {VD}, {VS}, "t")
    assert {(r["kind"], r["owner"], r["token_delta"]) for r in rows} == {("transfer", "a", -60), ("transfer", "b", 60)}


def test_lp_remove_both_vaults_fall():
    pre = [bal(1, MINT, AUTH, 1000), bal(2, WSOL, AUTH, 500, 9), bal(3, MINT, "lp", 0)]
    post = [bal(1, MINT, AUTH, 500), bal(2, WSOL, AUTH, 250, 9), bal(3, MINT, "lp", 500)]
    rows = parse_tx(tx(pre, post, KEYS, (0,) * 5, (0,) * 5), {VD}, {VS}, "t")
    assert rows[0]["kind"] == "lp_remove" and rows[0]["pool_sol_delta"] == -250


def test_curve_buy_uses_curve_lamports():
    pre = [bal(1, MINT, BONDING_CURVE, 1000)]
    post = [bal(1, MINT, BONDING_CURVE, 900), bal(3, MINT, "trader", 100)]
    keys = ("trader", "ataCurve", BONDING_CURVE, "traderAta")
    r = parse_tx(tx(pre, post, keys, (10, 0, 7, 0), (5, 0, 12, 0)), {VD}, {VS}, "t")[0]
    assert (r["kind"], r["venue"], r["token_delta"], r["sol_lamports"]) == ("swap", "pumpfun", 100, -5)


def test_other_venue_is_not_a_trader():
    # vente routée vers un pool CLMM : le trader perd les jetons, le pool paie, aucune fausse arête
    keys = ("trader", "ata", "clmmDmaga", "clmmWsol")
    pre = [bal(1, MINT, "trader", 100), bal(2, MINT, "clmm", 0), bal(3, WSOL, "clmm", 500, 9)]
    post = [bal(1, MINT, "trader", 0), bal(2, MINT, "clmm", 100), bal(3, WSOL, "clmm", 450, 9)]
    rows = parse_tx(tx(pre, post, keys, (0,) * 4, (0,) * 4), {VD}, {VS}, "t", {"clmm"})
    assert [(r["kind"], r["owner"], r["token_delta"], r["sol_lamports"]) for r in rows] == [("swap", "trader", -100, 50)]


def test_dlmm_one_sided_deposit_is_lp_not_transfer():
    keys = ("lp", "ata", "dlmmDmaga")
    pre = [bal(1, MINT, "lp", 100), bal(2, MINT, "dlmm", 0)]
    post = [bal(1, MINT, "lp", 40), bal(2, MINT, "dlmm", 60)]
    rows = parse_tx(tx(pre, post, keys, (0,) * 3, (0,) * 3), {VD}, {VS}, "t", {"dlmm"})
    assert [(r["kind"], r["owner"], r["token_delta"]) for r in rows] == [("lp_add", "lp", -60)]


def test_usdc_pool_swap_carries_usdc():
    from dmaga.normalize import USDC
    keys = ("trader", "ata", "poolD", "poolU")
    pre = [bal(1, MINT, "trader", 100), bal(2, MINT, "u", 0), bal(3, USDC, "u", 500)]
    post = [bal(1, MINT, "trader", 0), bal(2, MINT, "u", 100), bal(3, USDC, "u", 450)]
    r = parse_tx(tx(pre, post, keys, (0,) * 4, (0,) * 4), {VD}, {VS}, "t", {"u"})[0]
    assert (r["kind"], r["usdc_raw"], r["sol_lamports"]) == ("swap", 50, 0)


def test_fee_collector_is_not_a_buyer():
    pre = [bal(1, MINT, AUTH, 1000), bal(2, WSOL, AUTH, 500, 9), bal(3, MINT, "trader", 0), bal(4, MINT, "fee", 0)]
    post = [bal(1, MINT, AUTH, 900), bal(2, WSOL, AUTH, 600, 9), bal(3, MINT, "trader", 99), bal(4, MINT, "fee", 1)]
    keys = ("trader", VD, VS, "ata", "feeAta")
    rows = parse_tx(tx(pre, post, keys, (0,) * 5, (0,) * 5), {VD}, {VS}, "t")
    got = {r["owner"]: (r["kind"], r["sol_lamports"]) for r in rows}
    assert got["trader"] == ("swap", -100) and got["fee"] == ("fee_share", 0)


@pytest.mark.parametrize("kind,owner_delta,quote_direction", [
    ("swap", 1, 1), ("swap", -1, -1),
    ("lp_add", -1, 1), ("lp_remove", 1, -1),
])
@pytest.mark.parametrize("quote_mint,quote_field", [(WSOL, "sol_lamports"),
                                                  ("EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v", "usdc_raw")])
def test_multi_owner_quotes_conserve_raw_units(kind, owner_delta, quote_direction, quote_mint, quote_field):
    # Three equal shares of two raw quote units used to round to three units.
    keys = ("payer", VD, VS, "ata_c", "ata_a", "ata_b")
    pre = [bal(1, MINT, AUTH, 100), bal(2, quote_mint, AUTH, 100)]
    post = [bal(1, MINT, AUTH, 100 - 3 * owner_delta),
            bal(2, quote_mint, AUTH, 100 + 2 * quote_direction)]
    for i, owner in enumerate(("c", "a", "b"), 3):
        pre.append(bal(i, MINT, owner, 10))
        post.append(bal(i, MINT, owner, 10 + owner_delta))
    rows = parse_tx(tx(pre, post, keys, (0,) * 6, (0,) * 6), {VD}, {VS}, "t")
    assert {r["kind"] for r in rows} == {kind}
    assert sum(r[quote_field] for r in rows) == -2 * quote_direction
    assert sorted(abs(r[quote_field]) for r in rows) == [0, 1, 1]
    # Equal remainders have a stable owner tie-break, independent of account order.
    assert {r["owner"]: r[quote_field] for r in rows} == {
        "a": -quote_direction, "b": -quote_direction, "c": 0,
    }


def test_single_owner_quote_above_float_precision_stays_exact():
    quote = 2**53 + 1
    pre = [bal(1, MINT, AUTH, 100), bal(2, WSOL, AUTH, 0, 9), bal(3, MINT, "trader", 0)]
    post = [bal(1, MINT, AUTH, 0), bal(2, WSOL, AUTH, quote, 9), bal(3, MINT, "trader", 100)]
    rows = parse_tx(tx(pre, post, KEYS, (0,) * 5, (0,) * 5), {VD}, {VS}, "t")
    assert rows[0]["sol_lamports"] == -quote


def test_curve_creation_multiple_buyers_split_cost_once():
    keys = ("payer", "curveAta", BONDING_CURVE, "ata_b", "ata_a")
    post = [bal(1, MINT, BONDING_CURVE, 900), bal(3, MINT, "b", 30), bal(4, MINT, "a", 70)]
    rows = parse_tx(tx([], post, keys, (0,) * 5, (0, 0, 100, 0, 0)), {VD}, {VS}, "t")
    assert rows[0]["kind"] == "mint_supply" and rows[0]["token_delta"] == 1000
    buys = [r for r in rows if r["kind"] == "swap"]
    assert {r["owner"]: r["sol_lamports"] for r in buys} == {"b": -30, "a": -70}
    assert sum(r["sol_lamports"] for r in buys) == -100


def test_study_parser_matches_expected_on_real_shape():
    """parse_swaps de l'étude : frais écartés, réserve d'un autre venue écartée, comptage des rejets."""
    import importlib.util
    import pathlib
    import sys
    from collections import Counter
    code = pathlib.Path(__file__).resolve().parent.parent / "etude_final" / "code"
    sys.path.insert(0, str(code))
    spec = importlib.util.spec_from_file_location("col50", code / "col_50_ctrl.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    keys = ("trader", VD, VS, "ata", "feeAta", "otherD", "otherS")
    pre = [bal(1, MINT, AUTH, 1000), bal(2, WSOL, AUTH, 500, 9), bal(3, MINT, "trader", 0), bal(4, MINT, "fee", 0),
           bal(5, MINT, "amm2", 50), bal(6, WSOL, "amm2", 50, 9)]
    post = [bal(1, MINT, AUTH, 900), bal(2, WSOL, AUTH, 600, 9), bal(3, MINT, "trader", 99), bal(4, MINT, "fee", 1),
            bal(5, MINT, "amm2", 60), bal(6, WSOL, "amm2", 40, 9)]
    st = Counter()
    rows = m.parse_swaps(tx(pre, post, keys, (0,) * 7, (0,) * 7), MINT, VD, VS, st)
    assert [(r["owner"], r["qty"], r["sol"]) for r in rows] == [("trader", 99, -100)]
    assert st["parts_de_frais"] == 1 and st["non_signataire_deux_cotes"] == 1 and st["swaps"] == 1
