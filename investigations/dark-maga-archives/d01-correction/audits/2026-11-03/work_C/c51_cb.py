#!/usr/bin/env python3
"""Fenetre des retraits Coinbase avant le mint : qui recoit de 01:00 a 02:06 UTC le 14/07/2024, combien d'autres wallets, montants, lesquels achetent DMAGA.
Sortie cb_window.csv. Credits comptes."""
import csv, json, time, gzip
from pathlib import Path
import duckdb
from dmaga.helius import Helius
W="/Volumes/VERBATIM HD/Dark-MAGA-Investigation/audits_work/C"
ROOT=Path(__file__).resolve().parent
T0=1720922725
HOT={"H8sMJSCQxfKiFTCfDR3DUMLPwcRbM61LGFJ8N4dK3WjS":"Coinbase1","2AQdpHJ2JpcEgPiATUXjQxA8QmafFegfQwSLWSprPicm":"Coinbase2","GJRs4FwHtemZ5ZE9x3FNvJ8TMwitKTh21yxdRPqn7npE":"Coinbase3"}
h=Helius()
out=[]; pages=0
for hot,name in HOT.items():
    tok=None
    for _ in range(40):
        r=h.txs_page(hot,details="full",limit=100,sort="asc",token=tok,filters={"blockTime":{"gte":T0-7200,"lt":T0+60},"status":"succeeded"})
        pages+=1
        for tx in r["data"]:
            for i in tx["transaction"]["message"]["instructions"]:
                p=i.get("parsed")
                if i.get("program")=="system" and isinstance(p,dict) and p.get("type")=="transfer" and p["info"].get("source")==hot:
                    out.append((tx["blockTime"],name,p["info"]["destination"],int(p["info"]["lamports"]),tx["transaction"]["signatures"][0]))
        tok=r.get("paginationToken")
        if not tok: break
with open(ROOT/"credits.csv","a") as f:
    f.write(f"{time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime())},gtfa_full_x{pages},coinbase_window,{pages*10}\n")
print('pages',pages,'retraits',len(out))
con=duckdb.connect(); con.execute(f"SET memory_limit='250MB'; SET threads=1; SET temp_directory='{W}/tmp';")
con.execute("CREATE TEMP TABLE d(a VARCHAR)"); con.executemany("INSERT INTO d VALUES (?)",[(x[2],) for x in out])
own={r[0]:r[1] for r in con.execute(f"SELECT owner,n_tx FROM '{W}/owner_profile.parquet' WHERE owner IN (SELECT a FROM d)").fetchall()}
w=csv.writer(open(ROOT/"cb_window.csv","w",newline="")); w.writerow("utc hot dest sol sig dmaga_tx".split())
for x in sorted(out):
    w.writerow([time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime(x[0])),x[1],x[2],x[3]/1e9,x[4],own.get(x[2],0)])
print('destinataires',len({x[2] for x in out}),'avec DMAGA',len({x[2] for x in out if x[2] in own}))
for x in sorted(out):
    if x[2] in own: print(time.strftime('%H:%M:%S',time.gmtime(x[0])),x[1],x[2],x[3]/1e9,own[x[2]])
n105=[x for x in out if x[3]==1050000000]; print('retraits exacts 1,05 SOL',len(n105),[(time.strftime('%H:%M:%S',time.gmtime(x[0])),x[1],x[2][:8],x[2] in own) for x in n105])
n05=[x for x in out if x[3]==500000000]; print('retraits exacts 0,5 SOL',len(n05),[(time.strftime('%H:%M:%S',time.gmtime(x[0])),x[2][:8],x[2] in own) for x in n05][:30])
