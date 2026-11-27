"""Double compte dans la table de G : un ordre de pont compté aussi comme virement vers le compte de l'ordre ? Propriétaires des comptes d'ordre lus dans le brut. Répartition des ordres par périmètre. Doublons entre périmètres. Sortie i18_dbl.txt, i18_give_accounts.csv."""
import csv,sys,collections,gzip,json,os
sys.path.insert(0,"audits/2026-11-03/work_I")
from i_lib import *
OUT="audits/2026-11-03/work_I/"
sys.stdout=open(OUT+"i18_dbl.txt","w")
O={r["sig"]:r for r in csv.DictReader(open(OUT+"i14_orders.csv"))}
give={}
rows=[]
seen=set()
for sg,r in O.items():
    w=r["wallet_file"]
    for t in iter_tx(w):
        s=t["transaction"]["signatures"][0]
        if s!=sg: continue
        keys_=keys(t)
        post=t["meta"]["postTokenBalances"];pre=t["meta"]["preTokenBalances"]
        p0={b["accountIndex"]:int(b["uiTokenAmount"]["amount"]) for b in pre if b["mint"]==USDC}
        best=None
        for b in post:
            if b["mint"]!=USDC: continue
            d=int(b["uiTokenAmount"]["amount"])-p0.get(b["accountIndex"],0)
            if b["owner"]!=r["maker"] and d>0:
                exact=(d==int(r["give_amount"])+int(r["fee_pct"]) or d==int(r["give_amount"]))
                if exact: best=(keys_[b["accountIndex"]],b["owner"],d)
        rows.append((sg,r["maker"],r["utc"],int(r["give_amount"]),int(r["fee_pct"]),best))
        break
w=csv.writer(open(OUT+"i18_give_accounts.csv","w"));w.writerow("sig maker utc give fee token_account owner delta".split())
for x in rows:
    w.writerow([x[0],x[1],x[2],x[3],x[4],*(x[5] or ("","",""))])
print("ordres avec compte de dépôt identifié",sum(1 for x in rows if x[5]),"sur",len(rows))
owners={x[5][1] for x in rows if x[5]};taccs={x[5][0] for x in rows if x[5]}
F=list(csv.DictReader(open("audits/2026-11-03/work_G/flow_boundaries.csv",encoding="utf-8")))
dbl=[r for r in F if r["destination"] in owners or r["destination"] in taccs]
print("lignes de la table vers un compte d'ordre",len(dbl))
for r in dbl: print(" ",r["wallet_source"][:8],r["destination"][:10],r["actif"],r["montant"],r["sol_eq"],r["type_frontiere"],r["perimetre_source"],r["date_debut"])
print("SOL éq.",round(sum(float(r["sol_eq"]) for r in dbl),1))
# Répartition des ordres par périmètre selon la table
B=[r for r in F if r["type_frontiere"].startswith("pont")]
print("lignes pont",len(B),"par périmètre",collections.Counter(r["perimetre_source"] for r in B))
c=collections.Counter();u=collections.Counter()
for r in B:
    c[r["perimetre_source"]]+=float(r["sol_eq"]);
    if "USDC" in r["actif"]: u[r["perimetre_source"]]+=float(r["montant"])
print("SOL éq.",dict(c),"USD",dict(u))
per=collections.defaultdict(set)
for r in F:
    per[r["wallet_source"]].add(r["perimetre_source"])
print("wallets dans >1 périmètre",[(k[:8],sorted(v)) for k,v in per.items() if len(v)>1][:20])
print("ordres hors périmètres (hors dénominateur)",[(r["wallet_source"][:8],r["montant"]) for r in B if r["perimetre_source"] not in("P1 créateur et dépôt 9W9b","P2 groupe de 33 et salve du 23/07")])
MINT="2024-07-14T02:05:25Z"
pre=[r for r in O.values() if r["utc"]<MINT]
print("ordres avant le mint",len(pre),"USD",round(sum((int(r["give_amount"])+int(r["fee_pct"]))/1e6 for r in pre),2),collections.Counter(r["maker"][:8] for r in pre))
post=[r for r in O.values() if r["utc"]>=MINT]
print("après",len(post),round(sum((int(r["give_amount"])+int(r["fee_pct"]))/1e6 for r in post),2))
d1=[r for r in post if "2024-07-21T22:53:42Z"<=r["utc"]<"2024-07-22T22:53:42Z" and r["receiver"].startswith("0x2d86")]
print("vers 0x2d86 dans les 24 h après 22:53:42",len(d1),round(sum((int(r["give_amount"])+int(r["fee_pct"]))/1e6 for r in d1),2))
# 0xb29826
for r in sorted(O.values(),key=lambda r:r["utc"]):
    if r["receiver"].startswith("0xb29826"): print(" b298",r["utc"],r["maker"][:8],round((int(r["give_amount"])+int(r["fee_pct"]))/1e6,2),r["take_chain"],r["take_token"][:8])
# flows hors historique : la part qui peut être un swap
H=collections.Counter()
for r in F:
    if "hors historique" in r["type_frontiere"] or "hors historique" in r["precision"]:
        H[(r["perimetre_source"],r["type_frontiere"][:40])]+=float(r["sol_eq"])
print("hors historique",[(k,round(v,1)) for k,v in H.most_common(12)])
