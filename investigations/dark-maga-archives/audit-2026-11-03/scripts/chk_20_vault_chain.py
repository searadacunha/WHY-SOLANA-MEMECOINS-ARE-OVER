#!/usr/bin/env python3
"""Réconciliation comptable du pool : pour chaque vault, le solde après une transaction doit être le
solde avant la suivante, dans l'ordre (slot, tx_index). Toute rupture révèle une transaction absente.

Sortie : reports/data_checks/vault_chain.json. Sort en erreur si une rupture matérielle existe dans la zone couverte.
"""
import json
import sys
from pathlib import Path

from dmaga.db import connect

con = connect(mem="700MB")
report = {}
any_break = False
for vault, name in (("5HuEsLbebeuottMsFW3hHcXTrKVsu3WUNSQnSr6aX4eL", "DMAGA"), ("3p7DbnWekWjtMQkey6fp1emdwXbAAxecnYuD5eU9ZZPH", "WSOL")):
    n = con.execute(f"SELECT count(*) FROM (SELECT DISTINCT signature, slot, tx_index FROM vault WHERE vault='{vault}')").fetchone()[0]
    examples = con.execute(f"""
      WITH s AS (SELECT DISTINCT signature, slot, tx_index, block_time, pre, post FROM vault WHERE vault='{vault}'),
      o AS (SELECT *, lag(post) OVER (ORDER BY slot, tx_index) prev_post FROM s)
      SELECT signature, slot, tx_index, block_time, pre, prev_post, pre-prev_post FROM o
      WHERE prev_post IS NOT NULL AND prev_post<>pre ORDER BY slot""").fetchall()
    last = con.execute(f"SELECT slot, tx_index, post, block_time FROM vault WHERE vault='{vault}' ORDER BY slot DESC, tx_index DESC LIMIT 1").fetchone()
    report[name] = {"vault": vault, "tx": n, "breaks": len(examples), "examples": examples[:20], "last": last}
    # une rupture sous 1 jeton (dépôt direct de poussière sur le vault, sans le pool) reste écrite mais n'arrête pas la chaîne
    material = [e for e in examples if abs(e[6]) >= (10**6 if name == "DMAGA" else 10**7)]
    report[name]["material"] = len(material)
    any_break |= bool(material)
    print(name, "tx", n, "ruptures", len(examples), "matérielles", len(material), "dernier", last)
Path("reports/data_checks").mkdir(parents=True, exist_ok=True)
Path("reports/data_checks/vault_chain.json").write_text(json.dumps(report, indent=1))
sys.exit(1 if any_break else 0)
