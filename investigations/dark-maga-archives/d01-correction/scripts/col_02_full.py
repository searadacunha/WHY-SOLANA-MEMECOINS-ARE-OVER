#!/usr/bin/env python3
"""Téléchargement complet (transactions réussies) du pool et de la courbe, par tranches de temps.

Les tranches viennent de la liste exacte des signatures (col_01) : une tranche couvre environ
TARGET signatures. Chaque tranche a son propre curseur, donc tout est résumable et parallèle.
Usage : col_02_full.py [--until <unix>] [--since <unix>] [--workers N] [--rps R]
"""
import argparse
import gzip
import json
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from dmaga.collect import collect, logger
from dmaga.config import BONDING_CURVE, MINT, RAW, RAYDIUM_POOL
from dmaga.helius import Helius

TARGET = 40_000  # signatures par tranche, réussies et échouées confondues


def slices_from_sigs(label: str, until: int = 2**40, since: int = 0) -> list[tuple[int, int, int]]:
    """Découpe en tranches [gte, lt) à partir des signatures déjà listées. Rend (gte, lt, n)."""
    d = RAW / label
    st = json.loads((d / "cursor.json").read_text())
    if not st["complete"] and until >= 2**39:
        raise RuntimeError(f"{label} non complet : préciser --until sous la dernière date listée")
    out, n, start, last = [], 0, None, None
    for p in sorted(d.glob("p*.jsonl.gz")):
        with gzip.open(p, "rt") as f:
            for line in f:
                r = json.loads(line)
                bt = r["blockTime"]
                if bt < since:
                    continue
                if bt >= until:  # coupure nette : la dernière tranche finit à until
                    if start is not None:
                        out.append((start, until, n))
                    return out
                if start is None:
                    start = bt
                # coupure aux changements de jour : les tranches restent identiques d'un lancement à l'autre
                if n and bt != last and (n >= TARGET or bt // 86400 != last // 86400):
                    out.append((start, bt, n))
                    start, n = bt, 0
                n += 1
                last = bt
    # liste épuisée avant `until` : la dernière tranche s'arrête à la dernière signature lue. C'est ainsi qu'un trou
    # est apparu le 02/11 (23:36 à minuit le 23/07), repéré par chk_20_vault_chain.py. Toujours relancer ce contrôle.
    out.append((start, last + 1, n))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--since", type=int, default=0)
    ap.add_argument("--until", type=int, default=2**40)
    ap.add_argument("--workers", type=int, default=6)
    ap.add_argument("--rps", type=float, default=6)
    ap.add_argument("--source", choices=["pool", "mint"], default="pool")
    ap.add_argument("--calendar", action="store_true", help="tranches de calendrier, sans relire les signatures")
    a = ap.parse_args()
    h = Helius(rps=a.rps, timeout=240)
    log = logger("col_02_full")
    addr = RAYDIUM_POOL if a.source == "pool" else MINT
    if a.calendar:
        # l'activité retombe vite : 6 h jusqu'au 01/09/2024, puis 1 jour jusqu'au 01/01/2025, puis 7 jours
        cuts, t, end = [], a.since, int(time.time())
        while t < min(a.until, end):
            step = 6 * 3600 if t < 1725148800 else 86400 if t < 1735689600 else 7 * 86400
            cuts.append((t, t + step, 0))
            t += step
    else:
        cuts = [c for c in slices_from_sigs(f"sigs_{a.source}", a.until, a.since) if c[1] > a.since and c[0] < a.until]
    log(f"tranches {a.source}={len(cuts)} signatures={sum(c[2] for c in cuts)}")
    jobs = [("full_curve", BONDING_CURVE, None)] if a.source == "pool" and not a.since else []
    for gte, lt, _ in cuts:
        jobs.append((f"full_{a.source}/t{gte}", addr, {"blockTime": {"gte": gte, "lt": lt}, "status": "succeeded"}))

    failures = []
    done = threading.Semaphore(0)

    def run(job):
        label, addr, flt = job
        st = collect(h, label, addr, details="full", filters=flt, log=lambda m: None)
        return label, st["n"], st["complete"]

    t0 = time.time()
    n_done = n_tx = 0
    with ThreadPoolExecutor(a.workers) as ex:
        futs = {ex.submit(run, j): j for j in jobs}
        for fu in as_completed(futs):
            job = futs[fu]
            try:
                label, n, complete = fu.result()
                n_done += 1
                n_tx += n
                log(f"OK {label} n={n} complete={complete} [{n_done}/{len(jobs)}] total={n_tx} "
                    f"{n_tx / (time.time() - t0):.0f} tx/s {dict(h.stats)}")
            except Exception as e:  # une tranche en échec reste à refaire : son curseur est conservé
                failures.append(job[0])
                log(f"ECHEC {job[0]}: {e!r}")
    log(f"FIN tranches={n_done}/{len(jobs)} echecs={failures} stats={dict(h.stats)}")
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
