#!/usr/bin/env python3
"""Regarde la forme du brut : une transaction du mint, les curseurs, une ligne de flows."""
import gzip, json, sys
from pathlib import Path
RAW = Path("/Volumes/VERBATIM HD/Dark-MAGA-Investigation/raw")
d = sorted(p for p in (RAW/"full_mint").iterdir() if not p.name.startswith("._"))
print("full_mint fenetres", len(d), d[0].name, d[-1].name)
print((d[0]/"cursor.json").read_text())
with gzip.open(d[0]/"p000000.jsonl.gz","rt") as f:
    tx = json.loads(f.readline())
s = json.dumps(tx)
print("cles", list(tx.keys()), "taille", len(s))
print(s[:3500])
w = RAW/"flows"/"5QhJJcFZu2ashyKyWSTGHcsyo6ZBCbpVuJqeutvQHScd"
for n in ["first_in","in_before","sol_out_after","dmaga_all","age","usdc_out_after"]:
    j = json.load(gzip.open(w/f"{n}.json.gz","rt"))
    if "rows" in j:
        print(n, j["cfg"], j["truncated"], len(j["rows"]))
        if j["rows"]: print(json.dumps(j["rows"][0])[:800])
    else:
        print(n, json.dumps(j)[:500])
