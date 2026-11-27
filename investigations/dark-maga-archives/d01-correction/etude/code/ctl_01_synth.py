#!/usr/bin/env python3
"""Contrôles positifs : tout le calcul et le verdict sur des tokens synthétiques.

Chaque tirage : k tokens de fond, un token cible qui vient de la même loi (nul) ou reçoit une accumulation
injectée (moyen, fort). Le nul doit rester muet. Rapport : controles/synth.md. Registre : données synthétiques.
"""
import os
import sys

import numpy as np

ETUDE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from metrics import METRICS, compute, holm, rank_p, spike_hour, verdict  # noqa: E402
from registre import enregistrer  # noqa: E402

H = 3600
CREATED = 1_700_000_000
S = CREATED + 7 * 86400


def token(rng, effect: str):
    """Fond : achats et ventes poissonniens sur les 7 jours d'avant le pic, décroissants après le lancement."""
    n = rng.integers(400, 2500)
    t = CREATED + (rng.random(n) ** 2.2 * (S - CREATED)).astype(np.int64)
    owner = rng.integers(0, max(40, n // 4), n)
    is_buy = rng.random(n) < 0.55
    size = np.exp(rng.normal(-1.0, 1.1, n))
    qty = (size * 1e9).astype(np.int64) * np.where(is_buy, 1, -1)
    sol = -(size * 1e9).astype(np.int64) * np.where(is_buy, 1, -1)
    if effect == "baleine":
        # un seul wallet écrase les achats des dernières 24 h : M4 doit réagir
        m = 12
        t = np.concatenate([t, S - rng.integers(60, 24 * H - 60, m)])
        owner = np.concatenate([owner, np.full(m, 20_000_000)])
        s_ = np.exp(rng.normal(1.0, 0.3, m)) * 30
        qty = np.concatenate([qty, (s_ * 1e9).astype(np.int64)])
        sol = np.concatenate([sol, -(s_ * 1e9).astype(np.int64)])
    elif effect == "precoces":
        # les wallets entrés dans les 24 h ne revendent plus rien : M6 doit réagir
        early = set(owner[(t < CREATED + 24 * H) & (qty > 0)].tolist())
        keep = np.array([not (o in early and q < 0) for o, q in zip(owner.tolist(), qty.tolist())])
        t, owner, qty, sol = t[keep], owner[keep], qty[keep], sol[keep]
    elif effect != "nul":
        # wallets neufs qui achètent gros, juste avant le pic, certains dans le même slot
        m, mult = (6, 6.0) if effect == "moyen" else (18, 25.0)
        inj_t = S - rng.integers(60, 3 * H - 60, m)
        inj_t[: m // 2] = inj_t[0]  # la moitié dans le même slot
        inj_o = 10_000_000 + np.arange(m)
        inj_s = np.exp(rng.normal(0.5, 0.4, m)) * mult
        t = np.concatenate([t, inj_t])
        owner = np.concatenate([owner, inj_o])
        qty = np.concatenate([qty, (inj_s * 1e9).astype(np.int64)])
        sol = np.concatenate([sol, -(inj_s * 1e9).astype(np.int64)])
    o = np.argsort(t, kind="stable")
    t, owner, qty, sol = t[o], owner[o], qty[o], sol[o]
    slot = (t - CREATED) * 5 // 2
    return t, slot, owner, qty, sol, np.full(len(t), 200_000_000_000, dtype=np.int64)


def run(effect: str, seed: int, k: int = 150) -> tuple[str, dict]:
    rng = np.random.default_rng(seed)
    ctrl = [compute(*token(rng, "nul"), S, CREATED) for _ in range(k)]
    tgt = compute(*token(rng, effect), S, CREATED)
    ps = {m: rank_p(tgt[m], [c[m] for c in ctrl]) for m in METRICS}
    return verdict(ps, k), ps


def main():
    # contrôle de la règle de pic
    hist = {h: 3 for h in range(100, 400)}
    hist[300] = 600
    assert spike_hour(hist, 100 * H) == 300 * H
    assert spike_hour({h: 50 for h in range(100, 400)}, 100 * H) is None

    lines = ["# Contrôles positifs, tokens synthétiques", "",
             "k = 150 comparateurs par tirage, 40 graines par effet.", "",
             "| effet | verdict inhabituel | tirages | taux | mesures qui passent Holm au moins une fois |", "|---|---|---|---|---|"]
    rates = {}
    which_all = {}
    for effect in ("nul", "moyen", "fort", "baleine", "precoces"):
        hits = 0
        which: dict[str, int] = {}
        n = 40
        for seed in range(n):
            v, ps = run(effect, seed)
            if "INHABITUEL" in v:
                hits += 1
            for m, ok in holm(ps).items():
                if ok:
                    which[m] = which.get(m, 0) + 1
        rates[effect] = hits / n
        lines.append(f"| {effect} | {hits} | {n} | {hits / n:.2f} | {', '.join(f'{m}:{c}' for m, c in sorted(which.items())) or 'aucune'} |")
    lines += ["", f"Règle du nul : taux ≤ 0,10 attendu avec Holm à 0,05 sur 7 mesures, observé {rates['nul']:.2f}.",
              "", "Puissance : k = 139 est le minimum pour qu'un test puisse passer ; le verdict l'exige.",
              f"k = 50 rend bien l'inconclusif : {verdict({m: 1 / 51 for m in METRICS}, 50)[:40]}."]
    os.makedirs(os.path.join(ETUDE, "controles"), exist_ok=True)
    path = os.path.join(ETUDE, "controles", "synth.md")
    with open(path, "w") as f:
        f.write("\n".join(lines) + "\n")
    for effect, r in rates.items():
        enregistrer(ETUDE, test=f"controle_{effect}", declare=True, n=150, agent="controle-positif", stat=r,
                    donnees="synthetiques", n_comparaisons=7, sortie="controles/synth.md")
    print("\n".join(lines))
    if rates["nul"] > 0.10 or rates["fort"] < 0.8 or rates["baleine"] < 0.5 or rates["precoces"] < 0.5:
        sys.exit("contrôle en échec : nul trop bruyant, ou un effet dédié non détecté")


if __name__ == "__main__":
    main()
