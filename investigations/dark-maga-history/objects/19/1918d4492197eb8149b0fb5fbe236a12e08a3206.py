#!/usr/bin/env python3
"""Matérialise data/trades.parquet : une version de chaque transaction (pool ou courbe avant mint), triée (slot, index)."""
from dmaga.config import BIG
from dmaga.db import connect

(BIG / "trades.parquet").unlink(missing_ok=True)
con = connect()
tmp = BIG / "trades.tmp.parquet"
con.execute(f"COPY (SELECT * FROM trades ORDER BY slot, tx_index) TO '{tmp}' (FORMAT parquet, COMPRESSION zstd)")
tmp.replace(BIG / "trades.parquet")
print(con.execute(f"SELECT count(*), count(DISTINCT signature) FROM read_parquet('{BIG}/trades.parquet')").fetchone())
