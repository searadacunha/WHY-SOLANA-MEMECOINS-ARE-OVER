# Audit indépendant des reçus (second auditeur, 06/11/2026) : décodeur propre, hors ligne, sans code du dépôt.
# Rapport : FINDINGS.md §12. Lancer : python3 -I audit/second_auditor_receipts.py
"""Independent audit of claims C1-C6 from raw getTransaction receipts. Offline, read-only."""
import csv, glob, json, os, sys
from datetime import datetime, timezone
from decimal import Decimal

BASE = __import__("os").path.dirname(__import__("os").path.dirname(__import__("os").path.abspath(__file__)))  # dossier de l'enquête
REC = BASE + "/evidence/receipts"
DATA = BASE + "/data"
OUT = os.path.dirname(os.path.abspath(__file__)) + "/second_auditor_results.json"

G7 = "7GVCZAYG5NfiJsuqUdvc9hB2ts2W3tSrGdya4CyR1M5j"
S9 = "9Sxmf25WG5WVQ5p86ycWeo5hMEwxiWPkFtLdRdTrHSQS"
DMAGA = "7D7BRcBYepfi77vxySapmeqRNN1wsBBxnFPJGbH5pump"
PERPS = "PERPHjGBqRHArX4DySjwM6UJHiR3sWAatqfdBS2qQJu"
PUMP = "6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P"
WSOL = "So11111111111111111111111111111111111111112"
SYS = "11111111111111111111111111111111"
MINT_T = 1720922725
# programs that are neither token/system/budget/ATA/memo: anything else = "non-trivial program present"
TRIVIAL = {SYS, "TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA", "TokenzQdBNbLqP5VEhdkAS6EPFLC1PHnBqCXEpPxuEb",
           "ComputeBudget111111111111111111111111111111", "ATokenGPvbdGVxr1b2hvZbsiqW5xWH25efTNsLJA8knL",
           "MemoSq4gqABAXKb96qnH8TysNcWxMyWCqXgDLGmfcHr", "Memo1UhkJRfHyvLMcVucJwxXeuD728EqVDDwQDxFMNo"}


def utc(t):
    return datetime.fromtimestamp(t, timezone.utc).strftime("%Y-%m-%d %H:%M:%S")


def find(prefix):
    fs = [f for f in glob.glob(REC + "/" + prefix + "*.json")]
    return fs[0] if len(fs) == 1 else None


class Tx:
    def __init__(self, path):
        self.d = d = json.load(open(path))
        self.sig = d["transaction"]["signatures"][0]
        assert os.path.basename(path)[:-5] == self.sig, "file name != signature"
        m = d["transaction"]["message"]
        self.keys = [k["pubkey"] for k in m["accountKeys"]]
        self.signers = [k["pubkey"] for k in m["accountKeys"] if k["signer"]]
        meta = d["meta"]
        assert len(self.keys) == len(meta["preBalances"]) == len(meta["postBalances"]), "key/balance length mismatch"
        self.err = meta["err"]
        self.fee = meta["fee"]
        self.slot = d["slot"]
        self.t = d["blockTime"]
        self.native = {k: meta["postBalances"][i] - meta["preBalances"][i] for i, k in enumerate(self.keys)}
        self.pre_nat = {k: meta["preBalances"][i] for i, k in enumerate(self.keys)}
        # token balances by account index
        tb = {}
        for side in ("preTokenBalances", "postTokenBalances"):
            for b in meta.get(side) or []:
                e = tb.setdefault(b["accountIndex"], {"mint": b["mint"], "owner": b.get("owner"), "pre": 0, "post": 0})
                e["pre" if side.startswith("pre") else "post"] = int(b["uiTokenAmount"]["amount"])
                e["owner"] = e["owner"] or b.get("owner")
        self.tok = {self.keys[i]: v for i, v in tb.items()}
        # flat instruction list with path
        self.ix = []
        inner = {g["index"]: g["instructions"] for g in meta.get("innerInstructions") or []}
        for i, ins in enumerate(m["instructions"]):
            self.ix.append(((i, None), ins))
            for j, s in enumerate(inner.get(i, [])):
                self.ix.append(((i, j), s))
        self.programs = sorted({ins["programId"] for _, ins in self.ix})
        self.logs_ix = [l.split("Instruction: ", 1)[1] for l in meta.get("logMessages") or [] if "Instruction: " in l]

    def owner_delta(self, owner, mint):
        return sum(v["post"] - v["pre"] for v in self.tok.values() if v["owner"] == owner and v["mint"] == mint)

    def parsed(self, program=None, typ=None):
        out = []
        for path, ins in self.ix:
            p = ins.get("parsed")
            if not isinstance(p, dict):
                continue
            if program and ins.get("program") != program:
                continue
            if typ and p.get("type") not in (typ if isinstance(typ, tuple) else (typ,)):
                continue
            out.append((path, ins.get("programId"), p["type"], p["info"]))
        return out

    def head(self):
        return {"sig": self.sig, "slot": self.slot, "blockTime": self.t, "utc": utc(self.t), "signers": self.signers,
                "fee": self.fee, "err": self.err, "programs": self.programs, "log_instructions": self.logs_ix}


def tok_amount(info):
    return int(info["amount"]) if "amount" in info else int(info["tokenAmount"]["amount"])


R = {}

# ---------------- C1 ----------------
t = Tx(find("44Sd6xet31me1Hc1"))
c1 = t.head()
c1["delta_7GVC"] = t.native[G7]
c1["7GVC_signer"] = G7 in t.signers
c1["keeper_native_delta"] = {s: t.native[s] for s in t.signers}
c1["closeAccount"] = [(p, i) for p, _, _, i in t.parsed("spl-token", "closeAccount")]
c1["spl_transfers"] = [(p, i) for p, _, _, i in t.parsed("spl-token", ("transfer", "transferChecked"))]
c1["system_transfers"] = [(p, i) for p, _, _, i in t.parsed("system")]
c1["accounts_losing_lamports"] = {k: v for k, v in t.native.items() if v < 0}
c1["accounts_gaining_lamports"] = {k: v for k, v in t.native.items() if v > 0}
c1["token_balances"] = t.tok
c1["mint_minus_block_s"] = MINT_T - t.t
# decomposition: lamports of every account that went to zero (closed) inside this tx
closed = {k: t.pre_nat[k] for k in t.keys if t.pre_nat[k] > 0 and t.pre_nat[k] + t.native[k] == 0}
c1["closed_accounts_pre_lamports"] = closed
wsol_acct = c1["closeAccount"][0][1]["account"]
wsol_tokens_in = sum(tok_amount(i) for _, i in c1["spl_transfers"] if i["destination"] == wsol_acct)
c1["decomposition"] = {
    "wsol_tokens_transferred_into_closed_ata": wsol_tokens_in,
    "rent_of_closed_wsol_ata": t.pre_nat[wsol_acct],
    "other_closed_accounts": {k: v for k, v in closed.items() if k != wsol_acct},
}
c1["decomposition_sum"] = wsol_tokens_in + sum(closed.values())
c1["owner_of_closed_wsol_ata"] = c1["closeAccount"][0][1]["owner"]
for pfx in ("2VMyrqES", "GFDyshi4"):
    f = find(pfx)
    if not f:
        c1[pfx] = "MISSING"
        continue
    u = Tx(f)
    h = u.head()
    h["7GVC_signer"] = G7 in u.signers
    h["delta_7GVC"] = u.native[G7]
    h["spl"] = [(p, ty, i) for p, _, ty, i in u.parsed("spl-token")]
    h["system"] = [(p, ty, i) for p, _, ty, i in u.parsed("system")]
    h["perps_in_outer"] = [p[0] for p, ins in u.ix if p[1] is None and ins["programId"] == PERPS]
    c1[pfx] = h
R["C1"] = c1

# ---------------- C2 / C3 ----------------
c2 = {}
total = 0
for pfx in ("4QcZWRme", "34LDkYZr"):
    u = Tx(find(pfx))
    h = u.head()
    h["7GVC_signer"] = G7 in u.signers
    h["dmaga_delta_7GVC"] = u.owner_delta(G7, DMAGA)
    h["native_delta_7GVC"] = u.native[G7]
    h["pump_outer"] = [p[0] for p, ins in u.ix if ins["programId"] == PUMP and p[1] is None]
    h["dmaga_spl_moves"] = [(p, i) for p, _, _, i in u.parsed("spl-token", ("transfer", "transferChecked"))]
    h["system_moves"] = [(p, i) for p, _, _, i in u.parsed("system", "transfer")]
    h["wsol_delta_7GVC"] = u.owner_delta(G7, WSOL)
    h["other_token_deltas_7GVC"] = {v["mint"]: v["post"] - v["pre"] for v in u.tok.values() if v["owner"] == G7}
    total += h["dmaga_delta_7GVC"]
    c2[pfx] = h
c2["total_dmaga"] = total
c2["claimed_total"] = 41197138380017
R["C2"] = c2
later_buy = max(c2["4QcZWRme"]["blockTime"], c2["34LDkYZr"]["blockTime"])

u = Tx(find("2FezsDLM"))
c3 = u.head()
c3["spl"] = [(p, ty, i) for p, _, ty, i in u.parsed("spl-token")]
c3["dmaga_delta_7GVC"] = u.owner_delta(G7, DMAGA)
c3["dmaga_delta_9Sxm"] = u.owner_delta(S9, DMAGA)
c3["token_accounts"] = u.tok
c3["non_trivial_programs"] = [p for p in u.programs if p not in TRIVIAL]
c3["gap_after_later_buy_s"] = u.t - later_buy
c3["gap_hms"] = "%d min %d s" % divmod(u.t - later_buy, 60)
c3["mint_to_transfer_s"] = u.t - MINT_T
R["C3"] = c3

# ---------------- C4 ----------------
c4 = {}
for row in csv.DictReader(open(DATA + "/jeffro_satellites.csv")):
    sat = row["address"]
    e = {"claimed_sol": row["jeffro_sol"], "claimed_lag_s": row["first_buy_lag_s"], "funding": []}
    fund_t = []
    tot = 0
    for s in row["funding_signatures"].split(";"):
        f = find(s)
        if not f:
            e["funding"].append({"sig": s, "receipt": "MISSING"})
            continue
        v = Tx(f)
        h = v.head()
        tr = [(p, i) for p, _, _, i in v.parsed("system", "transfer") if i["destination"] == sat]
        h["transfers_to_sat"] = tr
        h["direct_from_7GVC"] = [i["lamports"] for p, i in tr if i["source"] == G7]
        h["7GVC_signer"] = G7 in v.signers
        h["sat_native_delta"] = v.native[sat]
        h["non_trivial_programs"] = [p for p in v.programs if p not in TRIVIAL]
        tot += sum(h["direct_from_7GVC"])
        fund_t.append(v.t)
        e["funding"].append(h)
    e["sum_direct_lamports"] = tot
    first_buy = row["buy_signatures"].split(";")[0]
    e["buy_receipts_present"] = [s[:8] for s in row["buy_signatures"].split(";") if find(s)]
    e["n_buy_sigs"] = len(row["buy_signatures"].split(";"))
    f = find(first_buy)
    if f:
        b = Tx(f)
        h = b.head()
        h["sat_signer"] = sat in b.signers
        h["sat_dmaga_delta"] = b.owner_delta(sat, DMAGA)
        h["sat_native_delta"] = b.native[sat]
        h["dmaga_moves"] = [(p, i) for p, _, _, i in b.parsed("spl-token", ("transfer", "transferChecked"))]
        e["first_buy"] = h
        e["lag_from_first_funding_s"] = b.t - min(fund_t)
        e["lag_from_last_funding_s"] = b.t - max(fund_t)
    else:
        e["first_buy"] = "MISSING"
    c4[sat] = e
R["C4"] = c4

# ---------------- C5 ----------------
c5 = {"rows": [], "pass": 0, "fail": 0, "group_mismatch_rows": [], "same_group_col_inconsistent": []}
for row in csv.DictReader(open(DATA + "/noah_edges.csv")):
    g1, g2 = row["src_group"][:1], row["dst_group"][:1]
    if g1 != g2:
        c5["group_mismatch_rows"].append((row["utc"], row["src_group"], row["dst_group"], row["signature"][:10]))
    if (g1 == g2) != (row["same_group"] == "True"):
        c5["same_group_col_inconsistent"].append(row["signature"][:10])
    if row["asset"] != "DMAGA" or row["source_table"] not in ("tx_balances", "token_direct"):
        continue
    src, dst = row["src"], row["dst"]
    want = int(Decimal(row["amount"]) * 10**6)
    r = {"sig": row["signature"][:10], "utc_csv": row["utc"], "src": src[:6], "dst": dst[:6], "want": want}
    f = find(row["signature"])
    if not f:
        r["verdict"] = "FAIL: receipt missing"
    else:
        v = Tx(f)
        r.update(utc=utc(v.t), slot=v.slot, signers=[s[:6] for s in v.signers], err=v.err)
        r["dst_delta"] = v.owner_delta(dst, DMAGA)
        r["src_delta"] = v.owner_delta(src, DMAGA)
        moves = [(p, i) for p, _, _, i in v.parsed("spl-token", ("transfer", "transferChecked"))]
        r["moves"] = [(p, tok_amount(i), (i.get("authority") or i.get("multisigAuthority") or "")[:6], "multisig-form" if "multisigAuthority" in i else "") for p, i in moves]
        r["non_trivial_programs"] = [p for p in v.programs if p not in TRIVIAL]
        probs = []
        if v.err is not None: probs.append("tx error")
        if r["dst_delta"] != want: probs.append("dst delta %d != %d" % (r["dst_delta"], want))
        if r["src_delta"] != -want: probs.append("src delta %d != -%d" % (r["src_delta"], want))
        if src not in v.signers: probs.append("src not signer")
        auth = lambda i: i.get("authority") or i.get("multisigAuthority")
        if not any(auth(i) == src and tok_amount(i) == want and pth[1] is None for pth, i in moves): probs.append("no top-level SPL transfer with authority=src and amount")
        if any(pth[1] is not None for pth, i in moves): probs.append("token move inside a CPI")
        # DeJBGd...: 1 account, 32 zero bytes, no CPI, no balance effect (wallet-side assertion), not a pool
        other = [x for x in r["non_trivial_programs"] if x != "DeJBGdMFa1uynnnKiwrVioatTuHmNLpyFKnmB5kaFdzQ"]
        if other: probs.append("other programs: %s" % other)
        if utc(v.t) != row["utc"]: probs.append("utc mismatch %s" % utc(v.t))
        r["verdict"] = "PASS" if not probs else "FAIL: " + "; ".join(probs)
    c5["pass" if r["verdict"] == "PASS" else "fail"] += 1
    c5["rows"].append(r)
R["C5"] = c5

# ---------------- C6 ----------------
HB = "HBsgbpsM1j1YsNYqtCXcFU4mCRofwcor2qFwifNqddmH"
rows = list(csv.DictReader(open(DATA + "/counterparty_%s.csv" % HB)))
c6 = {"n_rows": len(rows), "n_unique_sigs": len({r["signature"] for r in rows})}
pay = [r for r in rows if r["dir"] == "in" and not (r["kind"] == "sol" and int(r["amount_raw"]) <= 1000)]
c6["inbound_non_dust"] = []
for r in pay:
    e = {"utc": r["utc"], "payer": r["counterparty"], "kind": r["kind"], "mint": r["mint"][:6], "raw": int(r["amount_raw"]),
         "sig": r["signature"][:10]}
    f = find(r["signature"])
    if f:
        v = Tx(f)
        e["receipt"] = True
        e["receipt_utc"] = utc(v.t)
        e["payer_signer"] = r["counterparty"] in v.signers
        if r["kind"] == "sol":
            tr = [i["lamports"] for p, _, _, i in v.parsed("system", "transfer") if i["destination"] == HB and i["source"] == r["counterparty"]]
            e["receipt_lamports_to_HB"] = tr
            e["HB_native_delta"] = v.native.get(HB)
        else:
            e["receipt_token_delta_HB"] = v.owner_delta(HB, r["mint"])
            e["receipt_token_moves"] = [(p, tok_amount(i), (i.get("authority") or "")[:6]) for p, _, _, i in v.parsed("spl-token", ("transfer", "transferChecked"))]
        e["non_trivial_programs"] = [p for p in v.programs if p not in TRIVIAL]
    else:
        e["receipt"] = False
    c6["inbound_non_dust"].append(e)
c6["outbound"] = [(r["utc"], r["counterparty"][:8], r["kind"], int(r["amount_raw"])) for r in rows if r["dir"] == "out"]
c6["dust_in_rows"] = sum(1 for r in rows if r["dir"] == "in" and r["kind"] == "sol" and int(r["amount_raw"]) <= 1000)
# ~700 USD band at assumed 175-185 USD/SOL
lo, hi = 700 / 185, 700 / 175
c6["band_sol_700usd"] = (round(lo, 4), round(hi, 4))
c6["payers_in_band_or_700usdc"] = sorted({e["payer"] for e in c6["inbound_non_dust"]
                                         if (e["kind"] == "sol" and lo * 0.97 <= e["raw"] / 1e9 <= hi * 1.03)
                                         or (e["kind"] == "token" and e["mint"] == "EPjFWd" and e["raw"] == 700_000_000)})
# classification rule check
viol = []
for r in csv.DictReader(open(DATA + "/noah_cross_group.csv")):
    touched = int(r["dmaga_wallets_touched"])
    mx = float(r["max_sol"]) if r["max_sol"] else 0.0
    exp = "service" if (touched > 25 or r["label"].strip()) else ("poussière" if mx < 0.01 else "candidate")
    if exp != r["class"]:
        viol.append((r["counterparty"], touched, r["max_sol"], r["label"], r["class"], exp))
c6["cross_group_rule_violations"] = viol
# borderline rows: service only because of touched count with tiny amounts, or non-SOL only
c6["service_with_max_sol_lt_0.01"] = [(r["counterparty"][:8], r["dmaga_wallets_touched"], r["max_sol"], r["assets"])
                                      for r in csv.DictReader(open(DATA + "/noah_cross_group.csv"))
                                      if r["class"] == "service" and float(r["max_sol"] or 0) < 0.01]
c6["candidates_review"] = [dict(r) for r in csv.DictReader(open(DATA + "/noah_candidates_review.csv"))]
cg = {r["counterparty"]: r for r in csv.DictReader(open(DATA + "/noah_cross_group.csv"))}
c6["candidates_vs_cross_group"] = {r["counterparty"][:8]: cg.get(r["counterparty"], {}).get("class") for r in c6["candidates_review"]}
R["C6"] = c6

json.dump(R, open(OUT, "w"), indent=1, default=str, ensure_ascii=False)
print("wrote", OUT)
