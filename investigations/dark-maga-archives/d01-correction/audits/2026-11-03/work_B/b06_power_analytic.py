"""Puissance d'un test de rang à cible unique avec Holm à 7 tests. Calcul exact, sans donnée de l'étude.
Sortie : b06_power_analytic.txt."""
from pathlib import Path
import math
out = []
def holm_c(k, m=7, alpha=0.05):
    """Pour chaque rang i de Holm, plus grand nombre c de comparateurs >= cible tel que (1+c)/(k+1) <= alpha/(m-i)."""
    return [math.floor(alpha / (m - i) * (k + 1) - 1 + 1e-12) for i in range(m)]
for k in [139, 211, 245, 500, 1000]:
    c = holm_c(k)
    out.append(f"k={k} : plus petit p = 1/{k+1} = {1/(k+1):.5f}, seuil Holm 1er = {0.05/7:.5f}, c max par rang Holm = {c}")
out.append("")
out.append("Puissance = P(au plus c0 comparateurs au-dessus de la cible sur au moins une mesure), q = quantile vrai de la cible chez les pairs, comparateurs iid, mesures indépendantes. c0 = 0 pour k = 139 et 211.")
out.append("q      k=211,m=1  k=211,m=3  k=211,m=7  k=139,m=1  k=500,m=1")
for q in [0.5, 0.9, 0.95, 0.975, 0.99, 0.995, 0.9975, 0.999, 0.9995, 0.9999]:
    # binomiale : la 1re marche de Holm tolère c0 comparateurs au-dessus (c0 = 0 pour k = 139 et k = 211, 2 pour k = 500)
    def f(k, m):
        c0 = holm_c(k)[0]
        one = sum(math.comb(k, j) * (1 - q) ** j * q ** (k - j) for j in range(c0 + 1))
        return 1 - (1 - one) ** m
    out.append(f"{q:<6} {f(211,1):<10.4f} {f(211,3):<10.4f} {f(211,7):<10.4f} {f(139,1):<10.4f} {f(500,1):<10.4f}")
out.append("")
# quantile requis pour une puissance donnée, k=211, 1 mesure ; écart en z
from statistics import NormalDist
Z = NormalDist()
for pw in [0.5, 0.8, 0.9]:
    q = pw ** (1 / 211)
    out.append(f"puissance {pw:.0%} sur 1 mesure, k=211 : quantile vrai {q:.5f}, soit z = {Z.inv_cdf(q):.2f}, facteur {math.exp(Z.inv_cdf(q)):.1f}^sigma sur une loi log-normale")
out.append("")
# taille réelle sous le nul, mesures indépendantes (borne haute) ou identiques (borne basse), absence d'égalités
k = 211
for m in [1, 7]:
    out.append(f"sous le nul, k=211, {m} mesures indépendantes : P(min p = 1/212) = {1-(211/212)**m:.4f}")
out.append("seuil nominal 0,05 ; la discrétisation rend le test Holm conservateur : seul p = 1/212 ouvre la première marche.")
Path(__file__).with_name("b06_power_analytic.txt").write_text("\n".join(out) + "\n")
print("\n".join(out))
