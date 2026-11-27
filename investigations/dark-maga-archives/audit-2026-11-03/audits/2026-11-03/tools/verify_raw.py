#!/usr/bin/env python3
"""Relit le brut du disque USB contre evidence/RAW_MANIFEST.tsv, en flux, sans rien modifier.
Écrit : rapport JSON (manquants, différents, hors manifeste par dossier) et un manifeste de ce que RAW_MANIFEST exclut (ctrl_tx)."""
import hashlib
import json
import sys
import time
from collections import Counter
from pathlib import Path

EXT = Path("/Volumes/VERBATIM HD/Dark-MAGA-Investigation")
MANIFEST = Path("evidence/RAW_MANIFEST.tsv")
OUT = Path(sys.argv[1])


def sha(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


t0 = time.time()
seen, ok, bad, missing = set(), 0, [], []
octets = 0
with MANIFEST.open() as f:
    next(f)
    for i, line in enumerate(f, 1):
        want, size, rel = line.rstrip("\n").split("\t")
        seen.add(rel)
        p = EXT / rel
        if not p.exists():
            missing.append(rel)
            continue
        got = sha(p)
        octets += int(size)
        if got == want and p.stat().st_size == int(size):
            ok += 1
        else:
            bad.append({"chemin": rel, "attendu": want, "lu": got, "octets_attendus": int(size), "octets_lus": p.stat().st_size})
        if i % 2000 == 0:
            print(f"{i} lus, {octets/1e9:.2f} Go, {time.time()-t0:.0f} s, {len(bad)} différents, {len(missing)} manquants", flush=True)

extras = Counter()
extras_o = Counter()
ctrl = []
for root in ("raw", "data"):
    for p in (EXT / root).rglob("*"):
        if not p.is_file() or p.name.startswith("._"):
            continue
        rel = str(p.relative_to(EXT))
        if rel in seen:
            continue
        top = "/".join(rel.split("/")[:2])
        extras[top] += 1
        extras_o[top] += p.stat().st_size
        if rel.startswith("raw/ctrl_tx/"):
            ctrl.append(rel)
print(f"hors manifeste : {sum(extras.values())} fichiers", flush=True)
with (OUT / "CTRL_TX_MANIFEST.tsv").open("w") as out:
    out.write("sha256\toctets\tchemin\n")
    for i, rel in enumerate(sorted(ctrl), 1):
        p = EXT / rel
        out.write(f"{sha(p)}\t{p.stat().st_size}\t{rel}\n")
        if i % 500 == 0:
            out.flush()
            print(f"ctrl_tx {i}/{len(ctrl)}, {time.time()-t0:.0f} s", flush=True)
rep = {"manifeste_lignes": len(seen), "conformes": ok, "differents": bad, "manquants": missing, "octets_relus": octets,
       "hors_manifeste_fichiers": dict(extras), "hors_manifeste_octets": dict(extras_o), "ctrl_tx_haches": len(ctrl), "duree_s": round(time.time() - t0)}
(OUT / "raw_verify.json").write_text(json.dumps(rep, indent=1, ensure_ascii=False))
print("FINI", {k: (len(v) if isinstance(v, list) else v) for k, v in rep.items() if k not in ("hors_manifeste_fichiers", "hors_manifeste_octets")}, flush=True)
assert ok + len(bad) + len(missing) == len(seen)
