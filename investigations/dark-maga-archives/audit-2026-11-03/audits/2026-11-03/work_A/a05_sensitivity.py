#!/usr/bin/env python3
"""Auditeur A. Sensibilité des données : M1, M2 et le rang de DMAGA avec tout le SOL entré dans le vault (a03_tx), lignes exclues comprises ;
M1 à M7 sans les transactions dont la quantité attribuée diffère du vault de plus de 1 %. Ne change rien au protocole : mesure d'effet seulement."""
import csv, json
import numpy as np, duckdb
A = "/Volumes/VERBATIM HD/Dark-MAGA-Investigation/audits_work/A"
ROOT = "REDACTED_HOME/Projects/Dark-MAGA-Investigation"
OUT = ROOT + "/audits/2026-11-03/work_A/out"
DP = "CRSwXnfF21yHDXdYBVWwCwQ5Ni2A4QuK3qGYis5k7x7k"
H = 3600
FLOOR = 1e8
con = duckdb.connect(":memory:", config={"memory_limit": "600MB", "threads": 2, "temp_directory": A + "/duck05"})
prim = [r for r in csv.DictReader(open(ROOT + "/etude_final/derived/metrics.csv")) if r["variant"] == "primary"]
res = {}
for r in prim:
    p, S = r["pool"], int(r["S"])
    d = con.execute(f"SELECT t, ds, dt, sum_qty, n_lines, excl_two_sided FROM read_parquet('{A}/a03_tx.parquet') WHERE pool=? AND t<? AND t>=? AND kind='swap'", [p, S, S - 96 * H]).fetchnumpy()
    t, ds, dt, sq, nl, ex = d["t"], d["ds"].astype(float), d["dt"].astype(float), d["sum_qty"].astype(float), d["n_lines"], d["excl_two_sided"]
    buy = (ds > 0) & (dt < 0)
    amt = np.where(buy, ds, 0.0)
    def med(am, width, lo, hi):
        v, e = [], hi
        while e - width >= lo:
            v.append(am[(t >= e - width) & (t < e)].sum())
            e -= width
        return float(np.median(v)) if v else 0.0
    def ratios(am):
        return am[t >= S - 3 * H].sum() / max(med(am, 3 * H, S - 75 * H, S - 3 * H), FLOOR), am[t >= S - 24 * H].sum() / max(med(am, 24 * H, S - 96 * H, S - 24 * H), FLOOR)
    M1v, M2v = ratios(amt)
    # sans lignes : SOL entré au vault sans aucun bénéficiaire retenu, et SOL dont la quantité diffère du vault
    w24 = t >= S - 24 * H
    lost = amt[w24 & (nl == 0)].sum()
    diff = amt[w24 & (nl > 0) & (np.abs(np.abs(sq) - np.abs(dt)) > 0.01 * np.abs(dt))].sum()
    tot = amt[w24].sum()
    res[p] = dict(M1=float(r["M1"]), M2=float(r["M2"]), M1v=M1v, M2v=M2v, lost=lost / tot if tot else 0.0, diff=diff / tot if tot else 0.0, tot=tot / 1e9)
ctrl = [p for p in res if p != DP]
out = open(OUT + "/a05_sensitivity.txt", "w")
for k in ("M1", "M1v", "M2", "M2v", "lost", "diff", "tot"):
    v = np.array([res[p][k] for p in ctrl])
    tg = res[DP][k]
    print(k, "DMAGA", round(tg, 4), "médiane pairs", round(float(np.median(v)), 4), "p90", round(float(np.percentile(v, 90)), 4), "rang p", round((1 + (v >= tg).sum()) / (len(v) + 1), 4), file=out)
w = csv.writer(open(OUT + "/a05_sensitivity.csv", "w", newline=""))
w.writerow(["pool", *next(iter(res.values())).keys()])
for p, x in res.items():
    w.writerow([p, *x.values()])
out.close()
print("fini")
