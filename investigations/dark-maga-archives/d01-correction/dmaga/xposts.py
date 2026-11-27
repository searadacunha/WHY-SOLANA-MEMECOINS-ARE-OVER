"""Archive de publications X par identifiant : réponses brutes + une ligne normalisée par post.

Sources publiques, sans compte ni cookie : api.fxtwitter.com (tiers) et le point d'intégration
cdn.syndication.twimg.com. Pas de recherche ni de timeline ici : le découpage en identifiants vient
de la Wayback CDX, des articles et des threads archivés.
Écriture idempotente : un identifiant déjà présent dans x_posts.jsonl n'est pas refait.

usage:
  python -m dmaga.xposts fetch <id> [user] [--source note] [--follow]
  python -m dmaga.xposts cdx <account>        # liste les status archivés par la Wayback
  python -m dmaga.xposts media                # télécharge les médias de x_posts.jsonl avec sha256
"""
import argparse
import hashlib
import json
import math
import re
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

from .config import DATA, EVIDENCE

X_RAW = EVIDENCE / "x_raw"
X_MEDIA = EVIDENCE / "x_media"
POSTS = DATA / "x_posts.jsonl"
UA = {"User-Agent": "Mozilla/5.0 (research archive)"}


def snowflake_utc(i: str) -> str:
    return datetime.fromtimestamp(((int(i) >> 22) + 1288834974657) / 1000, timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _token(i: str) -> str:
    # calcul du jeton de widgets.js, seul prérequis du point d'intégration public
    n = (int(i) / 1e15) * math.pi
    d = "0123456789abcdefghijklmnopqrstuvwxyz"
    ip, fp = int(n), n - int(n)
    s = ""
    while ip:
        s = d[ip % 36] + s
        ip //= 36
    s = (s or "0") + "."
    for _ in range(11):
        fp *= 36
        s += d[int(fp)]
        fp -= int(fp)
    return s.replace("0", "").replace(".", "")


def _get(url: str, timeout=30) -> bytes:
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def _save(i: str, name: str, url: str):
    """Rend (statut, json|None). 404 = tombstone légitime, toute autre erreur est gardée dans `error`."""
    X_RAW.mkdir(parents=True, exist_ok=True)
    try:
        b = _get(url)
    except urllib.error.HTTPError as e:
        return e.code, None
    (X_RAW / f"{i}.{name}.json").write_bytes(b)
    return 200, json.loads(b)


def existing_ids() -> set[str]:
    if not POSTS.exists():
        return set()
    return {json.loads(line)["id"] for line in POSTS.open()}


def fetch(i: str, user: str = "i", source: str = "", follow: bool = False, depth: int = 0) -> dict | None:
    seen = existing_ids()
    if i in seen:
        return None
    fx_code, fx = _save(i, "fx", f"https://api.fxtwitter.com/{user}/status/{i}")
    syn_code, syn = _save(i, "synd", f"https://cdn.syndication.twimg.com/tweet-result?id={i}&token={_token(i)}&lang=en")
    t = (fx or {}).get("tweet") or {}
    synd_ok = bool(syn and syn.get("created_at"))
    media = [m.get("url") for m in (t.get("media") or {}).get("all", [])]
    if synd_ok and not media:
        media = [m.get("media_url_https") for m in syn.get("mediaDetails", []) if m.get("media_url_https")]
    created = None
    if synd_ok:
        created = syn["created_at"].replace(".000Z", "Z")
    elif t.get("created_timestamp"):
        created = datetime.fromtimestamp(t["created_timestamp"], timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    row = {
        "id": i,
        "author": (t.get("author") or {}).get("screen_name") or ((syn or {}).get("user") or {}).get("screen_name") or (user if user != "i" else None),
        "author_name": (t.get("author") or {}).get("name") or ((syn or {}).get("user") or {}).get("name"),
        "created_utc_metadata": created,
        "created_utc_snowflake": snowflake_utc(i),
        "ts_reliability": "metadata+snowflake" if created else "snowflake_only",
        "text": t.get("text") or (syn or {}).get("text"),
        "reply_to_user": t.get("replying_to") or (syn or {}).get("in_reply_to_screen_name"),
        "reply_to_id": t.get("replying_to_status") or (syn or {}).get("in_reply_to_status_id_str"),
        "quote_id": ((t.get("quote") or {}).get("id")) or ((syn or {}).get("quoted_tweet") or {}).get("id_str"),
        "retweets": t.get("retweets"), "likes": t.get("likes"), "replies": t.get("replies"), "views": t.get("views"),
        "media": media,
        "status": "ok" if (t or synd_ok) else "unavailable",
        "fx_http": fx_code, "synd_type": (syn or {}).get("__typename"),
        "source_note": source,
        "provenance": [f"evidence/x_raw/{i}.fx.json" if fx else None, f"evidence/x_raw/{i}.synd.json" if syn else None],
        "fetched_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    POSTS.parent.mkdir(parents=True, exist_ok=True)
    with POSTS.open("a") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")
    if follow and depth < 8:
        for nxt in (row["reply_to_id"], row["quote_id"]):
            if nxt:
                fetch(str(nxt), "i", f"parent-or-quote of {i}", True, depth + 1)
    return row


def cdx(account: str) -> list[dict]:
    """Status archivés par la Wayback pour un compte, twitter.com et x.com."""
    out = {}
    for host in ("twitter.com", "x.com"):
        url = (f"https://web.archive.org/cdx/search/cdx?url={host}/{account}/status/*&output=json"
               "&fl=timestamp,original,statuscode,digest&collapse=urlkey&limit=20000")
        for _ in range(4):
            try:
                rows = json.loads(_get(url, 90) or b"[]")
                break
            except Exception as e:
                last = e
                time.sleep(5)
        else:
            raise RuntimeError(f"CDX {account} {host}: {last!r}")
        for ts, orig, code, dig in rows[1:]:
            m = re.search(r"/status(?:es)?/(\d{10,})", orig)
            if m:
                out.setdefault(m.group(1), {"id": m.group(1), "wayback_ts": ts, "url": orig, "code": code, "digest": dig})
    d = EVIDENCE / "x_cdx"
    d.mkdir(parents=True, exist_ok=True)
    res = sorted(out.values(), key=lambda r: int(r["id"]))
    for r in res:
        r["created_utc_snowflake"] = snowflake_utc(r["id"])
    (d / f"{account}.json").write_text(json.dumps(res, indent=0))
    return res


def media() -> int:
    X_MEDIA.mkdir(parents=True, exist_ok=True)
    n = 0
    for line in POSTS.open():
        r = json.loads(line)
        for u in r.get("media") or []:
            name = f"{r['id']}_{Path(u.split('?')[0]).name}"
            p = X_MEDIA / name
            if p.exists():
                continue
            try:
                b = _get(u, 60)
            except Exception as e:
                print("media échec", r["id"], u, repr(e))
                continue
            p.write_bytes(b)
            n += 1
            print(name, hashlib.sha256(b).hexdigest())
    return n


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["fetch", "cdx", "media"])
    ap.add_argument("arg", nargs="?")
    ap.add_argument("user", nargs="?", default="i")
    ap.add_argument("--source", default="")
    ap.add_argument("--follow", action="store_true")
    a = ap.parse_args()
    if a.cmd == "fetch":
        print(json.dumps(fetch(a.arg, a.user, a.source, a.follow), ensure_ascii=False))
    elif a.cmd == "cdx":
        rows = cdx(a.arg)
        print(a.arg, len(rows), "status archivés")
        for r in rows:
            print(r["id"], r["created_utc_snowflake"], r["wayback_ts"], r["code"], r["url"])
    else:
        print(media(), "médias téléchargés")
