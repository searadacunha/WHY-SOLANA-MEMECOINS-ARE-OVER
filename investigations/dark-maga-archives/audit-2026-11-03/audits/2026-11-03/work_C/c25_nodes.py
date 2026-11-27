#!/usr/bin/env python3
"""Profil de chaque noeud de la composante de 5QhJJc : tx, tx signees, contreparties toutes tailles, etiquette, jetons recus et envoyes hors AMM.
Sorties: nodes_comp.csv et composante affichee."""
import csv, collections, sys
from pathlib import Path
import duckdb
from dmaga.labels import label
ROOT='REDACTED_HOME/Projects/Dark-MAGA-Investigation/audits/2026-11-03/work_C/'
W="/Volumes/VERBATIM HD/Dark-MAGA-Investigation/audits_work/C"
EXC=set(Path(ROOT+'excl_blind.txt').read_text().split())
rows=[r for r in csv.DictReader(open(ROOT+'direct_edges_all.csv')) if r['src'] not in EXC and r['dst'] not in EXC]
adj=collections.defaultdict(set)
for r in rows: adj[r['src']].add(r['dst']);adj[r['dst']].add(r['src'])
SEED="5QhJJcFZu2ashyKyWSTGHcsyo6ZBCbpVuJqeutvQHScd"
seen={SEED};st=[SEED]
while st:
    x=st.pop()
    for y in adj[x]:
        if y not in seen: seen.add(y);st.append(y)
con=duckdb.connect(); con.execute(f"SET memory_limit='250MB'; SET threads=1; SET TimeZone='UTC'; SET temp_directory='{W}/tmp';")
con.execute("CREATE TEMP TABLE n(a VARCHAR)"); con.executemany("INSERT INTO n VALUES (?)",[(a,) for a in seen])
pr={r[0]:r[1:] for r in con.execute(f"SELECT owner,n_tx,n_signed FROM '{W}/owner_profile.parquet' WHERE owner IN (SELECT a FROM n)").fetchall()}
ind=dict(con.execute(f"SELECT dst_o,count(DISTINCT src_o) FROM '{W}/xfer.parquet' WHERE dst_o IN (SELECT a FROM n) GROUP BY 1").fetchall())
oud=dict(con.execute(f"SELECT src_o,count(DISTINCT dst_o) FROM '{W}/xfer.parquet' WHERE src_o IN (SELECT a FROM n) GROUP BY 1").fetchall())
w=csv.writer(open(ROOT+'nodes_comp.csv','w',newline='')); w.writerow('node deg_ge1M n_tx n_signed in_all out_all label'.split())
for a in sorted(seen,key=lambda a:-len(adj[a])):
    p=pr.get(a,(0,0))
    w.writerow([a,len(adj[a]),p[0],p[1],ind.get(a,0),oud.get(a,0),label(a) or ''])
print('noeuds',len(seen))
for a in sorted(seen,key=lambda a:-ind.get(a,0))[:25]:
    print(a[:10],'deg',len(adj[a]),'tx',pr.get(a,(0,0)),'in_all',ind.get(a,0),'out_all',oud.get(a,0),label(a) or '')
