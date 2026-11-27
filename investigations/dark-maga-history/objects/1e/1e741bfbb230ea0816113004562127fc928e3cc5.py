#!/usr/bin/env python3
"""Normalise le brut en un parquet de flux (data/trades.parquet) et une chaîne de soldes du pool.

Traitement page par page : mémoire bornée (voir la mémoire piege-memoire-devient-swap-disque).
Sortie : BIG/trades_shards/<tranche>.parquet, BIG/vault_shards/<tranche>.parquet, puis fusion triée.
Une page illisible fait échouer la tranche : rien n'est ignoré en silence.
"""
import gzip
import json
import sys
from collections import Counter
from multiprocessing import Pool
from pathlib import Path

import pyarrow as pa
import pyarrow.parquet as pq

from dmaga.config import BIG, MINT, RAW, WSOL
from dmaga.normalize import _keys, parse_tx, token_deltas
from dmaga.venues import load as load_venues

VAULT_DMAGA = {"5HuEsLbebeuottMsFW3hHcXTrKVsu3WUNSQnSr6aX4eL"}
VAULT_WSOL = {"3p7DbnWekWjtMQkey6fp1emdwXbAAxecnYuD5eU9ZZPH"}
VENUES = set(load_venues())

SCHEMA = pa.schema([
    ("signature", pa.string()), ("slot", pa.int64()), ("tx_index", pa.int32()), ("block_time", pa.int64()),
    ("fee_payer", pa.string()), ("signers", pa.string()), ("fee", pa.int64()), ("source", pa.string()),
    ("kind", pa.string()), ("venue", pa.string()), ("owner", pa.string()), ("token_delta", pa.int64()),
    ("sol_lamports", pa.int64()), ("usdc_raw", pa.int64()), ("pool_token_delta", pa.int64()), ("pool_sol_delta", pa.int64()),
    ("n_owners", pa.int32()), ("owner_native_delta", pa.int64()), ("owner_wsol_delta", pa.int64()),
])
VAULT_SCHEMA = pa.schema([
    ("signature", pa.string()), ("slot", pa.int64()), ("tx_index", pa.int32()), ("block_time", pa.int64()),
    ("vault", pa.string()), ("pre", pa.int64()), ("post", pa.int64()),
])


def process_slice(args):
    label, source = args
    d = RAW / label
    name = label.replace("/", "_")
    out = BIG / "trades_shards" / f"{name}.parquet"
    out_v = BIG / "vault_shards" / f"{name}.parquet"
    stats_path = BIG / "trades_shards" / f"{name}.stats.json"
    if stats_path.exists():
        return json.loads(stats_path.read_text())
    st = json.loads((d / "cursor.json").read_text())
    if not st["complete"]:
        raise RuntimeError(f"{label}: tranche incomplète")
    rows, vrows = [], []
    c = Counter()
    for p in sorted(d.glob("p*.jsonl.gz")):
        with gzip.open(p, "rt") as f:
            for line in f:
                tx = json.loads(line)
                c["tx"] += 1
                if tx["meta"].get("err") is not None:
                    c["tx_failed"] += 1
                    continue
                res = parse_tx(tx, VAULT_DMAGA, VAULT_WSOL, source, VENUES)
                if not res:
                    c["tx_no_dmaga_flow"] += 1
                for r in res:
                    c[f"kind_{r['kind']}"] += 1
                rows.extend(res)
                keys = _keys(tx)
                for dl in token_deltas(tx, keys):
                    # réserves de tous les venues : leur chaîne de soldes prouve qu'aucune transaction ne manque
                    if dl["account"] in VAULT_DMAGA or dl["account"] in VAULT_WSOL or (dl["mint"] == MINT and dl["owner"] in VENUES):
                        vrows.append({"signature": tx["transaction"]["signatures"][0], "slot": tx["slot"],
                                      "tx_index": tx.get("transactionIndex"), "block_time": tx.get("blockTime"),
                                      "vault": dl["account"], "pre": dl["pre"], "post": dl["post"]})
    if c["tx"] != st["n"]:
        raise RuntimeError(f"{label}: {c['tx']} lues pour {st['n']} au curseur")
    out.parent.mkdir(parents=True, exist_ok=True)
    out_v.parent.mkdir(parents=True, exist_ok=True)
    pq.write_table(pa.Table.from_pylist(rows, schema=SCHEMA), out, compression="zstd")
    pq.write_table(pa.Table.from_pylist(vrows, schema=VAULT_SCHEMA), out_v, compression="zstd")
    res = {"label": label, **c}
    stats_path.write_text(json.dumps(res))
    return res


def main():
    (BIG / "trades.parquet").unlink(missing_ok=True)  # la table finale est périmée dès qu'on renormalise
    if "--force" in sys.argv:
        for p in list((BIG / "trades_shards").glob("*")) + list((BIG / "vault_shards").glob("*")):
            p.unlink(missing_ok=True)  # FAT32 : le ._ disparaît avec son fichier
    labels = [("full_curve", "curve")]
    for p in sorted((RAW / "full_pool").glob("t*")):
        labels.append((f"full_pool/{p.name}", "pool"))
    for p in sorted((RAW / "full_mint").glob("t*")):
        labels.append((f"full_mint/{p.name}", "mint"))
    for p in sorted((RAW / "full_venue").glob("[!.]*")):
        labels.append((f"full_venue/{p.name}", "venue"))
    total = Counter()
    with Pool(3, maxtasksperchild=8) as pool:
        for i, r in enumerate(pool.imap_unordered(process_slice, labels), 1):
            total.update({k: v for k, v in r.items() if k != "label"})
            if i % 10 == 0 or i == len(labels):
                print(i, "/", len(labels), dict(total), flush=True)
    (BIG / "trades_stats.json").write_text(json.dumps(total, indent=1))
    print("FIN", dict(total))


if __name__ == "__main__":
    main()
