#!/usr/bin/env python3
"""Historique complet de chaque venue découvert : les swaps directs sur CLMM ou Orca ne référencent ni le mint ni le pool Raydium.

Une tranche par venue, label full_venue/<adresse>, transactions réussies. Résumable. Rejeter un venue sans DMAGA n'a pas lieu
d'être : la liste vient de dis_05_venues.py, donc chacun a au moins un échange DMAGA observé.
"""
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from dmaga.collect import collect, logger
from dmaga.config import MINT
from dmaga.helius import Helius
from dmaga.venues import load

log = logger("col_03_venues")
h = Helius(rps=7, timeout=240)
venues = load()
failures = []
# autorité commune à tous les pools d'un programme : on suit ses seuls comptes DMAGA, jamais son historique entier
SHARED = {"GpMZbSM2GgvTKHJirzeGfMFoaZ8UR2X7F4v8vHTvxFbL"}
targets = {a: venues[a] for a in venues if a not in SHARED}
for a in SHARED & set(venues):
    res = h.call("getTokenAccountsByOwner", [a, {"mint": MINT}, {"encoding": "jsonParsed"}])
    for acc in res["value"]:
        targets[acc["pubkey"]] = venues[a] + "_compte"
    log(f"{a}: {len(res['value'])} compte(s) DMAGA")


def run(a):
    try:
        st = collect(h, f"full_venue/{a}", a, details="full", log=lambda m: None, filters={"status": "succeeded"})
        log(f"OK {a} {targets[a]} n={st['n']} {dict(h.stats)}")
    except Exception as e:  # le curseur reste : la relance reprend
        failures.append(a)
        log(f"ECHEC {a}: {e!r}")


with ThreadPoolExecutor(5) as ex:
    list(ex.map(run, list(targets)))
log(f"FIN venues={len(targets)} echecs={failures}")
sys.exit(1 if failures else 0)
