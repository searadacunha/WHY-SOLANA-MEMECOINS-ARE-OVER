#!/usr/bin/env python3
"""HW5MqvM1, fenêtre 15 au 31/07/2024 : réception de 1,5 M, revente, SOL. Destinataires externes de DMAGA de la série. Sortie g49.txt"""
import csv, sys, time, json, collections
sys.path.insert(0, "audits/2026-11-03/work_G")
import duckdb
from g_lib import parse, NETG
import gzip
G = "/Volumes/VERBATIM HD/Dark-MAGA-Investigation/audits_work/G/"; OUT = "audits/2026-11-03/work_G/"
sys.stdout = open(OUT + "g49.txt", "w")
iso = lambda t: time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(t))
HW = "HW5MqvM1kDySFUtynMtzsWCU6VcFfpeCXsbRyLq6iHk6"
for l in gzip.open(NETG + HW + ".win.jsonl.gz", "rt"):
    x = parse(json.loads(l))
    mv = [(a if a != "other" else m[:6], (s or "")[:8], (d or "")[:8], round(r / 10 ** (dc or 0), 3)) for k, a, m, s, d, r, dc in x["moves"] if (a == "SOL" and r >= 100_000_000) or a in ("DMAGA", "USDC", "USDT") or (a == "WSOL" and r >= 100_000_000)]
    if any(q[0] == "DMAGA" for q in mv) or any(q[0] == "SOL" for q in mv): print(" ", iso(x["bt"]), x["sig"][:14], "signe" if HW in x["signers"] else "-", mv[:4])
series = {r["wallet"] for r in csv.DictReader(open("audits/2026-11-03/work_C/cb_series.csv"))}
send9 = {r["sender"] for r in csv.DictReader(open("audits/2026-11-03/work_D/d20_senders.csv"))}
g33 = set(json.load(open("data/prevent_groups.json"))[0]["members"])
inp = list(csv.DictReader(open(OUT + "g30_in.csv"))); D = collections.defaultdict(set)
for r in inp: D[r["sender"]].add(r["depot"][:4])
con = duckdb.connect(":memory:", config={"memory_limit": "300MB", "threads": 1, "temp_directory": G + "duck"})
con.execute("CREATE TABLE s(a VARCHAR)"); con.executemany("INSERT INTO s VALUES (?)", [[a] for a in series])
rows = con.execute(f"SELECT owner,cp,sum(amt),min(bt),min(sig) FROM '{G}net_flows.parquet' WHERE owner IN (SELECT a FROM s) AND dir='out' AND asset='DMAGA' AND pure=1 AND amt>=1000 GROUP BY 1,2 ORDER BY 3 DESC").fetchall()
ext = [r for r in rows if r[1] not in series and r[1] not in send9 and r[1] not in g33]
print("transferts DMAGA purs de la série 15 : destinataires", len({r[1] for r in rows}), "hors série, expéditeurs 9W9b et 33 :", len({r[1] for r in ext}), "jetons M", round(sum(r[2] for r in ext) / 1e6, 2))
for r in ext: print(" ", r[0][:8], "->", r[1], round(r[2] / 1e6, 3), iso(r[3]), "dépôts utilisés", sorted(D.get(r[1], [])), r[4][:14])
