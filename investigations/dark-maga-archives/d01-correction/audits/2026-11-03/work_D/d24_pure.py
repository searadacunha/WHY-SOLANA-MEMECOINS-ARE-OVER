#!/usr/bin/env python3
"""Auditeur D. Suite de d23 sans réseau : même statistique, limitée aux virements purs (programmes System et ComputeBudget seulement, >= 0,05 SOL), pour écarter comptes de frais et pourboires. Sortie d24_pure.txt."""
import csv, gzip, json, sys, collections, time, calendar
OUT = "audits/2026-11-03/work_D/"; NET = "/Volumes/VERBATIM HD/Dark-MAGA-Investigation/audits_work/C/net/"; D = "/Volumes/VERBATIM HD/Dark-MAGA-Investigation/audits_work/D/"
sys.stdout = open(OUT + "d24_pure.txt", "w")
OK = {"11111111111111111111111111111111", "ComputeBudget111111111111111111111111111111"}
def dests(x, t):
    m = t["transaction"]["message"]; seq = list(m["instructions"])
    for g in t["meta"].get("innerInstructions") or []: seq += g["instructions"]
    if {i["programId"] for i in seq} - OK: return
    for i in seq:
        p = i.get("parsed")
        if i.get("program") == "system" and isinstance(p, dict) and p.get("type") == "transfer" and p["info"]["source"] == x and int(p["info"]["lamports"]) >= 50_000_000:
            yield p["info"]["destination"], int(p["info"]["lamports"])
plan = list(csv.DictReader(open(OUT + "d23_plan.csv")))
win = {p["dest"]: int(p["fenetre"]) for p in plan}
C = collections.defaultdict(lambda: collections.defaultdict(set)); N = collections.Counter(); seen = set()
with gzip.open(D + "d23_net.jsonl.gz", "rt") as fh:
    for l in fh:
        j = json.loads(l); x = j["x"]; w = win[x]
        if x not in seen: seen.add(x); N[w] += 1
        for d, v in dests(x, j["tx"]): C[w][d].add(x)
for w in sorted(N):
    top = sorted(((len(v), k) for k, v in C[w].items()), reverse=True)[:5]
    print("fenêtre", w, "wallets", N[w], "max par destination (virement pur >= 0,05 SOL)", top[0][0] if top else 0, [(n, k[:10]) for n, k in top])
ts = lambda u: calendar.timegm(time.strptime(u, "%Y-%m-%dT%H:%M:%SZ"))
ser = [r for r in csv.DictReader(open("audits/2026-11-03/work_C/cb_window.csv")) if "2024-07-14T01:32:20Z" <= r["utc"] <= "2024-07-14T01:40:51Z" and round(float(r["sol"]) * 1e9) in (500000000, 1000000000, 1050000000)]
CS = collections.defaultdict(set); CF = collections.defaultdict(set)
for r in ser:
    a = r["dest"]; txs = []
    with gzip.open(NET + a + ".jsonl.gz", "rt") as fh:
        for l in fh: txs.append(json.loads(l))
    txs.sort(key=lambda t: (t["slot"], t.get("transactionIndex") or 0))
    for i, t in enumerate(txs):
        for d, v in dests(a, t):
            CF[d].add(a)
            if i < 100: CS[d].add(a)
print("série, 100 premières tx", [(len(v), k[:10]) for k, v in sorted(CS.items(), key=lambda kv: -len(kv[1]))[:5]])
print("série, historique complet", [(len(v), k[:10]) for k, v in sorted(CF.items(), key=lambda kv: -len(kv[1]))[:5]])
