"""Contrôle de la lecture « id d'avatar = heure d'envoi » sur toutes les captures API v2 (dépôt + work_E).
Pour chaque compte vu avec deux avatars : l'ancien doit être vu avant l'id du nouveau, et le nouveau après.
usage: python3 -I avatar_control.py   écrit derived/avatar_changes.json
"""
import glob, json, re, sys
from collections import defaultdict
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import e

REPO = e.W.parent.parent.parent
seen = defaultdict(dict)


def add(u, t):
    m = re.search(r"profile_images/(\d+)/", u.get("profile_image_url") or "")
    if m and t:
        d = seen[u["username"]].setdefault(m.group(1), [t, t])
        d[0], d[1] = min(d[0], t), max(d[1], t)


for p in glob.glob(str(REPO / "evidence/x_wayback/*.raw")):
    try:
        d = json.load(open(p))
    except Exception:
        continue
    for u in (d.get("includes") or {}).get("users", []):
        add(u, (d.get("data") or {}).get("created_at"))
for l in open(e.W / "wb_status_recovered.jsonl"):
    x = json.loads(l)
    for u in x.get("users") or []:
        add(u, x.get("created_at"))
ok_after = ko_after = ok_before = ko_before = 0
gaps = []
kos = []
for name, imgs in seen.items():
    items = sorted(imgs.items(), key=lambda kv: int(kv[0]))
    for i, (a, b) in items:
        dt = e.sf(i)
        if dt > a[:19] + "Z":
            ko_after += 1
            kos.append((name, i, dt, a))
        else:
            ok_after += 1
    for (i0, (a0, b0)), (i1, (a1, b1)) in zip(items, items[1:]):
        dt1 = e.sf(i1)
        if b0[:19] + "Z" <= dt1:
            ok_before += 1
        else:
            ko_before += 1
            kos.append((name, "ancien vu après l'id du nouveau", i1, dt1, b0))
print("comptes", len(seen), "| 1re vue après l'id: ok", ok_after, "ko", ko_after, "| ancien vu avant l'id du nouveau: ok", ok_before, "ko", ko_before)
print(kos[:15])
json.dump({k: {i: {"upload": e.sf(i), "first_seen": v[0], "last_seen": v[1]} for i, v in s.items()} for k, s in seen.items()}, open(e.W / "derived/avatar_changes.json", "w"), indent=0)
