#!/usr/bin/env python3
"""Point 3. Entrées des comptes de dépôt : par date, par wallet, part liée au jeton, recouvrements, séance commune, salves. Lit les historiques (g_lib), net_txs, d01_own. Sorties : g30_in.csv, g30_overlap.csv, g30_by_month.csv, g30_by_wallet.csv, g30.txt."""
import csv, gzip, itertools, random, sys, time, collections
sys.path.insert(0, "audits/2026-11-03/work_G")
import duckdb
from g_lib import history, parse, CB, FAM
OUT = "audits/2026-11-03/work_G/"; G = "/Volumes/VERBATIM HD/Dark-MAGA-Investigation/audits_work/G/"; D_ = "/Volumes/VERBATIM HD/Dark-MAGA-Investigation/audits_work/D/"
sys.stdout = open(OUT + "g30.txt", "w")
DEP = {"9W9b": "9W9b3zgHH9mCEHDhsdbnbEPHStm9vvXS4aia4DWHBxpL", "Caw4": "Caw4RrwkmxqtbLSFzgSs6id3XiFxWQxs2t1mrn5a3mME", "AQVg": "AQVgyg8P5Yh5YcAqAMQRRGzDegy1R58gN4Qh87QsJAF1", "By6D": "By6Dao4QMNeBxmdUrqsoQA8dCGbHz7xWj57CdHV5M47r",
       "H9Xe": "H9XezqfdXuv4ZCHAAZ92oMLSSAPB6Dgm4ZSrRythCbPi", "42MS": "42MSVeV4YbESE7mNW7DfQrfd8E4RG6njxXZLAWTmXemv", "9kqT": "9kqTVnRUkVTFD7na9BTWcoG9piL4XpVTtS9kqVCV56tV", "8N4A": "8N4AvP9j5BditSQMk2WrTNxthhgpncGVzLKrYP4xdEqx"}
MINT_T = 1720922725
price = {r["date"]: float(r["close"]) for r in csv.DictReader(open(OUT + "sol_daily.csv"))}
def px(bt):
    d = time.strftime("%Y-%m-%d", time.gmtime(bt))
    return price.get(d) or price[min(price, key=lambda k: abs(time.mktime(time.strptime(k, "%Y-%m-%d")) - bt))]
iso = lambda t: time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(t))
roles = {r["wallet"]: r["roles"] for r in csv.DictReader(open(OUT + "targets.csv"))}
rows = []
for k, A in DEP.items():
    for t in history(A):
        x = parse(t)
        if x["err"]: continue
        for kind, asset, mint, s, d, raw, dec in x["moves"]:
            if d == A and s != A and ((asset == "SOL" and raw >= 1_000_000) or (asset in ("USDC", "USDT") and raw >= 1_000_000) or (asset == "DMAGA" and raw >= 1_000_000)):
                amt = raw / 1e9 if asset == "SOL" else raw / 1e6
                eq = amt if asset == "SOL" else (amt / px(x["bt"]) if asset != "DMAGA" else 0.0)
                rows.append(dict(dep=k, depot=A, sender=s, asset=asset, amt=amt, eq=eq, bt=x["bt"], sig=x["sig"], pure=x["pure"], signer=";".join(x["signers"])[:88]))
rows.sort(key=lambda r: r["bt"])
with open(OUT + "g30_in.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow("depot sender asset amount sol_eq utc signature pure signed_by_sender roles".split())
    for r in rows: w.writerow([r["depot"], r["sender"], r["asset"], r["amt"], round(r["eq"], 6), iso(r["bt"]), r["sig"], r["pure"], r["sender"] in r["signer"].split(";"), roles.get(r["sender"], "")])
sen = collections.defaultdict(set)
for r in rows: sen[r["dep"]].add(r["sender"])
print("expéditeurs par dépôt", {k: len(v) for k, v in sen.items()})
with open(OUT + "g30_overlap.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow("a b n_commun communs".split())
    for a, b in itertools.combinations(DEP, 2):
        c = sen[a] & sen[b]
        w.writerow([a, b, len(c), ";".join(sorted(c))])
        print(f"  recouvrement {a} {b} : {len(c)}", sorted(x[:8] for x in c)[:30])
con = duckdb.connect(":memory:", config={"memory_limit": "500MB", "threads": 2, "temp_directory": G + "duck"})
allsen = {r["sender"] for r in rows}
con.execute("CREATE TABLE q(a VARCHAR)"); con.executemany("INSERT INTO q VALUES (?)", [[a] for a in allsen])
touch = {r[0] for r in con.execute(f"SELECT DISTINCT owner FROM '{D_}d01_own.parquet' WHERE owner IN (SELECT a FROM q)").fetchall()}
# ventes DMAGA de chaque expéditeur, depuis net_txs (historique local seulement)
sales = collections.defaultdict(list); hist = set()
for l in csv.DictReader(gzip.open(G + "net_txs.csv.gz", "rt")):
    if l["owner"] in allsen:
        hist.add(l["owner"])
        if int(l["dmaga_delta"]) < 0 and l["err"] == "0" and l["pure"] == "0":
            bt = int(l["bt"]); got = int(l["native_delta"]) / 1e9 + int(l["wsol_delta"]) / 1e9 + (int(l["usdc_delta"]) + int(l["usdt_delta"])) / 1e6 / px(bt)
            if got > 0: sales[l["owner"]].append((bt, got))
import os
if os.path.exists(OUT + "g52_receipts.csv"):  # encaissements des ordres DCA vendant DMAGA : même plancher
    for l in csv.DictReader(open(OUT + "g52_receipts.csv")):
        if l["wallet"] in allsen: sales[l["wallet"]].append((int(l["bt"]), float(l["sol_eq"])))
    for k_ in sales: sales[k_].sort()
print("expéditeurs : avec historique local", len(hist), "sur", len(allsen))
# part liée : plancher = deposit couvert par les ventes DMAGA antérieures du même wallet ; plafond = tout versement post-mint d'un wallet touchant DMAGA ; non mesurable si pas d'historique
res = collections.defaultdict(lambda: collections.Counter()); per_wallet = collections.defaultdict(lambda: collections.Counter())
rem = collections.defaultdict(float); idx = collections.Counter()
for r in rows:
    s, k, a = r["sender"], r["dep"], r["eq"]
    if r["asset"] == "DMAGA": res[k]["DMAGA_jetons"] += r["amt"]; continue
    L = sales.get(s, [])
    while idx[s] < len(L) and L[idx[s]][0] < r["bt"]:
        rem[s] += L[idx[s]][1]; idx[s] += 1
    res[k]["total"] += a; per_wallet[(k, s)]["total"] += a; per_wallet[(k, s)]["n"] += 1
    if r["bt"] < MINT_T: res[k]["avant_mint"] += a; per_wallet[(k, s)]["avant_mint"] += a; continue
    if s in touch: res[k]["post_touche"] += a
    else: res[k]["post_ne_touche_pas"] += a
    lien = min(a, rem[s]); rem[s] -= lien
    res[k]["lie_plancher"] += lien; per_wallet[(k, s)]["lie_plancher"] += lien
for k in DEP:
    c = res[k]
    print(f"{k} total {c['total']:.2f} SOL éq. ; avant mint {c['avant_mint']:.2f} ; après mint expéditeur touche DMAGA {c['post_touche']:.2f} (plafond lié) ; dont couvert par ses ventes antérieures {c['lie_plancher']:.2f} (plancher lié) ; après mint expéditeur ne touche pas {c['post_ne_touche_pas']:.2f} ; DMAGA reçus {c['DMAGA_jetons']:.0f}")
    S = sen[k]; print(f"   expéditeurs {len(S)}, touchent DMAGA {len(S & touch)}, hors {sum(1 for x in S if x in roles)} cibles {len(S - set(roles))} dont touchent {len((S - set(roles)) & touch)}")
with open(OUT + "g30_by_wallet.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow("depot sender n sol_eq avant_mint lie_plancher touche_dmaga historique_local roles".split())
    for (k, s), c in sorted(per_wallet.items(), key=lambda kv: (kv[0][0], -kv[1]["total"])):
        w.writerow([DEP[k], s, c["n"], round(c["total"], 4), round(c["avant_mint"], 4), round(c["lie_plancher"], 4), s in touch, s in hist, roles.get(s, "")])
mon = collections.Counter(); nmon = collections.defaultdict(set)
for r in rows:
    if r["asset"] == "DMAGA": continue
    m = iso(r["bt"])[:7]; mon[(r["dep"], m)] += r["eq"]; nmon[(r["dep"], m)].add(r["sender"])
with open(OUT + "g30_by_month.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow("depot mois sol_eq n_expediteurs".split())
    for (k, m), v in sorted(mon.items()): w.writerow([DEP[k], m, round(v, 3), len(nmon[(k, m)])])
for k in ("9W9b", "Caw4"):
    print(k, "par mois", [(m[1], round(v, 1), len(nmon[m])) for m, v in sorted(mon.items()) if m[0] == k])
# salves : au moins 3 expéditeurs distincts en 30 min
for k in ("Caw4", "9W9b", "AQVg", "By6D"):
    R = [r for r in rows if r["dep"] == k and r["asset"] != "DMAGA"]
    i = 0; bursts = []
    while i < len(R):
        j = i
        while j + 1 < len(R) and R[j + 1]["bt"] - R[i]["bt"] <= 1800: j += 1
        ss = {x["sender"] for x in R[i:j + 1]}
        if len(ss) >= 3:
            bursts.append((iso(R[i]["bt"]), iso(R[j]["bt"])[11:], len(ss), round(sum(x["amt"] for x in R[i:j + 1]), 2), sorted(a[:6] for a in ss)[:14])); i = j + 1
        else: i += 1
    print(k, "salves >=3 en 30 min", bursts)
# séance commune : pour chaque wallet versant à 9W9b et à Caw4, écart minimal entre versements
T9 = collections.defaultdict(list); TC = collections.defaultdict(list)
for r in rows:
    if r["dep"] == "9W9b": T9[r["sender"]].append(r["bt"])
    if r["dep"] == "Caw4": TC[r["sender"]].append(r["bt"])
com = sorted(set(T9) & set(TC))
def mingap(a, b): return min(abs(x - y) for x in a for y in b)
gaps = {s: mingap(T9[s], TC[s]) for s in com}
n15 = sum(1 for v in gaps.values() if v <= 900); n60 = sum(1 for v in gaps.values() if v <= 3600); nd = sum(1 for v in gaps.values() if v <= 86400)
print("communs 9W9b et Caw4", len(com), "écart minimal <=15 min", n15, "<=1 h", n60, "<=24 h", nd, "sur", len(gaps))
rng = random.Random(20261103); N = 5000; ge = [0, 0, 0]; sumstat = [0, 0, 0]
keys = com[:]
for _ in range(N):
    p = keys[:]; rng.shuffle(p)
    g = [mingap(T9[a], TC[b]) for a, b in zip(keys, p)]
    v = (sum(1 for x in g if x <= 900), sum(1 for x in g if x <= 3600), sum(1 for x in g if x <= 86400))
    for i in range(3):
        sumstat[i] += v[i]; ge[i] += v[i] >= (n15, n60, nd)[i]
print("permutation des wallets (même calendrier global), moyenne <=15 min, <=1 h, <=24 h", [round(x / N, 2) for x in sumstat], "P(>= observé)", [(g + 1) / (N + 1) for g in ge])
# 23/07/2024 : les 4 de la salve vers 9W9b
for r in rows:
    if r["dep"] == "9W9b" and iso(r["bt"]).startswith("2024-07-23"): print("  salve 23/07", iso(r["bt"]), r["sender"], r["amt"], r["sig"])
