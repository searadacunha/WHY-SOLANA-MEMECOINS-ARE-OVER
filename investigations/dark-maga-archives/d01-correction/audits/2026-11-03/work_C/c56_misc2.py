#!/usr/bin/env python3
"""Programmes et frais des achats de la 1re heure (bots vendus en service ?), destinations de 9W9b dans le temoin, ensembles elargis, DCA du createur. Sortie c56.out"""
import csv, gzip, json, os, time, collections
from pathlib import Path
from dmaga.labels import label
ROOT=Path(__file__).resolve().parent; REPO=ROOT.parents[2]
NET="/Volumes/VERBATIM HD/Dark-MAGA-Investigation/audits_work/C/net/"
MINT="7D7BRcBYepfi77vxySapmeqRNN1wsBBxnFPJGbH5pump"; T0=1720922725; TL=1721588607; TH=1721590213
M=set(json.load(open(REPO/'data/prevent_groups.json'))[0]['members'])
SER=[r['wallet'] for r in csv.DictReader(open(ROOT/'cb_series.csv'))]
tab={r['wallet']:r for r in csv.DictReader(open(ROOT/'members_table.csv'))}
print('tab miss',[a[:8] for a in SER if a not in tab])
BASEP={'ComputeBudget111111111111111111111111111111','TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA','ATokenGPvbdGVxr1b2hvZbsiqW5xWH25efTNsLJA8knL','11111111111111111111111111111111'}
prog=collections.Counter(); dest=collections.Counter(); destw=collections.defaultdict(set); fees=collections.Counter(); perw={}
for a in sorted(M|set(SER)):
    p=NET+a+'.jsonl.gz'
    if not os.path.exists(p): continue
    for l in gzip.open(p,'rt'):
        t=json.loads(l)
        if t['blockTime']>=T0+3600: continue
        me=t['meta']; m=t['transaction']['message']; keys=[k['pubkey'] for k in m['accountKeys']]
        if keys[0]!=a: continue
        d=0
        for s,n in ((-1,'preTokenBalances'),(1,'postTokenBalances')):
            for b in me.get(n) or []:
                if b.get('owner')==a and b['mint']==MINT: d+=s*int(b['uiTokenAmount']['amount'])
        if d<=0: continue
        seq=list(m['instructions'])
        for g in me.get('innerInstructions') or []: seq+=g['instructions']
        ps={i['programId'] for i in seq}-BASEP
        for x in ps: prog[x]+=1
        fees[me['fee']]+=1
        for i in seq:
            q=i.get('parsed')
            if i.get('program')=='system' and isinstance(q,dict) and q.get('type')=='transfer' and q['info'].get('source')==a:
                dest[q['info']['destination']]+=1; destw[q['info']['destination']].add(a)
print('programmes',prog.most_common(14))
print('frais de tx',fees.most_common(10))
print('destinations SOL',[(k,v,len(destw[k]),label(k)) for k,v in dest.most_common(14)])
# Destinations non Coinbase de 9W9b dans le temoin
D={'FpwQQhQQoEaVu3WU2qZMfF1hx48YyfwsLoRgXG83E99Q','D89hHJT5Aqyx1trP6EnGY9jJUB3whgnq3aUvvCqedvzf','9obNtb5GyUegcs3a1CbBkLuc5hEWynWfJC6gjz5uWQkE','DPqsobysNf5iA9w7zrQM8HLzCKZEDMkZsWbiidsAt1xo','4NyK1AdJBNbgaJ9EsKz3J4rfeHsuYdjkTPg3JaNdLeFw','8JUEoHNMbWM4eegcMvx6ZQJt3V3fbo8JNjpWiCtJgxfF'}
HOT={"H8sMJSCQxfKiFTCfDR3DUMLPwcRbM61LGFJ8N4dK3WjS","2AQdpHJ2JpcEgPiATUXjQxA8QmafFegfQwSLWSprPicm","GJRs4FwHtemZ5ZE9x3FNvJ8TMwitKTh21yxdRPqn7npE"}
oth=collections.Counter(); xs=collections.defaultdict(set); cbt=collections.Counter(); vol=collections.Counter()
for l in gzip.open(NET+'ctrl_deposits.jsonl.gz','rt'):
    j=json.loads(l); x=j['x']; tx=j['tx']
    for i in tx['transaction']['message']['instructions']:
        q=i.get('parsed')
        if i.get('program')=='system' and isinstance(q,dict) and q.get('type')=='transfer' and q['info'].get('source')==x:
            de=q['info']['destination']; am=int(q['info']['lamports'])
            if de in D: xs[de].add(x); oth[de]+=1
            if de not in HOT: vol['autres']+=am
            else: vol['hot']+=am
print('dans le temoin, depots qui balaient aussi vers les 6 destinations',{k[:8]:(oth[k],len(xs[k])) for k in D},'depots touches',len(set().union(*xs.values())) if xs else 0)
# echantillon probe : autre chose ? lien entre 6 destinations et hot wallets
for l in gzip.open(NET+'probe_dest9w.jsonl.gz','rt'):
    pass
# ensembles elargis
send={r['sender'] for r in csv.DictReader(open(ROOT/'9W9b3z_senders.csv'))}
def s(ws,k): return sum(float(tab[a][k] or 0) for a in ws if a in tab)
A=set(SER)
print('serie: n',len(A),'dans 33',len(A&M),'held Tlow',round(s(A,'held_Tlow'),2),'hors 33',round(s(A-M,'held_Tlow'),2),'buy1h M',round(s(A,'buy1h_tokens')/1e6,2),'buy1h SOL',round(s(A,'buy1h_sol'),2),'sell24 SOL',round(s(A,'sell24_sol'),1),'hors33',round(s(A-M,'sell24_sol'),1))
print('expediteurs 9W9b: n',len(send),'dans 33',len(send&M),'held Tlow',round(s(send,'held_Tlow'),2),'hors33',round(s(send-M,'held_Tlow'),2),'sell24 SOL',round(s(send,'sell24_sol'),1),'hors33',round(s(send-M,'sell24_sol'),1))
U=M|A|send
print('union',len(U),'held Tlow',round(s(U,'held_Tlow'),2),'part de 938',round(100*s(U,'held_Tlow')/938.0,1),'sell24 SOL',round(s(U,'sell24_sol'),1),'usdc',round(s(U,'sell24_usdc')))
print('premier achat/series',[(a[:6],(tab[a]['first_funder'] or '')[:6]) for a in send-M-A][:30])
print('Expediteurs series dans 9W9b',len(A&send),[a[:6] for a in A-send])
print('Habp5bnc held Tlow',tab.get('Habp5bncMSsBC3vkChyebepym5dcTNRYeg2LVG464E96',{}).get('held_Tlow'))
