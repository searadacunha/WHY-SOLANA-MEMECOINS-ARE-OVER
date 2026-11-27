#!/usr/bin/env python3
"""Auditeur A. Forme de trades.parquet : doublons, kinds, sources, swaps dont la quantité diffère du vault, routeurs, venues. Lecture seule."""
import duckdb
A = "/Volumes/VERBATIM HD/Dark-MAGA-Investigation/audits_work/A"
T = "'/Volumes/VERBATIM HD/Dark-MAGA-Investigation/data/trades.parquet'"
con = duckdb.connect(":memory:", config={"memory_limit": "800MB", "threads": 2, "temp_directory": A + "/duck11"})
con.execute("SET TimeZone='UTC'")
q = lambda s: con.execute(s).fetchall()
print("lignes, signatures", q(f"SELECT count(*), count(DISTINCT signature) FROM read_parquet({T})"))
print("par kind", q(f"SELECT kind, count(*), count(DISTINCT signature) FROM read_parquet({T}) GROUP BY 1 ORDER BY 2 DESC"))
print("par source", q(f"SELECT source, count(*), count(DISTINCT signature) FROM read_parquet({T}) GROUP BY 1 ORDER BY 2 DESC"))
print("signatures à plus d'une source", q(f"SELECT count(*) FROM (SELECT signature FROM read_parquet({T}) GROUP BY 1 HAVING count(DISTINCT source)>1)"))
print("doublons exacts (signature,kind,owner,token_delta)", q(f"SELECT count(*), sum(n-1) FROM (SELECT count(*) n FROM read_parquet({T}) GROUP BY signature,kind,owner,token_delta HAVING count(*)>1)"))
print("block_time nul, tx_index nul", q(f"SELECT sum((block_time IS NULL)::int), sum((tx_index IS NULL)::int), min(block_time), max(block_time) FROM read_parquet({T})"))
print("swap par venue (top)", q(f"SELECT venue, count(*), round(sum(CASE WHEN token_delta>0 THEN -sol_lamports ELSE 0 END)/1e9), round(sum(CASE WHEN token_delta<0 THEN sol_lamports ELSE 0 END)/1e9) FROM read_parquet({T}) WHERE kind='swap' GROUP BY 1 ORDER BY 2 DESC LIMIT 15"))
print("swap total SOL", q(f"SELECT round(sum(CASE WHEN token_delta>0 THEN -sol_lamports ELSE 0 END)/1e9), round(sum(CASE WHEN token_delta<0 THEN sol_lamports ELSE 0 END)/1e9), sum((sol_lamports=0)::int), sum(usdc_raw<>0::int) FROM read_parquet({T}) WHERE kind='swap'") if False else "")
# échelle : quantité de la ligne (par signature) contre le vault
print("doublons par kind/source", q(f"""WITH d AS (SELECT signature,kind,owner,token_delta,source,count(*) n, sum(abs(sol_lamports)) s FROM read_parquet({T}) GROUP BY ALL HAVING count(*)>1)
   SELECT kind,source,count(*),sum(n-1),round(sum(s*(n-1)/n)/1e9,2),min(n),max(n) FROM d GROUP BY 1,2 ORDER BY 3 DESC"""))
print("exemples", q(f"""SELECT signature,kind,owner,token_delta,source,count(*) n,min(block_time),max(sol_lamports) FROM read_parquet({T}) GROUP BY signature,kind,owner,token_delta,source HAVING count(*)>1 ORDER BY abs(token_delta) DESC LIMIT 6"""))
print("échelle par signature, swaps :")
r = q(f"""WITH s AS (SELECT signature, any_value(pool_token_delta) p, any_value(pool_sol_delta) ps, sum(abs(token_delta)) q, sum(abs(sol_lamports)) sol, count(*) n, any_value(venue) v
                     FROM read_parquet({T}) WHERE kind='swap' GROUP BY 1)
          SELECT CASE WHEN p=0 THEN 'p0' WHEN q*1.0/abs(p) < 0.01 THEN 'a <1%' WHEN q*1.0/abs(p)<0.5 THEN 'b 1-50%' WHEN q*1.0/abs(p)<0.99 THEN 'c 50-99%' WHEN q*1.0/abs(p)<=1.01 THEN 'd 99-101%' WHEN q*1.0/abs(p)<2 THEN 'e 101-200%' ELSE 'f >200%' END c,
                 count(*), round(sum(sol)/1e9), round(sum(q)/1e12,1), round(sum(abs(p))/1e12,1) FROM s GROUP BY 1 ORDER BY 1""")
for x in r:
    print(" ", x)
print("mêmes tranches, par fenêtre 21/07 avant S et 24 h après la borne haute :")
for name, a, b in (("avant_S_21h", 1721588400 - 24 * 3600, 1721588400), ("24h_apres_musk", 1721590213, 1721590213 + 86400)):
    r = q(f"""WITH s AS (SELECT signature, any_value(pool_token_delta) p, sum(abs(token_delta)) q, sum(abs(sol_lamports)) sol FROM read_parquet({T})
                         WHERE kind='swap' AND block_time>={a} AND block_time<{b} GROUP BY 1)
              SELECT CASE WHEN p=0 THEN 'p0' WHEN q*1.0/abs(p)<0.5 THEN 'moins de 50%' WHEN q*1.0/abs(p)<=1.01 THEN '50-101%' ELSE 'plus de 101%' END c, count(*), round(sum(sol)/1e9,1) FROM s GROUP BY 1 ORDER BY 1""")
    print(" ", name, r)
print("multi-bénéficiaires", q(f"SELECT n_owners, count(*), round(sum(abs(sol_lamports))/1e9) FROM read_parquet({T}) WHERE kind='swap' GROUP BY 1 ORDER BY 1 LIMIT 12"))
print("bénéficiaire non signataire", q(f"SELECT (position(owner in signers)>0) signe, count(*), round(sum(abs(sol_lamports))/1e9) FROM read_parquet({T}) WHERE kind='swap' GROUP BY 1"))
print("top non signataires par SOL", q(f"SELECT owner, count(*), round(sum(abs(sol_lamports))/1e9) s FROM read_parquet({T}) WHERE kind='swap' AND position(owner in signers)=0 GROUP BY 1 ORDER BY s DESC LIMIT 25"))
print("lignes usdc", q(f"SELECT count(*), round(sum(abs(usdc_raw))/1e6), round(sum(abs(sol_lamports))/1e9) FROM read_parquet({T}) WHERE kind='swap' AND usdc_raw<>0"))
print("lignes usdc ET sol", q(f"SELECT count(*), round(sum(abs(usdc_raw))/1e6), round(sum(abs(sol_lamports))/1e9) FROM read_parquet({T}) WHERE kind='swap' AND usdc_raw<>0 AND sol_lamports<>0"))
print("sens incohérent swap", q(f"SELECT sum((token_delta>0 AND sol_lamports>0)::int), sum((token_delta<0 AND sol_lamports<0)::int), sum((sol_lamports=0 AND usdc_raw=0)::int) FROM read_parquet({T}) WHERE kind='swap'"))
print("internal", q(f"SELECT round(sum(abs(sol_lamports))/1e9), round(sum(abs(pool_token_delta))/1e12,1) FROM read_parquet({T}) WHERE kind='internal'"))
