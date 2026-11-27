#!/usr/bin/env python3
"""Un seul calcul lourd à la fois pour tous les auditeurs : verrou fcntl, puis chien de garde du projet.
usage: python3 audits/2026-11-03/tools/heavy.py [--rss-mo 1000] -- scripts/py.sh mon_script.py ...   (depuis la racine du dépôt)
"""
import fcntl
import os
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
lock = open(ROOT / "audits/2026-11-03/tools/.heavy.lock", "w")
t0 = time.time()
fcntl.flock(lock, fcntl.LOCK_EX)
waited = time.time() - t0
if waited > 1:
    print(f"verrou obtenu après {waited:.0f} s", file=sys.stderr, flush=True)
guard = str(ROOT / "scripts/guard.py")
os.set_inheritable(lock.fileno(), True)  # le verrou vit tant que guard et le calcul vivent
os.execv(sys.executable, [sys.executable, guard, *sys.argv[1:]])
