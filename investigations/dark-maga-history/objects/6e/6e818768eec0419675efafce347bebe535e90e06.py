"""Archive des posts X du mémo historique (A1-A12, B), hors du corpus x_posts.jsonl qui reste à 5 155 lignes.

Mêmes sources publiques que dmaga.xposts (api.fxtwitter.com, cdn.syndication.twimg.com), sans compte. Pour chaque ID demandé :
l'ID et l'auteur de l'objet RENVOYÉ sont gardés séparément ; un ID renvoyé différent signale un repost (l'API rend l'original).
usage: h20_xfetch.py [id ...] (sans argument : la liste IDS). Sortie : evidence/x_hist/*.json, data/x_hist_posts.jsonl."""
import json
import sys
import time
import urllib.error
from h_lib import DATA, EVID
from dmaga.xposts import _get, _token, snowflake_utc

IDS = {
    "1815291249102119198": "A3 JeffroBTC", "1815372294426124565": "A4 Noah_nftn", "1815106321810919673": "A2 AutismCapital",
    "1815332020765049139": "A5 Orkusx", "1815778958337602027": "A6 JLKHatesYou", "1815088124193579253": "A7 dissident42069",
    "1815088727250858444": "A7 contexte", "1815627489802387584": "A8 bossiethetroll", "1815423397532454959": "A8 campagne",
    "1812482060818186492": "A9 CristusVictor original", "1812491802844471629": "A9 kanpai citation",
    "1842790031007920519": "A10 DarkMagaCoin octobre", "1818184433498755544": "A11 toupaiwang", "1797198462930317356": "A12 CryptoGirlAnna",
    "1815095993186328850": "B2 Bitcoin_is_king", "1815481336528032232": "B4 rushgrowth", "1815187430926139641": "_wmoon DARKMUSK",
    "1814763940410499481": "A1 original pmarca", "1813086353741230327": "A1 original kanpai 16/07", "1812984492157771825": "A1 original kanpai 15/07",
    "1814920352134537332": "original de 1815004677160776126 (TIMELINE)", "1815107549903135205": "original de 1815107774113587625 (TIMELINE)",
    "1814738306589917312": "kikisknees cité par pmarca",
}
OUT = EVID / "x_hist"


def get(i, name, url):
    try:
        b = _get(url)
    except urllib.error.HTTPError as e:
        return e.code, None
    (OUT / f"{i}.{name}.json").write_bytes(b)
    return 200, json.loads(b)


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    ids = sys.argv[1:] or list(IDS)
    rows = {}
    path = DATA / "x_hist_posts.jsonl"
    if path.exists():
        rows = {json.loads(l)["requested_id"]: json.loads(l) for l in path.open()}
    for i in ids:
        if i in rows:
            continue
        fc, fx = get(i, "fx", f"https://api.fxtwitter.com/i/status/{i}")
        sc, sy = get(i, "synd", f"https://cdn.syndication.twimg.com/tweet-result?id={i}&token={_token(i)}&lang=en")
        t = (fx or {}).get("tweet") or {}
        sy = sy if (sy and sy.get("created_at")) else {}
        ret = {x for x in (t.get("id"), sy.get("id_str")) if x}
        rows[i] = {
            "requested_id": i, "why": IDS.get(i, ""), "requested_snowflake_utc": snowflake_utc(i),
            "returned_ids": sorted(ret), "relation": "unavailable" if not ret else ("self" if ret == {i} else "repost_resolved_to_original"),
            "author": (t.get("author") or {}).get("screen_name") or (sy.get("user") or {}).get("screen_name"),
            "author_id": (t.get("author") or {}).get("id") or (sy.get("user") or {}).get("id_str"),
            "created_utc_metadata": sy.get("created_at", "").replace(".000Z", "Z") or None,
            "text": t.get("text") or sy.get("text"),
            "reply_to_id": t.get("replying_to_status") or sy.get("in_reply_to_status_id_str"),
            "quote_id": (t.get("quote") or {}).get("id") or (sy.get("quoted_tweet") or {}).get("id_str"),
            "media": [m.get("url") for m in (t.get("media") or {}).get("all", [])] or [m.get("media_url_https") for m in sy.get("mediaDetails", [])],
            "fx_http": fc, "synd_http": sc, "fetched_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        }
        print(i, rows[i]["relation"], rows[i]["author"], rows[i]["created_utc_metadata"], flush=True)
        time.sleep(1)
    path.write_text("".join(json.dumps(rows[k], ensure_ascii=False) + "\n" for k in sorted(rows)))
