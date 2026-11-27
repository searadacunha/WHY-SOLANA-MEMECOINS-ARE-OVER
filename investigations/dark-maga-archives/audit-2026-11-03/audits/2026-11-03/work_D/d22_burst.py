#!/usr/bin/env python3
"""Auditeur D. Empreinte de 9W9b contre le témoin, avec et sans le filtre choisi par C (rond et vidé). Sortie d22_burst.txt. Aucun réseau."""
import gzip, json, sys, collections, statistics as st, time, csv
NET = "/Volumes/VERBATIM HD/Dark-MAGA-Investigation/audits_work/C/net/"
OUT = "audits/2026-11-03/work_D/"
W9 = "9W9b3zgHH9mCEHDhsdbnbEPHStm9vvXS4aia4DWHBxpL"
sys.stdout = open(OUT + "d22_burst.txt", "w")
def rows(x, t):
    r = []
    keys = [k["pubkey"] for k in t["transaction"]["message"]["accountKeys"]]
    seq = list(t["transaction"]["message"]["instructions"])
    for g in t["meta"].get("innerInstructions") or []: seq += g["instructions"]
    for i in seq:
        p = i.get("parsed")
        if i.get("program") == "system" and isinstance(p, dict) and p.get("type") == "transfer" and p["info"]["destination"] == x and int(p["info"]["lamports"]) >= 1_000_000:
            s = p["info"]["source"]; post = t["meta"]["postBalances"][keys.index(s)] if s in keys else None
            r.append((t["blockTime"], s, int(p["info"]["lamports"]), post))
    return r
by = collections.defaultdict(dict)
with gzip.open(NET + "ctrl_deposits.jsonl.gz", "rt") as fh:
    for l in fh:
        j = json.loads(l); s = j["tx"]["transaction"]["signatures"][0]
        for k, v in enumerate(rows(j["x"], j["tx"])): by[j["x"]][(s, k)] = v
with gzip.open(NET + W9 + ".jsonl.gz", "rt") as fh:
    for l in fh:
        t = json.loads(l); s = t["transaction"]["signatures"][0]
        for k, v in enumerate(rows(W9, t)): by[W9][(s, k)] = v
def burst(L, win=600):
    L = sorted(L); best = 0
    for i, a in enumerate(L):
        best = max(best, len({b[1] for b in L[i:] if b[0] < a[0] + win}))
    return best
res = {}
for x, d in by.items():
    L = list(d.values())
    rnd = [r for r in L if r[2] % 1_000_000 == 0]
    emp = [r for r in L if r[3] is not None and r[3] < 20_000_000]
    both = [r for r in rnd if r[3] is not None and r[3] < 20_000_000]
    res[x] = dict(n=len(L), senders=len({r[1] for r in L}), any_=burst(L), rnd=burst(rnd), emp=burst(emp), both=burst(both), mult=sum(1 for c in collections.Counter(r[1] for r in L).values() if c > 1))
print("9W9b", res[W9])
ctrl = {k: v for k, v in res.items() if k != W9}
for f in ("any_", "rnd", "emp", "both"):
    vals = sorted(v[f] for v in ctrl.values())
    print(f"témoin {f}: médiane {st.median(vals)}, p90 {vals[int(.9*(len(vals)-1))]}, max {vals[-1]} ; dépôts >= valeur de 9W9b ({res[W9][f]}) : {sum(1 for x in vals if x >= res[W9][f])} sur {len(vals)}")
print("témoins aux rafales brutes les plus fortes", sorted(((v["any_"], v["senders"], v["both"], k[:8]) for k, v in ctrl.items()), reverse=True)[:8])
print("témoins à 20 expéditeurs ou plus :", sum(1 for v in ctrl.values() if v["senders"] >= 20))
# régularité de la salve : écarts successifs
s9 = sorted(by[W9].values())
jan = [r for r in s9 if 1737849600 <= r[0] < 1737936000]
g = [b[0] - a[0] for a, b in zip(jan, jan[1:])]
print("écarts 26/01/2025", g)
# série : première tx du wallet égale au retrait ?
ROOT = "audits/2026-11-03/work_C/"
ser = [r for r in csv.DictReader(open(ROOT + "cb_window.csv")) if "2024-07-14T01:32:20Z" <= r["utc"] <= "2024-07-14T01:40:51Z" and round(float(r["sol"]) * 1e9) in (500000000, 1000000000, 1050000000)]
import os, calendar
fresh = 0
for r in ser:
    a = r["dest"]; p = NET + a + ".jsonl.gz"
    if not os.path.exists(p): print("pas d'historique", a); continue
    m = None; n = 0
    with gzip.open(p, "rt") as fh:
        for l in fh:
            t = json.loads(l); n += 1
            b = t["blockTime"]; m = b if m is None or b < m else m
    tt = calendar.timegm(time.strptime(r["utc"], "%Y-%m-%dT%H:%M:%SZ"))
    fresh += m == tt
    print("  ", r["utc"][11:19], a[:8], "tx", n, "1re tx = retrait", m == tt)
print("série : 1re tx = retrait", fresh, "sur", len(ser))
