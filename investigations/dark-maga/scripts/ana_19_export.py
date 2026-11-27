#!/usr/bin/env python3
"""Matérialise data/trades.parquet : une version de chaque transaction (pool ou courbe avant mint), triée (slot, index)."""
from dmaga.config import BIG
from dmaga.db import connect

# Preserve the previous materialized result until the rebuilt export has passed validation.
# Mémoire bornée (machine partagée, garde à 1,2 Go) : DuckDB déborde sur le disque USB plutôt que de gonfler le processus.
con = connect(mem="500MB", threads=1, prefer_materialized=False)
tmp = BIG / "trades.tmp.parquet"
tmp.unlink(missing_ok=True)  # only an unfinished staging file, never the last good export
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
