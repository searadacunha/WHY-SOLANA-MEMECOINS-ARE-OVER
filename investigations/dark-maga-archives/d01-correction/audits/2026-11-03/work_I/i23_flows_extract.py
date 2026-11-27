"""Extrait de raw/flows : tous les sol_out_after et usdc_out_after, ligne par ligne, vers un CSV gz sur le disque USB (traitement en flux). Colonnes src dst asset amount bt truncated. Sortie audits_work/I/flows_out.csv.gz."""
import gzip,json,os,csv
R="/Volumes/VERBATIM HD/Dark-MAGA-Investigation"
d=R+"/raw/flows";out=gzip.open(R+"/audits_work/I/flows_out.csv.gz","wt");w=csv.writer(out);w.writerow("src dst asset amount bt truncated sig".split())
n=tr=0
for x in sorted(os.listdir(d)):
    if x.startswith("._"):continue
    for f,a,dec in (("sol_out_after","SOL",9),("usdc_out_after","USDC",6),("usdt_out_after","USDT",6)):
        p=f"{d}/{x}/{f}.json.gz"
        if not os.path.exists(p):continue
        o=json.load(gzip.open(p,"rt"));tt=int(bool(o.get("truncated")));tr+=tt
        for r in o["rows"]:
            if r.get("toUserAccount")==x: continue
            w.writerow([x,r.get("toUserAccount"),a,int(r["amount"])/10**dec,r["blockTime"],tt,r["signature"]]);n+=1
out.close();print("lignes",n,"fichiers tronqués",tr)
