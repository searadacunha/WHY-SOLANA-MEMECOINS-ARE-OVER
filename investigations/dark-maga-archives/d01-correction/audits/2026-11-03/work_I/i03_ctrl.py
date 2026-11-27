"""Témoin de recouvrement refait sur le brut ctrl_deposits : tailles, plafond arithmétique, coefficient de recouvrement, part d'USDC, durée couverte, troncature.
Question : le « au plus 4 sur 7 140 » a-t-il le pouvoir de distinguer 27 sur 48 et 55 ? Sortie i03_ctrl.txt."""
import gzip, json, sys, collections, itertools, statistics as st
sys.path.insert(0,"audits/2026-11-03/work_I")
from i_lib import *
OUT="audits/2026-11-03/work_I/"
sys.stdout=open(OUT+"i03_ctrl.txt","w")
sol=collections.defaultdict(dict); usd=collections.defaultdict(dict); ntx=collections.Counter(); tmin={}; tmax={}; usdout=collections.Counter(); solin=collections.Counter()
with gzip.open(R+"/audits_work/C/net/ctrl_deposits.jsonl.gz","rt") as h:
    for l in h:
        j=json.loads(l); x=j["x"]; t=j["tx"]; ntx[x]+=1
        ts=t["blockTime"]; tmin[x]=min(tmin.get(x,ts),ts); tmax[x]=max(tmax.get(x,ts),ts)
        if t["meta"]["err"] is not None: continue
        sd=sol_delta(t); td,dec=tok_delta(t)
        if sd.get(x,0)>0:
            for k,v in sd.items():
                if v<0 and k!=x: sol[x][k]=sol[x].get(k,0)+(-v)/1e9
            solin[x]+=sd[x]/1e9
        for (o,m),v in td.items():
            if o==x and m in(USDC,USDT) and v>0:
                for (o2,m2),v2 in td.items():
                    if m2==m and v2<0 and o2!=x: usd[x][o2]=usd[x].get(o2,0)+(-v2)/10**dec[m]
xs=sorted(ntx)
print("dépôts",len(xs),"tx par dépôt : médiane",st.median(ntx.values()),"max",max(ntx.values()))
print("dépôts à 300 tx ou plus (coupés par 3 pages)",sum(1 for x in xs if ntx[x]>=295))
span=[(tmax[x]-tmin[x])/86400 for x in xs]
print("durée lue, jours : médiane",round(st.median(span),1),"p90",round(sorted(span)[int(.9*len(span))],1),"max",round(max(span),1))
sS={x:{k for k,v in sol[x].items() if v>=0.01} for x in xs}
sU={x:{k for k,v in usd[x].items() if v>=1} for x in xs}
print("expéditeurs SOL >=0,01 : médiane",st.median(len(v) for v in sS.values()),"p90",sorted(len(v) for v in sS.values())[int(.9*len(xs))],"max",max(len(v) for v in sS.values()),"; dépôts avec >=48 :",sum(1 for v in sS.values() if len(v)>=48),"; >=27 :",sum(1 for v in sS.values() if len(v)>=27))
print("expéditeurs USDC/USDT >=1 : dépôts qui en ont",sum(1 for v in sU.values() if v),"médiane parmi eux",st.median([len(v) for v in sU.values() if v] or [0]),"max",max(len(v) for v in sU.values()))
pairs=list(itertools.combinations(xs,2))
print("paires",len(pairs),"paires où le plafond min(|A|,|B|) atteint 27 :",sum(1 for a,b in pairs if min(len(sS[a]),len(sS[b]))>=27),"; atteint 5 :",sum(1 for a,b in pairs if min(len(sS[a]),len(sS[b]))>=5))
ov=sorted(((len(sS[a]&sS[b]),len(sS[a]),len(sS[b]),a,b) for a,b in pairs),reverse=True)
print("top recouvrement",[(o[0],o[1],o[2],o[3][:8],o[4][:8]) for o in ov[:8]])
print("distribution",collections.Counter(o[0] for o in ov))
big=[o for o in ov if min(o[1],o[2])>=5]
print("coefficient recouvrement/min, paires >=5 expéditeurs chacun, top :",[(round(o[0]/min(o[1],o[2]),3),o[0],o[1],o[2]) for o in sorted(big,key=lambda o:-o[0]/min(o[1],o[2]))[:8]])
big2=[o for o in ov if min(o[1],o[2])>=20]
print("paires >=20 chacun",len(big2),"max recouvrement",max([o[0] for o in big2] or [0]),"max coef",round(max([o[0]/min(o[1],o[2]) for o in big2] or [0]),3))
print("9W9b/Caw4 : coefficient recouvrement/min = 27/48 =",round(27/48,3))
# SOL contre USDC dans le témoin : seul moyen de voir un croisement d'actifs
cross=sorted(((len(sS[a]&sU[b]),len(sS[a]),len(sU[b]),a,b) for a in xs for b in xs if a!=b and sU[b]),reverse=True)
print("croisement SOL(a) x USDC(b) dans le témoin : paires testées",len(cross),"top",[(c[0],c[1],c[2],c[3][:8],c[4][:8]) for c in cross[:6]])
same=[(len(sS[x]&sU[x]),len(sS[x]),len(sU[x])) for x in xs if sU[x]]
print("même dépôt, SOL et USDC : recouvrement",sorted(same,reverse=True)[:6])
# Poids des expéditeurs communs (hot wallets, poussière) dans le témoin
cnt=collections.Counter(s for v in sS.values() for s in v)
print("expéditeurs à >=3 dépôts",[(k,c) for k,c in cnt.most_common(12) if c>=3])
gas="59L2oxymiQQ9Hvhh92nt8Y7nDYjsauFkdb3SybdnsG6h"
print("59L2oxym versé dans dépôts témoins (toute somme) :",sum(1 for x in xs if gas in sol[x]),[round(sol[x][gas],8) for x in xs if gas in sol[x]][:10])
