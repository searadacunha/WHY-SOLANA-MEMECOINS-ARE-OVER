#!/usr/bin/env python3
"""Refait le test de N01 sur le second dépôt : parmi les destinataires des retraits Coinbase de la fenêtre de 2 h (cb_window.csv de C), combien versent à 9W9b, à Caw4, aux deux, à l'un ou l'autre, et où sont-ils dans le temps. Aucun filtre de montant. Sortie g66.txt."""
import csv, sys, collections
OUT = "audits/2026-11-03/work_G/"
sys.stdout = open(OUT + "g66.txt", "w")
inp = list(csv.DictReader(open(OUT + "g30_in.csv")))
S9 = {r["sender"] for r in inp if r["depot"].startswith("9W9b")}; SC = {r["sender"] for r in inp if r["depot"].startswith("Caw4")}
rows = list(csv.DictReader(open("audits/2026-11-03/work_C/cb_window.csv")))
dest = {r["dest"] for r in rows}
print("retraits", len(rows), "destinataires", len(dest), "de", rows[0]["utc"], "à", rows[-1]["utc"])
print("versent à 9W9b", len(dest & S9), "; à Caw4", len(dest & SC), "; aux deux", len(dest & S9 & SC), "; à l'un ou l'autre", len(dest & (S9 | SC)))
L = [r for r in rows if r["dest"] in (S9 | SC)]
for r in L: print(" ", r["utc"], r["dest"], r["sol"], "9W9b" if r["dest"] in S9 else "-", "Caw4" if r["dest"] in SC else "-")
inside = [r for r in L if "2024-07-14T01:32:20Z" <= r["utc"] <= "2024-07-14T01:40:51Z"]
print("dans la fenêtre 01:32:20 à 01:40:51", len({r["dest"] for r in inside}), "hors fenêtre", sorted({r["dest"] for r in L} - {r["dest"] for r in inside}))
