#!/usr/bin/env python3
"""evidence/DATA_V2_MANIFEST.tsv : empreintes de data_v2. mk_manifest.py réécrirait RAW_MANIFEST.tsv, qui doit rester tel quel."""
import hashlib
from pathlib import Path

from dmaga.paths import BIG, exige_v2

exige_v2()


def sha(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


n = t = 0
with Path("evidence/DATA_V2_MANIFEST.tsv").open("w") as out:
    out.write("sha256\toctets\tchemin\n")
    for p in sorted(BIG.rglob("*")):
        if p.is_file() and not p.name.startswith("._"):
            s = p.stat().st_size
            out.write(f"{sha(p)}\t{s}\t{p.relative_to(BIG.parent)}\n")
            n += 1
            t += s
print("fichiers", n, "octets", t)
