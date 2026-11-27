#!/usr/bin/env python3
"""Auditeur A. Assertions testables du groupe sur le brut : détention à la borne basse (soldes réels des comptes de jetons), flottant, ventes 24 h, gestes, premier achat, activité entre visuel et bascule."""
import json, sys
import duckdb
A = "/Volumes/VERBATIM HD/Dark-MAGA-Investigation/audits_work/A"
B = "/Volumes/VERBATIM HD/Dark-MAGA-Investigation/data"
ROOT = "REDACTED_HOME/Projects/Dark-MAGA-Investigation"
sys.path.insert(0, ROOT)
from dmaga.venues import load as lv
con = duckdb.connect(":memory:", config={"memory_limit": "450MB", "threads": 2, "temp_directory": A + "/duck23", "preserve_insertion_order": False})
con.execute("SET TimeZone='UTC'")
def show(n, s, *a):
    print(n, con.execute(s, *a).fetchall(), flush=True)
T0, WINIG, LOW, ENV, HIGH = 1720922725, 1721577749, 1721588607, 1721589800, 1721590213
g = json.load(open(ROOT + "/data/prevent_groups.json"))[0]
gs = json.load(open(ROOT + "/data/group_split.json"))
con.execute("CREATE TEMP TABLE g0(a VARCHAR)")
con.executemany("INSERT INTO g0 VALUES (?)", [[m] for m in g["members"]])
con.execute("CREATE TEMP TABLE ven(a VARCHAR)")
con.executemany("INSERT INTO ven VALUES (?)", [[a] for a in lv()])
CA = f"read_parquet('{A}/a13_ca.parquet')"
LEG = f"read_parquet('{A}/a15_leg.parquet')"
print("rapport : détenu", g["held_before_musk_M"], "acheteurs 1re heure", gs["acheteurs_premiere_heure"], "ventes", gs["ventes_24h"])
con.execute(f"CREATE TEMP TABLE bal AS SELECT account, arg_max(owner,(slot,tx_index)) o, arg_max(post,(slot,tx_index)) p, max(t) t FROM {CA} WHERE t<{LOW} GROUP BY 1")
show("solde réel à la borne basse des 33 (M), comptes", "SELECT round(sum(p)/1e12,3), count(*), sum((p>0)::int) FROM bal WHERE o IN (SELECT a FROM g0)")
show("  détail", "SELECT o, round(sum(p)/1e12,3) FROM bal WHERE o IN (SELECT a FROM g0) AND p>0 GROUP BY 1 ORDER BY 2 DESC")
show("soldes totaux à la borne basse : tous, réserves et courbe, hors pools (M)", """SELECT round(sum(p)/1e12,2), round(sum(CASE WHEN o IN (SELECT a FROM ven) OR o='5Q544fKrFoe6tsEbD7S8EmxGTJYAKtTVhAW5Q5pge4j1' OR o='87g44hEXP7R8ZxoAJtz941tsVftpEXC1LqAFTf2ZHtkH' THEN p ELSE 0 END)/1e12,2), round(sum(CASE WHEN o IN (SELECT a FROM ven) OR o='5Q544fKrFoe6tsEbD7S8EmxGTJYAKtTVhAW5Q5pge4j1' OR o='87g44hEXP7R8ZxoAJtz941tsVftpEXC1LqAFTf2ZHtkH' THEN 0 ELSE p END)/1e12,2) FROM bal""")
show("  top détenteurs non pool à la borne basse", """SELECT o, round(sum(p)/1e12,3) s FROM bal WHERE o NOT IN (SELECT a FROM ven) AND o<>'5Q544fKrFoe6tsEbD7S8EmxGTJYAKtTVhAW5Q5pge4j1' AND o<>'87g44hEXP7R8ZxoAJtz941tsVftpEXC1LqAFTf2ZHtkH' GROUP BY 1 ORDER BY s DESC LIMIT 15""")
show("ventes 24 h après la borne haute : marché, groupe (SOL)", f"SELECT round(sum(CASE WHEN dmaga<0 THEN sol ELSE 0 END)/1e9,1), round(sum(CASE WHEN dmaga<0 AND owner IN (SELECT a FROM g0) THEN sol ELSE 0 END)/1e9,1) FROM {LEG} WHERE t>={HIGH} AND t<{HIGH + 86400}")
show("groupe : achats en première heure, membres", f"SELECT count(DISTINCT owner) FROM {LEG} WHERE dmaga>0 AND t<{T0 + 3600} AND owner IN (SELECT a FROM g0)")
show("groupe : swaps entre visuel et borne basse", f"SELECT owner, signature, t, dmaga/1e12, sol/1e9 FROM {LEG} WHERE t>={WINIG} AND t<{LOW} AND owner IN (SELECT a FROM g0) ORDER BY t")
show("groupe : swaps entre borne basse et borne haute", f"SELECT owner, signature, t, dmaga/1e12, sol/1e9 FROM {LEG} WHERE t>={LOW} AND t<={HIGH} AND owner IN (SELECT a FROM g0) ORDER BY t")
show("transferts du groupe entre visuel et borne haute (a02)", f"SELECT owner, signature, t, (post-pre)/1e12 FROM {CA} WHERE t>={WINIG} AND t<={HIGH} AND owner IN (SELECT a FROM g0) ORDER BY t LIMIT 20")
sigs = [x["sig"] for x in gs["gestes_du_jour"]]
con.execute("CREATE TEMP TABLE gest(s VARCHAR)")
con.executemany("INSERT INTO gest VALUES (?)", [[s] for s in sigs])
show("gestes du jour relus dans a02 : n, min, max", f"SELECT count(DISTINCT signature), min(t), max(t) FROM {CA} WHERE signature IN (SELECT s FROM gest)")
edges = g["edges_top"]
print("arêtes du groupe", len(edges))
con.execute("CREATE TEMP TABLE ed(s VARCHAR, a VARCHAR, b VARCHAR, m DOUBLE)")
con.executemany("INSERT INTO ed VALUES (?,?,?,?)", [[e["sig"], e["src"], e["dst"], e["M"]] for e in edges])
show("arêtes relues : source qui perd et destination qui gagne le même montant dans a02", f"""WITH d AS (SELECT signature, owner, sum(post-pre) x FROM {CA} WHERE signature IN (SELECT s FROM ed) GROUP BY 1,2)
    SELECT count(*), sum((abs(a.x+b.x)<=1000 AND abs(a.x/1e12+ed.m)<0.002)::int) FROM ed JOIN d a ON a.signature=ed.s AND a.owner=ed.a JOIN d b ON b.signature=ed.s AND b.owner=ed.b""")
show("arêtes absentes de a02", f"SELECT count(*) FROM ed WHERE s NOT IN (SELECT DISTINCT signature FROM {CA})")
show("programmes des arêtes", f"""SELECT progs, count(*) FROM read_parquet('{A}/a15_tx.parquet') WHERE signature IN (SELECT s FROM ed) GROUP BY 1 ORDER BY 2 DESC""")
