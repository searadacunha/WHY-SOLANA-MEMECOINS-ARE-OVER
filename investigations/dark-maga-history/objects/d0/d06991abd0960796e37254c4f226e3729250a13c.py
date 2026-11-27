#!/usr/bin/env python3
"""PnL par wallet, au coût moyen, sur l'historique normalisé. Rend data/wallets.parquet + prix minute.

Prix du pool : réserve WSOL / réserve DMAGA après chaque transaction. Prix USD : clôture SOLUSDT 1 min.
Valorisation résiduelle : quantité restante × prix du pool à la date de coupure, indiquée en clair.
"""
import csv
import io
import sys
import zipfile
from pathlib import Path

import pyarrow as pa
import pyarrow.parquet as pq

from dmaga.config import BIG, RAW
from dmaga.db import connect
from dmaga.pnl import Wallet
from dmaga.venues import load as load_venues

VD = "5HuEsLbebeuottMsFW3hHcXTrKVsu3WUNSQnSr6aX4eL"
VS = "3p7DbnWekWjtMQkey6fp1emdwXbAAxecnYuD5eU9ZZPH"
EXCLUDE = {"5Q544fKrFoe6tsEbD7S8EmxGTJYAKtTVhAW5Q5pge4j1", "87g44hEXP7R8ZxoAJtz941tsVftpEXC1LqAFTf2ZHtkH",
           "39azUYFWPz3VHgKCf3VChUwbpURdCHRxjWVowf5jUJjg", "PNLCQcVCD26aC7ZWgRyr5ptfaR7bBrWdTFgRWwu2tvF"}
VENUES = set(load_venues())


def sol_usd() -> dict[int, float]:
    """Minute unix -> clôture SOLUSDT (fichiers mensuels publics Binance)."""
    out = {}
    for z in sorted((RAW / "solusd").glob("SOLUSDT-1m-*.zip")):
        if z.name.startswith("._"):
            continue
        with zipfile.ZipFile(z) as f:
            with f.open(f.namelist()[0]) as fh:
                for row in csv.reader(io.TextIOWrapper(fh)):
                    if not row or not row[0].isdigit():
                        continue
                    ms = int(row[0])
                    ms = ms // 1000 if ms > 10**14 else ms  # Binance est passé aux microsecondes en 2025
                    out[ms // 60000] = float(row[4])
    if not out:
        raise RuntimeError("aucun prix SOL/USD chargé")
    return out


def main():
    cutoff = int(sys.argv[1]) if len(sys.argv) > 1 else None
    px = sol_usd()
    con = connect()
    where = f"AND block_time < {cutoff}" if cutoff else ""
    wallets: dict[str, Wallet] = {}
    usd_cost: dict[str, float] = {}
    usd_proceeds: dict[str, float] = {}
    missing_px = 0
    n = 0
    # transferts vus seulement par getTransfersByAddress (SPL sans référence au mint) : deux lignes par arête, sans double compte
    edges = BIG / "token_edges.parquet"
    extra = ""
    if edges.exists():
        con.execute(f"""CREATE TEMP TABLE x AS SELECT e.signature, e.slot, e.block_time, e.src, e.dst, CAST(round(e.qty*1e6) AS BIGINT) q
            FROM read_parquet('{edges}') e WHERE e.how='gtba' AND e.dst <> '(multiple)' AND NOT EXISTS
            (SELECT 1 FROM trades t WHERE t.signature=e.signature AND (t.owner=e.src OR t.owner=e.dst))""")
        cut = f"AND block_time < {cutoff}" if cutoff else ""
        extra = f"""UNION ALL SELECT src, 'transfer', -q, 0, block_time, signature, slot, 2147483647, NULL, 0 FROM x WHERE 1=1 {cut}
                    UNION ALL SELECT dst, 'transfer', q, 0, block_time, signature, slot, 2147483647, NULL, 0 FROM x WHERE 1=1 {cut}"""
        print("transferts ajoutés depuis les flux", con.execute("SELECT count(*) FROM x").fetchone()[0])
    cur = con.execute(f"""SELECT owner, kind, token_delta, sol_lamports, block_time, signature, slot, tx_index, venue, usdc_raw
                          FROM trades WHERE kind IN ('swap','transfer','lp_add','lp_remove','fee_share','swap_other') AND owner IS NOT NULL {where}
                          {extra}
                          ORDER BY slot, tx_index""")
    while True:
        rows = cur.fetchmany(50000)
        if not rows:
            break
        for owner, kind, td, sol, t, sig, slot, idx, venue, usdc in rows:
            n += 1
            if owner in EXCLUDE or owner in VENUES:
                continue
            if usdc:  # part du swap passée par un pool USDC, convertie en SOL à la minute du trade
                p = px.get(t // 60)
                if p is None:
                    missing_px += 1
                else:
                    sol += int(usdc / 1e6 / p * 1e9)
            w = wallets.setdefault(owner, Wallet(owner))
            w.apply(kind, td, sol, t, sig, slot, idx, venue)
            if kind == "swap":
                p = px.get(t // 60)
                if p is None:
                    missing_px += 1
                    continue
                if td > 0:
                    usd_cost[owner] = usd_cost.get(owner, 0) + (-sol / 1e9) * p
                else:
                    usd_proceeds[owner] = usd_proceeds.get(owner, 0) + (sol / 1e9) * p
    last_dmaga = con.execute(f"SELECT post, block_time FROM vault WHERE vault='{VD}' {where} ORDER BY slot DESC, tx_index DESC LIMIT 1").fetchone()
    last_sol = con.execute(f"SELECT post FROM vault WHERE vault='{VS}' {where} ORDER BY slot DESC, tx_index DESC LIMIT 1").fetchone()
    price_sol = (last_sol[0] / 1e9) / (last_dmaga[0] / 1e6)
    ref_t = last_dmaga[1]
    ref_usd = px.get(ref_t // 60)
    rows = []
    for w in wallets.values():
        rows.append({
            "owner": w.owner, "n_buys": w.n_buys, "n_sells": w.n_sells, "n_transfers": w.n_transfers,
            "bought_qty": w.bought_qty / 1e6, "bought_sol": w.bought_sol / 1e9, "sold_qty": w.sold_qty / 1e6,
            "sold_sol": w.sold_sol / 1e9, "realized_sol": w.realized / 1e9, "cost_usd": usd_cost.get(w.owner, 0.0),
            "proceeds_usd": usd_proceeds.get(w.owner, 0.0),
            "residual_qty": w.qty / 1e6, "residual_cost_sol": w.cost / 1e9,
            "residual_value_sol_at_cutoff": w.qty / 1e6 * price_sol,
            "lp_token_in": w.lp_token_in / 1e6, "lp_token_out": w.lp_token_out / 1e6,
            "lp_sol_in": w.lp_sol_in / 1e9, "lp_sol_out": w.lp_sol_out / 1e9,
            "net_sol_all": (w.sold_sol - w.bought_sol + w.lp_sol_out - w.lp_sol_in) / 1e9,
            "transfer_in_qty": w.transfer_in_qty / 1e6, "transfer_out_qty": w.transfer_out_qty / 1e6,
            "sold_no_basis_qty": w.sold_no_basis_qty / 1e6,
            "first_buy_time": w.first_buy_time, "first_buy_sig": w.first_buy_sig, "first_buy_slot": w.first_buy_slot,
            "first_buy_tx_index": w.first_buy_tx_index,
            "first_buy_sol": (w.first_buy_sol or 0) / 1e9, "first_buy_qty": (w.first_buy_qty or 0) / 1e6,
            "first_sell_time": w.first_sell_time, "last_sell_time": w.last_sell_time,
            "last_activity_time": w.last_activity_time, "venues": ",".join(sorted(w.venues)),
            "completeness": w.completeness, "valuation_ref_time": ref_t,
        })
    table = pa.Table.from_pylist(rows)
    BIG.mkdir(parents=True, exist_ok=True)
    pq.write_table(table, BIG / "wallets.parquet", compression="zstd")
    print(f"lignes={n} wallets={len(rows)} sans_prix_usd={missing_px} prix_ref={price_sol:.10f} SOL à t={ref_t} usd_sol={ref_usd}")


if __name__ == "__main__":
    main()
