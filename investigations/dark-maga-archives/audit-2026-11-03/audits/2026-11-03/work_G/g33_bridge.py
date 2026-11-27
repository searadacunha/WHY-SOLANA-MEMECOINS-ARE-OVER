#!/usr/bin/env python3
"""Arêtes pures entre le bloc G41 (G41vRrsH, NxtXcmEW, GFpqfjEQ et receveurs) et le bloc DfYyxDNE (expéditeurs de 9W9b), toutes dates, avec seuil, nature, soldes. Sortie g33_bridge.csv, stdout."""
import csv, sys, time, collections
sys.path.insert(0, "audits/2026-11-03/work_G")
import duckdb
from dmaga.labels import label
OUT = "audits/2026-11-03/work_G/"; G = "/Volumes/VERBATIM HD/Dark-MAGA-Investigation/audits_work/G/"
iso = lambda t: time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(t))
series = {r["wallet"] for r in csv.DictReader(open("audits/2026-11-03/work_C/cb_series.csv"))}
send9 = {r["sender"] for r in csv.DictReader(open("audits/2026-11-03/work_D/d20_senders.csv"))}
g33 = set(__import__("json").load(open("data/prevent_groups.json"))[0]["members"])
PC = (series | send9) - g33; CR = "8YLEuUtZ4eFMJbf46oNb1CeG6dYFWGyxnQSh9hrgzBzR"
# le créateur et les expéditeurs hors 33 d'un côté, les 33 de l'autre
con = duckdb.connect(":memory:", config={"memory_limit": "500MB", "threads": 2, "temp_directory": G + "duck"})
con.execute("CREATE TABLE a(x VARCHAR)"); con.executemany("INSERT INTO a VALUES (?)", [[x] for x in PC])
con.execute("CREATE TABLE b(x VARCHAR)"); con.executemany("INSERT INTO b VALUES (?)", [[x] for x in g33])
F = f"read_parquet('{G}net_flows.parquet')"
rows = con.execute(f"""SELECT DISTINCT bt,owner,dir,cp,asset,amt,pure,sig FROM {F} WHERE asset IN ('SOL','USDC','USDT','WSOL','DMAGA') AND ((owner IN (SELECT x FROM a) AND cp IN (SELECT x FROM b)) OR (owner IN (SELECT x FROM b) AND cp IN (SELECT x FROM a))) ORDER BY bt""").fetchall()
seen = set(); out = []
for bt, o, d, c, asset, amt, pure, sig in rows:
    s, t = (o, c) if d == "out" else (c, o)
    k = (sig, s, t, asset, amt)
    if k in seen: continue
    seen.add(k); out.append((iso(bt), s, t, asset, amt, pure, sig, "33" if s in g33 else "PC", "33" if t in g33 else "PC"))
w = csv.writer(open(OUT + "g33_bridge.csv", "w", newline="")); w.writerow("utc src dst asset amount pure signature src_set dst_set".split()); w.writerows(out)
real = [r for r in out if (r[3] == "SOL" and r[4] >= 0.01) or (r[3] in ("USDC", "USDT") and r[4] >= 1) or r[3] == "WSOL" and r[4] >= 0.01 or (r[3] == "DMAGA" and r[4] >= 1000)]
print("arêtes entre 33 et périmètre créateur hors 33 :", len(out), "au-dessus de la poussière", len(real))
for r in real: print(" ", r[0], r[1][:8], r[7], "->", r[2][:8], r[8], r[3], round(r[4], 4), "pur" if r[5] else "med", r[6][:14])
