#!/usr/bin/env python3
"""Auditeur A. Signataires du programme 3GMsedVP et destination du SOL : piste de contrôle, sans conclusion sur les personnes. Recoupe avec le groupe de 33, les wallets nommés, le top 100."""
import json, re
import duckdb
A = "/Volumes/VERBATIM HD/Dark-MAGA-Investigation/audits_work/A"
B = "/Volumes/VERBATIM HD/Dark-MAGA-Investigation/data"
ROOT = "REDACTED_HOME/Projects/Dark-MAGA-Investigation"
con = duckdb.connect(":memory:", config={"memory_limit": "400MB", "threads": 2, "temp_directory": A + "/duck37", "preserve_insertion_order": False})
SVC = "3GMsedVPsXjWR7HYUvwm1YUpvBC2bTgSkXixm4gMXnPk"
TX = f"read_parquet('{A}/a15_tx.parquet')"
W = f"read_parquet('{B}/wallets.parquet')"
rows = con.execute(f"SELECT signers, count(*), min(t), max(t) FROM {TX} WHERE progs LIKE '%{SVC}%' GROUP BY 1 ORDER BY 2 DESC").fetchall()
print("signataires", len(rows), rows[:12])
s = {x for r in rows for x in r[0].split(",")}
g = json.load(open(ROOT + "/data/prevent_groups.json"))[0]
print("dans le groupe de 33", sorted(s & set(g["members"])))
print("wallets nommés", [n for n in ("H3QsBrrivimFJmSpTXuvig2n1Bh7JuYxrriRSEszT6cc", "GXZvXsD6hxaLeFvQisWpdAwsayJxga7w9EeafhFZG2Ra", "9PrmF8sfoD2YShtWUghrGEYgxwabpnzog8gT1V6LEtdq", "5QhJJcFZu2ashyKyWSTGHcsyo6ZBCbpVuJqeutvQHScd", "8YLEuUtZ4eFMJbf46oNb1CeG6dYFWGyxnQSh9hrgzBzR") if n in s])
txt = open(ROOT + "/reports/TOP_TRADERS.md").read()
sec = txt.split("## 100 plus gros réalisés")[1].split("\n## ")[0]
top = [m for m in re.findall(r"\| \d+ \| `(\w+)` \|", sec)]
print("dans le top 100 réalisés", [(top.index(a) + 1, a) for a in top if a in s])
con.execute("CREATE TEMP TABLE sg(a VARCHAR)")
con.executemany("INSERT INTO sg VALUES (?)", [[a] for a in s])
print("réalisé cumulé des signataires, nb", con.execute(f"SELECT round(sum(realized_sol)), round(sum(bought_sol)), round(sum(sold_sol)), count(*), min(first_buy_time) FROM {W} WHERE owner IN (SELECT a FROM sg)").fetchone())
print("top", con.execute(f"SELECT owner, round(realized_sol), round(bought_sol), round(sold_sol), n_buys, n_sells, first_buy_time FROM {W} WHERE owner IN (SELECT a FROM sg) ORDER BY sold_sol DESC LIMIT 10").fetchall())
LEG = f"read_parquet('{A}/a15_leg.parquet')"
con.execute(f"CREATE TEMP TABLE st AS SELECT signature FROM {TX} WHERE progs LIKE '%{SVC}%'")
S = 1721588400
for n, a, b in (("3 h avant S", S - 10800, S), ("24 h avant S", S - 86400, S), ("3 h avant Winig", 1721577749 - 10800, 1721577749), ("24 h après borne haute", 1721590213, 1721590213 + 86400), ("toute l'histoire", 0, 1800000000)):
    print(n, "achats SOL en tx 3GMsedVP, total, part %, propriétaires", con.execute(f"SELECT round(sum(CASE WHEN signature IN (SELECT signature FROM st) THEN -sol ELSE 0 END)/1e9,1), round(sum(-sol)/1e9,1), round(100.0*sum(CASE WHEN signature IN (SELECT signature FROM st) THEN -sol ELSE 0 END)/sum(-sol),2), count(DISTINCT CASE WHEN signature IN (SELECT signature FROM st) THEN owner END) FROM {LEG} WHERE dmaga>0 AND t>={a} AND t<{b}").fetchone())
