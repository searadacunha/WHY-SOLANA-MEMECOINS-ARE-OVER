#!/usr/bin/env python3
"""Lit l'historique complet d'un wallet telecharge et imprime SOL et jetons. usage: c22_hub.py <wallet> [minsol]"""
import gzip,json,sys,time,collections
w=sys.argv[1]; ms=float(sys.argv[2]) if len(sys.argv)>2 else 0.05
MINT="7D7BRcBYepfi77vxySapmeqRNN1wsBBxnFPJGbH5pump"
rows=[json.loads(l) for l in gzip.open(f"/Volumes/VERBATIM HD/Dark-MAGA-Investigation/audits_work/C/net/{w}.jsonl.gz","rt")]
rows.sort(key=lambda t:(t['slot'],t.get('transactionIndex') or 0))
for t in rows:
    m=t['transaction']['message'];me=t['meta']
    keys=[k['pubkey'] for k in m['accountKeys']]
    i=keys.index(w) if w in keys else None
    sol=(me['postBalances'][i]-me['preBalances'][i])/1e9 if i is not None else 0
    tok=collections.Counter()
    own={}
    for s,sign in (('preTokenBalances',-1),('postTokenBalances',1)):
        for b in me.get(s) or []:
            own[keys[b['accountIndex']]]=b.get('owner')
            if b.get('owner')==w: tok[b['mint'][:6]]+=sign*float(b['uiTokenAmount']['uiAmountString'] or 0)
    tok={k:round(v,3) for k,v in tok.items() if abs(v)>1e-6}
    moves=[]
    seq=list(m['instructions'])
    for g in me.get('innerInstructions') or []: seq+=g['instructions']
    prog=set()
    for x in seq:
        prog.add(x['programId'][:6])
        p=x.get('parsed')
        if x.get('program')=='system' and isinstance(p,dict) and p.get('type')=='transfer':
            a=p['info']
            if a['source']==w or a['destination']==w:
                if int(a['lamports'])>=ms*1e9: moves.append(f"{a['source'][:6]}>{a['destination'][:6]}:{int(a['lamports'])/1e9:.3f}")
    if tok or moves or abs(sol)>=ms:
        print(time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime(t['blockTime'])),t['transaction']['signatures'][0][:10],'P' if keys[0]==w else 'p:'+keys[0][:6],f'sol={sol:+.3f}',tok,moves[:3],sorted(prog-{'Comput','111111','Tokenk','AToken'})[:4])
print(len(rows))
