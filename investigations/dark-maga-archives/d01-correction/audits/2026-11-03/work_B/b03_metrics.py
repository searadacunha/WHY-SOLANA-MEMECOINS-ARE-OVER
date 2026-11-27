"""Auditeur B, aveugle : M1 à M7 et filtres depuis les parquets de b02_parse, un token à la fois.
Sorties : b03_main.csv (S20, plan principal), b03_r1.csv (S10), b03_r3.csv (S20−1 h).
Choix sur ambiguïtés : voir AMBIGUITES_PLAN.md dans ce dossier.
"""
import csv, gc, io, json, os, sys, zipfile
from pathlib import Path
import numpy as np
import pyarrow as pa
import pyarrow.parquet as pq
pa.set_memory_pool(pa.system_memory_pool())  # rend la mémoire au système entre deux tokens
EXT = Path("/Volumes/VERBATIM HD/Dark-MAGA-Investigation")
HERE = Path(__file__).parent
TOK = EXT / "audits_work/B/tok"
H = 3600
LAM = 1e9
METRICS = ["M1", "M2", "M3", "M4", "M5", "M6", "M7", "M7b", "M3b", "M6b"]


def bought(t, sol, side, a, b):
    m = (side == 1) & (t >= a) & (t < b)
    return float(sol[m].sum())


def win_median(t, sol, side, start, end, width):
    """Médiane du SOL acheté par fenêtres contiguës de `width` secondes sur [start, end). Les fenêtres vides valent 0."""
    edges = np.arange(start, end + 1, width)
    assert edges[-1] == end
    m = (side == 1) & (t >= start) & (t < end)
    v, _ = np.histogram(t[m], bins=edges, weights=sol[m])
    return float(np.median(v))


def metrics(S, created, slot, idx, t, side, w, sol, tok, res_key, res_pre):
    """S en secondes. Lignes triées (slot, idx). sol en SOL. Rend dict des mesures, sans donnée >= S."""
    keep = t < S
    slot, idx, t, side, w, sol, tok = slot[keep], idx[keep], t[keep], side[keep], w[keep], sol[keep], tok[keep]
    out = {k: float("nan") for k in METRICS}
    a24 = S - 24 * H
    # M1, M2 : toujours définies (plancher sur le dénominateur)
    out["M1"] = bought(t, sol, side, S - 3 * H, S) / max(0.1, win_median(t, sol, side, S - 75 * H, S - 3 * H, 3 * H))
    out["M2"] = bought(t, sol, side, a24, S) / max(0.1, win_median(t, sol, side, S - 96 * H, a24, 24 * H))
    win = (side == 1) & (t >= a24)
    tot = float(sol[win].sum())
    out["sol_24h"] = tot
    n_buyers = 0
    if win.any() and tot > 0:
        ww, ss, sl = w[win], sol[win], slot[win]
        uw, first = np.unique(ww, return_index=True)
        n_buyers = len(uw)
        # M3 : wallets dont le premier swap (achat ou vente) tombe dans la fenêtre
        uall, firstall = np.unique(w, return_index=True)
        new = t[firstall][np.searchsorted(uall, uw)] >= a24
        by = np.bincount(np.searchsorted(uw, ww), weights=ss, minlength=len(uw))
        out["M3"] = float(by[new].sum() / tot)
        # M3b, variante : seul le premier achat d'un nouveau wallet compte
        out["M3b"] = float(ss[first][new].sum() / tot)
        # M4
        out["M4"] = float(np.sort(by)[::-1][:5].sum() / tot)
        # M5
        if n_buyers >= 2:
            _, c = np.unique(sl[first], return_counts=True)
            pairs = float((c * (c - 1) / 2).sum())
            exp = n_buyers * (n_buyers - 1) / 2 / 216000.0
            out["M5"] = pairs / exp
            out["M5_pairs"] = pairs
        # M7 : le plus gros achat (en SOL), rapporté à la réserve juste avant ; M7b : plus grand ratio
        keys = slot[win] * 100000 + idx[win]
        pos = np.searchsorted(res_key, keys)
        assert (res_key[pos] == keys).all()
        resv = res_pre[pos] / LAM
        k = int(np.argmax(ss))
        out["M7"] = float(ss[k] / resv[k]) if resv[k] > 0 else float("nan")
        with np.errstate(divide="ignore", invalid="ignore"):
            r = ss / resv
        out["M7b"] = float(np.nanmax(r[resv > 0])) if (resv > 0).any() else float("nan")
    out["n_buyers_24h"] = n_buyers
    # M6
    early = np.unique(w[(side == 1) & (t >= created) & (t < created + 24 * H)])
    out["n_early"] = len(early)
    if len(early):
        nw = int(w.max()) + 1
        b = np.bincount(w[side == 1], weights=tok[side == 1], minlength=nw)
        s = np.bincount(w[side == -1], weights=tok[side == -1], minlength=nw)
        be, se = b[early], s[early]
        if be.sum() > 0:
            out["M6"] = float(np.maximum(be - se, 0).sum() / be.sum())
            # M6b : moyenne non pondérée des parts par wallet
            out["M6b"] = float((np.maximum(be - se, 0) / be).mean())
    return out


def _test():
    # 2 acheteurs hors fenêtre, un wallet ancien et deux nouveaux dans la fenêtre
    S = 1000 * H
    created = S - 200 * H
    t = np.array([created + 10, created + 20, S - 80 * H, S - 2 * H, S - 2 * H, S - H, S - 1, S + 5], dtype=np.int64)
    side = np.array([1, 1, -1, 1, 1, 1, -1, 1], dtype=np.int8)
    w = np.array([0, 1, 1, 0, 2, 3, 2, 9], dtype=np.int32)
    slot = np.arange(100, 108, dtype=np.int64); slot[4] = slot[3]  # wallets 0 et 2 même slot
    idx = np.arange(8, dtype=np.int32)
    sol = np.array([5., 5., 1., 2., 4., 2., 1., 100.])
    tok = np.array([10., 10., 4., 2., 2., 1., 1., 100.])
    key = slot * 100000 + idx
    pre = np.full(8, 40 * LAM)
    o = metrics(S, created, slot, idx, t, side, w, sol, tok, key, pre)
    assert abs(o["M3"] - 6 / 8) < 1e-12, o           # wallets 2, 3 nouveaux, wallet 0 ancien
    assert abs(o["M4"] - 1.0) < 1e-12
    assert abs(o["M7"] - 4 / 40) < 1e-12
    assert abs(o["M2"] - 8 / 0.1) < 1e-9            # médiane de 3 fenêtres : 0
    assert abs(o["M1"] - 8 / 0.1) < 1e-9
    assert abs(o["M5"] - 1 / (3 / 216000)) < 1e-6   # 3 acheteurs, 1 paire même slot
    # M6 : précoces 0 et 1. wallet 0 achète 10+2 et ne vend pas ; wallet 1 achète 10, vend 4 : (12+6)/22
    assert abs(o["M6"] - 18 / 22) < 1e-12, o
_test()


def load_solusd():
    """Close à la minute, tableau numpy mis en cache (un processus par token)."""
    cache = EXT / "audits_work/B/solusd_close.npz"
    if cache.exists():
        z = np.load(cache)
        return z["m0"].item(), z["v"]
    arr = {}
    for ym in ["2024-06", "2024-07", "2024-08", "2024-09", "2024-10", "2024-11"]:
        p = EXT / f"raw/solusd/SOLUSDT-1m-{ym}.zip"
        with zipfile.ZipFile(p) as z:
            name = [n for n in z.namelist() if n.endswith(".csv")][0]
            with z.open(name) as f:
                for line in io.TextIOWrapper(f):
                    a = line.split(",")
                    if not a[0].isdigit():
                        continue
                    ms = int(a[0])
                    arr[ms // 60000] = float(a[4])  # close
    m0 = min(arr); v = np.full(max(arr) - m0 + 1, np.nan)
    for k, x in arr.items():
        v[k - m0] = x
    np.savez(cache, m0=m0, v=v)
    return m0, v


def main():
    peak = {}
    with open(HERE / "b01_peak.csv") as f:
        for r in csv.DictReader(f):
            if int(r["hist_hours"]) > 0:
                peak[r["pool"]] = r
    stats = {}
    with open(HERE / "b02_stats.jsonl") as f:
        for line in f:
            s = json.loads(line)
            stats[s["pool"]] = s
    m0, sol_v = load_solusd()
    print("minutes SOL/USD présentes", int(np.isfinite(sol_v).sum()), "sur", len(sol_v), flush=True)
    only = set(sys.argv[1:])
    hdr = ["pool", "mint", "created", "S", "cap_S1h", "swap_before_S1_age_s", "swap_rank_in_last_res", "rows_96h", "chain_breaks", "chain_breaks_tok", "cursor_complete", "tx_lines", "rows_total", "decimals", "solusd_ok", "n_before_S", "last_res_time"] + METRICS + ["sol_24h", "n_buyers_24h", "n_early", "M5_pairs"]
    # reprise : un token dont les lignes existent déjà est sauté (écriture token par token, vidée à chaque fois)
    seen = set()
    new_file = not (HERE / "b03_main.csv").exists() or (HERE / "b03_main.csv").stat().st_size == 0
    if not new_file:
        for k in ["main", "r1", "r3"]:
            with open(HERE / f"b03_{k}.csv") as f:
                rd = csv.DictReader(f)
                assert rd.fieldnames == hdr, "en-tête ancien : supprimer les b03_*.csv"
                seen |= {r["pool"] for r in rd}
    files = {k: open(HERE / f"b03_{k}.csv", "a", newline="") for k in ["main", "r1", "r3"]}
    wr = {k: csv.DictWriter(v, fieldnames=hdr, restval="") for k, v in files.items()}
    if new_file:
        for v in wr.values():
            v.writeheader()
    for pool, st in stats.items():
        if (only and pool not in only) or pool in seen:
            continue
        pk = peak[pool]
        rows = pq.read_table(TOK / f"{pool}.parquet", use_threads=False)
        res = pq.read_table(TOK / f"{pool}.res.parquet", use_threads=False)
        order = np.lexsort((rows["idx"].to_numpy(), rows["slot"].to_numpy()))
        slot, idx, t, side, w = [rows[c].to_numpy()[order] for c in ("slot", "idx", "time", "side", "w")]
        sol = rows["sol"].to_numpy()[order] / LAM
        decs = [int(k) for k in st["decimals"] if int(k) >= 0]
        assert len(decs) == 1, (pool, st["decimals"])
        tok = rows["tok"].to_numpy()[order] / 10 ** decs[0]
        rk = res["slot"].to_numpy() * 100000 + res["idx"].to_numpy()
        rt, rpre, rpost, rpt, rpot = [res[c].to_numpy() for c in ("time", "pre_s", "post_s", "pre_t", "post_t")]
        assert (np.diff(rk) > 0).all()
        del rows, res, order
        created = st["created"]
        variants = {}
        if pk["S20"]:
            s20 = int(float(pk["S20"])) * H
            variants["main"] = s20
            variants["r3"] = s20 - H
        if pk["S10"]:
            variants["r1"] = int(float(pk["S10"])) * H
        for name, S in variants.items():
            row = {"pool": pool, "mint": st["mint"], "created": created, "S": S, "chain_breaks": st["chain_breaks"], "chain_breaks_tok": st["chain_breaks_tok"],
                   "cursor_complete": st["cursor_complete"], "tx_lines": st["lines"], "rows_total": st["rows"], "decimals": decs[0]}
            row["rows_96h"] = int(((t >= S - 96 * H) & (t < S)).sum())
            row["n_before_S"] = int((t < S).sum())
            row["last_res_time"] = int(rt[-1])
            # capitalisation : dernier swap avant S−1 h
            S1 = S - H
            dS = rpost - rpre; dT = rpot - rpt
            sw = np.nonzero((np.sign(dS) * np.sign(dT) < 0) & (rt < S1))[0]
            if len(sw):
                j = int(sw[-1])
                n_before = int((rt < S1).sum())
                row["swap_rank_in_last_res"] = n_before - j
                row["swap_before_S1_age_s"] = S1 - int(rt[j])
                px = (rpost[j] / LAM) / (rpot[j] / 10 ** decs[0])
                m = S1 // 60
                usd = float(sol_v[m - m0]) if 0 <= m - m0 < len(sol_v) and np.isfinite(sol_v[m - m0]) else None
                row["solusd_ok"] = int(usd is not None)
                row["cap_S1h"] = px * 1e9 * usd if usd else ""
            row.update(metrics(S, created, slot, idx, t, side, w, sol, tok, rk, rpre))
            wr[name].writerow(row)
        for v in files.values():
            v.flush()
        del slot, idx, t, side, w, sol, tok, rk, rt, rpre, rpost, rpt, rpot
        gc.collect()
    print("fini", flush=True)


if __name__ == "__main__":
    main()
