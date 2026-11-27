"""G6 : jonction manquée ? Toutes les sorties de raw/flows (1 219 wallets, seuil de la collecte 0,1 SOL ou 100 USD) + expéditeurs des 8 dépôts. Grappes indépendantes de la classification de G sauf listes citées. Arêtes directes entre grappes, destinations partagées entre grappes hors étiquettes. DuckDB borné. Sorties i25_junction.txt, i25_shared.csv."""
import csv,json,sys,duckdb,collections
sys.path.insert(0,"audits/2026-11-03/work_I")
from dmaga.labels import label
OUT="audits/2026-11-03/work_I/";W="/Volumes/VERBATIM HD/Dark-MAGA-Investigation/audits_work/I/"
sys.stdout=open(OUT+"i25_junction.txt","w")
P1=[list(r.values())[0] for r in csv.DictReader(open("audits/2026-11-03/work_G/g40_p1_wallets.csv"))]
g33=json.load(open("data/prevent_groups.json"))[0]["members"]
SALVE=["G41vRrsHShLEvwMj58ruhqJycGfAtWXxtLD56uFExL8E","C73Yv9iHmTaf8SU2XFnGLt7QXUDqbeWNtUYza9WJhkae","AtZjv3DuV9cLn3Jxm72TMSdTN4aM6CrBaGyxUC4c2wDk","EGtyQEgMKGKXjppDqj9sYy97e9m7nvu1US4SfFXNakMy"]
S=collections.defaultdict(set)
for r in csv.DictReader(open(OUT+"i24_dep_senders.csv")):
    v=float(r["somme"])
    if (r["asset"] in("SOL","WSOL") and v>=0.01) or (r["asset"] in("USDC","USDT") and v>=1): S[r["depot"]].add(r["sender"])
C={}
def put(ws,c):
    for w in ws:
        if w not in C: C[w]=c
put(P1,"P1");put(S["9W9b"]-set(SALVE),"P1");put(S["Caw4"]-{"59L2oxymiQQ9Hvhh92nt8Y7nDYjsauFkdb3SybdnsG6h"},"P1_C")
put(g33,"P2");put(SALVE,"P2")
put(S["AQVg"]-{"59L2oxymiQQ9Hvhh92nt8Y7nDYjsauFkdb3SybdnsG6h"},"AQVg");put(S["By6D"],"By6D");put(S["H9Xe"],"H9Xe")
for x in ("ASTyfSima4LLAdDgoFGkgqoKowG1LZFDr9fAQrg7iaJZ","AbLzAvob4vAZrXJjMACeYsEP1vef1Lm8gkCgwy9x3tg3"): S["8N4A"].discard(x);S["9kqT"].discard(x)
put(S["8N4A"]|S["42MS"]|S["9kqT"],"GXb")
put(["H3QsBrrivimFJmSpTXuvig2n1Bh7JuYxrriRSEszT6cc"],"H3")
print("grappes",collections.Counter(C.values()))
DEPS={"9W9b3zgHH9mCEHDhsdbnbEPHStm9vvXS4aia4DWHBxpL","Caw4RrwkmxqtbLSFzgSs6id3XiFxWQxs2t1mrn5a3mME","AQVgyg8P5Yh5YcAqAMQRRGzDegy1R58gN4Qh87QsJAF1","By6Dao4QMNeBxmdUrqsoQA8dCGbHz7xWj57CdHV5M47r","H9XezqfdXuv4ZCHAAZ92oMLSSAPB6Dgm4ZSrRythCbPi","8N4AvP9j5BditSQMk2WrTNxthhgpncGVzLKrYP4xdEqx","42MSVeV4YbESE7mNW7DfQrfd8E4RG6njxXZLAWTmXemv","9kqTVnRUkVTFD7na9BTWcoG9piL4XpVTtS9kqVCV56tV"}
con=duckdb.connect(":memory:",config={"memory_limit":"800MB","threads":2,"temp_directory":W+"duck"})
con.execute("SET TimeZone='UTC'")
con.execute("CREATE TABLE c(w VARCHAR PRIMARY KEY,g VARCHAR)");con.executemany("INSERT INTO c VALUES (?,?)",list(C.items()))
con.execute(f"CREATE TABLE f AS SELECT src,dst,asset,amount::DOUBLE amt,bt::BIGINT bt FROM read_csv_auto('{W}flows_out.csv.gz',header=true,all_varchar=true) WHERE dst IS NOT NULL AND asset<>'DMAGA' UNION ALL BY NAME SELECT src,dst,asset,amount::DOUBLE amt,bt::BIGINT bt FROM read_csv_auto('{W}net_out.csv.gz',header=true,all_varchar=true) WHERE dst IS NOT NULL AND asset<>'DMAGA'")
print("lignes",con.execute("select count(*),count(distinct src),count(distinct dst) from f").fetchone())
con.execute("CREATE TEMP VIEW p AS SELECT f.*,c.g gs,d.g gd FROM f JOIN c ON c.w=f.src LEFT JOIN c d ON d.w=f.dst")
print("couverture : expéditeurs de grappes avec au moins une sortie lue",con.execute("select gs,count(distinct src) from p group by 1 order by 1").fetchall())
print("\nARÊTES DIRECTES ENTRE GRAPPES (hors P1<->P1_C)")
for r in con.execute("""select gs,gd,src,dst,asset,round(sum(amt),3),count(*),strftime(to_timestamp(min(bt)),'%Y-%m-%d %H:%M:%S'),strftime(to_timestamp(max(bt)),'%Y-%m-%d %H:%M:%S') from p where gd is not null and gs<>gd and not (gs in('P1','P1_C') and gd in('P1','P1_C')) group by all order by 1,2,6 desc""").fetchall():
    print(" ",r[0],"->",r[1],r[2],r[3],r[4],r[5],"n",r[6],str(r[7])[:19],str(r[8])[:19])
print("\nDESTINATIONS PARTAGÉES ENTRE AU MOINS 2 GRAPPES (P1 et P1_C comptent pour une)")
Q=con.execute("""with x as (select dst,src,case when gs in('P1','P1_C') then 'P1' else gs end gs,asset,amt,bt from p where gd is null)
 select dst,count(distinct gs) ng,string_agg(distinct gs,',') gs,count(distinct src) ns,round(sum(case when asset='SOL' then amt else amt/170 end),2) soleq,strftime(to_timestamp(min(bt)),'%Y-%m-%d %H:%M:%S'),strftime(to_timestamp(max(bt)),'%Y-%m-%d %H:%M:%S'),
   round(min(s),2) from (select dst,gs,src,asset,amt,bt,sum(case when asset='SOL' then amt else amt/170 end) over(partition by dst,gs) s from x) group by dst having count(distinct gs)>=2 order by soleq desc""").fetchall()
tot={r[0]:r[1] for r in con.execute("select dst,count(distinct src) from f group by 1").fetchall()}
w=csv.writer(open(OUT+"i25_shared.csv","w"));w.writerow("dst label ngrappes grappes nsrc_grappes nsrc_tous soleq premier dernier mini_par_grappe".split())
n=0
for r in Q:
    lab=label(r[0])
    w.writerow([r[0],lab,r[1],r[2],r[3],tot.get(r[0],0),r[4],str(r[5])[:19],str(r[6])[:19],r[7]])
    n+=1
print("candidates",n)
rows=list(csv.DictReader(open(OUT+"i25_shared.csv")))
sel=[r for r in rows if not r["label"] or r["label"] in("None","")]
print("sans étiquette",len(sel))
for r in sel[:60]:
    print(" ",r["dst"],r["grappes"],"ns",r["nsrc_grappes"],"tous",r["nsrc_tous"],"soleq",r["soleq"],"min",r["mini_par_grappe"],r["premier"],r["dernier"])
