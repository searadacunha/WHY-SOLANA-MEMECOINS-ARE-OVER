#!/usr/bin/env python3
"""Auditeur A. Flux bruts : troncatures par requête, premier financeur avec et sans poussière, C16, C28, C30, C36, C41. En flux, lecture de raw/flows pour le seul groupe, compteurs pour tous."""
import collections, gzip, json, os, sys
import duckdb
ROOT = "REDACTED_HOME/Projects/Dark-MAGA-Investigation"
sys.path.insert(0, ROOT)
from dmaga.labels import label
from dmaga.venues import load as lv
F = "/Volumes/VERBATIM HD/Dark-MAGA-Investigation/raw/flows"
A = "/Volumes/VERBATIM HD/Dark-MAGA-Investigation/audits_work/A"
B = "/Volumes/VERBATIM HD/Dark-MAGA-Investigation/data"
RAY = "5Q544fKrFoe6tsEbD7S8EmxGTJYAKtTVhAW5Q5pge4j1"
V = set(lv())
tr = collections.Counter()
for d in os.listdir(F):
    if d.startswith("._"):
        continue
    for name in ("first_in", "in_before", "dmaga_all", "sol_out_after", "usdc_out_after", "usdt_out_after"):
        p = f"{F}/{d}/{name}.json.gz"
        if os.path.exists(p):
            with gzip.open(p) as fh:
                j = json.load(fh)
            tr[(name, "n")] += 1
            tr[(name, "tronque")] += bool(j["truncated"])
print("requêtes, tronquées", sorted(tr.items()), flush=True)
g = json.load(open(ROOT + "/data/prevent_groups.json"))[0]
gs = json.load(open(ROOT + "/data/group_split.json"))
mem = g["members"]
G41 = gs["g41"]["address"]
res = {}
seen = 0
for m in mem:
    p = f"{F}/{m}/first_in.json.gz"
    if not os.path.exists(p):
        res[m] = None
        continue
    seen += 1
    with gzip.open(p) as fh:
        rows = json.load(fh)["rows"]
    rows = [r for r in rows if r.get("fromUserAccount") and r["fromUserAccount"] != RAY and r["fromUserAccount"] not in V]
    a = rows[0] if rows else None
    b = next((r for r in rows if int(r["amount"]) >= 10_000_000), None)
    res[m] = (a and a["fromUserAccount"], a and a["uiAmount"], b and b["fromUserAccount"], b and b["uiAmount"], a and a["blockTime"])
print("membres tracés", seen, "sur", len(mem))
ms = set(mem)
print("C36 sans filtre : financeur dans le groupe", sum(1 for v in res.values() if v and v[0] in ms), "G41", sum(1 for v in res.values() if v and v[0] == G41))
print("C36 avec >= 0,01 SOL : financeur dans le groupe", sum(1 for v in res.values() if v and v[2] in ms), "G41", sum(1 for v in res.values() if v and v[2] == G41), "premier différent", sum(1 for v in res.values() if v and v[0] != v[2]))
print("  premiers financeurs poussière", [(k[:8], v[0][:8], v[1], (v[2] or "")[:8], v[3]) for k, v in res.items() if v and v[0] != v[2]][:12])
print("  rapport", gs["premier_financeur"])
C = "8YLEuUtZ4eFMJbf46oNb1CeG6dYFWGyxnQSh9hrgzBzR"
with gzip.open(f"{F}/{C}/first_in.json.gz") as fh:
    r = json.load(fh)["rows"][0]
print("C28 premier reçu du créateur", r["fromUserAccount"], label(r["fromUserAccount"]), r["uiAmount"], r["blockTime"], "écart au mint (s)", 1720922725 - r["blockTime"], "signature", r["signature"])
Q = "5QhJJcFZu2ashyKyWSTGHcsyo6ZBCbpVuJqeutvQHScd"
with gzip.open(f"{F}/{Q}/sol_out_after.json.gz") as fh:
    rows = json.load(fh)["rows"]
hit = [x for x in rows if x.get("toUserAccount") == C]
print("C16 lignes 5QhJJc vers créateur", [(x["uiAmount"], x["blockTime"], x["signature"]) for x in hit])
ao = [x for x in gs["g41"]["avant_le_mint"] if str(x["sol"]).startswith("0.5") and x["t"] < 1720922725]
ok = 0
for x in ao:
    p = f"{F}/{x['dst']}/first_in.json.gz"
    if os.path.exists(p):
        with gzip.open(p) as fh:
            if any(r["signature"] == x["sig"] and r["fromUserAccount"] == G41 and r["uiAmount"].startswith("0.5") for r in json.load(fh)["rows"]):
                ok += 1
print("C30 virements de 0,5 SOL", len(ao), "relus dans le first_in du destinataire", ok, "jamais acheteurs", sum(1 for x in ao if not x["a_achete_sur_le_marche"]))
con = duckdb.connect(":memory:", config={"memory_limit": "400MB", "threads": 2, "temp_directory": A + "/duck29", "preserve_insertion_order": False})
LOW, HIGH = 1721588607, 1721590213
CA = f"read_parquet('{A}/a13_ca.parquet')"
LEG = f"read_parquet('{A}/a15_leg.parquet')"
con.execute("CREATE TEMP TABLE g0(a VARCHAR)")
con.executemany("INSERT INTO g0 VALUES (?)", [[m] for m in mem])
con.execute("CREATE TEMP TABLE svc(a VARCHAR)")
con.executemany("INSERT INTO svc VALUES (?)", [[a] for a in V | {RAY, "87g44hEXP7R8ZxoAJtz941tsVftpEXC1LqAFTf2ZHtkH"}])
con.execute(f"INSERT INTO svc SELECT address FROM read_parquet('{B}/nodes.parquet') WHERE kind<>'wallet'")
print("C41 groupe : vendu M en 24 h, part de 217,04 M", con.execute(f"SELECT sum(-dmaga)/1e12, 100*sum(-dmaga)/1e12/217.0365 FROM {LEG} WHERE dmaga<0 AND t>={HIGH} AND t<{HIGH + 86400} AND owner IN (SELECT a FROM g0)").fetchone())
con.execute(f"CREATE TEMP TABLE bal AS SELECT account, arg_max(owner,(slot,tx_index)) o, arg_max(post,(slot,tx_index)) p FROM {CA} WHERE t<{LOW} GROUP BY 1")
print("C41 autres détenteurs >= 1 M à la borne basse", con.execute(f"""WITH h AS (SELECT o, sum(p)/1e12 m FROM bal WHERE o NOT IN (SELECT a FROM g0) AND o NOT IN (SELECT a FROM svc) GROUP BY 1 HAVING sum(p)/1e12>=1),
     v AS (SELECT owner, sum(-dmaga)/1e12 s FROM {LEG} WHERE dmaga<0 AND t>={HIGH} AND t<{HIGH + 86400} GROUP BY 1)
     SELECT count(*), sum(h.m), sum(coalesce(v.s,0)), 100*sum(coalesce(v.s,0))/sum(h.m) FROM h LEFT JOIN v ON v.owner=h.o""").fetchone())
