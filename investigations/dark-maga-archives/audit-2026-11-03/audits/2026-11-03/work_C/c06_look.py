#!/usr/bin/env python3
"""Regarde les lignes non payeur du createur et les graines par categories"""
import csv, collections
rows=list(csv.DictReader(open('chrono_8YLEuU.csv')))
c=collections.Counter()
ex={}
for r in rows:
    if r['payer'].startswith('8YLE'): continue
    k=(r['programs'][:60], int(r['sol_delta'])!=0, r['dmaga_delta_seed']!='0', bool(r['other_token_deltas']))
    c[k]+=1; ex.setdefault(k,r)
for k,v in c.most_common(20):
    r=ex[k]; print(v,k,r['utc'],r['sig'],r['payer'][:8],r['sol_delta'],r['other_token_deltas'][:80],r['dmaga_moves'][:100])
oth=collections.Counter()
for r in rows:
    for x in r['other_token_deltas'].split(';'):
        if x: m,v=x.rsplit(':',1); oth[m]+=float(v)
print(oth.most_common(15))
print([r['utc'] for r in rows if 'pumpswap' in r['programs']][:2],[r['utc'] for r in rows if 'pumpswap' in r['programs']][-2:])
