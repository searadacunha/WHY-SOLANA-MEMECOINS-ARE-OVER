#!/usr/bin/env python3
"""Auditeur A. Transferts DMAGA vus seulement par getTransfersByAddress (raw/flows) : signatures absentes du brut pool/mint/courbe/venues. Quelles adresses les concentrent : venues non découverts ? Écrit un échantillon de signatures pour le contrôle réseau."""
import json, sys
import duckdb
sys.path.insert(0, "REDACTED_HOME/Projects/Dark-MAGA-Investigation")
from dmaga.venues import load as lv
A = "/Volumes/VERBATIM HD/Dark-MAGA-Investigation/audits_work/A"
B = "/Volumes/VERBATIM HD/Dark-MAGA-Investigation/data"
OUT = "REDACTED_HOME/Projects/Dark-MAGA-Investigation/audits/2026-11-03/work_A/out"
con = duckdb.connect(":memory:", config={"memory_limit": "450MB", "threads": 2, "temp_directory": A + "/duck26", "preserve_insertion_order": False})
con.execute("SET TimeZone='UTC'")
def show(n, s, *a):
    print(n, con.execute(s, *a).fetchall(), flush=True)
con.execute("CREATE TEMP TABLE ven(a VARCHAR, n VARCHAR)")
con.executemany("INSERT INTO ven VALUES (?,?)", [[a, n] for a, n in lv().items()])
TX = f"read_parquet('{A}/a15_tx.parquet')"
con.execute(f"""COPY (SELECT e.* FROM read_parquet('{B}/token_edges.parquet') e ANTI JOIN (SELECT signature FROM {TX}) t USING (signature) WHERE e.how='gtba') TO '{A}/a26_h.parquet' (FORMAT parquet)""")
H = f"read_parquet('{A}/a26_h.parquet')"
show("gtba hors brut : lignes, signatures, M, min t, max t", f"SELECT count(*), count(DISTINCT signature), round(sum(qty)/1e6,1), min(block_time), max(block_time) FROM {H}")
show("  par année", f"SELECT block_time//31536000+1970, count(*), round(sum(qty)/1e6,1) FROM {H} GROUP BY 1 ORDER BY 1")
show("  avec un venue connu à un bout", f"SELECT count(*), round(sum(qty)/1e6,1) FROM {H} WHERE src IN (SELECT a FROM ven) OR dst IN (SELECT a FROM ven)")
show("  venues connus concernés", f"SELECT n, count(*), round(sum(qty)/1e6,1) FROM {H} JOIN ven ON src=a OR dst=a GROUP BY 1 ORDER BY 3 DESC")
show("  top contreparties source", f"SELECT src, count(*), count(DISTINCT dst), round(sum(qty)/1e6,1) s FROM {H} GROUP BY 1 ORDER BY s DESC LIMIT 15")
show("  top contreparties destination", f"SELECT dst, count(*), count(DISTINCT src), round(sum(qty)/1e6,1) s FROM {H} GROUP BY 1 ORDER BY s DESC LIMIT 15")
show("  hors venues connus, >= 1 M, avant la borne basse", f"SELECT src, dst, qty/1e6, block_time, signature FROM {H} WHERE qty>=1000000 AND block_time<1721588607 AND src NOT IN (SELECT a FROM ven) AND dst NOT IN (SELECT a FROM ven) ORDER BY block_time LIMIT 40")
rows = con.execute(f"""SELECT signature, src, dst, qty FROM (SELECT *, row_number() OVER (PARTITION BY (src IN (SELECT a FROM ven) OR dst IN (SELECT a FROM ven)), block_time>=1721590213 ORDER BY hash(signature)) r FROM {H}) WHERE r<=6""").fetchall()
json.dump([list(r) for r in rows], open(OUT + "/a26_sample.json", "w"), indent=0)
print("échantillon réseau", len(rows))
g = json.load(open("REDACTED_HOME/Projects/Dark-MAGA-Investigation/data/prevent_groups.json"))[0]
txs = {r[0] for r in con.execute(f"SELECT signature FROM {TX} WHERE signature IN (SELECT unnest(?))", [[e["sig"] for e in g["edges_top"]]]).fetchall()}
ab = [e for e in g["edges_top"] if e["sig"] not in txs]
json.dump(ab, open(OUT + "/a26_group_absent.json", "w"), indent=0)
print("arêtes du groupe absentes du brut", [(e["src"], e["dst"], e["M"], e["t"], e["sig"]) for e in ab], "somme M", sum(e["M"] for e in ab))
show("exit_flows, lignes de 2021 : wallets, lignes, tronqué", f"SELECT wallet, count(*), bool_or(truncated), min(block_time), max(block_time), max(amount) FROM read_parquet('{B}/exit_flows.parquet') WHERE asset='SOL' AND amount>100000 GROUP BY 1 ORDER BY 2 DESC LIMIT 5")
show("exit_flows antérieurs au 14/07/2024", f"SELECT count(*), count(DISTINCT wallet), max(block_time) FROM read_parquet('{B}/exit_flows.parquet') WHERE block_time<1720922725")
show("sorties tronquées : wallets", f"SELECT asset, count(DISTINCT wallet), sum(truncated::int), count(*) FROM read_parquet('{B}/exit_flows.parquet') WHERE truncated GROUP BY 1")
