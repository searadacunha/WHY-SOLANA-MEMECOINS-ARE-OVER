#!/usr/bin/env python3
"""Auditeur D. Allers-retours (A-04) depuis MON parseur d01_own (deltas réels), pas trades.parquet. Règle : pour un même propriétaire, achat suivi d'une vente de même quantité à 1 % près sous 10 s.
Le SOL est lu sur le vault Raydium quand il bouge dans la tx, sinon WSOL+natif du propriétaire. Sortie : d41_roundtrip.txt."""
import collections, json, os, sys
import duckdb
D = "/Volumes/VERBATIM HD/Dark-MAGA-Investigation/audits_work/D"; OUT = "audits/2026-11-03/work_D/"
BIG = "/Volumes/VERBATIM HD/Dark-MAGA-Investigation/data"
con = duckdb.connect(":memory:", config={"memory_limit": "800MB", "threads": 2, "temp_directory": D + "/duck", "preserve_insertion_order": False})
con.execute("SET TimeZone='UTC'")
sys.stdout = open(OUT + "d41_roundtrip.txt", "w")
LOW, ENV, HIGH = 1721588607, 1721589800, 1721590213
# lignes de swap de trades.parquet dédoublonnées, mêmes montants que le rapport ; statut signataire relu dans d01_own
con.execute(f"""CREATE TEMP TABLE s AS SELECT DISTINCT signature,owner,slot,tx_index,block_time t,token_delta d,CASE WHEN token_delta>0 THEN -sol_lamports ELSE sol_lamports END v,venue FROM read_parquet('{BIG}/trades.parquet') WHERE kind='swap'""")
print("lignes swap uniques", con.execute("SELECT count(*),round(sum(CASE WHEN d>0 THEN v ELSE 0 END)/1e9,1) FROM s").fetchone(), flush=True)
cur = con.execute("SELECT owner,slot,tx_index,t,d,v,signature FROM s ORDER BY owner,slot,tx_index")
rt_all = 0.0; rt_owner = collections.Counter(); buy_owner = collections.Counter(); wins = collections.Counter(); wbuy = collections.Counter()
WIN = {"fen_musk_19:03-19:30": (LOW, HIGH + 1), "envoi_19:23-19:30": (ENV, HIGH), "24h_apres": (HIGH, HIGH + 86400), "3h_avant_envoi": (ENV - 10800, ENV), "3h_avant_winig": (1721577749 - 10800, 1721577749), "avant_S_24h": (1721588400 - 86400, 1721588400)}
def proc(rows):
    global rt_all
    open_ = []  # achats encore appariables
    for sl, ix, t, d, v, sg in rows:
        if d > 0:
            buy_owner[own] += v
            for k, (a, z) in WIN.items():
                if a <= t < z: wbuy[k] += v
            open_.append([t, d, v])
        else:
            q = -d
            for b in open_:
                if b[1] and t - b[0] <= 10 and abs(q - b[1]) <= 0.01 * b[1]:
                    rt_all += b[2]; rt_owner[own] += b[2]
                    for k, (a, z) in WIN.items():
                        if a <= b[0] < z: wins[k] += b[2]
                    b[1] = 0
                    break
            open_ = [b for b in open_ if b[1] and t - b[0] <= 10]
own = None; buf = []
while True:
    b = cur.fetchmany(20000)
    if not b: break
    for o, sl, ix, t, d, v, sg in b:
        if o != own:
            if own is not None: proc(buf)
            own, buf = o, []
        buf.append((sl, ix, t, d, v, sg))
proc(buf)
tot = sum(buy_owner.values())
print("achats totaux SOL", round(tot / 1e9, 1), "allers-retours SOL", round(rt_all / 1e9, 1), "part", round(100 * rt_all / tot, 2))
for k in WIN: print(k, "achats", round(wbuy[k] / 1e9, 2), "allers-retours", round(wins[k] / 1e9, 2), "part %", round(100 * wins[k] / max(1, wbuy[k]), 1))
print("top acheteurs (SOL), part aller-retour %, lignes signataire / total (d01_own)")
for o, v in buy_owner.most_common(12):
    r = con.execute(f"SELECT sum(signer::int),count(*) FROM read_parquet('{D}/d01_own.parquet') WHERE owner='{o}'").fetchone()
    print("  ", o, round(v / 1e9, 1), round(100 * rt_owner[o] / v, 1), r)
print("wallets > 50 % d'allers-retours et >= 100 SOL achetés", sum(1 for o, v in buy_owner.items() if v >= 100e9 and rt_owner[o] > .5 * v), "SOL", round(sum(v for o, v in buy_owner.items() if v >= 100e9 and rt_owner[o] > .5 * v) / 1e9, 1))
# fenêtre de Musk : première ligne du tableau d'A
print("achats fen. envoi par propriétaire", con.execute(f"SELECT owner,round(sum(v)/1e9,2),count(*) FROM s WHERE d>0 AND t>={ENV} AND t<{HIGH} GROUP BY 1 ORDER BY 2 DESC LIMIT 6").fetchall())
print("achats 3 h avant envoi", con.execute(f"SELECT owner,round(sum(v)/1e9,2),count(*) FROM s WHERE d>0 AND t>={ENV-10800} AND t<{ENV} GROUP BY 1 ORDER BY 2 DESC LIMIT 5").fetchall())
