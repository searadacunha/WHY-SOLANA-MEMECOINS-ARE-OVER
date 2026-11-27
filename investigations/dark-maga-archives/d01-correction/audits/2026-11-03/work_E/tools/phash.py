"""pHash/dHash des médias de work_E contre l'avatar de Musk et l'image de @ChrisWinig (même méthode que scripts/ana_40_visual.py).
usage: /opt/homebrew/bin/python3.12 -I phash.py    écrit derived/visual_new.csv
"""
import csv, json, sys
from pathlib import Path
sys.path.insert(0, "/Volumes/VERBATIM HD/Dark-MAGA-Investigation/pylib")
import imagehash
from PIL import Image

W = Path(__file__).resolve().parent.parent
REPO = W.parent.parent.parent
REFS = {"winig": REPO / "evidence/x_media/1815054750775173447_GTBerExWkAEFQuT.jpg", "avatar": REPO / "evidence/x_media/profile_new_1815105297410666496.jpg"}
refs = {k: imagehash.phash(Image.open(p).convert("RGB")) for k, p in REFS.items()}
refd = {k: imagehash.dhash(Image.open(p).convert("RGB")) for k, p in REFS.items()}
assert refs["winig"] - refs["avatar"] == 0  # contrôle : le dépôt rapporte une distance pHash de 0 entre ces deux images
posts = {json.loads(l)["id"]: json.loads(l) for l in open(W / "x_posts_new.jsonl")}
rows = []
for p in sorted((W / "evidence/x_media_new").iterdir()):
    pid = p.name.split("_")[0]
    try:
        im = Image.open(p).convert("RGB")
    except Exception as ex:
        rows.append({"post_id": pid, "file": p.name, "note": f"illisible {type(ex).__name__}"})
        continue
    h, d = imagehash.phash(im), imagehash.dhash(im)
    x = posts.get(pid, {})
    rows.append({"post_id": pid, "author": x.get("author"), "created_utc": x.get("created_utc_snowflake"), "reply_to": x.get("reply_to_user"), "file": p.name, "w": im.width, "h": im.height,
                 "phash_winig": h - refs["winig"], "phash_avatar": h - refs["avatar"], "dhash_avatar": d - refd["avatar"], "text": (x.get("text") or "")[:80].replace("\n", " "), "note": ""})
rows.sort(key=lambda r: r.get("created_utc") or "9")
with open(W / "derived/visual_new.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["post_id", "author", "created_utc", "reply_to", "file", "w", "h", "phash_winig", "phash_avatar", "dhash_avatar", "text", "note"])
    w.writeheader()
    w.writerows(rows)
for r in rows:
    if r.get("phash_avatar") is not None and r["phash_avatar"] <= 16:
        print(r["created_utc"], r["author"], r["post_id"], f'{r["w"]}x{r["h"]}', "pH", r["phash_avatar"], "dH", r["dhash_avatar"], "|", r["text"][:60])
print("images", len(rows))
