#!/usr/bin/env python3
"""Sorties d'USD par programme sans contrepartie reçue par le wallet (src5qyZH et autres) : le jeton acheté part-il vers un tiers ? Sortie g38.txt."""
import csv, gzip, sys, time, collections
sys.path.insert(0, "audits/2026-11-03/work_G")
from g_lib import history, parse
from dmaga.labels import label
OUT = "audits/2026-11-03/work_G/"; G = "/Volumes/VERBATIM HD/Dark-MAGA-Investigation/audits_work/G/"
sys.stdout = open(OUT + "g38.txt", "w")
iso = lambda t: time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(t))
T = {r["wallet"] for r in csv.DictReader(open(OUT + "targets.csv"))}
want = collections.defaultdict(set)
for l in csv.DictReader(gzip.open(G + "net_txs.csv.gz", "rt")):
    if l["owner"] in T and l["err"] == "0" and l["pure"] == "0" and l["signed"] == "1" and int(l["usdc_delta"]) + int(l["usdt_delta"]) < -50_000_000 and int(l["native_delta"]) <= 0 and int(l["wsol_delta"]) == 0 and int(l["n_other_mints"]) == 0 and int(l["dmaga_delta"]) == 0:
        want[l["owner"]].add(l["sig"])
print("tx", sum(len(v) for v in want.values()))
for a, S in want.items():
    for t in history(a):
        s = t["transaction"]["signatures"][0]
        if s in S:
            x = parse(t)
            print(iso(x["bt"]), a[:8], s, "programmes", [p[:10] for p in x["progs"]], "| jetons", [((o or "")[:8], m[:6], v) for (o, m), v in sorted(x["tok"].items(), key=lambda kv: -abs(kv[1]))[:5]])
            print("    transferts", [(asset if asset != "other" else mint[:6], (src or "")[:8], (d or "")[:8], round(raw / (10 ** (dec or 0)), 3)) for k, asset, mint, src, d, raw, dec in x["moves"] if k == "spl"][:6], "journaux", [m[13:50] for m in (t["meta"].get("logMessages") or []) if "Program log: Instruction" in m][:2])
