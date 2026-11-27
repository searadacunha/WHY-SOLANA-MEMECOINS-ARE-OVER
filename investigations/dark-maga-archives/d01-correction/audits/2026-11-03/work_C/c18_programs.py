#!/usr/bin/env python3
"""Programmes dans les tx >=1M sans AMM connu, avec exemples, depuis cand_edges."""
import csv, collections
rows=[r for r in csv.DictReader(open('REDACTED_HOME/Projects/Dark-MAGA-Investigation/audits/2026-11-03/work_C/cand_edges_1M.csv')) if r['has_amm']=='False']
BASE={'ComputeBudget111111111111111111111111111111','TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA','ATokenGPvbdGVxr1b2hvZbsiqW5xWH25efTNsLJA8knL','11111111111111111111111111111111','MemoSq4gqABAXKb96qnH8TysNcWxMyWCqXgDLGmfcHr','Memo1UhkJRfHyvLMcVucJwxXeuD728EqVDDwQDxFMNo','TokenzQdBNbLqP5VEhdkAS6EPFLC1PHnBqCXEpPxuEb','DeJBGdMFa1uynnnKiwrVioatTuHmNLpyFKnmB5kaFdzQ'}
c=collections.Counter();ex={}
clean=0
for r in rows:
    ps=set(r['programs'].split('|'))-BASE
    if not ps: clean+=1
    for p in ps:
        c[p]+=1; ex.setdefault(p,(r['sig'],r['src'],r['dst'],int(r['amount'])/1e6,r['authority'],r['outer_prog'],r['utc']))
print('propres',clean,'sur',len(rows))
for p,v in c.most_common(30): print(v,p,ex[p])
