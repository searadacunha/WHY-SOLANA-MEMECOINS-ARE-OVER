#!/usr/bin/env python3
"""Affiche le grand livre d'un wallet, sans agrégat lourd. usage: g05_show.py <préfixe> [seuil SOL] [--all]"""
import csv, sys
p = sys.argv[1]; th = float(sys.argv[2]) if len(sys.argv) > 2 else 0.5
for r in csv.DictReader(open("audits/2026-11-03/work_G/g04_ledger.csv")):
    if not r["owner"].startswith(p): continue
    a = float(r["amt"]); t = th if r["asset"] in ("SOL", "WSOL") else (th * 150 if r["asset"] in ("USDC", "USDT") else th * 1e5)
    if a >= t and r["pure"] == "1":
        print(r["owner"][:8], r["dir"], r["asset"], r["cp"], r["label"][:22], "n", r["n"], round(a, 3), r["first"], r["last"][:10], r["sig_ex"][:12])
