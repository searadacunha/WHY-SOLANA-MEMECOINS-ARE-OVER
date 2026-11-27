import duckdb
c=duckdb.connect(":memory:",config={"memory_limit":"300MB","threads":2})
print(c.execute("describe select * from read_parquet('/Volumes/VERBATIM HD/Dark-MAGA-Investigation/data/trades.parquet')").fetchall())
print(c.execute("select count(*),min(block_time),max(block_time) from read_parquet('/Volumes/VERBATIM HD/Dark-MAGA-Investigation/data/trades.parquet')").fetchone() if False else "")
