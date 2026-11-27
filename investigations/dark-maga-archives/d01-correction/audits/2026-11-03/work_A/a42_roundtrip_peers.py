#!/usr/bin/env python3
"""Auditeur A. Allers-retours rapides (<= 10 s, même propriétaire) dans les fenêtres du test, DMAGA contre pairs. Mesure d'effet seulement, le protocole gelé n'est pas changé."""
import csv
import numpy as np, duckdb
A = "/Volumes/VERBATIM HD/Dark-MAGA-Investigation/audits_work/A"
ROOT = "REDACTED_HOME/Projects/Dark-MAGA-Investigation"
OUT = ROOT + "/audits/2026-11-03/work_A/out"
DP = "CRSwXnfF21yHDXdYBVWwCwQ5Ni2A4QuK3qGYis5k7x7k"
H = 3600
FLOOR = 1e8
con = duckdb.connect(":memory:", config={"memory_limit": "500MB", "threads": 2, "temp_directory": A + "/duck42"})
prim = [r for r in csv.DictReader(open(ROOT + "/etude_final/derived/metrics.csv")) if r["variant"] == "primary"]
res = {}
for r in prim:
    p, S = r["pool"], int(r["S"])
    tb = con.execute(f"""SELECT t, qty, sol, (qty>0 AND sol<0 AND lead(qty) OVER w < 0 AND lead(t) OVER w - t <= 10) rt FROM read_parquet('{A}/a03_lines.parquet') WHERE pool=? AND t<? AND t>=? WINDOW w AS (PARTITION BY owner ORDER BY slot, tx_index)""", [p, S, S - 96 * H]).fetchnumpy()
    t, q, s, rt = tb["t"], tb["qty"], tb["sol"].astype(float), tb["rt"]
    rt = np.nan_to_num(np.asarray(rt, dtype=float), nan=0.0).astype(bool)
    buy = (q > 0) & (s < 0)
    a = np.where(buy, -s, 0.0)
    b = np.where(buy & ~rt, -s, 0.0)
    def med(am, width, lo, hi):
        v, e = [], hi
        while e - width >= lo:
            v.append(am[(t >= e - width) & (t < e)].sum())
            e -= width
        return float(np.median(v)) if v else 0.0
    def m(am):
        return am[t >= S - 3 * H].sum() / max(med(am, 3 * H, S - 75 * H, S - 3 * H), FLOOR), am[t >= S - 24 * H].sum() / max(med(am, 24 * H, S - 96 * H, S - 24 * H), FLOOR)
    M1a, M2a = m(a)
    M1b, M2b = m(b)
    w = t >= S - 24 * H
    tot = a[w].sum()
    res[p] = dict(share_rt_24=(a[w].sum() - b[w].sum()) / tot if tot else 0.0, M1=M1a, M2=M2a, M1_sans_rt=M1b, M2_sans_rt=M2b)
ctrl = [p for p in res if p != DP]
with open(OUT + "/a42_roundtrip_peers.txt", "w") as f:
    for k in ("share_rt_24", "M1", "M1_sans_rt", "M2", "M2_sans_rt"):
        v = np.array([res[p][k] for p in ctrl])
        tg = res[DP][k]
        print(k, "DMAGA", round(tg, 4), "médiane", round(float(np.median(v)), 4), "p90", round(float(np.percentile(v, 90)), 4), "rang p", round((1 + (v >= tg).sum()) / (len(v) + 1), 4), file=f)
print("fini")
