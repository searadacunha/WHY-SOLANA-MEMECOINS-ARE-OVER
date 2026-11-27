#!/usr/bin/env python3
"""Affiche une chronologie filtree. usage: c05_show.py <prefixe> [--payer] [--minsol X] [--dmaga] [--since ISO] [--until ISO]"""
import csv, sys
a=sys.argv
pref=a[1]; payer='--payer' in a; dmaga='--dmaga' in a
minsol=float(a[a.index('--minsol')+1]) if '--minsol' in a else None
since=a[a.index('--since')+1] if '--since' in a else ''
until=a[a.index('--until')+1] if '--until' in a else '9'
n=m=0
for r in csv.DictReader(open(f"chrono_{pref}.csv")):
    n+=1
    if not (since<=r['utc']<=until): continue
    keep=True
    if payer or dmaga or minsol is not None:
        keep=(payer and r['payer'].startswith(pref)) or (dmaga and r['dmaga_delta_seed']!='0') or (minsol is not None and abs(int(r['sol_delta']))>=minsol*1e9)
    if not keep: continue
    m+=1
    pr=[p[:10] for p in r['programs'].split('|') if p not in('cb','system','spl','ata')]
    print(r['utc'],r['sig'][:10],'P' if r['payer'].startswith(pref) else 'p:'+r['payer'][:6],f"sol={int(r['sol_delta'])/1e9:+.4f}",f"dm={int(r['dmaga_delta_seed'])/1e6:+,.0f}", 'in='+r['sys_in'][:90] if r['sys_in'] else '', 'out='+r['sys_out'][:150] if r['sys_out'] else '', 'oth='+r['other_token_deltas'][:70] if r['other_token_deltas'] else '', ','.join(pr)[:60])
print('lignes',n,'affichees',m)
