#!/usr/bin/env python3
"""Table des mesures : une ligne par (token, variante). Écrit derived/metrics.csv et le décompte d'exclusions."""
import csv
import json
import os
import sys

import numpy as np
import pyarrow.parquet as pq

ETUDE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from col_50_ctrl import BAND, WIDE  # noqa: E402
from metrics import METRICS, compute  # noqa: E402

from dmaga.config import BIG  # noqa: E402

H = 3600
OUT = BIG / "controls"
DMAGA_POOL = "CRSwXnfF21yHDXdYBVWwCwQ5Ni2A4QuK3qGYis5k7x7k"


def load(pool):
    t = pq.read_table(OUT / "swaps" / f"{pool}.parquet")  # déjà trié par (slot, tx_index) à l'écriture
    d = t.to_pydict()
    uniq = {}
    owner = np.array([uniq.setdefault(o, len(uniq)) for o in d["owner"]], dtype=np.int64)
    return (np.array(d["t"], dtype=np.int64), np.array(d["slot"], dtype=np.int64), owner,
            np.array(d["qty"], dtype=np.int64), np.array(d["sol"], dtype=np.int64), np.array(d["vault_pre"], dtype=np.int64))


def main():
    rows = [json.loads(x) for x in (OUT / "selection.jsonl").read_text().splitlines()]
    if len({r["pool"] for r in rows}) != len(rows):
        sys.exit("selection.jsonl contient des doublons")
    counts = {}
    for r in rows:
        counts[r["status"]] = counts.get(r["status"], 0) + 1
    stats = {}
    for x in (OUT / "swaps_stats.jsonl").read_text().splitlines():
        v = json.loads(x)
        stats[v["pool"]] = v
    agg = {}
    for v in stats.values():
        for k, n in v.items():
            if k != "pool":
                agg[k] = agg.get(k, 0) + n
    table = []
    missing = []
    for r in rows:
        if r["status"] != "retenu_superset":
            continue
        path = OUT / "swaps" / f"{r['pool']}.parquet"
        if not path.exists():
            missing.append(r["pool"])
            continue
        st = stats.get(r["pool"])
        if st is None:
            missing.append(r["pool"])
            continue
        if st.get("ruptures", 0):
            counts["exclu_rupture_de_chaine"] = counts.get("exclu_rupture_de_chaine", 0) + 1
            continue
        if r.get("tronque_sans_S20"):
            counts["tronque_sans_S20"] = counts.get("tronque_sans_S20", 0) + 1
        data = load(r["pool"])
        f20, f10 = r.get("fdv_s20"), r.get("fdv_s10")
        specs = []
        if r["S20"] and f20 is not None and BAND[0] <= f20 <= BAND[1]:
            specs.append(("primary", r["S20"], f20))
            specs.append(("R3_S_moins_1h", r["S20"] - H, f20))
        if r["S10"] and f10 is not None and BAND[0] <= f10 <= BAND[1]:
            specs.append(("R1_10x", r["S10"], f10))
        if r["S20"] and f20 is not None and WIDE[0] <= f20 <= WIDE[1]:
            specs.append(("R2_bande_large", r["S20"], f20))
        for name, S, fdv in specs:
            m = compute(*data, S, r["created"])
            if m["n_swaps_96h"] < 20:
                counts[f"moins_de_20_swaps_{name}"] = counts.get(f"moins_de_20_swaps_{name}", 0) + 1
                continue
            table.append({"pool": r["pool"], "mint": r["mint"], "variant": name, "S": S, "created": r["created"],
                          "fdv_usd": round(fdv, 2), "is_dmaga": r["pool"] == DMAGA_POOL, **m})
    counts["swaps_manquants"] = len(missing)
    counts["parse"] = agg
    os.makedirs(os.path.join(ETUDE, "derived"), exist_ok=True)
    with open(os.path.join(ETUDE, "derived", "selection_counts.json"), "w") as f:
        json.dump(counts, f, indent=1)
    if missing:  # jamais de table sur une population partielle
        sys.exit(f"swaps manquants pour {len(missing)} tokens : relancer col_50_ctrl.py swaps")
    with open(os.path.join(ETUDE, "derived", "metrics.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["pool", "mint", "variant", "S", "created", "fdv_usd", "is_dmaga", *METRICS,
                                          "n_swaps_before", "n_swaps_96h", "n_buyers_24h"])
        w.writeheader()
        w.writerows(table)
    print(counts, "lignes", len(table))


if __name__ == "__main__":
    main()
