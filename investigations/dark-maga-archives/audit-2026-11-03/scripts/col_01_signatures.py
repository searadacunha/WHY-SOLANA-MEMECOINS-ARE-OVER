#!/usr/bin/env python3
"""Liste toutes les signatures (réussies et échouées) du mint, de la courbe et du pool.

10 crédits pour 1 000 signatures. Sert d'univers exact et de témoin de complétude pour la collecte
complète par tranches. Résumable : voir dmaga.collect.
"""
import sys
import threading
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from dmaga.collect import collect, logger
from dmaga.config import BONDING_CURVE, MINT, RAYDIUM_POOL
from dmaga.helius import Helius

h = Helius(rps=6)
log = logger("col_01_signatures")
errors = []


def run(label, addr):
    try:
        st = collect(h, label, addr, details="signatures", log=log)
        log(f"FIN {label} n={st['n']} complete={st['complete']}")
    except Exception as e:  # le fil meurt mais l'échec reste visible et le curseur permet la reprise
        errors.append((label, repr(e)))
        log(f"ECHEC {label}: {e!r}")


threads = [threading.Thread(target=run, args=a) for a in
           [("sigs_curve", BONDING_CURVE), ("sigs_pool", RAYDIUM_POOL), ("sigs_mint", MINT)]]
for t in threads:
    t.start()
for t in threads:
    t.join()
log(f"stats {dict(h.stats)} erreurs={errors}")
sys.exit(1 if errors else 0)
