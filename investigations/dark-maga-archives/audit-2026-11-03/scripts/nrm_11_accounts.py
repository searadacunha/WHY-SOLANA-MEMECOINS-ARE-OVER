#!/usr/bin/env python3
"""Chaîne de chaque compte de jetons DMAGA, et programmes vus par les propriétaires non signataires. Un seul fichier par sortie, flux, sans réseau.

Sorties (BIG) : accounts.parquet (une ligne par variation), account_ruptures.parquet (solde avant différent du dernier solde vu : mouvement
absent du brut, K04, N12), owner_programs.parquet (programmes de premier niveau par propriétaire non signataire, K06).
"""
import gzip
import json

import pyarrow as pa
import pyarrow.parquet as pq

from dmaga.config import MINT, RAW
from dmaga.db import connect
from dmaga.normalize import _keys, _signers, token_deltas
from dmaga.paths import BIG, exige_v2

GENERIQUES = {"ComputeBudget111111111111111111111111111111", "11111111111111111111111111111111", "TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA",
              "TokenzQdBNbLqP5VEhdkAS6EPFLC1PHnBqCXEpPxuEb", "ATokenGPvbdGVxr1b2hvZbsiqW5xWH25efTNsLJA8knL", "MemoSq4gqABAXKb96qnH8TysNcWxMyWCqXgDLGmfcHr",
              "Memo1UhkJRfHyvLMcVucJwxXeuD728EqVDDwQDxFMNo"}
S_AC = pa.schema([("signature", pa.string()), ("slot", pa.int64()), ("tx_index", pa.int32()), ("block_time", pa.int64()),
                  ("account", pa.string()), ("owner", pa.string()), ("pre", pa.int64()), ("post", pa.int64())])
S_PR = pa.schema([("signature", pa.string()), ("owner", pa.string()), ("program", pa.string())])
TMP_AC, TMP_PR = BIG / "accounts.tmp.parquet", BIG / "owner_programs.tmp.parquet"


class Ecrivain:
    def __init__(self, path, schema):
        self.w, self.schema, self.buf = pq.ParquetWriter(path, schema, compression="zstd"), schema, []

    def add(self, row):
        self.buf.append(row)
        if len(self.buf) >= 20000:
            self.flush()

    def flush(self):
        if self.buf:
            self.w.write_table(pa.Table.from_pylist(self.buf, schema=self.schema))
            self.buf = []

    def close(self):
        self.flush()
        self.w.close()


def dossiers():
    yield RAW / "full_curve"
    for s in ("pool", "mint", "venue"):
        yield from sorted(p for p in (RAW / f"full_{s}").iterdir() if p.is_dir() and not p.name.startswith("._"))


def main():
    exige_v2()
    ac, pr = Ecrivain(TMP_AC, S_AC), Ecrivain(TMP_PR, S_PR)
    n = 0
    for d in dossiers():
        for p in sorted(x for x in d.iterdir() if x.name.endswith(".jsonl.gz") and not x.name.startswith("._")):
            with gzip.open(p, "rt") as f:
                for line in f:
                    t = json.loads(line)
                    n += 1
                    if t["meta"].get("err") is not None:
                        continue
                    keys = _keys(t)
                    ds = [x for x in token_deltas(t, keys) if x["mint"] == MINT]
                    if not ds:
                        continue
                    sig = t["transaction"]["signatures"][0]
                    for x in ds:
                        ac.add({"signature": sig, "slot": t["slot"], "tx_index": t.get("transactionIndex"), "block_time": t.get("blockTime"),
                                "account": x["account"], "owner": x["owner"], "pre": x["pre"], "post": x["post"]})
                    signers = set(_signers(t))
                    programs = {i.get("programId") for i in t["transaction"]["message"]["instructions"]} - GENERIQUES - {None}
                    for o in {x["owner"] for x in ds if x["owner"] and x["owner"] not in signers}:
                        for prog in programs:
                            pr.add({"signature": sig, "owner": o, "program": prog})
    ac.close()
    pr.close()
    print("transactions lues", n, flush=True)
    con = connect(mem="600MB")
    con.execute(f"COPY (SELECT DISTINCT * FROM read_parquet('{TMP_AC}') ORDER BY slot, tx_index) TO '{BIG}/accounts.parquet' (FORMAT parquet, COMPRESSION zstd)")
    con.execute(f"COPY (SELECT DISTINCT * FROM read_parquet('{TMP_PR}')) TO '{BIG}/owner_programs.parquet' (FORMAT parquet, COMPRESSION zstd)")
    con.execute(f"""COPY (WITH c AS (SELECT *, lag(post) OVER w prev, lag(block_time) OVER w prev_t, lag(owner) OVER w prev_owner
                                      FROM read_parquet('{BIG}/accounts.parquet') WINDOW w AS (PARTITION BY account ORDER BY slot, tx_index))
                          SELECT signature, slot, tx_index, block_time, account, owner, prev_owner, pre, post, prev, prev_t, pre - coalesce(prev, 0) gap
                          FROM c WHERE pre <> coalesce(prev, 0)) TO '{BIG}/account_ruptures.parquet' (FORMAT parquet, COMPRESSION zstd)""")
    TMP_AC.unlink()
    TMP_PR.unlink()
    print("lignes, comptes", con.execute(f"SELECT count(*), count(DISTINCT account) FROM read_parquet('{BIG}/accounts.parquet')").fetchone(),
          "ruptures, comptes", con.execute(f"SELECT count(*), count(DISTINCT account) FROM read_parquet('{BIG}/account_ruptures.parquet')").fetchone())


if __name__ == "__main__":
    main()
