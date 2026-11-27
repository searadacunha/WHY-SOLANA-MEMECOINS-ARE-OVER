#!/usr/bin/env python3
"""Auditeur D. Échantillon des assertions X et sociales relues dans evidence/, pHash écrit à part, C14 au niveau propriétaire, activité horaire du 21/07. Sortie d47_social.txt."""
import csv, json, os, re, sys, time
from pathlib import Path
import duckdb
import numpy as np
from PIL import Image
OUT = "audits/2026-11-03/work_D/"; BIG = "/Volumes/VERBATIM HD/Dark-MAGA-Investigation/data"
sys.stdout = open(OUT + "d47_social.txt", "w")
snow = lambda i: time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(((int(i) >> 22) + 1288834974657) // 1000))
# C03
p = json.load(open("evidence/web/profiles/fx_DarkMagaCoin.json"))
print("C03 profil", {k: v for k, v in (p.get("user") or p).items() if k in ("created_at", "joined", "screen_name")})
txt = open("evidence/web/threadreader_1843704335823454430.txt").read()
i = txt.find("two days"); print("C03 thread", repr(txt[max(0, i - 220):i + 80]) if i >= 0 else "introuvable")
print("C03 mention de mint dans le thread", len(re.findall(r"\bmint\b|\bpump\.fun\b|7D7BRc", txt)))
# C04
wb = sorted(os.listdir("evidence/web/wb_elonmusk"))
print("C04 fichiers archive", len(wb), wb[:6])
print("C04 snowflake avatar", snow(1815105297410666496), "ancien", snow(1780044485541699584))
# C31 pHash propre : réduction à 8x8 de la DCT d'une image 32x32, écrite sans c55
def dct_m(n):
    return np.array([[np.cos((2 * x + 1) * u * np.pi / (2 * n)) for x in range(n)] for u in range(n)])
def ph(path):
    a = np.asarray(Image.open(path).convert("L").resize((32, 32), Image.LANCZOS), dtype=float)
    m = dct_m(32); d = (m @ a @ m.T)[:8, :8].ravel()
    return d > np.median(d[1:])
base = "evidence/x_media/"
w, av, old = ph(base + "1815054750775173447_GTBerExWkAEFQuT.jpg"), ph(base + "profile_new_1815105297410666496.jpg"), ph(base + "profile_old_1780044485541699584.jpg")
print("C31 pHash Winig/avatar", int((w != av).sum()), "Winig/ancien", int((w != old).sum()), "snowflake Winig", snow(1815054750775173447))
vm = list(csv.DictReader(open("data/visual_matches.csv")))
vm.sort(key=lambda r: r["created_utc"])
near = [r for r in vm if r["phash_dist"] not in ("", None) and float(r["phash_dist"]) <= 4]
print("C31 images proches : n", len(vm), "à distance <= 4 :", len(near), "la plus ancienne", near[0]["created_utc"], near[0]["author"], "avant Winig, distance <= 10 :", [(r["created_utc"], r["author"]) for r in vm if r["created_utc"] < "2024-07-21T16:02:29Z" and float(r["phash_dist"] or 99) <= 10][:5])
# C32, C33
rec = [json.loads(l) for l in open("evidence/x_wayback/recovered.jsonl")]
kk = [r for r in rec if r.get("account_in_url") == "kikisknees"]
print("C32 kikisknees récupérés", len(kk), [(r.get("snowflake"), (r.get("text") or "")[:70]) for r in kk if "pfp by me" in (r.get("text") or "")][:2])
print("C32 16:00:08", [(r.get("snowflake"), (r.get("text") or "")[:70], str(r.get("media"))[:40]) for r in kk if "2024-07-21T16:00" in (r.get("snowflake") or "")][:2])
xp = [json.loads(l) for l in open("data/x_posts.jsonl")]
print("x_posts", len(xp), "clés", list(xp[0].keys())[:14])
ac = lambda r: (r.get("author") or r.get("account") or r.get("user") or r.get("screen_name") or "")
tm = lambda r: r.get("created_utc") or r.get("created_at") or r.get("t_utc") or r.get("snowflake") or ""
for a, kw in (("koreanjewcrypto", "DMAGA"), ("kanpai", "DMAGA"), ("DarkMagaCoin", ""), ("pmarca", "")):
    L = sorted((tm(r), (r.get("text") or "")[:60]) for r in xp if ac(r).lower() == a.lower())
    print("C33", a, "n", len(L), L[:2], "mentionne DMAGA", sum(1 for r in xp if ac(r).lower() == a.lower() and "dmaga" in (r.get("text") or "").lower()))
print("IMG_5658", [r.get("post_id") or r.get("id") for r in xp if "IMG_5658" in json.dumps(r)][:3], snow(1815130791208530273))
# C22 : adresses base58 dans les posts du noyau
core = {"darkmagacoin", "kikisknees", "aristos_revenge", "chriswinig"}
b58 = re.compile(r"\b[1-9A-HJ-NP-Za-km-z]{32,44}\b")
seen = {}
for r in xp:
    if ac(r).lower() in core:
        for m in b58.findall(r.get("text") or ""):
            seen.setdefault(m, []).append(ac(r))
print("C22 adresses publiées par le noyau", {k: sorted(set(v)) for k, v in seen.items()})
# C14 niveau propriétaire, activité horaire
con = duckdb.connect(":memory:", config={"memory_limit": "300MB", "threads": 1}); T0 = 1720922725
G = json.load(open("data/prevent_groups.json"))[0]["members"]
L = ",".join(repr(x) for x in G)
print("C14", con.execute(f"SELECT count(DISTINCT owner),round(sum(token_delta)/1e12,2),round(sum(-sol_lamports)/1e9,2) FROM read_parquet('{BIG}/trades.parquet') WHERE kind='swap' AND token_delta>0 AND block_time<{T0+3600} AND owner IN ({L})").fetchone())
act = next(json.loads(l) for l in open(BIG + "/controls/activity.jsonl") if '"CRSwXnfF21yHDXdYBVWwCwQ5Ni2A4QuK3qGYis5k7x7k"' in l)
H = dict((a, b) for a, b in act["hist"])
print("B-06 activité 21/07 par heure", [(h, H.get((1721520000 + h * 3600) // 3600)) for h in range(9, 21)])
med = sorted(H.get((1721520000 + 14 * 3600) // 3600 - k, 0) for k in range(1, 73))[36]
print("  médiane 72 h avant 14:00", med, "plancher 5, ratio", H.get((1721520000 + 14 * 3600) // 3600) / max(med, 5))
