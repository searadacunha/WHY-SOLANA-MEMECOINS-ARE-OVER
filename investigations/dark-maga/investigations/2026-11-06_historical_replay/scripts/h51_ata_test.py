"""Recoupement par compte de jetons associé (ATA) : un wallet a-t-il touché un mint avant une date, et dans une fenêtre ?

Test fixé avant lecture : ensembles et fenêtres ci-dessous, mêmes requêtes pour le groupe testé et pour ses témoins.
Une activité d'ATA n'est pas forcément un achat (poussière, création par un tiers) : chaque positif est relu (h52).
Limite : un compte de jetons non associé échappe au test (méthode et contrôle 797/797 de k12, enquête Kekius).
usage: h51_ata_test.py kllary|retiredio. Sortie : data/ata_<test>.csv."""
import csv
import sys
import duckdb
from h_lib import DATA, DMAGA_BIG, NOAH
import k16_pubrpc as pub
from k12_ata import ata
from h32_noah import SAT

B = str(DMAGA_BIG).replace("/data", "/data_v2")
KLLARY = "AUS4wtGQZcb6GPQxU4K8FRVqQMwUx2Q8G7K9JKuUpump"
RETIREDIO = "DyKwrqZMEDVHYAd4gn9V8vFioQQg1bVEgGxqbUr5Mkvo"
T_JEFFRO = 1721634134       # 22/07 07:42:14, post de Jeffro
T_BIDEN, T_LOW, T_WINIG = 1721583960, 1721588607, 1721577749


def sets(test):
    con = duckdb.connect(config={"memory_limit": "200MB", "threads": 1})
    if test == "kllary":
        tested = [(f"noah{g}", a) for g, l in NOAH.items() for a in l] + [("jeffro_sat", a) for a in SAT]
        first = [o for (o,) in con.execute(f"select owner from '{B}/trades.parquet' where kind='swap' and token_delta>0 and owner is not null "
                                           "group by 1 order by min(block_time) limit 140").fetchall()]
        ctl = [("first140_buyers", o) for o in first if o not in {a for _, a in tested}]
        return KLLARY, tested + ctl, [("before_jeffro", 0, T_JEFFRO), ("two_weeks_before", T_JEFFRO - 21 * 86400, T_JEFFRO - 7 * 86400)]
    buy = lambda a, b: [o for (o,) in con.execute(f"select distinct owner from '{B}/trades.parquet' where kind='swap' and token_delta>0 "
                                                  f"and block_time>={a} and block_time<{b} and owner is not null").fetchall()]
    tested = [("dmaga_buyer_biden_to_low", o) for o in buy(T_BIDEN, T_LOW)]
    ctl = [("dmaga_buyer_winig_to_biden", o) for o in buy(T_WINIG, T_BIDEN) if o not in {a for _, a in tested}]
    return RETIREDIO, tested + ctl, [("ever_before_low", 0, T_LOW), ("on_21_07_before_low", T_LOW - 6 * 3600, T_LOW)]


if __name__ == "__main__":
    test = sys.argv[1]
    mint, wallets, wins = sets(test)
    rows = []
    for label, o in wallets:
        acc = ata(o, mint)
        s, trunc = pub.sigs(acc, max_pages=3)
        ok = [x for x in s if not x.get("err")]
        r = {"set": label, "owner": o, "ata": acc, "n_sigs": len(ok), "truncated": trunc,
             "first_utc_unix": min((x["blockTime"] for x in ok), default=""), "first_sig": min(ok, key=lambda x: x["slot"])["signature"] if ok else ""}
        for name, a, b in wins:
            r[name] = sum(1 for x in ok if a <= x["blockTime"] < b)
        rows.append(r)
    with (DATA / f"ata_{test}.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    for lab in sorted({r["set"] for r in rows}):
        g = [r for r in rows if r["set"] == lab]
        print(test, lab, "n", len(g), {name: sum(1 for r in g if r[name] > 0) for name, _, _ in wins}, "jamais", sum(1 for r in g if r["n_sigs"] == 0))
