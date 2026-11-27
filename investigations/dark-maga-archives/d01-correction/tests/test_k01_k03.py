"""K01 : aucune ligne doublée, tranche du 23/07 coupée à minuit. K03 : l'autorité CPMM ne compte que les réserves de DMAGA."""
import gzip
import importlib.util
import json
import pathlib

import pyarrow as pa
import pyarrow.parquet as pq

import dmaga.db
from dmaga.config import MINT, WSOL
from dmaga.normalize import CPMM_AUTH, CPMM_PAIR, RAYDIUM_AUTH as AUTH, parse_tx

VD, VS = "vaultDmaga", "vaultSol"
ROOT = pathlib.Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("nrm10", ROOT / "scripts" / "nrm_10_trades.py")
nrm10 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(nrm10)


def bal(i, mint, owner, amount, dec=6):
    return {"accountIndex": i, "mint": mint, "owner": owner, "uiTokenAmount": {"amount": str(amount), "decimals": dec}}


def tx(pre, post, keys, sig="sig", t=2):
    return {"slot": 1, "blockTime": t, "transactionIndex": 3,
            "transaction": {"signatures": [sig], "message": {"accountKeys": [{"pubkey": k, "signer": i == 0} for i, k in enumerate(keys)]}},
            "meta": {"err": None, "fee": 5000, "preBalances": [0] * len(keys), "postBalances": [0] * len(keys), "preTokenBalances": pre, "postTokenBalances": post}}


def test_k03_wsol_of_another_cpmm_pool_is_ignored():
    # achat routé : le trader paie par un autre pool CPMM, 80 SOL entrent au vault Raydium de DMAGA, 80 SOL sortent d'une réserve étrangère
    keys = ("trader", VD, VS, "ata", "cpmmWsolAutrePool")
    pre = [bal(1, MINT, AUTH, 1000), bal(2, WSOL, AUTH, 500, 9), bal(3, MINT, "trader", 0), bal(4, WSOL, CPMM_AUTH, 900, 9)]
    post = [bal(1, MINT, AUTH, 900), bal(2, WSOL, AUTH, 580, 9), bal(3, MINT, "trader", 100), bal(4, WSOL, CPMM_AUTH, 820, 9)]
    rows = parse_tx(tx(pre, post, keys), {VD}, {VS}, "t", {CPMM_AUTH})
    assert [(r["kind"], r["owner"], r["token_delta"], r["sol_lamports"], r["venue"]) for r in rows] == [("swap", "trader", 100, -80, "raydium")]


def test_k03_cpmm_pair_stays_swap_other():
    # le pool CPMM de DMAGA, contre un autre jeton : quantité connue, valeur non comptée, jamais un dépôt de liquidité
    pair = next(iter(CPMM_PAIR))
    keys = ("trader", "dmagaCpmm", pair, "ata")
    pre = [bal(1, MINT, CPMM_AUTH, 1000), bal(2, "AutreJeton", CPMM_AUTH, 500), bal(3, MINT, "trader", 0)]
    post = [bal(1, MINT, CPMM_AUTH, 900), bal(2, "AutreJeton", CPMM_AUTH, 550), bal(3, MINT, "trader", 100)]
    rows = parse_tx(tx(pre, post, keys), {VD}, {VS}, "t", {CPMM_AUTH})
    assert [(r["kind"], r["owner"], r["token_delta"], r["sol_lamports"]) for r in rows] == [("swap_other", "trader", 100, 0)]


def _shard(path, sig, owner, delta, source="venue", venue="v", kind="swap"):
    t = pa.Table.from_pylist([{"signature": sig, "slot": 1, "tx_index": 1, "block_time": 5, "source": source, "kind": kind, "venue": venue, "owner": owner, "token_delta": delta}])
    pq.write_table(t, path)


def test_k01_view_keeps_one_line_when_two_histories_of_the_same_source_hold_a_tx(tmp_path, monkeypatch):
    for sub in ("trades_shards", "vault_shards"):
        (tmp_path / sub).mkdir()
    _shard(tmp_path / "trades_shards" / "a.parquet", "s1", "w", 10)
    _shard(tmp_path / "trades_shards" / "b.parquet", "s1", "w", 10)  # même transaction vue dans deux historiques de venues
    _shard(tmp_path / "trades_shards" / "c.parquet", "s1", "x", -10)  # autre propriétaire de la même transaction : à garder
    _shard(tmp_path / "trades_shards" / "d.parquet", "s2", "w", 10, source="mint")
    _shard(tmp_path / "trades_shards" / "e.parquet", "s2", "w", 10, source="pool")  # une source prioritaire écarte l'autre, comme avant
    pq.write_table(pa.Table.from_pylist([{"signature": "s1", "vault": "v", "pre": 0, "post": 1}]), tmp_path / "vault_shards" / "a.parquet")
    monkeypatch.setattr(dmaga.db, "BIG", tmp_path)
    con = dmaga.db.connect(mem="100MB", threads=1)
    assert sorted(con.execute("SELECT signature, owner, source FROM trades").fetchall()) == [("s1", "w", "venue"), ("s1", "x", "venue"), ("s2", "w", "pool")]


def test_k01_slice_stops_at_midnight_and_counts_every_line_read(tmp_path, monkeypatch):
    label = "full_pool/t1721777789"
    d = tmp_path / "raw" / label
    d.mkdir(parents=True)
    keys = ("trader", VD, VS, "ata")
    pre = [bal(1, MINT, AUTH, 1000), bal(2, WSOL, AUTH, 500, 9), bal(3, MINT, "trader", 0)]
    post = [bal(1, MINT, AUTH, 900), bal(2, WSOL, AUTH, 600, 9), bal(3, MINT, "trader", 100)]
    with gzip.open(d / "p000.jsonl.gz", "wt") as f:
        f.write(json.dumps(tx(pre, post, keys, "avant", 1721779199)) + "\n" + json.dumps(tx(pre, post, keys, "apres", 1721779200)) + "\n")
    (d / "cursor.json").write_text(json.dumps({"complete": True, "n": 2}))
    monkeypatch.setattr(nrm10, "RAW", tmp_path / "raw")
    monkeypatch.setattr(nrm10, "BIG", tmp_path / "big")
    monkeypatch.setattr(nrm10, "VAULT_DMAGA", {VD})
    monkeypatch.setattr(nrm10, "VAULT_WSOL", {VS})
    st = nrm10.process_slice((label, "pool"))
    assert st["tx"] == 2 and st["tx_hors_tranche"] == 1
    assert pq.read_table(tmp_path / "big" / "trades_shards" / "full_pool_t1721777789.parquet").column("signature").to_pylist() == ["avant"]
