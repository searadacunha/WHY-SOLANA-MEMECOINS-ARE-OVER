#!/usr/bin/env python3
"""Manifestes : evidence/MANIFEST.sha256 (preuves légères) et evidence/RAW_MANIFEST.tsv (brut et gros parquet sur le disque USB)."""
import hashlib
from pathlib import Path

from dmaga.config import BIG, RAW


def sha(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


ev = Path("evidence")
with (ev / "MANIFEST.sha256").open("w") as out:
    n = 0
    for p in sorted(ev.rglob("*")):
        if p.is_file() and p.name not in ("MANIFEST.sha256", "RAW_MANIFEST.tsv") and not p.name.startswith("."):
            out.write(f"{sha(p)}  {p}\n")
            n += 1
print("preuves", n)
with (ev / "RAW_MANIFEST.tsv").open("w") as out:
    out.write("sha256\toctets\tchemin\n")
    n = t = 0
    for root in (BIG, RAW):
        for p in sorted(root.rglob("*")):
            if p.is_file() and not p.name.startswith("._") and p.suffix in (".gz", ".parquet", ".jsonl", ".zip", ".csv", ".json") and "ctrl_tx" not in str(p):
                s = p.stat().st_size
                out.write(f"{sha(p)}\t{s}\t{p.relative_to(root.parent)}\n")
                n += 1
                t += s
print("brut", n, "fichiers", round(t / 1e9, 2), "Go")
