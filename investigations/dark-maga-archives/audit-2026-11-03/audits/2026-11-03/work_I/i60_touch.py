"""« Touche DMAGA » refait : expéditeurs des dépôts, 3 sources indépendantes de d01_own : trades.parquet (échanges), raw/flows/<w>/dmaga_all, net brut. Puis dates : première touche contre premier versement. Détail H9Xe et 9PrmF8. Sorties i60_touch.txt, i60_touch.csv."""
import csv,sys,collections,duckdb,gzip,json,os,datetime as dt
sys.path.insert(0,"audits/2026-11-03/work_I")
from i_lib import *
OUT="audits/2026-11-03/work_I/";W=R+"/audits_work/I/"
sys.stdout=open(OUT+"i60_touch.txt","w")
S=collections.defaultdict(dict)
for r in csv.DictReader(open(OUT+"i24_dep_senders.csv")):
    v=float(r["somme"]);a=r["asset"]
    if (a in("SOL","WSOL") and v>=0.01) or (a in("USDC","USDT") and v>=1):
        d=S[r["depot"]].setdefault(r["sender"],dict(sol=0,usd=0,first=r["first"],last=r["last"]))
        d["sol" if a in("SOL","WSOL") else "usd"]+=v;d["first"]=min(d["first"],r["first"]);d["last"]=max(d["last"],r["last"])
allw=sorted({w for d in S.values() for w in d})
con=duckdb.connect(":memory:",config={"memory_limit":"800MB","threads":2,"temp_directory":W+"duck"})
con.execute("CREATE TABLE w(a VARCHAR)");con.executemany("INSERT INTO w VALUES (?)",[(x,) for x in allw])
T={r[0]:(r[1],r[2],r[3]) for r in con.execute("select owner,count(*),min(block_time),sum(token_delta)/1e6 from read_parquet('/Volumes/VERBATIM HD/Dark-MAGA-Investigation/data/trades.parquet') t join w on w.a=t.owner group by 1").fetchall()}
FL={};NT={}
for x in allw:
    p=f"{R}/raw/flows/{x}/dmaga_all.json.gz"
    if os.path.exists(p):
        rows=json.load(gzip.open(p,"rt"))["rows"]
        FL[x]=(len(rows),min([r["blockTime"] for r in rows] or [0]))
    if net_paths(x):
        n=0;f=None
        for t in iter_tx(x):
            td,dec=tok_delta(t)
            if (x,DMAGA) in td:
                n+=1;f=min(f or t["blockTime"],t["blockTime"])
        NT[x]=(n,f)
iso=lambda t:dt.datetime.fromtimestamp(t,dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S") if t else ""
w=csv.writer(open(OUT+"i60_touch.csv","w"));w.writerow("depot sender sol usd first last trades flows net touche first_touch".split())
SKIP={"59L2oxymiQQ9Hvhh92nt8Y7nDYjsauFkdb3SybdnsG6h"}
for dep,d in S.items():
    tc=0;unk=0;before=0;rows=[]
    for x,v in sorted(d.items()):
        t=T.get(x,(0,None,0));f=FL.get(x);n=NT.get(x)
        touch=bool(t[0] or (f and f[0]) or (n and n[0]))
        ft=min([y for y in [t[1],f[1] if f and f[0] else None,n[1] if n and n[0] else None] if y] or [0])
        known=x in FL or x in NT
        tc+=touch;unk+=(not touch and not known and not t[0])
        if touch and ft and iso(ft)<=v["first"]:before+=1
        w.writerow([dep,x,round(v["sol"],4),round(v["usd"],2),v["first"],v["last"],t[0],(f or (0,))[0],(n or (0,))[0],int(touch),iso(ft)])
        rows.append((x,round(v["sol"],2),round(v["usd"],2),v["first"][:10],v["last"][:10],t[0],(f or (0,))[0],(n or (0,))[0],touch,iso(ft)[:10]))
    print(dep,"expéditeurs",len(d),"touchent",tc,"sans aucune source lue",unk,"première touche avant le premier versement",before)
    if dep in("H9Xe","AQVg","By6D"):
        for r in sorted(rows,key=lambda r:-r[1]):print("   ",r)
print("\nH9Xe : DMAGA reçus par les expéditeurs et d'où (net + flows dmaga_all)")
H=S["H9Xe"]
for x in sorted(H,key=lambda k:-H[k]["sol"]):
    p=f"{R}/raw/flows/{x}/dmaga_all.json.gz";c=collections.Counter();ts=[]
    if os.path.exists(p):
        for r in json.load(gzip.open(p,"rt"))["rows"]:
            if r.get("toUserAccount")==x:
                c[r.get("fromUserAccount")]+=int(r.get("tokenAmount") or r.get("amount") or 0)/1e6/1e6;ts.append(r["blockTime"])
    print(" ",x,round(H[x]["sol"],2),H[x]["first"][:10],H[x]["last"][:10],"reçoit M",[(a[:8],round(v,2)) for a,v in c.most_common(4)],iso(min(ts))[:10] if ts else "")
print("\nrelations directes entre expéditeurs de H9Xe (net_out, flows_out)")
Hs=set(H)
con.execute(f"CREATE TABLE f AS SELECT DISTINCT src,dst,asset,amount::DOUBLE amt,bt::BIGINT bt,sig FROM read_csv_auto('{W}net_out.csv.gz',header=true,all_varchar=true) WHERE dst IS NOT NULL UNION SELECT DISTINCT src,dst,asset,amount::DOUBLE amt,bt::BIGINT bt,sig FROM read_csv_auto('{W}flows_out.csv.gz',header=true,all_varchar=true) WHERE dst IS NOT NULL")
con.execute("CREATE TABLE h(a VARCHAR)");con.executemany("INSERT INTO h VALUES (?)",[(x,) for x in Hs])
for r in con.execute("select src,dst,asset,round(sum(amt),3),count(*),strftime(to_timestamp(min(bt)),'%Y-%m-%d'),strftime(to_timestamp(max(bt)),'%Y-%m-%d') from f where src in (select a from h) and dst in (select a from h) group by 1,2,3 order by 4 desc limit 30").fetchall():print(" ",r)
# Même mesure pour 9W9b : densité des arêtes directes entre expéditeurs
for dep in("9W9b","Caw4","H9Xe","8N4A"):
    x=set(S[dep]);con.execute("DROP TABLE IF EXISTS h");con.execute("CREATE TABLE h(a VARCHAR)");con.executemany("INSERT INTO h VALUES (?)",[(y,) for y in x])
    e=con.execute("select count(distinct least(src,dst)||greatest(src,dst)) from f where src in (select a from h) and dst in (select a from h) and asset<>'DMAGA'").fetchone()[0]
    print(dep,"expéditeurs",len(x),"paires reliées (SOL/USD)",e,"densité",round(2*e/max(1,len(x)*(len(x)-1)),3))
