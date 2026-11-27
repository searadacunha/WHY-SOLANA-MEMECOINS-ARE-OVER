"""Vérifications avant correction (lecture seule) : comptes de GpMZbSM2 sur DMAGA, recouvrement de la tranche t1721777789."""
import duckdb, json
BIG = "/Volumes/VERBATIM HD/Dark-MAGA-Investigation/data"
D = "/Volumes/VERBATIM HD/Dark-MAGA-Investigation/audits_work/D"
con = duckdb.connect(":memory:", config={"memory_limit": "600MB", "threads": 2, "temp_directory": D + "/duck", "preserve_insertion_order": False})
GP = "GpMZbSM2GgvTKHJirzeGfMFoaZ8UR2X7F4v8vHTvxFbL"
print("comptes DMAGA de GpMZ", con.execute(f"SELECT account,count(*),min(bt),max(bt),min(pre),max(post) FROM read_parquet('{D}/d01_acct.parquet') WHERE owner='{GP}' GROUP BY 1").fetchall())
print("venues.json GpMZ", json.load(open("reports/data_checks/venues.json")).get(GP))
s = f"{BIG}/trades_shards"
print("tranche après minuit, lignes", con.execute(f"SELECT count(*) FROM read_parquet('{s}/full_pool_t1721777789.parquet') WHERE block_time>=1721779200").fetchone())
print("dont absentes des autres tranches pool", con.execute(f"""SELECT count(*) FROM read_parquet('{s}/full_pool_t1721777789.parquet') a WHERE block_time>=1721779200 AND signature NOT IN (SELECT signature FROM read_parquet('{s}/full_pool_t1721779200.parquet'))""").fetchone())
print("min max t", con.execute(f"SELECT min(block_time),max(block_time) FROM read_parquet('{s}/full_pool_t1721779200.parquet')").fetchone())
fe = f"read_parquet('{BIG}/funding_edges.parquet')"
print("mêmes clés, même requête, montants", con.execute(f"SELECT query,count(*),sum(n),round(sum(mx-mn)) FROM (SELECT query,wallet,signature,src,count(*) n,max(sol) mx,min(sol) mn FROM {fe} WHERE sol<1e6 GROUP BY 1,2,3,4 HAVING count(*)>1) GROUP BY 1").fetchall())
print("entre requêtes", con.execute(f"SELECT count(*) FROM (SELECT wallet,signature,src FROM {fe} WHERE sol<1e6 GROUP BY 1,2,3 HAVING count(DISTINCT query)>1)").fetchone())
print("entre requêtes, somme par requête égale", con.execute(f"""SELECT count(*),sum((abs(a-b)<1e-9)::int) FROM (SELECT wallet,signature,src,sum(CASE WHEN query='in_before' THEN sol END) a,sum(CASE WHEN query='first_in' THEN sol END) b FROM {fe} WHERE sol<1e6 GROUP BY 1,2,3 HAVING count(DISTINCT query)>1)""").fetchone())
print("exemples", con.execute(f"SELECT wallet,signature,src,query,sol FROM {fe} WHERE (wallet,signature,src) IN (SELECT wallet,signature,src FROM {fe} WHERE sol<1e6 GROUP BY 1,2,3 HAVING count(*)>1) ORDER BY 2,4 LIMIT 8").fetchall())
print("decimales", )
