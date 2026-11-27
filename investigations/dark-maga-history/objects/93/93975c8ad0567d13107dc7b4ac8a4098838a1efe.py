"""XC78 : contreparties SOL (≥ 0,5 SOL) des 16 wallets des achats co-signés et de Go5, toute leur histoire lisible,
puis recherche de ces contreparties dans les tables DMAGA (wallets, funding_edges, exit_flows, nodes).
Sortie : data/xc_bundle_counterparties.csv."""
import csv, json
from collections import defaultdict
import duckdb
from k_lib import DATA, DMAGA_BIG, EVID, EXT, XC, utc
from k11_parse import signers, sol_deltas, token_deltas
import k16_pubrpc as pub

idx = json.loads((EVID / "receipts" / "INDEX.json").read_text())
bund = set()
for s, why in idx.items():
    if "co-signé" in why:
        t = json.loads((EVID / "receipts" / f"{s}.json").read_text())
        bund |= {a for a, v in token_deltas(t, XC).items() if v > 0}
assert len(bund) == 16
rows = []
for w in sorted(bund):
    sg, trunc = pub.sigs(w, max_pages=2)
    for x in sg:
        if x.get("err"):
            continue
        t = pub.tx(x["signature"])
        sd = sol_deltas(t)
        me = sd.get(w, 0)
        if abs(me) < 5 * 10**8:
            continue
        for cp, v in sd.items():
            if cp != w and abs(v) >= 5 * 10**8 and (v > 0) != (me > 0):
                rows.append([w, cp, "out" if me < 0 else "in", round(abs(v) / 1e9, 9), utc(t["blockTime"]), x["signature"], len(sg), trunc])
B = str(DMAGA_BIG)
cps = sorted({r[1] for r in rows})
duckdb.sql("create table c(a varchar)"); duckdb.executemany("insert into c values (?)", [(a,) for a in cps])
hit = defaultdict(list)
for name, q in [("wallets", f"select owner from '{B}/wallets.parquet' join c on owner=c.a"),
                ("funding_src", f"select distinct src from '{B}/funding_edges.parquet' join c on src=c.a"),
                ("funding_wallet", f"select distinct wallet from '{B}/funding_edges.parquet' join c on wallet=c.a"),
                ("exit_dst", f"select distinct dst from '{B}/exit_flows.parquet' join c on dst=c.a"),
                ("nodes", f"select address from '{B}/nodes.parquet' join c on address=c.a")]:
    for (a,) in duckdb.sql(q).fetchall():
        hit[a].append(name)
with open(DATA / "xc_bundle_counterparties.csv", "w", newline="") as f:
    wr = csv.writer(f)
    wr.writerow(["bundle_wallet", "counterparty", "direction", "sol", "utc", "signature", "n_sigs_wallet", "truncated", "in_dmaga_tables"])
    for r in rows:
        wr.writerow(r + [";".join(hit.get(r[1], []))])
print(len(rows), "flux ≥ 0,5 SOL ;", len(cps), "contreparties ;", "dans DMAGA :", {a: hit[a] for a in hit})
