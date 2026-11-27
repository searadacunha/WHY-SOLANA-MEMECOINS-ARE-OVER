#!/usr/bin/env python3
"""Matérialise data/trades.parquet : une version de chaque transaction (pool ou courbe avant mint), triée (slot, index)."""
from dmaga.config import BIG
from dmaga.db import connect

(BIG / "trades.parquet").unlink(missing_ok=True)
con = connect()
tmp = BIG / "trades.tmp.parquet"
con.execute(f"COPY (SELECT * FROM trades ORDER BY slot, tx_index) TO '{tmp}' (FORMAT parquet, COMPRESSION zstd)")
# Check the actual exported file, not just the deduplicated SQL view.
duplicates = con.execute(f"""
    SELECT count(*) FROM (
        SELECT 1 FROM read_parquet('{tmp}')
        GROUP BY signature, kind, owner, venue, token_delta
        HAVING count(*) > 1
    )""").fetchone()[0]
if duplicates:
    tmp.unlink(missing_ok=True)
    raise RuntimeError(f"refusing export with {duplicates} duplicate trade keys")
tmp.replace(BIG / "trades.parquet")
print(con.execute(f"SELECT count(*), count(DISTINCT signature) FROM read_parquet('{BIG}/trades.parquet')").fetchone())
