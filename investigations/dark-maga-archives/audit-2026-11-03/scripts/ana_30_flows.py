#!/usr/bin/env python3
"""Graphe de financement et de sorties à partir de raw/flows/<wallet>/*.json.gz.

Sorties (BIG) :
  funding_edges.parquet : SOL reçu par un wallet tracé avant son premier achat, avec niveau de saut. Une ligne par (wallet, signature, src).
  exit_flows.parquet    : SOL, USDC, USDT sortis après sa première vente, hors réserves de pool.
Chaque arête porte sa signature et l'étiquette de la contrepartie : `terminal` indique une frontière
(échange, service) où la traçabilité s'arrête. Aucune continuité n'est créée à travers elle.
Montants lus sur `amount`, jamais `uiAmount` : les réponses de 2021 ont `decimals` = 0.
"""
import gzip
import json
import sys

import pyarrow as pa
import pyarrow.parquet as pq

from dmaga.config import BIG as BIG_GELE, RAW
from dmaga.labels import label
from dmaga.paths import BIG, exige_v2
from dmaga.venues import load as load_venues

FLOWS = RAW / "flows"
VENUES = load_venues()
RAY = "5Q544fKrFoe6tsEbD7S8EmxGTJYAKtTVhAW5Q5pge4j1"
DECIMALS = {"SOL": 9, "USDC": 6, "USDT": 6}
S_EXIT = pa.schema([("wallet", pa.string()), ("dst", pa.string()), ("asset", pa.string()), ("amount", pa.float64()), ("block_time", pa.int64()),
                    ("signature", pa.string()), ("dst_label", pa.string()), ("is_pool", pa.bool_()), ("terminal", pa.bool_()), ("truncated", pa.bool_())])
S_FUND = pa.schema([("wallet", pa.string()), ("src", pa.string()), ("sol", pa.float64()), ("block_time", pa.int64()), ("signature", pa.string()), ("query", pa.string()),
                    ("src_label", pa.string()), ("is_pool", pa.bool_()), ("terminal", pa.bool_()), ("level", pa.int64()), ("truncated", pa.bool_())])


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


def une_ligne_par_cle(funding):
    """Une ligne par (wallet, signature, src). Dans une requête, deux virements d'une même transaction s'additionnent.
    first_in et in_before se recouvrent mais filtrent différemment : on garde la somme la plus complète, sous la première requête vue."""
    somme = {}
    for r in funding:
        k = (r["wallet"], r["signature"], r["src"], r["query"])
        if k in somme:
            somme[k] = {**somme[k], "sol": somme[k]["sol"] + r["sol"]}
        else:
            somme[k] = r
    best = {}
    for r in somme.values():
        k = (r["wallet"], r["signature"], r["src"])
        best[k] = r if k not in best else {**best[k], "sol": max(best[k]["sol"], r["sol"])}
    return list(best.values())


def main():
    exige_v2()
    funding, exits = [], []
    n = n_exits = 0
    trunc = {}
    # trace_levels.json vient de ana_32_hops (réseau, hors recalcul) : lu dans BIG du gel
    level = json.loads((BIG_GELE / "trace_levels.json").read_text())
    w_exit = pq.ParquetWriter(BIG / "exit_flows.parquet", S_EXIT, compression="zstd")
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
            seen = set()
            for x in rows:
                src = x.get("fromUserAccount")
                if not src:
                    continue
                c = classify(src)
                sol = int(x["amount"]) / 10**9
                if (x["signature"], src, sol) in seen:  # même virement rendu deux fois par la pagination
                    continue
                seen.add((x["signature"], src, sol))
                funding.append({"wallet": owner, "src": src, "sol": sol, "block_time": x["blockTime"],
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
                exits.append({"wallet": owner, "dst": dst, "asset": asset, "amount": int(x["amount"]) / 10 ** DECIMALS[asset],
                              "block_time": x["blockTime"], "signature": x["signature"], "dst_label": c,
                              "is_pool": c == "pool", "terminal": c is not None and c != "pool", "truncated": tr})
        if len(exits) >= 50000:  # la mémoire devient du disque sur ce Mac : écrit au fil de l'eau
            w_exit.write_table(pa.Table.from_pylist(exits, schema=S_EXIT))
            n_exits += len(exits)
            exits = []
    w_exit.write_table(pa.Table.from_pylist(exits, schema=S_EXIT))
    w_exit.close()
    n_exits += len(exits)
    avant = len(funding)
    funding = une_ligne_par_cle(funding)
    pq.write_table(pa.Table.from_pylist(funding, schema=S_FUND), BIG / "funding_edges.parquet", compression="zstd")
    n_tr = sum(1 for v in trunc.values() if v)
    print(f"wallets={n} funding={len(funding)} (avant fusion {avant}) exits={n_exits} requêtes tronquées={n_tr}/{len(trunc)}")


if __name__ == "__main__":
    sys.exit(main())
