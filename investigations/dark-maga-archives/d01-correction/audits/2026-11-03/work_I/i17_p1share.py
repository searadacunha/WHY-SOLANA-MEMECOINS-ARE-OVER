"""86,6 % : refait sur le brut, virements purs (programmes BASIC seuls), sortants de chaque wallet de P1, seuil 0,01 SOL ou 1 USD, hors interne à P1. Part vers 9W9b et Caw4 : tout P1 ; série + créateur seuls (définis avant les dépôts) ; expéditeurs seuls (définis PAR le dépôt) ; après le mint seulement. Sorties i17_p1share.txt, i17_rows.csv."""
import csv,sys,collections,datetime as dt
sys.path.insert(0,"audits/2026-11-03/work_I")
from i_lib import *
OUT="audits/2026-11-03/work_I/"
sys.stdout=open(OUT+"i17_p1share.txt","w")
price={r["date"]:float(r["close"]) for r in csv.DictReader(open("audits/2026-11-03/work_G/sol_daily.csv"))}
def px(ts):
    d=dt.datetime.fromtimestamp(ts,dt.timezone.utc).strftime("%Y-%m-%d")
    return price.get(d) or (price[min(price)] if d<min(price) else price[max(price)])
P1=[list(r.values())[0] for r in csv.DictReader(open("audits/2026-11-03/work_G/g40_p1_wallets.csv"))]
P1s=set(P1)
series={r["wallet"] for r in csv.DictReader(open("audits/2026-11-03/work_C/cb_series.csv"))}
CR="8YLEuUtZ4eFMJbf46oNb1CeG6dYFWGyxnQSh9hrgzBzR"
D9="9W9b3zgHH9mCEHDhsdbnbEPHStm9vvXS4aia4DWHBxpL";DC="Caw4RrwkmxqtbLSFzgSs6id3XiFxWQxs2t1mrn5a3mME"
MINT=1720922725
w=csv.writer(open(OUT+"i17_rows.csv","w"));w.writerow("src dst asset amount soleq utc sig".split())
rows=[]
seen=set()
for s in P1:
    for t in iter_tx(s):
        if not ok(t) or s not in signers(t) or programs(t)-BASIC: continue
        sg=t["transaction"]["signatures"][0]
        if (s,sg) in seen: continue
        seen.add((s,sg))
        ts=t["blockTime"];sd=sol_delta(t);td,dec=tok_delta(t)
        fee=t["meta"]["fee"]
        v=-sd.get(s,0)-fee
        if v>=1e7:
            pos={k:x for k,x in sd.items() if x>0 and k!=s}
            tot=sum(pos.values()) or 1
            for k,x in pos.items():
                rows.append((s,k,"SOL",x/1e9,x/1e9,ts,sg))
        for (o,m),x in td.items():
            if o==s and x<0 and m in(USDC,USDT):
                pos=[(o2,y) for (o2,m2),y in td.items() if m2==m and y>0 and o2!=s]
                for o2,y in pos:
                    a=y/1e6
                    if a>=1: rows.append((s,o2,"USD",a,a/px(ts),ts,sg))
for r in rows:
    w.writerow([r[0],r[1],r[2],r[3],round(r[4],6),dt.datetime.fromtimestamp(r[5],dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),r[6]])
def share(f,label):
    x=[r for r in rows if f(r) and r[1] not in P1s]
    den=sum(r[4] for r in x); num=sum(r[4] for r in x if r[1] in(D9,DC)); n9=sum(r[4] for r in x if r[1]==D9); nc=sum(r[4] for r in x if r[1]==DC)
    print(f"{label}: dénominateur {den:.1f} ; vers les 2 dépôts {num:.1f} = {100*num/max(den,1e-9):.1f} % (9W9b {n9:.1f}, Caw4 {nc:.1f}) ; wallets {len({r[0] for r in x})}")
    return x
share(lambda r:True,"P1 entier, 46 wallets")
share(lambda r:r[5]>=MINT,"P1 après le mint")
share(lambda r:r[5]<MINT,"P1 avant le mint")
core=series|{CR}
share(lambda r:r[0] in core,"série + créateur, seuls définis sans le dépôt")
share(lambda r:r[0] in core and r[5]>=MINT,"série + créateur après le mint")
share(lambda r:r[0] not in core,"hors série : expéditeurs de 9W9b, définis par le dépôt")
x=[r for r in rows if r[0] in core and r[1] not in P1s and r[1] not in (D9,DC)]
c=collections.Counter()
for r in x:c[r[1]]+=r[4]
print("destinations hors dépôts de série + créateur",[(k[:10],round(v,2)) for k,v in c.most_common(12)])
print("série lue",len(core&set(P1)),"sur",len(core),"hors P1",[k for k in core if k not in P1s])
y=[r for r in rows if r[1] not in P1s and r[1] not in (D9,DC)]
c=collections.Counter()
for r in y:c[r[1]]+=r[4]
print("destinations hors dépôts de P1",[(k[:10],round(v,2)) for k,v in c.most_common(12)])
