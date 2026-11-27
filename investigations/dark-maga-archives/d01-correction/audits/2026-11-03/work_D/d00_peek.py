# Schéma des parquets et forme d'une transaction brute. Lecture seule.
import duckdb, gzip, json, glob, os, sys
BIG='/Volumes/VERBATIM HD/Dark-MAGA-Investigation/data'
RAW='/Volumes/VERBATIM HD/Dark-MAGA-Investigation/raw'
TMP='/Volumes/VERBATIM HD/Dark-MAGA-Investigation/audits_work/D/duck'
os.makedirs(TMP,exist_ok=True)
con=duckdb.connect(':memory:',config={'memory_limit':'800MB','threads':2,'temp_directory':TMP})
con.execute("SET TimeZone='UTC'")
for f in ['trades','wallets','funding_edges','exit_flows','link_edges','token_edges','nodes']:
    print('==',f)
    print(con.execute(f"DESCRIBE SELECT * FROM read_parquet('{BIG}/{f}.parquet')").fetchall())
    print(con.execute(f"SELECT count(*) FROM read_parquet('{BIG}/{f}.parquet')").fetchone())
p=sorted(x for x in glob.glob(RAW+'/full_pool/t1721601351/p*.jsonl.gz'))[0]
with gzip.open(p,'rt') as fh:
    t=json.loads(fh.readline())
print(json.dumps(t)[:3000])
