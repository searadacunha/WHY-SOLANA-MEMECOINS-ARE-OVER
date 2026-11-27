"""Ordres DCA DMAGA : encaissement en SOL natif, omis ou non ? Par ordre : mint de sortie vu, SOL natif reçu par le wallet dans les exécutions. Sortie i10_dca_sol.txt, i10_orders.csv."""
import csv,sys,collections,datetime as dt
sys.path.insert(0,"audits/2026-11-03/work_I")
from i_lib import *
OUT="audits/2026-11-03/work_I/"
sys.stdout=open(OUT+"i10_dca_sol.txt","w")
price={r["date"]:float(r["close"]) for r in csv.DictReader(open("audits/2026-11-03/work_G/sol_daily.csv"))}
ord_={r["order_pda"]:r for r in csv.DictReader(open(OUT+"i08_recon.csv"))}
byw=collections.defaultdict(set)
for o,r in ord_.items(): byw[r["wallet"]].add(o)
A=collections.defaultdict(lambda:dict(usd=0.0,sol=0.0,fills=0,sold=0.0,wsol_pda=0.0,other=collections.Counter()))
ex=[]
for w,os_ in byw.items():
    for t in iter_tx(w):
        if not ok(t): continue
        td,dec=tok_delta(t); logs=" ".join(t["meta"].get("logMessages") or [])
        hit={o for (o,m) in td}&os_
        if not hit or "OpenDca" in logs or "FulfillFlashFill" not in logs: continue
        o=sorted(hit)[0]; a=A[o]; a["fills"]+=1
        a["sold"]+=-sum(v for (x,m),v in td.items() if x==o and m==DMAGA and v<0)/1e6
        for (x,m),v in td.items():
            if x==w and v>0 and m==USDC: a["usd"]+=v/1e6
            elif x==w and v>0 and m!=DMAGA: a["other"][m]+=v/10**dec[m]
        sd=sol_delta(t).get(w,0)
        S=signers(t)
        if sd>0: 
            a["sol"]+=sd/1e9
            if len(ex)<6 and sd>1e8: ex.append((t["transaction"]["signatures"][0],sd/1e9,S[0]==w,o[:8]))
w_=csv.writer(open(OUT+"i10_orders.csv","w")); w_.writerow("pda wallet opened sold back fills usdc sol_natif autres px_usd_par_M px_sol_par_M".split())
tu=ts=0;nsol=0;soldsol=0;soldusd=0
for o,a in A.items():
    r=ord_[o]
    w_.writerow([o,r["wallet"],r["opened"],round(a["sold"],2),r["back"],a["fills"],round(a["usd"],2),round(a["sol"],6),dict(a["other"]),round(a["usd"]/max(a["sold"]/1e6,1e-9),1),round(a["sol"]/max(a["sold"]/1e6,1e-9),2)])
    tu+=a["usd"];ts+=a["sol"]
    if a["usd"]<1: nsol+=1; soldsol+=a["sold"]
    else: soldusd+=a["sold"]
print("ordres avec exécution",len(A),"USDC",round(tu,2),"SOL natif reçu",round(ts,4))
print("ordres sans USDC",nsol,"jetons M vendus",round(soldsol/1e6,3),"; ordres en USDC, jetons M",round(soldusd/1e6,3))
print("exemples",ex)
print("sans USDC :")
for o,a in A.items():
    if a["usd"]<1: print(" ",o[:10],ord_[o]["wallet"][:10],"vendu M",round(a["sold"]/1e6,3),"SOL",round(a["sol"],3),"fills",a["fills"],dict(a["other"]))
