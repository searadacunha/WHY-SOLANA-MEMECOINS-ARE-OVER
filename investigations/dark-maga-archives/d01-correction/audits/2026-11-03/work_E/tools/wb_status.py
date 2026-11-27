"""Lit dans la Wayback les captures des status listés par la CDX du dépôt (lecture seule).
usage: python3 -I wb_status.py <compte> <debut_iso> <fin_iso> [--desc] [--max N]
Reprend là où il s'est arrêté : un id déjà sauvegardé n'est pas refait. Une erreur est consignée, jamais prise pour une absence.
"""
import gzip, json, sys, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import e

REPO = e.W.parent.parent.parent
OUT = e.W / "wb_status_recovered.jsonl"
SUB = "wb_status"


def load(n):
    p = REPO / f"evidence/x_cdx/{n}.json.gz"
    return json.load(gzip.open(p)) if p.exists() else json.load(open(REPO / f"evidence/x_cdx/{n}.json"))


def parse(raw):
    d = json.loads(raw)
    x = d.get("data") or {}
    inc = d.get("includes") or {}
    return {"text": x.get("text"), "created_at": x.get("created_at"), "author_id": x.get("author_id"),
            "username": next((u["username"] for u in inc.get("users", []) if u["id"] == x.get("author_id")), None),
            "media": [{k: m.get(k) for k in ("media_key", "type", "url", "width", "height", "preview_image_url")} for m in inc.get("media", [])],
            "refs": x.get("referenced_tweets"), "reply_to_user": x.get("in_reply_to_user_id"),
            "ref_tweets": [{k: t.get(k) for k in ("id", "author_id", "created_at", "text")} for t in inc.get("tweets", []) if t.get("id") != x.get("id")],
            "users": [{k: u.get(k) for k in ("id", "username", "name", "created_at", "description", "public_metrics", "profile_image_url")} for u in inc.get("users", [])]}


def main():
    acc, a, b = sys.argv[1:4]
    desc = "--desc" in sys.argv
    mx = int(sys.argv[sys.argv.index("--max") + 1]) if "--max" in sys.argv else 10**9
    done = {json.loads(l)["id"] for l in OUT.open()} if OUT.exists() else set()
    old = {json.loads(l)["id"] for l in open(REPO / "evidence/x_wayback/recovered.jsonl") if "error" not in json.loads(l)}
    rows = [x for x in load(acc) if a <= x["created_utc_snowflake"] < b and x["id"] not in done and x["id"] not in old and x["code"] in ("-", "200")]
    rows.sort(key=lambda x: x["id"], reverse=desc)
    print(acc, "à lire", len(rows), flush=True)
    fails = rounds = n = 0
    for x in rows[:mx]:
        url = f"https://web.archive.org/web/{x['wayback_ts']}id_/{x['url']}"
        code, body, p, err = e.get(url, SUB, x["id"] + ".raw", timeout=40, note=f"status cdx {acc}")
        if err or code in (429, 503, 502, 504) or code is None:
            fails += 1
            print("échec", x["id"], code, err, flush=True)
            time.sleep(120 if code == 429 else 20)
            if fails >= 8:
                rounds += 1
                fails = 0
                print("pause longue", rounds, flush=True)
                if rounds >= 3:
                    print("arrêt : la Wayback refuse, reprendre plus tard", flush=True)
                    return
                time.sleep(300)
            continue
        fails = 0
        rec = {"id": x["id"], "account_in_url": acc, "url": x["url"], "wayback_ts": x["wayback_ts"], "snowflake": e.sf(x["id"]), "http": code, "file": f"evidence/{SUB}/{x['id']}.raw", "bytes": len(body)}
        try:
            rec.update(parse(body))
        except Exception as ex:
            rec["parse_error"] = f"{type(ex).__name__}: {ex}"
        with OUT.open("a") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
        n += 1
        if n % 50 == 0:
            print("lus", n, x["created_utc_snowflake"], flush=True)
        time.sleep(1.5)
    print("fini", n, flush=True)


if __name__ == "__main__":
    main()
