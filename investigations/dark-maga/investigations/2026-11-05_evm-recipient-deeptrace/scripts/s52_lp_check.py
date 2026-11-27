"""Recoupement indépendant des bornes de s51 par un programme linéaire exact (HiGHS, scipy requis ; hors CI).
Réservoirs couplés : b298, le relais 0x4978cd7e et, pour le marquage « makers », b947. Chaque sortie e porte t_e USDC marqués,
0 <= t_e <= x_e ; après chaque événement de chaque réservoir, marqué >= 0 et non marqué >= 0. Un transfert entre deux réservoirs
porte la part marquée de la sortie de l'émetteur. Le minimum (maximum) de t_e sur ce polyèdre est la borne exacte sur toutes les
allocations qui conservent la valeur ; il est atteint par une allocation.
Marquages : « b947 » = USDC envoyé par b947 à partir du 01/10/2024 (convention de s51) ; « makers » = USDC des exécutions deBridge
reçues par b947. Vérifie : les 31 bornes basses et hautes publiées, o1 et o2 seuls, et la borne commune de s51 (joint_bounds).
Lancer depuis scripts/ : ../../../scripts/py.sh s52_lp_check.py (Python du projet, scipy)"""
import csv
import numpy as np
from scipy.optimize import linprog
import s51_bounds as B

R, RL, W = B.load()
D = list(csv.DictReader(open("../evidence/dln_orders_evm.csv")))
FILLS = {r["tx"].lower() for r in D if r["wallet"] == "b947" and r["direction"] == "IN"}

def polytope(makers):
    pools = {"b298": (B.B298, R), "relay": (B.RELAY, RL)} | ({"b947": (B.B947, W)} if makers else {})
    who = {a: p for p, (a, _) in pools.items()}
    var, amt = {}, []
    for p, (_, L) in pools.items():
        for r in L:
            if r["direction"] == "OUT": var[(p,) + B.ref(r)] = len(amt); amt.append(int(r["amount_raw"]) / 1e6)
    n, A, h = len(amt), [], []
    for p, (_, L) in pools.items():
        cT, cC, fT, fC = np.zeros(n), np.zeros(n), 0.0, 0.0  # marqué = fT + cT.t ; non marqué = fC + cC.t
        for r in L:
            x = int(r["amount_raw"]) / 1e6; cp = r["counterparty"]
            if r["direction"] == "IN":
                k = (who.get(cp), r["tx_hash"].lower(), r["log_index"])
                if cp in who and who[cp] != p and k in var:
                    cT[var[k]] += 1; cC[var[k]] -= 1; fC += x
                elif cp in who and who[cp] != p:
                    raise AssertionError(f"transfert {k} sans sortie miroir")
                elif makers: marked = p == "b947" and r["tx_hash"].lower() in FILLS; fT += x * marked; fC += x * (not marked)
                else: marked = cp == B.B947 and r["timestamp_utc"] >= B.T0; fT += x * marked; fC += x * (not marked)
            else:
                i = var[(p,) + B.ref(r)]; cT[i] -= 1; cC[i] += 1; fC -= x
            A += [-cT.copy(), -cC.copy()]; h += [fT, fC]
    return var, np.array(A), np.array(h), [(0, a) for a in amt]

def solve(P, coef):
    var, A, h, bd = P; c = np.zeros(len(bd))
    for k, w in coef.items(): c[var[k]] = w
    r = linprog(c, A_ub=A, b_ub=h, bounds=bd, method="highs"); assert r.status == 0, r.message
    return round(r.fun, 6)

def key(P, tx): return next(k for k in P[0] if k[0] == "b298" and k[1] == tx)

if __name__ == "__main__":
    P = polytope(False)
    pub = list(csv.DictReader(open("../evidence/s51_b298_usdc_bounds.csv")))
    bad = [r["tx_hash"] for r in pub if solve(P, {key(P, r["tx_hash"].lower()): 1}) != float(r["from_b947_min"])
           or -solve(P, {key(P, r["tx_hash"].lower()): -1}) != float(r["from_b947_max"])]
    print(f"{len(pub) - len(bad)}/{len(pub)} bornes basses et hautes publiées = optimum exact"); assert not bad, bad
    o1, o2 = key(P, B.O1), key(P, B.O2)
    J = B.joint_bounds(R, RL, W, FILLS)
    lp = (solve(P, {o1: 1}), solve(P, {o2: 1}), solve(P, {o1: 1, o2: 1}))
    print("marqué = venu de b947 : o1 >=", lp[0], "; o2 >=", lp[1], "; o1 + o2 >=", lp[2], "(s51 :", B.U(J["joint"]), ")")
    assert lp == (46.814553, 0.0, B.U(J["joint"])), lp
    Pm = polytope(True); m1, m2 = key(Pm, B.O1), key(Pm, B.O2)
    lpm = solve(Pm, {m1: 1, m2: 1})
    print("marqué = exécutions deBridge reçues par b947 : o1 + o2 >=", lpm, "(s51 :", B.U(J["joint_makers"]), ")")
    assert lpm == B.U(J["joint_makers"]), lpm
