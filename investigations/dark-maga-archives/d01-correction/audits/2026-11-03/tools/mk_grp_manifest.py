#!/usr/bin/env python3
"""Empreintes du brut de l'étude de groupe, en flux."""
import hashlib, sys
from pathlib import Path
from dmaga.config import RAW
out = Path(sys.argv[1]); n = t = 0
with out.open("w") as f:
    f.write("sha256\toctets\tchemin\n")
    for p in sorted((RAW / "grp").glob("*.jsonl.gz")):
        if p.name.startswith("._"):
            continue
        h = hashlib.sha256()
        with p.open("rb") as g:
            for b in iter(lambda: g.read(1 << 20), b""):
                h.update(b)
        f.write(f"{h.hexdigest()}\t{p.stat().st_size}\traw/grp/{p.name}\n"); n += 1; t += p.stat().st_size
print(n, "fichiers", round(t / 1e6), "Mo")
