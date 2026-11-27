"""G6 : tous les dépôts contre tous, sur le brut, sans filtre puis filtrés. Sorties i24_cross.txt, i24_dep_senders.csv (dépôt, expéditeur, actif, somme, n, première, dernière)."""
import csv,sys,collections,itertools,datetime as dt
sys.path.insert(0,"audits/2026-11-03/work_I")
from i_lib import *
OUT="audits/2026-11-03/work_I/"
sys.stdout=open(OUT+"i24_cross.txt","w")
DEP={"9W9b":"9W9b3zgHH9mCEHDhsdbnbEPHStm9vvXS4aia4DWHBxpL","Caw4":"Caw4RrwkmxqtbLSFzgSs6id3XiFxWQxs2t1mrn5a3mME","AQVg":"AQVgyg8P5Yh5YcAqAMQRRGzDegy1R58gN4Qh87QsJAF1","By6D":"By6Dao4QMNeBxmdUrqsoQA8dCGbHz7xWj57CdHV5M47r","H9Xe":"H9XezqfdXuv4ZCHAAZ92oMLSSAPB6Dgm4ZSrRythCbPi","8N4A":"8N4AvP9j5BditSQMk2WrTNxthhgpncGVzLKrYP4xdEqx","42MS":"42MSVeV4YbESE7mNW7DfQrfd8E4RG6njxXZLAWTmXemv","9kqT":"9kqTVnRUkVTFD7na9BTWcoG9piL4XpVTtS9kqVCV56tV"}
A=collections.defaultdict(lambda:[0.0,0,None,None])
sw=collections.defaultdict(collections.Counter)
nt={}
for tag,d in DEP.items():
    n=0
    for t in iter_tx(d):
        n+=1
        if not ok(t):continue
        ts=t["blockTime"];sd=sol_delta(t);td,dec=tok_delta(t)
        v=sd.get(d,0)
        if v>0:
            for k,x in sd.items():
                if x<0 and k!=d:
                    a=A[(tag,k,"SOL")];a[0]+=min(v,-x)/1e9;a[1]+=1;a[2]=min(a[2] or ts,ts);a[3]=max(a[3] or ts,ts)
        for (o,m),x in td.items():
            if o==d and x>0 and m!=DMAGA:
                for (o2,m2),y in td.items():
                    if m2==m and y<0 and o2!=d:
                        a=A[(tag,o2,{USDC:"USDC",USDT:"USDT",WSOL:"WSOL"}.get(m,m[:6]))];a[0]+=min(x,-y)/10**dec[m];a[1]+=1;a[2]=min(a[2] or ts,ts);a[3]=max(a[3] or ts,ts)
    nt[tag]=n
w=csv.writer(open(OUT+"i24_dep_senders.csv","w"));w.writerow("depot sender asset somme n first last".split())
for (tag,k,a),v in sorted(A.items()):
    w.writerow([tag,k,a,round(v[0],6),v[1],dt.datetime.fromtimestamp(v[2],dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),dt.datetime.fromtimestamp(v[3],dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")])
def S(th_s,th_u):
    s=collections.defaultdict(set)
    for (tag,k,a),v in A.items():
        if (a=="SOL" and v[0]>=th_s) or (a!="SOL" and a in("USDC","USDT") and v[0]>=th_u) or (a=="WSOL" and v[0]>=th_s): s[tag].add(k)
    return s
print("tx lues",nt)
for label,(ts,tu) in {"sans seuil":(0,0),"0,01 SOL / 1 USD":(0.01,1),"0,1 SOL / 10 USD":(0.1,10)}.items():
    s=S(ts,tu)
    print("\n==",label,{k:len(v) for k,v in s.items()})
    for a,b in itertools.combinations(DEP,2):
        c=s[a]&s[b]
        if c: print(f"  {a} {b} : {len(c)}",sorted(c)[:40] if len(c)<=12 else f"{sorted(c)[:6]}...")
