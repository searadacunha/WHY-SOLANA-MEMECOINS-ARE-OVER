#!/usr/bin/env python3
"""Table des frontières et flow_boundaries.csv. Une ligne par flux (source, destination, actif). Lit net_flows (virements purs, historique C et G), flows_all (au-delà du dernier instant couvert pour les historiques tronqués), g30_in (entrées des dépôts).
Classe chaque destination, sans continuité à travers un échange. Sorties : flow_boundaries.csv, g40.txt, g40_p1_wallets.csv."""
import csv, json, os, sys, time, collections, gzip
import duckdb
from dmaga.labels import label
from dmaga.venues import load as lv
OUT = "audits/2026-11-03/work_G/"; G = "/Volumes/VERBATIM HD/Dark-MAGA-Investigation/audits_work/G/"
sys.stdout = open(OUT + "g40.txt", "w")
iso = lambda t: time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(t))
price = {r["date"]: float(r["close"]) for r in csv.DictReader(open(OUT + "sol_daily.csv"))}
def px(bt):
    d = time.strftime("%Y-%m-%d", time.gmtime(bt))
    if d in price: return price[d]
    return price[min(price)] if d < min(price) else price[max(price)]
series = {r["wallet"] for r in csv.DictReader(open("audits/2026-11-03/work_C/cb_series.csv"))}
send9 = {r["sender"] for r in csv.DictReader(open("audits/2026-11-03/work_D/d20_senders.csv"))}
g33 = set(json.load(open("data/prevent_groups.json"))[0]["members"])
CR = "8YLEuUtZ4eFMJbf46oNb1CeG6dYFWGyxnQSh9hrgzBzR"
SALVE = {"G41vRrsHShLEvwMj58ruhqJycGfAtWXxtLD56uFExL8E", "C73Yv9iHmTaf8SU2XFnGLt7QXUDqbeWNtUYza9WJhkae", "AtZjv3DuV9cLn3Jxm72TMSdTN4aM6CrBaGyxUC4c2wDk", "EGtyQEgMKGKXjppDqj9sYy97e9m7nvu1US4SfFXNakMy"}
P1 = (series | send9 | {CR}) - SALVE
P2 = (g33 | SALVE) - P1
H3 = "H3QsBrrivimFJmSpTXuvig2n1Bh7JuYxrriRSEszT6cc"; GX = "GXZvXsD6hxaLeFvQisWpdAwsayJxga7w9EeafhFZG2Ra"; P9 = "9PrmF8sfoD2YShtWUghrGEYgxwabpnzog8gT1V6LEtdq"
PER = {"P1 créateur et dépôt 9W9b": P1, "P2 groupe de 33 et salve du 23/07": P2, "H3QsBr": {H3}, "GXZvX": {GX}, "9PrmF8": {P9}}
print("tailles", {k: len(v) for k, v in PER.items()}, "33 dans P1", sorted(x[:8] for x in g33 & P1), "chevauchement P1 P2", len(P1 & P2))
DEP_CB = {"9W9b3zgHH9mCEHDhsdbnbEPHStm9vvXS4aia4DWHBxpL": "9W9b", "Caw4RrwkmxqtbLSFzgSs6id3XiFxWQxs2t1mrn5a3mME": "Caw4", "AQVgyg8P5Yh5YcAqAMQRRGzDegy1R58gN4Qh87QsJAF1": "AQVg", "H9XezqfdXuv4ZCHAAZ92oMLSSAPB6Dgm4ZSrRythCbPi": "H9Xe"}
DEP_OTH = {"By6Dao4QMNeBxmdUrqsoQA8dCGbHz7xWj57CdHV5M47r": "By6D vers service non nommé", "42MSVeV4YbESE7mNW7DfQrfd8E4RG6njxXZLAWTmXemv": "42MS vers 94xmX5J9", "9kqTVnRUkVTFD7na9BTWcoG9piL4XpVTtS9kqVCV56tV": "9kqT vers 94xmX5J9", "8N4AvP9j5BditSQMk2WrTNxthhgpncGVzLKrYP4xdEqx": "8N4A vers MEXC 1"}
FAM = {"FpwQQhQQoEaVu3WU2qZMfF1hx48YyfwsLoRgXG83E99Q", "D89hHJT5Aqyx1trP6EnGY9jJUB3whgnq3aUvvCqedvzf", "DPqsobysNf5iA9w7zrQM8HLzCKZEDMkZsWbiidsAt1xo", "5g7yNHyGLJ7fiQ9SN9mf47opDnMjc585kqXWt6d7aBWs", "9obNtb5GyUegcs3a1CbBkLuc5hEWynWfJC6gjz5uWQkE", "4NyK1AdJBNbgaJ9EsKz3J4rfeHsuYdjkTPg3JaNdLeFw", "8JUEoHNMbWM4eegcMvx6ZQJt3V3fbo8JNjpWiCtJgxfF", "AafGzY9eiC5Ud3YFZQwkaKApp48cVBAT2kksGvEjhUvH"}
ven = set(lv()) | {"5Q544fKrFoe6tsEbD7S8EmxGTJYAKtTVhAW5Q5pge4j1"}
pop = {}
for r in csv.DictReader(open(OUT + "g10_dest.csv")):
    pop[r["dst"]] = int(r["n_senders"])
ONEHOP = {"8YSi5yNRN2KMbGU7Q3i5w9W6fTRxnk1qatQ5YmzS5da7", "AGG2FsrpP4wN6hjptovXH3sykfdMt6ESADJGLxMYKcJZ", "E1wDwfkh1ySipYTgqx6DtCQrri2L8KCwzECC3arUMXyK", "BZ2UcCujoCr4XYZE2s23xTWYJMgiFSQoYopYrr1B2QmA", "5QbApAquHTJ2waLG2VXNctdF1a1QUvsmwTHew4pmnwG5", "Co3zTr2M8huMY5os2wuvKGP4x3S3q4D9fzAoMZeGSMbb", "AverrTRTKkP8SH4LHCiRKyvEMHoJGyCpkG1Bk2RJQYSp", "RBsneDCLZHmbTd3iuNyF2bJkiAoap2yiLuPQSkcAmaz", "7SEoKiBLaGhZxr5V8JYGdiV55ZhkgC727ftSYDST148i", "4Tqy4SPNJjD1RPPqqiyf7faReBXF5XqesoTchZn1e9DF", "B1KEP1nunxUGrCoWZPZzoFJZ2wvLAXuVyNQrycYKRJ91", "72Pgt5MregKZXqkJcYUVvf1vJBH7xun3L3SQfRUBba5Y", "7TQBJhqbhGFsKdgGuXsFAU4mHDm2zxsXz8YTb7EAo4Tv", "7zycfr97z815o7Bo9MWN47WJR8yv5WF1FcVGj3jL6pK7", "ASWgowZA74nBJM4UGZk7eAKnGqp2kvi5jzT7zwkrxj4W", "J2EuNwCSDfFGUhmpWdnoEgZKA17b4dgE9PQVY3jMFiQ3", "4aJ4oko7JKQnCAc76FwfjRcWskUZDzRc7wDyD8LMV6bp", "7Gw3gL8mq7TSENSe9VZD9DgJiPQF9dHd6Auwk6PRkjhx"}
def cls(d, me):
    if d in me: return ("interne", "", "A")
    for k, v in PER.items():
        if v is not me and d in v: return ("autre périmètre " + k.split()[0], "", "A")
    if d in DEP_CB: return ("compte de dépôt balayé vers Coinbase", DEP_CB[d], "B")
    if d in DEP_OTH: return ("compte balayé vers autre plate-forme", DEP_OTH[d], "B" if "MEXC" in DEP_OTH[d] else "C")
    l = label(d) or ""
    if d in ven or "Jupiter" in l or "Raydium" in l or "Pump" in l: return ("pool ou route", l, "A")
    if l: return ("hot wallet ou service étiqueté", l, "A")
    if d in FAM: return ("famille de hot wallets présumée", "balayée par des dépôts témoins, sans étiquette", "C")
    if pop.get(d, 0) >= 15: return ("service ou pool non nommé", f"{pop[d]} expéditeurs tracés", "C")
    if d in ONEHOP: return ("wallet sondé, trace arrêtée", "historique partiel lu", "C")
    return ("wallet non suivi", "aucun historique lu", "D")
con = duckdb.connect(":memory:", config={"memory_limit": "800MB", "threads": 2, "temp_directory": G + "duck", "preserve_insertion_order": False})
con.execute("SET TimeZone='UTC'")
allw = set().union(*PER.values())
con.execute("CREATE TABLE t(a VARCHAR)"); con.executemany("INSERT INTO t VALUES (?)", [[a] for a in allw])
rows = con.execute(f"""SELECT owner,cp,asset,amt,bt,sig FROM read_parquet('{G}net_flows.parquet') WHERE owner IN (SELECT a FROM t) AND dir='out' AND pure=1 AND asset IN ('SOL','USDC','USDT','DMAGA') AND cp<>''""").fetchall()
stat = {r["owner"]: r for r in csv.DictReader(open(G + "net_stats.csv"))}
trunc = {r["wallet"] for r in csv.DictReader(open(OUT + "targets.csv")) if r["net"] == "True" and r["net_complete"] != "True"}
SOLM = "So11111111111111111111111111111111111111111"; UC = "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"; UT = "Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB"
extra = []
for a in sorted(trunc & allw):
    last = int(stat[a]["last_bt"])
    for s, bt, d, m, raw in con.execute(f"""SELECT DISTINCT sig,bt,dst,mint,raw FROM read_parquet('{G}flows_all.parquet') WHERE src=? AND bt>{last} AND mint IN ('{SOLM}','{UC}','{UT}') AND dst IS NOT NULL""", [a]).fetchall():
        extra.append((a, d, "SOL" if m == SOLM else ("USDC" if m == UC else "USDT"), raw / (1e9 if m == SOLM else 1e6), bt, s))
ORD = {r["signature"] for r in csv.DictReader(open(OUT + "g43_orders.csv"))}
n0 = len(extra); extra = [e for e in extra if e[5] not in ORD]  # un ordre décodé compte comme pont, pas aussi comme wallet non suivi
print("lignes pures", len(rows), "lignes au-delà de la troncature (raw/flows, pureté inconnue)", len(extra), "retirées car ordres inter-chaînes", n0 - len(extra))
per_of = {}
for k, v in PER.items():
    for a in v: per_of.setdefault(a, (k, v))
agg = {}
extra_keys = set()
for src, d, asset, amt, bt, s in [(*r, ) for r in rows] + extra:
    if src == d or d is None: continue
    if (asset == "SOL" and amt < 0.01) or (asset in ("USDC", "USDT") and amt < 1) or (asset == "DMAGA" and amt < 1000): continue
    late = src in trunc and bt > int(stat[src]["last_bt"])
    k = (src, d, asset + ("~" if late else "")); e = agg.setdefault(k, [0.0, 0.0, bt, bt, s, 0])
    e[0] += amt; e[1] += amt if asset == "SOL" else (0.0 if asset == "DMAGA" else amt / px(bt)); e[2] = min(e[2], bt); e[3] = max(e[3], bt); e[5] += 1
    if late: extra_keys.add(k)
# ponts : ordres inter-chaînes décodés (g43_orders.csv), plus SwapAndBridge lu dans net_flows
import calendar
BR = {}
for r in csv.DictReader(open(OUT + "g43_orders.csv")):
    bt = calendar.timegm(time.strptime(r["utc"], "%Y-%m-%d %H:%M:%S")); usd = int(r["give_raw"]) / 1e6
    k = (r["wallet"], r["receiver_dst"], "USDC ordre inter-chaînes"); e = agg.setdefault(k, [0.0, 0.0, bt, bt, r["signature"], 0])
    e[0] += usd; e[1] += usd / px(bt); e[2] = min(e[2], bt); e[3] = max(e[3], bt); e[5] += 1
    BR[r["receiver_dst"]] = r["chain_id"]
for src, amt, bt, s in con.execute(f"""SELECT owner,amt,bt,sig FROM read_parquet('{G}net_flows.parquet') WHERE cp='7DyZQw3iV5zhHssnNA6Nopi5zc8NGLbYjHMcaok6NN66' AND dir='out' AND asset IN ('USDC','USDT') AND amt>=1""").fetchall():
    k = (src, "7DyZQw3iV5zhHssnNA6Nopi5zc8NGLbYjHMcaok6NN66", "USDC ordre inter-chaînes"); e = agg.setdefault(k, [0.0, 0.0, bt, bt, s, 0])
    e[0] += amt; e[1] += amt / px(bt); e[2] = min(e[2], bt); e[3] = max(e[3], bt); e[5] += 1
    BR[k[1]] = "SwapAndBridge, programme BrdgN2RP"
# balayages des dépôts
sys.path.insert(0, OUT)
from g_lib import history, parse
SWEEP = {}
for dep in list(DEP_CB) + list(DEP_OTH):
    for t in history(dep):
        x = parse(t)
        if x["err"]: continue
        for kd, asset, mint, a_, d_, raw, dc in x["moves"]:
            if a_ == dep and d_ != dep and asset in ("SOL", "USDC", "USDT") and (raw >= 1_000_000):
                amt = raw / (1e9 if asset == "SOL" else 1e6); k = (dep, d_, asset); e = agg.setdefault(k, [0.0, 0.0, x["bt"], x["bt"], x["sig"], 0])
                e[0] += amt; e[1] += amt if asset == "SOL" else amt / px(x["bt"]); e[2] = min(e[2], x["bt"]); e[3] = max(e[3], x["bt"]); e[5] += 1; SWEEP[k] = 1
# entrées des dépôts par des wallets hors périmètres : flux qualifiés aussi
for r in csv.DictReader(open(OUT + "g30_in.csv")):
    if r["sender"] in allw: continue
    bt = __import__("calendar").timegm(time.strptime(r["utc"], "%Y-%m-%d %H:%M:%S"))
    k = (r["sender"], r["depot"], r["asset"]); e = agg.setdefault(k, [0.0, 0.0, bt, bt, r["signature"], 0])
    e[0] += float(r["amount"]); e[1] += float(r["sol_eq"]); e[2] = min(e[2], bt); e[3] = max(e[3], bt); e[5] += 1
tab = collections.defaultdict(lambda: collections.Counter()); tabd = collections.defaultdict(lambda: collections.Counter())
with open(OUT + "flow_boundaries.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow("wallet_source destination actif montant sol_eq n date_debut date_fin type_frontiere precision niveau signature_exemple perimetre_source".split())
    for (src, d, asset0), e in sorted(agg.items(), key=lambda kv: -kv[1][1]):
        asset = asset0.rstrip("~")
        pname, me = per_of.get(src, ("hors périmètres", set()))
        c = cls(d, me)
        if asset.startswith("USDC ordre"):
            c = ("pont, ordre inter-chaînes", f"chaîne ou programme {BR[d]}", "B")
        elif (src, d, asset) in SWEEP:
            pname = "balayage de dépôt"
            c = ("balayage vers hot wallet étiqueté" if label(d) else ("balayage vers famille présumée" if d in FAM else "balayage vers service non nommé"), label(d) or "", "A" if label(d) else "C")
        elif (src, d, asset0) in extra_keys:
            c = (c[0] + " [au-delà de la troncature, pureté inconnue]", c[1], "C" if c[2] in ("A", "B") else c[2])
        w.writerow([src, d, asset, round(e[0], 6), round(e[1], 6), e[5], iso(e[2]), iso(e[3]), c[0], c[1], c[2], e[4], pname])
        if asset == "DMAGA": tabd[pname][c[0]] += e[0]
        else: tab[pname][c[0]] += e[1]
for p in PER:
    c = tab[p]; ext = sum(v for k, v in c.items() if k != "interne" and "pool ou route" not in k)
    print(f"== {p} : dénominateur hors interne, pools et routes {ext:.1f} SOL éq. ; interne {c['interne']:.1f} ; pools et routes {sum(v for k, v in c.items() if 'pool ou route' in k):.1f}")
    for k, v in c.most_common():
        if k != "interne" and "pool ou route" not in k: print(f"   {k} : {v:.1f} ; {100 * v / ext:.1f} %")
    d_ = tabd[p]; print("   DMAGA transférés, M de jetons", {k: round(v / 1e6, 2) for k, v in d_.most_common(6)})
# Vue par wallet de P1
tx = con.execute(f"""SELECT owner,sum(CASE WHEN dmaga_delta<0 AND pure=0 AND err=0 THEN greatest(native_delta+wsol_delta,0) ELSE 0 END)/1e9,sum(CASE WHEN dmaga_delta<0 AND pure=0 AND err=0 THEN greatest(usdc_delta+usdt_delta,0) ELSE 0 END)/1e6,sum(CASE WHEN dmaga_delta<0 AND pure=0 AND err=0 THEN -dmaga_delta ELSE 0 END)/1e12,sum(CASE WHEN dmaga_delta>0 AND pure=0 AND err=0 THEN dmaga_delta ELSE 0 END)/1e12,count(*) FROM read_csv('{G}net_txs.csv.gz',header=true,types={{'programs':'VARCHAR','owner':'VARCHAR','sig':'VARCHAR','signers':'VARCHAR','payer':'VARCHAR'}}) WHERE owner IN (SELECT a FROM t) GROUP BY 1""").fetchall()
txd = {r[0]: r for r in tx}
out = collections.defaultdict(lambda: collections.Counter())
for (src, d, asset0), e in agg.items():
    asset = asset0.rstrip("~")
    if src in P1 and asset != "DMAGA":
        c = cls(d, P1)
        out[src]["9W9b" if d.startswith("9W9b") else ("Caw4" if d.startswith("Caw4") else ("pont" if asset.startswith("USDC ordre") else c[0]))] += e[1]
with open(OUT + "g40_p1_wallets.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow("wallet serie15 exp9W9b g33 hist_complet ventes_jetons_M ventes_SOL ventes_USD achats_jetons_M vers_9W9b_soleq vers_Caw4_soleq interne_soleq hot_soleq non_suivi_soleq".split())
    for a in sorted(P1, key=lambda x: -(out[x]["9W9b"] + out[x]["Caw4"])):
        r = txd.get(a, (a, 0, 0, 0, 0, 0)); o = out[a]
        w.writerow([a, a in series, a in send9, a in g33, a not in trunc and a in stat, round(r[3], 3), round(r[1], 3), round(r[2], 2), round(r[4], 3), round(o["9W9b"], 3), round(o["Caw4"], 3), round(o["interne"], 3), round(o["hot wallet ou service étiqueté"] + o["famille de hot wallets présumée"], 3), round(o["wallet non suivi"], 3)])
for name, S in (("P1", P1), ("P2", P2), ("H3", {H3}), ("GX", {GX}), ("P9", {P9})):
    s = [txd[a] for a in S if a in txd]
    print(name, "ventes de jetons M", round(sum(x[3] for x in s), 2), "encaissé SOL", round(sum(x[1] for x in s), 1), "USD", round(sum(x[2] for x in s), 1), "wallets", len(s), "sur", len(S))
ser = [a for a in series]
print("série 15 : ventes jetons M, SOL, USD", round(sum(txd[a][3] for a in ser if a in txd), 2), round(sum(txd[a][1] for a in ser if a in txd), 1), round(sum(txd[a][2] for a in ser if a in txd), 1), "vers 9W9b", round(sum(out[a]["9W9b"] for a in ser), 1), "vers Caw4", round(sum(out[a]["Caw4"] for a in ser), 1))
