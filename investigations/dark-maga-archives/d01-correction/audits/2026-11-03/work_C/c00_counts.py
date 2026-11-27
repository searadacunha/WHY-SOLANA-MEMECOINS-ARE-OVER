#!/usr/bin/env python3
"""Compte les transactions annoncees par les curseurs de chaque dossier brut, et verifie 'complete'."""
import json
from pathlib import Path
RAW = Path("/Volumes/VERBATIM HD/Dark-MAGA-Investigation/raw")
for name in ["full_curve","full_mint","full_pool","full_venue"]:
    tot=0; inc=[]; ks=set(); filt=set(); addr=set()
    d = RAW/name
    if (d/"cursor.json").exists():
        c=json.loads((d/"cursor.json").read_text()); print(name,"racine",json.dumps(c)[:300])
    for p in sorted(x for x in d.iterdir() if not x.name.startswith("._") and x.is_dir()):
        c=json.loads((p/"cursor.json").read_text())
        tot+=c["n"]; addr.add(c["address"])
        if not c["complete"]: inc.append(p.name)
        filt.add(str(c.get("filters",{}).get("status")))
    print(name,"tx",tot,"incomplets",inc[:5],"status",filt,"adresses",len(addr), list(addr)[:2])
import duckdb
print("duckdb", duckdb.__version__)
