import duckdb,glob,json
f=[x for x in glob.glob('/Volumes/VERBATIM HD/Dark-MAGA-Investigation/data/controls/swaps/*.parquet') if '/._' not in x]
con=duckdb.connect(config={'memory_limit':'300MB','threads':1})
print(con.execute(f"DESCRIBE SELECT * FROM read_parquet('{f[0]}')").fetchall())
print(con.execute(f"SELECT * FROM read_parquet('{f[0]}') LIMIT 3").fetchall())
print(f[0])
L=[json.loads(l) for l in open('/Volumes/VERBATIM HD/Dark-MAGA-Investigation/data/controls/selection.jsonl')]
print(len(L),L[0],L[1])
import collections
print(collections.Counter(x.get('status') for x in L))
print(json.dumps(json.load(open('etude_final/tables/tests.json')))[:1500])
