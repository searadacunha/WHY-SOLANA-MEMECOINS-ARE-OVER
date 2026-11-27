#!/usr/bin/env python3
"""Lit raw/flows/<wallet>/ pour une liste d'adresses et aplatit toutes les lignes (une ligne par transfert) dans audits_work/G/flows_rows.csv.gz, en dédupliquant par signature, instruction, source, destination, mint.
usage : g06_flowsfile.py <fichier de wallets> (une adresse par ligne) ; sinon tous les dossiers de raw/flows sauf ._*.
Colonnes : wallet,query,truncated,sig,bt,from,to,mint,raw,dec. Pas d'agrégat mémoire au-delà d'un set par wallet."""
import csv, gzip, json, os, sys
FL = "/Volumes/VERBATIM HD/Dark-MAGA-Investigation/raw/flows/"
G = "/Volumes/VERBATIM HD/Dark-MAGA-Investigation/audits_work/G/"
ws = [l.strip() for l in open(sys.argv[1]) if l.strip()] if len(sys.argv) > 1 else sorted(d for d in os.listdir(FL) if not d.startswith("._"))
fo = gzip.open(G + "flows_rows.csv.gz", "wt", compresslevel=5, newline=""); w = csv.writer(fo)
w.writerow("wallet query truncated sig bt slot src dst mint raw dec txidx ins inner".split())
n = 0
for a in ws:
    if not os.path.isdir(FL + a): continue
    for q in sorted(os.listdir(FL + a)):
        if q.startswith("._") or not q.endswith(".json.gz") or q.startswith("age"): continue
        d = json.load(gzip.open(FL + a + "/" + q, "rt"))
        for r in d.get("rows") or []:
            w.writerow([a, q[:-8], int(bool(d.get("truncated"))), r["signature"], r["blockTime"], r.get("slot"), r.get("fromUserAccount"), r.get("toUserAccount"), r.get("mint"), r.get("amount"), r.get("decimals"), r.get("transactionIdx"), r.get("instructionIdx"), r.get("innerInstructionIdx")])
            n += 1
fo.close(); print("lignes", n, "wallets", len(ws))
