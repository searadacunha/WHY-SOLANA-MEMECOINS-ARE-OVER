"""Run the accounting pipeline on tiny local tables; no research cache or network."""
import importlib.util
from pathlib import Path
import sys

import duckdb
import pyarrow as pa
import pyarrow.parquet as pq
import pytest

from dmaga import venues


@pytest.fixture
def accounting(tmp_path, monkeypatch):
    monkeypatch.setattr(venues, "load", lambda: {})
    path = Path(__file__).resolve().parents[1] / "scripts" / "ana_20_pnl.py"
    spec = importlib.util.spec_from_file_location("pnl_pipeline", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    monkeypatch.setattr(module, "BIG", tmp_path)
    monkeypatch.setattr(module, "exige_v2", lambda: None)
    monkeypatch.setattr(sys, "argv", [str(path)])
    prices = {2: 100.0}
    monkeypatch.setattr(module, "sol_usd", lambda: prices)
    con = duckdb.connect(":memory:")
    con.execute("""CREATE TABLE trades(owner VARCHAR, kind VARCHAR, token_delta BIGINT,
        sol_lamports BIGINT, block_time BIGINT, signature VARCHAR, slot BIGINT,
        tx_index INTEGER, venue VARCHAR, usdc_raw BIGINT)""")
    con.execute("INSERT INTO trades VALUES ('buyer', 'swap', 100000000, -1000000000, 120, 'buy', 1, 0, 'raydium', 0)")
    con.execute("CREATE TABLE vault(vault VARCHAR, post BIGINT, block_time BIGINT, slot BIGINT, tx_index INTEGER)")
    con.executemany("INSERT INTO vault VALUES (?, ?, 120, 1, 0)",
                    [(module.VD, 1000 * 10**6), (module.VS, 100 * 10**9)])
    monkeypatch.setattr(module, "connect", lambda **kwargs: con)
    pq.write_table(pa.Table.from_pylist([{"account": "ata", "owner": "buyer", "post": 100000000,
                                        "slot": 1, "tx_index": 0, "block_time": 120}]),
                   tmp_path / "accounts.parquet")
    pq.write_table(pa.Table.from_pylist([], schema=pa.schema([
        ("owner", pa.string()), ("prev_owner", pa.string()), ("block_time", pa.int64())])),
        tmp_path / "account_ruptures.parquet")
    pq.write_table(pa.Table.from_pylist([], schema=pa.schema([
        ("signature", pa.string()), ("slot", pa.int64()), ("block_time", pa.int64()),
        ("src", pa.string()), ("dst", pa.string()), ("qty", pa.float64()), ("how", pa.string())])),
        tmp_path / "token_edges.parquet")
    yield module, con, prices
    con.close()


@pytest.mark.parametrize("stable", [False, True])
def test_missing_price_cannot_publish_a_partial_pnl(accounting, stable):
    module, con, prices = accounting
    if stable:
        con.execute("UPDATE trades SET sol_lamports=0, usdc_raw=-100000000")
    prices.clear()
    output = module.BIG / "wallets.parquet"
    output.write_bytes(b"previous verified output")
    with pytest.raises(ValueError, match="prix SOL/USD"):
        module.main()
    assert output.read_bytes() == b"previous verified output"


@pytest.mark.parametrize("price", [0, -1, float("nan"), float("inf")])
def test_invalid_quote_price_cannot_publish_a_pnl(accounting, price):
    module, con, prices = accounting
    prices[2] = price
    with pytest.raises(ValueError, match="prix SOL/USD"):
        module.main()
    assert not (module.BIG / "wallets.parquet").exists()


def test_missing_transfer_input_fails_before_accounting(accounting):
    module, _, _ = accounting
    (module.BIG / "token_edges.parquet").unlink()
    with pytest.raises(FileNotFoundError, match="token_edges.parquet"):
        module.main()
    assert not (module.BIG / "wallets.parquet").exists()


def test_stablecoin_swap_is_converted_at_its_own_minute(accounting):
    module, con, _ = accounting
    con.execute("UPDATE trades SET sol_lamports=0, usdc_raw=-100000000")
    module.main()
    row, = pq.read_table(module.BIG / "wallets.parquet").to_pylist()
    assert row["bought_sol"] == 1.0
    assert row["cost_usd"] == 100.0
    assert row["residual_qty"] == 100.0
    assert row["realized_sol"] == 0.0
