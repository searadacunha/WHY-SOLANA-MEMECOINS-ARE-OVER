#!/usr/bin/env python3
"""Verdict calculé depuis tables/tests.json, texte fixé par le plan. Écrit tables/verdict.json."""
import json
import os
import sys

ETUDE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from metrics import verdict  # noqa: E402

d = json.load(open(os.path.join(ETUDE, "tables", "tests.json")))
if "primary" not in d["variants"]:
    v = "INCONCLUSIF : DMAGA absent de la variante principale"
else:
    p = d["variants"]["primary"]
    v = verdict({m: x["p"] for m, x in p["mesures"].items()}, p["k"])
with open(os.path.join(ETUDE, "tables", "verdict.json"), "w") as f:
    json.dump({"verdict": v}, f, ensure_ascii=False, indent=1)
print(v)
