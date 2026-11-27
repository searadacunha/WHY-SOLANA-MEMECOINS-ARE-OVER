#!/usr/bin/env python3
"""Tests principaux (DMAGA contre comparateurs) et secondaires S1 (DMAGA contre son propre passé)."""
import csv
import json
import os
import sys

import numpy as np

ETUDE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ana_10_table import DMAGA_POOL, load  # noqa: E402
from metrics import METRICS, holm, rank_p  # noqa: E402
from registre import enregistrer  # noqa: E402

H = 3600
WINIG = 1721577749  # 21/07/2024 16:02:29 UTC, id 1815054750775173447
AVATAR = 1721589800  # 21/07/2024 19:23:20 UTC, snowflake de l'image 1815105297410666496
CREATED = 1720923331


def table(variant):
    counts = json.load(open(os.path.join(ETUDE, "derived", "selection_counts.json")))
    if counts.get("swaps_manquants"):
        sys.exit("population partielle : swaps manquants, aucun test calculé")
    rows = list(csv.DictReader(open(os.path.join(ETUDE, "derived", "metrics.csv"))))
    return [r for r in rows if r["variant"] == variant]


def compare(variant):
    rows = table(variant)
    tgt = [r for r in rows if r["pool"] == DMAGA_POOL]
    if len(tgt) != 1:
        return None
    ctrl = [r for r in rows if r["pool"] != DMAGA_POOL]
    out = {}
    for m in METRICS:
        allv = [float(c[m]) if c[m] not in ("", None) else float("nan") for c in ctrl]
        vals = [v for v in allv if v == v]
        out[m] = {"dmaga": float(tgt[0][m]), "p": rank_p(float(tgt[0][m]), vals), "median_ctrl": float(np.median(vals)) if vals else None,
                  "p90_ctrl": float(np.percentile(vals, 90)) if vals else None, "k": len(vals), "indefinis": len(allv) - len(vals)}
    days = len({int(c["S"]) // 86400 for c in ctrl})
    return {"variant": variant, "k": len(ctrl), "jours_de_pic_distincts": days, "S_dmaga": int(tgt[0]["S"]), "mesures": out}


def self_history():
    """S1 : SOL acheté et nouveaux wallets sur [E−3 h, E) contre les fenêtres de 3 h du passé de DMAGA."""
    t, slot, owner, qty, sol, _ = load(DMAGA_POOL)
    if t.max() < AVATAR:
        sys.exit("données DMAGA coupées avant l'envoi de l'avatar : S1 impossible")
    first = {}
    for o, x in zip(owner.tolist(), t.tolist()):
        first.setdefault(o, x)
    is_buy = (qty > 0) & (sol < 0)
    buy = np.where(is_buy, -sol, 0) / 1e9
    res = {}
    for name, E in (("winig", WINIG), ("avatar", AVATAR)):
        start = CREATED + 96 * H
        edges = np.arange(E - 3 * H, start - 1, -3 * H)
        vals_sol = np.array([buy[(t >= e) & (t < e + 3 * H)].sum() for e in edges])
        # nouveaux wallets : acheteurs distincts dont le premier swap tombe dans la fenêtre
        vals_new = np.array([len({o for o in owner[(t >= e) & (t < e + 3 * H) & is_buy].tolist() if e <= first[o] < e + 3 * H}) for e in edges])
        res[name] = {"E": E, "n_fenetres_passees": len(edges) - 1, "sol_achete": float(vals_sol[0]), "nouveaux_wallets": int(vals_new[0]),
                     "p_sol": float((1 + (vals_sol[1:] >= vals_sol[0]).sum()) / len(vals_sol)),
                     "p_new": float((1 + (vals_new[1:] >= vals_new[0]).sum()) / len(vals_new)),
                     "mediane_sol_passe": float(np.median(vals_sol[1:])), "mediane_new_passe": float(np.median(vals_new[1:]))}
    return res


def main():
    os.makedirs(os.path.join(ETUDE, "tables"), exist_ok=True)
    out = {"variants": {}}
    primary = compare("primary")
    if primary is None:
        out["erreur"] = "DMAGA absent de la variante principale"
    else:
        out["variants"]["primary"] = primary
        ps = {m: v["p"] for m, v in primary["mesures"].items()}
        out["holm_primary"] = holm(ps)
    for v in ("R1_10x", "R2_bande_large", "R3_S_moins_1h"):
        c = compare(v)
        if c:
            out["variants"][v] = c
    out["S1"] = self_history()
    ps1 = {f"{n}_{k}": out["S1"][n][f"p_{k}"] for n in out["S1"] for k in ("sol", "new")}
    out["S1_holm"] = holm(ps1)  # Holm séparé, jamais utilisé dans le verdict
    path = os.path.join(ETUDE, "tables", "tests.json")
    with open(path, "w") as f:
        json.dump(out, f, indent=1)
    rel = "tables/tests.json"
    if primary:
        for m, v in primary["mesures"].items():
            enregistrer(ETUDE, test=f"primary_{m}", declare=True, n=v["k"], n_effectif=primary["jours_de_pic_distincts"],
                        agent="analyse-principale", stat=v["dmaga"], p=v["p"], sortie=rel)
    for name, r in out["S1"].items():
        enregistrer(ETUDE, test=f"S1_{name}_sol", declare=True, n=r["n_fenetres_passees"], agent="analyse-principale",
                    stat=r["sol_achete"], p=r["p_sol"], sortie=rel)
        enregistrer(ETUDE, test=f"S1_{name}_new", declare=True, n=r["n_fenetres_passees"], agent="analyse-principale",
                    stat=r["nouveaux_wallets"], p=r["p_new"], sortie=rel)
    for v, c in out["variants"].items():
        if v != "primary":
            enregistrer(ETUDE, test=f"robustesse_{v}", declare=True, n=c["k"], agent="analyse-principale",
                        n_comparaisons=7, sortie=rel)
    print(json.dumps({"k": primary and primary["k"], "S1": out["S1"]}, indent=0)[:600])


if __name__ == "__main__":
    main()
