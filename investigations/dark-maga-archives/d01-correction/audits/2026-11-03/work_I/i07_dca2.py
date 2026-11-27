"""G3 suite. Pour les ordres DCA en DMAGA du périmètre : ouvert, rendu à la fermeture, réellement vendu, encaissé par exécution. Conversion SOL éq. au cours quotidien sol_daily.csv de G, seul fichier repris (contrôlé contre raw/solusd plus bas).
Sortie i07_dca2.txt, i07_fills.csv."""
import csv,sys,collections,datetime as dt,json,gzip,os,glob
sys.path.insert(0,"audits/2026-11-03/work_I")
from i_lib import *
OUT="audits/2026-11-03/work_I/"
DCA="DCA265Vj8a9CEuX1eb1LWRnDT7uK6q1xMipnNyatn23M"
sys.stdout=open(OUT+"i07_dca2.txt","w")
P1=[list(r.values())[0] for r in csv.DictReader(open("audits/2026-11-03/work_G/g40_p1_wallets.csv"))]
price={}
for r in csv.DictReader(open("audits/2026-11-03/work_G/sol_daily.csv")):
    k=list(r.keys()); price[r[k[0]][:10]]=float(r[k[-1]])
def pr(ts):
    d=dt.datetime.fromtimestamp(ts,dt.timezone.utc).strftime("%Y-%m-%d")
    return price[d]
opened=collections.defaultdict(float); ref=collections.defaultdict(float); orders=[]; cash=collections.Counter(); cashtok=collections.defaultdict(float); fills=[]
fw=csv.writer(open(OUT+"i07_fills.csv","w")); fw.writerow("wallet utc sig dmaga_sold out_mint out_amt soleq kind".split())
for w in P1:
    for t in iter_tx(w):
        if not ok(t) or DCA not in programs(t): continue
        logs=" ".join(t["meta"].get("logMessages") or [])
        td,dec=tok_delta(t); sd=sol_delta(t); ts=t["blockTime"]; sg=t["transaction"]["signatures"][0]
        u=dt.datetime.fromtimestamp(ts,dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        mine=td.get((w,DMAGA),0)
        if "OpenDca" in logs:
            if mine<0:
                orders.append((u,w,-mine/1e6,sg)); opened[w]+=-mine/1e6
            continue
        if "CloseDca" in logs or "EndAndClose" in logs:
            if mine>0: ref[w]+=mine/1e6
        # encaissement : le wallet reçoit stable/WSOL/SOL dans une tx où quelqu'un perd du DMAGA, ou dans une clôture
        sold=-sum(v for (o,m),v in td.items() if m==DMAGA and v<0)/1e6
        kind="fill" if "FulfillFlashFill" in logs else "close" if ("CloseDca" in logs or "EndAndClose" in logs) else "autre"
        rec=[]
        for m in (USDC,USDT,WSOL):
            v=td.get((w,m),0)
            if v>0: rec.append((m,v/10**dec[m]))
        for m,a in rec:
            se=a/pr(ts) if m in(USDC,USDT) else a
            fw.writerow([w,u,sg,sold,m,a,round(se,6),kind])
            fills.append((w,ts,sold,m,a,se,kind))
print("ordres ouverts en DMAGA (delta wallet négatif)",len(orders),"jetons M",round(sum(o[2] for o in orders)/1e6,3))
print("rendu à la clôture, M",round(sum(ref.values())/1e6,3))
print("vendu net, M",round((sum(opened.values())-sum(ref.values()))/1e6,3))
print("par wallet, plus gros",[(k[:8],round(v/1e6,3),round(ref[k]/1e6,3)) for k,v in sorted(opened.items(),key=lambda kv:-kv[1])[:10]])
# Encaissement : fills avec DMAGA vendu
fd=[f for f in fills if f[2]>0]
print("exécutions avec DMAGA qui sort",len(fd),"SOL éq.",round(sum(f[5] for f in fd),2),"USDC",round(sum(f[4] for f in fd if f[3]==USDC),2),"WSOL",round(sum(f[4] for f in fd if f[3]==WSOL),2),"USDT",round(sum(f[4] for f in fd if f[3]==USDT),2))
print(" jetons vendus par ces exécutions, M",round(sum(f[2] for f in fd)/1e6,3))
print(" stables reçus dans tx sans DMAGA (DCA d'autres jetons, exclus)",round(sum(f[5] for f in fills if f[2]==0),2))
print("ordres du 21/07")
for o in sorted(orders):
    if o[0].startswith("2024-07-1") or o[0].startswith("2024-07-2"): print(" ",o[0],o[1],round(o[2],3),o[3])
d=collections.Counter(o[0][:7] for o in orders); print("par mois",sorted(d.items()))
S0=1721590213
print("encaissé 24 h après 19:30:13, SOL éq.",round(sum(f[5] for f in fd if S0<=f[1]<S0+86400),2),"avant",round(sum(f[5] for f in fd if f[1]<S0),2))
# Salve du 22/07 05:22:29 à 05:24:16
s=[r for r in csv.DictReader(open(OUT+"i01_moves.csv")) if r["depot"]=="Caw4" and r["side"]=="in" and "2024-07-22T05:2"<=r["utc"]<"2024-07-22T05:3"]
print("salve",[(r["utc"],r["asset"],r["cp"][:8],r["amount"]) for r in s],"USDC",round(sum(float(r["amount"]) for r in s if r["asset"]=="USDC"),6))
# Part vendue par la salve par rapport aux encaissements de ces wallets
