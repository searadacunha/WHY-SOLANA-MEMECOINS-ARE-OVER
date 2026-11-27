import duckdb, glob, os
B="/Volumes/VERBATIM HD/Dark-MAGA-Investigation/data_v2"
c=duckdb.connect(":memory:",config={"memory_limit":"800MB","threads":2,"temp_directory":"/Volumes/VERBATIM HD/Dark-MAGA-Investigation/audits_work/H"})
c.execute("SET TimeZone='UTC'")
for f in sorted(os.listdir(B)):
    if f.endswith(".parquet") and not f.startswith("._"):
        d=c.execute(f"DESCRIBE SELECT * FROM read_parquet('{B}/{f}')").fetchall()
        n=c.execute(f"SELECT count(*) FROM read_parquet('{B}/{f}')").fetchone()[0]
        print(f,n,[x[0] for x in d])
