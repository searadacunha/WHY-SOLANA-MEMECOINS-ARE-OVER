"""Ligne « pont » de la table : pour chaque (source, receveur), montant de G contre décodage propre, et SOL éq. recalculé au cours du jour. Sortie i19_bridge_row.txt."""
import csv,collections,sys
OUT="audits/2026-11-03/work_I/"
sys.stdout=open(OUT+"i19_bridge_row.txt","w")
price={r["date"]:float(r["close"]) for r in csv.DictReader(open("audits/2026-11-03/work_G/sol_daily.csv"))}
O=list(csv.DictReader(open(OUT+"i14_orders.csv")))
D=collections.defaultdict(lambda:[0.0,0.0,0])
for r in O:
    v=(int(r["give_amount"])+int(r["fee_pct"]))/1e6
    d=D[(r["maker"],r["receiver"])];d[0]+=v;d[1]+=v/price.get(r["utc"][:10],price[min(price)]);d[2]+=1
F=[r for r in csv.DictReader(open("audits/2026-11-03/work_G/flow_boundaries.csv",encoding="utf-8")) if r["type_frontiere"].startswith("pont")]
gt=collections.Counter();mt=collections.Counter();ms=collections.Counter();per={}
seen=set()
for r in F:
    k=(r["wallet_source"],r["destination"]);seen.add(k)
    m=D.get(k,[0,0,0]);per[k]=r["perimetre_source"]
    print(k[0][:8],k[1][:10],r["actif"][:22],"G montant",round(float(r["montant"]),2),"n",r["n"],"G soleq",round(float(r["sol_eq"]),2),"| moi",round(m[0],2),"n",m[2],"soleq",round(m[1],2),"|",r["perimetre_source"][:2])
    gt[r["perimetre_source"]]+=float(r["sol_eq"]);ms[r["perimetre_source"]]+=m[1];mt[r["perimetre_source"]]+=m[0]
print("non vus dans la table de G",[(k[0][:8],k[1][:10],round(v[0],2)) for k,v in D.items() if k not in seen])
print("G SOL éq.",{k[:2]:round(v,1) for k,v in gt.items()});print("moi SOL éq.",{k[:2]:round(v,1) for k,v in ms.items()});print("moi USD",{k[:2]:round(v,2) for k,v in mt.items()})
print("P2 part corrigée",round(100*ms["P2 groupe de 33 et salve du 23/07"]/(12292.2-gt["P2 groupe de 33 et salve du 23/07"]+ms["P2 groupe de 33 et salve du 23/07"]),2))
print("total table part pont corrigée",round(100*(ms["P2 groupe de 33 et salve du 23/07"]+ms["P1 créateur et dépôt 9W9b"])/25735.4,2))
