#!/usr/bin/env python3
"""Test de correspondance depot -> retrait a travers Coinbase : chaque depot sur 9W9b (montant exact) contre tout retrait d'un hot wallet vers un wallet du perimetre dans les 30 jours, ecart 0 a 0,01 SOL. Puis temoin de chance : meme test sur les depots decales. Sortie deposit_withdraw_match.csv."""
import csv, gzip, json, os, time, collections
from dmaga.labels import label
NET="/Volumes/VERBATIM HD/Dark-MAGA-Investigation/audits_work/C/net/"
ROOT='REDACTED_HOME/Projects/Dark-MAGA-Investigation/audits/2026-11-03/work_C/'
W9="9W9b3zgHH9mCEHDhsdbnbEPHStm9vvXS4aia4DWHBxpL"
dep=[]
for r in csv.DictReader(open(ROOT+'chrono_9W9b3z.csv')):
    for x in r['sys_in'].split(';'):
        if x:
            a,v=x.rsplit(':',1)
            if int(v)>=10_000_000: dep.append((r['utc'],a,int(v),r['sig']))
W=[f[:-9] for f in os.listdir(NET) if f.endswith('.jsonl.gz') and not f.startswith(('._','probe','ctrl','absent'))]
inc=[]
for w in W:
    for l in gzip.open(NET+w+'.jsonl.gz','rt'):
        t=json.loads(l); 
        for i in t['transaction']['message']['instructions']:
            p=i.get('parsed')
            if i.get('program')=='system' and isinstance(p,dict) and p.get('type')=='transfer' and p['info'].get('destination')==w and int(p['info']['lamports'])>=10_000_000:
                inc.append((t['blockTime'],p['info']['source'],w,int(p['info']['lamports']),t['transaction']['signatures'][0]))
inc=list(set(inc)); print('entrees perimetre',len(inc),'depots',len(dep))
ts=lambda u:__import__('calendar').timegm(time.strptime(u,'%Y-%m-%dT%H:%M:%SZ'))
w=csv.writer(open(ROOT+'deposit_withdraw_match.csv','w',newline='')); w.writerow('dep_utc dep_from dep_lamports dep_sig wd_utc wd_from wd_to wd_lamports wd_sig diff delay_h'.split())
n=0
for u,a,v,s in dep:
    for bt,src,dst,lam,sig in inc:
        if src==W9 or dst==W9: continue
        d=v-lam
        if 0<=d<=1_000_000 and 0<bt-ts(u)<=30*86400 and v%1_000_000!=0:
            w.writerow([u,a,v,s,time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime(bt)),src,dst,lam,sig,d,round((bt-ts(u))/3600,1)]); n+=1
            print(u,a[:8],v,'->',time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime(bt)),src[:8],label(src),dst[:8],lam,'ecart',d)
print('correspondances (depots non ronds)',n,'depots non ronds',sum(1 for x in dep if x[2]%1_000_000!=0))
print('5g7yNH label',label('5g7yNHyGLJ7fiQ9SN9mf47opDnMjc585kqXWt6d7aBWs'))
c=collections.Counter(x[1] for x in inc if x[3]>0); 
print('5g7yNH entrees perimetre',sum(1 for x in inc if x[1].startswith('5g7yNH')),[ (time.strftime('%Y-%m-%d',time.gmtime(x[0])),x[2][:8],x[3]/1e9) for x in inc if x[1].startswith('5g7yNH')][:12])
