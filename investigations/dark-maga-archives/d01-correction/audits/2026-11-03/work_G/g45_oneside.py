#!/usr/bin/env python3
"""Sorties de valeur sans contrepartie reçue par le wallet, par programme : valeur nette (SOL natif, WSOL, USD stables) négative d'au moins 0,1 SOL éq., aucun autre jeton reçu, DMAGA inchangé. Cherche ponts, mixeurs, escrows, prêts. Sortie g45.txt."""
import csv, gzip, sys, time, collections
OUT = "audits/2026-11-03/work_G/"; G = "/Volumes/VERBATIM HD/Dark-MAGA-Investigation/audits_work/G/"
sys.stdout = open(OUT + "g45.txt", "w")
price = {r["date"]: float(r["close"]) for r in csv.DictReader(open(OUT + "sol_daily.csv"))}
def px(bt):
    d = time.strftime("%Y-%m-%d", time.gmtime(bt))
    return price.get(d) or (price[min(price)] if d < min(price) else price[max(price)])
T = {r["wallet"] for r in csv.DictReader(open(OUT + "targets.csv"))}
P = collections.defaultdict(lambda: [0, 0.0, set(), None])
tot = 0.0
for l in csv.DictReader(gzip.open(G + "net_txs.csv.gz", "rt")):
    if l["owner"] not in T or l["err"] != "0" or l["pure"] == "1" or l["signed"] != "1": continue
    if int(l["dmaga_delta"]) != 0 or int(l["n_other_mints"]) != 0: continue
    bt = int(l["bt"]); v = -(int(l["native_delta"]) + int(l["wsol_delta"])) / 1e9 - (int(l["usdc_delta"]) + int(l["usdt_delta"])) / 1e6 / px(bt)
    if v < 0.1: continue
    tot += v
    for p in l["programs"].split(";"):
        e = P[p]; e[0] += 1; e[1] += v; e[2].add(l["owner"]); e[3] = e[3] or l["sig"]
print("valeur totale", round(tot, 1))
for p, e in sorted(P.items(), key=lambda kv: -kv[1][1])[:30]:
    print(p, "tx", e[0], "SOL éq.", round(e[1], 1), "wallets", len(e[2]), "ex", e[3])
