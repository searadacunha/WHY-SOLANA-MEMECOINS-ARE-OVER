#!/usr/bin/env python3
"""Chronologie brute d'un wallet depuis net_flows (virements ≥ seuil, purs et médiés). usage : g34_chrono.py <addr> [n lignes] [seuil SOL] [--from AAAA-MM-JJ]"""
import sys, time, duckdb, calendar
G = "/Volumes/VERBATIM HD/Dark-MAGA-Investigation/audits_work/G/"
a = sys.argv[1]; n = int(sys.argv[2]) if len(sys.argv) > 2 else 25; th = float(sys.argv[3]) if len(sys.argv) > 3 else 0.01
frm = 0
if "--from" in sys.argv: frm = calendar.timegm(time.strptime(sys.argv[sys.argv.index("--from") + 1], "%Y-%m-%d"))
con = duckdb.connect(":memory:", config={"memory_limit": "200MB", "threads": 1, "temp_directory": G + "duck"})
con.execute("SET TimeZone='UTC'")
print(con.execute(f"SELECT count(*),count(DISTINCT sig),strftime(to_timestamp(min(bt)),'%Y-%m-%d'),strftime(to_timestamp(max(bt)),'%Y-%m-%d') FROM '{G}net_flows.parquet' WHERE owner=?", [a]).fetchone())
for r in con.execute(f"""SELECT strftime(to_timestamp(bt),'%Y-%m-%d %H:%M:%S'),dir,asset,round(amt,4),cp,pure,substr(sig,1,14) FROM '{G}net_flows.parquet' WHERE owner=? AND bt>={frm} AND asset IN ('SOL','USDC','USDT','DMAGA','WSOL') AND ((asset IN ('SOL','WSOL') AND amt>=?) OR (asset IN ('USDC','USDT') AND amt>=1) OR (asset='DMAGA' AND amt>=1000)) ORDER BY bt LIMIT ?""", [a, th, n]).fetchall(): print(*r)
