#!/usr/bin/env python3
"""Cohortes par événement, fenêtres temporelles et classements. Descriptif : aucun test ici.

Écrit :
  data/events.json             événements et leur source
  data/cohorts.parquet         pour chaque wallet : premier achat, cohorte, et ce qu'il avait acheté avant chaque événement
  data/windows.csv             volume, wallets, concentration par fenêtre autour des événements
  data/price_hourly.csv        prix du pool Raydium par heure
"""
import csv
import json

import pyarrow as pa
import pyarrow.parquet as pq

from dmaga.config import BIG, DATA
from dmaga.db import connect
from dmaga.venues import load as load_venues

EVENTS = [
    ("creation_mint", 1720922725, "A", "signature fePxr7ER…, slot 277417695"),
    ("migration_raydium", 1720923331, "A", "signature 2zmB9nbU…, slot 277419045"),
    ("pmarca_image_rouge", 1721512043, "A", "post 1814779160377602331, 20/07 21:47:23 UTC"),
    ("kikisknees_elon_mooning", 1721566245, "B", "post 1815006501896872388, 21/07 12:50 UTC, supprimé, texte par la Wayback"),
    ("kikisknees_reponse_musk", 1721577608, "B", "post 1815054158367432804, 21/07 16:00:08 UTC, supprimé, média perdu"),
    ("winig_visuel", 1721577749, "A", "post 1815054750775173447, 21/07 16:02:29 UTC, plus ancienne image exacte archivée"),
    ("annonce_biden", 1721583960, "C", "21/07 17:46 UTC, donnée de la mission, non revérifiée ici"),
    ("musk_borne_basse", 1721588607, "A", "capture Wayback 19:03:27 UTC, ancien avatar"),
    ("musk_envoi_image", 1721589800, "B", "snowflake de l'image 1815105297410666496, 19:23:20 UTC, lecture à confirmer"),
    ("musk_borne_haute", 1721590213, "A", "post 1815107030606385507, 19:30:13 UTC, nouvel avatar visible"),
    ("darkmagacoin_dm", 1721635821, "A", "post 1815298322325811663, 22/07 08:10:21 UTC, déclaration"),
    ("musk_retrait_borne_haute", 1721745389, "A", "capture Wayback, 23/07 14:36:29 UTC"),
]
EV = {n: t for n, t, _, _ in EVENTS}
WINDOWS = [
    ("avant_pmarca", EV["migration_raydium"], EV["pmarca_image_rouge"]),
    ("pmarca_a_winig", EV["pmarca_image_rouge"], EV["winig_visuel"]),
    ("winig_a_biden", EV["winig_visuel"], EV["annonce_biden"]),
    ("biden_a_musk_borne_basse", EV["annonce_biden"], EV["musk_borne_basse"]),
    ("fenetre_musk", EV["musk_borne_basse"], EV["musk_borne_haute"]),
    ("musk_plus_1h", EV["musk_borne_haute"], EV["musk_borne_haute"] + 3600),
    ("musk_1h_6h", EV["musk_borne_haute"] + 3600, EV["musk_borne_haute"] + 6 * 3600),
    ("musk_6h_24h", EV["musk_borne_haute"] + 6 * 3600, EV["musk_borne_haute"] + 24 * 3600),
    ("jusqua_retrait", EV["musk_borne_haute"] + 24 * 3600, EV["musk_retrait_borne_haute"]),
    ("retrait_plus_7j", EV["musk_retrait_borne_haute"], EV["musk_retrait_borne_haute"] + 7 * 86400),
    ("butler_oct", 1727740800, 1729036800),
]

con = connect()
venues = set(load_venues())
excl = venues | {"5Q544fKrFoe6tsEbD7S8EmxGTJYAKtTVhAW5Q5pge4j1", "87g44hEXP7R8ZxoAJtz941tsVftpEXC1LqAFTf2ZHtkH",
                 "39azUYFWPz3VHgKCf3VChUwbpURdCHRxjWVowf5jUJjg", "PNLCQcVCD26aC7ZWgRyr5ptfaR7bBrWdTFgRWwu2tvF"}
con.execute("CREATE TEMP TABLE excl(a VARCHAR)")
con.executemany("INSERT INTO excl VALUES (?)", [[a] for a in excl])

(DATA / "events.json").write_text(json.dumps([{"name": n, "t": t, "fiabilite": f, "source": s} for n, t, f, s in EVENTS], indent=1, ensure_ascii=False))

# fenêtres
rows = []
for name, a, b in WINDOWS:
    r = con.execute(f"""
      WITH s AS (SELECT owner, token_delta, sol_lamports, usdc_raw FROM trades
                 WHERE kind='swap' AND block_time>={a} AND block_time<{b} AND owner NOT IN (SELECT a FROM excl)),
      f AS (SELECT owner, min(block_time) t0 FROM trades WHERE kind='swap' AND token_delta>0 GROUP BY 1),
      b_ AS (SELECT owner, sum(-sol_lamports)/1e9 v FROM s WHERE token_delta>0 GROUP BY 1)
      SELECT (SELECT round(coalesce(sum(-sol_lamports),0)/1e9,2) FROM s WHERE token_delta>0),
             (SELECT round(coalesce(sum(sol_lamports),0)/1e9,2) FROM s WHERE token_delta<0),
             (SELECT count(*) FROM s WHERE token_delta>0), (SELECT count(*) FROM s WHERE token_delta<0),
             (SELECT count(DISTINCT owner) FROM s),
             (SELECT count(*) FROM f WHERE t0>={a} AND t0<{b}),
             (SELECT round(median(v),4) FROM b_), (SELECT round(avg(v),4) FROM b_),
             (SELECT round(100*sum(v)/nullif((SELECT sum(v) FROM b_),0),1) FROM (SELECT v FROM b_ ORDER BY v DESC LIMIT 5))
    """).fetchone()
    rows.append({"window": name, "from_t": a, "to_t": b, "hours": round((b - a) / 3600, 2), "buy_sol": r[0], "sell_sol": r[1], "n_buys": r[2],
                 "n_sells": r[3], "wallets": r[4], "new_buyers": r[5], "median_buy_by_wallet_sol": r[6], "mean_buy_by_wallet_sol": r[7], "top5_share_pct": r[8]})
with (DATA / "windows.csv").open("w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0]))
    w.writeheader()
    w.writerows(rows)

# prix horaire
VD, VS = "5HuEsLbebeuottMsFW3hHcXTrKVsu3WUNSQnSr6aX4eL", "3p7DbnWekWjtMQkey6fp1emdwXbAAxecnYuD5eU9ZZPH"
hp = con.execute(f"""
  WITH d AS (SELECT slot, tx_index, block_time, post FROM vault WHERE vault='{VD}'),
       s AS (SELECT slot, tx_index, post FROM vault WHERE vault='{VS}'),
       j AS (SELECT d.block_time//3600*3600 h, d.slot, d.tx_index, (s.post/1e9)/(d.post/1e6) p FROM d JOIN s USING (slot, tx_index) WHERE d.post>0)
  SELECT h, arg_min(p, (slot, tx_index)), max(p), min(p), arg_max(p, (slot, tx_index)), count(*) FROM j GROUP BY 1 ORDER BY 1""").fetchall()
with (DATA / "price_hourly.csv").open("w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["hour_utc", "open_sol", "high_sol", "low_sol", "close_sol", "n"])
    w.writerows(hp)

# cohortes
cols = ", ".join(f"sum(CASE WHEN block_time<{EV[e]} AND kind='swap' AND token_delta>0 THEN token_delta ELSE 0 END)/1e6 AS bought_before_{e}, "
                 f"sum(CASE WHEN block_time<{EV[e]} AND kind='swap' AND token_delta>0 THEN -sol_lamports ELSE 0 END)/1e9 AS sol_before_{e}"
                 for e in ("winig_visuel", "musk_borne_basse", "musk_borne_haute"))
t = con.execute(f"""SELECT owner, min(CASE WHEN kind='swap' AND token_delta>0 THEN block_time END) first_buy, {cols}
                    FROM trades WHERE owner IS NOT NULL AND owner NOT IN (SELECT a FROM excl) GROUP BY 1""").to_arrow_table()
pq.write_table(t, BIG / "cohorts.parquet", compression="zstd")
print("fenêtres", len(rows), "heures de prix", len(hp), "wallets cohortes", t.num_rows)
for r in rows:
    print(r["window"], r["hours"], "h", "achats", r["buy_sol"], "ventes", r["sell_sol"], "wallets", r["wallets"], "nouveaux", r["new_buyers"], "top5", r["top5_share_pct"])
