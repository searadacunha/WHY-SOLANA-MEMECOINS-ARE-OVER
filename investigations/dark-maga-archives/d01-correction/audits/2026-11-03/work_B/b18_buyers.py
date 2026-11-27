"""Phase 2 : indépendance des comparateurs : wallets communs entre tokens sur [S−24 h, S). Sortie : b18_buyers.txt.
Rang des tokens : 212 de la population principale. Traitement DuckDB, mémoire limitée."""
from pathlib import Path
import duckdb, pandas as pd
HERE = Path(__file__).parent
W = "/Volumes/VERBATIM HD/Dark-MAGA-Investigation/audits_work/B"
L = []
def P(*a):
    s = " ".join(str(x) for x in a); L.append(s); print(s)
con = duckdb.connect()
con.execute(f"SET memory_limit='800MB'; SET threads=2; SET TimeZone='UTC'; SET temp_directory='{W}/duck_tmp'")
DM = "CRSwXnfF21yHDXdYBVWwCwQ5Ni2A4QuK3qGYis5k7x7k"
pop = pd.read_csv(HERE / "blind_metrics.csv"); pop = pop[pop.retenu == 1][["pool"]]
con.register("pop", pop)
con.execute(f"CREATE TEMP TABLE b AS SELECT column0 AS pool, column1 AS w, column2 AS sol FROM read_csv('{W}/buyers.csv', header=false, columns={{'column0':'VARCHAR','column1':'VARCHAR','column2':'DOUBLE'}}) WHERE column0 IN (SELECT pool FROM pop)")
P("lignes", con.execute("select count(*), count(distinct pool), count(distinct w) from b").fetchone())
con.execute("CREATE TEMP TABLE wc AS SELECT w, count(*) n_tok, sum(sol) s FROM b GROUP BY w")
P("wallets présents sur k tokens :", con.execute("select case when n_tok=1 then '1' when n_tok<=4 then '2-4' when n_tok<=19 then '5-19' else '20+' end c, count(*), round(sum(s)) from wc group by 1 order by 1").fetchall())
r = con.execute("""select b.pool, sum(sol) tot, sum(case when n_tok>=2 then sol else 0 end)/sum(sol) p2, sum(case when n_tok>=5 then sol else 0 end)/sum(sol) p5, sum(case when n_tok>=20 then sol else 0 end)/sum(sol) p20
                   from b join wc using(w) group by 1""").fetchdf()
P("part du SOL acheté sur 24 h par des wallets vus sur >=2, >=5, >=20 tokens : médianes", r[["p2", "p5", "p20"]].median().round(3).to_dict())
P("DMAGA :", r[r.pool == DM][["p2", "p5", "p20"]].round(3).to_dict("records"))
top = con.execute("""with t as (select *, row_number() over (partition by pool order by sol desc) rk from b) select w, count(*) n from t where rk<=5 group by 1 order by 2 desc""").fetchdf()
P("wallets du top 5 présents dans le top 5 de plusieurs tokens :", int((top.n >= 2).sum()), "sur", len(top), "; max", int(top.n.max()))
d5 = con.execute(f"""with t as (select *, row_number() over (partition by pool order by sol desc) rk from b), a as (select w from t where pool='{DM}' and rk<=20)
   select count(*) from wc join a using(w) where n_tok>=2""").fetchone()[0]
P("top 20 DMAGA vus sur au moins un autre token de la population :", d5)
# paires de tokens partageant le plus de SOL
pr = con.execute("""with x as (select a.pool p1, b.pool p2, count(*) n from b a join b using(w) where a.pool<b.pool and w in (select w from wc where n_tok<=19) group by 1,2)
  select n, count(*) c from x group by 1 order by 1 desc limit 8""").fetchall()
P("paires de tokens : (nombre de wallets communs hors bots >=20 tokens, nombre de paires), plus hautes :", pr)
(HERE / "b18_buyers.txt").write_text("\n".join(L) + "\n")
