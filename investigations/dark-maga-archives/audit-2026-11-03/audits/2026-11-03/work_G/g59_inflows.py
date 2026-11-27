#!/usr/bin/env python3
"""Entrées par périmètre (virements purs reçus de hot wallets, de la famille présumée, d'autres), retraits après le mint, ventes DCA des deux membres des 33 présents dans P1 sur 24 h, premières ventes de C73Yv9iH, exemples de blocs du programme 3GMsedVP. Sortie g59.txt."""
import csv, json, sys, time, collections
import duckdb
from dmaga.labels import label
OUT = "audits/2026-11-03/work_G/"; G = "/Volumes/VERBATIM HD/Dark-MAGA-Investigation/audits_work/G/"; A = "/Volumes/VERBATIM HD/Dark-MAGA-Investigation/audits_work/A/"
sys.stdout = open(OUT + "g59.txt", "w")
iso = lambda t: time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(t))
price = {r["date"]: float(r["close"]) for r in csv.DictReader(open(OUT + "sol_daily.csv"))}
def px(bt):
    d = time.strftime("%Y-%m-%d", time.gmtime(bt))
    return price.get(d) or (price[min(price)] if d < min(price) else price[max(price)])
series = {r["wallet"] for r in csv.DictReader(open("audits/2026-11-03/work_C/cb_series.csv"))}
send9 = {r["sender"] for r in csv.DictReader(open("audits/2026-11-03/work_D/d20_senders.csv"))}
g33 = set(json.load(open("data/prevent_groups.json"))[0]["members"])
SAL = {"G41vRrsHShLEvwMj58ruhqJycGfAtWXxtLD56uFExL8E", "C73Yv9iHmTaf8SU2XFnGLt7QXUDqbeWNtUYza9WJhkae", "AtZjv3DuV9cLn3Jxm72TMSdTN4aM6CrBaGyxUC4c2wDk", "EGtyQEgMKGKXjppDqj9sYy97e9m7nvu1US4SfFXNakMy"}
P1 = (series | send9 | {"8YLEuUtZ4eFMJbf46oNb1CeG6dYFWGyxnQSh9hrgzBzR"}) - SAL
P2 = (g33 | SAL) - P1
FAM = {"FpwQQhQQoEaVu3WU2qZMfF1hx48YyfwsLoRgXG83E99Q", "D89hHJT5Aqyx1trP6EnGY9jJUB3whgnq3aUvvCqedvzf", "DPqsobysNf5iA9w7zrQM8HLzCKZEDMkZsWbiidsAt1xo", "5g7yNHyGLJ7fiQ9SN9mf47opDnMjc585kqXWt6d7aBWs", "9obNtb5GyUegcs3a1CbBkLuc5hEWynWfJC6gjz5uWQkE", "4NyK1AdJBNbgaJ9EsKz3J4rfeHsuYdjkTPg3JaNdLeFw", "8JUEoHNMbWM4eegcMvx6ZQJt3V3fbo8JNjpWiCtJgxfF", "AafGzY9eiC5Ud3YFZQwkaKApp48cVBAT2kksGvEjhUvH"}
MINT = 1720922725
con = duckdb.connect(":memory:", config={"memory_limit": "700MB", "threads": 2, "temp_directory": G + "duck", "preserve_insertion_order": False})
con.execute("SET TimeZone='UTC'")
for name, S in (("P1", P1), ("P2", P2), ("H3QsBr", {"H3QsBrrivimFJmSpTXuvig2n1Bh7JuYxrriRSEszT6cc"}), ("GXZvX", {"GXZvXsD6hxaLeFvQisWpdAwsayJxga7w9EeafhFZG2Ra"}), ("9PrmF8", {"9PrmF8sfoD2YShtWUghrGEYgxwabpnzog8gT1V6LEtdq"})):
    con.execute("CREATE OR REPLACE TEMP TABLE s(a VARCHAR)"); con.executemany("INSERT INTO s VALUES (?)", [[a] for a in S])
    rows = con.execute(f"SELECT cp,asset,amt,bt FROM '{G}net_flows.parquet' WHERE owner IN (SELECT a FROM s) AND dir='in' AND pure=1 AND asset IN ('SOL','USDC','USDT') AND ((asset='SOL' AND amt>=0.01) OR (asset<>'SOL' AND amt>=1)) AND cp NOT IN (SELECT a FROM s)").fetchall()
    c = collections.Counter(); pre = collections.Counter(); top = collections.Counter()
    for cp, asset, amt, bt in rows:
        v = amt if asset == "SOL" else amt / px(bt); l = label(cp) or ""
        k = "hot wallet étiqueté" if l and "Jupiter" not in l and "Raydium" not in l else ("famille présumée" if cp in FAM else "wallet ou service sans étiquette")
        c[k] += v
        if bt < MINT: pre[k] += v
        if k == "hot wallet étiqueté": top[l] += v
    print(name, "entrées pures externes SOL éq.", {k: round(v, 1) for k, v in c.most_common()}, "dont avant mint", {k: round(v, 1) for k, v in pre.most_common()}, "par étiquette", [(k, round(v, 1)) for k, v in top.most_common(5)])
# DCA des deux membres des 33 présents dans P1
E = 1721590213
rec = list(csv.DictReader(open(OUT + "g52_receipts.csv")))
for a in ("5QhJJcFZu2ashyKyWSTGHcsyo6ZBCbpVuJqeutvQHScd", "7FGoCB63x3FAJNF25MMZG8pheR4rRtJbApQuynJRxLdE"):
    print("DCA", a[:8], "24 h", round(sum(float(r["sol_eq"]) for r in rec if r["wallet"] == a and E <= int(r["bt"]) < E + 86400), 2), "toutes dates", round(sum(float(r["sol_eq"]) for r in rec if r["wallet"] == a), 2))
ser = sum(float(r["sol_eq"]) for r in rec if r["wallet"] in series and E <= int(r["bt"]) < E + 86400); print("DCA série 15, 24 h", round(ser, 1))
# C73Yv9iH : ventes le 21-22/07
C7 = "C73Yv9iHmTaf8SU2XFnGLt7QXUDqbeWNtUYza9WJhkae"
r = con.execute(f"SELECT bt,dmaga_delta,native_delta,wsol_delta,sig FROM read_csv('{G}net_txs.csv.gz',header=true,types={{'sig':'VARCHAR','owner':'VARCHAR','programs':'VARCHAR','signers':'VARCHAR','payer':'VARCHAR'}}) WHERE owner=? AND dmaga_delta<0 AND pure=0 AND err=0 ORDER BY bt LIMIT 3", [C7]).fetchall()
print("C73Yv9iH premières ventes", [(iso(x[0]), round(x[1] / 1e12, 3), round((x[2] + x[3]) / 1e9, 2), x[4]) for x in r])
# exemples de blocs du programme
SVC = "3GMsedVPsXjWR7HYUvwm1YUpvBC2bTgSkXixm4gMXnPk"
con.execute(f"CREATE TEMP TABLE st AS SELECT signature FROM '{A}a15_tx.parquet' WHERE progs LIKE '%{SVC}%'")
ex = con.execute(f"SELECT signature,owner,slot,tx_index,dmaga,sol FROM '{A}a15_leg.parquet' WHERE signature IN (SELECT signature FROM st) ORDER BY abs(sol) DESC LIMIT 1").fetchone()
for r in con.execute(f"SELECT signature,owner,slot,tx_index,dmaga/1e6,sol/1e9 FROM '{A}a15_leg.parquet' WHERE slot=? AND signature IN (SELECT signature FROM st) ORDER BY tx_index", [ex[2]]).fetchall(): print("  bloc", r)
a0 = con.execute(f"SELECT min(tx_index),max(tx_index) FROM '{A}a15_leg.parquet' WHERE slot=? AND signature IN (SELECT signature FROM st)", [ex[2]]).fetchone()
for r in con.execute(f"SELECT signature,owner,tx_index,dmaga/1e6,sol/1e9 FROM '{A}a15_leg.parquet' WHERE slot=? AND tx_index>? AND tx_index<? AND signature NOT IN (SELECT signature FROM st)", [ex[2], a0[0], a0[1]]).fetchall(): print("  tiers", r)
