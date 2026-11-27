import csv, json, os, time
from collections import defaultdict, Counter
from pathlib import Path
import duckdb
os.environ["TZ"] = "UTC"; time.tzset()
A = Path("audits/2026-11-03"); B = Path("/Volumes/VERBATIM HD/Dark-MAGA-Investigation/data_v2"); RAW = Path("/Volumes/VERBATIM HD/Dark-MAGA-Investigation/raw")
O = list(csv.DictReader(open(A / "work_G/g43_orders.csv")))
g33 = set(json.load(open(B / "prevent_groups.json"))[0]["members"])
print("autres ordres", [(r["utc"], r["wallet"][:8], r["usd_sortis"]) for r in O if r["wallet"] not in g33])
d = Counter()
for r in O: d[r["wallet"][:8]] += float(r["usd_sortis"])
print("par wallet", {k: round(v, 2) for k, v in d.most_common()})
print("signatures doublées", [k for k, v in Counter(r["signature"] for r in O).items() if v > 1][:5])
FB = list(csv.DictReader(open(A / "work_G/flow_boundaries.csv")))
pb = [r for r in FB if r["type_frontiere"].startswith("pont")]
print("lignes pont", len(pb), Counter(r["perimetre_source"] for r in pb), "actifs", Counter(r["actif"] for r in pb), "montant", round(sum(float(r["montant"] or 0) for r in pb), 2), "sol_eq", round(sum(float(r["sol_eq"] or 0) for r in pb), 1), "n", sum(int(float(r["n"] or 0)) for r in pb))
for per in {r["perimetre_source"] for r in pb}:
    print(per, round(sum(float(r["montant"] or 0) for r in pb if r["perimetre_source"] == per), 2), sum(int(float(r["n"] or 0)) for r in pb if r["perimetre_source"] == per))
con = duckdb.connect(":memory:", config={"memory_limit": "500MB", "threads": 2, "temp_directory": "/Volumes/VERBATIM HD/Dark-MAGA-Investigation/audits_work/H"})
con.execute("SET TimeZone='UTC'")
WP, AC, ED, RU = (f"read_parquet('{B}/{n}.parquet')" for n in ("wallets", "accounts", "token_edges", "account_ruptures"))
AR = "ARu4n5mFdZogZAravu7CcizaojWnS6oqka37gdLT5SZn"
print("ARu4 traced", (RAW / "flows" / AR).exists(), con.execute(f"SELECT residual_qty/1e6, residual_flux_qty/1e6, n_ruptures, transfer_in_qty/1e6, transfer_out_qty/1e6, n_buys, n_sells, completeness FROM {WP} WHERE owner='{AR}'").fetchall())
print("ARu4 comptes", con.execute(f"SELECT count(*) FROM {AC} WHERE owner='{AR}'").fetchone(), "aretes", con.execute(f"SELECT how, count(*), sum(qty)/1e6, min(block_time), max(block_time) FROM {ED} WHERE src='{AR}' OR dst='{AR}' GROUP BY 1").fetchall(), "src top", con.execute(f"SELECT src, dst, qty/1e6, strftime(to_timestamp(block_time),'%d/%m/%Y') FROM {ED} WHERE src='{AR}' OR dst='{AR}' ORDER BY qty DESC LIMIT 4").fetchall())
# créateur et 1re minute
C = "8YLEuUtZ4eFMJbf46oNb1CeG6dYFWGyxnQSh9hrgzBzR"
TR = f"read_parquet('{B}/trades.parquet')"
T0 = 1720922725
print("créateur lignes", con.execute(f"SELECT kind, venue, token_delta/1e12, sol_lamports/1e9, strftime(to_timestamp(block_time),'%d/%m/%Y %H:%M:%S') FROM {TR} WHERE owner='{C}' ORDER BY block_time LIMIT 8").fetchall())
print("slot création", con.execute(f"SELECT count(DISTINCT owner) FROM {TR} WHERE slot=277417695 AND kind='swap' AND token_delta>0").fetchone(), con.execute(f"SELECT count(DISTINCT owner), sum(token_delta)/1e12, sum(-sol_lamports)/1e9 FROM {TR} WHERE kind='swap' AND token_delta>0 AND block_time<{T0 + 60}").fetchone())
print("ventes créateur avant 2025", con.execute(f"SELECT count(*) FROM {TR} WHERE owner='{C}' AND kind='swap' AND token_delta<0 AND block_time<1735689600").fetchone())
gs = [json.loads(json.dumps(x)) for x in json.load(open(B / "group_split.json"))["gestes_du_jour"]]
print("gestes", len(gs), gs[0] if gs else None)
print("transferts 14:22-14:25", con.execute(f"SELECT src, dst, qty/1e6 FROM {ED} WHERE block_time>=1721571720 AND block_time<1721572000 AND src IN ({','.join(repr(x) for x in g33)}) ORDER BY block_time").fetchall())
# fenêtre pmarca dans windows.csv, et postes K03 du pic
for w in csv.DictReader(open(B / "windows.csv")): 
    if w["window"].startswith(("avant_pmarca", "pmarca_a")): print(w["window"], w["from_t"], w["to_t"], w["hours"])
