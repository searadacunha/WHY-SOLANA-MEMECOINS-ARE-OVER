#!/usr/bin/env python3
"""Vue d'ensemble : contreparties de virements purs (SOL, USDC, USDT, WSOL, DMAGA) sur les historiques complets. Sortie : work_G/g03_cp.csv, work_G/g03_cp.txt."""
import duckdb, csv, sys
G = "/Volumes/VERBATIM HD/Dark-MAGA-Investigation/audits_work/G/"
OUT = "audits/2026-11-03/work_G/"
sys.stdout = open(OUT + "g03_cp.txt", "w")
from dmaga.labels import label
con = duckdb.connect(":memory:", config={"memory_limit": "800MB", "threads": 2, "temp_directory": G + "duck", "preserve_insertion_order": False})
con.execute("SET TimeZone='UTC'")
con.execute(f"CREATE TABLE m AS SELECT * FROM read_csv('{G}net_moves.csv.gz', header=true, types={{'raw':'DOUBLE','decimals':'VARCHAR','src':'VARCHAR','dst':'VARCHAR','sig':'VARCHAR'}}, ignore_errors=false) WHERE err=0")
print("lignes", con.execute("SELECT count(*), count(DISTINCT owner), count(DISTINCT sig) FROM m").fetchone())
print(con.execute("SELECT asset,kind,pure,count(*),round(sum(raw)/1e9,1) FROM m GROUP BY 1,2,3 ORDER BY 1,2,3").fetchall())
con.execute("""CREATE TABLE f AS
 SELECT owner,'out' dir,dst cp,asset,raw,bt,sig,pure,kind FROM m WHERE src=owner AND dst<>owner
 UNION ALL SELECT owner,'in' dir,src cp,asset,raw,bt,sig,pure,kind FROM m WHERE dst=owner AND src<>owner""")
q = con.execute("""SELECT cp, count(DISTINCT owner) n_owners, count(*) n, sum(CASE WHEN asset='SOL' AND dir='out' THEN raw END)/1e9 sol_out, sum(CASE WHEN asset='SOL' AND dir='in' THEN raw END)/1e9 sol_in,
 sum(CASE WHEN asset IN ('USDC','USDT') AND dir='out' THEN raw END)/1e6 usd_out, sum(CASE WHEN asset IN ('USDC','USDT') AND dir='in' THEN raw END)/1e6 usd_in,
 strftime(to_timestamp(min(bt)),'%Y-%m-%d') first, strftime(to_timestamp(max(bt)),'%Y-%m-%d') last, avg(pure) pure_part FROM f WHERE pure=1 GROUP BY 1 ORDER BY greatest(coalesce(sol_out,0),coalesce(sol_in,0)) DESC""").fetchall()
with open(OUT + "g03_cp.csv", "w", newline="") as fh:
    w = csv.writer(fh); w.writerow("cp label n_owners n sol_out sol_in usd_out usd_in first last pure".split())
    for r in q: w.writerow([r[0], label(r[0]) or "", *r[1:]])
print("contreparties", len(q))
for r in q[:90]:
    print(r[0], (label(r[0]) or "-")[:30], r[1], r[2], *(round(x or 0, 1) for x in r[3:7]), str(r[7])[:10], str(r[8])[:10], round(r[9], 2))
