#!/usr/bin/env python3
"""Toutes les destinations de SOL et d'USD stables des wallets tracés (flows_all + net_flows, virements dédoublonnés par signature).
Pour chaque destination : expéditeurs, montants, périmètres touchés. Cherche les comptes de dépôt récurrents et les jonctions entre périmètres.
Sorties : work_G/g10_dest.csv (destinations d'au moins 2 expéditeurs tracés ou 5 SOL), work_G/g10_join.txt (destinations reliant deux périmètres)."""
import csv, json, sys, collections
import duckdb
from dmaga.labels import label
from dmaga.venues import load as lv
G = "/Volumes/VERBATIM HD/Dark-MAGA-Investigation/audits_work/G/"; OUT = "audits/2026-11-03/work_G/"
con = duckdb.connect(":memory:", config={"memory_limit": "800MB", "threads": 2, "temp_directory": G + "duck", "preserve_insertion_order": False})
con.execute("SET TimeZone='UTC'")
ven = set(lv())
SOLM = "So11111111111111111111111111111111111111111"
USD = ("EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v", "Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB")
con.execute(f"""CREATE TABLE e AS SELECT DISTINCT sig,bt,src,dst,mint,raw,ins,inner_ FROM read_parquet('{G}flows_all.parquet') WHERE mint IN ('{SOLM}','{USD[0]}','{USD[1]}') AND src<>dst AND src IS NOT NULL AND dst IS NOT NULL AND raw>=1000000""")
con.execute(f"""INSERT INTO e SELECT sig,bt,owner,cp,CASE asset WHEN 'SOL' THEN '{SOLM}' WHEN 'USDC' THEN '{USD[0]}' ELSE '{USD[1]}' END,round(amt*CASE asset WHEN 'SOL' THEN 1e9 ELSE 1e6 END),NULL,NULL
 FROM read_parquet('{G}net_flows.parquet') n WHERE dir='out' AND pure=1 AND asset IN ('SOL','USDC','USDT') AND amt>=0.001
 AND NOT EXISTS (SELECT 1 FROM e x WHERE x.sig=n.sig AND x.src=n.owner AND x.dst=n.cp)""")
print("arêtes", con.execute("SELECT count(*),count(DISTINCT src),count(DISTINCT dst) FROM e").fetchone())
roles = collections.defaultdict(set)
for r in csv.DictReader(open(OUT + "targets.csv")):
    for x in r["roles"].split("|"): roles[r["wallet"]].add(x)
rows = con.execute(f"""SELECT dst,count(DISTINCT src) ns,count(*) n,sum(CASE WHEN mint='{SOLM}' THEN raw/1e9 ELSE raw/1e6/170 END) soleq,strftime(to_timestamp(min(bt)),'%Y-%m-%d') a,strftime(to_timestamp(max(bt)),'%Y-%m-%d') b,string_agg(DISTINCT src,',') ss FROM e GROUP BY dst HAVING count(DISTINCT src)>=2 OR soleq>=5""").fetchall()
rows.sort(key=lambda r: -r[1])
with open(OUT + "g10_dest.csv", "w", newline="") as fh:
    w = csv.writer(fh); w.writerow("dst label venue n_senders n soleq first last roles senders".split())
    for r in rows:
        ss = r[6].split(",")
        rc = collections.Counter(x for s in ss for x in roles.get(s, ()))
        w.writerow([r[0], label(r[0]) or "", r[0] in ven, r[1], r[2], round(r[3], 3), r[4], r[5], ";".join(f"{k}:{v}" for k, v in sorted(rc.items())), ";".join(ss)[:800]])
print("destinations retenues", len(rows))
