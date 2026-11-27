#!/usr/bin/env python3
"""Auditeur A. Population de départ : transactions du compte de migration, combien portent initialize2, combien sont écartées. En flux, sans importer col_40."""
import collections, gzip, json
from pathlib import Path
RAW = Path("/Volumes/VERBATIM HD/Dark-MAGA-Investigation/raw/ctrl_migrations")
C = Path("/Volumes/VERBATIM HD/Dark-MAGA-Investigation/data/controls")
RAY = "675kPX9MHTjS2zt1qfr1NYHuzeLXfQM9H24wFSUt1Mp8"
AUTH = "5Q544fKrFoe6tsEbD7S8EmxGTJYAKtTVhAW5Q5pge4j1"
WSOL = "So11111111111111111111111111111111111111112"
known = {json.loads(x)["signature"] for x in open(C / "migrations.jsonl")}
c = collections.Counter()
progs = collections.Counter()
ex = []
for p in sorted(RAW.glob("p*.jsonl.gz")):
    with gzip.open(p, "rt") as f:
        for line in f:
            t = json.loads(line)
            c["tx"] += 1
            sig = t["transaction"]["signatures"][0]
            logs = t["meta"].get("logMessages") or []
            init2 = any("initialize2" in l for l in logs)
            top = any(i.get("programId") == RAY for i in t["transaction"]["message"]["instructions"])
            inner = any(i.get("programId") == RAY for g in (t["meta"].get("innerInstructions") or []) for i in g["instructions"])
            held = [b for b in t["meta"].get("postTokenBalances") or [] if b.get("owner") == AUTH]
            c["initialize2"] += init2
            if init2:
                c["init2_top"] += top
                c["init2_inner_seulement"] += (inner and not top)
                c["init2_retenue"] += sig in known
                if sig not in known:
                    c["init2_non_retenue"] += 1
                    if len(ex) < 5:
                        ex.append((sig, t["blockTime"], top, inner, len(held)))
                c[f"init2_wsol_{any(b['mint'] == WSOL for b in held)}"] += 1
            else:
                for i in t["transaction"]["message"]["instructions"]:
                    progs[i.get("programId")] += 1
print(dict(c))
print("exemples non retenus", ex)
print("programmes des transactions sans initialize2", progs.most_common(8))
print("signatures connues absentes du brut", len(known) - c["init2_retenue"])
