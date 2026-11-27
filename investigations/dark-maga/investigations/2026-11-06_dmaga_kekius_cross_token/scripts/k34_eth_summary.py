"""KEKIUS Ethereum : 100 premiers acheteurs et 100 plus gros acheteurs avant le changement de nom de Musk (06:02:01 UTC le
31/12/2024, borne basse vérifiée, evidence/social/MUSK_PROFILE_TIMELINE.md), avec leurs ventes jusqu'au 04/01/2025."""
import csv, gzip
from collections import defaultdict
from k_lib import DATA, utc

T_MUSK = 1735624921  # 2024-12-31 06:02:01 UTC
L = list(csv.DictReader(gzip.open(DATA / "eth_kekius_ledger.csv.gz", "rt")))
g = defaultdict(lambda: defaultdict(int))
first = {}
for r in L:
    a, t, v, e = r["owner"], int(r["time"]), int(r["kekius_raw"]), int(r["eth_wei"])
    pre = t < T_MUSK
    if r["kind"] == "buy":
        first.setdefault(a, (int(r["block"]), int(r["tx_index"]), t, r["tx"]))
        g[a]["buy_pre" if pre else "buy_post"] += v
        g[a]["eth_in_pre" if pre else "eth_in_post"] += -e
    elif r["kind"] == "sell":
        g[a]["sell_pre" if pre else "sell_post"] += -v
        g[a]["eth_out_pre" if pre else "eth_out_post"] += e
    elif r["kind"] == "transfer_in":
        g[a]["xin"] += v
    else:
        g[a]["xout"] += -v
cols = ["rank", "owner", "first_buy_utc", "first_buy_block", "first_buy_tx", "bought_pre_M", "eth_spent_pre", "sold_pre_M",
        "eth_recv_pre", "bought_post_M", "eth_spent_post", "sold_post_M", "eth_recv_post", "realized_eth_to_0104", "transfer_in_M", "transfer_out_M"]


def row(i, a):
    x, f = g[a], first.get(a)
    return [i, a, utc(f[2]) if f else "", f[0] if f else "", f[3] if f else "", x["buy_pre"] / 1e15, x["eth_in_pre"] / 1e18,
            x["sell_pre"] / 1e15, x["eth_out_pre"] / 1e18, x["buy_post"] / 1e15, x["eth_in_post"] / 1e18, x["sell_post"] / 1e15,
            x["eth_out_post"] / 1e18, (x["eth_out_pre"] + x["eth_out_post"] - x["eth_in_pre"] - x["eth_in_post"]) / 1e18,
            x["xin"] / 1e15, x["xout"] / 1e15]


def dump(name, addrs):
    with open(DATA / name, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(cols)
        for i, a in enumerate(addrs, 1):
            w.writerow([round(v, 6) if isinstance(v, float) else v for v in row(i, a)])


dump("eth_first100_buyers.csv", sorted(first, key=lambda a: first[a][:2])[:100])
dump("eth_top100_pre_event.csv", sorted((a for a in g if g[a]["eth_in_pre"] > 0), key=lambda a: -g[a]["eth_in_pre"])[:100])
dump("eth_top100_realized.csv", sorted(g, key=lambda a: -(g[a]["eth_out_pre"] + g[a]["eth_out_post"] - g[a]["eth_in_pre"] - g[a]["eth_in_post"]))[:100])
print("acheteurs", len(first), "acheteurs avant Musk", sum(1 for a in g if g[a]["buy_pre"] > 0))
