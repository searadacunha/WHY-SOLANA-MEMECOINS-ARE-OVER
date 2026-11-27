"""Outils de collecte en lecture seule : un GET, sauvegarde brute, ligne de manifeste, snowflake.
usage: python3 -I e.py get <url> <sous-dossier> [nom] ; python3 -I e.py sf <id>...
"""
import hashlib, json, re, sys, time, urllib.error, urllib.parse, urllib.request
from datetime import datetime, timezone
from pathlib import Path

W = Path(__file__).resolve().parent.parent
EV = W / "evidence"
MAN = W / "evidence_manifest.jsonl"
UA = {"User-Agent": "Mozilla/5.0 (research archive; read-only)"}


def sf_ms(i) -> datetime:
    return datetime.fromtimestamp(((int(i) >> 22) + 1288834974657) / 1000, timezone.utc)


def sf(i) -> str:
    return sf_ms(i).strftime("%Y-%m-%dT%H:%M:%SZ")


def now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def get(url, sub, name=None, timeout=45, headers=None, note=""):
    """Rend (http, octets, chemin). Toute réponse HTTP, erreur comprise, est sauvegardée et consignée."""
    name = name or re.sub(r"[^A-Za-z0-9._=-]+", "_", url.split("://", 1)[-1])[:150]
    d = EV / sub
    d.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(url, headers={**UA, **(headers or {})})
    code, body, err, ctype = None, b"", None, None
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            code, body, ctype = r.status, r.read(), r.headers.get("content-type")
    except urllib.error.HTTPError as e:
        code, ctype = e.code, e.headers.get("content-type")
        try:
            body = e.read()
        except Exception:
            body = b""
    except Exception as e:
        err = f"{type(e).__name__}: {e}"
    p = d / name
    if err is None:
        p.write_bytes(body)
    rec = {"url": url, "file": str(p.relative_to(W)) if err is None else None, "http": code, "error": err, "content_type": ctype,
           "collected_utc": now(), "sha256": hashlib.sha256(body).hexdigest() if err is None else None, "bytes": len(body), "note": note}
    with MAN.open("a") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    return code, body, p, err


if __name__ == "__main__":
    # auto-contrôle : post et avatar déjà datés par le dépôt
    assert sf("1815054750775173447") == "2024-07-21T16:02:29Z"
    assert sf("1815105297410666496") == "2024-07-21T19:23:20Z"
    if sys.argv[1] == "sf":
        for i in sys.argv[2:]:
            print(i, sf(i))
    elif sys.argv[1] == "get":
        c, b, p, e = get(sys.argv[2], sys.argv[3], sys.argv[4] if len(sys.argv) > 4 else None)
        print(c, len(b), p, e)
        print(b[:1500].decode("utf8", "replace"))
