"""Contrôle final : data_v2 correspond à evidence/DATA_V2_MANIFEST.tsv. Lecture seule."""
import csv, hashlib
from pathlib import Path
EXT = Path("/Volumes/VERBATIM HD/Dark-MAGA-Investigation")
rows = list(csv.DictReader(open("evidence/DATA_V2_MANIFEST.tsv"), delimiter="\t"))
bad = [r["chemin"] for r in rows if hashlib.sha256((EXT / r["chemin"]).read_bytes()).hexdigest() != r["sha256"]]
n = sum(1 for p in (EXT / "data_v2").rglob("*") if p.is_file() and not p.name.startswith("._"))
print("lignes", len(rows), "fichiers sur le disque", n, "non conformes", len(bad), bad[:5])
