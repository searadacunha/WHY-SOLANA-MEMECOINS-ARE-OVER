"""Tests hors ligne du rejeu historique : chaque chiffre clé de FINDINGS.md est recalculé depuis les reçus figés et les tables.

Bibliothèque standard seulement (python -I). Aucun réseau, aucune clé."""
import csv
import json
import sys
import unittest
from pathlib import Path

INV = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(INV / "scripts"))
from h_decode import movements, pump_create_event, signers, sol_delta, token_delta, keys  # noqa: E402

REC = INV / "evidence" / "receipts"
DATA = INV / "data"
W7GVC = "7GVCZAYG5NfiJsuqUdvc9hB2ts2W3tSrGdya4CyR1M5j"
W9SXM = "9Sxmf25WG5WVQ5p86ycWeo5hMEwxiWPkFtLdRdTrHSQS"
DMAGA = "7D7BRcBYepfi77vxySapmeqRNN1wsBBxnFPJGbH5pump"
T_CREATE = 1720922725


def receipt(prefix):
    hit = [p for p in REC.glob(f"{prefix}*.json")]
    assert len(hit) == 1, (prefix, hit)
    return json.loads(hit[0].read_text())


def rows(name):
    with (DATA / name).open() as f:
        return list(csv.DictReader(f))


class Jeffro(unittest.TestCase):
    def test_190_sol_is_own_perps_position_close(self):
        t = receipt("44Sd6xet31me1Hc1")
        self.assertEqual(sol_delta(t, W7GVC), 189_656_068_999)
        self.assertEqual(T_CREATE - t["blockTime"], 33 * 60 + 14)
        self.assertNotIn(W7GVC, signers(t))  # exécuté par un keeper
        self.assertIn("PERPHjGBqRHArX4DySjwM6UJHiR3sWAatqfdBS2qQJu", {ix.get("programId") for ix in t["transaction"]["message"]["instructions"]})
        close = [m for m in movements(t) if m["kind"] == "close" and m["dst"] == W7GVC]
        self.assertEqual([m["amount"] for m in close], [189_653_006_599])
        claim = next(r for r in rows("jeffro_claims.csv") if r["id"] == "C1")
        for s in claim["signatures"].split(";")[1:]:  # demandes de clôture : signées par 7GVC
            self.assertIn(W7GVC, signers(receipt(s[:16])))

    def test_pumpfun_buys_and_20m_transfer(self):
        claim = {r["id"]: r for r in rows("jeffro_claims.csv")}
        buys = [receipt(s[:16]) for s in claim["C2"]["signatures"].split(";")]
        self.assertEqual(sum(token_delta(t, W7GVC, DMAGA) for t in buys), 41_197_138_380_017)
        t = receipt(claim["C3"]["signatures"][:16])
        mv = [m for m in movements(t) if m["kind"] == "token" and m["mint"] == DMAGA]
        self.assertEqual([(m["src"], m["dst"], m["amount"], m["authority"]) for m in mv], [(W7GVC, W9SXM, 20_000_000_000_000, W7GVC)])
        self.assertEqual(t["blockTime"] - max(b["blockTime"] for b in buys), 11 * 60 + 26)

    def test_satellites_funded_by_7gvc_with_jeffro_amounts(self):
        for r in rows("jeffro_satellites.csv"):
            got = 0
            for s in r["funding_signatures"].split(";"):
                got += sum(m["amount"] for m in movements(receipt(s[:16])) if m["kind"] == "sol" and m["src"] == W7GVC and m["dst"] == r["address"])
            self.assertEqual(got, int(r["jeffro_sol"]) * 10**9, r["abbr"])
            self.assertTrue(r["address"].startswith(r["abbr"][:4]) and r["address"].endswith(r["abbr"][-4:]))


class Noah(unittest.TestCase):
    def test_no_direct_edge_between_groups(self):
        e = rows("noah_edges.csv")
        self.assertGreater(len(e), 100)
        self.assertEqual([r for r in e if r["same_group"] != "True"], [])

    def test_dmaga_edges_match_receipts(self):
        n = 0
        for r in rows("noah_edges.csv"):
            if r["asset"] == "DMAGA" and r["source_table"] in ("tx_balances", "token_direct"):
                t = receipt(r["signature"][:16])
                self.assertEqual(token_delta(t, r["dst"], DMAGA), round(float(r["amount"]) * 10**6), r["signature"])
                n += 1
        self.assertGreaterEqual(n, 10)

    def test_holdings_verified_on_chain_and_max_entity(self):
        v = rows("noah_holdings_verified.csv")
        self.assertEqual(len(v), 15)
        self.assertTrue(all(abs(float(r["diff_vs_trades"])) < 1e-6 for r in v))
        g2 = sum(float(r["onchain_ata_balance"]) for r in v if r["group"] == "2")
        self.assertAlmostEqual(100 * g2 / 1e9, 6.751, places=3)  # Noah : 6,73 % au plus par entité

    def test_fixed_price_vendor_payments(self):
        pay = [r for r in rows("counterparty_HBsgbpsM1j1YsNYqtCXcFU4mCRofwcor2qFwifNqddmH.csv") if r["dir"] == "in"]
        usdc = [r for r in pay if r["mint"].startswith("EPjF")]
        self.assertEqual([int(r["amount_raw"]) for r in usdc], [700_000_000])
        payers = {r["counterparty"] for r in pay}
        self.assertTrue({W7GVC, W9SXM, "7mdCAs8CWYJxkWz2gfj3sRhDBmUi6Q9qvRGuKiv2Bazu"} <= payers)
        self.assertGreaterEqual(len(payers), 10)


class Others(unittest.TestCase):
    def test_plain_transfer_lacks_mint_account(self):
        t = receipt("58SeigZv41h2")
        self.assertNotIn(DMAGA, keys(t))
        self.assertEqual(token_delta(t, "AtZjv3DuV9cLn3Jxm72TMSdTN4aM6CrBaGyxUC4c2wDk", DMAGA), 13_193_693_055_782)

    def test_kllary_create_event(self):
        ev = pump_create_event(receipt("5kGaZNhDcm7PaPFAeYhD"))
        self.assertEqual((ev["symbol"], ev["mint"]), ("KLLARY", "AUS4wtGQZcb6GPQxU4K8FRVqQMwUx2Q8G7K9JKuUpump"))

    def test_gxzvx_last_three_sells(self):
        g = "GXZvXsD6hxaLeFvQisWpdAwsayJxga7w9EeafhFZG2Ra"
        ts = [receipt(p) for p in ("29NFuxQwFq", "2WJ1MmWWsr", "521vdgUCSk")]
        self.assertEqual([t["blockTime"] for t in ts], sorted(t["blockTime"] for t in ts))
        self.assertLessEqual(ts[-1]["blockTime"] - ts[0]["blockTime"], 74)
        self.assertTrue(all(token_delta(t, g, DMAGA) < 0 for t in ts))

    def test_rotation_counts(self):
        r = rows("rotation_retiredio.csv")
        test = [x for x in r if x["set"] == "dmaga_buyer_biden_to_low"]
        ctl = [x for x in r if x["set"] == "dmaga_buyer_winig_to_biden"]
        self.assertEqual((sum(x["rotation"] == "True" for x in test), sum(x["rotation"] == "True" for x in ctl)), (11, 4))
        a = rows("ata_retiredio.csv")
        self.assertEqual((sum(x["set"] == "dmaga_buyer_biden_to_low" for x in a), sum(x["set"] == "dmaga_buyer_winig_to_biden" for x in a)), (35, 149))


class H3QsAndCircuit(unittest.TestCase):
    def test_joe_to_dmaga_rotation(self):
        h3 = "H3QsBrrivimFJmSpTXuvig2n1Bh7JuYxrriRSEszT6cc"
        r = next(x for x in rows("h3qs_rotations.csv") if x["bought_mint"] == DMAGA and x["sold_mint"].startswith("JoeX"))
        sell, buy = receipt(r["sell_signature"][:20]), receipt(r["buy_signature"][:20])
        self.assertLess(token_delta(sell, h3, r["sold_mint"]), 0)
        self.assertGreater(token_delta(buy, h3, DMAGA), 0)
        self.assertEqual(buy["blockTime"] - sell["blockTime"], 23)

    def test_first_activity_signed_by_7gvc_and_9sxm(self):
        for pre, src, dst in (("4UiQXVF3UAkRVbmw", W9SXM, "6QFDe4yu9mVhv3cbbaMtkTnakz4bGJLAjLjhwrMn5jqD"),
                              ("4pcw28aApDZVvvJR", W7GVC, "AeiMit5PMUvdJSsa8jm2RpHJCdfJLFyW6dzkm65w1ybh")):
            t = receipt(pre)
            self.assertEqual(signers(t), [src])
            self.assertTrue(any(m["kind"] == "token" and m["src"] == src and m["dst"] == dst for m in movements(t)))


class Pass3(unittest.TestCase):
    def test_9sxm_1_8m_sale_is_17_875_sol_gross(self):
        t = receipt("2PHU4HTSGRJ6xKncBiVm")
        self.assertEqual(token_delta(t, W9SXM, DMAGA), -1_800_000_000_000)
        gross = sum(m["amount"] for m in movements(t) if m["kind"] == "token" and m["src"] == "5Q544fKrFoe6tsEbD7S8EmxGTJYAKtTVhAW5Q5pge4j1")
        self.assertEqual(gross, 17_874_608_396)
        self.assertEqual(round(gross / 1e9, 3), 17.875)

    def test_barron_creation_and_no_shared_movement(self):
        ev = pump_create_event(receipt("veJgufrqRRfWvo6fXNeG"))
        self.assertEqual((ev["symbol"], ev["mint"], ev["user"]),
                         ("Barron", "HmAgiwjjP9CXqK5wQNsHKtjAt2CH3Kv8Q7xH5kGL2nqZ", "3DLBntwLgbHx1HsLqJGKqhNtyHbuuoLWet2xhhcTvRuC"))
        shared = movements(receipt("3wFx6C1HXs1PuKcMQVsj"))
        creators = {"3DLBntwLgbHx1HsLqJGKqhNtyHbuuoLWet2xhhcTvRuC", "8YLEuUtZ4eFMJbf46oNb1CeG6dYFWGyxnQSh9hrgzBzR"}
        self.assertEqual([m for m in shared if {m["src"], m["dst"]} & creators], [])

    def test_6qfd_display_by_truncation(self):
        r = json.loads((DATA / "pass3_tests.json").read_text())["L01_6QFD"]
        self.assertEqual(r["ata_txs_21_07_to_noah"], 0)
        self.assertTrue(r["display_15_3M_1_53pct_by_truncation"])


class NoInventedAddress(unittest.TestCase):
    def test_every_address_in_findings_exists_in_evidence(self):
        import re
        text = (INV / "FINDINGS.md").read_text()
        cited = set(re.findall(r"`([1-9A-HJ-NP-Za-km-z]{32,44})`", text))
        pool = "".join(p.read_text() for p in list(DATA.glob("*.csv")) + list(DATA.glob("*.json")) + list(REC.glob("*.json")))
        missing = sorted(a for a in cited if a not in pool)
        self.assertEqual(missing, [])
        sigs = set(re.findall(r"`([1-9A-HJ-NP-Za-km-z]{86,88})`", text))
        self.assertGreaterEqual(len(sigs), 10)
        self.assertEqual(sorted(x for x in sigs if x not in pool), [])


class XProvenance(unittest.TestCase):
    def test_every_metadata_mismatch_is_a_repost(self):
        s = json.loads((DATA / "x_reconcile_summary.json").read_text())
        self.assertEqual(s["metadata_disagree_explained_by_repost"], s["metadata_snowflake_disagree"])

    def test_timeline_cites_no_repost(self):
        rep = {r["requested_id"] for r in rows("x_observations_reconciled.csv") if r["relation"] == "repost"}
        import re
        cited = set(re.findall(r"\| id (\d{18,19}),", (INV.parents[1] / "docs" / "TIMELINE.md").read_text()))
        self.assertTrue(cited)
        self.assertEqual(cited & rep, set())


if __name__ == "__main__":
    unittest.main()
