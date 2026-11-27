#!/usr/bin/env python3
"""Auto-contrôle du livrable : aucune adresse ni signature absente des sorties, aucun tiret long, aucune clé ni URL de clé, colonnes du CSV, crédits sous le plafond. Échoue par assert."""
import csv, glob, os, re
OUT = "audits/2026-11-03/work_G/"
md = open(OUT + "FLOW_BOUNDARIES.md", encoding="utf-8").read()
csvf = open(OUT + "flow_boundaries.csv", encoding="utf-8").read()
for name, s in (("md", md), ("csv", csvf)):
    assert "—" not in s and "–" not in s, name + " : tiret long ou demi-long"
    assert "api-key" not in s and "api_key" not in s, name
corpus = ""
for f in glob.glob(OUT + "*"):
    if f.endswith((".csv", ".txt")) and not f.endswith("flow_boundaries.csv") and not os.path.basename(f).startswith("._"):
        corpus += open(f, encoding="utf-8", errors="replace").read()
tok = set(re.findall(r"\b[1-9A-HJ-NP-Za-km-z]{32,90}\b", md))
missing = [t for t in tok if t not in corpus and t not in csvf]
assert not missing, missing[:10]
hdr = next(csv.reader(open(OUT + "flow_boundaries.csv", encoding="utf-8")))
for c in "wallet_source destination actif montant date_debut date_fin type_frontiere niveau signature_exemple".split(): assert c in hdr, c
r = list(csv.DictReader(open(OUT + "credits.csv")))
tot = sum(int(x["credits"]) for x in r); assert tot <= 5000, tot
sz = sum(os.path.getsize(f) for f in glob.glob(OUT + "*")) / 1e6; assert sz < 100, sz
print("contrôle ok : références", len(tok), "lignes csv", csvf.count("\n") - 1, "crédits", tot, "taille Mo", round(sz, 1))
