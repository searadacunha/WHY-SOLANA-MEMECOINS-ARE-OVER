"""Phase 2 : variables explicatives par token (dénominateurs, planchers, âge, réserve, capitalisation antérieure, sommes par fenêtre),
mesures à S−2 h, S−3 h, S−6 h (EXPLORATOIRE), liste des acheteurs de [S−24 h, S). Un processus par token, reprise par CSV.
Sorties : b12_features.jsonl, audits_work/B/buyers.csv."""
import csv, json, sys
from pathlib import Path
import numpy as np, pyarrow as pa, pyarrow.parquet as pq
sys.path.insert(0, str(Path(__file__).parent))
pa.set_memory_pool(pa.system_memory_pool())
from b03_metrics import metrics, load_solusd, TOK, HERE, H, LAM
OUT = HERE / "b12_features.jsonl"
BUY = Path("/Volumes/VERBATIM HD/Dark-MAGA-Investigation/audits_work/B/buyers.csv")


def cap_at(T, rt, rpre, rpost, rpt, rpot, dec, m0, sol_v):
    dS = rpost - rpre; dT = rpot - rpt
    sw = np.nonzero((np.sign(dS) * np.sign(dT) < 0) & (rt < T))[0]
    if not len(sw): return None
    j = int(sw[-1])
    m = T // 60 - m0
    usd = float(sol_v[m]) if 0 <= m < len(sol_v) and np.isfinite(sol_v[m]) else None
    if usd is None or rpot[j] <= 0: return None
    return (rpost[j] / LAM) / (rpot[j] / 10 ** dec) * 1e9 * usd


def main(pool):
    st = None
    for line in open(HERE / "b02_stats.jsonl"):
        s = json.loads(line)
        if s["pool"] == pool: st = s
    S = None
    for r in csv.DictReader(open(HERE / "b03_main.csv")):
        if r["pool"] == pool: S = int(r["S"])
    if S is None: return
    if OUT.exists():
        for line in open(OUT):
            if json.loads(line)["pool"] == pool: return
    rows = pq.read_table(TOK / f"{pool}.parquet", use_threads=False)
    res = pq.read_table(TOK / f"{pool}.res.parquet", use_threads=False)
    order = np.lexsort((rows["idx"].to_numpy(), rows["slot"].to_numpy()))
    slot, idx, t, side, w = [rows[c].to_numpy()[order] for c in ("slot", "idx", "time", "side", "w")]
    dec = [int(k) for k in st["decimals"] if int(k) >= 0][0]
    sol = rows["sol"].to_numpy()[order] / LAM; tok = rows["tok"].to_numpy()[order] / 10 ** dec
    rk = res["slot"].to_numpy() * 100000 + res["idx"].to_numpy()
    rt, rpre, rpost, rpt, rpot = [res[c].to_numpy() for c in ("time", "pre_s", "post_s", "pre_t", "post_t")]
    del rows, res, order
    m0, sol_v = load_solusd()
    created = st["created"]
    f = {"pool": pool, "S": S, "created": created, "age_jours": (S - created) / 86400}
    keep = t < S
    a24 = S - 24 * H
    buy = (side == 1) & keep
    # sommes par fenêtre de M1 (24 fenêtres) et de M2 (3 fenêtres)
    e1 = np.arange(S - 75 * H, S - 3 * H + 1, 3 * H); m1w = np.histogram(t[buy], bins=e1, weights=sol[buy])[0]
    e2 = np.arange(S - 96 * H, a24 + 1, 24 * H); m2w = np.histogram(t[buy], bins=e2, weights=sol[buy])[0]
    f["m1_windows"] = [round(float(x), 6) for x in m1w]; f["m2_windows"] = [round(float(x), 6) for x in m2w]
    f["num3"] = float(sol[buy & (t >= S - 3 * H)].sum()); f["num24"] = float(sol[buy & (t >= a24)].sum())
    f["num1h"] = float(sol[buy & (t >= S - H)].sum())
    f["sol_sell_24h"] = float(sol[(side == -1) & keep & (t >= a24)].sum())
    win = buy & (t >= a24)
    ww, ss, sl = w[win], sol[win], slot[win]
    if len(ww):
        uw, first = np.unique(ww, return_index=True)
        uall, firstall = np.unique(w[keep], return_index=True)
        new = t[keep][firstall][np.searchsorted(uall, uw)] >= a24
        by = np.bincount(np.searchsorted(uw, ww), weights=ss, minlength=len(uw))
        f["newsol"] = float(by[new].sum()); f["top5"] = [round(float(x), 6) for x in np.sort(by)[::-1][:5]]
        _, c = np.unique(sl[first], return_counts=True)
        f["pairs"] = float((c * (c - 1) / 2).sum()); f["n_buyers"] = int(len(uw)); f["n_new"] = int(new.sum())
        keys = sl * 100000 + idx[win]
        resv = rpre[np.searchsorted(rk, keys)] / LAM
        k = int(np.argmax(ss)); f["maxbuy"] = float(ss[k]); f["maxbuy_res"] = float(resv[k])
        wallets = (TOK / f"{pool}.wallets.txt").read_text().split("\n")
        with open(BUY, "a", newline="") as fo:
            wr = csv.writer(fo)
            for a, b in zip(uw.tolist(), by.tolist()):
                wr.writerow([pool, wallets[a], round(b, 6)])
        del wallets
    else:
        f.update(newsol=0.0, top5=[], pairs=0.0, n_buyers=0, n_new=0, maxbuy=0.0, maxbuy_res=0.0)
    # M6 : achetés et nets des précoces
    early = np.unique(w[buy & (t < created + 24 * H)])
    nw = int(w.max()) + 1 if len(w) else 1
    b = np.bincount(w[buy], weights=tok[buy], minlength=nw); se = (side == -1) & keep
    s = np.bincount(w[se], weights=tok[se], minlength=nw)
    f["early_bought"] = float(b[early].sum()); f["early_net"] = float(np.maximum(b[early] - s[early], 0).sum()); f["n_early"] = int(len(early))
    # réserves et capitalisations
    for name, T in (("S1h", S - H), ("S3h", S - 3 * H), ("S24h", a24), ("S96h", S - 96 * H)):
        j = np.nonzero(rt < T)[0]
        f[f"res_{name}"] = float(rpost[j[-1]] / LAM) if len(j) else None
        f[f"cap_{name}"] = cap_at(T, rt, rpre, rpost, rpt, rpot, dec, m0, sol_v)
    # mesures décalées, EXPLORATOIRE
    for dh in (2, 3, 6):
        mm = metrics(S - dh * H, created, slot, idx, t, side, w, sol, tok, rk, rpre)
        f[f"shift{dh}"] = {k: (None if isinstance(v, float) and v != v else v) for k, v in mm.items() if k in ("M1", "M2", "M3", "M4", "M5", "M6", "M7")}
    with open(OUT, "a") as fo:
        fo.write(json.dumps(f) + "\n")


if __name__ == "__main__":
    main(sys.argv[1])
