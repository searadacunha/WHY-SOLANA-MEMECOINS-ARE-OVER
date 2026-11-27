"""Autocontrôle hors ligne des affirmations de FINDINGS.md : reçus figés (evidence/receipts) et transferts KEKIUS Ethereum
(data/eth_kekius_transfers.csv.gz, data/eth_kekius_pool_weth.csv.gz). Aucun accès réseau.

Lancer : python -m unittest discover -s investigations/2026-11-06_dmaga_kekius_cross_token/tests -v"""
import csv
import datetime as dt
import gzip
import json
import sys
import unittest
from collections import defaultdict
from pathlib import Path

INV = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(INV / "scripts"))
from k11_parse import signers, sol_deltas, token_deltas  # noqa: E402

REC = INV / "evidence" / "receipts"
KM = "HuAncxDEsakCDgZS2Yfo9xJbHmtHXMnxxkT9jqdXnHhm"
XC = "XC78JjRHnSqaysrHiTrhR8eRngFbvX3rrHyRjWEpump"
DMAGA = "7D7BRcBYepfi77vxySapmeqRNN1wsBBxnFPJGbH5pump"
SNIPER_PROGRAM = "9NLjj4Gj2fEYhujN7znkiLTVjDsiKi7h1mQvMdEffDTw"
GO5 = "Go5rFkwKpTYGVck7emf4Uop81HBozmHHZfEhe2zJDY5u"
ETH_KEKIUS = "0x26e550ac11b26f78a04489d5f20f24e3559f7dd9"
T_MUSK = 1735624921  # 2024-12-31 06:02:01 UTC, borne basse du changement de nom


def rec(sig):
    return json.loads((REC / f"{sig}.json").read_text())


def utc(t):
    return dt.datetime.fromtimestamp(t, dt.UTC).strftime("%Y-%m-%d %H:%M:%S")


def progs(t):
    return {i.get("programId") for i in t["transaction"]["message"]["instructions"]}


class Solana(unittest.TestCase):
    def test_creations(self):
        km = rec("51W3rg9BpBtWXTTcoRhB3akNPXUpPq9XnkjkDyHV7hCS7wR6MU8U9pnYGUWFW4qBW68iFhSHTxGRCELi8NEcxFsK")
        self.assertEqual(utc(km["blockTime"]), "2024-12-10 07:29:00")
        self.assertEqual(signers(km)[0], "4GUgVRftPkeqTNFc7nwZVRjqheBPMVToAhNYdkQVUz3e")
        self.assertEqual(token_deltas(km, KM)["4GUgVRftPkeqTNFc7nwZVRjqheBPMVToAhNYdkQVUz3e"], 104_000_000 * 10**6)
        xc = rec("2xz9tgPBSztVPE6voEL8yKCFv37qUyojVUtEA1Uab4FzeJtDpi6ePPCpsFUzfhKfLTVrPuzpdYFLyk8dojREBq7D")
        self.assertEqual((utc(xc["blockTime"]), xc["slot"]), ("2024-12-29 16:33:45", 310594124))
        self.assertEqual(signers(xc)[0], "9dtGg97QAfxc2UF4LGaxLzYdB4MJpnNMK7Y2iUwGidoy")
        mig = rec("5wEA4w1XUd987pABFyXYujoCKHJkJ1VSKwaD3bKxgBKy8xeBJ9j4uMvDc6Y5gkDfMfuz2MyhoMwoSjuwsAwPRSiZ")
        self.assertEqual(utc(mig["blockTime"]), "2024-12-29 16:36:01")
        self.assertEqual(utc(rec("BA2V9YnMrWxk1PyF1ty6mNpg4Yu8y244YdH3QbcBBHyyMyniuit5fT8L4vLpjdKwgksxJtLRMxfGMQ8UeSzQJAR")["blockTime"]),
                         "2024-12-10 07:31:01")

    def test_go5_buy_then_split_to_ten_wallets(self):
        buy = rec("5p39GsYPf4zwCMRdLV8iJrqtHjcQw8VtPAP6oYugqCF3oyj98JEFXg7VT78uPpJWhxxKWHDWGsENG1ndDRuAjhST")
        self.assertEqual(buy["slot"], 310594124)
        self.assertEqual(token_deltas(buy, XC)[GO5], 748_786_277_680_244)
        self.assertEqual(sol_deltas(buy)[GO5], -70_031_366_319)
        sell = rec("5GvjoEMEiPfjqnck7iegRCGuKUrtfe1amJYvvR6D7WxrcPWA19peM163vuEQuorCZDFpYHmknUJ5TDSnPxHfYBxn")
        self.assertEqual(signers(sell), [GO5])
        self.assertEqual(token_deltas(sell, XC)[GO5], -748_786_277_680_244)
        sd = sol_deltas(sell)
        ten = {a for a, v in sd.items() if v == 6_655_700_950}
        self.assertEqual(len(ten), 10)
        self.assertEqual(sd[GO5], 2_061_527_511)
        # Les 10 bénéficiaires achètent dans le même slot, dans 3 des 4 tx co-signées
        idx = json.loads((REC / "INDEX.json").read_text())
        bundles = [rec(s) for s, why in idx.items() if "co-signé" in why]
        self.assertEqual(len(bundles), 4)
        owners = set()
        for t in bundles:
            self.assertEqual(t["slot"], 310594130)
            self.assertEqual(len(signers(t)), 4)
            owners |= {a for a, v in token_deltas(t, XC).items() if v > 0}
        self.assertEqual(len(owners), 16)
        self.assertTrue(ten <= owners)
        bought = sum(v for t in bundles for a, v in token_deltas(t, XC).items() if v > 0)
        self.assertEqual(round(bought / 1e12, 2), 673.91)

    def test_bot_operator_link_dmaga_xc78(self):
        tr = rec("4dChb1EMrLFYNpDx9iWAtKzXde1VeGoxGF6LQ8kTDpE6FX8WMrFr7y2VYTJyqbtoJM1sY4yKxoDMs24Nu1EgiAyV")
        self.assertEqual(utc(tr["blockTime"]), "2024-07-11 13:10:39")
        self.assertEqual(sol_deltas(tr)["FJkb8WnWocfuQYj4v4vg5VpZoST3LebjQk8WpuD7VbgC"], 1_474_847_595)
        self.assertEqual(signers(tr), ["DQmMnakiKr1YNE2gcpggLCzBrauBwFbQkAaao2FTbjgp"])
        dm = rec("meMfnP6CTuwsCquuMzwqVYLUovQL3mc9MfjYNGRYscgxtdfyv5NYMCUJ2K2RL5WuXnpJuTNL6jgmJ8rTrNdmiWp")
        self.assertEqual(utc(dm["blockTime"]), "2024-07-14 02:15:33")
        self.assertIn(SNIPER_PROGRAM, progs(dm))
        xc = rec("5xqzEckQ4aC7KEPiPRRPPvigz7TihYxvt9aSFYRNJ1H54e1swR5uceJ6yPLhVaXxdBfvW8ktyDPPMbcCAzCvPd3Z")
        self.assertEqual(utc(xc["blockTime"]), "2024-12-29 16:36:52")
        self.assertIn(SNIPER_PROGRAM, progs(xc))
        init = rec("3hpRnD1mQ9LwfjkdwMFoP7RX2aEp3Z3GJoA9ipriyQGPKrs3v7bdj2bvwLLRNXcfBSwuqG5r55GqMvSNz7tTi5RR")
        self.assertEqual(xc["blockTime"] - init["blockTime"], 1)

    def test_xc78_operator_funding(self):
        idx = json.loads((REC / "INDEX.json").read_text())
        ops = "3oqARBNDr56L2oWQ9aR2QzS7FeTMEubd8J2v29wP5N58"
        got = {}
        for sig, why in idx.items():
            if "3oqARBND" in why:
                t = rec(sig)
                got[utc(t["blockTime"])] = sol_deltas(t)
        self.assertEqual(got["2024-12-29 16:31:42"][GO5], 70_060_000_000)
        self.assertEqual(got["2024-12-30 11:26:46"][ops], 11_916_477_761)
        self.assertEqual(got["2024-12-30 18:21:24"][ops], 1_975_732_039)
        self.assertEqual(got["2024-12-23 19:14:41"][ops], 86_082_111_120)
        fee = "C6UEzXJcTqqJHpAGUts2tA4s6E7MS5KoPzzfsrT6qCpL"
        r1 = got["2024-12-30 11:26:46"][fee] / got["2024-12-30 11:26:46"][ops]
        r2 = got["2024-12-30 18:21:24"][fee] / got["2024-12-30 18:21:24"][ops]
        self.assertEqual((round(r1 * 100, 3), round(r2 * 100, 3)), (6.957, 6.961))


class Ethereum(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.T = list(csv.DictReader(gzip.open(INV / "data" / "eth_kekius_transfers.csv.gz", "rt")))

    def test_creation_and_open_trading(self):
        first = self.T[0]
        self.assertEqual((first["block"], first["from"], int(first["raw"])),
                         ("21397776", "0x" + "0" * 40, 10**18))
        self.assertEqual(utc(int(first["time"])), "2024-12-14 02:29:35")
        lp = [r for r in self.T if r["to"] == "0xfff8d5fff6ee3226fa2f5d7d5d8c3ff785be9c74" and r["block"] == "21397848"]
        self.assertEqual(int(lp[0]["raw"]), 790_000_000 * 10**9)

    def test_no_dmaga_evm_wallet_in_kekius(self):
        # Adresses complètes relues dans investigations/2026-11-05_evm-recipient-deeptrace (comptage d'occurrences),
        # sosies d'empoisonnement (0xb947c5c6…, 0xb29875ef…) exclus.
        dmaga_evm = {"0xb947bf7f409e998b28f8e218802fc9575c3c8c57", "0xb29826d809aa04d2ead6f2310d8965a45b87fa67",
                     "0x86f99097c563e84dd5190f3e85f6a2988f1c47a5", "0x2d86499a410a9ac2139833ba8d6942b8a8700a7b",
                     "0x4978cd7e5a3565cafcc88a105940b0ea01adc04d"}
        deeptrace = (INV.parent / "2026-11-05_evm-recipient-deeptrace" / "FINDINGS.md").read_text().lower()
        for a in dmaga_evm:
            self.assertIn(a, deeptrace + (INV.parent / "2026-11-05_evm-recipient-deeptrace" / "evidence" / "relay_4978_history.csv").read_text().lower())
        seen = {r["from"] for r in self.T} | {r["to"] for r in self.T}
        self.assertFalse(dmaga_evm & seen)

    def test_0x33a5_pre_event(self):
        import k32_eth_wallets as k
        rows, _ = k.ledger()
        q = [r for r in rows if r["owner"] == "0x33a57f4e88c9ceb0788eb41a407e51533d70cc4d"]
        pre = [r for r in q if r["kind"] == "buy" and r["time"] < T_MUSK]
        self.assertEqual(len(pre), 7)
        self.assertEqual(round(sum(r["kekius_raw"] for r in pre) / 1e15, 4), 8.4482)
        self.assertEqual(round(-sum(r["eth_wei"] for r in pre) / 1e18, 4), 16.0)
        self.assertEqual(utc(min(r["time"] for r in pre)), "2024-12-19 07:55:47")
        sells = [r for r in q if r["kind"] == "sell" and T_MUSK <= r["time"] < 1735948800]
        self.assertEqual(round(sum(r["eth_wei"] for r in sells) / 1e18, 2), 285.71)
        self.assertEqual(utc(min(r["time"] for r in sells)), "2025-01-01 07:34:47")


class Tables(unittest.TestCase):
    def test_funding_graph_ethereum_rows_match_sources(self):
        hist = {}
        for f in (INV / "data" / "eth_history").glob("*.csv"):
            for r in csv.DictReader(open(f)):
                hist.setdefault(r["tx"], []).append(r)
        bs = {t["hash"].lower(): t for t in json.loads((INV / "evidence" / "blockscout_0xecaa5a79_outgoing.json").read_text())["items"]}
        n = 0
        for r in csv.DictReader(open(INV / "FUNDING_GRAPH.csv")):
            if r["chain"] != "ethereum":
                continue
            n += 1
            if r["tx_or_signature"] in hist:
                h = [x for x in hist[r["tx_or_signature"]] if x["kind"] == "tx"][0]
                self.assertEqual((h["from"], h["to"], h["time_utc"]), (r["src"], r["dst"], r["utc"]))
                self.assertAlmostEqual(float(h["amount"]), float(r["amount"]), places=6)
            else:
                b = bs[r["tx_or_signature"]]
                self.assertEqual((b["from"]["hash"].lower(), b["to"]["hash"].lower()), (r["src"], r["dst"]))
                self.assertEqual(b["timestamp"][:19].replace("T", " "), r["utc"])
                self.assertAlmostEqual(int(b["value"]) / 1e18, float(r["amount"]), places=6)
        self.assertEqual(n, 13)


if __name__ == "__main__":
    unittest.main()
