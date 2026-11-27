#!/usr/bin/env python3
"""Auditeur A. Suite de a13 (tué par le garde à 1 056 Mo) : propriétaires sans ligne trades, et chaîne de chaque compte de jetons DMAGA. Limite DuckDB 500 Mo."""
import duckdb
A = "/Volumes/VERBATIM HD/Dark-MAGA-Investigation/audits_work/A"
B = "/Volumes/VERBATIM HD/Dark-MAGA-Investigation/data"
VS = "3p7DbnWekWjtMQkey6fp1emdwXbAAxecnYuD5eU9ZZPH"
con = duckdb.connect(":memory:", config={"memory_limit": "500MB", "threads": 2, "temp_directory": A + "/duck13b", "preserve_insertion_order": False})
con.execute("SET TimeZone='UTC'")
def show(n, s):
    print(n, con.execute(s).fetchall(), flush=True)
con.execute(f"COPY (SELECT signature, owner, any_value(dmaga) dmaga, any_value(is_signer) sg FROM read_parquet('{A}/a02_own.parquet') GROUP BY 1,2) TO '{A}/a13_ow.parquet' (FORMAT parquet, COMPRESSION zstd)")
con.execute(f"COPY (SELECT DISTINCT signature, owner FROM read_parquet('{B}/trades.parquet') WHERE owner IS NOT NULL AND kind<>'mint_supply') TO '{A}/a13_tr.parquet' (FORMAT parquet, COMPRESSION zstd)")
OW, TR = f"read_parquet('{A}/a13_ow.parquet')", f"read_parquet('{A}/a13_tr.parquet')"
show("couples propres sans trades, par signataire", f"SELECT sg, count(*), round(sum(abs(dmaga))/1e6) FROM {OW} o ANTI JOIN {TR} t USING (signature, owner) GROUP BY 1")
show("  top propriétaires sans ligne trades", f"SELECT owner, count(*), round(sum(abs(dmaga))/1e6) s FROM {OW} o ANTI JOIN {TR} t USING (signature, owner) GROUP BY 1 ORDER BY s DESC LIMIT 30")
# chaîne de chaque compte de jetons, tri et fenêtre dans DuckDB, spill sur le disque USB
con.execute(f"""COPY (SELECT account, any_value(owner) owner, signature, any_value(slot) slot, any_value(tx_index) tx_index, any_value(block_time) t, any_value(pre) pre, any_value(post) post
     FROM read_parquet('{A}/a02_acct.parquet') WHERE account<>'{VS}' GROUP BY account, signature) TO '{A}/a13_ca.parquet' (FORMAT parquet, COMPRESSION zstd)""")
CA = f"read_parquet('{A}/a13_ca.parquet')"
con.execute(f"COPY (SELECT *, lag(post) OVER (PARTITION BY account ORDER BY slot, tx_index) pp FROM {CA}) TO '{A}/a13_oa.parquet' (FORMAT parquet, COMPRESSION zstd)")
OA = f"read_parquet('{A}/a13_oa.parquet')"
show("comptes, lignes, ruptures, comptes rompus, jetons M manquants", f"SELECT count(DISTINCT account), count(*), sum((pp IS NOT NULL AND pp<>pre)::int), count(DISTINCT CASE WHEN pp IS NOT NULL AND pp<>pre THEN account END), round(sum(CASE WHEN pp IS NOT NULL AND pp<>pre THEN abs(pre-pp) ELSE 0 END)/1e12,3) FROM {OA}")
show("comptes dont le premier solde vu n'est pas nul : n, M", f"WITH f AS (SELECT account, arg_min(pre,(slot,tx_index)) p0 FROM {CA} GROUP BY 1) SELECT count(*), round(sum(p0)/1e12,3) FROM f WHERE p0>0")
show("top ruptures par propriétaire", f"SELECT owner, count(*), round(sum(abs(pre-pp))/1e12,3) s FROM {OA} WHERE pp IS NOT NULL AND pp<>pre GROUP BY 1 ORDER BY s DESC LIMIT 30")
show("ruptures avant Musk, n, M", f"SELECT count(*), round(sum(abs(pre-pp))/1e12,3) FROM {OA} WHERE pp IS NOT NULL AND pp<>pre AND t<1721588607")
show("jetons M manquants par bucket de part", f"SELECT CASE WHEN abs(pre-pp)<1e6 THEN 'moins de 1 jeton' WHEN abs(pre-pp)<1e9 THEN 'moins de 1000' WHEN abs(pre-pp)<1e12 THEN 'moins de 1 M' ELSE 'au moins 1 M' END c, count(*), round(sum(abs(pre-pp))/1e12,3) FROM {OA} WHERE pp IS NOT NULL AND pp<>pre GROUP BY 1 ORDER BY 3 DESC")
