#!/usr/bin/env python3
"""Arêtes de transfert direct de DMAGA entre propriétaires, hors swap.

Source : lignes kind='transfer' de trades (pool, courbe, mint), puis `dmaga_all` de chaque wallet tracé
(getTransfersByAddress), qui voit les transferts sans référence au mint. Dédoublonnage par
(signature, from, to, qty). Sortie : BIG/token_edges.parquet.
Une arête prouve qu'un transfert a eu lieu, pas que les deux wallets ont le même propriétaire.
"""
import gzip
import json

import pyarrow as pa
import pyarrow.parquet as pq

from dmaga.config import RAW
from dmaga.db import connect
from dmaga.labels import label
from dmaga.paths import BIG, exige_v2

exige_v2()
con = connect(mem="700MB")
rows = {}
cur = con.execute("""SELECT signature, slot, block_time, owner, token_delta, venue, source FROM trades
                     WHERE kind='transfer' AND owner IS NOT NULL ORDER BY signature""")
batch, last = [], None


def flush(batch):
    outs = [(o, -d) for _, _, _, o, d, _, _ in batch if d < 0]
    ins = [(o, d) for _, _, _, o, d, _, _ in batch if d > 0]
    if not outs or not ins:
        return
    sig, slot, t = batch[0][:3]
    if len(outs) == 1:
        for o, q in ins:
            rows[(sig, outs[0][0], o, q)] = (slot, t, "tx_balances", len(ins))
    elif len(ins) == 1:
        for o, q in outs:
            rows[(sig, o, ins[0][0], q)] = (slot, t, "tx_balances", len(outs))
    else:  # plusieurs émetteurs et récepteurs : on n'invente pas d'appariement
        for o, q in outs:
            rows[(sig, o, "(multiple)", q)] = (slot, t, "tx_balances_ambiguous", len(ins))


while True:
    chunk = cur.fetchmany(20000)
    if not chunk:
        break
    for r in chunk:
        if r[0] != last and batch:
            flush(batch)
            batch = []
        last = r[0]
        batch.append(r)
if batch:
    flush(batch)
n_tx = len(rows)

n_w = 0
flows = RAW / "flows"
if flows.exists():
    for d in flows.iterdir():
        p = d / "dmaga_all.json.gz"
        if not p.exists() or d.name.startswith("._"):
            continue
        n_w += 1
        j = json.load(gzip.open(p))
        for x in j["rows"]:
            a, b = x.get("fromUserAccount"), x.get("toUserAccount")
            if a in (None,) or b in (None,):
                continue
            if label(a) or label(b):  # pool, courbe, migration : déjà comptés comme swaps
                continue
            q = int(x["amount"])
            rows.setdefault((x["signature"], a, b, q), (x["slot"], x["blockTime"], "gtba", 1))

out = [{"signature": k[0], "src": k[1], "dst": k[2], "qty": k[3] / 1e6, "slot": v[0], "block_time": v[1],
        "how": v[2], "n_counterparts": v[3], "src_label": label(k[1]), "dst_label": label(k[2])} for k, v in rows.items()]
pq.write_table(pa.Table.from_pylist(out), BIG / "token_edges.parquet", compression="zstd")
print(f"arêtes={len(out)} dont balances_tx={n_tx}, wallets gtba={n_w}")
