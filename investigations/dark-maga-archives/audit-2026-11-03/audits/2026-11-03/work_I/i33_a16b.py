"""G8 suite : bloc complet par tx, pour les 2 formes, deltas de tous les propriétaires. Puis recalcul : par bloc, jambes du service, sens du « trésor et signataire » pris ensemble. Sortie i33_a16b.txt, i33_blocks.csv."""
import csv,gzip,sys,collections,duckdb,statistics as st
OUT="audits/2026-11-03/work_I/";W="/Volumes/VERBATIM HD/Dark-MAGA-Investigation/audits_work/I/";D="/Volumes/VERBATIM HD/Dark-MAGA-Investigation/data/trades.parquet"
sys.stdout=open(OUT+"i33_a16b.txt","w")
O4="4ToQp55myvfpeprgKuqGbDqyji9Ezm7CZg7QbcTpL33S";AMM="5Q544fKrFoe6tsEbD7S8EmxGTJYAKtTVhAW5Q5pge4j1"
rows=list(csv.DictReader(gzip.open(W+"a16_tx.csv.gz","rt")))
tx=collections.defaultdict(list)
for r in rows:tx[r["sig"]].append(r)
by=collections.defaultdict(list)
for s,v in tx.items():by[int(v[0]["slot"])].append((int(v[0]["idx"]),s,v))
print("blocs",len(by),"tx par bloc",collections.Counter(len(v) for v in by.values()))
shown=collections.Counter()
A=[]
for sl,L in sorted(by.items()):
    L.sort(key=lambda x:x[0])
    def fmt(v):return [(x["owner"][:8],round(int(x["dmaga"])/1e6,2),round(int(x["sol"])/1e9,4),round(int(x["wsol"])/1e9,4)) for x in v]
    legs=[]
    for i,s,v in L:
        # sens côté non-pool : somme DMAGA des propriétaires hors AMM
        pool=sum(int(x["dmaga"]) for x in v if x["owner"]==AMM)/1e6
        solo=sum(int(x["sol"])+int(x["wsol"]) for x in v if x["owner"]!=AMM)/1e9
        legs.append(dict(i=i,s=s,pool=pool,dm=-pool,val=solo,owners=[x["owner"] for x in v if x["owner"]!=AMM],signer=v[0]["signer"]))
    if len(legs)!=2:continue
    a,b=legs
    k="achat_vente" if a["dm"]>0>b["dm"] else "vente_achat" if a["dm"]<0<b["dm"] else "autre"
    A.append((sl,a["i"],b["i"],k,a["signer"],b["signer"],abs(a["dm"]),abs(b["dm"]),a["val"],b["val"],a["val"]+b["val"],bool(set(a["owners"])&{O4}),bool(set(b["owners"])&{O4}),a["s"],b["s"]))
    if shown[k]<2:
        shown[k]+=1
        print(k,"slot",sl);print("  ",a["i"],a["s"][:14],a["signer"][:8],fmt(L[0][2]));print("  ",b["i"],b["s"][:14],b["signer"][:8],fmt(L[1][2]))
w=csv.writer(open(OUT+"i33_blocks.csv","w"));w.writerow("slot a b kind sign_a sign_b q_a q_b val_a val_b marge o4_a o4_b sig_a sig_b".split());w.writerows(A)
c=collections.Counter(x[3] for x in A);print("formes",c)
gap=collections.Counter((x[3],x[2]-x[1]) for x in A);print("écart d'index",gap)
for k in c:
    v=[x for x in A if x[3]==k]
    print(k,"quantité égale à 1 %",sum(1 for x in v if abs(x[6]-x[7])/max(x[6],x[7])<0.01),"marge SOL (hors pool, toutes clés)",round(sum(x[10] for x in v),3),"positives",sum(1 for x in v if x[10]>0),"médiane",round(st.median(x[10] for x in v),5),"même signataire",sum(1 for x in v if x[4]==x[5]))
con=duckdb.connect(":memory:",config={"memory_limit":"800MB","threads":2,"temp_directory":W+"duck"})
con.execute("CREATE TABLE p(sl BIGINT,a INT,b INT,k VARCHAR)");con.executemany("INSERT INTO p VALUES (?,?,?,?)",[(x[0],x[1],x[2],x[3]) for x in A])
q=con.execute(f"""select p.k,t.slot,t.tx_index,t.signature,t.owner,t.fee_payer,t.token_delta,t.sol_lamports,t.venue,p.a from p join read_parquet('{D}') t on t.slot=p.sl and t.tx_index>p.a and t.tx_index<p.b""").fetchall()
c=collections.Counter();v=collections.Counter();own=collections.Counter();bl=collections.Counter();ven=collections.Counter()
for r in q:
    d="achat" if r[6]>0 else "vente" if r[6]<0 else "nul";c[(r[0],d)]+=1;v[(r[0],d)]+=abs(r[7] or 0)/1e9;own[r[4]]+=1;bl[(r[1],r[9])]+=1;ven[r[8]]+=1
print("tiers par forme et sens",c);print("SOL",{k:round(x,1) for k,x in v.items()})
print("blocs avec tiers",len(bl),"sur",len(A),"tiers par bloc",collections.Counter(bl.values()),"; tiers distincts",len(own),"; top 10 part",round(sum(x for _,x in own.most_common(10))/sum(own.values()),3))
sg={x[4] for x in A}|{x[5] for x in A};print("signataires",len(sg),"tiers aussi signataires",len(set(own)&sg),"tiers = trésor",own.get(O4,0),"venues",ven.most_common(4))
ids=con.execute(f"select count(*),sum(case when token_delta>0 and sol_lamports<0 then -sol_lamports else 0 end)/1e9 from read_parquet('{D}')").fetchone()
con.execute("CREATE TABLE s(sig VARCHAR)");con.executemany("INSERT INTO s VALUES (?)",[(x[13],) for x in A]+[(x[14],) for x in A])
o=con.execute(f"select count(*),sum(case when token_delta>0 and sol_lamports<0 then -sol_lamports else 0 end)/1e9,sum(case when token_delta>0 then 1 else 0 end),sum(case when token_delta<0 then 1 else 0 end) from read_parquet('{D}') t join s on s.sig=t.signature").fetchone()
print("marché achats SOL",round(ids[1],2),"; jambes dans trades",o,"part",round(100*o[1]/ids[1],3))
# achats tels qu'un trader normal les lit : jambe où le pool perd du DMAGA
b=sum(-(x[8]) for x in A if x[3]=="achat_vente")+sum(-(x[9]) for x in A if x[3]=="vente_achat");print("achats calculés du pool (val<0) SOL",round(b,2),"part",round(100*b/ids[1],3))
