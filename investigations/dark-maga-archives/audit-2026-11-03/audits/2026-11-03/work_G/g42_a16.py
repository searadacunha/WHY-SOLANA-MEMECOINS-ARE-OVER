#!/usr/bin/env python3
"""Point 5, piste A-16. Depuis les tables de A (brut mint et pool) et les pages téléchargées : signataires, sens, volume par fenêtre, allers-retours, financement, déploiement du programme, autres jetons. Sortie g42.txt, g42_signers.csv."""
import csv, gzip, json, sys, time, collections
sys.path.insert(0, "audits/2026-11-03/work_G")
import duckdb
from g_lib import parse, NETG
OUT = "audits/2026-11-03/work_G/"; G = "/Volumes/VERBATIM HD/Dark-MAGA-Investigation/audits_work/G/"; A = "/Volumes/VERBATIM HD/Dark-MAGA-Investigation/audits_work/A/"; B = "/Volumes/VERBATIM HD/Dark-MAGA-Investigation/data/"
sys.stdout = open(OUT + "g42.txt", "w")
iso = lambda t: time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(t))
SVC = "3GMsedVPsXjWR7HYUvwm1YUpvBC2bTgSkXixm4gMXnPk"; O4 = "4ToQp55myvfpeprgKuqGbDqyji9Ezm7CZg7QbcTpL33S"
con = duckdb.connect(":memory:", config={"memory_limit": "800MB", "threads": 2, "temp_directory": G + "duck", "preserve_insertion_order": False})
con.execute("SET TimeZone='UTC'")
print("schéma a15_tx", [c[0] for c in con.execute(f"DESCRIBE SELECT * FROM '{A}a15_tx.parquet'").fetchall()])
print("schéma a15_leg", [c[0] for c in con.execute(f"DESCRIBE SELECT * FROM '{A}a15_leg.parquet'").fetchall()])
con.execute(f"CREATE TABLE st AS SELECT signature,signers,t FROM '{A}a15_tx.parquet' WHERE progs LIKE '%{SVC}%'")
print("tx DMAGA du programme", con.execute("SELECT count(*),min(t),max(t) FROM st").fetchone())
sig = con.execute("SELECT signers,count(*),min(t),max(t) FROM st GROUP BY 1 ORDER BY 2 DESC").fetchall()
ss = {x for r in sig for x in r[0].split(",")}
print("signataires", len(ss), "groupes de signataires", len(sig))
con.execute("CREATE TABLE sg(a VARCHAR)"); con.executemany("INSERT INTO sg VALUES (?)", [[a] for a in ss])
# financement : qui donne du SOL aux signataires, qui reçoit d'eux
Fa = f"read_parquet('{G}flows_all.parquet')"
fe = con.execute(f"""SELECT src,count(DISTINCT dst) nd,sum(raw)/1e9 s,count(*) n FROM (SELECT DISTINCT sig,src,dst,raw,ins,inner_ FROM {Fa} WHERE mint='So11111111111111111111111111111111111111111' AND dst IN (SELECT a FROM sg) AND raw>=1000000) GROUP BY 1 ORDER BY 2 DESC LIMIT 12""").fetchall()
print("expéditeurs de SOL vers les signataires, vus par raw/flows", [(r[0], r[1], round(r[2], 2), r[3]) for r in fe])
print("signataires présents dans raw/flows comme traçés", con.execute(f"SELECT count(DISTINCT wallet) FROM {Fa} WHERE wallet IN (SELECT a FROM sg)").fetchone())
fo = con.execute(f"""SELECT dst,count(DISTINCT src) nd,sum(raw)/1e9 s,count(*) n FROM (SELECT DISTINCT sig,src,dst,raw,ins,inner_ FROM {Fa} WHERE mint='So11111111111111111111111111111111111111111' AND src IN (SELECT a FROM sg) AND raw>=1000000) GROUP BY 1 ORDER BY 2 DESC LIMIT 12""").fetchall()
print("destinations de SOL des signataires", [(r[0], r[1], round(r[2], 2), r[3]) for r in fo])
fundq = con.execute(f"""SELECT count(*) FROM (SELECT DISTINCT sig FROM {Fa} WHERE (src='{O4}' AND dst IN (SELECT a FROM sg)) OR (dst='{O4}' AND src IN (SELECT a FROM sg)))""").fetchone()
print("virements directs 4ToQp55m et signataires vus", fundq)
# volume
L = f"read_parquet('{A}a15_leg.parquet')"
con.execute(f"CREATE TABLE lg AS SELECT l.* FROM {L} l WHERE signature IN (SELECT signature FROM st)")
print("lignes de jambes", con.execute("SELECT count(*),count(DISTINCT owner),count(DISTINCT signature) FROM lg").fetchone())
print("colonnes exemple", con.execute("SELECT * FROM lg LIMIT 2").fetchall())
S = 1721588400
for n, a, b in (("3 h avant S", S - 10800, S), ("24 h avant S", S - 86400, S), ("24 h après 19:30:13", 1721590213, 1721590213 + 86400), ("toute l'histoire", 0, 1800000000)):
    r = con.execute(f"SELECT round(sum(CASE WHEN signature IN (SELECT signature FROM st) THEN -sol ELSE 0 END)/1e9,2),round(sum(-sol)/1e9,2),count(DISTINCT CASE WHEN signature IN (SELECT signature FROM st) THEN owner END) FROM {L} WHERE dmaga>0 AND t>={a} AND t<{b}").fetchone()
    print(n, "achats du programme SOL, total, propriétaires", r, "part %", round(100 * r[0] / r[1], 2) if r[1] else None)
# par signataire : achats, ventes, net, durée de détention
w = csv.writer(open(OUT + "g42_signers.csv", "w", newline="")); w.writerow("signataire n_tx premier dernier".split())
for r in sig: w.writerow([r[0], r[1], iso(int(r[2])), iso(int(r[3]))])
agg = con.execute("SELECT owner,sum(CASE WHEN dmaga>0 THEN -sol ELSE 0 END)/1e9 achat,sum(CASE WHEN dmaga<0 THEN sol ELSE 0 END)/1e9 vente,sum(CASE WHEN dmaga>0 THEN 1 ELSE 0 END) nb,sum(CASE WHEN dmaga<0 THEN 1 ELSE 0 END) ns,sum(dmaga) net_dmaga FROM lg GROUP BY 1 ORDER BY 2 DESC").fetchall()
print("par propriétaire de jambe (top 8)", [(r[0][:8], round(r[1], 1), round(r[2], 1), r[3], r[4], round(r[5] / 1e6, 3)) for r in agg[:8]])
print("somme achats, ventes", round(sum(r[1] for r in agg), 1), round(sum(r[2] for r in agg), 1), "propriétaires", len(agg), "net jetons M", round(sum(r[5] for r in agg) / 1e6, 3))
print("signataires avec un net de jetons nul à 1 % près", sum(1 for r in agg if r[1] > 0 and abs(r[1] - r[2]) / r[1] < 0.02), "sur", sum(1 for r in agg if r[1] > 0))
# délai entre achat et revente par propriétaire
d = con.execute("""WITH b AS (SELECT owner,t,row_number() OVER (PARTITION BY owner ORDER BY t) k FROM lg WHERE dmaga>0), s AS (SELECT owner,t,row_number() OVER (PARTITION BY owner ORDER BY t) k FROM lg WHERE dmaga<0) SELECT quantile_cont(s.t-b.t,[0.1,0.5,0.9]),count(*) FROM b JOIN s USING(owner,k) WHERE s.t>=b.t""").fetchone()
print("délai achat puis revente (s), p10 p50 p90, paires", d)
# pages du programme
for fn in (SVC + ".jsonl.gz", SVC + ".desc.jsonl.gz"):
    n = up = own = 0; mints = set(); sigs = set()
    for l in gzip.open(NETG + fn, "rt"):
        t = json.loads(l); x = parse(t); n += 1; sigs |= set(x["signers"])
        if any((o == O4) for (o, m) in x["tok"]): own += 1
        for (o, m) in x["tok"]: mints.add(m)
        if any(i.get("programId", "").startswith("BPFLoaderUpgradeab") for i in t["transaction"]["message"]["instructions"]):
            up += 1; print("  tx du chargeur", iso(x["bt"]), x["sig"], "signataires", x["signers"], "payeur", x["payer"], [i.get("parsed", {}).get("type") if isinstance(i.get("parsed"), dict) else None for i in t["transaction"]["message"]["instructions"]][:3])
    print(fn[-20:], "tx", n, "où le solde de jetons de 4ToQp55m bouge", own, "mints distincts", len(mints), "signataires", len(sigs), "4ToQp55m signe", O4 in sigs)
