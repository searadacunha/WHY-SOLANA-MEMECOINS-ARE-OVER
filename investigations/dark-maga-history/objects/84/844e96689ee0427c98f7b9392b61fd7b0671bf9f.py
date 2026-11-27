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
from dmaga.helius import Helius
from dmaga.venues import load

log = logger("col_03_venues")
h = Helius(rps=7, timeout=240)
venues = load()
failures = []


def run(a):
    try:
        st = collect(h, f"full_venue/{a}", a, details="full", log=lambda m: None, filters={"status": "succeeded"})
        log(f"OK {a} {venues[a]} n={st['n']} {dict(h.stats)}")
    except Exception as e:  # le curseur reste : la relance reprend
        failures.append(a)
        log(f"ECHEC {a}: {e!r}")


with ThreadPoolExecutor(5) as ex:
    list(ex.map(run, list(venues)))
log(f"FIN venues={len(venues)} echecs={failures}")
sys.exit(1 if failures else 0)
