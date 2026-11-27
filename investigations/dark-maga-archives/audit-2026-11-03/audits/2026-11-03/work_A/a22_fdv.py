#!/usr/bin/env python3
"""Auditeur A. Capitalisation une heure avant S : DMAGA et 30 comparateurs tirés au hasard (graine 20261103), relue dans le brut ctrl_tx, contre selection.jsonl. En flux."""
import csv, gzip, io, json, random, zipfile
from pathlib import Path
RAW = Path("/Volumes/VERBATIM HD/Dark-MAGA-Investigation/raw/ctrl_tx")
SOL = Path("/Volumes/VERBATIM HD/Dark-MAGA-Investigation/raw/solusd")
C = Path("/Volumes/VERBATIM HD/Dark-MAGA-Investigation/data/controls")
ROOT = "REDACTED_HOME/Projects/Dark-MAGA-Investigation"
DP = "CRSwXnfF21yHDXdYBVWwCwQ5Ni2A4QuK3qGYis5k7x7k"
H = 3600
px = {}
for z in sorted(SOL.glob("SOLUSDT-1m-2024-*.zip")):
    if z.name.startswith("._"):
        continue
    with zipfile.ZipFile(z) as f, f.open(f.namelist()[0]) as fh:
        for row in csv.reader(io.TextIOWrapper(fh)):
            if row and row[0].isdigit():
                px[int(row[0]) // 60000] = float(row[4])
sel = {}
for x in open(C / "selection.jsonl"):
    r = json.loads(x)
    if r["status"] == "retenu_superset":
        sel[r["pool"]] = r
prim = [r["pool"] for r in csv.DictReader(open(ROOT + "/etude_final/derived/metrics.csv")) if r["variant"] == "primary"]
rng = random.Random(20261103)
sample = [DP] + rng.sample([p for p in prim if p != DP], 30)
out = []
for p in sample:
    r = sel[p]
    S = r["S20"]
    best = None
    pages = sorted((RAW / p).glob("p*.jsonl.gz"), reverse=True)
    for pg in pages:
        with gzip.open(pg, "rt") as f:
            for line in f:
                tx = json.loads(line)
                if tx["blockTime"] >= S - H or tx["meta"].get("err") is not None:
                    continue
                keys = [k["pubkey"] for k in tx["transaction"]["message"]["accountKeys"]]
                pre = {keys[b["accountIndex"]]: int(b["uiTokenAmount"]["amount"]) for b in tx["meta"].get("preTokenBalances") or []}
                post = {keys[b["accountIndex"]]: (int(b["uiTokenAmount"]["amount"]), b["uiTokenAmount"]["decimals"]) for b in tx["meta"].get("postTokenBalances") or []}
                vt, vs = r["vault_token"], r["vault_sol"]
                if vt in post and vs in post and post[vt][0] != pre.get(vt, 0) and post[vs][0] != pre.get(vs, 0) and post[vt][0] > 0:
                    k = (tx["slot"], tx.get("transactionIndex") or 0)
                    if best is None or k > best[0]:
                        best = (k, tx["blockTime"], post[vs][0], post[vt][0], post[vt][1])
        if best:
            break
    if not best:
        out.append((p, None, r.get("fdv_s20")))
        continue
    k, t, q, b, dec = best
    fdv = (q / 1e9) / (b / 10**dec) * 1e9 * px[t // 60]
    out.append((p, round(fdv, 2), round(r.get("fdv_s20"), 2), t, S, dec))
bad = [x for x in out if x[1] is None or abs(x[1] - x[2]) > 0.001 * x[2]]
print("échantillon", len(out), "écarts > 0,1 %", len(bad), bad[:6])
print("DMAGA", out[0])
print("décimales vues", sorted({x[5] for x in out if x[1] is not None}))
print("S - t (s) max", max(x[4] - x[3] for x in out if x[1] is not None) - H)
