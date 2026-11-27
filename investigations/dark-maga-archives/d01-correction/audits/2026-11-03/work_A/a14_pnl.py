#!/usr/bin/env python3
"""Auditeur A. Coût moyen écrit depuis la description du rapport, sans importer dmaga/pnl.py. Deux passes sur trades.parquet : telle quelle (doit retomber sur wallets.parquet)
et sans les lignes en double. Sortie : out/a14_pnl_diff.csv (wallets dont le réalisé change), out/a14_pnl.txt. Mémoire : 72 000 wallets, une liste de 8 nombres chacun."""
import csv, io, zipfile, sys
from pathlib import Path
import numpy as np, duckdb
A = "/Volumes/VERBATIM HD/Dark-MAGA-Investigation/audits_work/A"
B = "/Volumes/VERBATIM HD/Dark-MAGA-Investigation/data"
RAW = Path("/Volumes/VERBATIM HD/Dark-MAGA-Investigation/raw/solusd")
OUT = "REDACTED_HOME/Projects/Dark-MAGA-Investigation/audits/2026-11-03/work_A/out"
EXCL = {"5Q544fKrFoe6tsEbD7S8EmxGTJYAKtTVhAW5Q5pge4j1", "87g44hEXP7R8ZxoAJtz941tsVftpEXC1LqAFTf2ZHtkH", "39azUYFWPz3VHgKCf3VChUwbpURdCHRxjWVowf5jUJjg", "PNLCQcVCD26aC7ZWgRyr5ptfaR7bBrWdTFgRWwu2tvF"}
sys.path.insert(0, "REDACTED_HOME/Projects/Dark-MAGA-Investigation")
from dmaga.venues import load as lv
EXCL |= set(lv())
M0 = 1717200000 // 60
px = np.full(1400000, np.nan, dtype=np.float32)
for z in sorted(RAW.glob("SOLUSDT-1m-*.zip")):
    if z.name.startswith("._"):
        continue
    with zipfile.ZipFile(z) as f, f.open(f.namelist()[0]) as fh:
        for row in csv.reader(io.TextIOWrapper(fh)):
            if row and row[0].isdigit():
                ms = int(row[0])
                ms = ms // 1000 if ms > 10**14 else ms
                i = ms // 60000 - M0
                if 0 <= i < len(px):
                    px[i] = float(row[4])
print("minutes de prix", int(np.isfinite(px).sum()), flush=True)
con = duckdb.connect(":memory:", config={"memory_limit": "400MB", "threads": 2, "temp_directory": A + "/duck14", "preserve_insertion_order": True})
con.execute("SET TimeZone='UTC'")
con.execute(f"""CREATE TEMP TABLE x AS SELECT e.signature, e.slot, e.block_time, e.src, e.dst, CAST(round(e.qty*1e6) AS BIGINT) q
                FROM read_parquet('{B}/token_edges.parquet') e WHERE e.how='gtba' AND e.dst <> '(multiple)' AND NOT EXISTS
                (SELECT 1 FROM read_parquet('{B}/trades.parquet') t WHERE t.signature=e.signature AND (t.owner=e.src OR t.owner=e.dst))""")
print("transferts gtba ajoutés", con.execute("SELECT count(*) FROM x").fetchone(), flush=True)
EXTRA = """UNION ALL SELECT src, 'transfer', -q, 0, block_time, signature, slot, 2147483647, NULL, 0 FROM x UNION ALL SELECT dst, 'transfer', q, 0, block_time, signature, slot, 2147483647, NULL, 0 FROM x"""
BASE = f"read_parquet('{B}/trades.parquet')"
KINDS = "('swap','transfer','lp_add','lp_remove','fee_share','swap_other')"
Q = {"tel": f"SELECT owner, kind, token_delta, sol_lamports, block_time, signature, slot, tx_index, venue, usdc_raw FROM {BASE} WHERE kind IN {KINDS} AND owner IS NOT NULL {EXTRA} ORDER BY slot, tx_index",
     "dedup": f"SELECT owner, kind, token_delta, sol_lamports, block_time, signature, slot, tx_index, venue, usdc_raw FROM (SELECT DISTINCT owner, kind, token_delta, sol_lamports, block_time, signature, slot, tx_index, venue, usdc_raw FROM {BASE} WHERE kind IN {KINDS} AND owner IS NOT NULL) {EXTRA} ORDER BY slot, tx_index"}
RES = {}
for name, sql in Q.items():
    W = {}
    cur = con.execute(sql)
    n = 0
    while True:
        rows = cur.fetchmany(50000)
        if not rows:
            break
        for owner, kind, td, sol, t, sig, slot, idx, venue, usdc in rows:
            n += 1
            if owner in EXCL:
                continue
            p = float(px[t // 60 - M0])
            if usdc and p == p:
                sol += int(usdc / 1e6 / p * 1e9)
            # qty, cost, realized, bought_sol, sold_sol, usd_cost, usd_proc, first_buy
            w = W.get(owner)
            if w is None:
                w = W[owner] = [0, 0.0, 0.0, 0, 0, 0.0, 0.0, None]
            if kind == "swap":
                if td > 0:
                    c = -sol
                    w[0] += td
                    w[1] += c
                    w[3] += c
                    if p == p:
                        w[5] += c / 1e9 * p
                    if w[7] is None:
                        w[7] = t
                else:
                    q = -td
                    k = min(q, max(w[0], 0))
                    basis = w[1] / w[0] * k if w[0] > 0 else 0.0
                    w[2] += sol - basis
                    w[1] -= basis
                    w[0] -= k
                    w[4] += sol
                    if p == p:
                        w[6] += sol / 1e9 * p
            elif td < 0:
                q = -td
                k = min(q, max(w[0], 0))
                if w[0] > 0:
                    w[1] -= w[1] / w[0] * k
                w[0] -= k
            else:
                w[0] += td
    RES[name] = W
    print(name, "lignes", n, "wallets", len(W), flush=True)
wp = {r[0]: r[1:] for r in con.execute(f"SELECT owner, realized_sol, bought_sol, sold_sol, cost_usd, proceeds_usd, first_buy_time FROM read_parquet('{B}/wallets.parquet')").fetchall()}
out = open(OUT + "/a14_pnl.txt", "w")
print("wallets.parquet", len(wp), "propre", len(RES["tel"]), file=out)
bad = 0
ex = []
for o, v in wp.items():
    w = RES["tel"].get(o)
    if w is None:
        bad += 1
        ex.append(("absent", o))
        continue
    if abs(w[2] / 1e9 - v[0]) > 1e-3 or abs(w[3] / 1e9 - v[1]) > 1e-3 or abs(w[4] / 1e9 - v[2]) > 1e-3:
        bad += 1
        ex.append((o, w[2] / 1e9, v[0], w[3] / 1e9, v[1], w[4] / 1e9, v[2]))
print("écarts passe telle quelle contre wallets.parquet", bad, ex[:8], file=out)
T, D = RES["tel"], RES["dedup"]
diff = []
for o, w in T.items():
    d = D.get(o) or [0, 0.0, 0.0, 0, 0, 0.0, 0.0, None]
    if abs(w[2] - d[2]) > 1e6 or abs(w[3] - d[3]) > 1e6 or abs(w[4] - d[4]) > 1e6:
        diff.append((o, w[2] / 1e9, d[2] / 1e9, w[3] / 1e9, d[3] / 1e9, w[4] / 1e9, d[4] / 1e9))
diff.sort(key=lambda x: -abs(x[1] - x[2]))
cw = csv.writer(open(OUT + "/a14_pnl_diff.csv", "w", newline=""))
cw.writerow(["owner", "realise_tel", "realise_dedup", "achete_tel", "achete_dedup", "vendu_tel", "vendu_dedup"])
cw.writerows(diff)
print("wallets touchés par les doublons", len(diff), "somme |écart réalisé|", round(sum(abs(x[1] - x[2]) for x in diff), 2), "SOL ; acheté en trop", round(sum(x[3] - x[4] for x in diff), 2), "vendu en trop", round(sum(x[5] - x[6] for x in diff), 2), file=out)
print("top écarts", diff[:15], file=out)
NAMED = {"H3QsBr": "H3QsBrrivimFJmSpTXuvig2n1Bh7JuYxrriRSEszT6cc", "GXZvX": "GXZvXsD6hxaLeFvQisWpdAwsayJxga7w9EeafhFZG2Ra", "9PrmF8": "9PrmF8sfoD2YShtWUghrGEYgxwabpnzog8gT1V6LEtdq", "5QhJJc": "5QhJJcFZu2ashyKyWSTGHcsyo6ZBCbpVuJqeutvQHScd"}
for k, o in NAMED.items():
    print(k, "tel", [round(x, 3) if isinstance(x, float) else x for x in T[o]], "dedup", [round(x, 3) if isinstance(x, float) else x for x in D[o]], "wallets.parquet", wp[o], "P&L USD dedup", round(D[o][6] - D[o][5]), file=out)
HIGH = 1721590213
for name, W in RES.items():
    entr = [o for o, w in W.items() if w[7] is not None and w[7] > HIGH]
    print(name, "entrés après Musk", len(entr), "réalisé > 0", sum(1 for o in entr if W[o][2] > 0), file=out)
# seuil de 0,5 lamport : un réalisé positif de poussière n'est pas un gain
for thr in (0, 1e6, 1e7, 1e8, 1e9):
    entr = [o for o, w in D.items() if w[7] is not None and w[7] > HIGH]
    print("  dedup, réalisé >", thr / 1e9, "SOL :", sum(1 for o in entr if D[o][2] > thr), file=out)
out.close()
print("fini")
