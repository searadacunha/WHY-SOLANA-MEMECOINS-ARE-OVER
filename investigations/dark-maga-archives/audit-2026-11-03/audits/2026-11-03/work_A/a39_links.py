#!/usr/bin/env python3
"""Auditeur A. Services non étiquetés dans link_edges : 4ToQp55m, comptes en tx DCA, comptes en programmes bots. Top des nœuds non étiquetés dans token_direct et sol_direct."""
import duckdb
A = "/Volumes/VERBATIM HD/Dark-MAGA-Investigation/audits_work/A"
B = "/Volumes/VERBATIM HD/Dark-MAGA-Investigation/data"
con = duckdb.connect(":memory:", config={"memory_limit": "400MB", "threads": 2, "temp_directory": A + "/duck39", "preserve_insertion_order": False})
L = f"read_parquet('{B}/link_edges.parquet')"
def show(n, s, *a):
    print(n, con.execute(s, *a).fetchall(), flush=True)
for o in ("4ToQp55myvfpeprgKuqGbDqyji9Ezm7CZg7QbcTpL33S", "CpoD6tWAsMDeyvVG2q2rD1JbDY6d4AujnvAn2NdrhZV2", "9nX7k7FQ4zgCMLfqi6hoTWHyVjCKWFEi4UBZK4Z9JfdT", "5V97uEb4ZNuXFudphU5nwUapRmt7a2V51TbULQvPJwnx", "AD65fgYti96iSSzSPaNazV9Bs29m7JbNomGjG4Cp5WFS", "425DZohsnqJjyMtMe2XfHsEuiAf9xBRAqsGSGsH8PKdc"):
    show(o[:10] + " dans link_edges", f"SELECT type, count(*) FROM {L} WHERE src=? OR dst=? GROUP BY 1", [o, o])
show("degré le plus élevé en token_direct et sol_direct", f"""SELECT a, count(DISTINCT b) n FROM (SELECT src a, dst b FROM {L} WHERE type IN ('token_direct','sol_direct') UNION ALL SELECT dst, src FROM {L} WHERE type IN ('token_direct','sol_direct')) GROUP BY 1 ORDER BY n DESC LIMIT 15""")
