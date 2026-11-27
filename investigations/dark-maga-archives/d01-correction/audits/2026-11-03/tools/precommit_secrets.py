#!/usr/bin/env python3
"""Avant publication : aucune clé, aucun jeton, aucune clé privée dans les fichiers à publier. usage: precommit_secrets.py <fichiers...> (lit la liste sur stdin si vide)"""
import re, sys, hashlib, json
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
sys.argv, av = sys.argv[:1], sys.argv[1:]
from scan_keys import KNOWN, UUID, fp
PAT = {"github": rb"gh[opsu]_[A-Za-z0-9]{20,}", "anthropic_openai": rb"sk-[A-Za-z0-9_\-]{20,}", "aws": rb"AKIA[0-9A-Z]{16}", "pem": rb"-----BEGIN [A-Z ]*PRIVATE KEY", "age": rb"AGE-SECRET-KEY-1", "url_cle": rb"api[-_]?key=[0-9a-f]{8}-", "telegram": rb"\b\d{8,10}:AA[A-Za-z0-9_\-]{30,}"}
files = av or [l.strip() for l in sys.stdin if l.strip()]
bad = 0
for f in files:
    p = Path(f)
    if not p.is_file():
        continue
    b = p.read_bytes()
    for k, r in PAT.items():
        n = len(re.findall(r, b))
        if n:
            print("ALERTE", k, n, f); bad += 1
    for m in UUID.finditer(b):
        if fp(m.group()) in KNOWN:
            print("ALERTE cle connue", fp(m.group())[:8], f); bad += 1
print(f"{len(files)} fichiers, {bad} alertes")
sys.exit(1 if bad else 0)
