#!/usr/bin/env python3
"""Diffusion du visuel : hachages perceptuels des médias archivés, distance à l'image de @ChrisWinig.

Référence : média du post 1815054750775173447. Sortie : data/visual_matches.csv, triée par date du post.
pHash, dHash et hash couleur ; proche = distance pHash <= 12 sur 64 bits (seuil usuel, à relire à l'œil
pour les cas limites). Une image proche prouve une ressemblance visuelle, pas qui l'a créée.
"""
import csv
import json
from pathlib import Path

import imagehash
from PIL import Image

from dmaga.config import DATA, EVIDENCE

REF = "1815054750775173447_GTBerExWkAEFQuT.jpg"
media = EVIDENCE / "x_media"
ref = Image.open(media / REF).convert("RGB")
rp, rd = imagehash.phash(ref), imagehash.dhash(ref)

posts = {}
for line in (DATA / "x_posts.jsonl").open():
    r = json.loads(line)
    posts.setdefault(r["id"], r)

rows, bad = [], 0
for p in sorted(media.iterdir()):
    if p.name.startswith(".") or "_" not in p.name:
        continue
    pid = p.name.split("_")[0]
    try:
        im = Image.open(p).convert("RGB")
    except Exception:  # vidéo, fichier partiel : compté, jamais noté comme non ressemblant
        bad += 1
        continue
    post = posts.get(pid, {})
    rows.append({"post_id": pid, "author": post.get("author"), "created_utc": post.get("created_utc_snowflake"),
                 "file": p.name, "w": im.width, "h": im.height, "phash_dist": imagehash.phash(im) - rp,
                 "dhash_dist": imagehash.dhash(im) - rd, "views": post.get("views"), "likes": post.get("likes"),
                 "reply_to": post.get("reply_to_user"), "text": (post.get("text") or "")[:140].replace("\n", " ")})
rows.sort(key=lambda r: (r["created_utc"] or "9"))
with (DATA / "visual_matches.csv").open("w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0]))
    w.writeheader()
    w.writerows(rows)
near = [r for r in rows if r["phash_dist"] <= 12]
print(f"images={len(rows)} illisibles={bad} proches={len(near)}")
for r in near[:40]:
    print(r["created_utc"], r["author"], r["phash_dist"], r["dhash_dist"], r["post_id"], r["w"], "x", r["h"], "|", r["text"][:70])
