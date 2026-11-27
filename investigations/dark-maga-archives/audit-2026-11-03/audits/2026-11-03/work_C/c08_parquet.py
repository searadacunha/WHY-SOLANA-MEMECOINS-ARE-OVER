#!/usr/bin/env python3
"""Convertit tx, ta, ix, flows en parquet (audits_work/C), et construit le fichier des transferts inter-proprietaires."""
import duckdb, time
W="/Volumes/VERBATIM HD/Dark-MAGA-Investigation/audits_work/C"
con=duckdb.connect()
con.execute(f"SET memory_limit='800MB'; SET threads=2; SET TimeZone='UTC'; SET temp_directory='{W}/tmp'; SET preserve_insertion_order=false;")
t=time.time()
for n,types in [("tx",{"sig":"VARCHAR","fee":"BIGINT"}),("ta",{"pre":"BIGINT","post":"BIGINT"}),("ix",{"amount":"BIGINT","ord":"VARCHAR"}),("flows_dmaga",{"amount":"BIGINT","idx":"BIGINT"})]:
    con.execute(f"COPY (SELECT * FROM read_csv('{W}/{n}.csv.gz',header=true,types={types},auto_detect=true,sample_size=20000,all_varchar=false)) TO '{W}/{n}.parquet' (FORMAT parquet, COMPRESSION zstd, ROW_GROUP_SIZE 100000)")
    print(n,con.execute(f"SELECT count(*) FROM '{W}/{n}.parquet'").fetchone(),round(time.time()-t),flush=True)
