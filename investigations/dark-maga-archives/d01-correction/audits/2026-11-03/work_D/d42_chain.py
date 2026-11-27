#!/usr/bin/env python3
"""Auditeur D. Chaîne de chaque compte de jetons depuis d01_acct (mon parseur). A-05 : ruptures, fenêtre, wallets tracés ou non. Soldes à T_low pour les périmètres de C-02, ventes et transferts 24 h pour C-05, angles morts de B-06.
Sorties : d42_chain.txt, audits_work/D/d42_rupt.parquet, audits_work/D/d42_bal_T.parquet."""
import csv, json, os, sys
import duckdb
D = "/Volumes/VERBATIM HD/Dark-MAGA-Investigation/audits_work/D"; BIG = "/Volumes/VERBATIM HD/Dark-MAGA-Investigation/data"; RAW = "/Volumes/VERBATIM HD/Dark-MAGA-Investigation/raw"
OUT = "audits/2026-11-03/work_D/"
con = duckdb.connect(":memory:", config={"memory_limit": "800MB", "threads": 2, "temp_directory": D + "/duck", "preserve_insertion_order": False})
con.execute("SET TimeZone='UTC'")
sys.stdout = open(OUT + "d42_chain.txt", "w")
def q(n, s):
    r = con.execute(s).fetchall(); print(n, r, flush=True); return r
AC = f"read_parquet('{D}/d01_acct.parquet')"
T0, S, LOW, HIGH = 1720922725, 1721588400, 1721588607, 1721590213
traced = [p for p in os.listdir(RAW + "/flows") if not p.startswith("._")]
con.execute("CREATE TEMP TABLE tr(a VARCHAR)"); con.executemany("INSERT INTO tr VALUES (?)", [[x] for x in traced])
G = json.load(open("data/prevent_groups.json"))[0]["members"]
con.execute("CREATE TEMP TABLE g(a VARCHAR)"); con.executemany("INSERT INTO g VALUES (?)", [[x] for x in G])
SER = [r["dest"] for r in csv.DictReader(open("audits/2026-11-03/work_C/cb_window.csv")) if "2024-07-14T01:32:20Z" <= r["utc"] <= "2024-07-14T01:40:51Z" and round(float(r["sol"]) * 1e9) in (500000000, 1000000000, 1050000000)]
assert len(SER) == 15
SEND = [r["sender"] for r in csv.DictReader(open(OUT + "d20_senders.csv"))]
assert len(SEND) == 48
con.execute("CREATE TEMP TABLE ser(a VARCHAR)"); con.executemany("INSERT INTO ser VALUES (?)", [[x] for x in SER])
con.execute("CREATE TEMP TABLE sen(a VARCHAR)"); con.executemany("INSERT INTO sen VALUES (?)", [[x] for x in SEND])
con.execute(f"""COPY (WITH a AS (SELECT DISTINCT sig,slot,idx,bt,account,owner,pre,post FROM {AC}),
     c AS (SELECT *, lag(post) OVER w prev, lag(bt) OVER w prev_bt, lag(owner) OVER w prev_owner FROM a WINDOW w AS (PARTITION BY account ORDER BY slot,idx))
     SELECT sig,slot,idx,bt,account,owner,prev_owner,pre,post,prev,prev_bt,pre-coalesce(prev,0) gap FROM c WHERE pre<>coalesce(prev,0)) TO '{D}/d42_rupt.parquet' (FORMAT parquet, COMPRESSION zstd)""")
R = f"read_parquet('{D}/d42_rupt.parquet')"
q("ruptures : n, comptes, entrées M, sorties M", f"SELECT count(*),count(DISTINCT account),round(sum(CASE WHEN gap>0 THEN gap ELSE 0 END)/1e12,1),round(sum(CASE WHEN gap<0 THEN -gap ELSE 0 END)/1e12,1) FROM {R}")
q("par année (de l'observation)", f"SELECT strftime(to_timestamp(bt),'%Y'),count(*),round(sum(abs(gap))/1e12,1) FROM {R} GROUP BY 1 ORDER BY 1")
con.execute(f"CREATE TEMP TABLE r2 AS SELECT *, coalesce(owner,prev_owner) o, prev_bt iv0, bt iv1 FROM {R}")
q("intervalle (dernière vue, observation) coupe ou précède T_low : avant T_low", f"SELECT count(*),round(sum(abs(gap))/1e12,3),count(DISTINCT o) FROM r2 WHERE iv1<{LOW}")
q("  à cheval sur T_low (solde périmé à T_low)", f"SELECT o,account,prev_bt,bt,round(gap/1e12,3) FROM r2 WHERE coalesce(iv0,0)<{LOW} AND iv1>={LOW} AND abs(gap)>1e9 ORDER BY abs(gap) DESC LIMIT 15")
q("  à cheval : n, somme", f"SELECT count(*),round(sum(abs(gap))/1e12,3) FROM r2 WHERE coalesce(iv0,0)<{LOW} AND iv1>={LOW}")
q("avant T_low, par propriétaire et tracé", f"SELECT o,(o IN (SELECT a FROM tr)),count(*),round(sum(gap)/1e12,3) FROM r2 WHERE iv1<{LOW} GROUP BY 1,2 ORDER BY abs(sum(gap)) DESC LIMIT 10")
q("24 h suivant T_high : n, somme M, comptes (intervalle chevauchant)", f"SELECT count(*),round(sum(abs(gap))/1e12,3),count(DISTINCT account) FROM r2 WHERE iv1>={HIGH} AND iv1<{HIGH+86400}")
q("24 h, sorties cachées de propriétaires tracés / non tracés", f"SELECT (o IN (SELECT a FROM tr)),count(*),round(sum(CASE WHEN gap<0 THEN -gap ELSE 0 END)/1e12,3),round(sum(CASE WHEN gap>0 THEN gap ELSE 0 END)/1e12,3) FROM r2 WHERE iv1>={HIGH} AND iv1<{HIGH+86400} GROUP BY 1")
q("tracé / non tracé, toutes dates", f"SELECT (o IN (SELECT a FROM tr)),count(*),count(DISTINCT o),round(sum(abs(gap))/1e12,1) FROM r2 GROUP BY 1")
q("non tracés, gap >= 1 M par période (avant T_low, 24 h, après)", f"SELECT CASE WHEN iv1<{LOW} THEN 'avant' WHEN iv1<{HIGH+86400} THEN '24h' ELSE 'apres' END p,count(*),round(sum(abs(gap))/1e12,1) FROM r2 WHERE abs(gap)>=1e12 AND o NOT IN (SELECT a FROM tr) GROUP BY 1")
NAM = ["H3QsBrrivimFJmSpTXuvig2n1Bh7JuYxrriRSEszT6cc", "GXZvXsD6hxaLeFvQisWpdAwsayJxga7w9EeafhFZG2Ra", "9PrmF8sfoD2YShtWUghrGEYgxwabpnzog8gT1V6LEtdq", "5QhJJcFZu2ashyKyWSTGHcsyo6ZBCbpVuJqeutvQHScd", "8YLEuUtZ4eFMJbf46oNb1CeG6dYFWGyxnQSh9hrgzBzR"]
q("ruptures des wallets nommés", f"SELECT o,(o IN (SELECT a FROM tr)),count(*),round(sum(abs(gap))/1e12,3) FROM r2 WHERE o IN ({','.join(repr(x) for x in NAM)}) GROUP BY 1,2")
q("ruptures du groupe de 33", f"SELECT o,count(*),round(sum(gap)/1e12,3),min(bt) FROM r2 WHERE o IN (SELECT a FROM g) GROUP BY 1 ORDER BY 3 DESC")
# 2. soldes à T_low
con.execute(f"""COPY (SELECT account,arg_max(owner,(slot,idx)) owner,arg_max(post,(slot,idx)) bal FROM (SELECT DISTINCT sig,slot,idx,bt,account,owner,pre,post FROM {AC}) WHERE bt<{LOW} GROUP BY 1) TO '{D}/d42_bal_T.parquet' (FORMAT parquet, COMPRESSION zstd)""")
B = f"read_parquet('{D}/d42_bal_T.parquet')"
q("somme des derniers soldes à T_low (M)", f"SELECT count(*),round(sum(bal)/1e12,3) FROM {B}")
EDG = f"read_parquet('{BIG}/token_edges.parquet')"
q("transferts gtba avant T_low absents de mon brut", f"SELECT count(*),round(sum(qty)/1e6,3) FROM {EDG} WHERE how='gtba' AND block_time<{LOW} AND signature NOT IN (SELECT sig FROM {AC})")
con.execute(f"""CREATE TEMP TABLE hid AS SELECT src,dst,qty*1e6 q,block_time,signature FROM {EDG} WHERE how='gtba' AND block_time<{LOW} AND signature NOT IN (SELECT sig FROM {AC}) AND dst<>'(multiple)'""")
q("  détail", "SELECT src,dst,round(q/1e12,3),block_time,signature FROM hid ORDER BY q DESC LIMIT 10")
# solde corrigé par propriétaire : les comptes sources restent périmés seulement si leur prochaine vue est après T_low ; la destination a déjà été revue si elle apparaît avant T_low
con.execute(f"""CREATE TEMP TABLE adj AS SELECT o, sum(g) d FROM (SELECT o, gap g FROM r2 WHERE coalesce(iv0,0)<{LOW} AND iv1>={LOW} AND 0=1) GROUP BY 1""")
con.execute(f"""CREATE TEMP TABLE own_T AS WITH b AS (SELECT owner,sum(bal) v FROM {B} GROUP BY 1),
   out_ AS (SELECT src a,sum(q) v FROM hid GROUP BY 1)
   SELECT b.owner, b.v - coalesce(out_.v,0) v FROM b LEFT JOIN out_ ON out_.a=b.owner""")
from dmaga.venues import load as lv
ven = list(lv()) + ["5Q544fKrFoe6tsEbD7S8EmxGTJYAKtTVhAW5Q5pge4j1", "87g44hEXP7R8ZxoAJtz941tsVftpEXC1LqAFTf2ZHtkH", "39azUYFWPz3VHgKCf3VChUwbpURdCHRxjWVowf5jUJjg"]
con.execute("CREATE TEMP TABLE ve(a VARCHAR)"); con.executemany("INSERT INTO ve VALUES (?)", [[x] for x in ven])
q("somme corrigée, pools, hors pools (M)", "SELECT round(sum(v)/1e12,3),round(sum(CASE WHEN owner IN (SELECT a FROM ve) THEN v ELSE 0 END)/1e12,3),round(sum(CASE WHEN owner IN (SELECT a FROM ve) THEN 0 ELSE v END)/1e12,3) FROM own_T")
def per(name, tbl):
    return q(name, f"SELECT count(*),round(sum(v)/1e12,3),round(100*sum(v)/938e12,2),(SELECT count(*) FROM {tbl}) FROM own_T WHERE owner IN (SELECT a FROM {tbl})")
per("groupe 33 à T_low", "g"); per("série 15", "ser"); per("48 expéditeurs", "sen")
con.execute("CREATE TEMP TABLE ser13 AS SELECT a FROM ser WHERE a IN (SELECT a FROM sen)"); per("série retour 13", "ser13")
con.execute("CREATE TEMP TABLE un AS SELECT a FROM g UNION SELECT a FROM ser UNION SELECT a FROM sen"); per("union", "un")
con.execute("CREATE TEMP TABLE sg AS SELECT a FROM ser WHERE a NOT IN (SELECT a FROM g)"); per("série hors 33", "sg")
con.execute("CREATE TEMP TABLE eg AS SELECT a FROM sen WHERE a NOT IN (SELECT a FROM g)"); per("expéditeurs hors 33", "eg")
q("créateur dans le groupe ?", "SELECT count(*) FROM g WHERE a='8YLEuUtZ4eFMJbf46oNb1CeG6dYFWGyxnQSh9hrgzBzR'")
q("intersection g/ser, g/sen", "SELECT (SELECT count(*) FROM g WHERE a IN (SELECT a FROM ser)),(SELECT count(*) FROM g WHERE a IN (SELECT a FROM sen)),(SELECT count(*) FROM ser WHERE a IN (SELECT a FROM sen))")
# transferts du créateur : mon brut, flux du créateur
CR = NAM[4]
q("créateur : lignes transfer dans trades, gtba", f"SELECT kind,count(*),round(sum(token_delta)/1e12,3) FROM read_parquet('{BIG}/trades.parquet') WHERE owner='{CR}' GROUP BY 1")
q("créateur : arêtes token_edges", f"SELECT src,dst,round(qty/1e6,3),block_time,signature,how FROM {EDG} WHERE src='{CR}' OR dst='{CR}' ORDER BY block_time")
q("arêtes token_edges créateur <-> 33", f"SELECT count(*) FROM {EDG} WHERE (src='{CR}' AND dst IN (SELECT a FROM g)) OR (dst='{CR}' AND src IN (SELECT a FROM g))")
# 3. expéditeurs avec DMAGA
OW = f"read_parquet('{D}/d01_own.parquet')"
q("48 expéditeurs : touchent DMAGA (delta non nul dans mon brut)", f"SELECT count(DISTINCT owner) FROM {OW} WHERE owner IN (SELECT a FROM sen)")
q("  dont hors série et hors 33", f"SELECT count(DISTINCT owner) FROM {OW} WHERE owner IN (SELECT a FROM sen) AND owner NOT IN (SELECT a FROM ser) AND owner NOT IN (SELECT a FROM g)")
q("  expéditeurs hors série et hors 33 (dénominateur)", "SELECT count(*) FROM sen WHERE a NOT IN (SELECT a FROM ser) AND a NOT IN (SELECT a FROM g)")
ctrl = [r["sender"] if "sender" in r else None for r in []]
