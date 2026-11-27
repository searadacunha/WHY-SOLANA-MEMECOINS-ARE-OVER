#!/usr/bin/env python3
"""Historiques tronqués (C à 1 200 tx) : jusqu'où vont-ils, et que voit le fichier raw/flows au-delà ? Puis programmes des sorties unilatérales (ponts, mixeurs) sur tout le périmètre. Sortie g36.txt"""
import csv, sys, time, collections, gzip
import duckdb
from dmaga.labels import label
OUT = "audits/2026-11-03/work_G/"; G = "/Volumes/VERBATIM HD/Dark-MAGA-Investigation/audits_work/G/"
sys.stdout = open(OUT + "g36.txt", "w")
iso = lambda t: time.strftime("%Y-%m-%d", time.gmtime(t))
con = duckdb.connect(":memory:", config={"memory_limit": "700MB", "threads": 2, "temp_directory": G + "duck", "preserve_insertion_order": False})
con.execute("SET TimeZone='UTC'")
SOLM = "So11111111111111111111111111111111111111111"
TR = [r["wallet"] for r in csv.DictReader(open(OUT + "targets.csv")) if r["net"] == "True" and r["net_complete"] != "True"]
stats = {}
for r in csv.DictReader(open(G + "net_stats.csv")): stats[r["owner"]] = r
for a in TR:
    if a.startswith("H9Xe"): continue
    last = int(stats[a]["last_bt"])
    rows = con.execute(f"""SELECT dst,mint,sum(raw),count(*) FROM (SELECT DISTINCT sig,src,dst,mint,raw,ins,inner_ FROM read_parquet('{G}flows_all.parquet') WHERE src=? AND bt>{last} AND mint IN ('{SOLM}','EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v','Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB')) GROUP BY 1,2 ORDER BY 3 DESC""", [a]).fetchall()
    s = sum(r[2] / 1e9 for r in rows if r[1] == SOLM); u = sum(r[2] / 1e6 for r in rows if r[1] != SOLM)
    print(a[:8], "n_net", stats[a]["n_tx"], "dernier", iso(last), "| au-delà dans raw/flows : SOL", round(s, 1), "USD", round(u, 1), "lignes", sum(r[3] for r in rows), "top", [(r[0][:8], (label(r[0]) or "")[:8], round(r[2] / (1e9 if r[1] == SOLM else 1e6), 1), "S" if r[1] == SOLM else "U") for r in rows[:6]])
# Sorties unilatérales : le wallet perd SOL ou USD sans recevoir de jeton dans la même tx, par un programme autre que le système
T = {r["wallet"] for r in csv.DictReader(open(OUT + "targets.csv"))}
con.execute("CREATE TABLE t(a VARCHAR)"); con.executemany("INSERT INTO t VALUES (?)", [[a] for a in T])
rows = con.execute(f"""SELECT programs,count(*),count(DISTINCT owner),sum(-native_delta)/1e9,sum(-(usdc_delta+usdt_delta))/1e6,min(sig),string_agg(DISTINCT substr(owner,1,6),',') FROM read_csv('{G}net_txs.csv.gz',header=true,types={{'programs':'VARCHAR','owner':'VARCHAR','sig':'VARCHAR','signers':'VARCHAR','payer':'VARCHAR'}})
 WHERE owner IN (SELECT a FROM t) AND pure=0 AND err=0 AND signed=1 AND n_other_mints=0 AND dmaga_delta=0 AND wsol_delta<=0 AND ((native_delta<-100000000 AND usdc_delta<=0 AND usdt_delta<=0) OR (usdc_delta+usdt_delta<-10000000 AND native_delta<=0 AND wsol_delta=0)) GROUP BY 1 ORDER BY 4 DESC LIMIT 40""").fetchall()
print("sorties unilatérales : programmes, tx, wallets, SOL, USD, exemple")
for r in rows: print(" ", [p[:14] for p in (r[0] or "").split(";")], r[1], r[2], round(r[3], 2), round(r[4], 1), r[5][:16], r[6][:50])
