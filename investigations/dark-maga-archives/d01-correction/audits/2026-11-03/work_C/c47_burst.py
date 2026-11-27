#!/usr/bin/env python3
"""Salves vers 9W9b : pour chaque versement, solde avant et apres de l'expediteur, residu, nombre de tx avant, role DMAGA. Ecrit bursts_9W9b.csv.
Puis: liens de H3QsBr, GXZvX, 9PrmF8 avec le perimetre (SOL et DMAGA, toutes tailles)."""
import csv, gzip, json, os, time
ROOT='REDACTED_HOME/Projects/Dark-MAGA-Investigation/audits/2026-11-03/work_C/'
REPO='REDACTED_HOME/Projects/Dark-MAGA-Investigation/'
NET='/Volumes/VERBATIM HD/Dark-MAGA-Investigation/audits_work/C/net/'
W9="9W9b3zgHH9mCEHDhsdbnbEPHStm9vvXS4aia4DWHBxpL"
M=set(json.load(open(REPO+'data/prevent_groups.json'))[0]['members'])
dm={r['sender']:(r['n_tx_dmaga'] or '0') for r in csv.DictReader(open(ROOT+'senders_dmaga.csv'))}
w=csv.writer(open(ROOT+'bursts_9W9b.csv','w',newline=''))
w.writerow('utc sender sol pre_sol post_sol residual_pct groupe n_tx_dmaga sig'.split())
rows=[]
for s in dm:
    p=NET+s+'.jsonl.gz'
    if not os.path.exists(p): continue
    for l in gzip.open(p,'rt'):
        t=json.loads(l); keys=[k['pubkey'] for k in t['transaction']['message']['accountKeys']]
        if W9 not in keys or s not in keys: continue
        i=keys.index(s); seq=t['transaction']['message']['instructions']
        amt=sum(int(x['parsed']['info']['lamports']) for x in seq if x.get('program')=='system' and isinstance(x.get('parsed'),dict) and x['parsed'].get('type')=='transfer' and x['parsed']['info'].get('destination')==W9 and x['parsed']['info'].get('source')==s)
        if amt<1e6: continue
        pre,post=t['meta']['preBalances'][i],t['meta']['postBalances'][i]
        rows.append((t['blockTime'],s,amt/1e9,pre/1e9,post/1e9,100*post/pre,s in M,dm[s],t['transaction']['signatures'][0]))
rows.sort()
for r in rows:
    w.writerow([time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime(r[0]))]+list(r[1:]))
import collections
by=collections.defaultdict(list)
for r in rows: by[time.strftime('%Y-%m-%d',time.gmtime(r[0]))].append(r)
for d,L in by.items():
    if len(L)>=4:
        print(d,len(L),'residu median %',sorted(x[5] for x in L)[len(L)//2],'post SOL median',round(sorted(x[4] for x in L)[len(L)//2],5),'DMAGA',sum(1 for x in L if x[7]!='0'),'montant ronds 3 dec',sum(1 for x in L if abs(x[2]*1000-round(x[2]*1000))<1e-6))
print('ensemble: post<0.01 SOL',sum(1 for r in rows if r[4]<0.01),'de',len(rows),'n',len(rows),'exp',len({r[1] for r in rows}))
print('2025-01-26',[(time.strftime('%H:%M:%S',time.gmtime(r[0])),r[1][:6],r[2],round(r[3],4),round(r[4],5)) for r in by.get('2025-01-26',[])])
print('2024-09-29',[(time.strftime('%H:%M:%S',time.gmtime(r[0])),r[1][:6],r[2],round(r[3],4),round(r[4],5)) for r in by.get('2024-09-29',[])])
sol=list(csv.DictReader(open(ROOT+'sol_edges.csv')))
tok=list(csv.DictReader(open(ROOT+'token_moves.csv')))
for a in ('H3QsBrrivimFJmSpTXuvig2n1Bh7JuYxrriRSEszT6cc','GXZvXsD6hxaLeFvQisWpdAwsayJxga7w9EeafhFZG2Ra','9PrmF8sfoD2YShtWUghrGEYgxwabpnzog8gT1V6LEtdq'):
    print(a[:8])
    print(' SOL',[(x['utc'],x['src'][:8],x['dst'][:8],int(x['lamports'])/1e9) for x in sol if a in (x['src'],x['dst'])][:15])
    print(' DMAGA',[(x['utc'],x['member'][:8],x['dir'],x['counterparty'][:8],round(float(x['tokens']),2),(x['nonbase_programs'] or '')[:6]) for x in tok if x['counterparty']==a or x['member']==a if not x['nonbase_programs']][:15])
