#!/usr/bin/env python3
"""Principales destinations encore non qualifiées dans flow_boundaries.csv, par périmètre. Sortie g54.txt, probe_11.txt (liste à sonder, sans doublon ni historique déjà lu)."""
import csv, collections, os, sys
OUT = "audits/2026-11-03/work_G/"; G = "/Volumes/VERBATIM HD/Dark-MAGA-Investigation/audits_work/G/net/"
sys.stdout = open(OUT + "g54.txt", "w")
agg = collections.defaultdict(lambda: [0.0, 0, set(), "", ""])
for r in csv.DictReader(open(OUT + "flow_boundaries.csv")):
    if r["perimetre_source"] in ("hors périmètres", "balayage de dépôt") or r["actif"] == "DMAGA": continue
    t = r["type_frontiere"]
    if not (t.startswith("wallet non suivi") or t.startswith("wallet sondé")): continue
    k = (r["perimetre_source"].split()[0], r["destination"], t.split(" [")[0], "tronc" if "[" in t else "pur")
    e = agg[k]; e[0] += float(r["sol_eq"]); e[1] += int(r["n"]); e[2].add(r["wallet_source"][:6]); e[3] = min(e[3] or r["date_debut"], r["date_debut"]); e[4] = max(e[4], r["date_fin"])
per = collections.defaultdict(list)
for k, e in agg.items(): per[k[0]].append((k, e))
want = []
for p, L in per.items():
    L.sort(key=lambda x: -x[1][0])
    print("==", p, "total", round(sum(x[1][0] for x in L), 1), "destinations", len(L))
    for k, e in L[:22]:
        print(" ", k[1], k[2][:12], k[3], round(e[0], 1), "n", e[1], sorted(e[2])[:4], e[3][:10], e[4][:10])
        if k[3] == "pur" and e[0] >= 40 and k[2].startswith("wallet non suivi") and not os.path.exists(G + k[1] + ".jsonl.gz"): want.append(k[1])
open(OUT + "probe_11.txt", "w").write("\n".join(dict.fromkeys(want)) + "\n")
print("à sonder", len(set(want)))
