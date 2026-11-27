#!/usr/bin/env python3
"""Ventes de DMAGA par ordre Jupiter DCA : escrow = adresse qui reçoit les jetons dans une tx du programme DCA265Vj signée par le wallet ; encaissements = stables et SOL reçus de cet escrow. Sorties g52.txt, g52_orders.csv, g52_receipts.csv (wallet, utc, sol_eq)."""
import csv, gzip, json, sys, time, collections
import duckdb
OUT = "audits/2026-11-03/work_G/"; G = "/Volumes/VERBATIM HD/Dark-MAGA-Investigation/audits_work/G/"
sys.stdout = open(OUT + "g52.txt", "w")
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
DCA = "DCA265Vj8a9CEuX1eb1LWRnDT7uK6q1xMipnNyatn23M"
dsig = set()
for l in csv.DictReader(gzip.open(G + "net_txs.csv.gz", "rt")):
    if DCA in l["programs"] and l["err"] == "0" and l["signed"] == "1": dsig.add((l["owner"], l["sig"]))
con = duckdb.connect(":memory:", config={"memory_limit": "400MB", "threads": 2, "temp_directory": G + "duck"})
con.execute("CREATE TABLE d(o VARCHAR, s VARCHAR)"); con.executemany("INSERT INTO d VALUES (?,?)", list(dsig))
op = con.execute(f"""SELECT f.owner,f.cp,sum(f.amt),min(f.bt),min(f.sig) FROM '{G}net_flows.parquet' f JOIN d ON d.o=f.owner AND d.s=f.sig WHERE f.dir='out' AND f.asset='DMAGA' AND f.amt>=1000 GROUP BY 1,2 ORDER BY 4""").fetchall()
w = csv.writer(open(OUT + "g52_orders.csv", "w", newline="")); w.writerow("wallet escrow jetons ouverture signature p1 g33 encaisse_sol_eq n_encaissements premier dernier".split())
rw = csv.writer(open(OUT + "g52_receipts.csv", "w", newline="")); rw.writerow("wallet utc bt sol_eq asset amount escrow".split())
tot = collections.Counter()
MUSK_END = 1721590213
win = collections.Counter()
for o, e, q, bt, s in op:
    rec = con.execute(f"""SELECT bt,asset,amt,sig FROM '{G}net_flows.parquet' WHERE owner=? AND cp=? AND dir='in' AND asset IN ('SOL','WSOL','USDC','USDT') AND amt>0 ORDER BY bt""", [o, e]).fetchall()
    eq = 0.0
    for b, a, amt, sg in rec:
        v = amt if a in ("SOL", "WSOL") else amt / px(b)
        if a == "SOL" and amt < 0.01: continue  # rent et poussière d'escrow
        eq += v; rw.writerow([o, iso(b), b, round(v, 6), a, amt, e])
        if o in P1:
            if MUSK_END <= b < MUSK_END + 86400: win["24h_apres"] += v
            if b < MUSK_END: win["avant_19h30"] += v
    w.writerow([o, e, q, iso(bt), s, o in P1, o in g33, round(eq, 4), len(rec), iso(rec[0][0]) if rec else "", iso(rec[-1][0]) if rec else ""])
    k = "P1" if o in P1 else "hors_P1"
    tot[k + "_jetons"] += q; tot[k + "_ordres"] += 1; tot[k + "_sol_eq"] += eq
print("ordres DCA vendant DMAGA", len(op), {k: round(v, 1) for k, v in tot.items()})
print("P1, encaissé par DCA : avant 19:30:13 le 21/07", round(win["avant_19h30"], 1), "; 24 h après", round(win["24h_apres"], 1))
# 21-22/07
for o, e, q, bt, s in op:
    if o in P1 and bt < MUSK_END + 2 * 86400: print(" ", iso(bt), o[:8], "jetons", round(q), "série" if o in series else "", s[:14])
