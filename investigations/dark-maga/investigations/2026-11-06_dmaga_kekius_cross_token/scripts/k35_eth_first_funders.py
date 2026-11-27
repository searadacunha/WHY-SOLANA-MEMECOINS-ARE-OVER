"""KEKIUS Ethereum : premier financeur en ETH des acheteurs du bloc d'ouverture 21397848 (Routescan txlist, 20 premières tx).

Premier financeur = expéditeur de la première tx entrante de valeur > 0 avant le bloc d'ouverture. Étiquettes Blockscout."""
import csv, json, time, urllib.request
from collections import Counter
from k_lib import DATA, utc
import ev_lib

buyers = [r["owner"] for r in csv.DictReader(open(DATA / "eth_first100_buyers.csv")) if r["first_buy_block"] == "21397848"]
out = []
for a in buyers:
    txs = ev_lib.rs(module="account", action="txlist", address=a, startblock=0, endblock=21397848, page=1, offset=20, sort="asc") or []
    inc = [t for t in txs if t["to"].lower() == a and int(t["value"]) > 0 and t["isError"] == "0"]
    f = inc[0] if inc else None
    out.append({"buyer": a, "n_tx_before_open": len(txs), "first_funder": f["from"] if f else "", "first_funding_eth": int(f["value"]) / 1e18 if f else "",
                "first_funding_utc": utc(f["timeStamp"]) if f else "", "first_funding_tx": f["hash"] if f else ""})
labels = {}
for fa in {o["first_funder"] for o in out if o["first_funder"]}:
    labels[fa] = ev_lib.meta_tags(fa)
for o in out:
    o["funder_labels"] = ";".join(labels.get(o["first_funder"], []) or [])
with open(DATA / "eth_open_block_funders.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(out[0])); w.writeheader(); w.writerows(out)
c = Counter(o["first_funder"] for o in out)
print(len(out), "acheteurs ;", [(k, n, labels.get(k)) for k, n in c.most_common(8)])
