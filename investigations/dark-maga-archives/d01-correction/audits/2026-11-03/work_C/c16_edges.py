#!/usr/bin/env python3
"""Tri des transferts >= 1 M : proprietaires a fort volume, tx sans AMM, composantes depuis les graines."""
import csv, collections, sys
TH=sys.argv[1] if len(sys.argv)>1 else '1'
rows=list(csv.DictReader(open(f'cand_edges_{TH}M.csv')))
print('lignes',len(rows),'avec amm',sum(r['has_amm']=='True' for r in rows))
na=[r for r in rows if r['has_amm']=='False']
print('sans amm',len(na))
print('programmes top (sans amm)',collections.Counter(r['programs'][:120] for r in na).most_common(12))
deg=collections.Counter()
for r in na: deg[r['src']]+=1; deg[r['dst']]+=1
print('owners forts degre',[ (k,v) for k,v in deg.most_common(25)])
print('src vide',sum(1 for r in na if not r['src']),'dst vide',sum(1 for r in na if not r['dst']))
print('auth != src',sum(1 for r in na if r['authority']!=r['src']))
for r in na[:6]: print(r['utc'],r['sig'][:12],r['src'][:8],r['dst'][:8],int(r['amount'])/1e6,r['authority'][:8],r['programs'][:80],r['kind'],r['ord'],r['src_ntx'],r['src_nsig'],r['dst_ntx'],r['dst_nsig'])
