#!/usr/bin/env python3
"""Dernières corrections de g63_prose.md, d'après g43.txt, g45.txt et g67.txt relus. Chaque remplacement doit trouver exactement une occurrence."""
p = "audits/2026-11-03/work_G/g63_prose.md"
s = open(p, encoding="utf-8").read()
for a, b in [
    ("de 06:05:00 à 06:45:52 environ, 1,22 SOL au total", "de 06:05:00 à 06:55:29, 1,22 SOL au total"),
    ("4 779,4 SOL éq. lus (`g45.txt`)", "6 575,5 SOL éq. lus (`g45.txt`)"),
    ("chacun avec exactement 2 jambes de même quantité à 1 % près et exactement une jambe de tiers entre les deux.", "chacun avec exactement 2 jambes de même quantité à 1 % près et exactement une jambe de tiers entre les deux, à des index distants de 2 dans le bloc (`g67.txt`)."),
]:
    assert s.count(a) == 1, (s.count(a), a)
    s = s.replace(a, b)
open(p, "w", encoding="utf-8").write(s)
print("ok")
