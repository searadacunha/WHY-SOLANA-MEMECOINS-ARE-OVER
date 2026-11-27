#!/usr/bin/env python3
"""flows_rows.csv.gz -> flows_all.parquet (sans dédoublonnage global : trop de mémoire). Le même transfert peut figurer dans plusieurs requêtes :
toute somme doit passer par SELECT DISTINCT sig,src,dst,mint,raw,ins,inner_ sur un sous-ensemble filtré. Tri par mint pour lire vite."""
import duckdb
G = "/Volumes/VERBATIM HD/Dark-MAGA-Investigation/audits_work/G/"
con = duckdb.connect(":memory:", config={"memory_limit": "500MB", "threads": 1, "temp_directory": G + "duck", "preserve_insertion_order": False})
con.execute("SET TimeZone='UTC'")
con.execute(f"""COPY (SELECT wallet,query,truncated trunc,sig,bt,slot,src,dst,mint,raw,dec,txidx,ins,"inner" inner_ FROM read_csv('{G}flows_rows.csv.gz',header=true,types={{'raw':'DOUBLE','src':'VARCHAR','dst':'VARCHAR','sig':'VARCHAR','dec':'VARCHAR','mint':'VARCHAR'}}))
 TO '{G}flows_all.parquet' (FORMAT PARQUET, COMPRESSION ZSTD, ROW_GROUP_SIZE 50000)""")
print(con.execute(f"SELECT count(*) FROM '{G}flows_all.parquet'").fetchone())
print(con.execute(f"SELECT mint,count(*) c,sum(raw) FROM '{G}flows_all.parquet' GROUP BY 1 ORDER BY c DESC LIMIT 8").fetchall())
