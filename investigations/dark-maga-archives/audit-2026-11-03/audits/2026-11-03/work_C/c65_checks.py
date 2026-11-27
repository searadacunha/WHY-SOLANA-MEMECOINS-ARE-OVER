#!/usr/bin/env python3
"""Verifie des chiffres cites : ecarts rafale 26/01, residus, 14 ou 15 versements a C7qEaB, 6 SOL NxtXcm-GFpqfj avant 14/07, delai USDC 71 s, 13/15 G41, age des wallets neufs, part 5QhJJc, prix du gre a gre."""
import csv,json,time,calendar,gzip
R='REDACTED_HOME/Projects/Dark-MAGA-Investigation/audits/2026-11-03/work_C/'
ts=lambda u:calendar.timegm(time.strptime(u,'%Y-%m-%dT%H:%M:%SZ'))
B=[r for r in csv.DictReader(open(R+'bursts_9W9b.csv')) if r['utc'].startswith('2025-01-26')]
print('n',len(B),'ecarts',[ts(b['utc'])-ts(a['utc']) for a,b in zip(B,B[1:])],'post',[round(float(r['post_sol']),5) for r in B])
E=[r for r in csv.DictReader(open(R+'direct_edges_all.csv')) if r['dst'].startswith('C7qEaB6a')]
print('C7q aretes>=1M',len(E),'exp',len({r['src'] for r in E}),[round(int(r['amount'])/1e12,3) for r in E])
S=list(csv.DictReader(open(R+'sol_edges.csv')))
x=[(r['utc'],r['src'][:6],r['dst'][:6],int(r['lamports'])/1e9) for r in S if {r['src'][:8],r['dst'][:8]}=={'NxtXcmEW','GFpqfjEQ'} and r['utc']<'2024-07-14T03']
print('Nxt-GFp',len(x),x)
t=[r for r in csv.DictReader(open(R+'edges40_replay.csv'))]
print('dst neuf delta s',[(r['dst'][:8],ts(r['utc'])-ts(r['dst_first_tx_utc'])) for r in t if ts(r['utc'])-ts(r['dst_first_tx_utc'])<400])
print('prix otc SOL/jeton',23/18e6)
import duckdb
c=duckdb.connect();c.execute("SET memory_limit='200MB';SET threads=1;")
p=list(csv.DictReader(open('REDACTED_HOME/Projects/Dark-MAGA-Investigation/data/price_hourly.csv')))
print([r for r in p if r['hour_utc'].startswith('2024-07-18') and r['hour_utc'][11:13] in('20','21','22')][:3])
G=[r for r in csv.DictReader(open(R+'chrono_G41vRr.csv')) if r['utc']<'2024-07-14T02:05:25Z' and r['utc']>'2024-07-14T01:40']
print('G41 fenetre',G[0]['utc'],G[-1]['utc'],len(G))
L=[json.loads(l) for l in gzip.open('/Volumes/VERBATIM HD/Dark-MAGA-Investigation/audits_work/C/net/BuHUkjUyWGTwz1suyWpqY6ZcYLX9rbfRsT5nnHFGXykc.jsonl.gz','rt')]
L.sort(key=lambda t:(t['slot'],t.get('transactionIndex') or 0)); print([ (t['blockTime'],t['transaction']['signatures'][0][:12],t['transaction']['message']['accountKeys'][0]['pubkey'][:8]) for t in L[:2]])
print('fan-out GFpqfj',sum(1 for r in t if r['src'].startswith('GFpqfj')), {r['dst'][:6] for r in t if r['src'].startswith('GFpqfj')})
print('Transit tx',[(k[:6],v['n_tx']) for k,v in {r['wallet']:r for r in csv.DictReader(open(R+'members_table.csv'))}.items() if k[:6] in ('FjuV7m','HkrGvx','HKXb8L','8xjM4f')])
