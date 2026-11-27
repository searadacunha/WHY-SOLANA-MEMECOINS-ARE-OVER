"""G2 refait sans filtre. Destinataires des retraits Coinbase (cb_window.csv de C, seule trace : les pages brutes de C n'ont pas été gardées) croisés avec TOUS les expéditeurs bruts des deux dépôts, sans seuil.
Puis contrôle par les historiques bruts : chaque retrait cité existe-t-il dans le net du wallet ? Puis premier financeur des 76 expéditeurs. Sortie i05_g2.txt."""
import csv,sys,collections,datetime as dt,gzip,json,os
sys.path.insert(0,"audits/2026-11-03/work_I")
from i_lib import *
OUT="audits/2026-11-03/work_I/"
sys.stdout=open(OUT+"i05_g2.txt","w")
HOT={"H8sMJSCQxfKiFTCfDR3DUMLPwcRbM61LGFJ8N4dK3WjS","2AQdpHJ2JpcEgPiATUXjQxA8QmafFegfQwSLWSprPicm","GJRs4FwHtemZ5ZE9x3FNvJ8TMwitKTh21yxdRPqn7npE"}
FAM={"D89hHJT5Aqyx1trP6EnGY9jJUB3whgnq3aUvvCqedvzf","FpwQQhQQoEaVu3WU2qZMfF1hx48YyfwsLoRgXG83E99Q","DPqsobysNf5iA9w7zrQM8HLzCKZEDMkZsWbiidsAt1xo","9obNtb5GyUegcs3a1CbBkLuc5hEWynWfJC6gjz5uWQkE","4NyK1AdJBNbgaJ9EsKz3J4rfeHsuYdjkTPg3JaNdLeFw","8JUEoHNMbWM4eegcMvx6ZQJt3V3fbo8JNjpWiCtJgxfF"}
mv=[r for r in csv.DictReader(open(OUT+"i01_moves.csv")) if r["side"]=="in"]
amt=collections.defaultdict(float)
for r in mv: amt[(r["depot"],r["cp"],"SOL" if r["asset"]=="SOL" else "USD")]+=float(r["amount"])
S9={k[1] for k in amt if k[0]=="9W9b"}; SC={k[1] for k in amt if k[0]=="Caw4"}
cb=list(csv.DictReader(open("audits/2026-11-03/work_C/cb_window.csv")))
dest={r["dest"] for r in cb}
print("retraits",len(cb),"destinataires",len(dest),cb[0]["utc"],cb[-1]["utc"])
print("SANS SEUIL expéditeurs bruts : 9W9b",len(S9),"Caw4",len(SC),"réunion",len(S9|SC))
print(" croisement sans seuil : 9W9b",len(dest&S9),"Caw4",len(dest&SC),"les deux",len(dest&S9&SC),"réunion",len(dest&(S9|SC)))
L=sorted((r["utc"],r["dest"],r["sol"],r["hot"]) for r in cb if r["dest"] in S9|SC)
for x in L:
    d=x[1]; print(" ",x[0],x[3],d,x[2],"sol9",round(amt.get(("9W9b",d,"SOL"),0),6),"usdC",round(amt.get(("Caw4",d,"USD"),0),4),"solC",round(amt.get(("Caw4",d,"SOL"),0),6))
ts=lambda u:dt.datetime.strptime(u,"%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=dt.timezone.utc).timestamp()
a,b=ts("2024-07-14T01:32:23Z"),ts("2024-07-14T01:40:50Z")
wd=[r for r in cb if a<=ts(r["utc"])<=b]
print("fenêtre 507 s : retraits",len(wd),"destinataires",len({r["dest"] for r in wd}),"; 2 h :",round(ts(cb[-1]["utc"])-ts(cb[0]["utc"])),"s")
print(" taux de retraits par 507 s sur 2 h",round(len(cb)*507/(ts(cb[-1]["utc"])-ts(cb[0]["utc"])),1))
# fenêtre glissante : autres grappes de retraits ronds vers wallets qui reviennent (aucune), et répartition hors 507 s
inwin={x[1] for x in L if a<=ts(x[0])<=b}
print(" dans 507 s",len(inwin),"hors",len({x[1] for x in L})-len(inwin))
# Le retrait existe-t-il dans le net du wallet, et est-ce sa première tx ?
print("contrôle brut des retraits des wallets cités")
seen=set()
for x in L+[("", "A52fNskQ?", "", "")]:
    d=x[1]
    if d in seen or d.endswith("?"):continue
    seen.add(d)
    ps=net_paths(d)
    if not ps: print(" ",d,"pas d'historique net");continue
    first=None;found=None;n=0
    for t in iter_tx(d):
        n+=1
        if first is None or (t["slot"],t["transactionIndex"])<(first["slot"],first["transactionIndex"]): first=t
        sd=sol_delta(t)
        if any(h in sd and sd[h]<0 for h in HOT) and sd.get(d,0)>0 and t["blockTime"]<=b+60: found=t
    print(" ",d,"tx",n,"retrait vu" if found else "retrait NON vu","première tx = retrait" if found is first else "première tx autre",dt.datetime.fromtimestamp(first["blockTime"],dt.timezone.utc).strftime("%m-%dT%H:%M:%S"))
# Premiers financeurs des expéditeurs >= 0,01/1
ss=list(csv.DictReader(open(OUT+"i02_senders.csv")))
print("\nPremier financeur en SOL des 76 expéditeurs, raw/flows/first_in si présent, sinon net")
c=collections.Counter(); rows=[]
for r in ss:
    s=r["sender"]; p=f"{R}/raw/flows/{s}/first_in.json.gz"; fr=None
    if os.path.exists(p):
        rr=json.load(gzip.open(p,"rt"))["rows"]
        if rr: fr=(rr[0]["blockTime"],rr[0]["fromUserAccount"],int(rr[0]["amount"])/1e9,"flows")
    if fr is None and net_paths(s):
        best=None
        for t in iter_tx(s):
            sd=sol_delta(t)
            if sd.get(s,0)>0 and (best is None or t["blockTime"]<best[0]):
                neg=[k for k,v in sd.items() if v<0]
                best=(t["blockTime"],neg[0] if neg else "?",sd[s]/1e9,"net")
        fr=best
    lab="absent" if fr is None else ("Coinbase3etiq" if fr[1] in HOT else "famille" if fr[1] in FAM else "autre")
    c[lab]+=1
    rows.append((fr[0] if fr else 0,s,fr[1] if fr else "",fr[2] if fr else 0,lab,fr[3] if fr else "",r["in9W9b"],r["inCaw4"]))
print(c)
for x in sorted(rows):
    if x[4] in("Coinbase3etiq","famille"): print(" ",dt.datetime.fromtimestamp(x[0],dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S"),x[1],x[2][:8],round(x[3],4),x[4],x[5],x[6],x[7])
