"""Phase 2 : sélection, biais, amendement 001. Comparaison collectés / reportés sur ce qui est connu sans transaction,
ordre de collecte, bornes sur R1 et R2, tronqués. Sorties : b14_selection.txt, b14_r_bornes.csv."""
import json
from pathlib import Path
import numpy as np, pandas as pd
from scipy import stats
HERE = Path(__file__).parent; ROOT = HERE.parents[2]
EXT = Path("/Volumes/VERBATIM HD/Dark-MAGA-Investigation")
DM = "CRSwXnfF21yHDXdYBVWwCwQ5Ni2A4QuK3qGYis5k7x7k"
MS = ["M1", "M2", "M3", "M4", "M5", "M6", "M7"]
L = []
def P(*a):
    s = " ".join(str(x) for x in a); L.append(s); print(s)
sel = pd.read_json(EXT / "data/controls/selection.jsonl", lines=True)
sel["pos"] = np.arange(len(sel))
pk = pd.read_csv(HERE / "b01_peak.csv")[["pool", "hist_hours", "hist_sum", "last_hist_hour", "nS20", "med20", "nS10", "med10", "pages", "n_late_first_page"]]
d = sel.merge(pk, on="pool")
d["age_s20"] = (d.S20 - d.created) / 86400
d["ratio"] = d.nS20 / d.med20.clip(lower=5)
d["fdv"] = d.fdv_s20.fillna(d.fdv_s10)
B = (100000, 10000000); W = (10000, 50000000)
d["main"] = d.S20.notna() & d.fdv_s20.between(*B)
d["r2"] = d.S20.notna() & d.fdv_s20.between(*W)
d["r1"] = d.S10.notna() & d.fdv_s10.between(*B)
sup = d[d.status.isin(["retenu_superset", "reporte_budget"])].copy()
P("position dans selection.jsonl par statut :", sel.groupby("status").pos.agg(["min", "max", "count"]).to_string())
pr = sup.sort_values("pos")
P("les 213 principaux viennent d'abord :", bool(pr.iloc[:213].main.all()), " ; superset :", len(sup))
col = sup[sup.status == "retenu_superset"]; rep = sup[sup.status == "reporte_budget"]; non_main_col = col[~col.main]
P("collectés", len(col), "dont principaux", int(col.main.sum()), "hors principaux", len(non_main_col), "reportés", len(rep))
P("positions des collectés hors principaux :", non_main_col.pos.min(), non_main_col.pos.max(), "reportés :", rep.pos.min(), rep.pos.max())
def cmp(a, b, name):
    P(f"\n== {name} : n {len(a)} contre {len(b)}")
    for v in ["created", "S20", "age_s20", "fdv", "fdv_s20", "fdv_s10", "hist_sum", "nS20", "med20", "ratio", "pages", "truncated"]:
        x, y = a[v].dropna().astype(float), b[v].dropna().astype(float)
        if len(x) < 2 or len(y) < 2: continue
        u = stats.mannwhitneyu(x, y, alternative="two-sided"); ks = stats.ks_2samp(x, y)
        f = (lambda z: pd.to_datetime(z, unit="s").strftime("%m-%d")) if v in ("created", "S20") else (lambda z: f"{z:.4g}")
        P(f"{v:10s} médianes {f(x.median())} / {f(y.median())} ; quartiles {f(x.quantile(.25))}-{f(x.quantile(.75))} / {f(y.quantile(.25))}-{f(y.quantile(.75))} ; MW p {u.pvalue:.2e} ; KS p {ks.pvalue:.2e}")
cmp(col, rep, "245 collectés / 278 reportés")
cmp(non_main_col, rep, "32 collectés hors principaux / 278 reportés (hors principaux des deux côtés)")
cmp(d[d.main], rep, "213 principaux / 278 reportés")
r2only_c = col[col.r2 & ~col.main]; r2only_r = rep[rep.r2 & ~rep.main]
cmp(r2only_c, r2only_r, "R2 hors bande principale : collectés / reportés")
P("R2 : fdv sous 100 k$ collectés", int((r2only_c.fdv_s20 < 1e5).sum()), "au-dessus de 10 M$ collectés", int((r2only_c.fdv_s20 > 1e7).sum()), " ; reportés", int((r2only_r.fdv_s20 < 1e5).sum()), int((r2only_r.fdv_s20 > 1e7).sum()))
# neutralité de l'ordre chez les non principaux
nm = sup[~sup.main].sort_values("pos")
for v in ["created", "hist_sum", "nS20", "fdv", "age_s20"]:
    z = nm[[v, "pos"]].dropna()
    P(f"Spearman position / {v} chez les {len(z)} non principaux : {stats.spearmanr(z.pos, z[v]).statistic:+.3f} (p {stats.spearmanr(z.pos, z[v]).pvalue:.2e})")
# ordre du fichier d'activité
act_order = {}
for i, line in enumerate(open(EXT / "data/controls/activity.jsonl")):
    act_order[json.loads(line)["pool"]] = i
nm = nm.assign(act_pos=nm.pool.map(act_order))
P("Spearman position selection / position activity (non principaux) :", round(stats.spearmanr(nm.pos, nm.act_pos).statistic, 4), " ; activity / created :", round(stats.spearmanr(nm.act_pos, nm.created).statistic, 4))
# bornes
mt = pd.read_csv(ROOT / "etude_final/derived/metrics.csv")
rows = []
P("\nS10 différent de S20 chez les collectés :", int(((col.S10 != col.S20) & col.S20.notna() & col.S10.notna()).sum()), "sur", int((col.S20.notna() & col.S10.notna()).sum()))
for var, flag in (("R1_10x", "r1"), ("R2_bande_large", "r2")):
    a = mt[mt.variant == var]; D = a[a.pool == DM].iloc[0]; C = a[a.pool != DM]
    delta = int((rep[flag]).sum()); k = len(C); K = k + delta
    prim = set(mt[mt.variant == "primary"].pool)
    P(f"{var}: k réel {k}, reportés admissibles {delta}, K théorique maximal {K}, part de pairs déjà dans le principal {len(set(C.pool) & prim)}/{k}")
    for m in MS:
        c = int((C[m] >= D[m]).sum())
        pmin = (1 + c) / (K + 1); pmax = (1 + c + delta) / (K + 1)
        qlo = (k - c) / K; qhi = (k - c + delta) / K
        rows.append(dict(variante=var, mesure=m, k=k, c=c, p_reel=(1 + c) / (k + 1), reportes=delta, K=K, p_si_tous_reportes_sous_D=pmin, p_si_tous_au_dessus=pmax, centile_reel=(k - c) / k, centile_min=qlo, centile_max=qhi, k_requis_pour_holm_1re=int(np.ceil((1 + c) / (0.05 / 7) - 1))))
rb = pd.DataFrame(rows); rb.to_csv(HERE / "b14_r_bornes.csv", index=False)
P(rb.round(4).to_string())
# les 29 pairs de R2 hors bande principale : extrapolation vers les 258 reportés
prim_pools = set(mt[mt.variant == "primary"].pool)
a2 = mt[mt.variant == "R2_bande_large"]; D2 = a2[a2.pool == DM].iloc[0]; ex = a2[(a2.pool != DM) & ~a2.pool.isin(prim_pools)]
P("\nR2 : pairs ajoutés au principal", len(ex), " ; date de création min/max", pd.to_datetime(ex.created.min(), unit="s"), pd.to_datetime(ex.created.max(), unit="s"), " ; fdv min/max", ex.fdv_usd.min(), ex.fdv_usd.max())
for m in MS:
    prim = a2[(a2.pool != DM) & a2.pool.isin(prim_pools)]
    c0 = int((prim[m] >= D2[m]).sum()); sh = float((ex[m] >= D2[m]).mean())
    K = len(prim) + len(ex) + 258
    pex = (1 + c0 + (ex[m] >= D2[m]).sum() + 258 * sh) / (K + 1)
    u = stats.mannwhitneyu(ex[m].dropna(), prim[m].dropna(), alternative="two-sided").pvalue
    P(f"{m}: médiane ajoutés {ex[m].median():.3f}, principal {prim[m].median():.3f}, MW p {u:.3f} ; ajoutés >= DMAGA {(ex[m] >= D2[m]).sum()}/{len(ex)} ; p extrapolé si les 258 reportés ressemblent aux 29 : {pex:.3f}")
# lien mesure et date sur les 242 tokens à S20 collectés (R2)
z = a2[a2.pool != DM]
P("Spearman mesure / date de création sur R2 :", {m: round(stats.spearmanr(z.created, z[m], nan_policy="omit").statistic, 3) for m in MS})
# tronqués et effet sur le rang
pop = mt[mt.variant == "primary"].merge(sel[["pool", "truncated"]], on="pool")
C = pop[pop.pool != DM]; D = pop[pop.pool == DM].iloc[0]
P("\nTronqués : population principale", int(C.truncated.sum()), "sur", len(C), " ; DMAGA tronqué", bool(D.truncated))
for m in MS:
    x, y = C[C.truncated][m], C[~C.truncated][m]
    P(f"{m}: médiane tronqués {x.median():.3f}, non tronqués {y.median():.3f}, MW p {stats.mannwhitneyu(x, y).pvalue:.3f} ; pairs tronqués >= DMAGA {(x >= D[m]).sum()}/{len(x)} ; non tronqués {(y >= D[m]).sum()}/{len(y)}")
tr = pd.read_csv(HERE / "b08_trunc.csv")
tt = tr[tr.status == "sans_pic"]
P("135 tronque_sans_pic : couverture médiane", tt.couverture_jours.median(), "n'atteignent pas 96 h", int((tt.atteint_96h == 0).sum()), "max horaire médian", tt.max_h.median())
P("Tronqués avec S20 (113) dans la bande principale :", int(((sel.truncated) & sel.S20.notna() & sel.fdv_s20.between(*B)).sum()))
for m in ["M6"]:
    c = int((C[m] >= D[m]).sum())
    P(f"Sur {m}, k nécessaire pour p <= 0,05/7 à c={c} constant : {int(np.ceil((1 + c) / (0.05 / 7) - 1))} ; sur M1 : {int(np.ceil((1 + (C.M1 >= D.M1).sum()) / (0.05 / 7) - 1))}")
# activité d'avant 96 h des exclus contre DMAGA
for line in open(EXT / "data/controls/activity.jsonl"):
    r = json.loads(line)
    if r["pool"] == DM:
        h = {a: b for a, b in r["hist"]}; cr = r["created"]
        P("DMAGA signatures sur [24 h, 96 h) :", sum(v for k, v in h.items() if k * 3600 < cr + 96 * 3600), "; heures du 21/07 de 12:00 à 20:00 :", {pd.to_datetime(k * 3600, unit="s").strftime("%H:%M"): h.get(k, 0) for k in range(478212, 478221)})
        S = 478219
        med = lambda x: float(np.median([h.get(y, 0) for y in range(x - 72, x)]))
        P("médiane 72 h avant 13:00..19:00 :", {pd.to_datetime(k * 3600, unit="s").strftime("%H:%M"): (h.get(k, 0), med(k), round(h.get(k, 0) / max(med(k), 5), 1)) for k in range(478213, 478220)})
# 4 curseurs incomplets
for p in ["5jG2h6zF", "8deVHU54", "EUr4qeHV", "acaDbR5Q"]:
    z = d[d.pool.str.startswith(p)].iloc[0]
    P("curseur incomplet", p, "statut", z.status, "main", z.main, "fdv_s20", z.fdv_s20, "fdv_s10", z.fdv_s10, "pos", z.pos)
(HERE / "b14_selection.txt").write_text("\n".join(L) + "\n")
