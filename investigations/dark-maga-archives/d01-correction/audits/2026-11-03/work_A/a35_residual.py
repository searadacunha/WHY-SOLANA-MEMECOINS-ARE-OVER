#!/usr/bin/env python3
"""Auditeur A. Attribution de swap_other à l'autorité partagée, et résiduels du rapport contre le dernier solde vu du compte de jetons."""
import duckdb
A = "/Volumes/VERBATIM HD/Dark-MAGA-Investigation/audits_work/A"
B = "/Volumes/VERBATIM HD/Dark-MAGA-Investigation/data"
con = duckdb.connect(":memory:", config={"memory_limit": "400MB", "threads": 2, "temp_directory": A + "/duck35", "preserve_insertion_order": False})
def show(n, s, *a):
    print(n, con.execute(s, *a).fetchall(), flush=True)
T = f"read_parquet('{B}/trades.parquet')"
show("swap_other par présence de GpMZbSM2", f"SELECT position('GpMZbSM2' in venue)>0, count(*), round(sum(abs(token_delta))/1e12,2) FROM {T} WHERE kind='swap_other' GROUP BY 1")
OO = f"read_parquet('{A}/a19_only_own.parquet')"
show("seulement propre, swap_other, par présence de GpMZbSM2", f"""SELECT position('GpMZbSM2' in k.venue)>0, count(*), round(sum(abs(o.sol))/1e9,1) FROM {OO} o JOIN (SELECT DISTINCT signature, owner, kind, venue FROM {T}) k ON o.signature=k.signature AND o.owner=k.owner WHERE k.kind='swap_other' GROUP BY 1""")
show("lignes swap dont le SOL diffère (> 2 lamports) du propre, par présence de GpMZbSM2", f"""SELECT position('GpMZbSM2' in t.venue)>0, count(*), round(sum(abs(t.sol_lamports-l.sol))/1e9,1) FROM read_parquet('{A}/a15_trd.parquet') t JOIN read_parquet('{A}/a15_leg.parquet') l ON t.signature=l.signature AND t.owner=l.owner WHERE abs(t.sol_lamports-l.sol)>2 GROUP BY 1""")
OA = f"read_parquet('{A}/a13_oa.parquet')"
con.execute(f"CREATE TEMP TABLE last AS SELECT owner o, sum(p)/1e12 m FROM (SELECT account, arg_max(owner,(slot,tx_index)) owner, arg_max(post,(slot,tx_index)) p FROM {OA} GROUP BY 1) GROUP BY 1")
show("25 plus gros résiduels de wallets.parquet : résiduel M, dernier solde vu M", f"""SELECT w.owner, round(w.residual_qty/1e6,2), round(coalesce(l.m,0),2), round(w.transfer_in_qty/1e6,1), round(w.transfer_out_qty/1e6,1), w.completeness FROM read_parquet('{B}/wallets.parquet') w LEFT JOIN last l ON l.o=w.owner WHERE w.owner NOT IN (SELECT address FROM read_parquet('{B}/nodes.parquet') WHERE kind IN ('router','venue','cex')) ORDER BY w.residual_qty DESC LIMIT 25""")
show("somme des résiduels (M), wallets", f"SELECT round(sum(residual_qty)/1e6,1), count(*) FROM read_parquet('{B}/wallets.parquet')")
