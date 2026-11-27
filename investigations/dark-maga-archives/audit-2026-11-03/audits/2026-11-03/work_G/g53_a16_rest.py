#!/usr/bin/env python3
"""A-16 : les 1 913 blocs, toutes jambes confondues. Ordre, écart de quantité, marge, tiers intercalés, par propriétaire. Sortie g53.txt."""
import sys, collections
import duckdb
A = "/Volumes/VERBATIM HD/Dark-MAGA-Investigation/audits_work/A/"; G = "/Volumes/VERBATIM HD/Dark-MAGA-Investigation/audits_work/G/"
sys.stdout = open("audits/2026-11-03/work_G/g53.txt", "w")
SVC = "3GMsedVPsXjWR7HYUvwm1YUpvBC2bTgSkXixm4gMXnPk"; O4 = "4ToQp55myvfpeprgKuqGbDqyji9Ezm7CZg7QbcTpL33S"
con = duckdb.connect(":memory:", config={"memory_limit": "800MB", "threads": 2, "temp_directory": G + "duck", "preserve_insertion_order": False})
con.execute(f"CREATE TABLE st AS SELECT signature FROM '{A}a15_tx.parquet' WHERE progs LIKE '%{SVC}%'")
rows = con.execute(f"SELECT slot,tx_index,owner,dmaga,sol,t,sg FROM '{A}a15_leg.parquet' WHERE signature IN (SELECT signature FROM st) ORDER BY slot,tx_index").fetchall()
by = collections.defaultdict(list)
for r in rows: by[r[0]].append(r)
print("blocs", len(by), "jambes par bloc", collections.Counter(len(v) for v in by.values()).most_common(4))
c = collections.Counter(); m = collections.defaultdict(float); ratio = collections.Counter(); own = collections.Counter(); blocks = []
for sl, L in by.items():
    if len(L) != 2: c["autre"] += 1; continue
    a, b = L
    first_buy = a[3] > 0 and b[3] < 0
    first_sell = a[3] < 0 and b[3] > 0
    kind = "achat_puis_vente" if first_buy else ("vente_puis_achat" if first_sell else "autre")
    q1, q2 = abs(a[3]), abs(b[3]); same = abs(q1 - q2) / max(q1, q2) < 0.01
    o = "4ToQp55m" if (a[2] == O4 and b[2] == O4) else ("signataire" if a[2] != O4 and b[2] != O4 else "mixte")
    key = (kind, "même quantité" if same else "quantité différente", o)
    c[key] += 1; m[key] += (a[4] + b[4]) / 1e9
    blocks.append((sl, a[1], b[1], key))
for k, v in c.most_common(): print(k, v, "marge SOL", round(m.get(k, 0.0), 2))
# tiers intercalés par catégorie
con.execute("CREATE TABLE p(sl BIGINT,a INT,z INT,k VARCHAR)"); con.executemany("INSERT INTO p VALUES (?,?,?,?)", [[s, min(a_, z), max(a_, z), "|".join(k)] for s, a_, z, k in blocks])
for r in con.execute(f"""SELECT p.k,count(DISTINCT (p.sl,p.a)),count(l.signature),sum(CASE WHEN l.dmaga>0 THEN -l.sol ELSE 0 END)/1e9,sum(CASE WHEN l.dmaga<0 THEN l.sol ELSE 0 END)/1e9 FROM p LEFT JOIN '{A}a15_leg.parquet' l ON l.slot=p.sl AND l.tx_index>p.a AND l.tx_index<p.z AND l.signature NOT IN (SELECT signature FROM st) GROUP BY 1""").fetchall():
    print("tiers entre les jambes :", r[0], "blocs", r[1], "jambes tierces", r[2], "achats tiers SOL", round(r[3] or 0, 1), "ventes tierces SOL", round(r[4] or 0, 1))
print("jambes signées par le propriétaire de la jambe", sum(1 for r in rows if r[6]), "sur", len(rows))
