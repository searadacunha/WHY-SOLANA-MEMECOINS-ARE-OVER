"""Écran de variations de soldes SOL associées à l'opérateur XC78 3oqARBND… (toute son histoire, 4 386 tx) : destinations d'au moins 1 SOL, sommes et dates,
puis recherche de comptes candidats dans les tables DMAGA. ATTENTION : une variation positive simultanée ne suffit pas à prouver un transfert direct si plusieurs comptes financent une transaction. Sortie : data/xc_operator_outflows.csv."""
import csv, json
from collections import defaultdict
import duckdb
from k_lib import DATA, DMAGA_BIG, EXT, utc
from k11_parse import signers, sol_deltas
import k16_pubrpc as pub

OPS = "3oqARBNDr56L2oWQ9aR2QzS7FeTMEubd8J2v29wP5N58"
sigs = json.load(open(EXT / f"sigs_{OPS}.json"))
agg = defaultdict(lambda: [0, 0.0, None, None, ""])
for x in sigs:
    if x.get("err"):
        continue
    t = pub.tx(x["signature"])
    sd = sol_deltas(t)
    if sd.get(OPS, 0) > -10**9:
        continue
    for d, v in sd.items():
        if d != OPS and v >= 10**9:
            a = agg[d]
            a[0] += 1; a[1] += v / 1e9
            a[2] = min(a[2] or t["blockTime"], t["blockTime"]); a[3] = max(a[3] or 0, t["blockTime"])
            a[4] = a[4] or x["signature"]
B = str(DMAGA_BIG)
duckdb.sql("create table c(a varchar)")
duckdb.executemany("insert into c values (?)", [(a,) for a in agg])
hit = defaultdict(list)
for name, q in [("wallets", f"select owner from '{B}/wallets.parquet' join c on owner=c.a"),
                ("funding_src", f"select distinct src from '{B}/funding_edges.parquet' join c on src=c.a"),
                ("funding_wallet", f"select distinct wallet from '{B}/funding_edges.parquet' join c on wallet=c.a"),
                ("exit_dst", f"select distinct dst from '{B}/exit_flows.parquet' join c on dst=c.a"),
                ("nodes", f"select address from '{B}/nodes.parquet' join c on address=c.a")]:
    for (a,) in duckdb.sql(q).fetchall():
        hit[a].append(name)
with open(DATA / "xc_operator_outflows.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["destination", "n_transfers", "sol", "first_utc", "last_utc", "example_signature", "in_dmaga_tables"])
    for d, (n, s, t0, t1, sig) in sorted(agg.items(), key=lambda x: -x[1][1]):
        w.writerow([d, n, round(s, 9), utc(t0), utc(t1), sig, ";".join(hit.get(d, []))])
print(len(agg), "destinations ≥ 1 SOL ;", round(sum(v[1] for v in agg.values()), 3), "SOL ; dans DMAGA :", dict(hit))
