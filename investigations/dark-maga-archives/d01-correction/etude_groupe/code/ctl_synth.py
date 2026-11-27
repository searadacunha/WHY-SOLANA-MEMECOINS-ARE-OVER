#!/usr/bin/env python3
"""Contrôle de la plomberie sur transactions synthétiques, sans réseau. Lignes de registre marquées synthétiques. Écrit controles/synth.md."""
import random
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from ana_grp import ETUDE, holm, rank_p, verdict  # noqa: E402
from graphe import ONE_M, ata, b58d, b58e, measures, transfers  # noqa: E402
from registre import enregistrer  # noqa: E402

MINT = "7D7BRcBYepfi77vxySapmeqRNN1wsBBxnFPJGbH5pump"


def tx(pre, post, keys=(), lam=None, err=None, other=None):
    def bal(d, m=MINT):
        return [{"mint": m, "owner": o, "uiTokenAmount": {"amount": str(v)}} for o, v in d.items()]
    o_pre, o_post = (other or ({}, {}))
    return {"transaction": {"message": {"accountKeys": [{"pubkey": k} for k in keys]}},
            "meta": {"err": err, "preTokenBalances": bal(pre) + bal(o_pre, "AUTRE"), "postTokenBalances": bal(post) + bal(o_post, "AUTRE"),
                     "preBalances": [0 for _ in keys], "postBalances": list(lam or [0 for _ in keys])}}


# ATA : triple relu dans le brut de DMAGA (propriétaire, mint, compte de jetons)
assert ata("8YLEuUtZ4eFMJbf46oNb1CeG6dYFWGyxnQSh9hrgzBzR", MINT) == "3KD3hsPo4yp7UBLx5gW3bz78FmZhxPH4XdLSQjTsC1EB"
assert b58e(b58d(MINT)) == MINT

# transfert pur, compte créé chez le receveur
assert transfers(tx({"A": 5 * ONE_M}, {"A": 3 * ONE_M, "B": 2 * ONE_M}), MINT) == ([["A", "B", 2 * ONE_M]], False)
# plusieurs receveurs, le petit n'est pas une arête
assert transfers(tx({"A": 5 * ONE_M}, {"B": 4 * ONE_M, "C": ONE_M // 2, "A": ONE_M // 2}), MINT)[0] == [["A", "B", 4 * ONE_M]]
# sous le seuil, échec, deux expéditeurs, somme fausse
assert transfers(tx({"A": ONE_M}, {"B": ONE_M - 1, "A": 1}), MINT) == ([], False)
assert transfers(tx({"A": 2 * ONE_M}, {"B": 2 * ONE_M}, err={"x": 1}), MINT) == ([], False)
assert transfers(tx({"A": 2 * ONE_M, "C": 2 * ONE_M}, {"B": 4 * ONE_M}), MINT) == ([], True)
assert transfers(tx({"A": 2 * ONE_M}, {"B": ONE_M}), MINT) == ([], False)
# swap : le SOL de l'acheteur bouge ou un autre mint bouge, jamais une arête
assert transfers(tx({"P": 9 * ONE_M}, {"P": 7 * ONE_M, "B": 2 * ONE_M}, keys=["B"], lam=[-60_000_000]), MINT) == ([], False)
assert transfers(tx({"P": 9 * ONE_M}, {"P": 7 * ONE_M, "B": 2 * ONE_M}, other=({"B": 9}, {"B": 1})), MINT) == ([], False)
# 0,002 SOL de loyer n'empêche pas
assert transfers(tx({"A": 2 * ONE_M}, {"B": 2 * ONE_M}, keys=["A"], lam=[-2_039_280]), MINT)[0] == [["A", "B", 2 * ONE_M]]

# mesures : chaîne de 3, paire isolée, service à 15 voisins retiré
e = [["A", "B", ONE_M], ["B", "C", ONE_M], ["D", "E", 9 * ONE_M], ["A", "B", ONE_M]]
g = measures(e, {"A": 10**14, "B": 0, "C": 10**14, "D": 10**15})
assert (g["G1"], g["G2"], g["G3"]) == (3, 0.2, 3), g
assert measures(e, {}, min_raw=5 * ONE_M)["G1"] == 2
hub = [["H", f"w{i}", ONE_M] for i in range(15)]
assert measures(hub, {})["G1"] == 0 and measures(hub, {})["services_retires"] == 1
assert measures(hub, {}, hub=None)["G1"] == 16
assert measures([], {}) == {"G1": 0, "G2": 0.0, "G3": 0, "services_retires": 0}

# verdict
assert verdict({"G1": 1 / 60, "G2": 0.5, "G3": 0.5}, 58).startswith("INCONCLUSIF")
assert verdict({"G1": 1 / 60, "G2": 0.5, "G3": 0.5}, 59).startswith("ORGANISATION INHABITUELLE SUR G1")
assert verdict({"G1": 2 / 60, "G2": 0.5, "G3": 0.5}, 59).startswith("AUCUNE")
assert rank_p(3, [1, 3, 5, float("nan")]) == 3 / 4


def draw(rng, n, big):
    """Pairs : 80 % sans arête, sinon petit graphe. big : cible à groupe marqué."""
    if big:
        return (rng.randint(20, 40), rng.uniform(0.1, 0.3), rng.randint(20, 50))
    if rng.random() < 0.8:
        return (0, 0.0, 0)
    return (rng.randint(2, 6), rng.uniform(0, 0.05), rng.randint(1, 8))


lines = ["# Contrôle de la plomberie, transactions et graphes synthétiques", "",
         "**Ce contrôle teste le code, pas la puissance.** Effets synthétiques choisis faciles à voir. Il ne dit rien de ce que le test détecterait sur la distribution réelle des pairs : celle-ci n'est pas connue au gel, elle sera rapportée avec les résultats.", "",
         "Assertions passées : dérivation ATA contre un triple relu dans le brut de DMAGA, 11 cas de transferts (pur, multi-receveurs, seuil, échec, ambigu, somme fausse, swap par le SOL, swap par un autre mint, loyer), 5 cas de mesures, verdict à k = 58 et 59, rang avec NaN.", "",
         "| Effet | Tirages | Verdict inhabituel | k |", "|---|---|---|---|"]
for name, big in (("nul", False), ("fort", True)):
    hits = 0
    for seed in range(200):
        rng = random.Random(seed)
        k = 115
        peers = [draw(rng, k, False) for _ in range(k)]
        t = draw(rng, k, big)
        ps = {m: rank_p(t[i], [p[i] for p in peers]) for i, m in enumerate(("G1", "G2", "G3"))}
        hits += verdict(ps, k).startswith("ORGANISATION")
    lines.append(f"| {name} | 200 | {hits} | 115 |")
    enregistrer(ETUDE, test=f"controle_{name}", declare=True, n=200, agent="controle", n_tirages=200, n_hits=hits, donnees="synthetiques", sortie="controles/synth.md")
    if name == "nul":
        assert hits <= 200 * 0.1, hits
    else:
        assert hits == 200, hits
assert holm({"a": 0.01, "b": 0.5}) == {"a": True, "b": False}
Path(ETUDE, "controles").mkdir(exist_ok=True)
Path(ETUDE, "controles", "synth.md").write_text("\n".join(lines) + "\n")
print("\n".join(lines[-3:]))
