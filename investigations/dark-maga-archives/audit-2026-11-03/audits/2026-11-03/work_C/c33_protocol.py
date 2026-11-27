#!/usr/bin/env python3
"""Controle protocole en lecture : selection.jsonl contre le plan (population, amendement 001), metrics.csv recalcule en rang, recalcule p et Holm."""
import csv, json, collections, sys, os, time
from pathlib import Path
BIG=Path("/Volumes/VERBATIM HD/Dark-MAGA-Investigation/data/controls")
ROOT=Path("REDACTED_HOME/Projects/Dark-MAGA-Investigation")
for f in sorted(BIG.iterdir()):
    if f.name.startswith('._'): continue
    print(f.name, f.stat().st_size if f.is_file() else 'dir', time.strftime('%Y-%m-%d %H:%M:%S',time.gmtime(f.stat().st_mtime)))
rows=[json.loads(x) for x in (BIG/'selection.jsonl').read_text().splitlines()]
c=collections.Counter(r['status'] for r in rows); print(len(rows),c)
BAND=(100_000,10_000_000)
prim=[r for r in rows if r.get('S20') and r.get('fdv_s20') is not None and BAND[0]<=r['fdv_s20']<=BAND[1]]
print('primaire au sens du plan',len(prim),collections.Counter(r['status'] for r in prim))
print('primaire tronque',sum(1 for r in prim if r.get('truncated')))
trsans=[r for r in rows if r.get('tronque_sans_S20')]; print('tronque_sans_S20',len(trsans),collections.Counter(r['status'] for r in trsans))
dm=[r for r in rows if r['pool']=='CRSwXnfF21yHDXdYBVWwCwQ5Ni2A4QuK3qGYis5k7x7k'][0]; print('DMAGA',{k:dm[k] for k in dm if k not in('hist',)})
mig=[json.loads(x) for x in (BIG/'migrations.jsonl').read_text().splitlines()]; ts=[m.get('t') or m.get('created') or m.get('blockTime') for m in mig]
print('migrations',len(mig),list(mig[0].keys()),min(ts),max(ts),time.strftime('%Y-%m-%d %H:%M:%S',time.gmtime(min(ts))),time.strftime('%Y-%m-%d %H:%M:%S',time.gmtime(max(ts))))
m=list(csv.DictReader(open(ROOT/'etude_final/derived/metrics.csv')))
vc=collections.Counter(r['variant'] for r in m); print(vc)
p=[r for r in m if r['variant']=='primary']; d=[r for r in p if r['pool']==dm['pool']][0]; o=[r for r in p if r['pool']!=dm['pool']]
print('k',len(o),'jours',len({int(r['S'])//86400 for r in o}))
ps={}
for k in ['M1','M2','M3','M4','M5','M6','M7']:
    v=[float(r[k]) for r in o if r[k] not in('','nan')]
    ps[k]=(1+sum(1 for x in v if x>=float(d[k])))/(len(v)+1)
    print(k,round(float(d[k]),3),round(ps[k],4),'rang',1+sum(1 for x in v if x>=float(d[k])))
print('meilleur p',min(ps.values()),'rang',min(1+sum(1 for r in o if float(r[k] or 'nan')>=float(d[k])) for k in ps))
print('Holm seuil 0.05/7',0.05/7)
# createur double ? comparateurs par mint unique
print('mints uniques',len({r['mint'] for r in p}),'pools uniques',len({r['pool'] for r in p}))
print('hist selection fenetre plan: created min/max',time.strftime('%Y-%m-%d',time.gmtime(min(int(r['created']) for r in p))),time.strftime('%Y-%m-%d',time.gmtime(max(int(r['created']) for r in p))))
print('DMAGA S',d['S'],'created',d['created'],'fdv',d['fdv_usd'],'n_swaps',d['n_swaps_96h'],'n_buyers',d['n_buyers_24h'])
print('fdv hors bande primary',sum(1 for r in p if not BAND[0]<=float(r['fdv_usd'])<=BAND[1]))
