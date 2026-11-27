#!/usr/bin/env python3
"""Auditeur A. Chaîne des réserves des venues sur le parseur propre, comptes de frais, adresses non signataires, compte sans flux. Lit a13_oa.parquet (a13b)."""
import sys, duckdb
sys.path.insert(0, "REDACTED_HOME/Projects/Dark-MAGA-Investigation")
from dmaga.venues import load as lv
from dmaga.labels import load as ll
A = "/Volumes/VERBATIM HD/Dark-MAGA-Investigation/audits_work/A"
B = "/Volumes/VERBATIM HD/Dark-MAGA-Investigation/data"
con = duckdb.connect(":memory:", config={"memory_limit": "500MB", "threads": 2, "temp_directory": A + "/duck18", "preserve_insertion_order": False})
con.execute("SET TimeZone='UTC'")
def show(n, s, *a):
    print(n, con.execute(s, *a).fetchall(), flush=True)
V = lv()
con.execute("CREATE TEMP TABLE ven(a VARCHAR, n VARCHAR)")
con.executemany("INSERT INTO ven VALUES (?,?)", [[a, n] for a, n in V.items()])
OA = f"read_parquet('{A}/a13_oa.parquet')"
show("réserves des venues : comptes, tx, ruptures, jetons M manquants", f"SELECT count(DISTINCT account), count(*), sum((pp IS NOT NULL AND pp<>pre)::int), round(sum(CASE WHEN pp IS NOT NULL AND pp<>pre THEN abs(pre-pp) ELSE 0 END)/1e12,3) FROM {OA} WHERE owner IN (SELECT a FROM ven)")
show("  par type de venue", f"SELECT n, count(DISTINCT account), count(*), sum((pp IS NOT NULL AND pp<>pre)::int) FROM {OA} JOIN ven ON owner=a GROUP BY 1 ORDER BY 3 DESC")
show("  ruptures, détail", f"SELECT owner, account, signature, t, pre, pp FROM {OA} WHERE owner IN (SELECT a FROM ven) AND pp IS NOT NULL AND pp<>pre ORDER BY abs(pre-pp) DESC LIMIT 15")
show("  comptes de venues hors du compte project (a02 voit plus de réserves ?)", f"SELECT count(DISTINCT account), count(DISTINCT owner) FROM {OA} WHERE owner IN (SELECT a FROM ven)")
T = f"read_parquet('{B}/trades.parquet')"
show("fee_share : bénéficiaires", f"SELECT owner, count(*), round(sum(abs(token_delta))/1e12,3) FROM {T} WHERE kind='fee_share' GROUP BY 1 ORDER BY 3 DESC LIMIT 12")
show("PNLCQc dans trades", f"SELECT kind, count(*), round(sum(abs(token_delta))/1e12,3) FROM {T} WHERE owner='PNLCQcVCD26aC7ZWgRyr5ptfaR7bBrWdTFgRWwu2tvF' GROUP BY 1")
# non signataires classés wallet qui concentrent le volume, programme associé
for o in ("5V97uEb4ZNuXFudphU5nwUapRmt7a2V51TbULQvPJwnx", "AD65fgYti96iSSzSPaNazV9Bs29m7JbNomGjG4Cp5WFS", "BmanDqQELF7QY5uRPw8vg3eMjR74WZnszKmNbLJKkay3", "4ToQp55myvfpeprgKuqGbDqyji9Ezm7CZg7QbcTpL33S", "8aHVf4T3t4Z2kjnNojLh87zswhH21EU2iFnVoadN3MXx"):
    show(o[:8] + " signataire ?, kinds", f"SELECT kind, count(*), round(sum(abs(sol_lamports))/1e9), min(block_time), max(block_time), sum((position(owner in signers)>0)::int) FROM {T} WHERE owner=? GROUP BY 1", [o])
    show("   tenue moyenne : achat puis vente, en secondes (appariement ordonné)", f"""WITH s AS (SELECT block_time t, token_delta d, row_number() OVER (ORDER BY slot, tx_index) r FROM (SELECT DISTINCT signature, block_time, slot, tx_index, token_delta FROM {T} WHERE kind='swap' AND owner=?)),
        n AS (SELECT t, d, lead(t) OVER (ORDER BY r) nt, lead(d) OVER (ORDER BY r) nd FROM s) SELECT count(*), median(nt-t), quantile_cont(nt-t,0.9), sum((d>0 AND nd<0)::int) FROM n WHERE nt IS NOT NULL""", [o])
    show("   programmes (top)", f"""SELECT progs, count(*) n FROM (SELECT any_value(progs) progs FROM read_parquet('{A}/a15_tx.parquet') WHERE signature IN (SELECT signature FROM read_parquet('{A}/a15_ow.parquet') WHERE owner=?) GROUP BY signature) GROUP BY 1 ORDER BY 2 DESC LIMIT 2""", [o])
show("Comptes de tx : n_dmaga=0, non échouées (toutes lectures)", f"SELECT sum((n_dmaga=0 AND NOT failed)::int), sum(failed::int), count(*) FROM read_parquet('{A}/a02_tx.parquet')")
show("burn : signatures, jetons", f"SELECT count(*), sum(s)/1e6 FROM (SELECT signature, any_value(dmaga_sum) s FROM read_parquet('{A}/a02_tx.parquet') WHERE dmaga_sum<0 GROUP BY 1)")
W = f"read_parquet('{B}/wallets.parquet')"
show("wallets.parquet", f"SELECT count(*), sum((first_buy_time>1721590213)::int), sum((first_buy_time>1721590213 AND realized_sol>0)::int), sum((realized_sol>0 AND realized_sol<=0.001 AND first_buy_time>1721590213)::int) FROM {W}")
show("completeness, part par libellé", f"SELECT completeness, count(*), round(sum(realized_sol)) FROM {W} GROUP BY 1 ORDER BY 2 DESC")
