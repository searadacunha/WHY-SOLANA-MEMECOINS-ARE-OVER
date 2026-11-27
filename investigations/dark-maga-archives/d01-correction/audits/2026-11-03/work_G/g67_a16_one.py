#!/usr/bin/env python3
"""A-16 : nombre de jambes tierces par bloc, pour vérifier « exactement une ». Sortie g67.txt."""
import collections, sys
import duckdb
A = "/Volumes/VERBATIM HD/Dark-MAGA-Investigation/audits_work/A/"; G = "/Volumes/VERBATIM HD/Dark-MAGA-Investigation/audits_work/G/"
sys.stdout = open("audits/2026-11-03/work_G/g67.txt", "w")
SVC = "3GMsedVPsXjWR7HYUvwm1YUpvBC2bTgSkXixm4gMXnPk"
con = duckdb.connect(":memory:", config={"memory_limit": "700MB", "threads": 2, "temp_directory": G + "duck", "preserve_insertion_order": False})
con.execute(f"CREATE TABLE st AS SELECT signature FROM '{A}a15_tx.parquet' WHERE progs LIKE '%{SVC}%'")
con.execute(f"CREATE TABLE b AS SELECT slot sl,min(tx_index) a,max(tx_index) z,count(*) n FROM '{A}a15_leg.parquet' WHERE signature IN (SELECT signature FROM st) GROUP BY 1")
r = con.execute(f"""SELECT n3,count(*) FROM (SELECT b.sl,count(l.signature) n3 FROM b LEFT JOIN '{A}a15_leg.parquet' l ON l.slot=b.sl AND l.tx_index>b.a AND l.tx_index<b.z AND l.signature NOT IN (SELECT signature FROM st) GROUP BY 1) GROUP BY 1 ORDER BY 1""").fetchall()
print("jambes tierces par bloc, nombre de blocs", r)
print("écart d'index entre les deux jambes, nombre de blocs", con.execute("SELECT z-a,count(*) FROM b GROUP BY 1 ORDER BY 2 DESC LIMIT 6").fetchall())
