#!/usr/bin/env python3
"""Auditeur A. Schéma et contenu de funding_edges, link_edges, nodes, wallet_clusters. Teste les étiquettes de service. Lecture seule."""
import duckdb, json, collections
from dmaga.labels import label, load as L
from dmaga.venues import load as V
A = "/Volumes/VERBATIM HD/Dark-MAGA-Investigation/audits_work/A"
B = "/Volumes/VERBATIM HD/Dark-MAGA-Investigation/data"
con = duckdb.connect(":memory:", config={"memory_limit": "800MB", "threads": 2, "temp_directory": A + "/duck12"})
con.execute("SET TimeZone='UTC'")
q = lambda s: con.execute(s).fetchall()
for n in ("funding_edges", "link_edges", "nodes", "token_edges", "cohorts"):
    print(n, q(f"SELECT count(*) FROM read_parquet('{B}/{n}.parquet')"), [(c[0], c[1]) for c in q(f"DESCRIBE SELECT * FROM read_parquet('{B}/{n}.parquet')")])
print("nodes par kind", q(f"SELECT kind, count(*) FROM read_parquet('{B}/nodes.parquet') GROUP BY 1 ORDER BY 2 DESC"))
print("kind=cex, labels", q(f"SELECT label, count(*) FROM read_parquet('{B}/nodes.parquet') WHERE kind='cex' GROUP BY 1 ORDER BY 2 DESC LIMIT 40"))
print("funding_edges, aperçu", q(f"SELECT * FROM read_parquet('{B}/funding_edges.parquet') LIMIT 3"))
print("link_edges, types", q(f"SELECT type, count(*) FROM read_parquet('{B}/link_edges.parquet') GROUP BY 1 ORDER BY 2 DESC"))
print("link_edges, aperçu", q(f"SELECT * FROM read_parquet('{B}/link_edges.parquet') LIMIT 2"))
g = json.load(open("data/prevent_groups.json"))[0]
mem = g["members"]
LL = L(); VV = V()
print("membres étiquetés", [(m, LL.get(m)) for m in mem if m in LL], "venues", [m for m in mem if m in VV])
nodes = dict(q(f"SELECT address, kind FROM read_parquet('{B}/nodes.parquet')"))
print("kinds des membres", collections.Counter(nodes.get(m) for m in mem))
print("nodes des membres (contreparties)", q(f"SELECT address, kind, n_counterparts, n_tx, pass_through, round(qty_moved) FROM read_parquet('{B}/nodes.parquet') WHERE address IN {tuple(mem)} ORDER BY n_counterparts DESC"))
print("wallets classés router/hub (top)", q(f"SELECT address, kind, label, n_counterparts, pass_through, round(qty_moved) FROM read_parquet('{B}/nodes.parquet') WHERE kind IN ('router','hub') ORDER BY n_counterparts DESC LIMIT 25"))
print("kind=wallet, degré élevé", q(f"SELECT address, n_counterparts, n_tx, pass_through, round(qty_moved) FROM read_parquet('{B}/nodes.parquet') WHERE kind='wallet' ORDER BY n_counterparts DESC LIMIT 40"))
