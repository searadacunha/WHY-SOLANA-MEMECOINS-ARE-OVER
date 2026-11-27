#!/usr/bin/env python3
"""Auditeur A. M1 à M7 écrits depuis le texte du plan, sans importer metrics.py, sur les lignes du parseur propre (a03_lines).
Compare à derived/metrics.csv et à swaps/<pool>.parquet. Variantes de sensibilité de données : A vault entier, B sans lignes dont la quantité diffère du vault,
C pic sur réussies. Traitement pool par pool. Sortie : out/a04_metrics.csv, out/a04_compare.txt."""
import csv, json, statistics, sys
import numpy as np, duckdb
import pyarrow.parquet as pq
A = "/Volumes/VERBATIM HD/Dark-MAGA-Investigation/audits_work/A"
C = "/Volumes/VERBATIM HD/Dark-MAGA-Investigation/data/controls"
ROOT = "REDACTED_HOME/Projects/Dark-MAGA-Investigation"
OUT = ROOT + "/audits/2026-11-03/work_A/out"
DP = "CRSwXnfF21yHDXdYBVWwCwQ5Ni2A4QuK3qGYis5k7x7k"
H = 3600
con = duckdb.connect(":memory:", config={"memory_limit": "400MB", "threads": 1, "temp_directory": A + "/duck04"})
FLOOR = 1e8


def own(t, slot, owner, qty, sol, vp, S, created):
    m = t < S
    t, slot, owner, qty, sol, vp = t[m], slot[m], owner[m], qty[m], sol[m], vp[m]
    buy = (qty > 0) & (sol < 0)
    amt = np.where(buy, -sol.astype(float), 0.0)
    def med(width, lo, hi):
        v = []
        e = hi
        while e - width >= lo:
            v.append(amt[(t >= e - width) & (t < e)].sum())
            e -= width
        return float(np.median(v)) if v else 0.0
    w3 = amt[t >= S - 3 * H].sum()
    w24m = t >= S - 24 * H
    w24 = amt[w24m].sum()
    M1 = w3 / max(med(3 * H, S - 75 * H, S - 3 * H), FLOOR)
    M2 = w24 / max(med(24 * H, S - 96 * H, S - 24 * H), FLOOR)
    ix = np.where(w24m & buy)[0]
    if len(ix) == 0:
        return dict(M1=M1, M2=M2, M3=float("nan"), M4=float("nan"), M5=float("nan"), M6=float("nan"), M7=float("nan"), n96=int((t >= S - 96 * H).sum()), nb=0)
    # premier swap de chaque wallet, tous sens
    uo, first_idx = np.unique(owner, return_index=True)
    first_t = dict(zip(uo.tolist(), t[first_idx].tolist()))
    M3 = sum(amt[i] for i in ix.tolist() if first_t[owner[i]] >= S - 24 * H) / w24 if w24 > 0 else float("nan")
    per = {}
    fs = {}
    for i in ix.tolist():
        o = owner[i]
        per[o] = per.get(o, 0.0) + amt[i]
        fs.setdefault(o, int(slot[i]))
    M4 = sum(sorted(per.values())[-5:]) / w24
    nb = len(per)
    cnt = {}
    for s in fs.values():
        cnt[s] = cnt.get(s, 0) + 1
    M5 = (sum(c * (c - 1) / 2 for c in cnt.values()) / (nb * (nb - 1) / 2 / 216000)) if nb >= 2 else float("nan")
    early = set(owner[(t < created + 24 * H) & buy].tolist())
    b, n = {}, {}
    for o, q in zip(owner.tolist(), qty.tolist()):
        if o in early:
            n[o] = n.get(o, 0) + q
            if q > 0:
                b[o] = b.get(o, 0) + q
    tot = sum(b.values())
    M6 = sum(max(0, min(n[o], b[o])) for o in b) / tot if tot else float("nan")
    j = ix[np.argmax(amt[ix])]
    M7 = amt[j] / max(float(vp[j]), 1.0)
    return dict(M1=M1, M2=M2, M3=M3, M4=M4, M5=M5, M6=M6, M7=M7, n96=int((t >= S - 96 * H).sum()), nb=nb)


rows = [r for r in csv.DictReader(open(ROOT + "/etude_final/derived/metrics.csv"))]
pools_stats = {}
for line in open(A + "/a03_pools.jsonl"):
    v = json.loads(line)
    pools_stats[v["pool"]] = v
act = {}
for line in open(C + "/activity.jsonl"):
    a = json.loads(line)
    if a["pool"] in pools_stats:
        act[a["pool"]] = {int(k): int(v) for k, v in a["hist"]}
pools = sorted({r["pool"] for r in rows if r["pool"] in pools_stats})
fout = open(OUT + "/a04_compare.txt", "w")
print("pools couverts", len(pools), "lignes metrics", len(rows), file=fout)
w = csv.writer(open(OUT + "/a04_metrics.csv", "w", newline=""))
Ms = ["M1", "M2", "M3", "M4", "M5", "M6", "M7"]
w.writerow(["pool", "variant", "S", *Ms, "n96", "nb"])
ncmp, nbad, ex = 0, 0, []
par_pool = []
for pool in pools:
    r0 = [r for r in rows if r["pool"] == pool]
    created = int(r0[0]["created"])
    tb = con.execute(f"SELECT t, slot, tx_index, owner, qty, sol, vault_pre FROM read_parquet('{A}/a03_lines.parquet') WHERE pool=? ORDER BY slot, tx_index", [pool]).to_arrow_table()
    d = {c: tb[c].to_numpy() for c in tb.column_names}
    t, sl, ow, q, so, vp = d["t"].astype(np.int64), d["slot"].astype(np.int64), d["owner"], d["qty"].astype(np.int64), d["sol"].astype(np.int64), d["vault_pre"].astype(np.int64)
    # comparaison ligne à ligne au parquet du projet
    sw = pq.read_table(f"{C}/swaps/{pool}.parquet", columns=["t", "slot", "tx_index", "owner", "qty", "sol", "vault_pre"])
    same_n = sw.num_rows == len(t)
    if same_n:
        k1 = sorted(zip(sl.tolist(), d["tx_index"].tolist(), ow.tolist(), q.tolist(), so.tolist(), vp.tolist()))
        k2 = sorted(zip(sw["slot"].to_pylist(), sw["tx_index"].to_pylist(), sw["owner"].to_pylist(), sw["qty"].to_pylist(), sw["sol"].to_pylist(), sw["vault_pre"].to_pylist()))
        same = k1 == k2
    else:
        same = False
    par_pool.append((pool, len(t), sw.num_rows, same))
    for r in r0:
        S = int(r["S"])
        m = own(t, sl, ow, q, so, vp, S, created)
        w.writerow([pool, r["variant"], S, *[m[k] for k in Ms], m["n96"], m["nb"]])
        for k in Ms:
            a, b = m[k], float(r[k]) if r[k] not in ("", None) else float("nan")
            ncmp += 1
            if not ((a != a and b != b) or abs(a - b) <= 1e-9 * max(abs(a), abs(b), 1)):
                nbad += 1
                if len(ex) < 12:
                    ex.append((pool, r["variant"], k, a, b))
print("comparaisons", ncmp, "écarts", nbad, ex, file=fout)
print("parquet identique ligne à ligne", sum(1 for x in par_pool if x[3]), "/", len(par_pool), "écarts", [x for x in par_pool if not x[3]][:12], file=fout)
fout.flush()
# état des pools
bad = {k: [p for p, v in pools_stats.items() if v.get(k)] for k in ("nonmono", "ruptures_token", "ruptures_sol", "err", "sans_tx_index", "keys_ne_balances", "un_seul_vault")}
print("anomalies par pool", {k: len(v) for k, v in bad.items()}, file=fout)
print("ruptures vault jeton", sorted(((pools_stats[p]["ruptures_token"], p) for p in bad["ruptures_token"]), reverse=True)[:12], file=fout)
print("un seul vault", sorted(((pools_stats[p]["un_seul_vault"], p) for p in bad["un_seul_vault"]), reverse=True)[:6], file=fout)
print("incomplets", [p for p, v in pools_stats.items() if not v["complete"]], "n curseur != lu", [p for p, v in pools_stats.items() if v["tx"] != v["cursor_n"]], file=fout)
sel = {}
for x in open(C + "/selection.jsonl"):
    a = json.loads(x)
    if a["pool"] in pools_stats:
        sel[a["pool"]] = a
bad_f = []
for p, v in pools_stats.items():
    f = v["filters"]["blockTime"]
    end = max(x for x in (sel[p]["S20"], sel[p]["S10"]) if x) + H
    if p == DP:
        end = max(end, 1721589801)
    if f["gte"] != v["created"] or f["lt"] != end or v["filters"].get("status") != "succeeded":
        bad_f.append((p, f, end))
print("filtres de collecte non conformes", bad_f[:5], file=fout)
print("premier pre vault SOL non nul", [(p, v["first_pre_sol"]) for p, v in pools_stats.items() if v["first_pre_sol"]][:8], file=fout)
print("tmin avant created, tmax après fin", [p for p, v in pools_stats.items() if v["tmin"] is not None and v["tmin"] < v["created"]], file=fout)
# part des pics faite d'échecs
prim = [r for r in rows if r["variant"] == "primary"]
share = []
for r in prim:
    p, S = r["pool"], int(r["S"])
    if p not in pools_stats:
        continue
    ok = dict((int(a), int(b)) for a, b in pools_stats[p]["hist_ok"])
    n = act[p].get(S // H, 0)
    k = ok.get(S // H, 0)
    # S recalculé sur réussies, dans la partie collectée seulement
    cr = int(r["created"])
    lo = (cr + 96 * H + H - 1) // H
    Sok = None
    last = max(ok) if ok else lo
    for h in range(lo, last + 1):
        x = ok.get(h, 0)
        if x >= 500 and x >= 20 * max(statistics.median([ok.get(y, 0) for y in range(h - 72, h)]), 5):
            Sok = h * H
            break
    share.append((p, S, n, k, Sok))
w2 = csv.writer(open(OUT + "/a04_spike_success.csv", "w", newline=""))
w2.writerow(["pool", "S", "signatures_S", "reussies_S", "S_sur_reussies_dans_partie_collectee"])
w2.writerows(share)
n_lt = sum(1 for x in share if x[3] < 500)
fr = sorted(1 - x[3] / max(x[2], 1) for x in share)
print("pics primaires : réussies à l'heure S sous 500 :", n_lt, "/", len(share), "part d'échec à S médiane", round(fr[len(fr) // 2], 3), "p10", round(fr[len(fr) // 10], 3), "p90", round(fr[int(len(fr) * .9)], 3), file=fout)
print("DMAGA", [x for x in share if x[0] == DP], file=fout)
print("Sok différent de S", sum(1 for x in share if x[4] != x[1]), "Sok absent (au-delà de la collecte ou sans pic)", sum(1 for x in share if x[4] is None), file=fout)
fout.close()
print("fini")
