#!/usr/bin/env python3
"""Auditeur A. Résiduels contre derniers soldes vus, tous wallets ; service 3GMsedVP et bénéficiaire 4ToQp55m ; ventes sans SOL pour le vendeur."""
import duckdb
A = "/Volumes/VERBATIM HD/Dark-MAGA-Investigation/audits_work/A"
B = "/Volumes/VERBATIM HD/Dark-MAGA-Investigation/data"
con = duckdb.connect(":memory:", config={"memory_limit": "400MB", "threads": 2, "temp_directory": A + "/duck36", "preserve_insertion_order": False})
def show(n, s, *a):
    print(n, con.execute(s, *a).fetchall(), flush=True)
OA = f"read_parquet('{A}/a13_oa.parquet')"
W = f"read_parquet('{B}/wallets.parquet')"
con.execute(f"CREATE TEMP TABLE last AS SELECT owner o, sum(p)/1e12 m FROM (SELECT account, arg_max(owner,(slot,tx_index)) owner, arg_max(post,(slot,tx_index)) p FROM {OA} GROUP BY 1) GROUP BY 1")
show("somme résiduels M, somme derniers soldes des mêmes wallets M", f"SELECT round(sum(w.residual_qty)/1e6,1), round(sum(coalesce(l.m,0)),1) FROM {W} w LEFT JOIN last l ON l.o=w.owner")
show("wallets résiduel >= 1 M : n, |écart| > 10 %, |écart| M", f"SELECT count(*), sum((abs(w.residual_qty/1e6-coalesce(l.m,0))>0.1*w.residual_qty/1e6)::int), round(sum(abs(w.residual_qty/1e6-coalesce(l.m,0))),1) FROM {W} w LEFT JOIN last l ON l.o=w.owner WHERE w.residual_qty>=1e6")
show("les 8 plus grands écarts", f"SELECT w.owner, round(w.residual_qty/1e6,2), round(coalesce(l.m,0),2), round(w.net_sol_all,1) FROM {W} w LEFT JOIN last l ON l.o=w.owner ORDER BY abs(w.residual_qty/1e6-coalesce(l.m,0)) DESC LIMIT 8")
SVC = "3GMsedVPsXjWR7HYUvwm1YUpvBC2bTgSkXixm4gMXnPk"
TX = f"read_parquet('{A}/a15_tx.parquet')"
show("programme 3GMsedVP : tx, signataires distincts", f"SELECT count(*), count(DISTINCT signers), min(t), max(t) FROM {TX} WHERE progs LIKE '%{SVC}%'")
Q = "4ToQp55myvfpeprgKuqGbDqyji9Ezm7CZg7QbcTpL33S"
show("4ToQp55m dans nodes", f"SELECT * FROM read_parquet('{B}/nodes.parquet') WHERE address='{Q}'")
show("4ToQp55m dans wallets", f"SELECT realized_sol, bought_sol, sold_sol, n_buys, n_sells, n_transfers, completeness, first_buy_time FROM {W} WHERE owner='{Q}'")
show("  financeur de wallets tracés", f"SELECT count(DISTINCT wallet), round(sum(sol)) FROM read_parquet('{B}/funding_edges.parquet') WHERE src='{Q}'")
S = f"read_parquet('{A}/a19_sell.parquet')"
show("ventes signataires 'rien de visible' : part dans une tx 3GMsedVP", f"""SELECT t.progs LIKE '%{SVC}%' svc, count(*), round(sum(s.rec)/1e9,1) FROM {S} s JOIN (SELECT signature, progs FROM {TX}) t USING (signature) WHERE s.cash<0.5*s.rec AND s.rec>0 AND s.stable<=0 AND s.other_opp='' GROUP BY 1""")
show("toutes lignes propres en tx 3GMsedVP : achats, ventes", f"""SELECT round(sum(CASE WHEN l.dmaga>0 THEN -l.sol ELSE 0 END)/1e9,1), round(sum(CASE WHEN l.dmaga<0 THEN l.sol ELSE 0 END)/1e9,1), count(DISTINCT l.owner) FROM read_parquet('{A}/a15_leg.parquet') l JOIN (SELECT signature FROM {TX} WHERE progs LIKE '%{SVC}%') t USING (signature)""")
