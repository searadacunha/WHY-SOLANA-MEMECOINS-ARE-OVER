#!/usr/bin/env python3
"""Clusters financiers à partir d'arêtes réelles, séparées par type de preuve.

Types d'arêtes, du plus fort au plus faible :
  token_direct   transfert de DMAGA entre deux wallets, hors swap, ≥ 100 000 jetons, sans contrepartie en SOL dans la tx
  sol_direct     SOL direct ≥ 0,1 SOL entre deux wallets
  funder_commun  même financeur direct, non service, dans les 72 h avant le premier achat
  sink_commun    même destination de sortie, non service, à moins de 7 jours d'écart
Un nœud `service` (échange, routeur, hub, venue, ou plus de 1 000 signatures récentes sans étiquette) n'est jamais
un lien. Poussière de SOL écartée. Un cluster dit « ces wallets sont reliés par ces transactions », pas « une
même personne » ; la force et les explications alternatives sont écrites avec lui.

Sorties : data/wallet_clusters.parquet, BIG/link_edges.parquet.
"""
import gzip
import json
from collections import defaultdict
from pathlib import Path

import networkx as nx
import pyarrow as pa
import pyarrow.parquet as pq

from dmaga.config import BIG, DATA, RAW
from dmaga.db import connect
from dmaga.labels import label
from dmaga.venues import load as load_venues

FLOWS = RAW / "flows"
venues = load_venues()
INFRA = {"5Q544fKrFoe6tsEbD7S8EmxGTJYAKtTVhAW5Q5pge4j1", "39azUYFWPz3VHgKCf3VChUwbpURdCHRxjWVowf5jUJjg",
         "87g44hEXP7R8ZxoAJtz941tsVftpEXC1LqAFTf2ZHtkH", "PNLCQcVCD26aC7ZWgRyr5ptfaR7bBrWdTFgRWwu2tvF"}
DUST = 0.1

con = connect()
con.execute(f"CREATE VIEW n AS SELECT * FROM read_parquet('{BIG}/nodes.parquet')")
con.execute(f"CREATE VIEW e AS SELECT * FROM read_parquet('{BIG}/token_edges.parquet')")
service = {a for (a,) in con.execute("SELECT address FROM n WHERE kind <> 'wallet'").fetchall()} | INFRA | set(venues)
# activité : plus de 1 000 signatures sur la dernière page = comportement de service ou de bot, jamais un lien de propriété
busy = set()
for d in FLOWS.iterdir():
    p = d / "age.json.gz"
    if d.name.startswith("._") or not p.exists():
        continue
    j = json.load(gzip.open(p))
    if j.get("more") and j.get("recent_page", 0) >= 1000:
        busy.add(d.name)
# une contrepartie jamais tracée mais vue par beaucoup de wallets tracés est traitée comme un service
seen_by = defaultdict(set)
for d in FLOWS.iterdir():
    if d.name.startswith("._") or not d.is_dir():
        continue
    for q in ("in_before", "sol_out_after", "usdc_out_after", "usdt_out_after"):
        p = d / f"{q}.json.gz"
        if not p.exists():
            continue
        for x in json.load(gzip.open(p))["rows"]:
            other = x["toUserAccount"] if q != "in_before" else x["fromUserAccount"]
            if other:
                seen_by[other].add(d.name)
popular = {a for a, s in seen_by.items() if len(s) >= 15}


def bad(a):
    return a is None or a == "(multiple)" or a in service or a in popular or label(a) is not None


edges = []
for sig, a, b, q, t, how in con.execute(
        "SELECT signature, src, dst, qty, block_time, how FROM e WHERE qty >= 100000 AND dst <> '(multiple)'").fetchall():
    if bad(a) or bad(b):
        continue
    edges.append({"src": a, "dst": b, "type": "token_direct", "amount": q, "asset": "DMAGA", "block_time": t, "signature": sig})

funded = defaultdict(list)
sinks = defaultdict(list)
first_buy = dict(con.execute(f"SELECT owner, first_buy_time FROM read_parquet('{BIG}/wallets.parquet')").fetchall())
for d in FLOWS.iterdir():
    if d.name.startswith("._") or not d.is_dir():
        continue
    w = d.name
    for q in ("in_before", "first_in", "sol_out_after"):
        p = d / f"{q}.json.gz"
        if not p.exists():
            continue
        for x in json.load(gzip.open(p))["rows"]:
            a, b = x.get("fromUserAccount"), x.get("toUserAccount")
            amt = float(x["uiAmount"])
            if amt < DUST:
                continue
            other = a if b == w else b
            if bad(other):
                continue
            edges.append({"src": a, "dst": b, "type": "sol_direct", "amount": amt, "asset": "SOL", "block_time": x["blockTime"], "signature": x["signature"]})
            if b == w and q == "in_before" and first_buy.get(w) and first_buy[w] - x["blockTime"] <= 72 * 3600:
                funded[a].append((w, x["blockTime"], x["signature"], amt))
            if a == w and q == "sol_out_after":
                sinks[b].append((w, x["blockTime"], x["signature"], amt))

for f, lst in funded.items():
    ws = sorted({x[0] for x in lst})
    for i, u in enumerate(ws):
        for v in ws[i + 1:]:
            edges.append({"src": u, "dst": v, "type": "funder_commun", "amount": 0.0, "asset": f, "block_time": min(x[1] for x in lst), "signature": ""})
for s, lst in sinks.items():
    for i, u in enumerate(lst):
        for v in lst[i + 1:]:
            if u[0] != v[0] and abs(u[1] - v[1]) <= 7 * 86400:
                edges.append({"src": u[0], "dst": v[0], "type": "sink_commun", "amount": 0.0, "asset": s, "block_time": min(u[1], v[1]), "signature": u[2]})

uniq = {(e["src"], e["dst"], e["type"], e["signature"], e["asset"]): e for e in edges}
edges = list(uniq.values())
pq.write_table(pa.Table.from_pylist(edges), BIG / "link_edges.parquet", compression="zstd")

# composantes sur les seules preuves directes : les liens faibles sont listés, ils ne fusionnent pas
G = nx.Graph()
for e in edges:
    if e["type"] in ("token_direct", "sol_direct"):
        G.add_edge(e["src"], e["dst"])
pnl = {r[0]: r[1:] for r in con.execute(f"SELECT owner, realized_sol, net_sol_all, bought_sol, residual_qty, first_buy_time, bought_qty, transfer_in_qty, transfer_out_qty FROM read_parquet('{BIG}/wallets.parquet')").fetchall()}
weak = defaultdict(lambda: defaultdict(int))
for e in edges:
    if e["type"] in ("funder_commun", "sink_commun"):
        weak[e["src"]][e["type"]] += 1
        weak[e["dst"]][e["type"]] += 1
clusters = []
for i, comp in enumerate(sorted(nx.connected_components(G), key=len, reverse=True)):
    if len(comp) < 2:
        continue
    members = sorted(comp)
    inside = [e for e in edges if e["src"] in comp and e["dst"] in comp and e["type"] in ("token_direct", "sol_direct")]
    tok = [e for e in inside if e["type"] == "token_direct"]
    pair_dirs = defaultdict(set)
    for e in inside:
        pair_dirs[frozenset((e["src"], e["dst"]))].add(e["src"])
    two_way = sum(1 for v in pair_dirs.values() if len(v) == 2)
    known = [pnl[m] for m in members if m in pnl]
    fb = [k[4] for k in known if k[4]]
    strength = ("B" if (len(tok) >= 2 and two_way >= 1) or len(tok) >= 3 else "C")
    clusters.append({
        "cluster": i, "n_wallets": len(members), "members": ",".join(members),
        "n_token_edges": len(tok), "n_sol_edges": len(inside) - len(tok), "n_two_way_pairs": two_way,
        "dmaga_moved": sum(e["amount"] for e in tok), "realized_sol_sum": sum(k[0] for k in known),
        "net_sol_sum": sum(k[1] for k in known), "bought_sol_sum": sum(k[2] for k in known),
        "bought_qty_sum": sum(k[5] for k in known), "residual_qty_sum": sum(k[3] for k in known),
        "first_buy": min(fb) if fb else None, "strength": strength,
        "signatures": ",".join(sorted({e["signature"] for e in tok})[:40]),
        "justification": (f"{len(tok)} transfert(s) direct(s) de DMAGA ≥ 100 k, {len(inside) - len(tok)} virement(s) de SOL ≥ 0,1, "
                          f"{two_way} paire(s) dans les deux sens. Alternatives : vente de gré à gré, cadeau, partage au sein d'un "
                          "groupe sans propriétaire unique, paiement d'un service."),
    })
schema_rows = clusters or [{"cluster": -1}]
pq.write_table(pa.Table.from_pylist(schema_rows), DATA / "wallet_clusters.parquet", compression="zstd")
print(f"arêtes={len(edges)} clusters={len(clusters)} services={len(service)} populaires={len(popular)} occupés={len(busy)}")
for c in clusters[:12]:
    print(c["cluster"], c["n_wallets"], "tok", c["n_token_edges"], "sol", c["n_sol_edges"], "2 sens", c["n_two_way_pairs"], "achetés", round(c["bought_qty_sum"]), "réalisé", round(c["realized_sol_sum"]), c["strength"])
