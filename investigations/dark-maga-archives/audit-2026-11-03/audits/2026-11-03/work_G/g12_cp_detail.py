#!/usr/bin/env python3
"""Détail, depuis net_flows, de tous les virements vers ou depuis une contrepartie. usage : g12_cp_detail.py <adresse> [--tx]"""
import duckdb, sys
from dmaga.labels import label
G = "/Volumes/VERBATIM HD/Dark-MAGA-Investigation/audits_work/G/"
con = duckdb.connect(":memory:", config={"memory_limit": "300MB", "threads": 1, "temp_directory": G + "duck"})
con.execute("SET TimeZone='UTC'")
a = sys.argv[1]
rows = con.execute(f"""SELECT owner,dir,asset,pure,count(*) n,sum(amt) s,strftime(to_timestamp(min(bt)),'%Y-%m-%d %H:%M') x,strftime(to_timestamp(max(bt)),'%Y-%m-%d %H:%M') y FROM read_parquet('{G}net_flows.parquet') WHERE cp=? GROUP BY 1,2,3,4 ORDER BY asset,dir,s DESC""", [a]).fetchall()
print("wallets", len({r[0] for r in rows}))
agg = {}
for r in rows:
    k = (r[2], r[1], r[3]); agg[k] = agg.get(k, 0) + r[5]
print("totaux", {k: round(v, 2) for k, v in agg.items()})
for r in rows: print(r[0], r[1], r[2], "pur" if r[3] else "med", r[4], round(r[5], 3), r[6], r[7])
if "--tx" in sys.argv:
    for r in con.execute(f"""SELECT strftime(to_timestamp(bt),'%Y-%m-%d %H:%M:%S'),owner,dir,asset,amt,pure,sig FROM read_parquet('{G}net_flows.parquet') WHERE cp=? ORDER BY bt""", [a]).fetchall(): print(r)
