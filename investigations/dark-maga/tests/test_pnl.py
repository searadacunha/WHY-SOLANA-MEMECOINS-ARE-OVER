import importlib.util
from pathlib import Path

import duckdb
import pyarrow as pa
import pyarrow.parquet as pq
import pytest

from dmaga.pnl import Wallet

L = 10**9


def buy(w, q, s, t=1):
    w.apply("swap", q, -s, t, "s", 1, 1, "raydium")


def sell(w, q, s, t=2):
    w.apply("swap", -q, s, t, "s", 1, 1, "raydium")


def test_average_cost_realized():
    w = Wallet("a")
    buy(w, 100, 10 * L)
    buy(w, 100, 30 * L)
    sell(w, 100, 50 * L)
    assert w.realized == 30 * L  # coût moyen 0,2 SOL par jeton : 100 jetons coûtent 20 SOL
    assert w.qty == 100 and w.cost == 20 * L


def test_sell_beyond_known_qty_is_flagged_not_hidden():
    w = Wallet("a")
    buy(w, 10, 1 * L)
    sell(w, 30, 9 * L)
    assert w.sold_no_basis_qty == 20
    assert w.qty == 0 and w.realized == 8 * L
    assert "ventes sans quantité" in w.completeness


def test_transfer_in_has_no_cost_and_is_flagged():
    w = Wallet("a")
    w.apply("transfer", 50, 0, 1, "s", 1, 1, None)
    sell(w, 50, 5 * L)
    assert w.realized == 5 * L and w.transfer_in_qty == 50
    assert "reçus" in w.completeness


def test_transfer_out_removes_cost():
    w = Wallet("a")
    buy(w, 100, 10 * L)
    w.apply("transfer", -50, 0, 2, "s", 1, 1, None)
    assert w.qty == 50 and w.cost == 5 * L and w.realized == 0


def test_unrealized_is_never_in_realized():
    w = Wallet("a")
    buy(w, 100, 10 * L)
    assert w.realized == 0 and w.sold_sol == 0


def test_lp_deposit_leaves_stock_without_realized():
    w = Wallet("a")
    buy(w, 100, 10 * L)
    w.apply("lp_add", -60, 0, 2, "s", 1, 1, "dlmm")
    assert w.qty == 40 and w.lp_token_in == 60 and w.realized == 0 and w.sold_sol == 0
    assert "liquidité" in w.completeness


@pytest.fixture
def run_pnl(tmp_path, monkeypatch):
    """Exercise the actual export with tiny, offline trade and GTBA fixtures."""
    path = Path(__file__).resolve().parents[1] / "scripts" / "ana_20_pnl.py"
    spec = importlib.util.spec_from_file_location("ana_20_pnl_test", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    con = duckdb.connect(config={"threads": 1})
    con.execute("""CREATE TABLE trades(
        owner VARCHAR, kind VARCHAR, token_delta BIGINT, sol_lamports BIGINT,
        block_time BIGINT, signature VARCHAR, slot BIGINT, tx_index INTEGER,
        venue VARCHAR, usdc_raw BIGINT)""")
    con.execute("CREATE TABLE vault(vault VARCHAR, post BIGINT, block_time BIGINT, slot BIGINT, tx_index INTEGER)")
    con.executemany("INSERT INTO vault VALUES (?, ?, 180, 3, 0)", [
        (module.VD, 100_000_000), (module.VS, 100 * L),
    ])
    monkeypatch.setattr(module, "BIG", tmp_path)
    monkeypatch.setattr(module, "VENUES", set())
    monkeypatch.setattr(module, "connect", lambda: con)
    monkeypatch.setattr(module, "sol_usd", lambda: {1: 100.0, 2: 100.0, 3: 100.0})
    monkeypatch.setattr(module.sys, "argv", [str(path)])

    def run(edges, buys, sells=(), *, prices=None, quote="sol"):
        if prices is not None:
            monkeypatch.setattr(module, "sol_usd", lambda: prices)
        trades = [(owner, "swap", qty, -cost if quote == "sol" else 0,
                   60, "buy_" + owner, 1, i, "test", -cost if quote == "usdc" else 0)
                  for i, (owner, qty, cost) in enumerate(buys)]
        trades += [(owner, "swap", -qty, proceeds if quote == "sol" else 0,
                    180, "sell_" + owner, 3, i, "test", proceeds if quote == "usdc" else 0)
                   for i, (owner, qty, proceeds) in enumerate(sells)]
        con.executemany("INSERT INTO trades VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", trades)
        if edges:
            pq.write_table(pa.Table.from_pylist([
                {"signature": "transfer", "slot": 2, "block_time": 120,
                 "src": src, "dst": dst, "qty": qty / 1e6, "how": "gtba"}
                for src, dst, qty in edges
            ]), tmp_path / "token_edges.parquet")
        module.main()
        return {r["owner"]: r for r in pq.read_table(tmp_path / "wallets.parquet").to_pylist()}

    yield run
    con.close()


def test_gtba_self_transfer_preserves_stock_and_cost(run_pnl):
    rows = run_pnl([("A", "A", 50_000_000)], [("A", 100_000_000, 10 * L)])
    assert rows["A"]["residual_qty"] == 100
    assert rows["A"]["residual_cost_sol"] == 10
    assert rows["A"]["n_transfers"] == 0


def test_gtba_pass_through_preserves_existing_cost_and_realized_pnl(run_pnl):
    # B only forwards A's tokens within this transaction; its old inventory is intact.
    rows = run_pnl([("A", "B", 50_000_000), ("B", "C", 50_000_000)],
                   [("A", 100_000_000, 10 * L), ("B", 20_000_000, 4 * L)],
                   [("B", 20_000_000, 8 * L)])
    assert rows["A"]["residual_qty"] == 50
    assert rows["A"]["residual_cost_sol"] == 5
    assert rows["B"]["residual_qty"] == 0
    assert rows["B"]["realized_sol"] == 4
    assert rows["B"]["n_transfers"] == 0
    assert rows["C"]["residual_qty"] == 50
    assert rows["C"]["transfer_in_qty"] == 50


def test_gtba_real_transfer_preserves_both_legs(run_pnl):
    rows = run_pnl([("A", "B", 40_000_000)], [("A", 100_000_000, 10 * L)])
    assert rows["A"]["residual_qty"] == 60
    assert rows["A"]["residual_cost_sol"] == 6
    assert rows["A"]["transfer_out_qty"] == 40
    assert rows["B"]["residual_qty"] == 40
    assert rows["B"]["transfer_in_qty"] == 40
    assert rows["B"]["residual_cost_sol"] == 0
    assert "reçus sans coût" in rows["B"]["completeness"]


def test_gtba_partial_pass_through_counts_only_net_inventory(run_pnl):
    rows = run_pnl([("A", "B", 50_000_000), ("B", "C", 30_000_000)],
                   [("A", 100_000_000, 10 * L), ("B", 20_000_000, 4 * L)])
    assert rows["B"]["residual_qty"] == 40
    assert rows["B"]["residual_cost_sol"] == 4
    assert rows["B"]["transfer_in_qty"] == 20
    assert rows["B"]["transfer_out_qty"] == 0


@pytest.mark.parametrize("bad_price", [None, 0.0, -1.0, float("nan"), float("inf"), -float("inf")])
@pytest.mark.parametrize("quote", ["sol", "usdc"])
@pytest.mark.parametrize("minute", [1, 3], ids=["buy", "sell"])
def test_invalid_required_price_preserves_previous_export(run_pnl, tmp_path, bad_price, quote, minute):
    output = tmp_path / "wallets.parquet"
    pq.write_table(pa.Table.from_pylist([{"known_good_export": "keep"}]), output)
    before = output.read_bytes()
    prices = {1: 100.0, 2: 100.0, 3: 100.0}
    if bad_price is None:
        del prices[minute]
    else:
        prices[minute] = bad_price
    amount = 10 * L if quote == "sol" else 100_000_000
    with pytest.raises(RuntimeError, match="prix SOL/USD"):
        run_pnl([], [("A", 100_000_000, amount)], [("A", 100_000_000, 2 * amount)],
                prices=prices, quote=quote)
    assert output.read_bytes() == before


def test_valid_stablecoin_quotes_keep_sol_and_usd_accounting(run_pnl):
    rows = run_pnl([], [("A", 100_000_000, 100_000_000)], [("A", 100_000_000, 200_000_000)],
                   prices={1: 100.0, 3: 200.0}, quote="usdc")
    assert rows["A"]["bought_sol"] == 1
    assert rows["A"]["sold_sol"] == 1
    assert rows["A"]["cost_usd"] == 100
    assert rows["A"]["proceeds_usd"] == 200
    assert rows["A"]["realized_sol"] == 0
