#!/usr/bin/env python3
"""Point 4. Jonctions entre les gagnants (et leurs wallets suivants) et les périmètres : arêtes directes, puis contreparties communes rares (au plus 10 adresses tracées, non étiquetées, non service). Population du dépôt H9Xezqfd. Sortie g46.txt, g46_common.csv."""
import csv, json, sys, time, collections
import duckdb
from dmaga.labels import label
from dmaga.venues import load as lv
OUT = "audits/2026-11-03/work_G/"; G = "/Volumes/VERBATIM HD/Dark-MAGA-Investigation/audits_work/G/"
sys.stdout = open(OUT + "g46.txt", "w")
iso = lambda t: time.strftime("%Y-%m-%d", time.gmtime(t))
H3 = "H3QsBrrivimFJmSpTXuvig2n1Bh7JuYxrriRSEszT6cc"; GX = "GXZvXsD6hxaLeFvQisWpdAwsayJxga7w9EeafhFZG2Ra"; P9 = "9PrmF8sfoD2YShtWUghrGEYgxwabpnzog8gT1V6LEtdq"
series = {r["wallet"] for r in csv.DictReader(open("audits/2026-11-03/work_C/cb_series.csv"))}
g33 = set(json.load(open("data/prevent_groups.json"))[0]["members"])
inp = list(csv.DictReader(open(OUT + "g30_in.csv")))
S = collections.defaultdict(set)
for r in inp: S[r["depot"][:4]].add(r["sender"])
W = {"H3QsBr": {H3, "8YSi5yNRN2KMbGU7Q3i5w9W6fTRxnk1qatQ5YmzS5da7", "AGG2FsrpP4wN6hjptovXH3sykfdMt6ESADJGLxMYKcJZ", "E1wDwfkh1ySipYTgqx6DtCQrri2L8KCwzECC3arUMXyK", "BZ2UcCujoCr4XYZE2s23xTWYJMgiFSQoYopYrr1B2QmA", "5QbApAquHTJ2waLG2VXNctdF1a1QUvsmwTHew4pmnwG5", "nbL5GccMxEgEJECJ5C4SqhLWuyXW2GbW13ctLF9JXGQ"},
     "GXZvX": {GX, "Co3zTr2M8huMY5os2wuvKGP4x3S3q4D9fzAoMZeGSMbb", "AverrTRTKkP8SH4LHCiRKyvEMHoJGyCpkG1Bk2RJQYSp", "FB8241Dxskd2CiSsNC3aB6gsSMPmsxpJKwJRaUj4G2o5"} | S["42MS"] | S["9kqT"] | S["8N4A"],
     "9PrmF8": {P9} | S["H9Xe"]}
W["GXZvX"] -= {"ASTyfSima4LLAdDgoFGkgqoKowG1LZFDr9fAQrg7iaJZ"}  # hot wallet MEXC 1, pas un wallet du périmètre
P = (series | g33 | S["9W9b"] | S["Caw4"] | S["AQVg"] | S["By6D"] | {"8YLEuUtZ4eFMJbf46oNb1CeG6dYFWGyxnQSh9hrgzBzR"}) - {"59L2oxymiQQ9Hvhh92nt8Y7nDYjsauFkdb3SybdnsG6h"}
for k, v in W.items(): print(k, "wallets", len(v), "dans le périmètre P", sorted(x[:8] for x in v & P))
con = duckdb.connect(":memory:", config={"memory_limit": "800MB", "threads": 2, "temp_directory": G + "duck", "preserve_insertion_order": False})
con.execute("SET TimeZone='UTC'")
SOLM = "So11111111111111111111111111111111111111111"; UC = "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"; UT = "Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB"; DM = "7D7BRcBYepfi77vxySapmeqRNN1wsBBxnFPJGbH5pump"
con.execute("CREATE TABLE s(a VARCHAR, g VARCHAR)")
for k, v in W.items(): con.executemany("INSERT INTO s VALUES (?,?)", [[a, k] for a in v])
con.executemany("INSERT INTO s VALUES (?,?)", [[a, "P"] for a in P])
con.execute(f"""CREATE TABLE e AS SELECT DISTINCT sig,bt,src,dst,mint,raw FROM read_parquet('{G}flows_all.parquet') WHERE (src IN (SELECT a FROM s) OR dst IN (SELECT a FROM s)) AND src<>dst AND ((mint='{SOLM}' AND raw>=10000000) OR (mint IN ('{UC}','{UT}') AND raw>=1000000) OR (mint='{DM}' AND raw>=1000000000))""")
con.execute(f"""INSERT INTO e SELECT sig,bt,CASE WHEN dir='out' THEN owner ELSE cp END,CASE WHEN dir='out' THEN cp ELSE owner END,CASE asset WHEN 'SOL' THEN '{SOLM}' WHEN 'USDC' THEN '{UC}' WHEN 'USDT' THEN '{UT}' ELSE '{DM}' END,round(amt*CASE asset WHEN 'SOL' THEN 1e9 ELSE 1e6 END) FROM read_parquet('{G}net_flows.parquet') WHERE pure=1 AND asset IN ('SOL','USDC','USDT','DMAGA') AND (owner IN (SELECT a FROM s)) AND ((asset='SOL' AND amt>=0.01) OR (asset IN ('USDC','USDT') AND amt>=1) OR (asset='DMAGA' AND amt>=1000))""")
print("arêtes", con.execute("SELECT count(*) FROM e").fetchone())
for k in W:
    r = con.execute(f"""SELECT DISTINCT src,dst,mint,raw,bt,sig FROM e WHERE (src IN (SELECT a FROM s WHERE g='{k}') AND dst IN (SELECT a FROM s WHERE g='P')) OR (dst IN (SELECT a FROM s WHERE g='{k}') AND src IN (SELECT a FROM s WHERE g='P'))""").fetchall()
    print(k, "arêtes directes avec P :", len(r))
    for x in r[:12]: print("   ", iso(x[4]), x[0], "->", x[1], x[2][:5], x[3], x[5][:18])
    r2 = con.execute(f"""SELECT DISTINCT src,dst,mint,raw,bt,sig FROM e WHERE (src IN (SELECT a FROM s WHERE g='{k}') AND dst IN (SELECT a FROM s WHERE g<>'{k}' AND g<>'P')) OR (dst IN (SELECT a FROM s WHERE g='{k}') AND src IN (SELECT a FROM s WHERE g<>'{k}' AND g<>'P'))""").fetchall()
    print(k, "arêtes directes avec un autre gagnant :", len(r2), [(iso(x[4]), x[0][:8], x[1][:8]) for x in r2[:6]])
# contreparties communes rares : X touche au moins un wallet de W et au moins un de P
ven = set(lv()) | {"5Q544fKrFoe6tsEbD7S8EmxGTJYAKtTVhAW5Q5pge4j1"}
POP = {r["dst"]: int(r["n_senders"]) for r in csv.DictReader(open(OUT + "g10_dest.csv"))}
pop = collections.Counter(); byX = collections.defaultdict(lambda: collections.defaultdict(list))
Wall = {a: k for k, v in W.items() for a in v}
for src, dst, mint, raw, bt, sig in con.execute("SELECT DISTINCT src,dst,mint,raw,bt,sig FROM e").fetchall():
    for a, x in ((src, dst), (dst, src)):
        if a in Wall or a in P:
            if x in Wall or x in P: continue
            byX[x][a].append((iso(bt), mint[:5], raw, sig))
rows = []
for x, d in byX.items():
    wk = {Wall[a] for a in d if a in Wall}; hp = [a for a in d if a in P]
    if not wk or not hp: continue
    if x in ven or label(x) or len(d) > 10 or POP.get(x, 0) >= 15: continue  # 15 expéditeurs tracés ou plus : service ou pool
    rows.append((x, sorted(wk), len(hp), len(d), d))
print("contreparties communes rares, non étiquetées, au plus 10 wallets :", len(rows))
w = csv.writer(open(OUT + "g46_common.csv", "w", newline="")); w.writerow("contrepartie gagnant_cote wallets_P wallets_total detail".split())
for x, wk, nh, nd, d in sorted(rows, key=lambda r: r[3]):
    det = {a[:8]: [(q[0], q[1], q[2]) for q in v[:2]] for a, v in d.items()}
    w.writerow([x, "|".join(wk), nh, nd, json.dumps(det)[:600]])
    print("  ", x, wk, "P", nh, "total", nd, str(det)[:230])
# Population de H9Xe
print("H9Xe : expéditeurs", sorted(S["H9Xe"]))
d = con.execute(f"""SELECT a,sum(CASE WHEN dst=a THEN raw ELSE 0 END)/1e6,sum(CASE WHEN src=a THEN raw ELSE 0 END)/1e6,min(bt) FROM (SELECT x.a,y.* FROM (SELECT unnest(?) a) x JOIN (SELECT DISTINCT sig,bt,src,dst,raw,ins,inner_ FROM read_parquet('{G}flows_all.parquet') WHERE mint='{DM}') y ON y.src=x.a OR y.dst=x.a) GROUP BY 1""", [list(S["H9Xe"])]).fetchall()
for r in d: print("   DMAGA", r[0][:8], "reçus M", round(r[1] / 1e6, 2), "sortis M", round(r[2] / 1e6, 2), "premier", iso(r[3]))
