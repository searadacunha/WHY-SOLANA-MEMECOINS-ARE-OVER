import duckdb,csv,time,json
W="/Volumes/VERBATIM HD/Dark-MAGA-Investigation/audits_work/C"
B="/Volumes/VERBATIM HD/Dark-MAGA-Investigation/data"
c=duckdb.connect();c.execute(f"SET memory_limit='250MB';SET threads=1;SET TimeZone='UTC';SET temp_directory='{W}/tmp';")
H='Habp5bncMSsBC3vkChyebepym5dcTNRYeg2LVG464E96'
print(c.execute(f"SELECT t.bt,t.sig,a.pre,a.post FROM '{W}/ta.parquet' a JOIN '{W}/tx.parquet' t USING(tid) WHERE a.owner_post='{H}' OR a.owner_pre='{H}' ORDER BY t.bt").fetchall())
print(c.execute(f"SELECT first_sell_time,last_sell_time,sold_sol,sold_qty FROM '{B}/wallets.parquet' WHERE owner='{H}'").fetchall())
print(c.execute(f"SELECT signature,block_time,kind,token_delta,sol_lamports FROM '{B}/trades.parquet' WHERE owner='{H}'").fetchall())
