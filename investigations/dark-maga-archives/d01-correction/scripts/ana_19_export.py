#!/usr/bin/env python3
"""Matérialise data/trades.parquet : une version de chaque transaction (pool ou courbe avant mint), sans ligne doublée, triée (slot, index)."""
from dmaga.db import connect
from dmaga.paths import BIG, exige_v2

exige_v2()
(BIG / "trades.parquet").unlink(missing_ok=True)
con = connect(mem="700MB")
tmp = BIG / "trades.tmp.parquet"
con.execute(f"COPY (SELECT * FROM trades ORDER BY slot, tx_index) TO '{tmp}' (FORMAT parquet, COMPRESSION zstd)")
tmp.replace(BIG / "trades.parquet")
print(con.execute(f"SELECT count(*), count(DISTINCT signature) FROM read_parquet('{BIG}/trades.parquet')").fetchone())
