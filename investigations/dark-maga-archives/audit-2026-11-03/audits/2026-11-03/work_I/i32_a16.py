"""G8 : forme de sandwich sur le brut (a16_tx.csv.gz, extrait de raw/full_*) + voisins du bloc dans trades.parquet. Rien de A ni G. Sortie i32_a16.txt, i32_third.csv."""
import csv,gzip,sys,collections,duckdb,statistics as st
sys.path.insert(0,"audits/2026-11-03/work_I")
OUT="audits/2026-11-03/work_I/";W="/Volumes/VERBATIM HD/Dark-MAGA-Investigation/audits_work/I/";D="/Volumes/VERBATIM HD/Dark-MAGA-Investigation/data/trades.parquet"
sys.stdout=open(OUT+"i32_a16.txt","w")
O4="4ToQp55myvfpeprgKuqGbDqyji9Ezm7CZg7QbcTpL33S"
rows=list(csv.DictReader(gzip.open(W+"a16_tx.csv.gz","rt")))
print("lignes",len(rows),"tx",len({r["sig"] for r in rows}),"err non vides",sum(1 for r in rows if r["err"] not in("","None")))
print("programmes",collections.Counter(r["progs"][:120] for r in rows).most_common(6))
# une tx -> propriétaire(s) qui bougent DMAGA
tx=collections.defaultdict(list)
for r in rows:tx[r["sig"]].append(r)
print("propriétaires DMAGA par tx",collections.Counter(len(v) for v in tx.values()))
AMM={"5Q544fKrFoe6tsEbD7S8EmxGTJYAKtTVhAW5Q5pge4j1"}
legs=[]
for s,v in tx.items():
    tr=[x for x in v if x["owner"] not in AMM and int(x["dmaga"])!=0]
    pool=[x["owner"][:8] for x in v if x["owner"] in AMM]
    if len(tr)!=1:legs.append(dict(s=s,bad=len(tr),own=[x["owner"][:8] for x in v]));continue
    x=tr[0];legs.append(dict(s=s,slot=int(x["slot"]),idx=int(x["idx"]),owner=x["owner"],signer=x["signer"],dm=int(x["dmaga"])/1e6,sol=int(x["sol"])/1e9,wsol=int(x["wsol"])/1e9,usdc=int(x["usdc"])/1e6,bt=int(x["bt"]),pool=pool))
bad=[l for l in legs if "bad" in l]
print("tx sans propriétaire unique hors AMM",len(bad),bad[:3])
good=[l for l in legs if "bad" not in l]
by=collections.defaultdict(list)
for l in good:by[l["slot"]].append(l)
print("blocs",len(by),"jambes par bloc",collections.Counter(len(v) for v in by.values()))
print("propriétaire = 4ToQp55m",sum(1 for l in good if l["owner"]==O4),"propriétaire = signataire",sum(1 for l in good if l["owner"]==l["signer"]),"signataires",len({l["signer"] for l in good}),"Raydium v4 dans la tx",sum(1 for l in good if l["pool"]))
cat=collections.Counter();marg=collections.defaultdict(list);gap=collections.Counter();same=0;A=[]
for sl,v in by.items():
    if len(v)!=2:cat["autre"]+=1;continue
    a,b=sorted(v,key=lambda l:l["idx"])
    gap[b["idx"]-a["idx"]]+=1
    k=("achat_vente" if a["dm"]>0>b["dm"] else "vente_achat" if a["dm"]<0<b["dm"] else "autre","4To" if a["owner"]==O4 else "sign")
    q=abs(abs(a["dm"])-abs(b["dm"]))/max(abs(a["dm"]),abs(b["dm"]));same+=q<0.01
    m=a["sol"]+b["sol"]+a["wsol"]+b["wsol"]
    cat[k]+=1;marg[k].append(m);A.append((sl,a["idx"],b["idx"],k,a["owner"],b["owner"],a["signer"],b["signer"],a["dm"],b["dm"],m,a["sol"]+a["wsol"],b["sol"]+b["wsol"]))
print("catégories",cat,"écart d'index",gap,"quantité égale à 1 %",same)
for k,v in marg.items():print(k,"marge SOL",round(sum(v),3),"positives",sum(1 for x in v if x>0),"sur",len(v),"médiane",round(st.median(v),5))
print("même signataire entre les 2 jambes",sum(1 for x in A if x[6]==x[7]),"sur",len(A),"; même propriétaire",sum(1 for x in A if x[4]==x[5]))
con=duckdb.connect(":memory:",config={"memory_limit":"800MB","threads":2,"temp_directory":W+"duck"})
con.execute("SET TimeZone='UTC'")
con.execute("CREATE TABLE p(sl BIGINT,a INT,b INT,k VARCHAR,own VARCHAR)")
con.executemany("INSERT INTO p VALUES (?,?,?,?,?)",[(x[0],x[1],x[2],x[3][0]+"|"+x[3][1],x[4]) for x in A])
cols=[c[0] for c in con.execute(f"describe select * from read_parquet('{D}')").fetchall()]
print("colonnes trades",cols)
q=con.execute(f"""select p.k,t.slot,t.tx_index,t.signature,t.owner,t.fee_payer,t.token_delta,t.sol_lamports,t.venue,p.a,p.b from p join read_parquet('{D}') t on t.slot=p.sl and t.tx_index>p.a and t.tx_index<p.b""").fetchall()
print("lignes tierces dans trades.parquet",len(q))
w=csv.writer(open(OUT+"i32_third.csv","w"));w.writerow("k slot idx sig owner payer token_delta sol venue".split())
c=collections.Counter();tb=collections.Counter();own=collections.Counter();ven=collections.Counter();byk=collections.defaultdict(float);bl=collections.defaultdict(int);signers={l["signer"] for l in good}
for r in q:
    w.writerow(r[:9]);dirn="achat" if r[6]>0 else "vente" if r[6]<0 else "nul"
    c[(r[0],dirn)]+=1;own[r[4]]+=1;ven[r[8]]+=1;bl[(r[1],r[9])]+=1
    byk[(r[0],dirn)]+=abs(r[7] or 0)/1e9
print("jambes tierces par catégorie et sens",c);print("SOL par catégorie et sens",{k:round(v,1) for k,v in byk.items()})
print("blocs avec au moins un tiers",len(bl),"; nombre de tiers par bloc",collections.Counter(bl.values()))
print("tiers distincts",len(own),"top",own.most_common(8));print("venues des tiers",ven.most_common(6))
print("tiers qui sont aussi signataires du service",len(set(own)&signers),"; tiers = 4ToQp55m",own.get(O4,0))
top=sum(v for _,v in own.most_common(10));print("part des 10 premiers tiers",round(top/sum(own.values()),3))
# Volume
tot=con.execute(f"select count(*),sum(case when token_delta>0 and sol_lamports<0 then -sol_lamports else 0 end)/1e9,sum(case when token_delta>0 then 1 else 0 end) from read_parquet('{D}')").fetchone()
print("marché : lignes",tot[0],"achats SOL",round(tot[1],1),"achats n",tot[2])
own_buy=-sum(min(0,l["sol"]+l["wsol"]) for l in good if l["dm"]>0)
print("achats des jambes SOL",round(own_buy,2),"part",round(100*own_buy/tot[1],3),"% ; par trades.parquet :",end=" ")
con.execute("CREATE TABLE s(sig VARCHAR)");con.executemany("INSERT INTO s VALUES (?)",[(l["s"],) for l in good])
v=con.execute(f"select sum(case when token_delta>0 and sol_lamports<0 then -sol_lamports else 0 end)/1e9,count(*) from read_parquet('{D}') t join s on s.sig=t.signature").fetchone();print(v,"part",round(100*v[0]/tot[1],3))
print("net DMAGA des jambes, M",round(sum(l["dm"] for l in good)/1e6,4),"marge totale",round(sum(sum(v) for v in marg.values()),2))
print("premier et dernier bloc",min(l["bt"] for l in good),max(l["bt"] for l in good))
print("USDC dans les jambes",round(sum(abs(l["usdc"]) for l in good),2))
