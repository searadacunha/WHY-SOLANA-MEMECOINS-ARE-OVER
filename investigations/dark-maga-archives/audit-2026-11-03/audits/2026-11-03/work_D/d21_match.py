#!/usr/bin/env python3
"""Auditeur D. Témoin à 120 dépôts relu depuis le brut, et test de correspondance dépôt -> retrait contre un nul empirique. Aucun réseau. Sortie d21_match.txt."""
import csv, gzip, json, os, statistics as st, sys, time, collections
NET = "/Volumes/VERBATIM HD/Dark-MAGA-Investigation/audits_work/C/net/"
OUT = "audits/2026-11-03/work_D/"
W9 = "9W9b3zgHH9mCEHDhsdbnbEPHStm9vvXS4aia4DWHBxpL"
HOT = {"H8sMJSCQxfKiFTCfDR3DUMLPwcRbM61LGFJ8N4dK3WjS", "2AQdpHJ2JpcEgPiATUXjQxA8QmafFegfQwSLWSprPicm", "GJRs4FwHtemZ5ZE9x3FNvJ8TMwitKTh21yxdRPqn7npE"}
FAM = {"FpwQQhQQoEaVu3WU2qZMfF1hx48YyfwsLoRgXG83E99Q", "D89hHJT5Aqyx1trP6EnGY9jJUB3whgnq3aUvvCqedvzf", "9obNtb5GyUegcs3a1CbBkLuc5hEWynWfJC6gjz5uWQkE", "DPqsobysNf5iA9w7zrQM8HLzCKZEDMkZsWbiidsAt1xo", "4NyK1AdJBNbgaJ9EsKz3J4rfeHsuYdjkTPg3JaNdLeFw", "8JUEoHNMbWM4eegcMvx6ZQJt3V3fbo8JNjpWiCtJgxfF"}
G5 = "5g7yNHyGLJ7fiQ9SN9mf47opDnMjc585kqXWt6d7aBWs"
BU = "BuHUkjUyWGTwz1suyWpqY6ZcYLX9rbfRsT5nnHFGXykc"
sys.stdout = open(OUT + "d21_match.txt", "w")
iso = lambda t: time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(t))
def tr(t):
    m = t["transaction"]["message"]; seq = list(m["instructions"])
    for g in t["meta"].get("innerInstructions") or []: seq += g["instructions"]
    for i in seq:
        p = i.get("parsed")
        if i.get("program") == "system" and isinstance(p, dict) and p.get("type") == "transfer":
            yield p["info"]["source"], p["info"]["destination"], int(p["info"]["lamports"])
# témoin : flux par dépôt
dep_in = collections.defaultdict(list); out_to = collections.Counter(); out_dep = collections.defaultdict(set); fees = collections.defaultdict(collections.Counter); senders_all = collections.defaultdict(set)
dep_amounts = []
seen = set()
with gzip.open(NET + "ctrl_deposits.jsonl.gz", "rt") as fh:
    for l in fh:
        j = json.loads(l); x = j["x"]; t = j["tx"]; s = t["transaction"]["signatures"][0]
        if (x, s) in seen: continue
        seen.add((x, s))
        for a, b, v in tr(t):
            if b == x and v >= 1_000_000:
                dep_in[x].append((t["blockTime"], a, v)); senders_all[x].add(a)
                if v >= 10_000_000: dep_amounts.append((t["blockTime"], x, a, v))
            if a == x:
                out_to[b] += v; out_dep[b].add(x); fees[x][t["meta"]["fee"]] += 1
print("dépôts témoin", len(dep_in), "versements >= 0,01 SOL", len(dep_amounts), "expéditeurs distincts", len(set().union(*senders_all.values())))
print("destinations de balayage les plus reçues par nb de dépôts", [(k[:10], len(v), k in HOT, k in FAM) for k, v in sorted(out_dep.items(), key=lambda kv: -len(kv[1]))[:14]])
print("5g7yNH reçoit du témoin ?", G5 in out_dep, len(out_dep.get(G5, ())), out_to.get(G5, 0) / 1e9)
sn = sorted(len(v) for v in senders_all.values())
print("nb expéditeurs par dépôt quantiles", {q: sn[int(q * (len(sn) - 1))] for q in (0, .5, .75, .9, .95, 1)})
pf = sum(1 for x, c in fees.items() if 155000 in dict(c.most_common(3)))
print("dépôts où 155 000 lamports est dans le top 3 des frais", pf, "sur", len(fees))
# correspondances : périmètre = historiques locaux (mêmes wallets que C)
W = [f[:-9] for f in os.listdir(NET) if f.endswith(".jsonl.gz") and not f.startswith(("._", "probe", "ctrl", "absent"))]
inc = set()
for w in W:
    with gzip.open(NET + w + ".jsonl.gz", "rt") as fh:
        for l in fh:
            t = json.loads(l)
            for a, b, v in tr(t):
                if b == w and v >= 10_000_000 and a != W9:
                    inc.add((t["blockTime"], a, w, v, t["transaction"]["signatures"][0]))
inc = sorted(inc)
print("wallets locaux", len(W), "entrées >= 0,01 SOL", len(inc))
# dépôts réels sur 9W9b
dep9 = []
with gzip.open(NET + W9 + ".jsonl.gz", "rt") as fh:
    sg = set()
    for l in fh:
        t = json.loads(l); s = t["transaction"]["signatures"][0]
        if s in sg: continue
        sg.add(s)
        for a, b, v in tr(t):
            if b == W9 and v >= 10_000_000: dep9.append((t["blockTime"], a, v, s))
nr = [d for d in dep9 if d[2] % 1_000_000]
print("dépôts 9W9b >= 0,01 SOL", len(dep9), "non ronds à 0,001", len(nr), [d[2] / 1e9 for d in nr])
def matches(deps, day=30, lo=0, hi=1_000_000, placebo=False):
    n = []
    for bt, a, v, *_ in deps:
        for t, src, w, lam, sig in inc:
            d = v - lam
            if lo <= d <= hi and ((0 < t - bt <= day * 86400) if not placebo else (0 < bt - t <= day * 86400)):
                n.append((bt, a, v, t, src, w, lam, d))
    return n
m = matches(nr); print("correspondances dépôt -> retrait, 30 j, 0 à 1e6 lamports", len(m)); [print("  ", iso(x[0]), x[1][:8], x[2], "->", iso(x[3]), x[4][:8], x[5][:8], x[6], "écart", x[7]) for x in m]
m0 = matches(nr, placebo=True); print("placebo temps inversé (entrée AVANT le dépôt)", len(m0)); [print("  ", iso(x[0]), x[1][:8], x[2], "<-", iso(x[3]), x[4][:8], x[5][:8], x[6], "écart", x[7]) for x in m0]
big = [d for d in nr if d[2] >= 1_000_000_000]; print("dépôts non ronds >= 1 SOL", len(big), [d[2] / 1e9 for d in big])
# nul empirique : dépôts du témoin, mêmes règles, tous temps et 30 j
cn = [(bt, a, v) for bt, x, a, v in dep_amounts if v % 1_000_000]
print("dépôts témoin non ronds", len(cn), ">=1 SOL", sum(1 for c in cn if c[2] >= 1e9))
import bisect
lams = sorted(x[3] for x in inc)
def anytime(v, hi):
    return bisect.bisect_right(lams, v) - bisect.bisect_left(lams, v - hi)
for hi, lab in ((1_000_000, "0 à 1e6"), (100_000, "0 à 1e5"), (0, "égal")):
    a_all = sum(anytime(v, hi) for _, _, v in cn); a_big = sum(anytime(v, hi) for _, _, v in cn if v >= 1e9)
    print(f"nul, dépôt témoin contre toutes les entrées du périmètre, écart {lab}, tous temps : {a_all} paires sur {len(cn)} dépôts, soit {a_all/len(cn):.5f} par dépôt ; dépôts >=1 SOL : {a_big} paires, {a_big/max(1,sum(1 for c in cn if c[2]>=1e9)):.5f} par dépôt")
ex = sum(1 for _, _, v in cn if any(l == v - 100000 for l in lams[bisect.bisect_left(lams, v - 100000):bisect.bisect_right(lams, v - 100000)]))
print("nul, écart EXACT 100 000 lamports, dépôts témoin", ex, "sur", len(cn))
ex2 = sum(1 for _, _, v in cn if v >= 1e9 and any(True for l in lams[bisect.bisect_left(lams, v - 100000):bisect.bisect_right(lams, v - 100000)]))
print("nul, idem, dépôts >= 1 SOL", ex2)
# même nul sur écart multiple de 100 000 (0 à 1e6) et >= 1 SOL : 11 valeurs
ex3 = 0
for _, _, v in cn:
    if v < 1e9: continue
    for k in range(0, 11):
        q = v - k * 100000
        if bisect.bisect_right(lams, q) > bisect.bisect_left(lams, q): ex3 += 1
print("nul, écart multiple de 100 000 de 0 à 1e6, dépôts >= 1 SOL", ex3)
# entrée de BuHUkjUy, détail
if os.path.exists(NET + BU + ".jsonl.gz"):
    r = []
    with gzip.open(NET + BU + ".jsonl.gz", "rt") as fh:
        for l in fh:
            t = json.loads(l); me = t["meta"]; keys = [k["pubkey"] for k in t["transaction"]["message"]["accountKeys"]]
            tk = []
            for s, n in ((-1, "preTokenBalances"), (1, "postTokenBalances")):
                for b in me.get(n) or []:
                    if b.get("owner") == BU: tk.append((b["mint"][:6], s * int(b["uiTokenAmount"]["amount"])))
            agg = collections.Counter()
            for mm, v in tk: agg[mm] += v
            r.append((t["slot"], t["blockTime"], t["transaction"]["signatures"][0], keys[0][:8], [(a[:8], b[:8], v / 1e9) for a, b, v in tr(t)][:3], {k: v for k, v in agg.items() if v}))
    r.sort()
    print("BuHUkjUy tx", len(r))
    for x in r[:14]: print("  ", iso(x[1]), x[2], "payeur", x[3], x[4], x[5])
    print("  ... dernière", iso(r[-1][1]))
