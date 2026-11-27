#!/usr/bin/env python3
"""Bilan DMAGA de chaque graine depuis sa chronologie : achats, ventes, transferts, DCA. Ecrit seed_token_summary.csv."""
import csv,collections
ROOT='REDACTED_HOME/Projects/Dark-MAGA-Investigation/audits/2026-11-03/work_C/'
w=csv.writer(open(ROOT+'seed_token_summary.csv','w',newline='')); w.writerow('seed category n tokens_M sol_delta usdc_delta first last'.split())
USDC='EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v'
for pref in ('8YLEuU','5QhJJc','G41vRr','9W9b3z'):
    st=collections.defaultdict(lambda:[0,0,0,0,None,None])
    for r in csv.DictReader(open(ROOT+f'chrono_{pref}.csv')):
        d=int(r['dmaga_delta_seed'])
        if d==0: continue
        p=r['programs']
        amm=any(x in p for x in('raydium','jup6','jup4','meteora','orca','pumpswap','phoenix'))
        cat=('curve_buy' if 'pumpfun' in p and d>0 else 'curve_sell' if 'pumpfun' in p else
             'dca' if 'jup_dca' in p else
             'amm_buy' if amm and d>0 else 'amm_sell' if amm else
             'transfer_in' if d>0 else 'transfer_out')
        s=st[cat]; s[0]+=1; s[1]+=d/1e6; s[2]+=int(r['sol_delta'])/1e9
        for x in r['other_token_deltas'].split(';'):
            if x.startswith(USDC): s[3]+=float(x.rsplit(':',1)[1])
        s[4]=s[4] or r['utc']; s[5]=r['utc']
    for c,s in sorted(st.items()):
        w.writerow([pref,c,s[0],round(s[1]/1e6,4),round(s[2],4),round(s[3],3),s[4],s[5]]); print(pref,c,s[0],round(s[1]/1e6,4),'M sol',round(s[2],4),'usdc',round(s[3],2),s[4],s[5])
