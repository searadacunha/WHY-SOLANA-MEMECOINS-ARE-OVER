from dmaga.pnl import Wallet, residuel_corrige

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


def test_residual_applies_only_hidden_transfers_after_the_last_seen_balance():
    soldes = {"vide": 100, "revu": 70, "dest": 5}
    vu = {"vide": 10, "revu": 50, "dest": 10}
    # "vide" part après son dernier solde : retiré. "revu" part avant : son solde le reflète déjà. "dest" reçoit après son dernier solde : ajouté.
    r = residuel_corrige(soldes, vu, [("vide", "dest", 100, 20), ("revu", "autre", 30, 40)])
    assert r == {"vide": 0, "revu": 70, "dest": 105, "autre": 30}
