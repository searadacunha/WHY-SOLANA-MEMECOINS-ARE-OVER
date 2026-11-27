#!/usr/bin/env python3
"""Grand livre par wallet : virements purs et médiés, par contrepartie et actif, depuis net_moves. Sortie : work_G/g04_ledger.csv (une ligne par wallet, sens, actif, contrepartie)
et net_balance.csv (delta natif total, deltas de jetons, sommes signées, ruptures)."""
import duckdb, csv
from dmaga.labels import label
G = "/Volumes/VERBATIM HD/Dark-MAGA-Investigation/audits_work/G/"
OUT = "audits/2026-11-03/work_G/"
con = duckdb.connect(":memory:", config={"memory_limit": "800MB", "threads": 2, "temp_directory": G + "duck", "preserve_insertion_order": False})
con.execute("SET TimeZone='UTC'")
con.execute(f"CREATE TABLE m AS SELECT * FROM read_csv('{G}net_moves.csv.gz', header=true, types={{'raw':'DOUBLE','decimals':'VARCHAR','src':'VARCHAR','dst':'VARCHAR','sig':'VARCHAR'}}) WHERE err=0")
con.execute("""CREATE TABLE f AS
 SELECT owner,'out' dir,dst cp,asset,mint,CASE WHEN asset='SOL' OR asset='WSOL' THEN raw/1e9 WHEN asset IN ('USDC','USDT','DMAGA') THEN raw/1e6 ELSE raw END amt,bt,sig,pure,signed,kind FROM m WHERE src=owner AND dst<>owner
 UNION ALL SELECT owner,'in' dir,src cp,asset,mint,CASE WHEN asset='SOL' OR asset='WSOL' THEN raw/1e9 WHEN asset IN ('USDC','USDT','DMAGA') THEN raw/1e6 ELSE raw END amt,bt,sig,pure,signed,kind FROM m WHERE dst=owner AND src<>owner""")
con.execute(f"COPY f TO '{G}net_flows.parquet' (FORMAT PARQUET)")
rows = con.execute("""SELECT owner,dir,asset,cp,pure,count(*) n,sum(amt) amt,strftime(to_timestamp(min(bt)),'%Y-%m-%d %H:%M:%S') a,strftime(to_timestamp(max(bt)),'%Y-%m-%d %H:%M:%S') b,min(sig) ex,min(signed) sgn
 FROM f WHERE asset IN ('SOL','WSOL','USDC','USDT','DMAGA') GROUP BY 1,2,3,4,5 ORDER BY owner,dir,asset,amt DESC""").fetchall()
with open(OUT + "g04_ledger.csv", "w", newline="") as fh:
    w = csv.writer(fh); w.writerow("owner dir asset cp label pure n amt first last sig_ex".split())
    for r in rows: w.writerow([r[0], r[1], r[2], r[3], label(r[3]) or "", r[4], r[5], r[6], r[7], r[8], r[9]])
print("lignes", len(rows))
