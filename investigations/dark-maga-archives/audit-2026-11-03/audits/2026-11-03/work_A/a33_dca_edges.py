#!/usr/bin/env python3
"""Auditeur A. Arêtes token_direct dans des transactions d'échange ou DCA : jambes de service restées comme liens ? Groupes de prevent_groups touchés. Composante du groupe de 33 recalculée."""
import json, sys, collections
import duckdb
ROOT = "REDACTED_HOME/Projects/Dark-MAGA-Investigation"
A = "/Volumes/VERBATIM HD/Dark-MAGA-Investigation/audits_work/A"
B = "/Volumes/VERBATIM HD/Dark-MAGA-Investigation/data"
con = duckdb.connect(":memory:", config={"memory_limit": "400MB", "threads": 2, "temp_directory": A + "/duck33", "preserve_insertion_order": False})
G = json.load(open(ROOT + "/data/prevent_groups.json"))
print("groupes", len(G), [(g["n"], g["edges"], round(g["held_before_musk_M"], 1)) for g in G])
TX = f"read_parquet('{A}/a15_tx.parquet')"
AMM = {"675kPX9MHTjS2zt1qfr1NYHuzeLXfQM9H24wFSUt1Mp8": "raydium4", "CAMMCzo5YL8w4VFF8KVHrK22GGUsp5VTaW7grrKgrWqK": "clmm", "LBUZKhRxPF3XUpBCjp4YzTKgLccjZhTSDM9YuVaPwxo": "dlmm", "whirLbMiicVdio4qvUfM5KAg6Ct8VwpYzGff3uctyCc": "orca", "JUP6LkbZbjS1jKKwapdHNy74zcZ3tLUZoi5QNyVTaV4": "jup6", "DCA265Vj8a9CEuX1eb1LWRnDT7uK6q1xMipnNyatn23M": "dca", "6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P": "pump"}
all_edges = []
for gi, g in enumerate(G):
    for e in g["edges_top"]:
        all_edges.append((gi, e["src"], e["dst"], e["M"], e["t"], e["sig"]))
con.execute("CREATE TEMP TABLE ed(g INT, a VARCHAR, b VARCHAR, m DOUBLE, t BIGINT, s VARCHAR)")
con.executemany("INSERT INTO ed VALUES (?,?,?,?,?,?)", all_edges)
rows = con.execute(f"SELECT e.g, e.a, e.b, e.m, e.s, t.progs, t.signers FROM ed e LEFT JOIN {TX} t ON t.signature=e.s").fetchall()
print("arêtes listées", len(rows), "absentes du brut", sum(1 for r in rows if r[5] is None))
hit = [(r[0], r[1], r[2], r[3], r[4], [AMM[p] for p in (r[5] or "").split(",") if p in AMM], r[6]) for r in rows if r[5] and any(p in AMM for p in r[5].split(","))]
print("arêtes dans une transaction d'échange", len(hit), hit[:12])
print("groupes touchés", collections.Counter(h[0] for h in hit))
print("groupe 0 : signataire est la source ?", sum(1 for r in rows if r[0] == 0 and r[6] and r[1] in r[6].split(",")), "sur", sum(1 for r in rows if r[0] == 0 and r[6] is not None))
m0 = set(G[0]["members"])
par = {x: x for x in m0}
def f(x):
    while par[x] != x:
        par[x] = par[par[x]]
        x = par[x]
    return x
for r in rows:
    if r[0] == 0:
        par[f(r[1])] = f(r[2])
print("composantes du groupe 0 sur ses 40 arêtes", len({f(x) for x in m0}), "nœuds hors liste", [r[1] for r in rows if r[0] == 0 and r[1] not in m0] + [r[2] for r in rows if r[0] == 0 and r[2] not in m0], "montant min", min(r[3] for r in rows if r[0] == 0))
