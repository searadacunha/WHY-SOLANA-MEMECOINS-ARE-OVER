"""Section 6 de G : recalcul des sommes depuis flow_boundaries.csv (dérivé de G, on teste son arithmétique), double compte entre périmètres, dates, puis part sur un périmètre non conditionné. Sortie i16_table.txt."""
import csv,collections,sys
OUT="audits/2026-11-03/work_I/"
sys.stdout=open(OUT+"i16_table.txt","w")
R=list(csv.DictReader(open("audits/2026-11-03/work_G/flow_boundaries.csv",encoding="utf-8")))
print("lignes",len(R),"colonnes",list(R[0].keys()))
print("périmètres",collections.Counter(r["perimetre_source"] for r in R))
PER=["P1 créateur et dépôt 9W9b","P2 groupe de 33 et salve du 23/07","H3QsBr","GXZvX","9PrmF8"]
T=collections.defaultdict(collections.Counter)
for r in R:
    if r["actif"]=="DMAGA" or r["perimetre_source"] not in PER: continue
    T[r["perimetre_source"]][r["type_frontiere"].split(" [")[0]]+=float(r["sol_eq"])
for p in PER:
    print(p)
    den=0
    for k,v in T[p].most_common():
        print("   ",round(v,1),k)
        if not k.startswith(("interne","pool ou route")): den+=v
    print("   dénominateur",round(den,1))
# double compte : même wallet source dans plusieurs périmètres ; même signature/destination dans plusieurs
src=collections.defaultdict(set);sg=collections.defaultdict(set)
kw=[k for k in R[0] if k in("wallet_source","source","wallet","from")]
print("clé wallet",kw)
