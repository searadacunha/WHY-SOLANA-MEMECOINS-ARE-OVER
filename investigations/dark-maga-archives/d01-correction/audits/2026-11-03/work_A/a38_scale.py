#!/usr/bin/env python3
"""Auditeur A. Échelle quantité contre vault après dédoublonnage ; lignes lp_remove du parseur propre ; rapports qui citent les chiffres du groupe touchés."""
import duckdb
A = "/Volumes/VERBATIM HD/Dark-MAGA-Investigation/audits_work/A"
B = "/Volumes/VERBATIM HD/Dark-MAGA-Investigation/data"
con = duckdb.connect(":memory:", config={"memory_limit": "400MB", "threads": 2, "temp_directory": A + "/duck38", "preserve_insertion_order": False})
T = f"read_parquet('{B}/trades.parquet')"
print(con.execute(f"""WITH d AS (SELECT DISTINCT signature, owner, token_delta, sol_lamports, pool_token_delta FROM {T} WHERE kind='swap'),
   s AS (SELECT signature, any_value(pool_token_delta) p, sum(abs(token_delta)) q, sum(abs(sol_lamports)) sol FROM d GROUP BY 1)
   SELECT CASE WHEN p=0 THEN 'p0' WHEN q*1.0/abs(p)<0.5 THEN 'a moins de 50%' WHEN q*1.0/abs(p)<0.99 THEN 'b 50-99%' WHEN q*1.0/abs(p)<=1.01 THEN 'c 99-101%' WHEN q*1.0/abs(p)<2 THEN 'd 101-200%' ELSE 'e plus de 200%' END c, count(*), round(sum(sol)/1e9,1), round(100.0*sum(sol)/sum(sum(sol)) OVER (),3) FROM s GROUP BY 1 ORDER BY 1""").fetchall())
print(con.execute(f"""WITH d AS (SELECT DISTINCT signature, owner, token_delta, sol_lamports, pool_token_delta, venue FROM {T} WHERE kind='swap'),
   s AS (SELECT signature, any_value(pool_token_delta) p, sum(abs(token_delta)) q, sum(abs(sol_lamports)) sol, any_value(venue) v FROM d GROUP BY 1)
   SELECT signature, p, q, sol/1e9, v FROM s WHERE q*1.0/abs(p)>1.5 ORDER BY sol DESC LIMIT 5""").fetchall())
OO = f"read_parquet('{A}/a19_only_own.parquet')"
print("lp_remove du propre, par owner", con.execute(f"""SELECT o.owner, count(*), round(sum(abs(o.sol))/1e9,2) s FROM {OO} o JOIN (SELECT DISTINCT signature, owner, kind FROM {T}) k ON o.signature=k.signature AND o.owner=k.owner WHERE k.kind='lp_remove' GROUP BY 1 ORDER BY s DESC LIMIT 6""").fetchall())
