"""Réconciliation par ordre DCA : chaque ordre = le propriétaire (PDA) qui reçoit le DMAGA à l'ouverture. Ouvert, sorti par exécution, rendu au wallet, reste. Sorties i08_recon.csv, i08_recon.txt."""
import csv,sys,collections,datetime as dt
sys.path.insert(0,"audits/2026-11-03/work_I")
from i_lib import *
OUT="audits/2026-11-03/work_I/"
DCA="DCA265Vj8a9CEuX1eb1LWRnDT7uK6q1xMipnNyatn23M"
sys.stdout=open(OUT+"i08_recon.txt","w")
P1=[list(r.values())[0] for r in csv.DictReader(open("audits/2026-11-03/work_G/g40_p1_wallets.csv"))]
O={}
ev=[]
for w in P1:
    for t in iter_tx(w):
        if not ok(t) or DCA not in programs(t): continue
        ev.append((t["slot"],t["transactionIndex"],w,t["transaction"]["signatures"][0],t["meta"].get("logMessages") or [],tok_delta(t)[0]))
ev.sort(key=lambda e:e[:2])
seen=set()
for sl,ix,w,sg,logs,td in ev:
    if sg in seen: continue
    seen.add(sg)
    L=" ".join(logs)
    dm={o:v for (o,m),v in td.items() if m==DMAGA}
    if "OpenDca" in L and dm.get(w,0)<0:
        for o,v in dm.items():
            if v>0: O[o]=dict(wallet=w,open_sig=sg,slot=sl,opened=v/1e6,sold=0.0,back=0.0,nfill=0,usd=0.0)
        continue
    for o,v in dm.items():
        if o in O and v<0:
            if "FulfillFlashFill" in L:
                O[o]["sold"]+=-v/1e6; O[o]["nfill"]+=1
            elif dm.get(O[o]["wallet"],0)>0:
                O[o]["back"]+=-v/1e6
            else:
                O[o]["other"]=O[o].get("other",0)+(-v/1e6)
w=csv.writer(open(OUT+"i08_recon.csv","w")); w.writerow("order_pda wallet open_sig opened sold back other reste nfill".split())
tot=collections.Counter()
for o,d in O.items():
    r=d["opened"]-d["sold"]-d["back"]-d.get("other",0)
    w.writerow([o,d["wallet"],d["open_sig"],round(d["opened"],3),round(d["sold"],3),round(d["back"],3),round(d.get("other",0),3),round(r,3),d["nfill"]])
    tot["opened"]+=d["opened"];tot["sold"]+=d["sold"];tot["back"]+=d["back"];tot["other"]+=d.get("other",0);tot["reste"]+=r
print("ordres",len(O),{k:round(v/1e6,3) for k,v in tot.items()})
print("ordres avec reste > 1000 jetons",sum(1 for o,d in O.items() if d["opened"]-d["sold"]-d["back"]-d.get("other",0)>1000))
for o,d in sorted(O.items(),key=lambda kv:-(kv[1]["opened"]-kv[1]["sold"]-kv[1]["back"]-kv[1].get("other",0)))[:10]:
    print(" ",o[:10],d["wallet"][:10],"ouvert",round(d["opened"]/1e6,3),"vendu",round(d["sold"]/1e6,3),"rendu",round(d["back"]/1e6,3),"reste",round((d["opened"]-d["sold"]-d["back"]-d.get("other",0))/1e6,3),"fills",d["nfill"])
print("ordres intégralement rendus sans vente",sum(1 for d in O.values() if d["sold"]<1 and d["back"]>0),"jetons M",round(sum(d["back"] for d in O.values() if d["sold"]<1)/1e6,3))
