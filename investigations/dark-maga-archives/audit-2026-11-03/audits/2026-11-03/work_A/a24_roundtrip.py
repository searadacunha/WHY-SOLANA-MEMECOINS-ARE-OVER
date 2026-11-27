#!/usr/bin/env python3
"""Auditeur A. Allers-retours rapides dans les achats rapportés : un achat revendu par le même propriétaire en moins de 10 s n'est pas une accumulation. Parseur propre (a15_leg). DMAGA seulement."""
import re, duckdb
A = "/Volumes/VERBATIM HD/Dark-MAGA-Investigation/audits_work/A"
ROOT = "REDACTED_HOME/Projects/Dark-MAGA-Investigation"
con = duckdb.connect(":memory:", config={"memory_limit": "450MB", "threads": 2, "temp_directory": A + "/duck24", "preserve_insertion_order": False})
con.execute("SET TimeZone='UTC'")
def show(n, s, *a):
    print(n, con.execute(s, *a).fetchall(), flush=True)
LEG = f"read_parquet('{A}/a15_leg.parquet')"
con.execute(f"""COPY (WITH s AS (SELECT owner, signature, t, slot, tx_index, dmaga, sol, sg, lead(t) OVER (PARTITION BY owner ORDER BY slot, tx_index) nt, lead(dmaga) OVER (PARTITION BY owner ORDER BY slot, tx_index) nd FROM {LEG})
     SELECT *, (dmaga>0 AND nd<0 AND nt-t<=10) rt FROM s) TO '{A}/a24_rt.parquet' (FORMAT parquet, COMPRESSION zstd)""")
R = f"read_parquet('{A}/a24_rt.parquet')"
WINIG, LOW, S, HIGH = 1721577749, 1721588607, 1721588400, 1721590213
for n, a, b in (("6 h avant visuel à borne basse", WINIG - 21600, LOW), ("3 h avant Winig", WINIG - 10800, WINIG), ("24 h avant S", S - 86400, S), ("3 h avant S", S - 10800, S), ("fenêtre Musk", LOW, HIGH), ("24 h après borne haute", HIGH, HIGH + 86400), ("toute l'histoire", 0, 1800000000)):
    show(n + " : SOL acheté, dont revendu <=10 s, part %, par non-signataires", f"SELECT round(sum(-sol)/1e9,1), round(sum(CASE WHEN rt THEN -sol ELSE 0 END)/1e9,1), round(100.0*sum(CASE WHEN rt THEN -sol ELSE 0 END)/sum(-sol),1), round(sum(CASE WHEN NOT sg THEN -sol ELSE 0 END)/1e9,1) FROM {R} WHERE dmaga>0 AND t>={a} AND t<{b}")
txt = open(ROOT + "/reports/EARLY_BUYERS.md").read()
sec = txt.split("## Plus gros acheteurs dans les 6 h")[1].split("\n## ")[0]
top = re.findall(r"\| `(\w+)` \|", sec)[:12]
for o in top:
    show(o[:10] + " dans la fenêtre du tableau : SOL acheté, revendu <=10 s, SOL vendu même fenêtre, signataire", f"SELECT round(sum(CASE WHEN dmaga>0 THEN -sol ELSE 0 END)/1e9,2), round(sum(CASE WHEN rt THEN -sol ELSE 0 END)/1e9,2), round(sum(CASE WHEN dmaga<0 THEN sol ELSE 0 END)/1e9,2), bool_or(sg) FROM {R} WHERE owner=? AND t>={WINIG - 21600} AND t<{LOW}", [o])
show("top 15 acheteurs de l'histoire : part allers-retours <=10 s, signataire", f"""SELECT owner, round(sum(-sol)/1e9) a, round(100.0*sum(CASE WHEN rt THEN -sol ELSE 0 END)/sum(-sol),1), bool_or(sg), count(*) FROM {R} WHERE dmaga>0 GROUP BY 1 ORDER BY a DESC LIMIT 15""")
