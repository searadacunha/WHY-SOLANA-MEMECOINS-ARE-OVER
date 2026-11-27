"""Régression du décodeur SPL qui préserve le mint (dmaga.spl, issue #27), sur des transactions réelles figées."""
import json
import unittest
from pathlib import Path

from dmaga.spl import keys, movements, token_accounts

FIX = Path(__file__).resolve().parent / "fixtures" / "spl"
DMAGA = "7D7BRcBYepfi77vxySapmeqRNN1wsBBxnFPJGbH5pump"
WSOL = "So11111111111111111111111111111111111111112"
W7GVC = "7GVCZAYG5NfiJsuqUdvc9hB2ts2W3tSrGdya4CyR1M5j"
W9SXM = "9Sxmf25WG5WVQ5p86ycWeo5hMEwxiWPkFtLdRdTrHSQS"


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


if __name__ == "__main__":
    unittest.main()
