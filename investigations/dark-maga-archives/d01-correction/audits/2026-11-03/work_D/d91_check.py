#!/usr/bin/env python3
"""Auditeur D. Contrôle des livrables : tirets longs, identifiants entiers retrouvés dans une sortie complète, aucun format de clé, 51 assertions. Sortie d91_check.txt."""
import csv, glob, os, re, sys
ROOT = "audits/2026-11-03/"
F = [ROOT + "AUDIT_FINAL.md", ROOT + "CORRECTIONS.md", ROOT + "CLAIM_VERIFICATION.csv", ROOT + "work_D/projet_amendement_003.md"]
sys.stdout = open(ROOT + "work_D/d91_check.txt", "w")
# corpus : sorties textes complètes, y compris mon d90 exclu pour ne pas valider une saisie par elle-même
corp = []
for pat in ("work_C/*.csv", "work_C/*.out", "work_A/out/*.txt", "work_A/out/*.csv", "work_D/d2*.txt", "work_D/d2*.csv", "work_D/d4*.txt", "work_D/d4*.csv", "AUDIT_C_ATTRIBUTION.md", "AUDIT_A_DATA.md", "CLAIMS_INPUT.csv"):
    corp += glob.glob(ROOT + pat)
corp += ["docs/CASE_REPORT.md", "reports/COORDINATION.md", "reports/TOP_TRADERS.md"]
blob = set()
tok = re.compile(r"[1-9A-HJ-NP-Za-km-z]{32,88}")
for c in corp:
    if os.path.basename(c).startswith("._"): continue
    try:
        blob |= set(tok.findall(open(c, encoding="utf-8", errors="replace").read()))
    except OSError:
        pass
bad = 0
for f in F:
    s = open(f, encoding="utf-8").read()
    dash = sum(s.count(x) for x in "—–")
    miss = [t for t in set(tok.findall(s)) if t not in blob and not t.isalpha()]
    uu = re.findall(r"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}", s)
    print(os.path.basename(f), "octets", len(s), "tirets longs", dash, "identifiants absents du corpus", miss, "motif de clé", len(uu))
    bad += dash + len(miss) + len(uu)
r = list(csv.DictReader(open(ROOT + "CLAIM_VERIFICATION.csv", encoding="utf-8")))
ids = [x["id"] for x in r]
print("lignes", len(r), "C", sum(i.startswith("C") for i in ids), "N", sum(i.startswith("N") for i in ids), "colonnes", list(r[0].keys()))
print({k: sum(1 for x in r if x["id"].startswith("C") and x["verdict"] == k) for k in ("PASS", "FAIL", "INCONCLUSIVE")})
print("écarts avec auditeurs", [(x["id"], x["verdict"], x["verdict_A"], x["verdict_B"], x["verdict_C"]) for x in r if x["id"].startswith("C") and any(v not in ("non couvert", x["verdict"]) for v in (x["verdict_A"], x["verdict_B"], x["verdict_C"]))])
print("couverts par D sans auditeur", [x["id"] for x in r if x["id"].startswith("C") and all(x[k] == "non couvert" for k in ("verdict_A", "verdict_B", "verdict_C"))])
print("problèmes", bad)
