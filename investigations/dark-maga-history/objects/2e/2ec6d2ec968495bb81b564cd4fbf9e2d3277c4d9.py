#!/usr/bin/env python3
"""Groupes liés par transferts directs de DMAGA avant Musk : le sous-graphe le plus probant, sans les liens de SOL.

Arêtes : token_direct ≥ 1 M de jetons, avant la borne basse 21/07 19:03:27 UTC, hors services. Pour chaque composante : jetons
achetés sur le marché, déplacés, détenus juste avant la borne basse, et résultat final. Sortie : data/prevent_groups.json.
Une composante dit que ces wallets se sont passé des jetons. Elle ne dit pas qu'ils ont un seul propriétaire.
"""
import json
from datetime import datetime, timezone

import networkx as nx

from dmaga.config import BIG, DATA
from dmaga.db import connect
from dmaga.labels import label

T_LOW = 1721588607
con = connect()
con.execute(f"CREATE VIEW l AS SELECT * FROM read_parquet('{BIG}/link_edges.parquet')")
con.execute(f"CREATE VIEW w AS SELECT * FROM read_parquet('{BIG}/wallets.parquet')")
E = con.execute(f"SELECT src, dst, amount, block_time, signature FROM l WHERE type='token_direct' AND amount>=1000000 AND block_time<{T_LOW}").fetchall()
G = nx.Graph()
for a, b, q, t, s in E:
    G.add_edge(a, b)
pnl = {r[0]: r[1:] for r in con.execute("SELECT owner, realized_sol, net_sol_all, bought_sol, bought_qty, first_buy_time, sold_sol, proceeds_usd, cost_usd, residual_qty FROM w").fetchall()}
# position juste avant la borne basse, par wallet, depuis les flux normalisés et les transferts tracés
pos = dict(con.execute(f"""SELECT owner, sum(token_delta)/1e6 FROM trades WHERE block_time<{T_LOW} AND kind IN ('swap','transfer','fee_share','swap_other','lp_add','lp_remove')
                           AND owner IS NOT NULL GROUP BY 1""").fetchall())
for a, b, q, t, s in E:  # transferts vus seulement par getTransfersByAddress
    if not con.execute("SELECT 1 FROM trades WHERE signature=? AND owner=? LIMIT 1", [s, a]).fetchone():
        pos[a] = pos.get(a, 0) - q
        pos[b] = pos.get(b, 0) + q
out = []
for comp in sorted(nx.connected_components(G), key=len, reverse=True):
    members = sorted(comp)
    ed = [e for e in E if e[0] in comp and e[1] in comp]
    k = [pnl.get(m, (0,) * 9) for m in members]
    out.append({"n": len(members), "members": members, "edges": len(ed), "moved_M": sum(e[2] for e in ed) / 1e6,
                "first_edge": min(e[3] for e in ed), "bought_sol": sum(x[2] or 0 for x in k), "bought_M": sum(x[3] or 0 for x in k) / 1e6,
                "first_buy": min((x[4] for x in k if x[4]), default=None), "realized_sol": sum(x[0] or 0 for x in k), "net_sol": sum(x[1] or 0 for x in k),
                "proceeds_usd": sum(x[6] or 0 for x in k), "cost_usd": sum(x[7] or 0 for x in k),
                "held_before_musk_M": sum(max(pos.get(m, 0), 0) for m in members) / 1e6,
                "signatures": [e[4] for e in sorted(ed, key=lambda e: -e[2])[:30]],
                "edges_top": [{"src": e[0], "dst": e[1], "M": round(e[2] / 1e6, 3), "t": e[3], "sig": e[4]} for e in sorted(ed, key=lambda e: e[3])[:60]]})
out.sort(key=lambda g: -g["held_before_musk_M"])
(DATA / "prevent_groups.json").write_text(json.dumps(out, indent=1))
print("arêtes", len(E), "groupes", len(out), "wallets", G.number_of_nodes())
tot = sum(max(v, 0) for v in pos.values()) / 1e6
print("jetons détenus par tous les non-pools avant la borne basse (M)", round(tot, 1))
fmt = lambda t: datetime.fromtimestamp(t, timezone.utc).strftime("%d/%m %H:%M") if t else "?"
for g in out[:14]:
    print(g["n"], "arêtes", g["edges"], "détenu M", round(g["held_before_musk_M"], 1), "acheté M", round(g["bought_M"], 1), "SOL", round(g["bought_sol"], 1), "réalisé", round(g["realized_sol"]), "net", round(g["net_sol"]), "1er achat", fmt(g["first_buy"]), "|", ",".join(m[:6] for m in g["members"][:9]))
