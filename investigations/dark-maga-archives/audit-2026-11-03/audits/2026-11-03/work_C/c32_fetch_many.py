#!/usr/bin/env python3
"""Telecharge l'historique complet (plafond 12 pages de 100, ordre chronologique) d'une liste de wallets. Reprend les curseurs. Sortie: audits_work/C/net/<wallet>.jsonl.gz.
Arrete si credits >= 16000."""
import csv, json, sys, importlib.util
from pathlib import Path
from dmaga.helius import Helius
W=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('c03',W/'c03_net.py'); c03=importlib.util.module_from_spec(spec); spec.loader.exec_module(c03)
addrs=[l.strip() for l in open(sys.argv[1]) if l.strip()]
h=Helius()
for i,a in enumerate(addrs):
    if c03.used()>=16000:
        print('plafond credits atteint',i); break
    c03.full(h,a,12)
print('fin',len(addrs),c03.used(),dict(h.stats))
