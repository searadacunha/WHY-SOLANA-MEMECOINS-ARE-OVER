"""Phase 2 : puissance sur la distribution réelle. Chaque token de la population est pris tour à tour comme cible contre les 211 autres.
Scénarios d'initié injectés (calcul incrémental depuis b12_features, vérifié sur l'effet nul), facteurs multiplicatifs, décalages de S,
rangs conditionnels (EXPLORATOIRE). Sorties : b13_power.txt, b13_scenarios.csv, b13_facteurs.csv."""
import json
from pathlib import Path
import numpy as np, pandas as pd
from scipy import stats
HERE = Path(__file__).parent; ROOT = HERE.parents[2]
DM = "CRSwXnfF21yHDXdYBVWwCwQ5Ni2A4QuK3qGYis5k7x7k"
MS = ["M1", "M2", "M3", "M4", "M5", "M6", "M7"]
L = []
def P(*a):
    s = " ".join(str(x) for x in a); L.append(s); print(s)
F = {}
for line in open(HERE / "b12_features.jsonl"):
    r = json.loads(line); F[r["pool"]] = r
b = pd.read_csv(HERE / "blind_metrics.csv")
pop = b[b.retenu == 1].set_index("pool")
pools = list(pop.index); n = len(pools); assert n == 212 and all(p in F for p in pools)
X = pop[MS].to_numpy(float)
iD = pools.index(DM)

def base_m(f):
    den1 = max(.1, np.median(f["m1_windows"])); den2 = max(.1, np.median(f["m2_windows"]))
    t = f["num24"]
    return dict(M1=f["num3"] / den1, M2=t / den2, M3=f["newsol"] / t, M4=sum(f["top5"]) / t, M5=f["pairs"] / (f["n_buyers"] * (f["n_buyers"] - 1) / 2 / 216000), M6=f["early_net"] / f["early_bought"], M7=f["maxbuy"] / f["maxbuy_res"])
for i, p in enumerate(pools):
    bm = base_m(F[p])
    for j, m in enumerate(MS):
        assert abs(bm[m] - X[i, j]) <= 1e-5 * max(abs(X[i, j]), 1e-9), (p, m, bm[m], X[i, j])
P("calcul incrémental identique à b03 sur les 212 tokens, effet nul : OK")

def inject(f, x, w, win, sync=False):
    """x SOL en plus, w wallets neufs. win=3 : un achat par wallet sur les 3 dernières heures. win=24 : 8 achats par wallet, un par tranche de 3 h."""
    t = f["num24"] + x
    m1w = np.array(f["m1_windows"], float)
    if win == 3:
        add3 = x; size = x / w
    else:
        add3 = x / 8; size = x / (w * 8)
        m1w = m1w.copy(); m1w[-7:] += x / 8  # [S−24 h, S−3 h) recouvre les 7 dernières fenêtres du dénominateur de M1
    M1 = (f["num3"] + add3) / max(.1, np.median(m1w))
    M2 = t / max(.1, np.median(f["m2_windows"]))
    M3 = (f["newsol"] + x) / t
    top = sorted(f["top5"] + [x / w] * min(w, 5), reverse=True)[:5]
    M4 = sum(top) / t
    nb = f["n_buyers"] + w
    pairs = f["pairs"] + (w // 2) * (w // 2 - 1) / 2 if sync else f["pairs"]
    M5 = pairs / (nb * (nb - 1) / 2 / 216000)
    res = f["res_S24h"] if win == 24 else f["res_S3h"]
    M7 = size / res if size > f["maxbuy"] and res else f["maxbuy"] / f["maxbuy_res"]
    M6 = f["early_net"] / f["early_bought"]
    return np.array([M1, M2, M3, M4, M5, M6, M7])

def verdict_row(target_vals, i):
    """p de rang contre les 211 autres, Holm. Rend (passe, ps)."""
    others = np.delete(X, i, axis=0)
    # tolérance : M3 et M4 valent 1 à l'arrondi flottant près chez B ; un ex aequo au plafond compte contre la cible, comme dans le plan
    ps = (1 + (others >= target_vals - 1e-9).sum(0)) / (others.shape[0] + 1)
    order = np.argsort(ps); go = True; passed = []
    for r, j in enumerate(order):
        go = go and ps[j] <= 0.05 / (7 - r)
        if go: passed.append(MS[j])
    return passed, ps

# nul
base = [verdict_row(X[i], i)[0] for i in range(n)]
P("Nul empirique : cibles passant Holm", sum(bool(x) for x in base), "sur", n, "=", round(sum(bool(x) for x in base) / n, 4))

rows = []
scen = []
for win in (3, 24):
    for w in (1, 5, 25):
        for frac in (0.1, 0.25, 0.5, 1, 2, 5):
            scen.append(dict(nom=f"{frac:g}R_{w}w_{win}h", frac=frac, w=w, win=win, sync=False, abs_sol=None))
    for frac in (0.5, 2):
        scen.append(dict(nom=f"{frac:g}R_25w_{win}h_sync", frac=frac, w=25, win=win, sync=True, abs_sol=None))
# effets du contrôle positif de l'étude, appliqués à la distribution réelle
scen.append(dict(nom="controle_moyen_6w_60SOL_3h_sync", frac=None, w=6, win=3, sync=True, abs_sol=6 * 6 * np.exp(0.5 + 0.08)))
scen.append(dict(nom="controle_fort_18w_740SOL_3h_sync", frac=None, w=18, win=3, sync=True, abs_sol=18 * 25 * np.exp(0.5 + 0.08)))
for sc in scen:
    hit = 0; per = dict.fromkeys(MS, 0); pmins = []
    for i, p in enumerate(pools):
        f = F[p]
        x = sc["abs_sol"] if sc["abs_sol"] else sc["frac"] * (f["res_S24h"] if sc["win"] == 24 else f["res_S3h"])
        if not x: continue
        v = inject(f, x, sc["w"], sc["win"], sc["sync"])
        pas, ps = verdict_row(v, i)
        hit += bool(pas); pmins.append(ps.min())
        for m in pas: per[m] += 1
    fD = F[DM]
    xD = sc["abs_sol"] if sc["abs_sol"] else sc["frac"] * (fD["res_S24h"] if sc["win"] == 24 else fD["res_S3h"])
    vD = inject(fD, xD, sc["w"], sc["win"], sc["sync"])
    pasD, psD = verdict_row(vD, iD)
    rows.append(dict(scenario=sc["nom"], taux_verdict_inhabituel=hit / n, p_min_median=float(np.median(pmins)), **{f"passe_{m}": per[m] for m in MS}, SOL_sur_DMAGA=round(xD, 1), M_DMAGA=np.round(vD, 3).tolist(), p_DMAGA=np.round(psD, 4).tolist(), DMAGA_passe=",".join(pasD)))
sc_df = pd.DataFrame(rows); sc_df.to_csv(HERE / "b13_scenarios.csv", index=False)
P(sc_df[["scenario", "taux_verdict_inhabituel", "p_min_median", "SOL_sur_DMAGA", "DMAGA_passe"]].round(4).to_string())
P("réserve DMAGA S−24 h", round(F[DM]["res_S24h"], 1), "S−3 h", round(F[DM]["res_S3h"], 1), "S−1 h", round(F[DM]["res_S1h"], 1), "cap S−1h", F[DM]["cap_S1h"], "S−24h", F[DM]["cap_S24h"], "S−96h", F[DM]["cap_S96h"], "somme 24 h", round(F[DM]["num24"], 1), "3 h", round(F[DM]["num3"], 1), "1 h", round(F[DM]["num1h"], 1))
P("dénominateurs DMAGA M1", np.median(F[DM]["m1_windows"]), "M2", np.median(F[DM]["m2_windows"]), "acheteurs", F[DM]["n_buyers"], "nouveaux", F[DM]["n_new"], "paires", F[DM]["pairs"])

# détenteur précoce passif : Δ jetons achetés dans les 24 h et jamais vendus, M6 seule change
fD = F[DM]; Bq, Hq = fD["early_bought"], fD["early_net"]
target = np.delete(X, iD, 0)[:, 5].max()
need = (target * Bq - Hq) / (1 - target)
P(f"M6 DMAGA : précoces {fD['n_early']}, achetés {Bq/1e6:.1f} M, encore détenus {Hq/1e6:.1f} M. Pour dépasser le maximum des pairs {target:.4f} il faudrait {need/1e6:.1f} M jetons de plus détenus, soit {need/1e9:.1%} de l'offre")
rr = []
for q in (0.01, 0.02, 0.05, 0.1, 0.2, 0.3):
    d = q * 1e9; hit = 0
    for i, p in enumerate(pools):
        f = F[p]; v = X[i].copy(); v[5] = (f["early_net"] + d) / (f["early_bought"] + d)
        hit += bool(verdict_row(v, i)[0])
    v = X[iD].copy(); v[5] = (Hq + d) / (Bq + d)
    pasD, psD = verdict_row(v, iD)
    rr.append(dict(part_offre=q, taux=hit / n, M6_DMAGA=round(v[5], 4), p_M6_DMAGA=round(psD[5], 4), DMAGA_passe=",".join(pasD)))
P("Détenteur précoce passif :\n" + pd.DataFrame(rr).to_string())

# facteurs : une mesure multipliée par phi (M3, M4, M6 : sur les cotes), chaque token tour à tour
def apply_phi(v, j, phi):
    v = v.copy()
    if MS[j] in ("M3", "M4", "M6"):
        o = min(v[j], 1 - 1e-12) / (1 - min(v[j], 1 - 1e-12)); o *= phi; v[j] = o / (1 + o)
    else:
        v[j] *= phi
    return v
fac = []
for phi in (1, 2, 5, 10, 20, 50, 100, 1000, 10000):
    d = {"facteur": phi}
    for j, m in enumerate(MS):
        d[m] = np.mean([bool(verdict_row(apply_phi(X[i], j, phi), i)[0]) for i in range(n)])
    vall = lambda i: np.array([apply_phi(X[i], j, phi)[j] for j in range(7)])
    d["toutes"] = np.mean([bool(verdict_row(vall(i), i)[0]) for i in range(n)])
    d["DMAGA_une_mesure_suffit"] = ",".join(MS[j] for j in range(7) if verdict_row(apply_phi(X[iD], j, phi), iD)[0])
    fac.append(d)
fd = pd.DataFrame(fac); fd.to_csv(HERE / "b13_facteurs.csv", index=False)
P("\nTaux de verdict inhabituel si une seule mesure de la cible est multipliée par phi (cotes pour M3, M4, M6) :\n" + fd.round(3).to_string())

# variables de confusion et planchers
A = pd.DataFrame({"pool": pools, "den1": [np.median(F[p]["m1_windows"]) for p in pools], "den2": [np.median(F[p]["m2_windows"]) for p in pools], "age": [F[p]["age_jours"] for p in pools], "n_buyers": [F[p]["n_buyers"] for p in pools],
                  "num24": [F[p]["num24"] for p in pools], "res1": [F[p]["res_S1h"] for p in pools], "cap1": [F[p]["cap_S1h"] for p in pools], "cap24": [F[p]["cap_S24h"] for p in pools], "cap96": [F[p]["cap_S96h"] for p in pools], "created": [F[p]["created"] for p in pools], "n_early": [F[p]["n_early"] for p in pools], "num1h": [F[p]["num1h"] for p in pools], "num3": [F[p]["num3"] for p in pools]})
for j, m in enumerate(MS): A[m] = X[:, j]
C = A[A.pool != DM]; D = A[A.pool == DM].iloc[0]
P("\nPlancher 0,1 SOL actif : M1", int((C.den1 <= .1).sum()), "/211 (DMAGA", bool(D.den1 <= .1), ") ; M2", int((C.den2 <= .1).sum()), "/211 ; dénominateur nul M1", int((C.den1 == 0).sum()), "M2", int((C.den2 == 0).sum()))
P("Spearman avec âge, acheteurs, volume 24 h, dénominateurs, date de création, capitalisation S−1 h :")
P(C[MS + ["age", "n_buyers", "num24", "den1", "den2", "created", "cap1"]].corr(method="spearman").loc[MS, ["age", "n_buyers", "num24", "den1", "den2", "created", "cap1"]].round(2).to_string())
def cond(mask, label):
    g = C[mask]
    pv = {m: round((1 + (g[m] >= D[m]).sum()) / (len(g) + 1), 3) for m in MS}
    P(f"EXPLORATOIRE {label} : k={len(g)}, p={pv}")
P("\nRangs conditionnels, EXPLORATOIRE, sans correction, ne remplacent jamais le verdict gelé :")
cond(C.den1 > .1, "M1 sans plancher actif (M1)")
cond(C.den2 > .1, "M2 sans plancher actif (M2)")
cond((C.den1 >= D.den1 / 3) & (C.den1 <= D.den1 * 3), "dénominateur M1 à un facteur 3 de DMAGA")
cond(C.n_buyers >= 100, "au moins 100 acheteurs sur 24 h")
cond((C.n_buyers >= D.n_buyers / 2) & (C.n_buyers <= D.n_buyers * 2), "acheteurs à un facteur 2 de DMAGA")
cond((C.age >= D.age / 1.5) & (C.age <= D.age * 1.5), "âge à S à un facteur 1,5 de DMAGA")
cond((C.cap1 >= D.cap1 / 3) & (C.cap1 <= D.cap1 * 3), "capitalisation S−1 h à un facteur 3 de DMAGA")
cond((C.cap96 >= D.cap96 / 3) & (C.cap96 <= D.cap96 * 3), "capitalisation S−96 h à un facteur 3 de DMAGA")
cond(C.created.between(D.created - 14 * 86400, D.created + 14 * 86400), "création à 14 jours de DMAGA")
P("Comparaisons exploratoires de ce bloc : 9 sous-groupes × 7 mesures = 63")
rt = (C.cap1 / C.cap24); dr = D.cap1 / D.cap24
P(f"EXPLORATOIRE hausse de capitalisation S−24 h à S−1 h : DMAGA x{dr:.2f}, pairs >= DMAGA {(rt >= dr).sum()}/{rt.notna().sum()}, p {(1 + (rt >= dr).sum()) / (rt.notna().sum() + 1):.3f}")
P("Bande à S−96 h : pairs avec cap S−96 h dans la bande", int(C.cap96.between(1e5, 1e7).sum()), "; ratio cap S−1h / S−24h DMAGA", round(D.cap1 / D.cap24, 2), "médiane pairs", round((C.cap1 / C.cap24).median(), 2), "; ratio S−1h / S−96h DMAGA", round(D.cap1 / D.cap96, 2), "médiane", round((C.cap1 / C.cap96).median(), 2))
# décalages
P("\nDécalage de S (EXPLORATOIRE, 3 décalages × 7 mesures = 21 comparaisons) :")
for dh in (2, 3, 6):
    Y = np.array([[np.nan if F[p][f"shift{dh}"][m] is None else F[p][f"shift{dh}"][m] for m in MS] for p in pools], float)
    dY = Y[iD]; oY = np.delete(Y, iD, 0)
    ps = [(1 + np.nansum(oY[:, j] >= dY[j])) / (np.isfinite(oY[:, j]).sum() + 1) for j in range(7)]
    P(f"S−{dh} h : DMAGA {np.round(dY, 3).tolist()} ; médiane pairs {np.round(np.nanmedian(oY, 0), 3).tolist()} ; p {np.round(ps, 3).tolist()}")
P("S (plan) : DMAGA", np.round(X[iD], 3).tolist(), "médiane pairs", np.round(np.median(np.delete(X, iD, 0), 0), 3).tolist())
# population des comparateurs au-dessus de DMAGA identique étude et B ?
mt = pd.read_csv(ROOT / "etude_final/derived/metrics.csv"); mt = mt[mt.variant == "primary"].set_index("pool").loc[pools]
for j, m in enumerate(MS):
    s1 = set(np.array(pools)[(mt[m].to_numpy() >= mt[m].loc[DM])]) - {DM}
    s2 = set(np.array(pools)[X[:, j] >= X[iD, j]]) - {DM}
    P(f"{m} : pairs au-dessus de DMAGA, étude {len(s1)}, B {len(s2)}, différence symétrique {len(s1 ^ s2)}")
(HERE / "b13_power.txt").write_text("\n".join(L) + "\n")
