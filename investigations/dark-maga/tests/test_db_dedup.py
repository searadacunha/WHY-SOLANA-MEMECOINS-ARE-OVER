"""Offline regression for duplicate trades in overlapping raw-history slices.

No RPC calls or production raw data are used.
"""
import duckdb

import dmaga.db as database


def _parquet(con, table, path):
    escaped = str(path).replace("'", "''")
    con.execute(f"COPY {table} TO '{escaped}' (FORMAT PARQUET)")


def test_overlapping_trades_are_counted_once(tmp_path, monkeypatch):
    monkeypatch.setattr(database, "BIG", tmp_path)
    monkeypatch.setattr(database, "TMP", tmp_path / "tmp")
    (tmp_path / "trades_shards").mkdir()
    (tmp_path / "vault_shards").mkdir()

    con = duckdb.connect()
    con.execute("""CREATE TABLE trade_data(
        signature VARCHAR, source VARCHAR, kind VARCHAR, owner VARCHAR,
        venue VARCHAR, token_delta BIGINT, slot BIGINT, tx_index INTEGER,
        sol_lamports BIGINT
    )""")
    con.executemany("INSERT INTO trade_data VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", [
        ("s1", "pool", "swap", "alice", "ray", 100, 1, 0, -50),
        ("s1", "pool", "swap", "alice", "ray", 100, 1, 0, -50),  # overlapping slice
        ("s1", "mint", "swap", "alice", "ray", 100, 1, 0, -50),  # less trusted history
        ("s2", "pool", "swap", "alice", "ray", -40, 2, 0, 30),
        ("s3", "pool", "transfer", "alice", None, -25, 3, 0, 0),
        ("s3", "pool", "transfer", "bob", None, 25, 3, 0, 0),
    ])
    con.execute("CREATE TABLE vault_data(signature VARCHAR, slot BIGINT)")
    con.execute("INSERT INTO vault_data VALUES ('s1', 1)")
    _parquet(con, "trade_data", tmp_path / "trades_shards" / "one.parquet")
    _parquet(con, "vault_data", tmp_path / "vault_shards" / "one.parquet")

    expected = [
        ("s1", "pool", "alice", 100),
        ("s2", "pool", "alice", -40),
        ("s3", "pool", "alice", -25),
        ("s3", "pool", "bob", 25),
    ]
    live = database.connect()
    try:
        assert live.execute("SELECT count(*) FROM trades_all").fetchone()[0] == 6
        rows = live.execute("SELECT signature, source, owner, token_delta FROM trades ORDER BY signature, owner").fetchall()
        assert rows == expected
    finally:
        live.close()

    # The same safeguard also applies to an already materialized (stale) table.
    _parquet(con, "trade_data", tmp_path / "trades.parquet")
    con.close()
    cached = database.connect()
    try:
        rows = cached.execute("SELECT signature, source, owner, token_delta FROM trades ORDER BY signature, owner").fetchall()
        assert rows == expected
    finally:
        cached.close()

    # A rebuild must use the shards even if a previous Parquet file still exists.
    # This lets the exporter validate a staging file before replacing the old one.
    fresh = database.connect(prefer_materialized=False)
    try:
        rows = fresh.execute("SELECT signature, source, owner, token_delta FROM trades ORDER BY signature, owner").fetchall()
        assert rows == expected
    finally:
        fresh.close()
