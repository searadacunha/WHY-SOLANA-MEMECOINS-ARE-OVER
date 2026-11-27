"""Résumé de i14_orders.csv : jetons donnés, sommes, par maker, par receveur, champs atypiques, comparaison ligne à ligne avec g43_orders.csv. Sortie i15_dln_sum.txt."""
import csv,collections,sys,json
OUT="audits/2026-11-03/work_I/"
sys.stdout=open(OUT+"i15_dln_sum.txt","w")
R=list(csv.DictReader(open(OUT+"i14_orders.csv")))
G={r["signature"]:r for r in csv.DictReader(open("audits/2026-11-03/work_G/g43_orders.csv"))}
print("ordres",len(R),"G",len(G),"signatures communes",len({r["sig"] for r in R}&set(G)))
print("donné, par jeton",collections.Counter(r["give_token"] for r in R))
print("chaîne d'origine",collections.Counter(r["give_chain"] for r in R),"arrivée",collections.Counter(r["take_chain"] for r in R))
print("jeton d'arrivée",collections.Counter((r["take_chain"],r["take_token"]) for r in R).most_common())
print("appel externe",sum(1 for r in R if r["ext"]),"taker imposé",sum(1 for r in R if r["allowed_taker"]),"bénéficiaire d'annulation",sum(1 for r in R if r["cancel_benef"]),"receveur != autorité",sum(1 for r in R if r["receiver"]!=r["oauth"]),"maker != signataire",sum(1 for r in R if r["maker"]!=r["signer"]),"maker != fichier",sum(1 for r in R if r["maker"]!=r["wallet_file"]))
tot=sum(int(r["give_amount"]) for r in R)/1e6; totf=sum(int(r["give_amount"])+int(r["fee_pct"]) for r in R)/1e6
print("somme give (après frais %)",round(tot,2),"give+frais %",round(totf,2))
gs=sum(float(x["usd_sortis"]) for x in G.values());print("somme G usd_sortis",round(gs,2))
dif=[(r["sig"][:10],(int(r["give_amount"])+int(r["fee_pct"]))/1e6,G[r["sig"]]["usd_sortis"]) for r in R if r["sig"] in G and abs((int(r["give_amount"])+int(r["fee_pct"]))/1e6-float(G[r["sig"]]["usd_sortis"]))>0.02]
print("écarts avec G > 0,02",dif[:20])
difr=[r["sig"][:10] for r in R if r["sig"] in G and r["receiver"]!=G[r["sig"]]["receiver_dst"]]; print("receveurs différents de G",difr)
by=collections.defaultdict(lambda:[0.0,0,None,None])
for r in R:
    v=(int(r["give_amount"])+int(r["fee_pct"]))/1e6;b=by[r["maker"]];b[0]+=v;b[1]+=1;b[2]=min(b[2] or r["utc"],r["utc"]);b[3]=max(b[3] or r["utc"],r["utc"])
print("par maker")
for k,v in sorted(by.items(),key=lambda kv:-kv[1][0]): print(" ",k,round(v[0],2),v[1],v[2],v[3])
rv=collections.defaultdict(lambda:[0.0,0,set(),None,None,set()])
for r in R:
    v=(int(r["give_amount"])+int(r["fee_pct"]))/1e6;b=rv[r["receiver"]];b[0]+=v;b[1]+=1;b[2].add(r["maker"][:8]);b[3]=min(b[3] or r["utc"],r["utc"]);b[4]=max(b[4] or r["utc"],r["utc"]);b[5].add(r["take_chain"])
print("par receveur")
for k,v in sorted(rv.items(),key=lambda kv:-kv[1][0]): print(" ",k,round(v[0],2),v[1],sorted(v[2]),v[3],v[4],sorted(v[5]))
print("receveurs à plusieurs makers",[(k,sorted(v[2]),round(v[0],2)) for k,v in rv.items() if len(v[2])>1])
print("0xb947 détail")
for r in sorted(R,key=lambda r:r["utc"]):
    if r["receiver"].startswith("0xb947"): print(" ",r["utc"],r["maker"],(int(r["give_amount"])+int(r["fee_pct"]))/1e6,r["take_chain"],r["take_token"],r["take_raw"],r["receiver"],r["sig"])
print("C73 détail")
for r in sorted(R,key=lambda r:r["utc"]):
    if r["maker"].startswith("C73Yv9iH"): print(" ",r["utc"],(int(r["give_amount"])+int(r["fee_pct"]))/1e6,r["take_chain"],r["take_token"],r["take_raw"],r["receiver"])
# Valeur de sortie relative : ETH et stables
