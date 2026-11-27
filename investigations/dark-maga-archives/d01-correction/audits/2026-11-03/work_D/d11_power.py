#!/usr/bin/env python3
"""Auditeur D. Puissance indépendante de B : chaque token du principal devient cible à son tour contre les 211 autres, accumulation injectée.
Écrit sans lire b13_power.py. Base : d10_features.csv (mesures identiques à metrics.csv à 3e-16) plus le plus gros achat de 24 h. Impact de prix ignoré, comme toute simulation courte.
Sorties : d11_power.txt, d11_scenarios.csv, d11_factors.csv."""
import csv, math, os, random, statistics as st, sys
import duckdb
ROOT = "audits/2026-11-03/work_D/"
SW = "/Volumes/VERBATIM HD/Dark-MAGA-Investigation/data/controls/swaps/"
con = duckdb.connect(":memory:", config={"memory_limit": "300MB", "threads": 1})
F = list(csv.DictReader(open(ROOT + "d10_features.csv")))
assert len(F) == 212
sys.stdout = open(ROOT + "d11_power.txt", "w")
M = ["M1", "M2", "M3", "M4", "M5", "M6", "M7"]
T = []
for r in F:
    S = int(r["S"])
    mx = con.execute(f"SELECT coalesce(max(-sol),0)/1e9 FROM read_parquet('{SW}{r['pool']}.parquet') WHERE qty>0 AND t>={S-86400} AND t<{S}").fetchone()[0]
    T.append(dict(p=r["pool"], d=r["is_dmaga"] == "True", A3=float(r["A3"]), B3=float(r["B3"]), A24=float(r["A24"]), B24=float(r["B24"]), new24=float(r["new24"]),
                  n=int(r["n24"]), pairs=float(r["pairs"]), R=float(r["reserve_S3"]), top=[float(x) for x in r["top5"].split("|")] if r["top5"] else [],
                  mx=mx, **{m: float(r[m]) for m in M}))
i_d = next(i for i, t in enumerate(T) if t["d"])
print("réserve DMAGA à S-3 h", T[i_d]["R"], "A3", T[i_d]["A3"], "plus gros achat 24 h", T[i_d]["mx"], "reserves nulles", sum(1 for t in T if not t["R"] or math.isnan(t["R"])))
def holm(ps):
    o = sorted(ps.values()); m = len(o)
    return sum(1 for _ in iter(lambda: None, None)) if False else _holm(o)
def _holm(o):
    n = 0
    for i, p in enumerate(o):
        if p <= 0.05 / (len(o) - i): n += 1
        else: break
    return n
PEERS = {m: sorted(t[m] for t in T) for m in M}
import bisect
def ranks(i, vals):
    """p de rang de la cible i, valeurs vals, contre les 211 autres non modifiées"""
    out = {}
    for m in M:
        c = len(T) - bisect.bisect_left(PEERS[m], vals[m])  # valeurs >= vals[m], la cible comprise si sa valeur d'origine est >=
        if T[i][m] >= vals[m]: c -= 1
        out[m] = (1 + c) / 212
    return out
def inject(t, xs, slots=0, win=3):
    """xs : montants SOL par wallet neuf ; slots : nb de wallets réunis dans un même slot"""
    X = sum(xs); w = len(xs)
    v = {m: t[m] for m in M}
    a3 = t["A3"] + X if win == 3 else t["A3"]
    a24 = t["A24"] + X
    v["M1"] = a3 / max(t["B3"], 0.1); v["M2"] = a24 / max(t["B24"], 0.1)
    v["M3"] = (t["new24"] + X) / a24 if a24 else float("nan")
    top = sorted(t["top"] + list(xs), reverse=True)[:5]
    v["M4"] = sum(top) / a24
    n = t["n"] + w
    v["M5"] = (t["pairs"] + slots * (slots - 1) / 2) / (n * (n - 1) / 2 / 216000)
    big = max(xs)
    if big > t["mx"] and t["R"] > 0: v["M7"] = big / t["R"]
    return v
rng = random.Random(20261103)
SC = [("nul", lambda t: ([], 0, 3)),
      ("0,25 R, 1 wallet, 3 h", lambda t: ([0.25 * t["R"]], 0, 3)),
      ("1 R, 1 wallet, 3 h", lambda t: ([t["R"]], 0, 3)),
      ("2 R, 1 wallet, 3 h", lambda t: ([2 * t["R"]], 0, 3)),
      ("5 R, 1 wallet, 3 h", lambda t: ([5 * t["R"]], 0, 3)),
      ("2 R, 25 wallets, 3 h", lambda t: ([2 * t["R"] / 25] * 25, 0, 3)),
      ("2 R, 25 wallets, moitié dans un slot", lambda t: ([2 * t["R"] / 25] * 25, 12, 3)),
      ("2 R, 5 wallets, 24 h", lambda t: ([2 * t["R"] / 5] * 5, 0, 24)),
      ("moyen du contrôle (6 wallets, 6 x lognormale, moitié slot)", lambda t: ([math.exp(rng.gauss(.5, .4)) * 6 for _ in range(6)], 3, 3)),
      ("fort du contrôle (18 wallets, 25 x lognormale, moitié slot)", lambda t: ([math.exp(rng.gauss(.5, .4)) * 25 for _ in range(18)], 9, 3))]
w = csv.writer(open(ROOT + "d11_scenarios.csv", "w", newline="")); w.writerow("scenario detection_pct n_detectes p_min_median dmaga_passe dmaga_p_min dmaga_mesures".split())
print("scénario | détection | p min médian | DMAGA")
for name, fn in SC:
    reps = 20 if "contrôle" in name else 1
    det = 0; pm = []; dm = None
    for _ in range(reps):
        for i, t in enumerate(T):
            xs, sl, win = fn(t)
            vals = inject(t, xs, sl, win) if xs else {m: t[m] for m in M}
            ps = ranks(i, vals); o = sorted(ps.values())
            nrej = _holm(o); pm.append(o[0])
            det += nrej > 0
            if i == i_d and dm is None:
                dm = (nrej > 0, round(o[0], 4), sorted(m for m in M if ps[m] <= 0.05 / 7))
    rate = det / (212 * reps)
    print(f"{name} | {100*rate:.1f} % ({det}/{212*reps}) | {st.median(pm):.3f} | {dm}")
    w.writerow([name, round(100 * rate, 2), det, round(st.median(pm), 4), dm[0], dm[1], ",".join(dm[2])])
# facteur par mesure : même forme que B 5.3, recalcul indépendant
def odds(p, f):
    if p >= 1: return 1.0
    o = p / (1 - p) * f
    return o / (1 + o)
w2 = csv.writer(open(ROOT + "d11_factors.csv", "w", newline="")); w2.writerow(["facteur"] + M + ["toutes"])
print("facteur :", M, "toutes")
for f in (2, 10, 100, 1000):
    row = [f]
    for mm in M + ["all"]:
        det = 0
        for i, t in enumerate(T):
            v = {m: t[m] for m in M}
            for m in (M if mm == "all" else [mm]):
                v[m] = odds(t[m], f) if m in ("M3", "M4", "M6") else t[m] * f
            det += _holm(sorted(ranks(i, v).values())) > 0
        row.append(round(100 * det / 212, 1))
    w2.writerow(row); print(row)
# puissance exacte d'une mesure : p <= 0,05/7 exige c = 0
for q in (.95, .975, .99, .995, .999):
    print("quantile vrai", q, "1 mesure", round(100 * q ** 211, 2), "7 mesures indép.", round(100 * (1 - (1 - q ** 211) ** 7), 2))
# seuils sur DMAGA
d = T[i_d]
for m in M:
    sp = sorted((t[m] for j, t in enumerate(T) if j != i_d), reverse=True)
    c = sum(1 for x in sp if x >= d[m])
    print(m, "DMAGA", round(d[m], 4), "c", c, "p", round((1 + c) / 212, 4), "rang", c + 1, "pct sous", round(100 * sum(1 for x in sp if x < d[m]) / 211, 1), "max pairs", round(sp[0], 3), "nb au max", sum(1 for x in sp if x == sp[0]), "p minimal si dépasse tout", round((1 + sum(1 for x in sp if x == 1.0)) / 212, 4) if m in ("M3", "M4") else round(1 / 212, 5))
# B-05 : au-dessus de la médiane, P75, nombre de pairs dominants
med = {m: st.median(t[m] for j, t in enumerate(T) if j != i_d) for m in M}
p75 = {m: sorted(t[m] for j, t in enumerate(T) if j != i_d)[int(.75 * 210)] for m in M}
print("au-dessus médiane", [m for m in M if d[m] > med[m]], "au-dessus P75", [m for m in M if d[m] > p75[m]])
dom = [sum(1 for m in M if t[m] >= d[m]) for j, t in enumerate(T) if j != i_d]
print("pairs >= DMAGA sur k mesures", {k: dom.count(k) for k in range(8)})
pct = lambda i: st.mean(sum(1 for j, u in enumerate(T) if j != i and u[m] < T[i][m]) / 211 for m in M)
pcts = [pct(i) for i in range(212)]
c = sum(1 for i in range(212) if i != i_d and pcts[i] >= pcts[i_d])
print("centile moyen DMAGA", round(pcts[i_d], 4), "pairs au-dessus", c, "p exploratoire", round((1 + c) / 212, 4))
# rapport de vraisemblance d'un résultat non significatif, scénario 2 R : P(non sig | H1) / P(non sig | H0)
