import csv, gzip, io, itertools, json, os, re, time, zipfile
from collections import Counter
from pathlib import Path
import duckdb
os.environ["TZ"] = "UTC"; time.tzset()
A = Path("audits/2026-11-03"); B = Path("/Volumes/VERBATIM HD/Dark-MAGA-Investigation/data_v2"); RAW = Path("/Volumes/VERBATIM HD/Dark-MAGA-Investigation/raw")
con = duckdb.connect(":memory:", config={"memory_limit": "700MB", "threads": 2, "temp_directory": "/Volumes/VERBATIM HD/Dark-MAGA-Investigation/audits_work/H"})
con.execute("SET TimeZone='UTC'")
O = list(csv.DictReader(open(A / "work_G/g43_orders.csv")))
tot = sum(float(r["usd_sortis"]) for r in O); gap = tot - 1018687.18
print("écart", round(gap, 2))
small = [(float(r["usd_sortis"]), r["utc"], r["wallet"][:8]) for r in O if float(r["usd_sortis"]) <= gap + 0.05]
hit = []
for k in range(1, 7):
    for c in itertools.combinations(small, k):
        if abs(sum(x[0] for x in c) - gap) < 0.03:
            hit.append(c)
    if hit: break
print("sous-ensembles", len(small), hit[:3])
for p in sorted((A / "work_G").glob("*.txt")):
    t = p.read_text(errors="ignore")
    for m in re.finditer(r"1[ ,]?01[0-9][ ,.]?[0-9]{3}[.,][0-9]+", t):
        print(p.name, m.group(0))
print("ponts Essentiel : g33_bridge", list(csv.DictReader(open(A / "work_G/g33_bridge.csv")))[0].keys() if (A / "work_G/g33_bridge.csv").exists() else None)
AR = "ARu4n5mFdZogZAravu7CcizaojWnS6oqka37gdLT5SZn"
j = json.load(gzip.open(RAW / "flows" / AR / "dmaga_all.json.gz")); print("ARu4 dmaga_all tronqué", j["truncated"], len(j["rows"]))
WP = f"read_parquet('{B}/wallets.parquet')"; ND = f"read_parquet('{B}/nodes.parquet')"
print("ARu4 noeud", con.execute(f"SELECT kind,label,n_counterparts,n_tx FROM {ND} WHERE address='{AR}'").fetchall())
tr = []
for d in (RAW / "flows").iterdir():
    if d.is_dir() and not d.name.startswith("._") and (d / "dmaga_all.json.gz").exists():
        if json.load(gzip.open(d / "dmaga_all.json.gz"))["truncated"] is True: tr.append(d.name)
print("tronqués", len(tr), con.execute(f"SELECT count(*), sum(residual_qty)/1e6 FROM {WP} WHERE owner IN ({','.join(repr(x) for x in tr)})").fetchall(), con.execute(f"SELECT substr(owner,1,8), residual_qty/1e6 FROM {WP} WHERE owner IN ({','.join(repr(x) for x in tr)}) ORDER BY 2 DESC LIMIT 5").fetchall())
ex = json.load(open(B / "exit_summary.json"))
for n, a in (("H3", "H3QsBrrivimFJmSpTXuvig2n1Bh7JuYxrriRSEszT6cc"), ("GX", "GXZvXsD6hxaLeFvQisWpdAwsayJxga7w9EeafhFZG2Ra"), ("P9", "9PrmF8sfoD2YShtWUghrGEYgxwabpnzog8gT1V6LEtdq"), ("Q", "5QhJJcFZu2ashyKyWSTGHcsyo6ZBCbpVuJqeutvQHScd")):
    print(n, {k: round(v, 1) for k, v in sorted(ex.get(a, {}).get("frontieres", {}).items(), key=lambda kv: -kv[1])[:6]}, ex.get(a, {}).get("tronque"))
print("# top traders contre wallets")
txt = Path("reports/TOP_TRADERS.md").read_text()
sec = txt.split("## 100 plus gros réalisés")[1].split("## Plus gros vendeurs")[0]
num = lambda s: float(s.replace(" ", "").replace("\xa0", "").replace(" ", "").replace(",", "."))
rows = re.findall(r"^\| (\d+) \| `(\w+)` \| ([^|]+) \| ([^|]+) \| ([^|]+) \| ([^|]+) \| ([^|]+) \|", sec, re.M)
W = {r[0]: r[1:] for r in con.execute(f"SELECT owner, realized_sol, net_sol_all, bought_sol, sold_sol, proceeds_usd-cost_usd FROM {WP}").fetchall()}
bad = [r[1][:8] for r in rows if any(abs(num(r[i + 2]) - W[r[1]][i]) > tol for i, tol in ((0, 0.06), (1, 0.06), (2, 0.006), (3, 0.06), (4, 0.6)))]
print("lignes", len(rows), "écarts", bad[:10])
sec2 = txt.split("## 100 plus gros acheteurs")[1].split("## Écartés")[0]
rows2 = re.findall(r"^\| (\d+) \| `(\w+)` \| ([^|]+) \|", sec2, re.M)
print("acheteurs", len(rows2), "rang 100", rows2[-1][2] if rows2 else None)
bt = {r[0] for r in con.execute(f"SELECT owner FROM read_parquet('{B}/bots.parquet') WHERE bot_aller_retour").fetchall()}
print("bots dans classement", [r[1][:8] for r in rows2 if r[1] in bt], "AojsMucu dedans", any(r[1].startswith(("AojsMucu", "AzWs3s1W")) for r in rows2), "dans EARLY", sum(x in Path("reports/EARLY_BUYERS.md").read_text() for x in ("AojsMucu", "AzWs3s1W")))
ven = list(json.load(open("reports/data_checks/venues.json"))) + ["5Q544fKrFoe6tsEbD7S8EmxGTJYAKtTVhAW5Q5pge4j1", "87g44hEXP7R8ZxoAJtz941tsVftpEXC1LqAFTf2ZHtkH", "39azUYFWPz3VHgKCf3VChUwbpURdCHRxjWVowf5jUJjg"]
print("en-tête top", con.execute(f"SELECT count(*), sum(bought_sol), sum(sold_sol), sum(realized_sol) FROM {WP} WHERE owner NOT IN ({','.join(repr(x) for x in ven)}) AND owner NOT IN (SELECT address FROM {ND} WHERE kind IN ('router','venue','cex','service'))").fetchall())
print("# scénarios d11", [(r["scenario"], r["detection_pct"]) for r in csv.DictReader(open(A / "work_D/d11_scenarios.csv"))])
print("# visuel")
for r in csv.DictReader(open(A / "work_E/derived/visual_new.csv")):
    if r["post_id"] in ("1815006501896872388", "1815054374982324401", "1815054750775173447", "1815053713330876681", "1813310692243480937", "1815096055337496944", "1814063148917256375"):
        print(r["post_id"], r["author"], r["created_utc"], r["w"], r["h"], r["phash_avatar"], r["dhash_avatar"], r["note"][:60])
print("recoup fichier 18:46:37", [str(p.name) for p in Path("audits/2026-11-03/work_E/evidence").rglob("*1815096055337496944*")][:4], [p.name for p in Path("evidence").rglob("*1815096055337496944*")][:4])
print("post 18:46:37", [json.loads(l).get("media") or json.loads(l).get("note") for l in open(A / "work_E/x_posts_new.jsonl") if '"1815096055337496944"' in l][:2])
print("# selection, chaînes, Dune")
print("selection", sum(1 for _ in open("etude_final/derived/selection.jsonl")) if Path("etude_final/derived/selection.jsonl").exists() else "absent")
vc = list(csv.DictReader(open("reports/data_checks/venue_chain.csv")))
for c_ in ("DMAGA", "WSOL"):
    x = [r for r in vc if r["cote"] == c_]; print(c_, len(x), sum(int(r["n_tx"]) for r in x), sum(int(r["ruptures"]) for r in x), round(sum(float(r["manquants"]) for r in x), 2))
print(json.load(open("reports/data_checks/vault_chain.json")))
t = Path("evidence/labels/dune_cex_solana_addresses.sql").read_text(); a = re.findall(r"[1-9A-HJ-NP-Za-km-z]{32,44}", t); print("Dune occurrences", len(a), "uniques", len(set(a)), Counter(a).most_common(2))
print("# frise, capitalisations")
VD, VS = "5HuEsLbebeuottMsFW3hHcXTrKVsu3WUNSQnSr6aX4eL", "3p7DbnWekWjtMQkey6fp1emdwXbAAxecnYuD5eU9ZZPH"
fs = [str(p) for p in (B / "vault_shards").glob("*.parquet") if not p.name.startswith("._")]
con.execute(f"CREATE TEMP TABLE c AS WITH v AS (SELECT DISTINCT vault,slot,tx_index,block_time,post FROM read_parquet({fs!r}) WHERE vault IN ('{VD}','{VS}')), d AS (SELECT * FROM v WHERE vault='{VD}' AND post>0), s AS (SELECT * FROM v WHERE vault='{VS}') SELECT d.block_time t, d.slot, d.tx_index, (s.post/1e9)/(d.post/1e6) p FROM d JOIN s USING(slot,tx_index) ORDER BY 1,2,3")
px = {}
for z in sorted((RAW / "solusd").glob("SOLUSDT-1m-2024-07*.zip")) + sorted((RAW / "solusd").glob("SOLUSDT-1m-2024-10*.zip")):
    if z.name.startswith("._"): continue
    with zipfile.ZipFile(z) as f, f.open(f.namelist()[0]) as fh:
        for row in csv.reader(io.TextIOWrapper(fh)):
            if row and row[0].isdigit():
                ms = int(row[0]); px[(ms // 1000 if ms > 10**14 else ms) // 60000] = float(row[4])
from datetime import datetime, timezone
diff = 0; n = 0
for l in Path("docs/TIMELINE.md").read_text().splitlines():
    c_ = [x.strip() for x in l.split("|")]
    if len(c_) > 5 and re.match(r"\d\d/\d\d/\d{4}", c_[1]) and c_[4]:
        t = int(datetime.strptime(c_[1], "%d/%m/%Y %H:%M:%S").replace(tzinfo=timezone.utc).timestamp())
        r = con.execute(f"SELECT p FROM c WHERE t<={t} ORDER BY t DESC, slot DESC, tx_index DESC LIMIT 1").fetchone()
        v = r[0] * 1e9 * px.get(t // 60, 0)
        s = f"{v / 1e6:,.2f} M$" if v >= 1e6 else f"{v / 1e3:,.0f} k$"
        n += 1
        if s.replace(",", " ").replace(".", ",") != c_[4].replace(",", ",") and s != c_[4]:
            x = c_[4].replace(" ", "").replace("\xa0", "")
            if s.replace(",", "").replace(".", ",") .replace(" ", "") != x:
                diff += 1; print("écart", c_[1], c_[4], s)
print("lignes", n, "écarts", diff)
print("kanpai vraie date", con.execute(f"SELECT p FROM c WHERE t<=1721084161 ORDER BY t DESC LIMIT 1").fetchone()[0] * 1e9 * px[1721084161 // 60])
