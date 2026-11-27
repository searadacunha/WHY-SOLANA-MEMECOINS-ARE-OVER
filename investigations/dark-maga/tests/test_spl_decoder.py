"""Régression du décodeur SPL qui préserve le mint (dmaga.spl, issue #27), sur des transactions réelles figées."""
import base64
import json
import struct
import unittest
from pathlib import Path

import pytest

from dmaga.spl import keys, movements, pump_create_event, token_accounts

FIX = Path(__file__).resolve().parent / "fixtures" / "spl"
DMAGA = "7D7BRcBYepfi77vxySapmeqRNN1wsBBxnFPJGbH5pump"
WSOL = "So11111111111111111111111111111111111111112"
W7GVC = "7GVCZAYG5NfiJsuqUdvc9hB2ts2W3tSrGdya4CyR1M5j"
W9SXM = "9Sxmf25WG5WVQ5p86ycWeo5hMEwxiWPkFtLdRdTrHSQS"
PUMP = "6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P"
OTHER = "TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA"
RECEIPTS = FIX.parents[2] / "investigations" / "2026-11-06_historical_replay" / "evidence" / "receipts"
# Official Pump IDL, commit 639b87fb45c3adeffa6f7c4a1bf0cb85e392bf22:
# https://github.com/pump-fun/pump-public-docs/blob/639b87fb45c3adeffa6f7c4a1bf0cb85e392bf22/idl/pump.json
CREATE_EVENT = bytes([27, 114, 169, 77, 222, 235, 99, 118])


def tx(prefix):
    hit = list(FIX.glob(f"{prefix}*.json"))
    assert len(hit) == 1, prefix
    return json.loads(hit[0].read_text())


class SplDecoder(unittest.TestCase):
    def test_plain_transfer_without_mint_account_keeps_mint_and_owners(self):
        t = tx("58SeigZv41h2")
        self.assertNotIn(DMAGA, keys(t))  # le mint n'est pas cité : absent de l'historique du mint
        mv = [m for m in movements(t) if m["kind"] == "token"]
        self.assertEqual([(m["src"][:8], m["dst"][:8], m["amount"], m["mint"], m["src_owner_known"], m["dst_owner_known"]) for m in mv],
                         [("6t2dz4jm", "AtZjv3Du", 13_193_693_055_782, DMAGA, True, True)])

    def test_transfer_checked_is_decoded_the_same_way(self):
        mv = [m for m in movements(tx("2FezsDLMjqaseGDi")) if m["kind"] == "token"]
        self.assertEqual([(m["src"], m["dst"], m["amount"], m["mint"]) for m in mv], [(W7GVC, W9SXM, 20_000_000_000_000, DMAGA)])

    def test_account_created_and_closed_in_same_tx_is_resolved_by_its_initialization(self):
        t = tx("2PHU4HTSGRJ6xKncBiVm")
        temp = [a for a, (o, m) in token_accounts(t).items() if o == W9SXM and m == WSOL]
        self.assertEqual(len(temp), 1)
        mv = [m for m in movements(t) if m["kind"] == "token" and m["mint"] == WSOL]
        self.assertTrue(all(m["src_owner_known"] and m["dst_owner_known"] for m in mv))
        self.assertIn(("5Q544fKrFoe6tsEbD7S8EmxGTJYAKtTVhAW5Q5pge4j1", W9SXM, 17_874_608_396), [(m["src"], m["dst"], m["amount"]) for m in mv])

    def test_closed_wsol_account_returns_running_balance(self):
        close = [m for m in movements(tx("44Sd6xet31me1Hc1")) if m["kind"] == "close" and m["dst"] == W7GVC]
        self.assertEqual([m["amount"] for m in close], [189_653_006_599])  # WSOL reçu dans la transaction + loyer

    def test_transient_wsol_close_refunds_creation_rent(self):
        # Real 9Sxm swap: temporary account starts/ends at 0 lamports.
        # createAccount funds rent; WSOL arrives then a fee is transferred out.
        t = tx("2PHU4HTSGRJ6xKncBiVm")
        close = [m for m in movements(t) if m["kind"] == "close" and m["dst"] == W9SXM]
        rent = 2_039_280
        wsol_in = 17_874_608_396
        wsol_out = 211_782_429
        self.assertEqual(len(close), 1)
        self.assertEqual(close[0]["amount"], rent + wsol_in - wsol_out)
        self.assertEqual(close[0]["amount"], 17_664_865_247)


    def test_router_pass_through_leg_is_netted_by_normalize(self):
        # Real multi-hop route (WSOL → USDC → USDT → DMAGA, 11/11/2025): the router receives then forwards the same DMAGA.
        # Both gtba edges exist on chain, but trades already holds the buyer's net: the router leg must never be re-added.
        from dmaga.normalize import parse_tx
        t = tx("YQMWMCwa9pmKi9tn")
        pool, router, buyer = "4F6uLJwkvWhSkbkZnvBzaGhmDtFkzLA71jNYhfFrRznQ", "ARu4n5mFdZogZAravu7CcizaojWnS6oqka37gdLT5SZn", "Bya5eBy9KgqaXfnLKuvFYBaqzYqxip3JVimhtToKRxLp"
        mv = [(m["path"], m["src"], m["dst"], m["amount"]) for m in movements(t) if m["kind"] == "token" and m["mint"] == DMAGA]
        self.assertEqual(mv, [("o4.11", pool, router, 8_453_336_089_924), ("o4.13", router, buyer, 8_453_336_089_924)])
        rows = parse_tx(t, set(), set(), "mint", {pool})
        self.assertEqual([(r["kind"], r["owner"], r["token_delta"]) for r in rows], [("swap", buyer, 8_453_336_089_924)])

    def test_failed_transaction_moves_nothing(self):
        t = tx("2CSs5czbzHTKmK52")
        self.assertTrue(t["meta"]["err"])
        self.assertEqual(movements(t), [])


@pytest.fixture
def create_payload():
    receipt = json.loads(next(RECEIPTS.glob("5kGaZNhDcm7PaPFAeYhD*.json")).read_text())
    return next(base64.b64decode(line[14:]) for line in receipt["meta"]["logMessages"]
                if line.startswith("Program data: ") and base64.b64decode(line[14:]).startswith(CREATE_EVENT))


def data_line(payload):
    return "Program data: " + base64.b64encode(payload).decode("ascii")


def create_logs(lines, *, program=PUMP, err=None):
    return {"meta": {"err": err, "logMessages": [
        f"Program {program} invoke [1]", *lines, f"Program {program} success",
    ]}}


def damaged_create_line(payload, corruption):
    if corruption == "base64_junk":
        return "Program data: !!" + base64.b64encode(payload).decode("ascii")
    if corruption == "base64_padding":
        return "Program data: A"
    if corruption == "base64_non_ascii":
        return "Program data: é"
    if corruption == "discriminator":
        return data_line(b"BADMAGIC" + payload[8:])
    if corruption == "utf8":
        return data_line(payload[:12] + b"\xff" + payload[13:])
    if corruption == "partial_length":
        return data_line(CREATE_EVENT + b"\x01\x00")
    # Find the URI's length, then the end of the three Borsh strings.
    uri_offset = 8
    for _ in range(2):
        uri_offset += 4 + struct.unpack_from("<I", payload, uri_offset)[0]
    if corruption == "oversized_string":
        return data_line(payload[:uri_offset] + b"\xff" * 4 + payload[uri_offset + 4:])
    keys_offset = uri_offset + 4 + struct.unpack_from("<I", payload, uri_offset)[0]
    return data_line(payload[:keys_offset + (95 if corruption == "short_key" else 0)])


CORRUPT_CREATE = ["discriminator", "base64_junk", "base64_padding", "base64_non_ascii",
                  "utf8", "partial_length", "oversized_string", "missing_keys", "short_key"]


@pytest.mark.parametrize("corruption", CORRUPT_CREATE)
def test_create_event_rejects_invalid_payload(create_payload, corruption):
    assert pump_create_event(create_logs([damaged_create_line(create_payload, corruption)])) is None


@pytest.mark.parametrize("corruption", CORRUPT_CREATE)
def test_create_event_continues_after_unrelated_or_malformed_data(create_payload, corruption):
    expected = pump_create_event(create_logs([data_line(create_payload)]))
    got = pump_create_event(create_logs([damaged_create_line(create_payload, corruption), data_line(create_payload)]))
    assert expected is not None and got == expected


@pytest.mark.parametrize("err", [{"InstructionError": [0, {"Custom": 1}]}, {}])
def test_failed_creation_does_not_emit_an_event(create_payload, err):
    assert pump_create_event(create_logs([data_line(create_payload)], err=err)) is None


@pytest.mark.parametrize("prefix,symbol,mint", [
    ("5kGaZNhDcm7PaPFAeYhD", "KLLARY", "AUS4wtGQZcb6GPQxU4K8FRVqQMwUx2Q8G7K9JKuUpump"),
    ("veJgufrqRRfWvo6fXNeG", "Barron", "HmAgiwjjP9CXqK5wQNsHKtjAt2CH3Kv8Q7xH5kGL2nqZ"),
])
def test_historical_create_event_is_preserved(prefix, symbol, mint):
    receipt = json.loads(next(RECEIPTS.glob(prefix + "*.json")).read_text())
    event = pump_create_event(receipt)
    assert (event["symbol"], event["mint"]) == (symbol, mint)


def test_create_event_ignores_other_program_and_accepts_later_pump_event(create_payload):
    line = data_line(create_payload)
    foreign = create_logs([line], program=OTHER)
    assert pump_create_event(foreign) is None
    foreign["meta"]["logMessages"] += create_logs([line])["meta"]["logMessages"]
    assert pump_create_event(foreign)["symbol"] == "KLLARY"


def test_create_event_requires_complete_invocation_context(create_payload):
    line = data_line(create_payload)
    assert pump_create_event({"meta": {"err": None, "logMessages": [line]}}) is None
    assert pump_create_event({"meta": {"err": None, "logMessages": [f"Program {PUMP} invoke [1]", line]}}) is None


def test_create_event_from_other_callee_is_not_a_pump_event(create_payload):
    tx = create_logs([f"Program {OTHER} invoke [2]", data_line(create_payload), f"Program {OTHER} success"])
    assert pump_create_event(tx) is None


def test_create_event_from_successful_pump_cpi_is_accepted(create_payload):
    tx = create_logs([f"Program {PUMP} invoke [2]", data_line(create_payload), f"Program {PUMP} success"], program=OTHER)
    assert pump_create_event(tx)["symbol"] == "KLLARY"


def test_create_event_from_failed_pump_cpi_is_discarded(create_payload):
    tx = create_logs([f"Program {PUMP} invoke [2]", data_line(create_payload), f"Program {PUMP} failed: custom error"], program=OTHER)
    assert pump_create_event(tx) is None


def test_create_event_is_discarded_when_ancestor_cpi_fails(create_payload):
    system = "11111111111111111111111111111111"
    tx = create_logs([
        f"Program {system} invoke [2]", f"Program {PUMP} invoke [3]", data_line(create_payload),
        f"Program {PUMP} success", f"Program {system} failed: custom error",
    ], program=OTHER)
    assert pump_create_event(tx) is None


if __name__ == "__main__":
    unittest.main()
