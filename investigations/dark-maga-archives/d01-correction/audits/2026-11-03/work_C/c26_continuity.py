#!/usr/bin/env python3
"""Continuite des soldes par compte de jetons : le pre d'une tx doit egaler le post de la tx precedente sur ce compte.
Un ecart = une transaction non vue dans le brut (mint, pool, venue, courbe). Sortie: continuity_gaps.csv + bilan par proprietaire."""
import duckdb, csv
W="/Volumes/VERBATIM HD/Dark-MAGA-Investigation/audits_work/C"
ROOT='REDACTED_HOME/Projects/Dark-MAGA-Investigation/audits/2026-11-03/work_C/'
con=duckdb.connect(); con.execute(f"SET memory_limit='800MB'; SET threads=2; SET TimeZone='UTC'; SET temp_directory='{W}/tmp'; SET preserve_insertion_order=false;")
con.execute(f"""CREATE TEMP TABLE g AS SELECT * FROM (
 SELECT a.token_account, coalesce(nullif(a.owner_post,''),a.owner_pre) owner, a.pre, a.post, x.slot, x.txidx, x.bt, x.sig,
        lag(a.post) OVER w prev_post, lag(x.slot) OVER w prev_slot
 FROM '{W}/ta.parquet' a JOIN (SELECT tid, slot, txidx, bt, sig FROM '{W}/tx.parquet') x USING(tid)
 WINDOW w AS (PARTITION BY a.token_account ORDER BY x.slot, x.txidx)) WHERE (prev_post IS NULL AND pre<>0) OR (prev_post IS NOT NULL AND pre<>prev_post)""")
print('ecarts',con.execute("SELECT count(*), count(DISTINCT token_account), count(DISTINCT owner), sum(abs(pre-coalesce(prev_post,0)))/1e12 FROM g").fetchone())
print('ecarts >=1M',con.execute("SELECT count(*), count(DISTINCT owner), sum(abs(pre-coalesce(prev_post,0)))/1e12 FROM g WHERE abs(pre-coalesce(prev_post,0))>=1000000000000").fetchone())
con.execute(f"COPY (SELECT owner, token_account, pre-coalesce(prev_post,0) gap, prev_slot, slot, bt, sig FROM g WHERE abs(pre-coalesce(prev_post,0))>=1000000000000 ORDER BY abs(gap) DESC) TO '{ROOT}continuity_gaps_1M.csv' (HEADER)")
print(con.execute("SELECT owner, count(*), sum(pre-coalesce(prev_post,0))/1e12 FROM g GROUP BY 1 ORDER BY abs(sum(pre-coalesce(prev_post,0))) DESC LIMIT 15").fetchall())
