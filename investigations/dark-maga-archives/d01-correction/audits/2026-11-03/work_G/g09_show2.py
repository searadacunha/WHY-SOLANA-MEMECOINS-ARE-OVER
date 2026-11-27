#!/usr/bin/env python3
"""Lignes du grand livre, purs et médiés, au-dessus d'un seuil, plus le dernier instant couvert. usage: g09_show2.py <préfixe> <seuil SOL>"""
import csv, sys
p = sys.argv[1]; th = float(sys.argv[2])
for r in csv.DictReader(open("/Volumes/VERBATIM HD/Dark-MAGA-Investigation/audits_work/G/net_stats.csv")):
    if r["owner"].startswith(p): print(r)
rows = [r for r in csv.DictReader(open("audits/2026-11-03/work_G/g04_ledger.csv")) if r["owner"].startswith(p)]
for r in rows:
    a = float(r["amt"]); t = th if r["asset"] in ("SOL", "WSOL") else (th * 150 if r["asset"] in ("USDC", "USDT") else th * 2e5)
    if a >= t:
        print(r["dir"], r["asset"], "pur" if r["pure"] == "1" else "med", r["cp"], r["label"][:18], "n", r["n"], round(a, 2), r["first"][:16], r["last"][:10], r["sig_ex"][:10])
