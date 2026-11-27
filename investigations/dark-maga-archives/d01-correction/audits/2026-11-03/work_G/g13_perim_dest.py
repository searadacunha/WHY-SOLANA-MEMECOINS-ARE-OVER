#!/usr/bin/env python3
"""Destinations pures de SOL et USD stables pour le périmètre (créateur, série 15, expéditeurs 9W9b, g33, nommés) depuis net_flows. Sortie : g13_perim_dest.csv/.txt"""
import csv, sys, duckdb, collections
from dmaga.labels import label
G = "/Volumes/VERBATIM HD/Dark-MAGA-Investigation/audits_work/G/"; OUT = "audits/2026-11-03/work_G/"
sys.stdout = open(OUT + "g13_perim_dest.txt", "w")
con = duckdb.connect(":memory:", config={"memory_limit": "500MB", "threads": 2, "temp_directory": G + "duck"})
roles = {r["wallet"]: r["roles"] for r in csv.DictReader(open(OUT + "targets.csv"))}
con.execute("CREATE TABLE t(a VARCHAR, r VARCHAR)"); con.executemany("INSERT INTO t VALUES (?,?)", list(roles.items()))
F = f"read_parquet('{G}net_flows.parquet')"
for asset, cond in (("USD", "asset IN ('USDC','USDT')"), ("SOL", "asset='SOL'"), ("DMAGA", "asset='DMAGA'")):
    rows = con.execute(f"""SELECT cp,count(DISTINCT owner) ns,count(*) n,sum(amt) s,strftime(to_timestamp(min(bt)),'%Y-%m-%d') a,strftime(to_timestamp(max(bt)),'%Y-%m-%d') b,string_agg(DISTINCT substr(owner,1,6),',') FROM {F} f WHERE dir='out' AND pure=1 AND {cond} AND amt>=(CASE WHEN asset='DMAGA' THEN 1000 WHEN asset='SOL' THEN 0.01 ELSE 1 END) AND owner IN (SELECT a FROM t) GROUP BY 1 ORDER BY s DESC""").fetchall()
    tot = sum(r[3] for r in rows)
    print("==", asset, "destinations", len(rows), "total", round(tot, 2))
    for r in rows[:45]:
        print(r[0], (label(r[0]) or "-")[:16], "T" if r[0] in roles else "-", "ns", r[1], "n", r[2], round(r[3], 1), r[4], r[5], r[6][:60])
