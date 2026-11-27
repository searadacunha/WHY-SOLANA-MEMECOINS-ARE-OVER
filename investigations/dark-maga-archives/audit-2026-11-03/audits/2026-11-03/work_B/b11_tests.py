"""Phase 2 : recalcul à la main des p de rang et de Holm sur derived/metrics.csv et sur les mesures de B, variantes comprises,
percentiles, intervalles, égalités et plafonds, corrélations, dominance. Sorties : b11_tests.txt, b11_dmaga_table.csv."""
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
mt = pd.read_csv(ROOT / "etude_final/derived/metrics.csv")
tests = json.load(open(ROOT / "etude_final/tables/tests.json"))
def my_holm(ps, alpha=0.05):
    items = sorted(ps.items(), key=lambda kv: kv[1])
    m = len(items); res = {}; go = True
    for i, (k, p) in enumerate(items):
        go = go and p <= alpha / (m - i)
        res[k] = (go, alpha / (m - i))
    return res
for var in ["primary", "R1_10x", "R2_bande_large", "R3_S_moins_1h"]:
    a = mt[mt.variant == var]; D = a[a.pool == DM].iloc[0]; C = a[a.pool != DM]
    ps = {}; ok = True
    for m in MS:
        v = C[m].dropna().to_numpy()
        c = int((v >= D[m]).sum()); p = (1 + c) / (len(v) + 1); ps[m] = p
        tj = tests["variants"][var]["mesures"][m]
        ok = ok and abs(tj["p"] - p) < 1e-12 and tj["k"] == len(v) and abs(tj["dmaga"] - D[m]) < 1e-9
    h = my_holm(ps)
    P(f"{var}: k={len(C)}, tests.json identique={ok}, jours={C.S.div(86400).astype(int).nunique()}, min p={min(ps.values()):.4f}, passe Holm={[k for k,v in h.items() if v[0]]}, p<0,05 brut={[k for k,v in ps.items() if v<0.05]}")
    if var == "primary":
        P("  holm_primary de tests.json tous faux :", not any(tests["holm_primary"].values()), " seuils :", {k: round(v[1], 5) for k, v in h.items()})
a = mt[mt.variant == "primary"]; D = a[a.pool == DM].iloc[0]; C = a[a.pool != DM]
k = len(C)
b = pd.read_csv(HERE / "blind_metrics.csv"); bb = b[b.retenu == 1]; BD = bb[bb.pool == DM].iloc[0]; BC = bb[bb.pool != DM]
rows = []
for m in MS:
    v = np.sort(C[m].to_numpy()); d = D[m]; c = int((v >= d).sum()); below = int((v < d).sum()); eq = int((v == d).sum())
    # intervalle de Clopper-Pearson à 95 % sur la part de pairs au-dessus de la cible, puis quantile vrai
    lo = stats.beta.ppf(.025, c, k - c + 1) if c else 0; hi = stats.beta.ppf(.975, c + 1, k - c)
    hi1 = stats.beta.ppf(.95, c + 1, k - c)  # borne unilatérale
    cmax = v.max(); ties_at_max = int((v == cmax).sum())
    bounded = m in ("M3", "M4")
    bv = BC[m].to_numpy(); bc = int((bv >= BD[m]).sum())
    rows.append(dict(mesure=m, D_etude=d, D_B=BD[m], med_pairs=np.median(v), p75=np.quantile(v, .75), p90=np.quantile(v, .9), p99=np.quantile(v, .99), max_pairs=cmax, ex_aequo_au_max=ties_at_max, c=c, c_B=bc, p=(1 + c) / (k + 1), p_B=(1 + bc) / (k + 1), rang_sur_212=c + 1, percentile=below / k,
                     q_IC95_bas=1 - hi, q_IC95_haut=1 - lo, q_borne_haute_unilat95=1 - lo, facteur_pour_depasser_max=cmax / d, sup_ou_ega_1=int((v >= 1 - 1e-12).sum())))
t = pd.DataFrame(rows); t.to_csv(HERE / "b11_dmaga_table.csv", index=False)
P(t.round(5).T.to_string())
# Une mesure bornée à 1 avec un pair à 1 ne peut jamais ouvrir Holm
P("\nmesures à plafond : M3 pairs à 1,0 :", int((C.M3 >= 1 - 1e-12).sum()), "; M4 pairs à 1,0 :", int((C.M4 >= 1 - 1e-12).sum()), "; M6 pairs à 1,0 :", int((C.M6 >= 1 - 1e-12).sum()))
P("p minimal atteignable sur M3 :", (1 + (C.M3 >= 1 - 1e-12).sum()) / (k + 1), "sur M4 :", (1 + (C.M4 >= 1 - 1e-12).sum()) / (k + 1), "seuil 1re marche", 0.05 / 7)
# corrélations
sp = C[MS].corr(method="spearman"); P("\nSpearman entre mesures (pairs) :\n" + sp.round(2).to_string())
ev = np.linalg.eigvalsh(sp.to_numpy())
meff_nyholt = 1 + (7 - 1) * (1 - np.var(ev, ddof=1) / 7)
meff_liji = sum((1 if e >= 1 else 0) + (e - np.floor(e)) for e in ev)
P(f"nombre effectif de tests : Nyholt {meff_nyholt:.2f}, Li et Ji {meff_liji:.2f} ; valeurs propres {np.round(ev,2)}")
# dominance, EXPLORATOIRE
all_ = a.copy(); X = all_[MS].to_numpy(); dm = all_.pool.values == DM; d = X[dm][0]
above = (X[~dm] >= d)
P("\nEXPLORATOIRE, dominance : nombre de mesures sur lesquelles un pair est >= DMAGA ; distribution :", dict(zip(*np.unique(above.sum(1), return_counts=True))))
for n in range(1, 8):
    P(f"  pairs >= DMAGA sur au moins {n} mesures : {(above.sum(1) >= n).sum()}")
# rangs par token (centiles leave-one-out)
rmin = np.column_stack([stats.rankdata(X[:, j], method="min") for j in range(7)])
pv = (1 + 212 - rmin) / 212  # p = (1 + #{autres >= x}) / 212, les ex aequo comptent contre le token, comme dans le plan
meanpct = (np.column_stack([stats.rankdata(X[:, j], method="average") for j in range(7)]) / 212).mean(1)
assert abs(pv[dm][0][5] - 33 / 212) < 1e-12
fisher = -2 * np.log(pv).sum(1)
nmed = (X > np.median(X[~dm], axis=0)).sum(1)
np75 = (X >= np.quantile(X[~dm], .75, axis=0)).sum(1)
for name, s in (("centile moyen sur 7", meanpct), ("Fisher sur p de rang", fisher), ("mesures au-dessus de la médiane", nmed), ("mesures >= P75 des pairs", np75)):
    sd = s[dm][0]; c_ = int((s[~dm] >= sd).sum())
    P(f"EXPLORATOIRE {name} : DMAGA {sd:.3f}, pairs >= DMAGA {c_}/211, p {(1 + c_) / 212:.4f}")
# sans M4
idx = [0, 1, 2, 4, 5, 6]
sd = fisher_no4 = -2 * np.log(pv[:, idx]).sum(1); c_ = int((sd[~dm] >= sd[dm][0]).sum()); P(f"EXPLORATOIRE Fisher sans M4 : p {(1 + c_) / 212:.4f} (c={c_})")
P("nb comparaisons exploratoires dans ce bloc : 5 (combinaisons), aucune ne remplace le verdict gelé")
# min p par token : combien de tokens ont un p minimal <= 1/212, taux empirique du verdict sous le nul
h_all = 0; which = []
for i in range(212):
    ps = dict(zip(MS, pv[i])); hh = my_holm(ps)
    if any(v[0] for v in hh.values()):
        h_all += 1; which.append((all_.pool.values[i][:10], [k for k, v in hh.items() if v[0]]))
P(f"\nTaux de verdict « inhabituel » si chaque token est pris tour à tour comme cible contre les 211 autres : {h_all}/212 = {h_all/212:.3f}", which)
# jours
days = C.S.div(86400).astype(int)
vc = days.value_counts()
P("\nJours de pic : distincts", days.nunique(), "max par jour", vc.iloc[0], "tokens sur les 10 jours les plus chargés", vc.iloc[:10].sum(), "jour de DMAGA (21/07/2024) :", int((days == D.S // 86400).sum()), "même heure :", int((C.S == D.S).sum()))
P("Premier et dernier S :", pd.to_datetime(C.S.min(), unit="s"), pd.to_datetime(C.S.max(), unit="s"), " created min/max :", pd.to_datetime(C.created.min(), unit="s"), pd.to_datetime(C.created.max(), unit="s"))
# ICC par jour de pic sur log(mesure)
for m in MS:
    y = np.log(C[m].clip(lower=1e-6)); g = days
    groups = [y[g == d_].to_numpy() for d_ in g.unique()]
    N = len(y); kk = len(groups); gm = y.mean()
    msb = sum(len(x) * (x.mean() - gm) ** 2 for x in groups) / (kk - 1)
    msw = sum(((x - x.mean()) ** 2).sum() for x in groups) / (N - kk)
    n0 = (N - sum(len(x) ** 2 for x in groups) / N) / (kk - 1)
    icc = (msb - msw) / (msb + (n0 - 1) * msw)
    P(f"ICC jour de pic {m}: {icc:.3f} ; k effectif {N / (1 + (n0 - 1) * max(icc, 0)):.0f}")
(HERE / "b11_tests.txt").write_text("\n".join(L) + "\n")
