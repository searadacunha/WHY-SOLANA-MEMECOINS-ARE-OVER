"""Relecture des positifs de h51 : vraies ventes du jeton testé autour du premier achat DMAGA de chaque wallet.

Règle unique pour testés et témoins : premier achat DMAGA du wallet dans sa fenêtre (t_buy) ; transactions de l'ATA du jeton
testé dans [t_buy - 60 min, t_buy + 1 min] ; une « rotation » = solde du jeton en baisse pour le wallet dans cette plage.
usage: h52_rotation.py retiredio|kllary. Sortie : data/rotation_<test>.csv (une ligne par wallet relu)."""
import csv
import sys
import duckdb
from h_lib import DATA, DMAGA_BIG, utc
import k16_pubrpc as pub
from h_decode import sol_delta, token_delta
from h51_ata_test import KLLARY, RETIREDIO, T_BIDEN, T_LOW, T_WINIG

B = str(DMAGA_BIG).replace("/data", "/data_v2")
WIN = {"dmaga_buyer_biden_to_low": (T_BIDEN, T_LOW), "dmaga_buyer_winig_to_biden": (T_WINIG, T_BIDEN)}

if __name__ == "__main__":
    test = sys.argv[1]
    mint = RETIREDIO if test == "retiredio" else KLLARY
    rows = [r for r in csv.DictReader((DATA / f"ata_{test}.csv").open()) if int(r["n_sigs"]) > 0]
    con = duckdb.connect(config={"memory_limit": "200MB", "threads": 1})
    out = []
    for r in rows:
        o = r["owner"]
        a, b = WIN.get(r["set"], (0, 1721634134))
        tb = con.execute(f"select min(block_time) from '{B}/trades.parquet' where owner='{o}' and kind='swap' and token_delta>0 and block_time>={a} and block_time<{b}").fetchall()[0][0]
        if tb is None:  # kllary : premier achat DMAGA tout court
            tb = con.execute(f"select min(block_time) from '{B}/trades.parquet' where owner='{o}' and kind='swap' and token_delta>0").fetchall()[0][0]
        lo, hi = (tb - 3600, tb + 60) if test == "retiredio" else (0, 1721634134)
        sigs, _ = pub.sigs(r["ata"], max_pages=3)
        sel = sorted((x for x in sigs if not x.get("err") and lo <= x["blockTime"] <= hi), key=lambda x: x["slot"])
        sold = bought = sol_in = 0
        last_sell = None
        for x in sel:
            t = pub.tx(x["signature"])
            d = token_delta(t, o, mint)
            if d < 0:
                sold -= d
                sol_in += max(sol_delta(t, o), 0)
                last_sell = t["blockTime"]
            elif d > 0:
                bought += d
        out.append({"set": r["set"], "owner": o, "first_dmaga_buy_utc": utc(tb), "n_token_txs_in_range": len(sel), "token_sold_raw": sold,
                    "token_bought_raw": bought, "sol_from_sells_lamports": sol_in, "last_sell_utc": utc(last_sell) if last_sell else "",
                    "sell_to_buy_s": (tb - last_sell) if last_sell else "", "rotation": sold > 0})
        print(out[-1]["set"], o[:8], out[-1]["n_token_txs_in_range"], sold, out[-1]["sell_to_buy_s"], flush=True)
    with (DATA / f"rotation_{test}.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(out[0]))
        w.writeheader()
        w.writerows(out)
    for s in sorted({o["set"] for o in out}):
        g = [o for o in out if o["set"] == s]
        print(test, s, "relus", len(g), "rotations", sum(1 for o in g if o["rotation"]))
