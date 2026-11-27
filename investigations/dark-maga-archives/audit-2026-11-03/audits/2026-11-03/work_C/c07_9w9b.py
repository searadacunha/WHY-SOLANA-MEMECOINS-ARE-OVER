#!/usr/bin/env python3
"""Analyse comportementale de 9W9b3z depuis sa chronologie brute : balayages, delais, frais, destinations, cibles, soldes."""
import csv, collections, statistics as st, re, sys, time
rows=list(csv.DictReader(open('chrono_9W9b3z.csv')))
LAB={'H8sMJSCQxfKiFTCfDR3DUMLPwcRbM61LGFJ8N4dK3WjS':'Coinbase1','2AQdpHJ2JpcEgPiATUXjQxA8QmafFegfQwSLWSprPicm':'Coinbase2','GJRs4FwHtemZ5ZE9x3FNvJ8TMwitKTh21yxdRPqn7npE':'Coinbase3'}
def ts(u): return time.mktime(time.strptime(u,'%Y-%m-%dT%H:%M:%SZ'))
ins=[];outs=[]
for r in rows:
    if r['sys_in']:
        for x in r['sys_in'].split(';'):
            a,v=x.rsplit(':',1); ins.append((r['utc'],a,int(v),r['sig'],r['payer']))
    if r['sys_out']:
        for x in r['sys_out'].split(';'):
            a,v=x.rsplit(':',1); outs.append((r['utc'],a,int(v),r['sig'],r['payer']))
print('n tx',len(rows),'n in',len(ins),'n out',len(outs))
print('entrants > poussiere (>=0.001 SOL)',sum(1 for i in ins if i[2]>=1e6),'distincts',len({i[1] for i in ins if i[2]>=1e6}),'poussiere n',sum(1 for i in ins if i[2]<1e6),'distincts',len({i[1] for i in ins if i[2]<1e6}))
tot=sum(o[2] for o in outs)
c=collections.Counter()
for o in outs: c[LAB.get(o[1],o[1])]+=o[2]
print('sorties',{k:round(v/1e9,4) for k,v in c.items()},'total',tot/1e9)
cb=sum(v for k,v in c.items() if k.startswith('Coinbase'))
print('part Coinbase sorties',cb/tot)
# appariement chronologique: chaque sortie avec les entrees depuis la derniere sortie
bal=0;last=[];res=[]
evs=sorted([(i[0],'in',i) for i in ins]+[(o[0],'out',o) for o in outs],key=lambda e:(e[0],e[1]=='out'))
runbal=0;pend=[]
gaps=[];fees=collections.Counter()
lines=[]
for u,k,e in evs:
    if k=='in':
        if e[2]>=1e6: pend.append(e)
        runbal+=e[2]
    else:
        s=sum(p[2] for p in pend)
        fee=s-e[2]
        if pend:
            gap=ts(u)-ts(pend[-1][0]); gaps.append(gap)
            fees[fee]+=1
        lines.append((u,LAB.get(e[1],e[1]),e[2]/1e9,len(pend),[p[1][:6] for p in pend],fee,(ts(u)-ts(pend[-1][0])) if pend else None,e[3]))
        pend=[]
print('nb sorties',len(lines),'delai depuis derniere entree (s): med',st.median(gaps),'min',min(gaps),'max',max(gaps),'p90',sorted(gaps)[int(.9*len(gaps))])
print('frais implicites (entrees depuis la derniere sortie - sortie):',fees.most_common(12))
for l in lines:
    if not l[1].startswith('Coinbase'): print('NONCB',l)
print('sorties par an/mois',collections.Counter(l[0][:7] for l in lines))
print('multi-entrees',sum(1 for l in lines if l[3]>1), 'une entree',sum(1 for l in lines if l[3]==1))
# signataires des sorties
print('payeurs sorties',collections.Counter(o[4][:6] for o in outs))
print('payeurs entrees top',collections.Counter(i[4][:6] for i in ins if i[2]>=1e6).most_common(10))
# montants entrants
am=[i[2]/1e9 for i in ins if i[2]>=1e6]
print('montants entrants med',st.median(am),'min',min(am),'max',max(am),'ronds <3 dec',sum(1 for a in am if abs(a*1000-round(a*1000))<1e-6))
wr=csv.writer(open('9W9b3z_senders.csv','w',newline=''))
wr.writerow('sender n sol first last'.split())
agg=collections.defaultdict(list)
for i in ins:
    if i[2]>=1e6: agg[i[1]].append(i)
for a,v in sorted(agg.items(),key=lambda kv:-sum(x[2] for x in kv[1])):
    wr.writerow([a,len(v),sum(x[2] for x in v)/1e9,v[0][0],v[-1][0]])
print('expediteurs >=0.001 SOL',len(agg))
agg01={a for a,v in agg.items() if sum(x[2] for x in v)>=1e8}
print('expediteurs cumul >=0.1 SOL',len(agg01))
dust=collections.Counter(i[1] for i in ins if i[2]<1e6)
print('poussiere top',dust.most_common(8))
