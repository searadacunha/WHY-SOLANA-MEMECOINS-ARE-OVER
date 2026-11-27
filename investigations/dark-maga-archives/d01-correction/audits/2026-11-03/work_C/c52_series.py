#!/usr/bin/env python3
"""Serie de retraits Coinbase du 14/07/2024 01:32:23 a 01:40:50 : qui, combien, premiere tx, 9W9b, groupe, jetons a T_LOW. Temoins sur d'autres fenetres. Ecrit cb_series.csv, cb_series_ctrl.csv"""
import csv, gzip, json, os, time, collections, sys
from pathlib import Path
from dmaga.helius import Helius
ROOT=Path(__file__).resolve().parent; REPO=ROOT.parents[2]
NET=Path("/Volumes/VERBATIM HD/Dark-MAGA-Investigation/audits_work/C/net")
M=set(json.load(open(REPO/'data/prevent_groups.json'))[0]['members'])
send={r['sender'] for r in csv.DictReader(open(ROOT/'9W9b3z_senders.csv'))}
rows=list(csv.DictReader(open(ROOT/'cb_window.csv')))
S=[r for r in rows if '2024-07-14T01:32:20Z'<=r['utc']<='2024-07-14T01:40:51Z']
SER=[r for r in S if float(r['sol']) in (0.5,1.0,1.05)]
print('retraits dans la fenetre',len(S),'montants ronds serie',len(SER),'avec DMAGA',sum(1 for r in SER if r['dmaga_tx']!='0'))
print('intervalles s',[int(time.mktime(time.strptime(b['utc'],'%Y-%m-%dT%H:%M:%SZ'))-time.mktime(time.strptime(a['utc'],'%Y-%m-%dT%H:%M:%SZ'))) for a,b in zip(SER,SER[1:])])
print('autres retraits meme fenetre (non ronds)',[(r['sol'],r['dmaga_tx']) for r in S if r not in SER])
tab={r['wallet']:r for r in csv.DictReader(open(ROOT/'members_table.csv'))}
missing=[r['dest'] for r in SER if r['dest'] not in tab]
print('sans historique local',missing)
h=None
if missing:
    h=Helius()
    spec=__import__('importlib.util').util.spec_from_file_location('c03',ROOT/'c03_net.py'); c03=__import__('importlib.util').util.module_from_spec(spec); spec.loader.exec_module(c03)
    for a in missing: c03.full(h,a,12)
w=csv.writer(open(ROOT/'cb_series.csv','w',newline='')); w.writerow('utc hot wallet sol sig first_tx_is_this in33 sends_9W9b_sol held_Tlow'.split())
sol=list(csv.DictReader(open(ROOT/'sol_edges.csv')))
W9="9W9b3zgHH9mCEHDhsdbnbEPHStm9vvXS4aia4DWHBxpL"
for r in SER:
    a=r['dest']; t=tab.get(a,{})
    s9=sum(int(x['lamports']) for x in sol if x['src']==a and x['dst']==W9)/1e9
    w.writerow([r['utc'],r['hot'],a,r['sol'],r['sig'],(t.get('first_tx') or '')==r['utc'],a in M,s9,t.get('held_Tlow','')])
    print(r['utc'][11:19],r['hot'],a[:10],r['sol'],'1re tx',t.get('first_tx','?')[:19],'33' if a in M else '','9W',s9,'Tlow',t.get('held_Tlow','?')[:7],'buy1h',(t.get('buy1h_tokens') or '')[:10],'sell24',(t.get('sell24_sol') or '')[:7])
