#!/usr/bin/env python3
"""Auditeur A. Étiquettes et services : DCA, Jupiter, routeurs, CEX, venues dans link_edges et token_edges ; origine des fonds (C50). Lecture seule."""
import csv, json, sys, collections
import duckdb
sys.path.insert(0, "REDACTED_HOME/Projects/Dark-MAGA-Investigation")
from dmaga.labels import load as LL, KEEPERS, WSMO, INFRA
from dmaga.venues import load as VV
A = "/Volumes/VERBATIM HD/Dark-MAGA-Investigation/audits_work/A"
B = "/Volumes/VERBATIM HD/Dark-MAGA-Investigation/data"
con = duckdb.connect(":memory:", config={"memory_limit": "500MB", "threads": 2, "temp_directory": A + "/duck16", "preserve_insertion_order": False})
con.execute("SET TimeZone='UTC'")
q = lambda s, *a: con.execute(s, *a).fetchall()
def show(n, s, *a):
    print(n, q(s, *a), flush=True)
L, V = LL(), VV()
con.execute("CREATE TEMP TABLE lab(a VARCHAR, l VARCHAR, s VARCHAR)")
con.executemany("INSERT INTO lab VALUES (?,?,?)", [[a, v[0], v[1]] for a, v in L.items()])
con.execute("CREATE TEMP TABLE ven(a VARCHAR)")
con.executemany("INSERT INTO ven VALUES (?)", [[a] for a in V])
DCA = "DCA265Vj8a9CEuX1eb1LWRnDT7uK6q1xMipnNyatn23M"
print("programme DCA présent", q(f"SELECT count(DISTINCT signature) FROM read_parquet('{A}/a02_tx.parquet') WHERE progs LIKE '%{DCA}%'"))
show("signataires des tx DCA (top)", f"SELECT signers, count(DISTINCT signature) FROM read_parquet('{A}/a02_tx.parquet') WHERE progs LIKE '%{DCA}%' GROUP BY 1 ORDER BY 2 DESC LIMIT 15")
con.execute(f"CREATE TEMP TABLE dca AS SELECT DISTINCT signature, signers FROM read_parquet('{A}/a02_tx.parquet') WHERE progs LIKE '%{DCA}%'")
keep_found = {r[0] for r in q("SELECT DISTINCT signers FROM dca")}
print("signataires DCA connus de KEEPERS", {s: (s in KEEPERS) for s in list(keep_found)[:30]}, "n", len(keep_found))
print("signataires DCA hors étiquettes", [s for s in keep_found if not all(x in L for x in s.split(","))][:40])
show("propriétaires non signataires en tx DCA", f"""SELECT o.owner, count(DISTINCT o.signature), round(sum(abs(o.dmaga))/1e12,3), (SELECT l FROM lab WHERE a=o.owner) FROM read_parquet('{A}/a02_own.parquet') o JOIN dca USING (signature)
     WHERE NOT o.is_signer AND o.owner NOT IN (SELECT a FROM ven) GROUP BY 1 ORDER BY 2 DESC LIMIT 25""")
for name, tab in (("link_edges", f"read_parquet('{B}/link_edges.parquet')"), ("token_edges", f"read_parquet('{B}/token_edges.parquet')")):
    t = "type" if name == "link_edges" else "how"
    show(f"{name} : arêtes avec un service étiqueté", f"SELECT {t}, count(*) FROM {tab} WHERE src IN (SELECT a FROM lab) OR dst IN (SELECT a FROM lab) GROUP BY 1")
    show(f"{name} : arêtes avec une venue", f"SELECT {t}, count(*) FROM {tab} WHERE src IN (SELECT a FROM ven) OR dst IN (SELECT a FROM ven) GROUP BY 1")
show("link_edges funder_commun/sink_commun dont l'intermédiaire est étiqueté", f"SELECT type, count(*) FROM read_parquet('{B}/link_edges.parquet') WHERE type IN ('funder_commun','sink_commun') AND asset IN (SELECT a FROM lab) GROUP BY 1")
show("link_edges intermédiaire les plus fréquents", f"SELECT type, asset, count(*) n FROM read_parquet('{B}/link_edges.parquet') WHERE type IN ('funder_commun','sink_commun') GROUP BY 1,2 ORDER BY 3 DESC LIMIT 20")
# transferts directs : la transaction contient-elle un programme d'échange ?
con.execute(f"CREATE TEMP TABLE tx AS SELECT signature, any_value(progs) progs, any_value(signers) signers, any_value(vt_post-vt_pre) dt FROM read_parquet('{A}/a02_tx.parquet') WHERE signature IN (SELECT signature FROM read_parquet('{B}/link_edges.parquet') WHERE type='token_direct') GROUP BY 1")
AMM = ["675kPX9MHTjS2zt1qfr1NYHuzeLXfQM9H24wFSUt1Mp8", "CAMMCzo5YL8w4VFF8KVHrK22GGUsp5VTaW7grrKgrWqK", "LBUZKhRxPF3XUpBCjp4YzTKgLccjZhTSDM9YuVaPwxo", "whirLbMiicVdio4qvUfM5KAg6Ct8VwpYzGff3uctyCc", "JUP6LkbZbjS1jKKwapdHNy74zcZ3tLUZoi5QNyVTaV4", DCA]
cond = " OR ".join(f"t.progs LIKE '%{p}%'" for p in AMM)
show("token_direct : tx lue, tx avec programme d'échange, sans, tx absente du brut a02", f"""SELECT count(*), sum(({cond})::int), sum((t.signature IS NOT NULL AND NOT ({cond}))::int), sum((t.signature IS NULL)::int) FROM read_parquet('{B}/link_edges.parquet') e LEFT JOIN tx t USING (signature) WHERE e.type='token_direct'""")
show("  pour >= 1 M", f"""SELECT count(*), sum(({cond})::int), sum((t.signature IS NOT NULL AND NOT ({cond}))::int), sum((t.signature IS NULL)::int) FROM read_parquet('{B}/link_edges.parquet') e LEFT JOIN tx t USING (signature) WHERE e.type='token_direct' AND e.amount>=1000000""")
show("  >= 1 M avant borne basse, avec programme d'échange, exemples", f"""SELECT e.src, e.dst, e.amount, e.signature, t.progs FROM read_parquet('{B}/link_edges.parquet') e JOIN tx t USING (signature) WHERE e.type='token_direct' AND e.amount>=1000000 AND e.block_time<1721588607 AND ({cond}) LIMIT 8""")
g = json.load(open("REDACTED_HOME/Projects/Dark-MAGA-Investigation/data/prevent_groups.json"))[0]
con.execute("CREATE TEMP TABLE g0(a VARCHAR)")
con.executemany("INSERT INTO g0 VALUES (?)", [[m] for m in g["members"]])
show("membres du groupe jamais signataires dans le brut", f"""WITH s AS (SELECT DISTINCT unnest(string_split(signers,',')) a FROM read_parquet('{A}/a02_tx.parquet')) SELECT g0.a FROM g0 WHERE g0.a NOT IN (SELECT a FROM s)""")
show("membres dans DCA", f"SELECT DISTINCT o.owner FROM read_parquet('{A}/a02_own.parquet') o JOIN dca USING (signature) WHERE o.owner IN (SELECT a FROM g0)")
# origine des fonds
print("== C50")
F = f"read_parquet('{B}/funding_edges.parquet')"
show("funding : wallets, level, query", f"SELECT level, query, count(*), count(DISTINCT wallet), sum(terminal::int), sum(truncated::int) FROM {F} GROUP BY 1,2 ORDER BY 1,2")
show("funding : SOL par classe src_label (top)", f"SELECT coalesce(src_label,'(aucune)'), count(*), count(DISTINCT wallet), round(sum(sol)) FROM {F} WHERE level=0 GROUP BY 1 ORDER BY 4 DESC LIMIT 25")
show("funding : premier financeur non pool par wallet, classe", f"""WITH f AS (SELECT wallet, arg_min(src, block_time) s, arg_min(src_label, block_time) l, min(block_time) t FROM {F} WHERE level=0 AND NOT is_pool GROUP BY 1)
   SELECT CASE WHEN l IS NULL THEN 'sans étiquette' ELSE l END, count(*) FROM f GROUP BY 1 ORDER BY 2 DESC LIMIT 25""")
show("funding : SOL entrant niveau 0 selon classe large", f"""SELECT CASE WHEN is_pool THEN 'pool, trading antérieur' WHEN src_label IS NULL THEN 'sans étiquette' WHEN src_label LIKE 'Jupiter%' OR src_label LIKE 'Pont%' OR src_label LIKE 'Service%' THEN 'service' ELSE 'échange ou autre étiqueté' END c,
      count(*), count(DISTINCT wallet), round(sum(sol)), round(100.0*sum(sol)/sum(sum(sol)) OVER (),1) FROM {F} WHERE level=0 GROUP BY 1 ORDER BY 4 DESC""")
show("funding : sources sans étiquette à fort degré", f"SELECT src, count(DISTINCT wallet) n, round(sum(sol)) FROM {F} WHERE src_label IS NULL AND NOT is_pool GROUP BY 1 ORDER BY n DESC LIMIT 25")
show("exit_flows : colonnes", f"DESCRIBE SELECT * FROM read_parquet('{B}/exit_flows.parquet')")
