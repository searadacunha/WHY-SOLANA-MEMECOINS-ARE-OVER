#!/usr/bin/env python3
"""Auditeur D. C37 : sorties à 3 sauts recalculées depuis exit_flows.parquet avec un parcours réécrit, avec et sans les lignes à décimales fausses (A-12). Sortie d48_exits.txt."""
import json, sys, collections
import duckdb
from dmaga.labels import label
from dmaga.venues import load as lv
BIG = "/Volumes/VERBATIM HD/Dark-MAGA-Investigation/data"; D = "/Volumes/VERBATIM HD/Dark-MAGA-Investigation/audits_work/D"
sys.stdout = open("audits/2026-11-03/work_D/d48_exits.txt", "w")
con = duckdb.connect(":memory:", config={"memory_limit": "700MB", "threads": 2, "temp_directory": D + "/duck", "preserve_insertion_order": False})
X = f"read_parquet('{BIG}/exit_flows.parquet')"
SUM = json.load(open("data/exit_summary.json"))
print("wallets du résumé", len(SUM), "tronqués", sum(1 for v in SUM.values() if v.get("tronque")))
rep = collections.Counter()
for v in SUM.values():
    for k, x in v["frontieres"].items():
        if "pool" not in k and "Jupiter" not in k: rep[k.split(":", 1)[1]] += x
print("somme du résumé", [(k, round(v)) for k, v in rep.most_common(8)])
print("lignes", con.execute(f"SELECT count(*),count(DISTINCT wallet),sum((asset='SOL' AND amount>1e5)::int),count(DISTINCT CASE WHEN asset='SOL' AND amount>1e5 THEN wallet END),string_agg(DISTINCT CASE WHEN asset='SOL' AND amount>1e5 THEN wallet END,',') FROM {X}").fetchone())
print("assets", con.execute(f"SELECT asset,count(*),round(sum(CASE WHEN amount<1e5 THEN amount END)) FROM {X} GROUP BY 1").fetchall())
USD = 180.0
try:
    src = open("scripts/ana_62_exits.py").read()
    import re
    m = re.search(r"USD\s*=\s*([0-9.]+)", src); USD = float(m.group(1)) if m else USD
except Exception as e: print("USD non lu", e)
print("USD", USD)
ven = set(lv()) | {"5Q544fKrFoe6tsEbD7S8EmxGTJYAKtTVhAW5Q5pge4j1"}
for name, flt in (("toutes lignes", ""), ("sans décimales fausses", "AND NOT (asset='SOL' AND amount>1e5)")):
    con.execute(f"CREATE OR REPLACE TEMP TABLE a AS SELECT wallet,dst,sum(CASE WHEN asset='SOL' THEN amount ELSE amount/{USD} END) v FROM {X} WHERE dst IS NOT NULL {flt} GROUP BY 1,2")
    by = collections.defaultdict(list)
    for w, d_, v in con.execute("SELECT wallet,dst,v FROM a").fetchall(): by[w].append((d_, v))
    traced = set(by)
    pop = collections.Counter()
    for w, L in by.items():
        for d_, _ in L: pop[d_] += 1
    popular = {k for k, c in pop.items() if c >= 15}
    def cls(a):
        if a in ven: return "pool"
        l = label(a)
        if l: return l
        return "service" if a in popular else None
    agg = collections.Counter(); nw = 0
    for w in SUM:
        fr = {w: None}; seen = {w}; hit = False
        for lvl in range(3):
            nx = collections.Counter()
            for a, sh in fr.items():
                L = by.get(a)
                if not L: continue
                tot = sum(x[1] for x in L) or 1
                for d_, amt in L:
                    part = amt if a == w else sh * amt / tot
                    c = cls(d_)
                    if c:
                        hit = True
                        if "pool" not in c and "Jupiter" not in c: agg[c] += part
                    elif d_ not in seen:
                        seen.add(d_)
                        if d_ in traced and lvl < 2: nx[d_] += part
            fr = nx
        nw += hit
    print(name, "wallets atteignant une frontière", nw, [(k, round(v)) for k, v in agg.most_common(8)], flush=True)
    del by
