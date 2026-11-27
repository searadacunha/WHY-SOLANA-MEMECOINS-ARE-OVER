#!/usr/bin/env python3
"""Caractérise chaque adresse du graphe de jetons : wallet ordinaire ou service.

Règle, fixée avant de regarder les clusters :
- `venue` : réserve de pool (dmaga/venues.py) ou programme connu.
- `cex` : échange de la liste Dune.
- `service` : tout autre compte étiqueté (Jupiter, exécutants et escrows DCA, ponts).
- `router` : au moins 20 contreparties distinctes ET au moins 50 % de ses mouvements DMAGA sont
  des aller-retour dans la même transaction (jetons reçus et renvoyés dans la même signature).
- `hub` : au moins 50 contreparties distinctes sur DMAGA, sans pass-through.
- `wallet` : le reste. Seules les arêtes entre `wallet` servent aux clusters de propriété.
Sortie : BIG/nodes.parquet. Lit trades et token_edges, sans réseau.
"""
from collections import defaultdict

import pyarrow as pa
import pyarrow.parquet as pq

from dmaga.config import RAW
from dmaga.db import connect
from dmaga.labels import INFRA, label, load as load_labels
from dmaga.paths import BIG, exige_v2
from dmaga.venues import load as load_venues

exige_v2()
con = connect(mem="700MB")
venues = load_venues()
con.execute(f"CREATE VIEW e AS SELECT * FROM read_parquet('{BIG}/token_edges.parquet')")

counter = defaultdict(set)
sent = defaultdict(set)
recv = defaultdict(set)
vol = defaultdict(float)
for sig, a, b, q in con.execute("SELECT signature, src, dst, qty FROM e WHERE dst <> '(multiple)'").fetchall():
    counter[a].add(b)
    counter[b].add(a)
    sent[a].add(sig)
    recv[b].add(sig)
    vol[a] += q
    vol[b] += q

# un wallet d'exécution apparaît aussi côté flux brut : `dmaga_all` y montre le pass-through
rows = []
for a in counter:
    both = sent[a] & recv[a]
    total = len(sent[a] | recv[a])
    pt = len(both) / total if total else 0.0
    lab = label(a)
    if a in venues or a == "(multiple)":
        kind = "venue"
    elif lab:
        kind = "cex" if load_labels()[a][1].startswith("dune") else "venue" if a in INFRA else "service"
    elif len(counter[a]) >= 20 and pt >= 0.5:
        kind = "router"
    elif len(counter[a]) >= 50:
        kind = "hub"
    else:
        kind = "wallet"
    rows.append({"address": a, "kind": kind, "label": lab, "n_counterparts": len(counter[a]), "n_tx": total,
                 "pass_through": round(pt, 3), "qty_moved": vol[a]})

# les wallets d'exécution déjà vus dans `dmaga_all` : même règle, mesurée sur leurs lignes brutes
import gzip
import json

for d in (RAW / "flows").iterdir():
    if d.name.startswith("._") or not (d / "dmaga_all.json.gz").exists():
        continue
    j = json.load(gzip.open(d / "dmaga_all.json.gz"))
    a = d.name
    s_in, s_out, others = set(), set(), set()
    for x in j["rows"]:
        if x.get("fromUserAccount") == a:
            s_out.add(x["signature"])
            others.add(x.get("toUserAccount"))
        elif x.get("toUserAccount") == a:
            s_in.add(x["signature"])
            others.add(x.get("fromUserAccount"))
    total = len(s_in | s_out)
    pt = len(s_in & s_out) / total if total else 0.0
    if len(others) >= 20 and pt >= 0.5:
        for r in rows:
            if r["address"] == a:
                r.update(kind="router", pass_through=round(pt, 3), n_counterparts=max(r["n_counterparts"], len(others)))
                break
        else:
            rows.append({"address": a, "kind": "router", "label": label(a), "n_counterparts": len(others), "n_tx": total,
                         "pass_through": round(pt, 3), "qty_moved": 0.0})

pq.write_table(pa.Table.from_pylist(rows), BIG / "nodes.parquet", compression="zstd")
c = defaultdict(int)
for r in rows:
    c[r["kind"]] += 1
print(dict(c))
for r in sorted([x for x in rows if x["kind"] in ("router", "hub")], key=lambda r: -r["n_counterparts"])[:15]:
    print(r["address"], r["kind"], r["n_counterparts"], r["pass_through"])
