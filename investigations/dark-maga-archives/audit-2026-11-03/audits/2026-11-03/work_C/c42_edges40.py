#!/usr/bin/env python3
"""Rejoue les 40 transferts du groupe sur le brut et teste les explications alternatives :
 relecture (signataire, programmes, niveau, soldes), retour de SOL ou de valeur (gre a gre), gaz du donneur, age du destinataire, ce que devient le jeton.
 Sorties : edges40_replay.csv, member_evidence.csv"""
import csv, json, gzip, time, collections
ROOT='REDACTED_HOME/Projects/Dark-MAGA-Investigation/audits/2026-11-03/work_C/'
REPO='REDACTED_HOME/Projects/Dark-MAGA-Investigation/'
g=json.load(open(REPO+'data/prevent_groups.json'))[0]; M=set(g['members']); E=g['edges_top']; assert len(E)==40
raw={r['sig']:r for r in csv.DictReader(open(ROOT+'direct_edges_all.csv'))}
sol=list(csv.DictReader(open(ROOT+'sol_edges.csv')))
tab={r['wallet']:r for r in csv.DictReader(open(ROOT+'members_table.csv'))}
price={}
for r in csv.DictReader(open(REPO+'data/price_hourly.csv')):
    pass
hdr=list(r.keys()); print('price cols',hdr)
rows=[]
W=csv.writer(open(ROOT+'edges40_replay.csv','w',newline=''))
W.writerow('utc sig src dst tokens_M in_raw_or_absent clean_direct origin authority_is_src payer_is_src sol_back_7d_SOL sol_back_first_delay_s sol_fwd_gas_1h_SOL dst_first_tx_before_edge dst_first_tx_utc'.split())
nok=0
for e in sorted(E,key=lambda e:e['t']):
    r=raw.get(e['sig'])
    t=e['t']
    back=[x for x in sol if x['src']==e['dst'] and x['dst']==e['src'] and abs(int(x['bt'])-t)<=7*86400]
    fwd=[x for x in sol if x['src']==e['src'] and x['dst']==e['dst'] and abs(int(x['bt'])-t)<=3600]
    sb=sum(int(x['lamports']) for x in back)/1e9
    delay=min((int(x['bt'])-t for x in back),key=abs) if back else ''
    sf=sum(int(x['lamports']) for x in fwd)/1e9
    ft=tab[e['dst']]['first_tx']
    W.writerow([time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime(t)),e['sig'],e['src'],e['dst'],e['M'],bool(r),r and r['clean'],r and r['origin'],r and r['authority']==e['src'],r and r['payer']==e['src'],round(sb,4),delay,round(sf,4),ft<time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime(t)),ft])
    assert r and abs(int(r['amount'])/1e12-e['M'])<0.001 and r['src']==e['src'] and r['dst']==e['dst'], e['sig']
    nok+=1
    print(time.strftime('%m-%d %H:%M:%S',time.gmtime(t)),e['src'][:7],'>',e['dst'][:7],round(e['M'],2),'back',round(sb,3),delay,'gaz',round(sf,4),'dst1er',ft[:16])
print('rejoues ok',nok)
