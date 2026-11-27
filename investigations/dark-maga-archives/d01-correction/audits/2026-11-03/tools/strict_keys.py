#!/usr/bin/env python3
"""Deuxième passe : dans les fichiers déjà signalés, ne garde que les UUID en position de clé Helius (URL helius ou variable HELIUS).
Écrit emp8, classe et fichier ; aucune valeur. usage: strict_keys.py <key_hits_files.tsv> <sortie.tsv>"""
import csv
import os
import re
import sys
from pathlib import Path

sys.argv, argv = [sys.argv[0]], sys.argv
sys.path.insert(0, str(Path(__file__).parent))
from scan_keys import KNOWN, fp

HOME = str(Path.home())
STRICT = re.compile(rb"(?:helius(?:-rpc)?[^\s\"'\\]{0,60}api[-_]?key=|helius[a-z_]{0,20}(?:api[-_]?keys?)?[\s\"'\\]{0,6}[=:][\s\"'\\]{0,6})([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})", re.I)
files = sorted({r["emplacement"] for r in csv.DictReader(open(argv[1]), delimiter="\t") if "!" not in r["emplacement"]})
with open(argv[2], "w") as out:
    out.write("emp8\tclasse\tfichier\tnb\n")
    for name in files:
        p = Path(name.replace("~", HOME, 1))
        c = {}
        with p.open("rb") as f:
            tail = b""
            while b := f.read(8 << 20):
                buf = tail + b
                for m in STRICT.finditer(buf):
                    k = fp(m.group(1))
                    c[k] = c.get(k, 0) + 1
                tail = buf[-200:]
        for k, n in c.items():
            out.write(f"{k[:8]}\t{KNOWN.get(k, 'inconnue')}\t{name}\t{n}\n")
