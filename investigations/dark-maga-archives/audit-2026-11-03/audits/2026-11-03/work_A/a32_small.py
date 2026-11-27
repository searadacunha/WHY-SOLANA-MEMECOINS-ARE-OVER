#!/usr/bin/env python3
"""Auditeur A. Petits recoupements : fenêtre touchée par les doublons, transactions de vault sans ligne swap, écart de C05c, volume du vault contre lignes."""
import duckdb
A = "/Volumes/VERBATIM HD/Dark-MAGA-Investigation/audits_work/A"
B = "/Volumes/VERBATIM HD/Dark-MAGA-Investigation/data"
con = duckdb.connect(":memory:", config={"memory_limit": "450MB", "threads": 2, "temp_directory": A + "/duck32", "preserve_insertion_order": False})
con.execute("SET TimeZone='UTC'")
def show(n, s, *a):
    print(n, con.execute(s, *a).fetchall(), flush=True)
T = f"read_parquet('{B}/trades.parquet')"
D = f"(SELECT DISTINCT signature, kind, owner, token_delta, sol_lamports, block_time FROM {T})"
for n, a, b in (("retrait_plus_7j", 1721745389, 1722350189), ("zone de chevauchement 24/07 00:00-05:36:29", 1721779200, 1721799389), ("musk_6h_24h", 1721611813, 1721676613)):
    show(n + " : achats, ventes, lignes (tel)", f"SELECT round(sum(CASE WHEN token_delta>0 THEN -sol_lamports ELSE 0 END)/1e9,2), round(sum(CASE WHEN token_delta<0 THEN sol_lamports ELSE 0 END)/1e9,2), count(*) FROM {T} WHERE kind='swap' AND block_time>={a} AND block_time<{b}")
    show(n + " : achats, ventes, lignes (dédoublonné)", f"SELECT round(sum(CASE WHEN token_delta>0 THEN -sol_lamports ELSE 0 END)/1e9,2), round(sum(CASE WHEN token_delta<0 THEN sol_lamports ELSE 0 END)/1e9,2), count(*) FROM {D} WHERE kind='swap' AND block_time>={a} AND block_time<{b}")
show("doublons hors zone de chevauchement, par source", f"""WITH d AS (SELECT signature, source, kind, owner, token_delta, any_value(block_time) t, count(*) n FROM {T} GROUP BY 1,2,3,4,5 HAVING count(*)>1)
    SELECT source, (t>=1721779200 AND t<1721799389) z, count(*), sum(n-1) FROM d GROUP BY 1,2 ORDER BY 1,2""")
TX = f"read_parquet('{A}/a15_tx.parquet')"
show("vault Raydium : achats SOL, ventes SOL, tx", f"SELECT round(sum(CASE WHEN ds>0 AND dt<0 THEN ds ELSE 0 END)/1e9,1), round(sum(CASE WHEN ds<0 AND dt>0 THEN -ds ELSE 0 END)/1e9,1), sum((ds>0 AND dt<0)::int), sum((ds<0 AND dt>0)::int), sum((ds<>0 AND dt<>0 AND (ds>0)=(dt>0))::int) FROM {TX} WHERE NOT failed")
show("tx de swap vault sans ligne swap dans trades : n, SOL, kinds", f"""WITH v AS (SELECT signature, ds, dt, t FROM {TX} WHERE NOT failed AND ds<>0 AND dt<>0 AND (ds>0)<>(dt>0)), s AS (SELECT DISTINCT signature FROM {T} WHERE kind='swap')
    SELECT count(*), round(sum(abs(ds))/1e9,1), min(t), max(t) FROM v ANTI JOIN s USING (signature)""")
show("  kinds de ces tx", f"""WITH v AS (SELECT signature, ds FROM {TX} WHERE NOT failed AND ds<>0 AND dt<>0 AND (ds>0)<>(dt>0)), s AS (SELECT DISTINCT signature FROM {T} WHERE kind='swap'), o AS (SELECT * FROM v ANTI JOIN s USING (signature))
    SELECT k.kind, count(DISTINCT o.signature), round(sum(abs(o.ds))/1e9,1) FROM o JOIN (SELECT DISTINCT signature, kind FROM {T}) k USING (signature) GROUP BY 1 ORDER BY 3 DESC""")
show("écart de C05c : achat vault de l'heure suivante sans ligne swap", f"""WITH v AS (SELECT signature, ds, dt, t FROM {TX} WHERE NOT failed AND ds>0 AND dt<0 AND t>=1721590213 AND t<1721593813), s AS (SELECT DISTINCT signature FROM {T} WHERE kind='swap')
    SELECT v.signature, v.ds/1e9, v.t FROM v ANTI JOIN s USING (signature)""")
