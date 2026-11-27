#!/usr/bin/env python3
"""Auditeur D. Suite de d42 (qui a été tué par le garde sur un NOT IN coûteux, réécrit ici) : soldes à T_low corrigés, périmètres C-02, lien créateur, C-05, B-06. Sortie d43_perim.txt."""
import csv, json, os, sys
import duckdb
D = "/Volumes/VERBATIM HD/Dark-MAGA-Investigation/audits_work/D"; BIG = "/Volumes/VERBATIM HD/Dark-MAGA-Investigation/data"
OUT = "audits/2026-11-03/work_D/"
con = duckdb.connect(":memory:", config={"memory_limit": "700MB", "threads": 2, "temp_directory": D + "/duck", "preserve_insertion_order": False})
con.execute("SET TimeZone='UTC'")
sys.stdout = open(OUT + "d43_perim.txt", "w")
def q(n, s):
    r = con.execute(s).fetchall(); print(n, r, flush=True); return r
AC = f"read_parquet('{D}/d01_acct.parquet')"; OW = f"read_parquet('{D}/d01_own.parquet')"; TR = f"read_parquet('{BIG}/trades.parquet')"; EDG = f"read_parquet('{BIG}/token_edges.parquet')"; R = f"read_parquet('{D}/d42_rupt.parquet')"
T0, S, LOW, HIGH = 1720922725, 1721588400, 1721588607, 1721590213
G = json.load(open("data/prevent_groups.json"))[0]["members"]
con.execute("CREATE TEMP TABLE g(a VARCHAR)"); con.executemany("INSERT INTO g VALUES (?)", [[x] for x in G])
SER = [r["dest"] for r in csv.DictReader(open("audits/2026-11-03/work_C/cb_window.csv")) if "2024-07-14T01:32:20Z" <= r["utc"] <= "2024-07-14T01:40:51Z" and round(float(r["sol"]) * 1e9) in (500000000, 1000000000, 1050000000)]
assert len(SER) == 15
SEND = [r["sender"] for r in csv.DictReader(open(OUT + "d20_senders.csv"))]
assert len(SEND) == 48
con.execute("CREATE TEMP TABLE ser(a VARCHAR)"); con.executemany("INSERT INTO ser VALUES (?)", [[x] for x in SER])
con.execute("CREATE TEMP TABLE sen(a VARCHAR)"); con.executemany("INSERT INTO sen VALUES (?)", [[x] for x in SEND])
B = f"read_parquet('{D}/d42_bal_T.parquet')"
con.execute(f"CREATE TEMP TABLE cand AS SELECT src,dst,qty*1e6 q,block_time,signature FROM {EDG} WHERE how='gtba' AND block_time<{LOW} AND dst<>'(multiple)'")
con.execute(f"CREATE TEMP TABLE seen AS SELECT DISTINCT sig FROM {AC} WHERE bt<{LOW}")
con.execute("CREATE TEMP TABLE hid AS SELECT * FROM cand WHERE signature NOT IN (SELECT sig FROM seen)")
q("gtba avant T_low : candidats, absents de mon brut, M", "SELECT (SELECT count(*) FROM cand),count(*),round(sum(q)/1e12,3) FROM hid")
q("  détail", "SELECT src,dst,round(q/1e12,3),block_time,signature FROM hid ORDER BY q DESC LIMIT 8")
con.execute(f"""CREATE TEMP TABLE own_T AS WITH b AS (SELECT owner,sum(bal) v FROM {B} GROUP BY 1), o AS (SELECT src a,sum(q) v FROM hid GROUP BY 1)
   SELECT b.owner,b.v-coalesce(o.v,0) v FROM b LEFT JOIN o ON o.a=b.owner""")
from dmaga.venues import load as lv
ven = list(lv()) + ["5Q544fKrFoe6tsEbD7S8EmxGTJYAKtTVhAW5Q5pge4j1", "87g44hEXP7R8ZxoAJtz941tsVftpEXC1LqAFTf2ZHtkH", "39azUYFWPz3VHgKCf3VChUwbpURdCHRxjWVowf5jUJjg"]
con.execute("CREATE TEMP TABLE ve(a VARCHAR)"); con.executemany("INSERT INTO ve VALUES (?)", [[x] for x in ven])
q("somme corrigée, pools, hors pools (M)", "SELECT round(sum(v)/1e12,3),round(sum(CASE WHEN owner IN (SELECT a FROM ve) THEN v ELSE 0 END)/1e12,3),round(sum(CASE WHEN owner IN (SELECT a FROM ve) THEN 0 ELSE v END)/1e12,3) FROM own_T")
def per(name, tbl):
    return q(name + " : wallets avec solde vu, M, % de 938, taille", f"SELECT count(*),round(sum(v)/1e12,3),round(100*sum(v)/938e12,2),(SELECT count(*) FROM {tbl}) FROM own_T WHERE owner IN (SELECT a FROM {tbl})")
per("groupe 33", "g"); per("série 15", "ser"); per("48 expéditeurs", "sen")
con.execute("CREATE TEMP TABLE ser13 AS SELECT a FROM ser WHERE a IN (SELECT a FROM sen)"); per("série retour 13", "ser13")
con.execute("CREATE TEMP TABLE un AS SELECT a FROM g UNION SELECT a FROM ser UNION SELECT a FROM sen"); per("union", "un")
con.execute("CREATE TEMP TABLE sg AS SELECT a FROM ser WHERE a NOT IN (SELECT a FROM g)"); per("série hors 33", "sg")
con.execute("CREATE TEMP TABLE eg AS SELECT a FROM sen WHERE a NOT IN (SELECT a FROM g)"); per("expéditeurs hors 33", "eg")
con.execute("CREATE TEMP TABLE cr13 AS SELECT a FROM ser13 UNION SELECT a FROM sen"); per("série-retour + expéditeurs (sans les 33 pures)", "cr13")
q("intersection g/ser, g/sen, ser/sen", "SELECT (SELECT count(*) FROM g WHERE a IN (SELECT a FROM ser)),(SELECT count(*) FROM g WHERE a IN (SELECT a FROM sen)),(SELECT count(*) FROM ser WHERE a IN (SELECT a FROM sen))")
print("membres du groupe parmi les expéditeurs", [r[0] for r in con.execute("SELECT a FROM g WHERE a IN (SELECT a FROM sen)").fetchall()])
CR = "8YLEuUtZ4eFMJbf46oNb1CeG6dYFWGyxnQSh9hrgzBzR"
q("créateur dans le groupe ?", f"SELECT count(*) FROM g WHERE a='{CR}'")
q("créateur : lignes trades par kind", f"SELECT kind,count(*),round(sum(token_delta)/1e12,3) FROM {TR} WHERE owner='{CR}' GROUP BY 1")
q("créateur : arêtes token_edges", f"SELECT src,dst,round(qty/1e6,3),block_time,signature,how FROM {EDG} WHERE src='{CR}' OR dst='{CR}' ORDER BY block_time")
q("arêtes créateur <-> 33", f"SELECT count(*) FROM {EDG} WHERE (src='{CR}' AND dst IN (SELECT a FROM g)) OR (dst='{CR}' AND src IN (SELECT a FROM g))")
q("mon brut : tx où le créateur et un membre bougent DMAGA ensemble", f"WITH c AS (SELECT DISTINCT sig FROM {OW} WHERE owner='{CR}') SELECT o.owner,o.sig,o.d FROM {OW} o JOIN c USING(sig) WHERE o.owner IN (SELECT a FROM g)")
NAM = ["H3QsBrrivimFJmSpTXuvig2n1Bh7JuYxrriRSEszT6cc", "GXZvXsD6hxaLeFvQisWpdAwsayJxga7w9EeafhFZG2Ra", "9PrmF8sfoD2YShtWUghrGEYgxwabpnzog8gT1V6LEtdq"]
L = ",".join(repr(x) for x in NAM)
q("C20 mon brut : tx où un des 3 et un membre, créateur ou expéditeur bougent DMAGA en sens opposé, hors tx avec vault Raydium", f"""WITH c AS (SELECT DISTINCT sig,owner,d FROM {OW} WHERE owner IN ({L})), v AS (SELECT DISTINCT sig FROM read_parquet('{D}/d01_tx.parquet') WHERE vt_d<>0)
    SELECT c.owner,o.owner,o.sig,c.d,o.d FROM {OW} o JOIN c USING(sig) WHERE (o.owner IN (SELECT a FROM g) OR o.owner IN (SELECT a FROM sen) OR o.owner IN (SELECT a FROM ser)) AND sign(c.d)<>sign(o.d) AND o.sig NOT IN (SELECT sig FROM v) LIMIT 20""")
q("C20 token_edges entre les 3 et 33, série, expéditeurs", f"SELECT src,dst,round(qty/1e6,3),signature,how FROM {EDG} WHERE (src IN ({L}) AND (dst IN (SELECT a FROM un))) OR (dst IN ({L}) AND (src IN (SELECT a FROM un))) LIMIT 20")
# expéditeurs avec DMAGA
q("48 expéditeurs touchant DMAGA dans mon brut", f"SELECT count(DISTINCT owner) FROM {OW} WHERE owner IN (SELECT a FROM sen)")
q("  hors série et hors 33 : touchent, dénominateur", f"SELECT (SELECT count(DISTINCT owner) FROM {OW} WHERE owner IN (SELECT a FROM sen) AND owner NOT IN (SELECT a FROM ser) AND owner NOT IN (SELECT a FROM g)),(SELECT count(*) FROM sen WHERE a NOT IN (SELECT a FROM ser) AND a NOT IN (SELECT a FROM g))")
# témoin : expéditeurs du témoin, depuis ctrl_deposits
import gzip
NET = "/Volumes/VERBATIM HD/Dark-MAGA-Investigation/audits_work/C/net/"
pairs = set()
with gzip.open(NET + "ctrl_deposits.jsonl.gz", "rt") as fh:
    for l in fh:
        j = json.loads(l); x = j["x"]; t = j["tx"]; m = t["transaction"]["message"]; seq = list(m["instructions"])
        for g_ in t["meta"].get("innerInstructions") or []: seq += g_["instructions"]
        for i in seq:
            p = i.get("parsed")
            if i.get("program") == "system" and isinstance(p, dict) and p.get("type") == "transfer" and p["info"]["destination"] == x and int(p["info"]["lamports"]) >= 1_000_000:
                pairs.add((x, p["info"]["source"]))
con.execute("CREATE TEMP TABLE cs(x VARCHAR, s VARCHAR)"); con.executemany("INSERT INTO cs VALUES (?,?)", [list(p) for p in pairs])
q("témoin : paires, expéditeurs distincts", "SELECT count(*),count(DISTINCT s) FROM cs")
q("témoin : expéditeurs touchant DMAGA dans mon brut, dépôts concernés, max par dépôt", f"WITH h AS (SELECT DISTINCT cs.x,cs.s FROM cs JOIN (SELECT DISTINCT owner FROM {OW}) o ON o.owner=cs.s) SELECT count(*),count(DISTINCT s),count(DISTINCT x),(SELECT max(c) FROM (SELECT x,count(*) c FROM h GROUP BY 1)) FROM h")
# C-05 : transferts sortants du groupe en 24 h et ventes des destinataires, attribution plafonnée
TF = f"{HIGH}"; TZ = f"{HIGH+86400}"
con.execute(f"""CREATE TEMP TABLE gout AS SELECT src,dst,qty*1e6 q,block_time t,signature FROM {EDG} WHERE block_time>={TF} AND block_time<{TZ} AND src IN (SELECT a FROM g) AND dst NOT IN (SELECT a FROM g) AND dst<>'(multiple)'""")
q("groupe, transferts sortants hors groupe 24 h : n, M, destinataires", "SELECT count(*),round(sum(q)/1e12,3),count(DISTINCT dst) FROM gout")
q("détail", "SELECT src,dst,round(q/1e12,3),t,signature FROM gout ORDER BY q DESC LIMIT 15")
q("internes au groupe 24 h : n, M", f"SELECT count(*),round(sum(qty)/1e6,3) FROM {EDG} WHERE block_time>={TF} AND block_time<{TZ} AND src IN (SELECT a FROM g) AND dst IN (SELECT a FROM g)")
rows = con.execute("SELECT dst,min(t),sum(q) FROM gout GROUP BY 1").fetchall()
att = tot_all = 0.0; lines = []
for d_, t_, q_ in rows:
    r = con.execute(f"SELECT coalesce(sum(CASE WHEN token_delta<0 THEN -token_delta END),0),coalesce(sum(CASE WHEN token_delta<0 THEN sol_lamports END),0) FROM (SELECT DISTINCT signature,owner,kind,token_delta,sol_lamports FROM {TR} WHERE owner='{d_}' AND kind='swap' AND block_time>={TF} AND block_time<{TZ})").fetchone()
    r2 = con.execute(f"SELECT coalesce(sum(CASE WHEN token_delta<0 THEN -token_delta END),0),coalesce(sum(CASE WHEN token_delta<0 THEN sol_lamports END),0) FROM (SELECT DISTINCT signature,owner,kind,token_delta,sol_lamports FROM {TR} WHERE owner='{d_}' AND kind='swap' AND block_time>={t_} AND block_time<{TZ})").fetchone()
    tot_all += r[1]
    if r2[0]:
        capped = r2[1] * min(1.0, q_ / r2[0]); att += capped
        lines.append((d_, round(q_ / 1e12, 3), round(r[0] / 1e12, 3), round(r[1] / 1e9, 1), round(r2[0] / 1e12, 3), round(r2[1] / 1e9, 1), round(capped / 1e9, 1)))
print("destinataires vendeurs (reçu M, vendu 24 h M, SOL, vendu après réception M, SOL, SOL plafonné au reçu)", lines, flush=True)
print("ventes destinataires 24 h, toutes", round(tot_all / 1e9, 1), "plafonnées au reçu et après réception", round(att / 1e9, 1))
gs = con.execute(f"SELECT coalesce(sum(CASE WHEN token_delta<0 THEN sol_lamports END),0)/1e9,coalesce(sum(-token_delta),0)/1e12 FROM (SELECT DISTINCT signature,owner,kind,token_delta,sol_lamports FROM {TR} WHERE owner IN (SELECT a FROM g) AND kind='swap' AND token_delta<0 AND block_time>={TF} AND block_time<{TZ})").fetchone()
mk = con.execute(f"SELECT sum(sol_lamports)/1e9 FROM (SELECT DISTINCT signature,owner,kind,venue,token_delta,sol_lamports FROM {TR} WHERE kind='swap' AND token_delta<0 AND block_time>={TF} AND block_time<{TZ})").fetchone()[0]
print("ventes groupe SOL, M", gs, "marché dédoublonné", mk, "part", round(100 * gs[0] / mk, 3), "+ plafonné", round(100 * (gs[0] + att / 1e9) / mk, 3), "+ non plafonné", round(100 * (gs[0] + tot_all / 1e9) / mk, 3))
# autres détenteurs >= 1 M, même base
con.execute("CREATE TEMP TABLE o AS SELECT owner a,v FROM own_T WHERE v>=1e12 AND owner NOT IN (SELECT a FROM ve) AND owner NOT IN (SELECT a FROM g)")
con.execute(f"INSERT INTO ve SELECT address FROM read_parquet('{BIG}/nodes.parquet') WHERE kind<>'wallet'")
con.execute("DELETE FROM o WHERE a IN (SELECT a FROM ve)")
q("autres >= 1 M : n, M", "SELECT count(*),round(sum(v)/1e12,2) FROM o")
oth = con.execute(f"""SELECT kind,round(sum(-token_delta)/1e12,3),count(DISTINCT owner) FROM (SELECT DISTINCT signature,owner,kind,token_delta FROM {TR} WHERE owner IN (SELECT a FROM o) AND token_delta<0 AND block_time>={TF} AND block_time<{TZ}) GROUP BY 1""").fetchall()
print("autres, sorties 24 h par kind", oth, flush=True)
gx = con.execute(f"""SELECT kind,round(sum(-token_delta)/1e12,3),count(DISTINCT owner) FROM (SELECT DISTINCT signature,owner,kind,token_delta FROM {TR} WHERE owner IN (SELECT a FROM g) AND token_delta<0 AND block_time>={TF} AND block_time<{TZ}) GROUP BY 1""").fetchall()
print("groupe, sorties 24 h par kind", gx, flush=True)
q("autres, transferts token_edges 24 h sortants, vers autre que eux-mêmes", f"SELECT round(sum(qty)/1e6,3),count(*) FROM {EDG} WHERE block_time>={TF} AND block_time<{TZ} AND src IN (SELECT a FROM o) AND dst<>'(multiple)'")
q("  dont vers un autre détenteur >=1 M ou un service", f"SELECT round(sum(qty)/1e6,3) FROM {EDG} WHERE block_time>={TF} AND block_time<{TZ} AND src IN (SELECT a FROM o) AND dst IN (SELECT a FROM o)")
q("sorties cachées 24 h, autres >= 1 M (ruptures)", f"SELECT count(*),round(sum(-gap)/1e12,3) FROM {R} WHERE bt>={TF} AND bt<{TZ} AND gap<0 AND coalesce(owner,prev_owner) IN (SELECT a FROM o)")
q("sorties cachées 24 h, groupe", f"SELECT count(*),round(coalesce(sum(-gap),0)/1e12,3) FROM {R} WHERE bt>={TF} AND bt<{TZ} AND gap<0 AND coalesce(owner,prev_owner) IN (SELECT a FROM g)")
