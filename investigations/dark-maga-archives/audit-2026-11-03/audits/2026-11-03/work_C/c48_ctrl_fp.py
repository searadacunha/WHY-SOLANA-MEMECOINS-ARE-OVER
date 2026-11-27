#!/usr/bin/env python3
"""Empreinte des versements vers un depot : montant a 3 decimales, residu de l'expediteur, sur le temoin et sur 9W9b. Ecrit ctrl_fingerprint.csv."""
import gzip, json, csv, collections
NET="/Volumes/VERBATIM HD/Dark-MAGA-Investigation/audits_work/C/net/"
ROOT='REDACTED_HOME/Projects/Dark-MAGA-Investigation/audits/2026-11-03/work_C/'
def ins(x,tx):
    seq=list(tx['transaction']['message']['instructions'])
    keys=[k['pubkey'] for k in tx['transaction']['message']['accountKeys']]
    for i in seq:
        p=i.get('parsed')
        if i.get('program')=='system' and isinstance(p,dict) and p.get('type')=='transfer' and p['info'].get('destination')==x and int(p['info']['lamports'])>=1_000_000:
            s=p['info']['source']
            if s in keys:
                k=keys.index(s); yield (tx['blockTime'],s,int(p['info']['lamports']),tx['meta']['preBalances'][k],tx['meta']['postBalances'][k])
by=collections.defaultdict(list)
for l in gzip.open(NET+'ctrl_deposits.jsonl.gz','rt'):
    j=json.loads(l)
    by[j['x']].extend(ins(j['x'],j['tx']))
W9="9W9b3zgHH9mCEHDhsdbnbEPHStm9vvXS4aia4DWHBxpL"
by[W9]=[]
for l in gzip.open(NET+W9+'.jsonl.gz','rt'):
    by[W9].extend(ins(W9,json.loads(l)))
w=csv.writer(open(ROOT+'ctrl_fingerprint.csv','w',newline='')); w.writerow('x n_in n_senders pct_round3 pct_empty_lt_002 max_burst_round_empty_10min'.split())
res={}
for x,L in by.items():
    if not L: continue
    L.sort()
    rnd=[r for r in L if r[2]%1_000_000==0]
    emp=[r for r in L if r[4]<0.02e9]
    fp=[r for r in L if r[2]%1_000_000==0 and r[4]<0.02e9]
    b=0
    for i in range(len(fp)):
        b=max(b,len({r[1] for r in fp if fp[i][0]<=r[0]<fp[i][0]+600}))
    res[x]=(len(L),len({r[1] for r in L}),100*len(rnd)/len(L),100*len(emp)/len(L),b)
    w.writerow([x,len(L),len({r[1] for r in L}),round(100*len(rnd)/len(L),1),round(100*len(emp)/len(L),1),b])
print('9W9b',res[W9])
o=[v for k,v in res.items() if k!=W9]
print('temoins',len(o),'max rafale ronde+videe: distribution',sorted(collections.Counter(v[4] for v in o).items()))
print('part ronde mediane temoins',sorted(v[2] for v in o)[len(o)//2],'part videe mediane',sorted(v[3] for v in o)[len(o)//2])
print('temoins rafale>=5',[(k[:8],v) for k,v in res.items() if k!=W9 and v[4]>=5])
print('temoins >=20 expediteurs : part ronde et videe',[(k[:6],v[1],round(v[2]),round(v[3]),v[4]) for k,v in res.items() if k!=W9 and v[1]>=20])
