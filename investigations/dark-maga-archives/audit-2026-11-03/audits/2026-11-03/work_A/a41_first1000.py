#!/usr/bin/env python3
"""Auditeur A. Les 1 000 premiers acheteurs de EARLY_BUYERS contre le parseur propre : membres, ordre, slot, montant du premier achat."""
import re, duckdb
ROOT = "REDACTED_HOME/Projects/Dark-MAGA-Investigation"
A = "/Volumes/VERBATIM HD/Dark-MAGA-Investigation/audits_work/A"
con = duckdb.connect(":memory:", config={"memory_limit": "300MB", "threads": 2, "temp_directory": A + "/duck41", "preserve_insertion_order": False})
rows = re.findall(r"\| (\d+) \| `(\w+)` \| (\d{9}) \| (\d\d/\d\d \d\d:\d\d:\d\d) \| ([\d ,]+) \|", open(ROOT + "/reports/EARLY_BUYERS.md").read())
print("lignes lues", len(rows))
own = con.execute(f"SELECT owner, min(slot) s, arg_min(-sol, (slot, tx_index))/1e9 first_sol FROM read_parquet('{A}/a15_leg.parquet') WHERE dmaga>0 GROUP BY 1 ORDER BY 2 LIMIT 1200").fetchall()
pos = {o: (i + 1, s, x) for i, (o, s, x) in enumerate(own)}
miss, diff_slot, diff_sol = [], 0, 0
for r, o, slot, t, sol in rows:
    v = pos.get(o)
    if v is None:
        miss.append((int(r), o))
        continue
    if v[1] != int(slot):
        diff_slot += 1
    if abs(v[2] - float(sol.replace(" ", "").replace(",", "."))) > 0.0011:
        diff_sol += 1
print("absents du propre", len(miss), miss[:6], "slot différent", diff_slot, "montant du premier achat différent", diff_sol)
