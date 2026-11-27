#!/usr/bin/env python3
"""A-16 suite : achat puis revente du programme 3GMsedVP dans le même bloc ? Autres échanges entre les deux jambes ? Marge par paire, déployeur parmi les signataires, liens avec les périmètres. Sortie g47.txt."""
import csv, json, sys, time, collections
import duckdb
OUT = "audits/2026-11-03/work_G/"; G = "/Volumes/VERBATIM HD/Dark-MAGA-Investigation/audits_work/G/"; A = "/Volumes/VERBATIM HD/Dark-MAGA-Investigation/audits_work/A/"
sys.stdout = open(OUT + "g47.txt", "w")
SVC = "3GMsedVPsXjWR7HYUvwm1YUpvBC2bTgSkXixm4gMXnPk"; O4 = "4ToQp55myvfpeprgKuqGbDqyji9Ezm7CZg7QbcTpL33S"; FY = "FyC5nr3WJAir6cntnwwQRuurq4JUCWvsH2VS5p4vYZ8k"
con = duckdb.connect(":memory:", config={"memory_limit": "800MB", "threads": 2, "temp_directory": G + "duck", "preserve_insertion_order": False})
con.execute("SET TimeZone='UTC'")
con.execute(f"CREATE TABLE st AS SELECT signature,slot,tx_index,t,signers FROM '{A}a15_tx.parquet' WHERE progs LIKE '%{SVC}%'")
ss = {x for r in con.execute("SELECT DISTINCT signers FROM st").fetchall() for x in r[0].split(",")}
print("déployeur FyC5nr3W parmi les 45 signataires", FY in ss, "tx signées", con.execute(f"SELECT count(*) FROM st WHERE signers LIKE '%{FY}%'").fetchone())
con.execute(f"CREATE TABLE lg AS SELECT signature,owner,t,slot,tx_index,dmaga,sol FROM '{A}a15_leg.parquet' WHERE signature IN (SELECT signature FROM st) ORDER BY slot,tx_index")
rows = con.execute("SELECT signature,owner,t,slot,tx_index,dmaga,sol FROM lg ORDER BY slot,tx_index").fetchall()
# jambes par (slot) : achat puis vente de même quantité
by = collections.defaultdict(list)
for r in rows: by[r[3]].append(r)
same = 0; pairs = []; lone = 0
for sl, L in by.items():
    buys = [x for x in L if x[5] > 0]; sells = [x for x in L if x[5] < 0]
    for b in buys:
        m = next((s for s in sells if abs(abs(s[5]) - b[5]) / b[5] < 0.01 and s[4] > b[4]), None)
        if m: pairs.append((b, m)); sells.remove(m)
        else: lone += 1
print("jambes", len(rows), "slots", len(by), "paires achat puis vente même bloc, quantité à 1 %", len(pairs), "achats sans paire dans le bloc", lone)
gain = [(m[6] + b[6]) / 1e9 for b, m in pairs]
print("marge SOL par paire : somme", round(sum(gain), 2), "médiane", round(sorted(gain)[len(gain) // 2], 5), "paires positives", sum(1 for g in gain if g > 0), "négatives", sum(1 for g in gain if g < 0))
print("écart d'index dans le bloc : médiane", sorted(m[4] - b[4] for b, m in pairs)[len(pairs) // 2], "achat SOL médian", round(sorted(-b[6] / 1e9 for b, m in pairs)[len(pairs) // 2], 3), "plus gros", round(max(-b[6] / 1e9 for b, m in pairs), 1))
# autres tx DMAGA entre les deux jambes : victimes ?
con.execute("CREATE TABLE p(sl BIGINT, a INT, z INT)"); con.executemany("INSERT INTO p VALUES (?,?,?)", [[b[3], b[4], m[4]] for b, m in pairs])
inb = con.execute(f"""SELECT p.sl,p.a,p.z,count(l.signature) n,sum(CASE WHEN l.dmaga>0 THEN 1 ELSE 0 END) ach,sum(CASE WHEN l.dmaga<0 THEN 1 ELSE 0 END) ven,sum(CASE WHEN l.dmaga>0 THEN -l.sol ELSE 0 END)/1e9 achat FROM p LEFT JOIN '{A}a15_leg.parquet' l ON l.slot=p.sl AND l.tx_index>p.a AND l.tx_index<p.z AND l.signature NOT IN (SELECT signature FROM st) GROUP BY 1,2,3""").fetchall()
withv = [r for r in inb if r[3] and r[3] > 0]; wbuy = [r for r in inb if r[4] and r[4] > 0]
print("paires avec au moins une autre tx DMAGA entre les jambes", len(withv), "sur", len(inb), "avec au moins un achat tiers entre les jambes", len(wbuy), "SOL d'achats tiers intercalés", round(sum(r[6] or 0 for r in wbuy), 1))
print("par fenêtre : paires, SOL d'achat")
for n, a, b in (("avant 19:03:27 21/07", 0, 1721588607), ("19:03:27 21/07 à 19:30:13", 1721588607, 1721590213), ("24 h après", 1721590213, 1721590213 + 86400), ("ensuite", 1721590213 + 86400, 2000000000)):
    L = [(b_, m) for b_, m in pairs if a <= b_[2] < b]
    print(" ", n, len(L), round(sum(-b_[6] / 1e9 for b_, m in L), 1))
# liens
Fa = f"read_parquet('{G}flows_all.parquet')"
T = {r["wallet"] for r in csv.DictReader(open(OUT + "targets.csv"))} - {O4}
con.execute("CREATE TABLE tg(a VARCHAR)"); con.executemany("INSERT INTO tg VALUES (?)", [[a] for a in T])
con.execute("CREATE TABLE sg(a VARCHAR)"); con.executemany("INSERT INTO sg VALUES (?)", [[a] for a in (ss | {O4})])
d = con.execute(f"""SELECT src,dst,mint,sum(raw),count(*) FROM (SELECT DISTINCT sig,src,dst,mint,raw,ins,inner_ FROM {Fa} WHERE (src IN (SELECT a FROM sg) AND dst IN (SELECT a FROM tg)) OR (dst IN (SELECT a FROM sg) AND src IN (SELECT a FROM tg))) GROUP BY 1,2,3""").fetchall()
print("arêtes directes signataires ou 4ToQp55m avec les wallets cibles", [(r[0][:8], r[1][:8], r[2][:6], r[3], r[4]) for r in d])
o = con.execute(f"""SELECT dst,sum(raw)/1e9 s,count(*) n,min(bt),max(bt) FROM (SELECT DISTINCT sig,bt,src,dst,raw,ins,inner_ FROM {Fa} WHERE src='{O4}' AND mint='So11111111111111111111111111111111111111111') WHERE dst NOT IN (SELECT a FROM sg) GROUP BY 1 ORDER BY 2 DESC LIMIT 10""").fetchall()
print("4ToQp55m : sorties de SOL hors signataires (raw/flows tronqué)", [(r[0], round(r[1], 1), r[2]) for r in o])
