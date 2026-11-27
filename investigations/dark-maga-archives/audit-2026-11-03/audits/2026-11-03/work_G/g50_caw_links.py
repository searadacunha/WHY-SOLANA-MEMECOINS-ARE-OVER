#!/usr/bin/env python3
"""Expéditeurs de Caw4 hors des 48 de 9W9b, hors série et hors 33 : ont-ils une arête directe avec le périmètre créateur (hors dépôts, hors poussière) ? Couverture de l'historique notée. Sortie g50.txt, g50_caw_others.csv."""
import csv, json, os, sys, collections
import duckdb
OUT = "audits/2026-11-03/work_G/"; G = "/Volumes/VERBATIM HD/Dark-MAGA-Investigation/audits_work/G/"; NETC = "/Volumes/VERBATIM HD/Dark-MAGA-Investigation/audits_work/C/net/"
sys.stdout = open(OUT + "g50.txt", "w")
series = {r["wallet"] for r in csv.DictReader(open("audits/2026-11-03/work_C/cb_series.csv"))}
send9 = {r["sender"] for r in csv.DictReader(open("audits/2026-11-03/work_D/d20_senders.csv"))}
g33 = set(json.load(open("data/prevent_groups.json"))[0]["members"])
inp = list(csv.DictReader(open(OUT + "g30_in.csv")))
caw = collections.Counter(); usd = collections.Counter()
for r in inp:
    if r["depot"].startswith("Caw4") and r["asset"] != "DMAGA": caw[r["sender"]] += 1; usd[r["sender"]] += float(r["sol_eq"])
P1 = (series | send9 | {"8YLEuUtZ4eFMJbf46oNb1CeG6dYFWGyxnQSh9hrgzBzR"})
others = [s for s in caw if s not in P1 and s not in g33]
touch = {r["sender"] for r in inp if r["depot"].startswith("Caw4") and r["signed_by_sender"] and False}
con = duckdb.connect(":memory:", config={"memory_limit": "500MB", "threads": 2, "temp_directory": G + "duck"})
con.execute("CREATE TABLE o(a VARCHAR)"); con.executemany("INSERT INTO o VALUES (?)", [[a] for a in others])
con.execute("CREATE TABLE p(a VARCHAR)"); con.executemany("INSERT INTO p VALUES (?)", [[a] for a in P1])
tch = {r[0] for r in con.execute(f"SELECT DISTINCT owner FROM '/Volumes/VERBATIM HD/Dark-MAGA-Investigation/audits_work/D/d01_own.parquet' WHERE owner IN (SELECT a FROM o)").fetchall()}
SOLM = "So11111111111111111111111111111111111111111"
n = con.execute(f"""SELECT o.a,p.a,dir,asset,sum(amt),count(*) FROM o JOIN read_parquet('{G}net_flows.parquet') f ON f.owner=o.a JOIN p ON p.a=f.cp WHERE pure=1 AND asset IN ('SOL','USDC','USDT','DMAGA') AND ((asset='SOL' AND amt>=0.001) OR (asset<>'SOL' AND amt>=1)) GROUP BY 1,2,3,4""").fetchall()
m = con.execute(f"""SELECT f.cp,f.owner,dir,asset,sum(amt),count(*) FROM read_parquet('{G}net_flows.parquet') f WHERE f.owner IN (SELECT a FROM p) AND f.cp IN (SELECT a FROM o) AND pure=1 AND asset IN ('SOL','USDC','USDT','DMAGA') AND ((asset='SOL' AND amt>=0.001) OR (asset<>'SOL' AND amt>=1)) GROUP BY 1,2,3,4""").fetchall()
links = collections.defaultdict(set)
for r in n + m:
    links[r[0]].add((r[1][:8], r[3], round(r[4], 3)))
w = csv.writer(open(OUT + "g50_caw_others.csv", "w", newline="")); w.writerow("sender sol_eq_vers_caw4 touche_dmaga historique_lu lie_au_perimetre detail".split())
hist = {r["owner"] for r in csv.DictReader(open(G + "net_stats.csv"))}
for s in sorted(others, key=lambda x: -usd[x]):
    w.writerow([s, round(usd[s], 3), s in tch, s in hist, bool(links.get(s)), sorted(links.get(s, []))[:6]])
lk = [s for s in others if links.get(s)]
print("expéditeurs de Caw4", len(caw), "hors périmètre créateur et hors 33", len(others), "SOL éq.", round(sum(usd[s] for s in others), 2), "sur", round(sum(usd.values()), 2))
print("  dont avec arête directe au périmètre créateur", len(lk), "SOL éq.", round(sum(usd[s] for s in lk), 2), "; avec historique lu", sum(1 for s in others if s in hist), "; touchent DMAGA", len(set(others) & tch))
print("  sans arête vue", [(s[:8], round(usd[s], 1), "hist" if s in hist else "-") for s in others if not links.get(s)])
