"""G8 : analyse finale depuis a16_full. Par bloc : signataire, trésor, pool. Sens, quantité, marge au trésor en SOL, jetons gardés, pourboire, tiers. Part des achats. Sortie i35_a16c.txt."""
import gzip,json,collections,statistics as st,sys,duckdb
OUT="audits/2026-11-03/work_I/";W="/Volumes/VERBATIM HD/Dark-MAGA-Investigation/audits_work/I/";D="/Volumes/VERBATIM HD/Dark-MAGA-Investigation/data/trades.parquet"
sys.stdout=open(OUT+"i35_a16c.txt","w")
O4="4ToQp55myvfpeprgKuqGbDqyji9Ezm7CZg7QbcTpL33S"
TX=[json.loads(l) for l in gzip.open(W+"a16_full.jsonl.gz","rt")]
by=collections.defaultdict(list)
for t in TX:by[t["slot"]].append(t)
print("tx",len(TX),"blocs",len(by),collections.Counter(len(v) for v in by.values()),"échecs",sum(1 for t in TX if t["err"]))
print("programmes",collections.Counter(tuple(t["pg"]) for t in TX).most_common(4))
print("signature multiple",collections.Counter(len(t["sg"]) for t in TX))
print("pourboires connus : tx",sum(1 for t in TX if t["tip"]),"SOL",sum(t["tip"] for t in TX)/1e9)
R=[]
for sl,L in by.items():
    if len(L)!=2:continue
    a,b=sorted(L,key=lambda t:t["i"])
    S=a["sg"][0]
    def treas(k):return a[k].get(O4,0)+b[k].get(O4,0)
    dS=(a["dm"].get(S,0),b["dm"].get(S,0));dO=(a["dm"].get(O4,0),b["dm"].get(O4,0))
    act=S if abs(dS[0])>abs(dO[0]) else O4
    q1=a["dm"].get(act,0);q2=b["dm"].get(act,0)
    kind="achat_vente" if q1>0>q2 else "vente_achat" if q1<0<q2 else "autre"
    wsO=treas("ws")/1e9;solO=(a["sol"].get(O4,0)+b["sol"].get(O4,0))/1e9;dmO=treas("dm")/1e6
    solS=(a["sol"].get(S,0)+b["sol"].get(S,0))/1e9;dmS=(dS[0]+dS[1])/1e6;wsS=(a["ws"].get(S,0)+b["ws"].get(S,0))/1e9
    fee=(a["fee"]+b["fee"])/1e9
    R.append(dict(sl=sl,a=a["i"],b=b["i"],k=kind,act=act,S=S,same_signer=a["sg"][0]==b["sg"][0],q=abs(q1)/1e6,qe=abs(q1+q2)/max(abs(q1),abs(q2)),wsO=wsO,solO=solO,dmO=dmO,solS=solS,wsS=wsS,dmS=dmS,fee=fee,gap=b["i"]-a["i"],s1=a["s"],s2=b["s"],bt=a["bt"],tip=a["tip"]+b["tip"]))
c=collections.Counter(r["k"] for r in R);print("formes",c,"acteur",collections.Counter((r["k"],"trésor" if r["act"]==O4 else "signataire") for r in R))
print("écart d'index",collections.Counter(r["gap"] for r in R),"même signataire",sum(1 for r in R if r["same_signer"]))
for k in c:
    v=[r for r in R if r["k"]==k]
    print(k,"n",len(v),"quantité égale à 1 %",sum(1 for r in v if r["qe"]<0.01),"exacte",sum(1 for r in v if r["qe"]==0),"| trésor : WSOL net",round(sum(r["wsO"] for r in v),3),"SOL net",round(sum(r["solO"] for r in v),3),"DMAGA net M",round(sum(r["dmO"] for r in v)/1e6,3),"| signataire : SOL net",round(sum(r["solS"] for r in v),3),"WSOL",round(sum(r["wsS"] for r in v),3),"DMAGA net M",round(sum(r["dmS"] for r in v)/1e6,4),"| frais",round(sum(r["fee"] for r in v),3),"pourboires",round(sum(r["tip"] for r in v)/1e9,3))
    print("    marge trésor en WSOL+SOL : positives",sum(1 for r in v if r["wsO"]+r["solO"]>0),"médiane",round(st.median(r["wsO"]+r["solO"] for r in v),5),"; jetons gardés >0",sum(1 for r in v if r["dmO"]>0),"médiane",round(st.median(r["dmO"] for r in v),2))
print("trésor, DMAGA net total sur les blocs, M",round(sum(r["dmO"] for r in R)/1e6,4))
con=duckdb.connect(":memory:",config={"memory_limit":"800MB","threads":2,"temp_directory":W+"duck"})
con.execute("CREATE TABLE p(sl BIGINT,a INT,b INT,k VARCHAR)");con.executemany("INSERT INTO p VALUES (?,?,?,?)",[(r["sl"],r["a"],r["b"],r["k"]) for r in R])
q=con.execute(f"select p.k,t.slot,t.tx_index,t.owner,t.token_delta,t.sol_lamports,t.owner_wsol_delta,t.owner_native_delta,t.venue,p.a from p join read_parquet('{D}') t on t.slot=p.sl and t.tx_index>p.a and t.tx_index<p.b").fetchall()
cc=collections.Counter();v=collections.Counter();own=collections.Counter();bl=collections.Counter()
for r in q:
    d="achat" if r[4]>0 else "vente" if r[4]<0 else "nul";cc[(r[0],d)]+=1;v[(r[0],d)]+=abs(r[5] or 0)/1e9;own[r[3]]+=1;bl[(r[1],r[9])]+=1
print("tiers par forme et sens",cc);print("SOL tiers",{k:round(x,1) for k,x in v.items()})
print("blocs avec tiers",len(bl),"sur",len(R),"tiers par bloc",collections.Counter(bl.values()),"; tiers distincts",len(own),"; 10 premiers",round(sum(x for _,x in own.most_common(10))/sum(own.values()),3))
print("sans tiers, formes",collections.Counter(r["k"] for r in R if (r["sl"],r["a"]) not in bl))
sg={r["S"] for r in R};print("signataires",len(sg),"tiers aussi signataires",len(set(own)&sg),"tiers = trésor",own.get(O4,0))
print("10 premiers tiers",own.most_common(10))
ids=con.execute(f"select sum(case when token_delta>0 and sol_lamports<0 then -sol_lamports else 0 end)/1e9 from read_parquet('{D}')").fetchone()[0]
s=[(r["s1"],) for r in R]+[(r["s2"],) for r in R]
con.execute("CREATE TABLE s(sig VARCHAR)");con.executemany("INSERT INTO s VALUES (?)",s)
o=con.execute(f"select count(*),sum(case when token_delta>0 and sol_lamports<0 then -sol_lamports else 0 end)/1e9 from read_parquet('{D}') t join s on s.sig=t.signature").fetchone()
print("marché achats SOL",round(ids,2),"jambes dans trades",o,"part",round(100*o[1]/ids,3),"%")
import datetime as dt
print("période",dt.datetime.fromtimestamp(min(r["bt"] for r in R),dt.timezone.utc),dt.datetime.fromtimestamp(max(r["bt"] for r in R),dt.timezone.utc))
