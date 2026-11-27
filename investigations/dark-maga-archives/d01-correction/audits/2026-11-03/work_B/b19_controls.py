"""Phase 2 : relance les contrôles synthétiques de l'étude sans rien écrire dans etude_final (registre remplacé par un stub),
k = 150 et k = 211, plus de graines, et compare la dispersion synthétique à la dispersion réelle. Sortie : b19_controls.txt."""
import sys, types
from pathlib import Path
import numpy as np, pandas as pd
HERE = Path(__file__).parent; ROOT = HERE.parents[2]
stub = types.ModuleType("registre"); stub.enregistrer = lambda *a, **k: None
sys.modules["registre"] = stub
sys.path.insert(0, str(ROOT / "etude_final/code"))
import ctl_01_synth as C
from metrics import METRICS, compute, holm, rank_p, verdict
L = []
def P(*a):
    s = " ".join(str(x) for x in a); L.append(s); print(s, flush=True)
S, CREATED = C.S, C.CREATED
def clopper(x, n, a=.05):
    from scipy import stats
    lo = stats.beta.ppf(a / 2, x, n - x + 1) if x else 0.0
    hi = stats.beta.ppf(1 - a / 2, x + 1, n - x) if x < n else 1.0
    return lo, hi
# 1. même chose que le rapport : k = 150, 40 graines
for eff in ("nul", "moyen", "fort", "baleine", "precoces"):
    hits = sum("INHABITUEL" in C.run(eff, s)[0] for s in range(40))
    P(f"k=150, 40 graines, {eff}: {hits}/40")
# 2. nul à k = 150 et 211 avec plus de graines (mêmes tokens de fond réutilisés pour gagner du temps : nouvelle graine, nouvelle table)
for k, ns in ((150, 150), (211, 150)):
    hits = 0
    for s in range(1000, 1000 + ns):
        v, _ = C.run("nul", s, k=k)
        hits += "INHABITUEL" in v
    lo, hi = clopper(hits, ns)
    P(f"nul k={k}, {ns} graines : {hits} verdicts inhabituels, taux {hits/ns:.3f}, IC95 [{lo:.3f}, {hi:.3f}] ; attendu si mesures indépendantes 1-(k/(k+1))^7 = {1-(k/(k+1))**7:.3f}")
lo, hi = clopper(2, 40); P(f"rapport : nul 2/40 = 0,05, IC95 [{lo:.3f}, {hi:.3f}]")
# 3. dispersion
rng = np.random.default_rng(5)
syn = pd.DataFrame([compute(*C.token(rng, "nul"), S, CREATED) for _ in range(800)])[list(METRICS)]
mt = pd.read_csv(ROOT / "etude_final/derived/metrics.csv"); real = mt[(mt.variant == "primary") & (~mt.is_dmaga)][list(METRICS)]
rows = []
for m in METRICS:
    a, b = syn[m].dropna(), real[m].dropna()
    rows.append(dict(mesure=m, synth_med=a.median(), synth_p90=a.quantile(.9), synth_max=a.max(), synth_max_sur_med=a.max() / a.median() if a.median() else np.nan, reel_med=b.median(), reel_p90=b.quantile(.9), reel_max=b.max(), reel_max_sur_med=b.max() / b.median()))
P(pd.DataFrame(rows).round(3).to_string())
# 4. taille d'effet synthétique : quantile et facteur atteints par la cible injectée, dans la loi synthétique
for eff in ("moyen", "fort", "baleine", "precoces"):
    t = pd.DataFrame([compute(*C.token(np.random.default_rng(s), eff), S, CREATED) for s in range(40)])[list(METRICS)]
    P(eff, "médiane cible / médiane fond :", {m: round(t[m].median() / syn[m].median(), 1) if syn[m].median() else None for m in METRICS}, " médiane cible / max du fond :", {m: round(t[m].median() / syn[m].max(), 2) for m in METRICS})
    # même cible face aux vrais comparateurs
    hits = 0
    for _, r in t.iterrows():
        ps = {m: (1 + (real[m] >= r[m]).sum()) / (len(real) + 1) for m in METRICS}
        hits += any(holm(ps).values())
    P(f"   la même cible synthétique face aux 211 vrais comparateurs : {hits}/40 verdicts inhabituels")
(HERE / "b19_controls.txt").write_text("\n".join(L) + "\n")
