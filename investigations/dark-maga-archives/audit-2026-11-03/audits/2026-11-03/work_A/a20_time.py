#!/usr/bin/env python3
"""Auditeur A. Exactitude UTC : confronte blockTime brut aux heures écrites dans les fichiers et rapports. Détecte un décalage constant d'une heure."""
import csv, gzip, json, re, statistics, sys, zipfile, io
from datetime import datetime, timezone
from pathlib import Path
import duckdb
A = "/Volumes/VERBATIM HD/Dark-MAGA-Investigation/audits_work/A"
ROOT = Path("REDACTED_HOME/Projects/Dark-MAGA-Investigation")
RAWF = Path("/Volumes/VERBATIM HD/Dark-MAGA-Investigation/raw/flows")
SOLUSD = Path("/Volumes/VERBATIM HD/Dark-MAGA-Investigation/raw/solusd")
con = duckdb.connect(":memory:", config={"memory_limit": "500MB", "threads": 2, "temp_directory": A + "/duck20"})
con.execute("SET TimeZone='UTC'")
u = lambda t: datetime.fromtimestamp(t, timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
SF = lambda i: ((int(i) >> 22) + 1288834974657) / 1000
print("== événements en dur")
for e in json.load(open(ROOT / "data/events.json")):
    m = re.search(r"post (\d{15,})", e["source"]) or re.search(r"image (\d{15,})", e["source"])
    print(e["name"], e["t"], u(e["t"]), "| source:", e["source"][:70], "| snowflake:", (u(int(SF(m.group(1)))) if m else ""))
print("WINIG code", u(1721577749), "AVATAR code", u(1721589800), "snowflake image", SF(1815105297410666496), u(int(SF(1815105297410666496))), "CREATED", u(1720923331), "Butler code", u(1720908660))
print("== premiers acheteurs : EARLY_BUYERS contre slot brut")
con.execute(f"CREATE TEMP TABLE sl AS SELECT slot, min(block_time) a, max(block_time) b FROM read_parquet('{A}/a02_tx.parquet') GROUP BY 1")
n = bad = 0
dd = []
for line in open(ROOT / "reports/EARLY_BUYERS.md"):
    m = re.match(r"\| \d+ \| `(\w+)` \| (\d{9}) \| (\d\d)/(\d\d) (\d\d:\d\d:\d\d) \|", line)
    if not m:
        continue
    slot = int(m.group(2))
    r = con.execute("SELECT a,b FROM sl WHERE slot=?", [slot]).fetchone()
    if not r:
        continue
    t = int(datetime.strptime(f"2024-{m.group(4)}-{m.group(3)} {m.group(5)}", "%Y-%m-%d %H:%M:%S").replace(tzinfo=timezone.utc).timestamp())
    n += 1
    dd.append(t - r[0])
    if t != r[0]:
        bad += 1
print("lignes", n, "écarts", bad, "décalages distincts", sorted(set(dd))[:10])
print("== TIMELINE : lignes avec signature")
txt = (ROOT / "docs/TIMELINE.md").read_text()
for line in txt.splitlines():
    sig = re.search(r"`([1-9A-HJ-NP-Za-km-z]{80,90})`", line)
    d = re.match(r"\| (\d\d)/(\d\d)/(\d{4}) (\d\d:\d\d:\d\d) \|", line)
    if sig and d:
        r = con.execute(f"SELECT any_value(block_time) FROM read_parquet('{A}/a02_tx.parquet') WHERE signature=?", [sig.group(1)]).fetchone()
        print(d.group(0), sig.group(1)[:12], "brut", u(r[0]) if r and r[0] else None)
print("== TIMELINE : capitalisation recalculée (prix du pool juste avant l'instant × 1e9 × SOLUSDT minute)")
px = {}
for z in sorted(SOLUSD.glob("SOLUSDT-1m-2024-*.zip")):
    if z.name.startswith("._"):
        continue
    with zipfile.ZipFile(z) as f, f.open(f.namelist()[0]) as fh:
        for row in csv.reader(io.TextIOWrapper(fh)):
            if row and row[0].isdigit():
                ms = int(row[0])
                px[(ms // 1000 if ms > 10**14 else ms) // 60000] = float(row[4])
con.execute(f"""CREATE TEMP TABLE chain AS SELECT DISTINCT slot, tx_index, block_time t, vt_post, vs_post FROM read_parquet('{A}/a02_tx.parquet') WHERE vt_post IS NOT NULL AND vs_post IS NOT NULL AND vt_post<>vt_pre AND vs_post<>vs_pre AND NOT failed ORDER BY slot, tx_index""")
out = 0
for line in txt.splitlines():
    d = re.match(r"\| (\d\d)/(\d\d)/(\d{4}) (\d\d:\d\d:\d\d) \|.*?\|\s*([\d ,]+) (k|M)\$ \|", line)
    if not d:
        continue
    t = int(datetime.strptime(f"{d.group(3)}-{d.group(2)}-{d.group(1)} {d.group(4)}", "%Y-%m-%d %H:%M:%S").replace(tzinfo=timezone.utc).timestamp())
    r = con.execute("SELECT vt_post, vs_post FROM chain WHERE t<? ORDER BY slot DESC, tx_index DESC LIMIT 1", [t]).fetchone() or con.execute("SELECT vt_post, vs_post FROM chain ORDER BY slot, tx_index LIMIT 1").fetchone()
    cap = (r[1] / 1e9) / (r[0] / 1e6) * 1e9 * px[t // 60]
    rep = float(d.group(5).replace(" ", "").replace(",", ".")) * (1e3 if d.group(6) == "k" else 1e6)
    flag = "" if abs(cap - rep) <= 0.02 * rep else "ECART"
    out += bool(flag)
    print(d.group(1) + "/" + d.group(2), d.group(4), "rapport", rep, "recalcul", round(cap), flag)
print("écarts de capitalisation > 2 %", out)
print("== gestes du jour et autres époques de group_split.json, en UTC")
gs = json.load(open(ROOT / "data/group_split.json"))
print("gestes", [(u(x["t"]), round(x["M"], 2)) for x in gs["gestes_du_jour"]])
g41 = gs["g41"]
print("g41 0,5 SOL", [u(x["t"]) for x in g41["avant_le_mint"] if str(x["sol"]).startswith("0.5")][:3], "...", [u(x["t"]) for x in g41["avant_le_mint"] if str(x["sol"]).startswith("0.5")][-2:], "n", sum(1 for x in g41["avant_le_mint"] if str(x["sol"]).startswith("0.5") and x["t"] < 1720922725))
print("== price_hourly contre la chaîne")
rows = list(csv.DictReader(open(ROOT / "data/price_hourly.csv")))
print("heures", len(rows), "première", rows[0], "dernière", rows[-1])
top = max(rows, key=lambda r: float(r["high_sol"]))
print("sommet csv", top, u(int(top["hour_utc"])))
r = con.execute("SELECT t//3600*3600 h, max((vs_post/1e9)/(vt_post/1e6)) FROM chain WHERE vt_post>0 GROUP BY 1 ORDER BY 2 DESC LIMIT 1").fetchone()
print("sommet propre", r, u(r[0]), "capitalisation SOL", r[1] * 1e9)
print("== autres fichiers : motifs d'heures et signatures sur la même ligne, reports et docs")
hits = 0
checked = 0
for p in list((ROOT / "reports").glob("*.md")) + list((ROOT / "docs").glob("*.md")):
    for line in p.read_text().splitlines():
        for s in re.findall(r"[1-9A-HJ-NP-Za-km-z]{85,90}", line):
            m = re.search(r"(\d\d)/(\d\d)(?:/(\d{4}))? (\d\d:\d\d(?::\d\d)?)", line)
            if not m:
                continue
            r = con.execute(f"SELECT any_value(block_time) FROM read_parquet('{A}/a02_tx.parquet') WHERE signature=?", [s]).fetchone()
            if not (r and r[0]):
                continue
            checked += 1
            hhmm = u(r[0])[11:19]
            if not hhmm.startswith(m.group(4)[:5]):
                hits += 1
                print("  écart?", p.name, s[:12], "ligne", m.group(0), "brut", u(r[0]))
print("signatures contrôlées", checked, "écarts", hits)
