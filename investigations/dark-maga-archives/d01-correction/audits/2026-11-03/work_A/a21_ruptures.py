#!/usr/bin/env python3
"""Auditeur A. Ruptures de chaîne par compte de jetons : mouvements DMAGA invisibles dans le brut collecté, et ce qu'ils changent aux étiquettes de complétude, au top 100, au groupe."""
import csv, json, os, re, sys
import duckdb
A = "/Volumes/VERBATIM HD/Dark-MAGA-Investigation/audits_work/A"
B = "/Volumes/VERBATIM HD/Dark-MAGA-Investigation/data"
F = "/Volumes/VERBATIM HD/Dark-MAGA-Investigation/raw/flows"
ROOT = "REDACTED_HOME/Projects/Dark-MAGA-Investigation"
sys.path.insert(0, ROOT)
from dmaga.venues import load as lv
con = duckdb.connect(":memory:", config={"memory_limit": "450MB", "threads": 2, "temp_directory": A + "/duck21", "preserve_insertion_order": False})
con.execute("SET TimeZone='UTC'")
def show(n, s, *a):
    print(n, con.execute(s, *a).fetchall(), flush=True)
OA = f"read_parquet('{A}/a13_oa.parquet')"
W = f"read_parquet('{B}/wallets.parquet')"
traced = [d for d in os.listdir(F) if not d.startswith("._")]
con.execute("CREATE TEMP TABLE tr(a VARCHAR)")
con.executemany("INSERT INTO tr VALUES (?)", [[a] for a in traced])
con.execute("CREATE TEMP TABLE ven(a VARCHAR)")
con.executemany("INSERT INTO ven VALUES (?)", [[a] for a in lv()])
con.execute(f"""COPY (SELECT account, owner, signature, slot, tx_index, t, pp, pre, pre-pp d FROM {OA} WHERE pp IS NOT NULL AND pp<>pre) TO '{A}/a21_r.parquet' (FORMAT parquet)""")
R = f"read_parquet('{A}/a21_r.parquet')"
show("ruptures : entrées invisibles (M), sorties invisibles (M)", f"SELECT count(*), round(sum(CASE WHEN d>0 THEN d ELSE 0 END)/1e12,2), round(sum(CASE WHEN d<0 THEN -d ELSE 0 END)/1e12,2) FROM {R}")
show("ruptures par année", f"SELECT t//31536000+1970, count(*), round(sum(abs(d))/1e12,1) FROM {R} GROUP BY 1 ORDER BY 1")
show("avant S (S = 21/07 19:00)", f"SELECT account, owner, t, d/1e12, signature FROM {R} WHERE t<1721588400 ORDER BY t")
show("24 h suivant la borne haute", f"SELECT count(*), round(sum(abs(d))/1e12,2), count(DISTINCT owner) FROM {R} WHERE t>=1721590213 AND t<1721676613")
show("par statut : tracé dans raw/flows ou non", f"SELECT owner IN (SELECT a FROM tr) tr, count(*), count(DISTINCT owner), round(sum(abs(d))/1e12,1) FROM {R} GROUP BY 1")
show("venues dans les ruptures", f"SELECT count(*), round(sum(abs(d))/1e12,3) FROM {R} WHERE owner IN (SELECT a FROM ven)")
con.execute(f"""CREATE TEMP TABLE po AS SELECT owner, count(*) n, sum(CASE WHEN d>0 THEN d ELSE 0 END)/1e12 inM, sum(CASE WHEN d<0 THEN -d ELSE 0 END)/1e12 outM FROM {R} GROUP BY 1""")
show("par étiquette de complétude (wallets.parquet) : wallets, entrées invisibles M, réalisé SOL", f"SELECT w.completeness, count(*), round(sum(p.inM),1), round(sum(p.outM),1), round(sum(w.realized_sol)) FROM po p JOIN {W} w ON w.owner=p.owner GROUP BY 1 ORDER BY 3 DESC")
show("  entrées invisibles et wallet non tracé, label « complet »", f"""SELECT w.owner, p.n, round(p.inM,3), round(p.outM,3), round(w.realized_sol,1), round(w.bought_qty/1e6,3), round(w.sold_qty/1e6,3), w.completeness FROM po p JOIN {W} w ON w.owner=p.owner WHERE w.completeness LIKE 'complet%' AND p.inM>0.01 ORDER BY w.realized_sol DESC LIMIT 15""")
# top 100
txt = open(ROOT + "/reports/TOP_TRADERS.md").read()
sec = txt.split("## 100 plus gros réalisés")[1].split("\n## ")[0]
top = [m[1] for m in re.findall(r"\| (\d+) \| `(\w+)` \|", sec)]
con.execute("CREATE TEMP TABLE t100(a VARCHAR, r INT)")
con.executemany("INSERT INTO t100 VALUES (?,?)", [[a, i + 1] for i, a in enumerate(top)])
show("top 100 avec ruptures : rang, wallet, n, entrées M, sorties M", "SELECT t.r, p.owner, p.n, round(p.inM,3), round(p.outM,3) FROM po p JOIN t100 t ON t.a=p.owner ORDER BY t.r")
g = json.load(open(ROOT + "/data/prevent_groups.json"))[0]
con.execute("CREATE TEMP TABLE g0(a VARCHAR)")
con.executemany("INSERT INTO g0 VALUES (?)", [[m] for m in g["members"]])
show("groupe de 33 avec ruptures", f"SELECT owner, n, round(inM,3), round(outM,3) FROM po WHERE owner IN (SELECT a FROM g0) ORDER BY inM DESC")
show("  ruptures du groupe, dates et montants", f"SELECT owner, t, d/1e12, signature FROM {R} WHERE owner IN (SELECT a FROM g0) ORDER BY t LIMIT 30")
# les 5 plus gros comptes rompus sont-ils couverts par les flux dmaga_all ?
show("top 15 propriétaires", f"SELECT p.owner, p.n, round(p.inM,1), round(p.outM,1), p.owner IN (SELECT a FROM tr), round(coalesce(w.realized_sol,0)), coalesce(w.completeness,'absent') FROM po p LEFT JOIN {W} w ON w.owner=p.owner ORDER BY greatest(p.inM,p.outM) DESC LIMIT 15")
# réconciliation de l'offre : somme des derniers soldes connus
con.execute(f"""CREATE TEMP TABLE last AS SELECT account, arg_max(post,(slot,tx_index)) p, arg_max(owner,(slot,tx_index)) o FROM {OA} GROUP BY 1""")
show("somme des derniers soldes vus (M) ; par nature", "SELECT round(sum(p)/1e12,2), round(sum(CASE WHEN o IN (SELECT a FROM ven) OR o='5Q544fKrFoe6tsEbD7S8EmxGTJYAKtTVhAW5Q5pge4j1' OR o='87g44hEXP7R8ZxoAJtz941tsVftpEXC1LqAFTf2ZHtkH' THEN p ELSE 0 END)/1e12,2) FROM last")
# transferts vus par a02 contre token_edges gtba : combien de mouvements invisibles les flux expliquent-ils ?
con.execute(f"CREATE TEMP TABLE ge AS SELECT signature, src, dst, CAST(round(qty*1e6) AS BIGINT) q, block_time FROM read_parquet('{B}/token_edges.parquet') WHERE how='gtba'")
show("token_edges gtba : lignes, dont signature absente de a02", f"SELECT count(*), sum((signature NOT IN (SELECT signature FROM read_parquet('{A}/a15_tx.parquet')))::int), round(sum(CASE WHEN signature NOT IN (SELECT signature FROM read_parquet('{A}/a15_tx.parquet')) THEN q ELSE 0 END)/1e12,1) FROM ge")
