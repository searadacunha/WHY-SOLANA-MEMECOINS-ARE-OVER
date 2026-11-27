#!/usr/bin/env python3
"""Auto-contrôle des rapports : toute adresse ou signature citée doit exister dans les données.

Une chaîne base58 de 32 à 88 caractères dans docs/ ou reports/ est cherchée dans trades, token_edges, nodes,
funding_edges, exit_flows, link_edges, le manifeste de la création et les étiquettes. Une chaîne absente fait échouer
le contrôle : c'est ainsi qu'on repère une adresse complétée de mémoire (voir la mémoire piege-hash-complete-de-memoire).
Les fins de lignes `…` (forme tronquée) sont ignorées : une forme tronquée ne prétend pas être une référence.
"""
import gzip
import json
import re
import sys
from pathlib import Path

from dmaga.config import BIG, DATA, RAW
from dmaga.db import connect
from dmaga.labels import load as load_labels

B58 = re.compile(r"(?<![1-9A-HJ-NP-Za-km-z])[1-9A-HJ-NP-Za-km-z]{32,88}(?![1-9A-HJ-NP-Za-km-z…])")
con = connect()
known: set[str] = set(load_labels())
for sql in ("SELECT DISTINCT signature FROM trades", "SELECT DISTINCT owner FROM trades", "SELECT DISTINCT fee_payer FROM trades"):
    known |= {r[0] for r in con.execute(sql).fetchall() if r[0]}
for f, cols in (("token_edges", ("signature", "src", "dst")), ("funding_edges", ("wallet", "src", "signature")),
                ("exit_flows", ("wallet", "dst", "signature")), ("link_edges", ("src", "dst", "signature", "asset")),
                ("nodes", ("address",))):
    p = BIG / f"{f}.parquet"
    if p.exists():
        for c in cols:
            known |= {r[0] for r in con.execute(f"SELECT DISTINCT {c} FROM read_parquet('{p}')").fetchall() if r[0]}
for line in (DATA / "social_wallet_mentions.jsonl").open():
    known.add(json.loads(line).get("adresse_telle_quecrite", ""))
for d in (RAW / "flows").iterdir():
    if d.is_dir() and not d.name.startswith("._"):
        known.add(d.name)

# programmes et comptes vus dans la documentation du dépôt, vérifiés dans les transactions brutes
ALLOW = {"7D7BRcBYepfi77vxySapmeqRNN1wsBBxnFPJGbH5pump", "87g44hEXP7R8ZxoAJtz941tsVftpEXC1LqAFTf2ZHtkH",
         "CRSwXnfF21yHDXdYBVWwCwQ5Ni2A4QuK3qGYis5k7x7k", "5HuEsLbebeuottMsFW3hHcXTrKVsu3WUNSQnSr6aX4eL",
         "3p7DbnWekWjtMQkey6fp1emdwXbAAxecnYuD5eU9ZZPH", "XC78JjRHnSqaysrHiTrhR8eRngFbvX3rrHyRjWEpump",
         "Go5rFkwKpTYGVck7emf4Uop81HBozmHHZfEhe2zJDY5u", "CAMMCzo5YL8w4VFF8KVHrK22GGUsp5VTaW7grrKgrWqK",
         "LBUZKhRxPF3XUpBCjp4YzTKgLccjZhTSDM9YuVaPwxo", "whirLbMiicVdio4qvUfM5KAg6Ct8VwpYzGff3uctyCc",
         "JUP6LkbZbjS1jKKwapdHNy74zcZ3tLUZoi5QNyVTaV4"}
known |= ALLOW
# réponses de la chaîne archivées telles quelles par les scripts de vérification
for extra in (DATA / "group_split.json", DATA / "collector.json", DATA / "prevent_groups.json", Path("reports/data_checks/group_edges_check.json")):
    known |= set(B58.findall(extra.read_text()))
# candidats tiers cités par leur source dans les constats sociaux (Wifejak, homonymes) : présents dans le document, pas dans les données
known |= set(B58.findall(Path("docs/SOCIAL_FINDINGS.md").read_text()))

bad = {}
n = 0
for path in [*Path("docs").glob("*.md"), *Path("reports").glob("*.md")]:
    if path.name in ("SOCIAL_FINDINGS.md", "PRIOR_WORK.md"):  # citations de sources tierces, relues à part
        continue
    for m in B58.finditer(path.read_text()):
        s = m.group(0)
        if s.isdigit() or s.isalpha() and s.islower():
            continue
        n += 1
        if s not in known:
            bad.setdefault(str(path), set()).add(s)
print(f"références vérifiées: {n}, absentes des données: {sum(len(v) for v in bad.values())}")
for p, v in bad.items():
    print(p, sorted(v)[:20])
sys.exit(1 if bad else 0)
