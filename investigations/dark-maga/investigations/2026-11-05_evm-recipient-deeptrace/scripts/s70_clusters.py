"""Pour chaque destination EVM : tous les makers Solana connus (ordres décodés côté Solana par work_I/i14 et fills décodés côté Ethereum ici),
et les liens Solana indépendants entre makers d'une même destination (transferts directs du corpus DMAGA link_edges, financement de gaz
relu ici sur les ledgers s20/s21). Une convergence est notée forte si deux makers ont au moins un lien Solana direct ET la même destination EVM.
Lancer avec scripts/py.sh du projet (duckdb). Sortie : ../solana_to_evm_clusters.csv"""
import csv, json, sys, glob, itertools, duckdb
from pathlib import Path
PROJ = str(Path(__file__).resolve().parents[3])  # racine du dépôt
sys.path.insert(0, PROJ)
from dmaga.config import BIG  # données lourdes hors dépôt (DMAGA_EXT)
D = str(BIG) + "/"
G = json.load(open(PROJ + "/data/group_split.json"))
SUB = {w: i for i, s in enumerate(G["sous_ensembles"]) for w in s["members"]}
orders = {}  # (dest, chain, maker) -> list
for r in csv.DictReader(open(PROJ + "/investigations/2026-11-05_debridge_winners/evidence/i14_orders.csv")):
    usd = (int(r["give_amount"]) + int(r["fee_pct"])) / 1e6
    orders.setdefault((r["receiver"].lower(), r["take_chain"], r["maker"]), {})[r["sig"]] = (r["utc"].replace("T", " ").rstrip("Z"), usd, "solana-i14", int(r["give_amount"]))
for r in csv.DictReader(open("../evidence/dln_orders_evm.csv")):
    if r["direction"] == "IN" and r["give_chain"] == "solana":
        k = (r["receiver"].lower(), "1", r["maker"])
        hit = [s_ for s_, v in orders.get(k, {}).items() if v[3] == int(r["give_amount_raw"])]  # même giveAmount brut = même ordre
        if hit:
            v = orders[k][hit[0]]; orders[k][hit[0]] = (v[0], v[1], v[2] + "+ethereum-fill", v[3])
        else:  # ordre absent du corpus Solana : USD = give + 0,04 % de frais, comme i14
            orders.setdefault(k, {})[r["tx"]] = (r["utc"], int(r["give_amount_raw"]) * 1.0004 / 1e6, "ethereum-fill-only", int(r["give_amount_raw"]))
makers = sorted({m for (_, _, m) in orders})
L = ",".join(f"'{m}'" for m in makers)
edges = duckdb.sql(f"select src,dst,type,asset,count(*) n,min(block_time) t0,min(signature) sig from '{D}link_edges.parquet' where src in ({L}) and dst in ({L}) and type in ('token_direct','sol_direct','sol_petit') group by all").fetchall()
link = {}
for s, d, t, a, n, t0, sig in edges:
    link.setdefault(frozenset((s, d)), []).append(f"{s[:8]}->{d[:8]} {t} {a} n={n} ex={sig}")
# gaz commun : les wallets de parking de GZXKYzwZ (s21) reçoivent tous leur SOL d'Ei5yGz8d ; GZXKYzwZ aussi (s20)
gas = {}
for f in glob.glob("../evidence/s2[01]_*ledger.csv"):
    rows = list(csv.DictReader(open(f)))
    w = f.split("s21_")[-1].split("_ledger")[0] if "s21_" in f else "GZXKYzwZ"
    for r in rows:
        if int(r["sol_delta_lamports"]) >= 100_000_000 and r["fee_payer"] != "" and not r["fee_payer"].startswith(w[:8]):
            gas.setdefault(w[:8], set()).add(r["fee_payer"])
out = []
for d in sorted({d for (d, _, _) in orders}):
    ms = sorted({m for (dd, cc, m) in orders if dd == d})  # même adresse EVM sur toute chaîne = même clé
    for (_, c, m) in sorted(k for k in orders if k[0] == d):
        o = orders[(d, c, m)]
        others = [x for x in ms if x != m]
        lk = [e for x in others for e in link.get(frozenset((m, x)), [])]
        g = sorted(gas.get(m[:8], []))
        indep = (1 if lk else 0) + (1 if g and any(x.startswith(gg[:8]) for gg in g for x in others) else 0)
        out.append(dict(evm_destination=d, take_chain=c, solana_maker=m, n_orders=len(o), usd_total=round(sum(v[1] for v in o.values()), 2),
                        first_utc=min(v[0] for v in o.values()), last_utc=max(v[0] for v in o.values()), sources="|".join(sorted({v[2] for v in o.values()})),
                        maker_in_33=m in SUB, sub_ensemble=SUB.get(m, ""), other_makers_same_destination="|".join(x[:8] for x in others),
                        solana_direct_links_with_them=" ; ".join(lk)[:900], sol_gas_funders=("|".join(g))[:200],
                        independent_links=indep, convergence="FORTE (lien Solana direct + destination EVM commune)" if lk else ("seul maker" if not others else "destination commune seule")))
with open("../solana_to_evm_clusters.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(out[0])); w.writeheader(); w.writerows(out)
for r in out:
    if r["usd_total"] > 1000: print(r["evm_destination"][:10], r["take_chain"], r["solana_maker"][:8], r["n_orders"], r["usd_total"], r["sub_ensemble"], r["sources"], r["convergence"][:20], r["sol_gas_funders"][:30])
