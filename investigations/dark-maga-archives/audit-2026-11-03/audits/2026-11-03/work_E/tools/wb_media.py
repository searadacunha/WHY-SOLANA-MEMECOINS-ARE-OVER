"""CDX puis lecture Wayback des médias perdus, clé par clé. usage: python3 -I wb_media.py clé [clé...]"""
import json, sys, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import e

for k in sys.argv[1:]:
    p = e.EV / "wb_cdx" / f"cdx_media_{k}.json"
    if p.exists() and p.read_bytes()[:1] == b"[" and p.stat().st_size > 5:
        body = p.read_bytes()
        code = 200
    else:
        code, body, _, err = e.get(f"https://web.archive.org/cdx/search/cdx?url=pbs.twimg.com/media/{k}*&output=json&limit=10", "wb_cdx", f"cdx_media_{k}.json", note="CDX média")
        if err or code != 200:
            print(k, "CDX échec", code, err)
            time.sleep(30)
            continue
    rows = json.loads(body or b"[]")[1:]
    print(k, "captures", len(rows), [r[1] for r in rows][:5])
    done = False
    for r in rows:
        if r[4] != "200" and r[3].startswith("warc"):
            continue
        url = f"https://web.archive.org/web/{r[1]}id_/{r[2]}"
        ext = "png" if "png" in r[2] else "jpg"
        code, b, pth, err = e.get(url, "x_media_wb_new", f"{k}_{r[1]}.{ext}", note=f"média perdu {k}, capture Wayback {r[1]}")
        print("  ", r[1], r[2], r[4], code, len(b), err)
        if code == 200 and not err and b[:2] in (b"\xff\xd8", b"\x89P"):
            done = True
            break
        time.sleep(4)
    time.sleep(3)
