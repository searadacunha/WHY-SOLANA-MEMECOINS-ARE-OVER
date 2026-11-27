"""Livrable : lignes de evidence/RAW_MANIFEST.tsv non conformes. Empreinte complète pour data/, taille seule pour raw/ (91 Go, mécanique). Lecture seule."""
import csv
import hashlib
from pathlib import Path

EXT = Path("/Volumes/VERBATIM HD/Dark-MAGA-Investigation")


def sha(p):
    h = hashlib.sha256()
    with p.open("rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


rows = list(csv.DictReader(open("evidence/RAW_MANIFEST.tsv"), delimiter="\t"))
bad, n_data, n_raw, n_racine, ok_racine = [], 0, 0, 0, 0
for r in rows:
    p = EXT / r["chemin"]
    if not p.exists():
        bad.append(("absent", r["chemin"]))
    elif p.stat().st_size != int(r["octets"]):
        bad.append(("taille", r["chemin"], p.stat().st_size, r["octets"]))
    elif r["chemin"].startswith("data/"):
        n_data += 1
        conforme = sha(p) == r["sha256"]
        if r["chemin"].count("/") == 1 and r["chemin"].endswith(".parquet"):
            n_racine += 1
            ok_racine += conforme
        if not conforme:
            bad.append(("empreinte", r["chemin"]))
    else:
        n_raw += 1
print(f"manifeste : {len(rows)} lignes ; data/ avec empreinte : {n_data} ; raw/ en taille seule : {n_raw} ; data/*.parquet à la racine : {ok_racine} sur {n_racine} conformes")
print(f"non conformes : {len(bad)}")
for b in bad[:30]:
    print(" ", b)
racine = sorted(p.name for p in (EXT / "data").glob("*") if not p.name.startswith("._"))
print("data/ à la racine :", racine)
