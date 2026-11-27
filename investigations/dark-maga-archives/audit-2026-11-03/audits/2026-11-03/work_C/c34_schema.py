import duckdb
B="/Volumes/VERBATIM HD/Dark-MAGA-Investigation/data"
c=duckdb.connect(); c.execute("SET memory_limit='250MB'; SET threads=1; SET TimeZone='UTC';")
for n in ['trades','token_edges','link_edges','wallets','nodes','funding_edges','exit_flows']:
    print(n,[(r[0],r[1]) for r in c.execute(f"DESCRIBE SELECT * FROM '{B}/{n}.parquet'").fetchall()][:30])
print(c.execute(f"SELECT kind,count(*) FROM '{B}/trades.parquet' GROUP BY 1 ORDER BY 2 DESC").fetchall())
print(c.execute(f"SELECT kind,count(*) FROM '{B}/nodes.parquet' GROUP BY 1").fetchall())
print(c.execute(f"SELECT * FROM '{B}/trades.parquet' WHERE owner='5QhJJcFZu2ashyKyWSTGHcsyo6ZBCbpVuJqeutvQHScd' LIMIT 3").fetchall())
