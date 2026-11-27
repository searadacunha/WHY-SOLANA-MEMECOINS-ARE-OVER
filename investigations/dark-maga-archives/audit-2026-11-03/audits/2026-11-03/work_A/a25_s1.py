#!/usr/bin/env python3
"""Auditeur A. Test secondaire S1 refait sur le parseur propre, avec la règle du plan puis avec tout le SOL entré au vault. Compare à tables/tests.json."""
import json
import numpy as np, duckdb
A = "/Volumes/VERBATIM HD/Dark-MAGA-Investigation/audits_work/A"
ROOT = "REDACTED_HOME/Projects/Dark-MAGA-Investigation"
DP = "CRSwXnfF21yHDXdYBVWwCwQ5Ni2A4QuK3qGYis5k7x7k"
H = 3600
CREATED = 1720923331
con = duckdb.connect(":memory:", config={"memory_limit": "300MB", "threads": 1, "temp_directory": A + "/duck25"})
d = con.execute(f"SELECT t, slot, tx_index, owner, qty, sol FROM read_parquet('{A}/a03_lines.parquet') WHERE pool=? ORDER BY slot, tx_index", [DP]).fetchnumpy()
v = con.execute(f"SELECT t, ds, dt, n_lines FROM read_parquet('{A}/a03_tx.parquet') WHERE pool=? AND kind='swap'", [DP]).fetchnumpy()
t, own, q, s = d["t"], d["owner"], d["qty"], d["sol"]
buy = (q > 0) & (s < 0)
amt = np.where(buy, -s.astype(float), 0.0) / 1e9
tv, ds, dt = v["t"], v["ds"].astype(float), v["dt"].astype(float)
av = np.where((ds > 0) & (dt < 0), ds, 0.0) / 1e9
first = {}
for o, x in zip(own.tolist(), t.tolist()):
    first.setdefault(o, x)
rep = json.load(open(ROOT + "/etude_final/tables/tests.json"))["S1"]
for name, E in (("winig", 1721577749), ("avatar", 1721589800)):
    edges = []
    e = E - 3 * H
    while e >= CREATED + 96 * H:
        edges.append(e)
        e -= 3 * H
    so = np.array([amt[(t >= e) & (t < e + 3 * H)].sum() for e in edges])
    sv = np.array([av[(tv >= e) & (tv < e + 3 * H)].sum() for e in edges])
    nw = np.array([len({o for o, x, b in zip(own.tolist(), t.tolist(), buy.tolist()) if b and e <= x < e + 3 * H and e <= first[o] < e + 3 * H}) for e in edges])
    p = lambda a: (1 + (a[1:] >= a[0]).sum()) / len(a)
    print(name, "fenêtres passées", len(edges) - 1, "SOL", round(so[0], 3), "médiane", round(float(np.median(so[1:])), 3), "p", round(p(so), 4), "nouveaux", int(nw[0]), "méd", float(np.median(nw[1:])), "p", round(p(nw), 4),
          "| vault entier SOL", round(sv[0], 3), "médiane", round(float(np.median(sv[1:])), 3), "p", round(p(sv), 4), "| rapport", {k: rep[name][k] for k in ("sol_achete", "mediane_sol_passe", "p_sol", "nouveaux_wallets", "p_new", "n_fenetres_passees")})
