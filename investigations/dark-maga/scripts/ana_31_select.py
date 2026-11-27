#!/usr/bin/env python3
"""Liste des wallets à tracer, par règle : gagnants, gros acheteurs, gros détenteurs, premiers acheteurs,
wallets signalés, et voisins directs (transferts de DMAGA hors routeurs) des wallets déjà retenus.

Sortie : BIG/priority_wallets.csv (owner,t_buy,t_sell,raison). Relancer après chaque nouveau PnL.
"""
import csv

from dmaga.config import BIG
from dmaga.db import connect

REPORTED = {"9PrmF8sfoD2YShtWUghrGEYgxwabpnzog8gT1V6LEtdq": "signalé: mission priorité 1",
            "GXZvXsD6hxaLeFvQisWpdAwsayJxga7w9EeafhFZG2Ra": "signalé: @ai_9684xtpa",
            "5QhJJcFZu2ashyKyWSTGHcsyo6ZBCbpVuJqeutvQHScd": "signalé: @0xRamonos",
            "H3QsBrrivimFJmSpTXuvig2n1Bh7JuYxrriRSEszT6cc": "signalé: @ashrobinqt",
            "8YLEuUtZ4eFMJbf46oNb1CeG6dYFWGyxnQSh9hrgzBzR": "créateur"}

con = connect()
con.execute(f"CREATE VIEW w AS SELECT * FROM read_parquet('{BIG}/wallets.parquet')")
con.execute(f"CREATE VIEW n AS SELECT * FROM read_parquet('{BIG}/nodes.parquet')")
con.execute(f"CREATE VIEW e AS SELECT * FROM read_parquet('{BIG}/token_edges.parquet')")
reasons: dict[str, list[str]] = {a: [r] for a, r in REPORTED.items()}


def take(sql, tag):
    for (a,) in con.execute(sql).fetchall():
        reasons.setdefault(a, []).append(tag)


svc = "owner NOT IN (SELECT address FROM n WHERE kind <> 'wallet')"
take(f"SELECT owner FROM w WHERE {svc} ORDER BY realized_sol DESC LIMIT 100", "top100 réalisé")
take(f"SELECT owner FROM w WHERE {svc} ORDER BY net_sol_all DESC LIMIT 100", "top100 net SOL")
take(f"SELECT owner FROM w WHERE {svc} ORDER BY bought_sol DESC LIMIT 100", "top100 acheteurs")
take(f"SELECT owner FROM w WHERE {svc} ORDER BY residual_qty DESC LIMIT 50", "top50 résiduel")
take(f"""SELECT owner FROM w WHERE {svc} AND first_buy_time IS NOT NULL
         ORDER BY first_buy_slot, first_buy_tx_index LIMIT 150""", "150 premiers acheteurs")
take(f"""SELECT owner FROM w WHERE {svc} AND first_buy_time < 1721589800 AND bought_qty >= 1000000
         ORDER BY bought_sol DESC LIMIT 100""", "acheteur ≥ 1 M avant l'avatar")
# voisins directs des wallets retenus, sur des arêtes de transfert entre wallets ordinaires
base = list(reasons)
con.execute("CREATE TEMP TABLE b(a VARCHAR)")
con.executemany("INSERT INTO b VALUES (?)", [[a] for a in base])
take("""WITH ok AS (SELECT address FROM n WHERE kind='wallet')
        SELECT DISTINCT x FROM (
          SELECT dst x, qty FROM e WHERE src IN (SELECT a FROM b) AND dst IN (SELECT address FROM ok) AND dst <> '(multiple)' AND qty >= 100000
          UNION ALL
          SELECT src x, qty FROM e WHERE dst IN (SELECT a FROM b) AND src IN (SELECT address FROM ok) AND qty >= 100000)""",
     "voisin direct ≥ 100 k jetons")

times = {r[0]: r[1:] for r in con.execute("SELECT owner, first_buy_time, first_sell_time FROM w").fetchall()}
n = 0
with (BIG / "priority_wallets.csv").open("w", newline="") as f:
    w = csv.writer(f)
    for a, rs in reasons.items():
        tb, ts = times.get(a, (None, None))
        # un wallet sans achat ni vente : borne à la création, sa fenêtre de financement reste l'avant-lancement
        w.writerow([a, tb or 1720922725, ts or 1721589800, "; ".join(sorted(set(rs)))])
        n += 1
print("wallets à tracer", n)
