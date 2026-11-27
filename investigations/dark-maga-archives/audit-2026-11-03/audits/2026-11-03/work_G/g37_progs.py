#!/usr/bin/env python3
"""Ce que font les programmes des sorties unilatérales : pour chaque préfixe de programme, liste des tx du périmètre (net_txs), destinations réelles, journaux d'un exemple. Sortie g37.txt, g37_rows.csv (lignes par tx)."""
import csv, gzip, json, sys, time, collections
sys.path.insert(0, "audits/2026-11-03/work_G")
from g_lib import history, parse
from dmaga.labels import label
OUT = "audits/2026-11-03/work_G/"; G = "/Volumes/VERBATIM HD/Dark-MAGA-Investigation/audits_work/G/"
sys.stdout = open(OUT + "g37.txt", "w")
iso = lambda t: time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(t))
PRE = ("src5qyZH", "BrdgN2RP", "DeJBGdMF", "ENicYBBN", "Pinks8fX", "j1o2qRpj")
T = {r["wallet"] for r in csv.DictReader(open(OUT + "targets.csv"))}
hits = collections.defaultdict(list)
for l in csv.DictReader(gzip.open(G + "net_txs.csv.gz", "rt")):
    if l["owner"] in T and l["err"] == "0" and any(p.startswith(PRE) for p in l["programs"].split(";")):
        for p in PRE:
            if p in l["programs"]: hits[p].append(l)
w = csv.writer(open(OUT + "g37_rows.csv", "w", newline="")); w.writerow("programme owner utc sig native_delta_sol usdc usdt dmaga".split())
want = collections.defaultdict(set)
for p, L in hits.items():
    print("==", p, "tx", len(L), "wallets", len({x["owner"] for x in L}), "programme complet", {q for x in L for q in x["programs"].split(";") if q.startswith(p)})
    for x in L:
        w.writerow([p, x["owner"], iso(int(x["bt"])), x["sig"], int(x["native_delta"]) / 1e9, int(x["usdc_delta"]) / 1e6, int(x["usdt_delta"]) / 1e6, int(x["dmaga_delta"]) / 1e6])
        want[x["owner"]].add(x["sig"])
sx = {x["sig"]: p for p, L in hits.items() for x in L}
seen_ex = collections.Counter(); dst = collections.defaultdict(collections.Counter)
for a in want:
    for t in history(a):
        s = t["transaction"]["signatures"][0]
        if s in want[a]:
            x = parse(t); p = sx[s]
            for k, asset, mint, src, d, raw, dec in x["moves"]:
                if src == a and asset in ("SOL", "USDC", "USDT", "WSOL", "DMAGA"): dst[p][(d, asset)] += raw / (1e9 if asset in ("SOL", "WSOL") else 1e6)
            if seen_ex[p] < 2:
                seen_ex[p] += 1
                print("  ex", p, a[:8], iso(x["bt"]), s, "signataires", [q[:8] for q in x["signers"]], "moves", [(asset, (src or "")[:8], (d or "")[:8], raw / (1e9 if asset in ("SOL", "WSOL") else 1e6)) for k, asset, mint, src, d, raw, dec in x["moves"] if asset != "other"][:6])
                print("     journaux", [m[:70] for m in (t["meta"].get("logMessages") or []) if "Program log" in m][:5])
for p, c in dst.items():
    print(p, "destinations", [(k[0], (label(k[0]) or "")[:12], k[1], round(v, 2)) for k, v in c.most_common(10)])
