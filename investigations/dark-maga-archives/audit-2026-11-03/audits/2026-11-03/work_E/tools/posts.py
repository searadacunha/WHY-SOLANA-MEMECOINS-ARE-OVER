"""Archive des posts par id (fxtwitter + syndication), même schéma que data/x_posts.jsonl, écrit dans work_E seulement.
usage: python3 -I posts.py "<source_note>" id id ...   (--nomedia pour ne pas télécharger les images)
"""
import json, math, sys, time
from datetime import datetime, timezone
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import e

REPO = e.W.parent.parent.parent
NEW = e.W / "x_posts_new.jsonl"


def token(i):
    # calcul du jeton de widgets.js, copié de dmaga/xposts.py
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


def main():
    note = sys.argv[1]
    nomedia = "--nomedia" in sys.argv
    ids = [a for a in sys.argv[2:] if a.isdigit()]
    old = {json.loads(l)["id"] for l in open(REPO / "data/x_posts.jsonl")}
    new = {json.loads(l)["id"] for l in NEW.open()} if NEW.exists() else set()
    for i in dict.fromkeys(ids):
        if i in new:
            continue
        cf, bf, pf, ef = e.get(f"https://api.fxtwitter.com/i/status/{i}", "x_raw_new", f"{i}.fx.json", note=note)
        cs, bs, ps, es = e.get(f"https://cdn.syndication.twimg.com/tweet-result?id={i}&token={token(i)}&lang=en", "x_raw_new", f"{i}.synd.json", note=note)
        try:
            fx = json.loads(bf) if bf else {}
        except ValueError:
            fx = {}
        try:
            syn = json.loads(bs) if bs else {}
        except ValueError:
            syn = {}
        t = fx.get("tweet") or {}
        ok = bool(syn.get("created_at"))
        media = [m.get("url") for m in (t.get("media") or {}).get("all", [])]
        if ok and not media:
            media = [m.get("media_url_https") for m in syn.get("mediaDetails", []) if m.get("media_url_https")]
        created = syn["created_at"].replace(".000Z", "Z") if ok else (datetime.fromtimestamp(t["created_timestamp"], timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ") if t.get("created_timestamp") else None)
        row = {"id": i, "author": (t.get("author") or {}).get("screen_name") or (syn.get("user") or {}).get("screen_name"),
               "author_name": (t.get("author") or {}).get("name") or (syn.get("user") or {}).get("name"),
               "created_utc_metadata": created, "created_utc_snowflake": e.sf(i), "ts_reliability": "metadata+snowflake" if created else "snowflake_only",
               "text": t.get("text") or syn.get("text"), "reply_to_user": t.get("replying_to") or syn.get("in_reply_to_screen_name"),
               "reply_to_id": t.get("replying_to_status") or syn.get("in_reply_to_status_id_str"),
               "quote_id": (t.get("quote") or {}).get("id") or (syn.get("quoted_tweet") or {}).get("id_str"),
               "retweets": t.get("retweets"), "likes": t.get("likes"), "replies": t.get("replies"), "views": t.get("views"), "media": media,
               "status": "ok" if (t or ok) else "unavailable", "fx_http": cf, "synd_type": syn.get("__typename"), "source_note": note,
               "provenance": [f"audits/2026-11-03/work_E/evidence/x_raw_new/{i}.fx.json", f"audits/2026-11-03/work_E/evidence/x_raw_new/{i}.synd.json"],
               "fetched_utc": e.now()}
        with NEW.open("a") as f:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
        dims = [(m.get("width"), m.get("height")) for m in (t.get("media") or {}).get("all", [])]
        print(i, row["author"], row["created_utc_snowflake"], row["status"], "OLD" if i in old else "", "rep:", row["reply_to_user"], row["reply_to_id"], "q:", row["quote_id"], dims, repr((row["text"] or "")[:150]))
        if not nomedia:
            for u in media:
                if u and "pbs.twimg.com/media" in u:
                    base = u.split("?")[0]
                    e.get(base + "?name=orig", "x_media_new", f"{i}_{base.rsplit('/', 1)[1]}", note=f"media de {i}")
        time.sleep(0.7)


if __name__ == "__main__":
    main()
