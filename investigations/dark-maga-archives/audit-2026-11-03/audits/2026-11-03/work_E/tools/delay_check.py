"""Délai entre l'id d'une image et l'id de son post, sur les posts lus en direct. usage: python3 -I delay_check.py"""
import base64, json, statistics, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import e

REPO = e.W.parent.parent.parent


def mid(u):
    k = u.split("/media/")[1].split(".")[0].split("?")[0]
    return int.from_bytes(base64.urlsafe_b64decode(k + "=" * (-len(k) % 4))[:8], "big")


rows, seen = [], set()
for src in (e.W / "derived/x_posts_new_live_backup.jsonl", REPO / "data/x_posts.jsonl"):
    for l in open(src):
        x = json.loads(l)
        if x["id"] in seen or not x.get("media") or x.get("created_utc_metadata") != x.get("created_utc_snowflake"):
            continue
        seen.add(x["id"])
        u = x["media"][0]
        if u and "/media/" in u:
            d = ((int(x["id"]) >> 22) - (mid(u) >> 22)) / 1000
            if 0 <= d < 3600:
                rows.append(d)
print(len(rows), "médiane", statistics.median(rows), "part sous 2 s", round(sum(1 for d in rows if d < 2) / len(rows), 3))
