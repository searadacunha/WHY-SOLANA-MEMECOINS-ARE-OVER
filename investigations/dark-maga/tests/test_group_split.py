"""Régression des fenêtres disjointes, sans collecte ni corpus USB."""
import csv
import json
from decimal import Decimal
from pathlib import Path

import duckdb

from dmaga.group_split import window_purchases


ROOT = Path(__file__).resolve().parents[1]
REPLAY_DATA = ROOT / "investigations/2026-11-06_historical_replay/data"


def trade_table():
    con = duckdb.connect()
    con.execute("""CREATE TABLE trades(
        owner VARCHAR, kind VARCHAR, token_delta BIGINT,
        sol_lamports BIGINT, block_time BIGINT)""")
    return con


def test_purchases_use_disjoint_half_open_windows():
    events = {"musk_borne_basse": 100, "musk_envoi_image": 200, "musk_borne_haute": 300}
    with trade_table() as con:
        con.executemany("INSERT INTO trades VALUES (?, ?, ?, ?, ?)", [
            ("too_early", "swap", 1, -8_000_000_000, 99),
            ("first", "swap", 1, -1_000_000_000, 100),
            ("first", "swap", 1, -2_000_000_000, 199),
            ("second", "swap", 1, -4_000_000_000, 200),
            ("third", "swap", 1, -8_000_000_000, 299),
            ("at_capture", "swap", 1, -16_000_000_000, 300),
            ("after_capture", "swap", 1, -32_000_000_000, 301),
            ("seller", "swap", -1, 64_000_000_000, 250),
            ("receiver", "transfer", 1, 0, 250),
        ])
        assert window_purchases(con, events) == {
            "borne_basse_a_envoi": (3.0, 1),
            "envoi_a_borne_haute": (12.0, 2),
        }


def test_published_upper_bound_trades_explain_historical_overlap():
    events = {e["name"]: e["t"] for e in json.loads((ROOT / "data/events.json").read_text())}
    with (REPLAY_DATA / "trades_1925_1930.csv").open() as f:
        rows = [r for r in csv.DictReader(f)
                if int(r["block_time"]) == events["musk_borne_haute"]
                and int(r["token_delta_raw"]) > 0]
    assert len(rows) == 2
    with trade_table() as con:
        con.executemany("INSERT INTO trades VALUES (?, ?, ?, ?, ?)", [
            (r["owner"], "swap", int(r["token_delta_raw"]),
             int(r["sol_lamports"]), int(r["block_time"])) for r in rows
        ])
        assert window_purchases(con, events) == {
            "borne_basse_a_envoi": (0.0, 0),
            "envoi_a_borne_haute": (0.0, 0),
        }

    # Le bilan daté garde la valeur historique, même après régénération des données.
    historical = json.loads(
        (ROOT / "reports/data_checks/rebuild_20261107.json").read_text(), parse_float=Decimal,
    )
    before_fix = next(r["apres"] for r in historical["group_split_changements"]
                      if r["chemin"] == "/achats_fenetre/envoi_a_borne_haute/sol")
    overlap = Decimal(sum(-int(r["sol_lamports"]) for r in rows)) / Decimal(10**9)
    assert overlap == Decimal("0.277882029")
    corrected = before_fix - overlap
    assert corrected == Decimal("17.561000000")
    with (REPLAY_DATA / "windows_sensitivity.csv").open() as f:
        replay = next(r for r in csv.DictReader(f) if r["window"] == "envoi_image_a_borne_haute")
    assert corrected.quantize(Decimal("0.01")) == Decimal(replay["new_buy_sol"])
    group_split = json.loads((ROOT / "data/group_split.json").read_text(), parse_float=Decimal)
    total = group_split["achats_fenetre"]["borne_basse_a_envoi"]["sol"] + corrected
    with (ROOT / "data/windows.csv").open() as f:
        window = next(r for r in csv.DictReader(f) if r["window"] == "fenetre_musk")
    assert total.quantize(Decimal("0.01")) == Decimal(window["buy_sol"])
