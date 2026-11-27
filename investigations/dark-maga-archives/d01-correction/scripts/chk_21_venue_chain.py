#!/usr/bin/env python3
"""Continuité des réserves de chaque venue, côté DMAGA et côté WSOL. Rapporte les ruptures, ne les cache pas : reports/data_checks/venue_chain.csv."""
import csv
from pathlib import Path

from dmaga.config import MINT
from dmaga.db import connect

con = connect(mem="700MB")
rows = con.execute(f"""WITH s AS (SELECT vault, mint, signature, slot, tx_index, block_time, pre, post FROM vault WHERE vault NOT IN
      ('5HuEsLbebeuottMsFW3hHcXTrKVsu3WUNSQnSr6aX4eL','3p7DbnWekWjtMQkey6fp1emdwXbAAxecnYuD5eU9ZZPH')),
      o AS (SELECT *, lag(post) OVER (PARTITION BY vault ORDER BY slot, tx_index) p FROM s)
      SELECT CASE WHEN mint='{MINT}' THEN 'DMAGA' ELSE 'WSOL' END cote, vault, count(*), sum(CASE WHEN p IS NOT NULL AND p<>pre THEN 1 ELSE 0 END),
             sum(CASE WHEN p IS NOT NULL AND p<>pre THEN abs(pre-p) ELSE 0 END)/(CASE WHEN mint='{MINT}' THEN 1e6 ELSE 1e9 END),
             sum(abs(post-pre))/(CASE WHEN mint='{MINT}' THEN 1e6 ELSE 1e9 END) FROM o GROUP BY 1, 2, mint ORDER BY 1, 3 DESC""").fetchall()
Path("reports/data_checks").mkdir(parents=True, exist_ok=True)
with open("reports/data_checks/venue_chain.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["cote", "reserve", "n_tx", "ruptures", "manquants", "vus"])
    w.writerows(rows)
for cote in ("DMAGA", "WSOL"):
    c = [r for r in rows if r[0] == cote]
    miss, seen = sum(r[4] for r in c), sum(r[5] for r in c)
    print(f"{cote} : réserves={len(c)} tx={sum(r[2] for r in c)} ruptures={sum(r[3] for r in c)} manquants={miss:,.2f} vus={seen:,.0f} part manquante={100 * miss / max(seen, 1):.2f} %")
    for r in c[:6]:
        print(" ", r[1][:12], r[2], "ruptures", r[3], "manquants", round(r[4], 2), "vus", round(r[5]))
