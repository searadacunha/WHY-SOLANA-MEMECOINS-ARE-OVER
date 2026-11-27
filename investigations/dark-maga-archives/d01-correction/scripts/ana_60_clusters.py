#!/usr/bin/env python3
"""Clusters financiers à partir d'arêtes réelles, séparées par type de preuve. Calcul dans DuckDB, mémoire plafonnée.

Types d'arêtes, du plus fort au plus faible :
  token_direct   transfert de DMAGA entre deux wallets, hors swap, ≥ 100 000 jetons
  sol_direct     SOL direct ≥ 0,1 SOL entre deux wallets ayant échangé DMAGA, du 13/06/2024 au 31/12/2024
  sol_petit      SOL direct entre 0,005 et 0,1 : lien faible, listé, ne fusionne jamais deux wallets
  funder_commun  même financeur direct, non service, dans les 72 h avant le premier achat
  sink_commun    même destination de sortie, non service, à moins de 7 jours d'écart
Un nœud de service (échange, compte Jupiter, routeur, hub, venue, adresse vue par ≥ 15 wallets tracés, ≥ 30 voisins directs) n'est
jamais un lien. Un cluster dit « ces wallets sont reliés par ces transactions », pas « une même personne ».

Sorties : data/wallet_clusters.parquet, BIG/link_edges.parquet. À lancer sous scripts/guard.py.
"""
from collections import defaultdict

import networkx as nx
import pyarrow as pa
import pyarrow.parquet as pq

from dmaga.db import connect
from dmaga.hot_presume import HOT_PRESUME
from dmaga.labels import load as load_labels
from dmaga.paths import BIG, DATA, exige_v2
from dmaga.venues import load as load_venues

exige_v2()

INFRA = ["5Q544fKrFoe6tsEbD7S8EmxGTJYAKtTVhAW5Q5pge4j1", "39azUYFWPz3VHgKCf3VChUwbpURdCHRxjWVowf5jUJjg",
         "87g44hEXP7R8ZxoAJtz941tsVftpEXC1LqAFTf2ZHtkH", "PNLCQcVCD26aC7ZWgRyr5ptfaR7bBrWdTFgRWwu2tvF"]
con = connect(mem="700MB", threads=2)
con.execute("CREATE TEMP TABLE svc(a VARCHAR)")
con.executemany("INSERT INTO svc VALUES (?)", [[a] for a in set(load_labels()) | set(load_venues()) | set(INFRA) | HOT_PRESUME])
F, X = f"read_parquet('{BIG}/funding_edges.parquet')", f"read_parquet('{BIG}/exit_flows.parquet')"
W, E, N = f"read_parquet('{BIG}/wallets.parquet')", f"read_parquet('{BIG}/token_edges.parquet')", f"read_parquet('{BIG}/nodes.parquet')"
con.execute(f"INSERT INTO svc SELECT address FROM {N} WHERE kind <> 'wallet'")
con.execute(f"""INSERT INTO svc SELECT a FROM (SELECT dst a, wallet FROM {X} UNION ALL SELECT src a, wallet FROM {F})
                GROUP BY a HAVING count(DISTINCT wallet) >= 15""")
con.execute("CREATE TEMP TABLE bad AS SELECT DISTINCT a FROM svc")
con.execute(f"CREATE TEMP TABLE traders AS SELECT owner a, first_buy_time fb FROM {W}")
n_bad = con.execute("SELECT count(*) FROM bad").fetchone()[0]
T0, T1 = 1718300000, 1735689600
con.execute(f"""CREATE TEMP TABLE sol AS
    SELECT src, wallet dst, sol amount, block_time, signature FROM {F} WHERE wallet NOT IN (SELECT a FROM bad) AND src NOT IN (SELECT a FROM bad)
    UNION SELECT wallet src, dst, amount, block_time, signature FROM {X} WHERE asset='SOL' AND wallet NOT IN (SELECT a FROM bad) AND dst NOT IN (SELECT a FROM bad)""")
con.execute(f"""CREATE TEMP TABLE e AS
    SELECT src, dst, 'token_direct' type, qty amount, 'DMAGA' asset, block_time, signature FROM {E}
      WHERE qty >= 100000 AND dst <> '(multiple)' AND src NOT IN (SELECT a FROM bad) AND dst NOT IN (SELECT a FROM bad)
    UNION ALL SELECT src, dst, CASE WHEN amount >= 0.1 THEN 'sol_direct' ELSE 'sol_petit' END, amount, 'SOL', block_time, signature FROM sol
      WHERE amount >= 0.005 AND block_time BETWEEN {T0} AND {T1} AND src IN (SELECT a FROM traders) AND dst IN (SELECT a FROM traders)""")
# au moins 30 voisins directs : comportement de service, retiré
con.execute("""CREATE TEMP TABLE hub AS SELECT a FROM (SELECT src a, dst b FROM e WHERE type IN ('token_direct','sol_direct')
               UNION SELECT dst a, src b FROM e WHERE type IN ('token_direct','sol_direct')) GROUP BY a HAVING count(*) >= 30""")
con.execute("DELETE FROM e WHERE src IN (SELECT a FROM hub) OR dst IN (SELECT a FROM hub)")
con.execute(f"""INSERT INTO e WITH f AS (SELECT DISTINCT s.src f, s.dst w, s.block_time t FROM sol s JOIN traders tr ON tr.a = s.dst
                  WHERE s.amount >= 0.1 AND tr.fb IS NOT NULL AND s.block_time < tr.fb AND tr.fb - s.block_time <= 259200 AND s.src NOT IN (SELECT a FROM hub))
    SELECT a.w, b.w, 'funder_commun', 0.0, a.f, min(least(a.t, b.t)), '' FROM f a JOIN f b ON a.f = b.f AND a.w < b.w GROUP BY a.w, b.w, a.f""")
con.execute(f"""INSERT INTO e WITH o AS (SELECT DISTINCT wallet w, dst d, block_time t FROM {X} WHERE asset='SOL' AND amount >= 0.1 AND wallet NOT IN (SELECT a FROM bad)
                  AND wallet IN (SELECT a FROM traders) AND dst NOT IN (SELECT a FROM bad) AND dst NOT IN (SELECT a FROM hub) AND block_time < {T1})
    SELECT a.w, b.w, 'sink_commun', 0.0, a.d, min(least(a.t, b.t)), '' FROM o a JOIN o b ON a.d = b.d AND a.w < b.w AND abs(a.t - b.t) <= 604800 GROUP BY a.w, b.w, a.d""")
tmp = BIG / "link_edges.tmp.parquet"
con.execute(f"COPY e TO '{tmp}' (FORMAT parquet, COMPRESSION zstd)")
tmp.replace(BIG / "link_edges.parquet")
counts = dict(con.execute("SELECT type, count(*) FROM e GROUP BY 1").fetchall())

# composantes sur les seules preuves directes : les liens faibles sont listés, ils ne fusionnent pas
G = nx.Graph()
agg = defaultdict(lambda: [0, 0, 0.0])
dirs = defaultdict(set)
for a, b, k, q in con.execute("SELECT src, dst, type, amount FROM e WHERE type IN ('token_direct','sol_direct')").fetchall():
    G.add_edge(a, b)
    p = frozenset((a, b))
    agg[p][0 if k == "token_direct" else 1] += 1
    dirs[p].add(a)
    if k == "token_direct":
        agg[p][2] += q
pnl = {r[0]: r[1:] for r in con.execute(f"SELECT owner, realized_sol, net_sol_all, bought_sol, residual_qty, first_buy_time, bought_qty FROM {W}").fetchall()}
clusters = []
for i, comp in enumerate(sorted(nx.connected_components(G), key=len, reverse=True)):
    if len(comp) < 2:
        continue
    pairs = [frozenset((u, v)) for u, v in G.subgraph(comp).edges()]
    tok = sum(agg[p][0] for p in pairs)
    sol = sum(agg[p][1] for p in pairs)
    moved = sum(agg[p][2] for p in pairs)
    tw = sum(1 for p in pairs if len(dirs[p]) == 2)
    known = [pnl[m] for m in comp if m in pnl]
    fb = [k[4] for k in known if k[4]]
    clusters.append({
        "cluster": i, "n_wallets": len(comp), "members": ",".join(sorted(comp)), "n_token_edges": tok, "n_sol_edges": sol, "n_two_way_pairs": tw,
        "dmaga_moved": moved, "realized_sol_sum": sum(k[0] for k in known), "net_sol_sum": sum(k[1] for k in known), "bought_sol_sum": sum(k[2] for k in known),
        "bought_qty_sum": sum(k[5] for k in known), "residual_qty_sum": sum(k[3] for k in known), "first_buy": min(fb) if fb else None,
        "strength": "B" if (tok >= 2 and tw >= 1) or tok >= 3 else "C",
        "justification": (f"{tok} transfert(s) direct(s) de DMAGA ≥ 100 k, {sol} virement(s) de SOL ≥ 0,1, {tw} paire(s) dans les deux sens. Alternatives : vente de gré à "
                          "gré, cadeau, partage dans un groupe sans propriétaire unique, paiement d'un service. Une grande composante peut venir d'un effet de chaîne."),
    })
pq.write_table(pa.Table.from_pylist(clusters), DATA / "wallet_clusters.parquet", compression="zstd")
print(f"arêtes={counts} clusters={len(clusters)} services={n_bad}")
for c in sorted(clusters, key=lambda c: -c["bought_qty_sum"])[:8]:
    print(c["cluster"], c["n_wallets"], "tok", c["n_token_edges"], "sol", c["n_sol_edges"], "2 sens", c["n_two_way_pairs"], "réalisé", round(c["realized_sol_sum"]), c["strength"], c["members"][:60])
