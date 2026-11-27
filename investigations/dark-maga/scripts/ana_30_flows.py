#!/usr/bin/env python3
"""Graphe de financement et de sorties à partir de raw/flows/<wallet>/*.json.gz.

Sorties (data/) :
  funding_edges.parquet : SOL reçu par un wallet tracé avant son premier achat, avec niveau de saut.
  exit_flows.parquet    : SOL, USDC, USDT sortis après sa première vente, hors réserves de pool.
Chaque arête porte sa signature et l'étiquette de la contrepartie : `terminal` indique une frontière
(échange, service) où la traçabilité s'arrête. Aucune continuité n'est créée à travers elle.
"""
import gzip
import json
import sys

import pyarrow as pa
import pyarrow.parquet as pq

from dmaga.config import BIG, RAW
from dmaga.labels import label
from dmaga.venues import load as load_venues

FLOWS = RAW / "flows"
VENUES = load_venues()
RAY = "5Q544fKrFoe6tsEbD7S8EmxGTJYAKtTVhAW5Q5pge4j1"


def rows_of(owner, name):
    p = FLOWS / owner / f"{name}.json.gz"
    if not p.exists():
        return None, None
    j = json.load(gzip.open(p))
    return j["rows"], j["truncated"]


def classify(addr):
    if addr == RAY or addr in VENUES:
        return "pool"
    lab = label(addr) if addr else None
    return lab


def main():
    funding, exits = [], []
    n = 0
    trunc = {}
    level = json.loads((BIG / "trace_levels.json").read_text()) if (BIG / "trace_levels.json").exists() else {}
    for d in FLOWS.iterdir():
        if d.name.startswith("._") or not d.is_dir():
            continue
        owner = d.name
        n += 1
        for name in ("in_before", "first_in"):
            rows, tr = rows_of(owner, name)
            if rows is None:
                continue
            trunc[f"{owner}:{name}"] = tr
            for x in rows:
                src = x.get("fromUserAccount")
                if not src:
                    continue
                c = classify(src)
                funding.append({"wallet": owner, "src": src, "sol": float(x["uiAmount"]), "block_time": x["blockTime"],
                                "signature": x["signature"], "query": name, "src_label": c, "is_pool": c == "pool",
                                "terminal": c is not None and c != "pool", "level": level.get(owner, 0), "truncated": tr})
        for name, asset in (("sol_out_after", "SOL"), ("usdc_out_after", "USDC"), ("usdt_out_after", "USDT")):
            rows, tr = rows_of(owner, name)
            if rows is None:
                continue
            trunc[f"{owner}:{name}"] = tr
            for x in rows:
                dst = x.get("toUserAccount")
                if not dst:
                    continue
                c = classify(dst)
                exits.append({"wallet": owner, "dst": dst, "asset": asset, "amount": float(x["uiAmount"]),
                              "block_time": x["blockTime"], "signature": x["signature"], "dst_label": c,
                              "is_pool": c == "pool", "terminal": c is not None and c != "pool", "truncated": tr})
    seen = set()
    funding = [r for r in funding if not ((r["wallet"], r["signature"], r["src"], r["sol"]) in seen or seen.add((r["wallet"], r["signature"], r["src"], r["sol"])))]
    pq.write_table(pa.Table.from_pylist(funding), BIG / "funding_edges.parquet", compression="zstd")
    pq.write_table(pa.Table.from_pylist(exits), BIG / "exit_flows.parquet", compression="zstd")
    n_tr = sum(1 for v in trunc.values() if v)
    print(f"wallets={n} funding={len(funding)} exits={len(exits)} requêtes tronquées={n_tr}/{len(trunc)}")


if __name__ == "__main__":
    sys.exit(main())
