#!/usr/bin/env python3
"""Auditeur A. Registre, gel, synthétique. Lecture seule, n'importe pas registre.py pour ne rien écrire."""
import hashlib, json, os, re
ROOT = "REDACTED_HOME/Projects/Dark-MAGA-Investigation"
E = ROOT + "/etude_final"
lines = open(E + "/registre/tests.jsonl", "rb").read().splitlines()
print("lignes", len(lines))
first = json.loads(lines[0])
print("champs", list(first))
prev = "0" * 64
bad = 0
for i, b in enumerate(lines):
    d = json.loads(b)
    p = d.get("prev") or d.get("empreinte_precedente") or d.get("precedent")
    if p is not None and p != prev:
        bad += 1
    prev = hashlib.sha256(b).hexdigest()
print("chaînage rompu", bad, "(champ lu :", [k for k in first if "prec" in k or "prev" in k], ")")
rows = [json.loads(b) for b in lines]
import collections
print(collections.Counter(d.get("donnees") for d in rows))
print("réelles : scripts, gelé", collections.Counter((d.get("script"), d.get("script_gele", d.get("gele"))) for d in rows if d.get("donnees") == "reelles"))
print("synthétiques : scripts, heure", sorted({(d.get("script"), d.get("t_utc")) for d in rows if d.get("donnees") == "synthetiques"}))
print("n_comparaisons réelles", sum((d.get("n_comparaisons") or 1) for d in rows if d.get("donnees") == "reelles"))
for d in rows[10:12] + rows[-2:]:
    print({k: d[k] for k in d if k not in ("empreintes",)})
lock = json.load(open(E + "/PROTOCOL.lock"))
print("gel", lock["gele_le_utc"], "ajouts", [(a["t_utc"], a["fichiers"]) for a in lock.get("ajouts", [])])
for rel, sha in lock["fichiers"].items():
    h = hashlib.sha256(open(os.path.join(E, rel), "rb").read()).hexdigest()
    if h != sha:
        print("EMPREINTE DIFFERENTE", rel)
print("empreintes du gel relues", len(lock["fichiers"]))
print("références à etude/ dans le code gelé :", [f for f in os.listdir(E + "/code") if f.endswith(".py") and re.search(r"\.\./etude/|/etude/|'etude'", open(E + "/code/" + f).read())])
# un pool synthétique porterait les motifs de ctl_02 : VT, VS, w12, new3, post4
import csv
rows = list(csv.DictReader(open(E + "/derived/metrics.csv")))
print("pools de metrics.csv, longueur min/max", min(len(r["pool"]) for r in rows), max(len(r["pool"]) for r in rows))
base58 = re.compile(r"^[1-9A-HJ-NP-Za-km-z]{32,44}$")
print("pools non base58", [r["pool"] for r in rows if not base58.match(r["pool"])][:3], "mints non base58", [r["mint"] for r in rows if not base58.match(r["mint"])][:3])
print("tests.json k", json.load(open(E + "/tables/tests.json"))["variants"]["primary"]["k"], open(E + "/tables/verdict.json").read())
