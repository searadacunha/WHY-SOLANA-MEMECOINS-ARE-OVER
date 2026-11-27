"""Tests hors ligne du dossier, depuis un clone neuf : seules les fixtures publiées (evidence/fixtures/) sont lues.
Le réseau est coupé pendant les tests. Usage : python -m unittest discover -s <ce dossier> -v"""
import contextlib, copy, csv, gzip, hashlib, io, json, os, socket, subprocess, sys, tempfile, unittest
from unittest import mock
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
SCRIPTS = ROOT / "scripts"
FIX = ROOT / "evidence" / "fixtures"
os.environ["DMAGA_NT_RAW"] = tempfile.mkdtemp(prefix="dmaga_nt_raw_")  # cache local vide : rien d'autre que les fixtures
os.environ["DMAGA_NT_RAW_RO"] = ""
sys.path.insert(0, str(SCRIPTS))

def _no_net(*a, **k): raise OSError("réseau coupé pendant les tests")
socket.socket.connect = _no_net

import nt_lib as N            # noqa: E402
import dln_orderid as O       # noqa: E402
import s13_orderid_check as C # noqa: E402
import s60_positions as P     # noqa: E402

EI5 = N.EI5
def rd(p): return list(csv.DictReader(open(p)))
def sol(w): return [json.loads(l) for l in (FIX / "sol" / f"{w}.jsonl").read_text().splitlines()]

def keys_of(t):
    ks = [k["pubkey"] if isinstance(k, dict) else k for k in t["transaction"]["message"]["accountKeys"]]
    la = t["meta"].get("loadedAddresses") or {}
    return ks + la.get("writable", []) + la.get("readonly", [])

def sol_delta(t, w):
    ks = keys_of(t)
    return t["meta"]["postBalances"][ks.index(w)] - t["meta"]["preBalances"][ks.index(w)] if w in ks else 0

def tok_delta(t, w, mint):
    m = t["meta"]; s = 0
    for side, sg in (("preTokenBalances", -1), ("postTokenBalances", 1)):
        for b in m.get(side) or []:
            if b.get("owner") == w and b["mint"] == mint: s += sg * int(b["uiTokenAmount"]["amount"])
    return s

def sig(t): return t["transaction"]["signatures"][0]


class Fixtures(unittest.TestCase):
    def test_manifest(self):
        man = json.loads((FIX / "MANIFEST.json").read_text())
        for part in man.values():
            for rel, meta in part.items():
                b = (FIX / rel).read_bytes()
                self.assertEqual(hashlib.sha256(b).hexdigest(), meta["sha256"], rel)

    def test_no_machine_path(self):
        for p in list(SCRIPTS.glob("*.py")) + list(HERE.glob("*.py")):
            s = p.read_text()
            for bad in ("/Vol" + "umes/", "/Us" + "ers/"): self.assertNotIn(bad, s, p.name)


class OrderId(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.receipts = C.receipts()
        cls.events = [event for receipt in cls.receipts.values() for event in C.check(receipt)]
        cls.links = C.read_csv(ROOT / "CROSSCHAIN_LINKS.csv")
        cls.solana = C.solana_receipts()
        cls.index = C.read_csv(N.DEB_RECEIVERS)

    def validate(self, links=None, events=None, solana=None, index=None):
        return C.validate_links(self.links if links is None else links,
                                self.events if events is None else events,
                                self.solana if solana is None else solana,
                                self.index if index is None else index)

    def test_keccak(self):
        self.assertEqual(O.keccak256(b"").hex(), "c5d2460186f7233c927e7db2dcc703c0e500b653ca82273b7bfad8045d85a470")
        self.assertEqual(O.keccak256(b"abc").hex(), "4e03657aea45a94fc7d47ba826c8d667c0d1e6e33a64a036ec44f58fa12d6c45")

    def test_links_authenticated_by_orderid(self):
        self.assertEqual(len(self.events), 123)
        self.assertEqual(self.validate(), dict(links=88, src_evm_receipts=78, dst_evm_receipts=45,
                         src_solana_receipts=9, dst_solana_receipts=43, src_solana_index_only=1))

    def test_each_order_field_is_bound_to_the_receipt(self):
        for field, value in (("src_chain", "bsc"), ("dst_chain", "bsc"),
                             ("maker", "0x" + "1" * 40), ("receiver", "0x" + "1" * 40),
                             ("give_token", "0x" + "1" * 40), ("take_token", "0x" + "1" * 40),
                             ("give_amount_raw", "1"), ("take_amount_raw", "1")):
            link = dict(self.links[0], **{field: value})
            with self.subTest(field=field), self.assertRaisesRegex(ValueError, "fields mismatch"):
                self.validate(links=[link])

    def test_both_evm_transaction_hashes_are_bound(self):
        for side in ("src", "dst"):
            link = dict(self.links[0], **{side + "_tx": "0x" + "1" * 64})
            with self.subTest(side=side), self.assertRaisesRegex(ValueError, "EVM event"):
                self.validate(links=[link])

    def test_solana_address_case_is_significant(self):
        for side, field in (("src", "maker"), ("dst", "receiver")):
            link = next(dict(k) for k in self.links if k[side + "_chain"] == "solana")
            link[field] = link[field].swapcase()
            with self.subTest(field=field), self.assertRaisesRegex(ValueError, "fields mismatch"):
                self.validate(links=[link])

    def test_evm_hex_address_case_is_not_significant(self):
        link = dict(self.links[0])
        for field in ("maker", "receiver", "give_token", "take_token"):
            link[field] = "0x" + link[field][2:].upper()
        self.assertEqual(self.validate(links=[link])["links"], 1)

    def test_unknown_topic_or_failed_receipt_cannot_authenticate_order(self):
        receipt = next(rc for rc in self.receipts.values() if C.check(rc))
        for kind in ("failed", "topic", "topic_prefix"):
            bad = copy.deepcopy(receipt)
            if kind == "failed":
                bad["status"] = "0x0"
            else:
                for log in bad["logs"]:
                    prefix = log["topics"][0][:10] if kind == "topic_prefix" and log.get("topics") else "0x12345678"
                    log["topics"] = [prefix + "0" * 56]
            with self.subTest(kind=kind):
                self.assertEqual(C.check(bad), [])
                with self.assertRaises(ValueError):
                    self.validate(events=C.check(bad))

    def test_duplicate_order_and_event_are_rejected(self):
        with self.assertRaisesRegex(ValueError, "Duplicate cross-chain"):
            self.validate(links=self.links + [self.links[0]])
        with self.assertRaisesRegex(ValueError, "Duplicate EVM event"):
            self.validate(events=self.events + [self.events[0]])
        with self.assertRaisesRegex(ValueError, "Empty"):
            self.validate(links=[])

    def test_receipt_chain_must_match_recorded_rpc_provenance(self):
        receipt = next(copy.deepcopy(rc) for rc in self.receipts.values() if C.check(rc))
        receipt["_evidence_chain_id"] = 56 if receipt["_evidence_chain_id"] != 56 else 1
        with self.assertRaisesRegex(ValueError, "chain provenance"):
            C.check(receipt)
        with self.assertRaisesRegex(ValueError, "chain provenance"):
            C.request_chain("unknown eth_getTransactionReceipt []")

    def test_missing_raw_solana_receipt_is_not_silently_downgraded(self):
        link = next(k for k in self.links if k["src_chain"] == "solana" and k["src_tx"] in self.solana)
        solana = {key: tx for key, tx in self.solana.items() if key != link["src_tx"]}
        with self.assertRaisesRegex(ValueError, "Missing src Solana evidence"):
            self.validate(solana=solana)

    def test_index_only_source_requires_exact_index_match(self):
        link = next(k for k in self.links if k["orderId"] in C.INDEX_ONLY_SOURCES)
        with self.assertRaisesRegex(ValueError, "Missing src Solana evidence"):
            self.validate(links=[link], index=[])
        bad = dict(link, src_tx="invented")
        with self.assertRaisesRegex(ValueError, "Missing src Solana evidence"):
            self.validate(links=[bad])

    def test_failed_solana_fill_cannot_prove_destination(self):
        link = next(k for k in self.links if k["dst_chain"] == "solana")
        receipt = copy.deepcopy(self.solana[link["dst_tx"]])
        receipt["meta"]["err"] = {"InstructionError": [0, "Custom"]}
        with self.assertRaisesRegex(ValueError, "successful dst Solana"):
            self.validate(links=[link], solana={link["dst_tx"]: receipt})

    def test_wrong_solana_signature_or_amount_is_rejected(self):
        link = next(k for k in self.links if k["dst_chain"] == "solana")
        receipt = copy.deepcopy(self.solana[link["dst_tx"]])
        receipt["transaction"]["signatures"][0] = "invented"
        with self.assertRaisesRegex(ValueError, "Wrong dst Solana receipt"):
            self.validate(links=[link], solana={link["dst_tx"]: receipt})
        receipt = copy.deepcopy(self.solana[link["dst_tx"]])
        key = keys_of(receipt).index(link["receiver"])
        receipt["meta"]["postBalances"][key] += 1
        with self.assertRaisesRegex(ValueError, "amount mismatch"):
            self.validate(links=[link], solana={link["dst_tx"]: receipt})

    def test_cli_is_read_only_by_default_and_fails_nonzero(self):
        with mock.patch.object(sys, "argv", ["s13_orderid_check.py"]), \
                mock.patch.object(N, "write_csv") as write, contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(C.main(), 0)
            write.assert_not_called()
        bad = dict(self.links[0], dst_tx="0x" + "1" * 64)
        with mock.patch.object(sys, "argv", ["s13_orderid_check.py"]), \
                mock.patch.object(C, "read_csv", return_value=[bad]), \
                contextlib.redirect_stderr(io.StringIO()) as error:
            self.assertEqual(C.main(), 1)
            self.assertIn("Validation failed", error.getvalue())


class Positions(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        txs = P.per_tx(rd(ROOT / "data/base_0xb298_ledger.csv"), N.B298); taint = P.fill_taint()
        rows, cls.bk = P.run(txs, taint, min(t["ts"] for t in txs if t["tx"] in taint))
        cls.res = {t["tx"]: t["res"] for t in rows}

    def lo(self, tx, asset=P.ETH): return self.res[tx][asset][1]

    def test_coinbase_24_eth(self):
        # s50 donnait 23,748588577 ETH : sa borne portait sur la valeur et les frais de la tx ; celle des 24 ETH seuls est 23,748588117
        self.assertEqual(self.res["0x52da33cb31aa36ecce1a05774dd7bc69bed8d0a9b555db97e8659771a4a00245"][P.ETH][0], 24 * 10 ** 18)
        self.assertEqual(self.lo("0x52da33cb31aa36ecce1a05774dd7bc69bed8d0a9b555db97e8659771a4a00245") // 10 ** 9, 23748588117)

    def test_blofin_order_now_bounded(self):
        self.assertGreaterEqual(self.lo("0x81888303b2bab106e4fe8e6e7cd17ffa4107b5ccfc2f2b0310bd401f8d9dedb2"), 1154 * 10 ** 15)

    def test_poison_tokens_isolated(self):
        self.assertEqual(len(self.bk.broken), 4)
        self.assertNotIn(P.ETH, self.bk.broken); self.assertNotIn(P.USDC_BASE, self.bk.broken)


class SolanaReplay(unittest.TestCase):
    DMAGA = "7D7BRcBYepfi77vxySapmeqRNN1wsBBxnFPJGbH5pump"

    def test_complete_histories_continuous(self):
        """Chaque historique complet publié est continu : solde après une tx = solde avant la suivante."""
        man = json.loads((FIX / "MANIFEST.json").read_text())["sol"]
        for rel, meta in man.items():
            if not meta["complete_history"]: continue
            w = Path(rel).stem; T = sorted(sol(w), key=lambda t: (t["slot"], t.get("transactionIndex") or 0)); prev = 0
            for t in T:
                ks = keys_of(t)
                if w not in ks: continue
                i = ks.index(w); self.assertEqual(t["meta"]["preBalances"][i], prev, (w, sig(t))); prev = t["meta"]["postBalances"][i]

    def test_sale_wallets_return_to_ei5(self):
        for w, src, n in [("8kNKNiHKjbCPjaWGjoEEWeQ6X4jkZn2sDV7tz7azfL4t", "HGBiExZRtD2TZdQLWHE9azkTSmE2z7ygKqZMtehJDKYU", 3 * 10 ** 12),
                          ("BdX9J5pQZ9SoH7PqwDCiiQ2rzaMiT4D9WZ8C1DiwXgyX", "Gcyg2jeLfSY9gxxHf5za5QU74ijtxBb1dB2mdGSPZH3m", 27 * 10 ** 11)]:
            T = sol(w)
            self.assertEqual(sum(tok_delta(t, w, self.DMAGA) for t in T if tok_delta(t, w, self.DMAGA) > 0), n)
            self.assertEqual(sum(tok_delta(t, w, self.DMAGA) for t in T), 0)       # tout le DMAGA reçu est sorti
            self.assertEqual(T[-1]["meta"]["postBalances"][keys_of(T[-1]).index(w)], 0)
            self.assertIn(EI5, keys_of(T[0]) + keys_of(T[1]))

    def test_coinbase_deposit_shared_by_ei5_and_hp2(self):
        """39dTXaMM : deux entrées (Ei5yGz8d, Hp2BtvnZ), chacune balayée par l'adresse elle-même vers Coinbase 1 ou 3 (Dune)."""
        w = "39dTXaMMMy4AV6jhihEmfqdnAkhpwCpYpz9SnvP3y1h7"; T = sorted(sol(w), key=lambda t: t["slot"])
        self.assertEqual([keys_of(t)[0] for t in T], [EI5, w, "Hp2BtvnZvw7YxbQvSehqb1LC5jBSX1aLApzHQnDVwf3q", w])
        self.assertEqual([sol_delta(t, w) for t in T], [1550000000, -1550000000, 3270000000, -3270000000])
        hot = {"H8sMJSCQxfKiFTCfDR3DUMLPwcRbM61LGFJ8N4dK3WjS", "GJRs4FwHtemZ5ZE9x3FNvJ8TMwitKTh21yxdRPqn7npE"}
        sql = (N.REPO / "evidence/labels/dune_cex_solana_addresses.sql").read_text()
        self.assertTrue(all(h in sql for h in hot))
        for t in T[1::2]:
            self.assertTrue(hot & set(keys_of(t)))
            self.assertLess(t["blockTime"] - T[T.index(t) - 1]["blockTime"], 120)
        hp2 = sol("Hp2BtvnZvw7YxbQvSehqb1LC5jBSX1aLApzHQnDVwf3q")
        direct = [t for t in hp2 if EI5 in keys_of(t) and sol_delta(t, EI5) > 0]
        self.assertEqual([sol_delta(t, EI5) for t in direct], [1013173483])


class DcaCircuit(unittest.TestCase):
    """17/11/2024 : exécution b298 -> Ei5yGz8d -> DCA G1fC4Vgk -> FvgqHM -> 2aeEoq5n (wallet neuf) -> vente."""
    W2 = "2aeEoq5n8Cip2raJsiWHBVKuoJL4rid7adepkVYnVzDm"; FVG = "FvgqHMfL9yn39V79huDPy3YUNDoYJpuLWng2JfmQpump"

    def test_dca_and_transfer(self):
        import jup_dca as J
        E = sol(EI5); p = J.positions(E)["G1fC4VgkodbFbsEwV8k8mzb2cMkngfqpiCNMGRZkCwvU"]
        self.assertEqual((p["opened"]["in_deposited"], len(p["fills"]), p["in_filled"], p["out_filled"], p["consistent"]),
                         (482 * 10 ** 9, 35, 482 * 10 ** 9, 3018194265441, True))
        self.assertEqual(p["opened"]["user"], EI5)
        fill = next(t for t in E if sig(t).startswith("Z4XmFhZ8bUmq"))
        self.assertEqual(sol_delta(fill, EI5), 482634652095)
        self.assertEqual(fill["meta"]["preBalances"][keys_of(fill).index(EI5)], 18789476)
        x = next(t for t in E if sig(t).startswith("3ZousK8f"))
        self.assertEqual(tok_delta(x, EI5, self.FVG), -3018194265441)
        A = sorted(sol(self.W2), key=lambda t: t["slot"])
        self.assertEqual((keys_of(A[0])[0], sol_delta(A[0], self.W2), A[0]["meta"]["preBalances"][keys_of(A[0]).index(self.W2)]), (EI5, 25808220, 0))
        self.assertEqual(x["blockTime"] - A[0]["blockTime"], 26)
        sale = next(t for t in A if sig(t).startswith("sJyecugF"))
        self.assertEqual((tok_delta(sale, self.W2, self.FVG), sol_delta(sale, self.W2)), (-3018194265441, 393812873522))


class SelfCheck(unittest.TestCase):
    def test_selfcheck_script(self):
        r = subprocess.run([sys.executable, "-I", str(SCRIPTS / "s99_selfcheck.py")], capture_output=True, text=True,
                           env={**os.environ, "DMAGA_NT_RAW_RO": ""})
        self.assertEqual(r.returncode, 0, r.stdout[-2000:] + r.stderr[-2000:])
        self.assertIn("assertions passées, réseau coupé", r.stdout)


if __name__ == "__main__":
    unittest.main()
