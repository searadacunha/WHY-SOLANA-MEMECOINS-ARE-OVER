#!/usr/bin/env python3
"""Continuité des réserves DMAGA de chaque venue. Rapporte les ruptures, ne les cache pas : reports/data_checks/venue_chain.csv."""
import csv
from pathlib import Path

from dmaga.db import connect
from dmaga.venues import load

con = connect()
v = load()
rows = con.execute("""WITH s AS (SELECT vault, signature, slot, tx_index, block_time, pre, post FROM vault WHERE vault NOT IN
      ('5HuEsLbebeuottMsFW3hHcXTrKVsu3WUNSQnSr6aX4eL','3p7DbnWekWjtMQkey6fp1emdwXbAAxecnYuD5eU9ZZPH')),
      o AS (SELECT *, lag(post) OVER (PARTITION BY vault ORDER BY slot, tx_index) p FROM s)
      SELECT vault, count(*), sum(CASE WHEN p IS NOT NULL AND p<>pre THEN 1 ELSE 0 END),
             sum(CASE WHEN p IS NOT NULL AND p<>pre THEN abs(pre-p) ELSE 0 END)/1e6, sum(abs(post-pre))/1e6 FROM o GROUP BY 1 ORDER BY 2 DESC""").fetchall()
Path("reports/data_checks").mkdir(parents=True, exist_ok=True)
with open("reports/data_checks/venue_chain.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["reserve", "n_tx", "ruptures", "jetons_manquants", "jetons_vus"])
    w.writerows(rows)
tx = sum(r[1] for r in rows)
br = sum(r[2] for r in rows)
miss = sum(r[3] for r in rows)
seen = sum(r[4] for r in rows)
print(f"réserves={len(rows)} tx={tx} ruptures={br} jetons manquants={miss:,.0f} jetons vus={seen:,.0f} part manquante={100 * miss / max(seen, 1):.2f} %")
for r in rows[:8]:
    print(r[0][:12], r[1], "ruptures", r[2], "manquants", round(r[3]), "vus", round(r[4]))
