"""Recouvrement 9W9b / Caw4 depuis i01_moves.csv, à plusieurs seuils, avec routage et signataire. Sortie i02_overlap.txt, i02_senders.csv."""
import csv, collections, sys
OUT="audits/2026-11-03/work_I/"
sys.stdout=open(OUT+"i02_overlap.txt","w")
rows=[r for r in csv.DictReader(open(OUT+"i01_moves.csv")) if r["side"]=="in" and r["depot"] in("9W9b","Caw4")]
agg=collections.defaultdict(lambda:[0.0,0,0,None,None,0,0])  # (depot,asset,cp)-> somme, n, routed, first,last, n signer!=cp
for r in rows:
    a=agg[(r["depot"],r["asset"],r["cp"])]
    a[0]+=float(r["amount"]);a[1]+=1;a[2]+=int(r["routed"]);a[3]=min(a[3] or r["utc"],r["utc"]);a[4]=max(a[4] or r["utc"],r["utc"]);a[5]+=(r["signer"]!=r["cp"])
def S(dep,th_sol,th_usd):
    s=set()
    for (d,asset,c),v in agg.items():
        if d!=dep or c=="?":continue
        if (asset in("SOL","WSOL") and v[0]>=th_sol) or (asset in("USDC","USDT") and v[0]>=th_usd):s.add(c)
    return s
for ts,tu in [(0,0),(0.001,0.1),(0.01,1),(0.05,5),(0.1,10),(0.5,50),(1,100),(5,500)]:
    a,b=S("9W9b",ts,tu),S("Caw4",ts,tu)
    print(f"seuil somme {ts} SOL, {tu} USD: 9W9b {len(a)} Caw4 {len(b)} communs {len(a&b)} part de 9W9b {len(a&b)/max(1,len(a)):.3f} part de Caw4 {len(a&b)/max(1,len(b)):.3f}")
a,b=S("9W9b",0.01,1),S("Caw4",0.01,1)
print("\nexpéditeurs avec routage (programme hors BASIC) ou signataire différent, seuil 0,01/1")
for k,v in sorted(agg.items()):
    if k[0] in("9W9b","Caw4") and (v[2] or v[5]) and ((k[1]=="SOL" and v[0]>=0.01) or (k[1]!="SOL" and v[0]>=1)):
        print(k,round(v[0],4),"n",v[1],"routed",v[2],"signer!=cp",v[5],v[3],v[4])
w=csv.writer(open(OUT+"i02_senders.csv","w"));w.writerow("sender in9W9b inCaw4 sol_9W9b n9 first9 last9 usd_Caw4 solCaw4 nC firstC lastC".split())
for s in sorted(a|b):
    x=agg.get(("9W9b","SOL",s),[0,0,0,None,None,0,0]);y=agg.get(("Caw4","USDC",s),[0,0,0,None,None,0,0]);z=agg.get(("Caw4","SOL",s),[0,0,0,None,None,0,0])
    w.writerow([s,int(s in a),int(s in b),round(x[0],6),x[1],x[3],x[4],round(y[0],6),round(z[0],6),y[1]+z[1],y[3] or z[3],y[4] or z[4]])
tot9=sum(v[0] for k,v in agg.items() if k[0]=="9W9b" and k[1]=="SOL" and k[2] in a)
tot9c=sum(v[0] for k,v in agg.items() if k[0]=="9W9b" and k[1]=="SOL" and k[2] in a&b)
totC=sum(v[0] for k,v in agg.items() if k[0]=="Caw4" and k[1]=="USDC" and k[2] in b)
totCc=sum(v[0] for k,v in agg.items() if k[0]=="Caw4" and k[1]=="USDC" and k[2] in a&b)
print("\nSOL 9W9b par expéditeurs communs",round(tot9c,3),"sur",round(tot9,3),"; USDC Caw4 par communs",round(totCc,2),"sur",round(totC,2))
print("communs",len(a&b));print("réunion",len(a|b))
print("expéditeurs Caw4 seuil 0,01/1 hors USDC (SOL seul):",[ (k[2],round(v[0],5)) for k,v in agg.items() if k[0]=="Caw4" and k[1]=="SOL" and v[0]>=0.01])
