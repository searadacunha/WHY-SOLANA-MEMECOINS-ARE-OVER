#!/usr/bin/env python3
"""Mesure sur le temoin d'adresses qui balaient vers Coinbase : expediteurs, delais, frais, rythme, comparee a 9W9b.
Sortie: ctrl_stats.csv + impression."""
import gzip, json, csv, statistics as st, collections, time
NET="/Volumes/VERBATIM HD/Dark-MAGA-Investigation/audits_work/C/net"
HOT={"H8sMJSCQxfKiFTCfDR3DUMLPwcRbM61LGFJ8N4dK3WjS","2AQdpHJ2JpcEgPiATUXjQxA8QmafFegfQwSLWSprPicm","GJRs4FwHtemZ5ZE9x3FNvJ8TMwitKTh21yxdRPqn7npE"}
SEED="9W9b3zgHH9mCEHDhsdbnbEPHStm9vvXS4aia4DWHBxpL"
def analyze(x,txs):
    txs.sort(key=lambda t:(t['slot'],t.get('transactionIndex') or 0))
    ins=[];outs=[];fees=[];signed=0;other=0
    for tx in txs:
        msg=tx['transaction']['message']
        keys=[k for k in msg['accountKeys']]
        sg=[k['pubkey'] for k in keys if k['signer']]
        is_s = x in sg
        signed+=is_s
        progs={i['programId'] for i in msg['instructions']}
        for g in tx['meta'].get('innerInstructions') or []:
            for i in g['instructions']: progs.add(i['programId'])
        if progs-{"11111111111111111111111111111111","ComputeBudget111111111111111111111111111111"}: other+=1
        seq=list(msg['instructions'])
        for g in tx['meta'].get('innerInstructions') or []: seq+=g['instructions']
        for i in seq:
            p=i.get('parsed')
            if i.get('program')=='system' and isinstance(p,dict) and p.get('type')=='transfer':
                a=p['info']
                if a.get('destination')==x: ins.append((tx['blockTime'],a['source'],int(a['lamports'])))
                if a.get('source')==x: outs.append((tx['blockTime'],a['destination'],int(a['lamports']),tx['meta']['fee'],tx['blockTime']))
    real=[i for i in ins if i[2]>=1_000_000]
    senders={i[1] for i in real}
    tot_out=sum(o[2] for o in outs) or 1
    tocb=sum(o[2] for o in outs if o[1] in HOT)
    delays=[]
    for o in outs:
        prev=[i[0] for i in real if i[0]<=o[0]]
        if prev: delays.append(o[0]-max(prev))
    # rafales: >=3 expediteurs distincts en moins de 10 min
    bursts=0
    real_s=sorted(real)
    for k in range(len(real_s)):
        w=[r for r in real_s if real_s[k][0]<=r[0]<real_s[k][0]+600]
        if len({r[1] for r in w})>=3: bursts=max(bursts,len({r[1] for r in w}))
    secs=collections.Counter(o[0]%60 for o in outs)
    return dict(x=x,n_tx=len(txs),n_in=len(real),n_senders=len(senders),n_out=len(outs),share_cb=round(tocb/tot_out,4),med_delay=(st.median(delays) if delays else None),other_prog=other,signed=signed,fees=collections.Counter(o[3] for o in outs).most_common(3),burst=bursts,sum_in=round(sum(i[2] for i in real)/1e9,3))
by=collections.defaultdict(list)
for line in gzip.open(f"{NET}/ctrl_deposits.jsonl.gz","rt"):
    j=json.loads(line); by[j['x']].append(j['tx'])
comp={r['x']:r['complete'] for r in csv.DictReader(open('ctrl_sampled.csv'))}
res=[analyze(x,t) for x,t in by.items()]
w=csv.DictWriter(open('ctrl_stats.csv','w',newline=''),fieldnames=list(res[0].keys())+['complete'])
w.writeheader()
for r in res:
    r['complete']=comp[r['x']]; w.writerow(r)
pure=[r for r in res if r['other_prog']==0 and r['share_cb']>=0.8 and r['n_in']>0]
print('echantillon',len(res),'purs relais (aucun autre programme, >=80% vers hot wallets, au moins une entree)',len(pure))
print('n_senders purs: quantiles',[sorted(r['n_senders'] for r in pure)[int(q*(len(pure)-1))] for q in (0,.25,.5,.75,.9,.95,1)])
print('dist n_senders purs',sorted(collections.Counter(r['n_senders'] for r in pure).items()))
print('delai median purs: med',st.median([r['med_delay'] for r in pure if r['med_delay'] is not None]))
print('frais (top):',collections.Counter(f[0] for r in pure for f in r['fees']).most_common(8))
print('rafale max (distincts en 10 min), dist',sorted(collections.Counter(r['burst'] for r in pure).items()))
print('incomplets (plus de 3 pages)',sum(1 for r in pure if r['complete']=='False'))
for r in sorted(res,key=lambda r:-r['n_senders'])[:12]: print({k:r[k] for k in ('x','n_tx','n_senders','n_in','n_out','share_cb','med_delay','other_prog','signed','burst','complete','sum_in')})
seed=[json.loads(l) for l in gzip.open(f"{NET}/{SEED}.jsonl.gz","rt")]
s=analyze(SEED,seed); print('9W9b',s)
