"""A5 (@Orkusx, « IN 20 USD / OUT 60K USD » pour AtZj, 22/07 10:24:15) et A6 (@JLKHatesYou, trois ventes de GXZvX « 2 h avant »
le changement de photo, 23/07 16:00:13) : coût complet, produits et horaires.

Coût des jetons reçus par AtZj : achats des quatre wallets expéditeurs du lancement (virements relus en h39, absents de
trades.parquet car en `Transfer` simple), au cours SOLUSDT de chaque minute. Convention de coût moyen pondéré, écrite.
Sortie : data/atzj_gxzvx.json."""
import json
import duckdb
from h_lib import DATA, DMAGA_BIG, sol_usd, utc

B = str(DMAGA_BIG).replace("/data", "/data_v2")
ATZJ = "AtZjv3DuV9cLn3Jxm72TMSdTN4aM6CrBaGyxUC4c2wDk"
GXZ = "GXZvXsD6hxaLeFvQisWpdAwsayJxga7w9EeafhFZG2Ra"
T_ORKUS, T_JLK = 1721643855, 1721750413
WB_OLD, IMG_NEW, WB_NEW = 1721731385, 1721743284, 1721745389  # Wayback ancien avatar 10:43:05 ; id image 14:01:24 (B) ; Wayback nouvel avatar 14:36:29


def main():
    con = duckdb.connect(config={"memory_limit": "200MB", "threads": 1})
    q = lambda s: con.execute(s).fetchall()
    own = q(f"select block_time, token_delta, sol_lamports from '{B}/trades.parquet' where owner='{ATZJ}' and kind='swap' and block_time<={T_ORKUS} order by slot, tx_index")
    buys = [r for r in own if r[1] > 0]
    sells = [r for r in own if r[1] < 0]
    inflow = q(f"select src, sum(qty) from '{B}/token_edges.parquet' where dst='{ATZJ}' and block_time<={T_ORKUS} and qty>=1 group by 1")
    senders = {}
    for src, qty in inflow:
        b = q(f"select block_time, token_delta, sol_lamports from '{B}/trades.parquet' where owner='{src}' and kind='swap' and token_delta>0 and block_time<={T_ORKUS}")
        senders[src] = {"tokens_sent_to_atzj": qty, "own_buys_tokens": sum(x[1] for x in b) / 1e6, "own_buys_sol": -sum(x[2] for x in b) / 1e9,
                        "own_buys_usd": round(sum(-x[2] / 1e9 * sol_usd(x[0]) for x in b), 2)}
    back = {d for (d,) in q(f"select distinct dst from '{B}/token_edges.parquet' where src='{ATZJ}' and block_time<={T_ORKUS}")}
    launch = {k: v for k, v in senders.items() if k not in back}  # un expéditeur qui avait d'abord reçu d'AtZj renvoie des jetons d'AtZj
    tok_in = sum(v["tokens_sent_to_atzj"] for v in launch.values()) + sum(r[1] for r in buys) / 1e6
    sol_in = sum(v["own_buys_sol"] * v["tokens_sent_to_atzj"] / v["own_buys_tokens"] for v in launch.values()) - sum(r[2] for r in buys) / 1e9
    usd_in = sum(v["own_buys_usd"] * v["tokens_sent_to_atzj"] / v["own_buys_tokens"] for v in launch.values()) + sum(-r[2] / 1e9 * sol_usd(r[0]) for r in buys)
    sold = -sum(r[1] for r in sells) / 1e6
    atzj = {"own_buys": len(buys), "own_buy_tokens": sum(r[1] for r in buys) / 1e6, "own_buy_sol": -sum(r[2] for r in buys) / 1e9,
            "own_buy_usd": round(sum(-r[2] / 1e9 * sol_usd(r[0]) for r in buys), 2), "senders": senders,
            "sells": len(sells), "sold_tokens": sold, "proceeds_sol": sum(r[2] for r in sells) / 1e9,
            "proceeds_usd": round(sum(r[2] / 1e9 * sol_usd(r[0]) for r in sells), 2), "first_sell_utc": utc(sells[0][0]), "last_sell_utc": utc(sells[-1][0]),
            "avg_cost_sol_per_token_consolidated": sol_in / tok_in, "cost_of_sold_tokens_sol_avg_method": sol_in / tok_in * sold,
            "cost_of_sold_tokens_usd_avg_method": round(usd_in / tok_in * sold, 2), "launch_senders_cost_sol": sum(v["own_buys_sol"] for v in launch.values()),
            "launch_senders_cost_usd": round(sum(v["own_buys_usd"] for v in launch.values()), 2), "return_senders_excluded": sorted(set(senders) - set(launch))}
    g = q(f"select block_time, token_delta, sol_lamports, usdc_raw, signature from '{B}/trades.parquet' where owner='{GXZ}' and kind='swap' order by slot, tx_index")
    gb, gs = [r for r in g if r[1] > 0], [r for r in g if r[1] < 0]
    usd = lambda r: r[2] / 1e9 * sol_usd(r[0]) + r[3] / 1e6
    last3 = gs[-3:]
    gx = {"buys": len(gb), "sells": len(gs), "buy_usd": round(sum(-usd(r) for r in gb), 2), "sell_usd": round(sum(usd(r) for r in gs), 2),
          "first_sell_utc": utc(gs[0][0]), "last3": [{"utc": utc(r[0]), "tokens": -r[1] / 1e6, "usd": round(usd(r), 2), "signature": r[4]} for r in last3],
          "last3_usd": round(sum(usd(r) for r in last3), 2), "last_sell_to_wayback_old_s": last3[-1][0] - WB_OLD,
          "last_sell_to_image_id_s": IMG_NEW - last3[-1][0], "last_sell_to_wayback_new_s": WB_NEW - last3[-1][0],
          "share_of_tokens_sold_on_23_07": sum(-r[1] for r in gs if r[0] >= 1721692800) / sum(-r[1] for r in gs)}
    out = {"atzj": atzj, "gxzvx": gx}
    (DATA / "atzj_gxzvx.json").write_text(json.dumps(out, indent=1))
    print(json.dumps(out, indent=1)[:2500])


if __name__ == "__main__":
    main()
