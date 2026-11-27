"""Sensibilité des fenêtres d'achat aux deux corrections d'événements (repost pmarca, capture @AutismCapital).

Même requête et mêmes exclusions que scripts/ana_50_cohorts.py, sur les données courantes. Trois colonnes par fenêtre :
le windows.csv publié avant correction (git), les anciennes bornes sur les données courantes, les nouvelles bornes. L'écart
entre les deux premières vient des données (déduplication du 06/11), pas des bornes. Sortie : data/windows_sensitivity.csv et
data/trades_1925_1930.csv (swaps reclassés de « indécidable » à « après la borne haute »)."""
import csv
import io
import subprocess
from h_lib import DATA, REPO
from dmaga.db import connect
from dmaga.venues import load as load_venues

OLD = {"pmarca_image_rouge": 1721512043, "musk_borne_haute": 1721590213}  # repost 21:47:23, Bailey 19:30:13
NEW = {"pmarca_image_rouge": 1721508414, "musk_borne_haute": 1721589923}  # original 20:46:54, realjohnnewburg 19:25:23
FIX = {"migration_raydium": 1720923331, "winig_visuel": 1721577749, "annonce_biden": 1721583960, "musk_borne_basse": 1721588607,
       "musk_retrait_borne_haute": 1721745389}


def windows(ev):
    h = ev["musk_borne_haute"]
    return [("avant_pmarca", ev["migration_raydium"], ev["pmarca_image_rouge"]), ("pmarca_a_winig", ev["pmarca_image_rouge"], ev["winig_visuel"]),
            ("fenetre_musk", ev["musk_borne_basse"], h), ("musk_plus_1h", h, h + 3600), ("musk_1h_6h", h + 3600, h + 6 * 3600),
            ("musk_6h_24h", h + 6 * 3600, h + 24 * 3600), ("jusqua_retrait", h + 24 * 3600, ev["musk_retrait_borne_haute"])]


def measure(con, a, b):
    r = con.execute(f"""
      WITH s AS (SELECT owner, token_delta, sol_lamports FROM trades
                 WHERE kind='swap' AND block_time>={a} AND block_time<{b} AND owner NOT IN (SELECT a FROM excl)),
      f AS (SELECT owner, min(block_time) t0 FROM trades WHERE kind='swap' AND token_delta>0 GROUP BY 1)
      SELECT (SELECT round(coalesce(sum(-sol_lamports),0)/1e9,2) FROM s WHERE token_delta>0),
             (SELECT round(coalesce(sum(sol_lamports),0)/1e9,2) FROM s WHERE token_delta<0),
             (SELECT count(*) FROM s WHERE token_delta>0), (SELECT count(*) FROM s WHERE token_delta<0),
             (SELECT count(DISTINCT owner) FROM s), (SELECT count(*) FROM f WHERE t0>={a} AND t0<{b})""").fetchone()
    return dict(zip(("buy_sol", "sell_sol", "n_buys", "n_sells", "wallets", "new_buyers"), r))


def main():
    con = connect()
    excl = set(load_venues()) | {"5Q544fKrFoe6tsEbD7S8EmxGTJYAKtTVhAW5Q5pge4j1", "87g44hEXP7R8ZxoAJtz941tsVftpEXC1LqAFTf2ZHtkH",
                                 "39azUYFWPz3VHgKCf3VChUwbpURdCHRxjWVowf5jUJjg", "PNLCQcVCD26aC7ZWgRyr5ptfaR7bBrWdTFgRWwu2tvF"}
    con.execute("CREATE TEMP TABLE excl(a VARCHAR)")
    con.executemany("INSERT INTO excl VALUES (?)", [[a] for a in excl])
    pub = {r["window"]: r for r in csv.DictReader(io.StringIO(subprocess.run(
        ["git", "-C", str(REPO), "show", "e458794:data/windows.csv"], capture_output=True, text=True, check=True).stdout))}
    rows = []
    for (name, a0, b0), (_, a1, b1) in zip(windows({**FIX, **OLD}), windows({**FIX, **NEW})):
        o, n = measure(con, a0, b0), measure(con, a1, b1)
        rows.append({"window": name, "published_buy_sol": pub[name]["buy_sol"], "published_new_buyers": pub[name]["new_buyers"],
                     "old_bounds_from": a0, "old_bounds_to": b0, **{f"old_{k}": v for k, v in o.items()},
                     "new_bounds_from": a1, "new_bounds_to": b1, **{f"new_{k}": v for k, v in n.items()}})
    for name, a, b in (("reclasse_1925_1930", NEW["musk_borne_haute"], OLD["musk_borne_haute"]),
                       ("dont_1925_1927_avant_autismcapital", NEW["musk_borne_haute"], 1721590044),
                       ("reclasse_pmarca_2046_2147", NEW["pmarca_image_rouge"], OLD["pmarca_image_rouge"]),
                       ("envoi_image_a_borne_haute", 1721589800, NEW["musk_borne_haute"])):
        rows.append({"window": name, "new_bounds_from": a, "new_bounds_to": b, **{f"new_{k}": v for k, v in measure(con, a, b).items()}})
    with (DATA / "windows_sensitivity.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    det = con.execute(f"""SELECT block_time, slot, tx_index, signature, owner, token_delta, sol_lamports FROM trades
        WHERE kind='swap' AND block_time>={NEW['musk_borne_haute']} AND block_time<{OLD['musk_borne_haute']}
        AND owner NOT IN (SELECT a FROM excl) ORDER BY slot, tx_index""").fetchall()
    with (DATA / "trades_1925_1930.csv").open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["block_time", "slot", "tx_index", "signature", "owner", "token_delta_raw", "sol_lamports"])
        w.writerows(det)
    for r in rows:
        print(r["window"], {k: r.get(k) for k in ("published_buy_sol", "old_buy_sol", "new_buy_sol", "new_n_buys", "new_wallets", "new_new_buyers")})
    print("swaps reclassés 19:25:23-19:30:13 :", len(det))


if __name__ == "__main__":
    main()
