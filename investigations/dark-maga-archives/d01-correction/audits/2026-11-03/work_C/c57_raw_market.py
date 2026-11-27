#!/usr/bin/env python3
"""Ventes de marche depuis le brut sur [T_HIGH, T_HIGH+24 h) : sortie SOL du vault Raydium v4 dans le sens vente, par transaction, dedoublonnee. Sortie c57.out."""
import gzip, json, hashlib
from pathlib import Path
RAW=Path("/Volumes/VERBATIM HD/Dark-MAGA-Investigation/raw/full_pool")
TH=1721590213; END=TH+86400
VS="3p7DbnWekWjtMQkey6fp1emdwXbAAxecnYuD5eU9ZZPH"; VT="5HuEsLbebeuottMsFW3hHcXTrKVsu3WUNSQnSr6aX4eL"
dirs=sorted((p for p in RAW.iterdir() if p.is_dir() and not p.name.startswith('._')),key=lambda p:int(p.name[1:]))
use=[]
for i,d in enumerate(dirs):
    a=int(d.name[1:]); b=int(dirs[i+1].name[1:]) if i+1<len(dirs) else 1<<40
    if b>TH and a<END: use.append(d)
seen=set(); sell=buy=0; ns=nb=n=0
for d in use:
    for p in sorted(d.glob('p*.jsonl.gz')):
        if p.name.startswith('._'): continue
        with gzip.open(p,'rt') as f:
            for line in f:
                t=json.loads(line)
                if not TH<=t['blockTime']<END: continue
                s=t['transaction']['signatures'][0]
                if s in seen: continue
                seen.add(s); n+=1
                keys=[k['pubkey'] for k in t['transaction']['message']['accountKeys']]
                pre={keys[b['accountIndex']]:int(b['uiTokenAmount']['amount']) for b in t['meta'].get('preTokenBalances') or []}
                post={keys[b['accountIndex']]:int(b['uiTokenAmount']['amount']) for b in t['meta'].get('postTokenBalances') or []}
                if VS in post and VT in post:
                    ds=post[VS]-pre.get(VS,0); dt=post[VT]-pre.get(VT,0)
                    if ds<0 and dt>0: sell+=-ds; ns+=1
                    elif ds>0 and dt<0: buy+=ds; nb+=1
print('tx pool fenetre',n,'ventes',ns,round(sell/1e9,1),'SOL','achats',nb,round(buy/1e9,1),'SOL')
