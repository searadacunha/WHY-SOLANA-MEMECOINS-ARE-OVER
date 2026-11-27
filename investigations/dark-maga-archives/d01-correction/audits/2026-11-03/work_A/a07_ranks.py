#!/usr/bin/env python3
"""Auditeur A. Rangs recalculés depuis derived/metrics.csv (sans metrics.py) contre tables/tests.json, Holm et verdict. S'exécute sans lire le brut."""
import csv, json, statistics
ROOT = "REDACTED_HOME/Projects/Dark-MAGA-Investigation/etude_final"
DP = "CRSwXnfF21yHDXdYBVWwCwQ5Ni2A4QuK3qGYis5k7x7k"
rows = list(csv.DictReader(open(ROOT + "/derived/metrics.csv")))
T = json.load(open(ROOT + "/tables/tests.json"))
bad = 0
for v, c in T["variants"].items():
    r = [x for x in rows if x["variant"] == v]
    tg = [x for x in r if x["pool"] == DP][0]
    ct = [x for x in r if x["pool"] != DP]
    out = {}
    for m, d in c["mesures"].items():
        a = float(tg[m])
        vals = [float(x[m]) for x in ct if x[m] not in ("", "nan") and float(x[m]) == float(x[m])]
        p = (1 + sum(1 for y in vals if y >= a)) / (len(vals) + 1)
        out[m] = (round(a, 4), round(statistics.median(vals), 4), round(p, 4), sum(1 for y in vals if y >= a) + 1)
        if abs(p - d["p"]) > 1e-12 or abs(a - d["dmaga"]) > 1e-9 or d["k"] != len(vals):
            bad += 1
    print(v, "k", len(ct), "jours", len({int(x["S"]) // 86400 for x in ct}), out)
print("écarts avec tests.json", bad)
ps = {m: d["p"] for m, d in T["variants"]["primary"]["mesures"].items()}
o = sorted(ps, key=ps.get)
print("Holm, plus petit p", ps[o[0]], "seuil 0,05/7", 0.05 / 7, "passe", ps[o[0]] <= 0.05 / 7, "rang min possible 1/212", 1 / 212, "2/212", 2 / 212, "Bonferroni 33", 0.05 / 33)
print("S1 holm", T.get("S1_holm"))
