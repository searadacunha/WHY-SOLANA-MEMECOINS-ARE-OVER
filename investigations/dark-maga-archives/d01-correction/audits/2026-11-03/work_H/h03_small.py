import csv, json, re, statistics as st
from collections import defaultdict, Counter
from pathlib import Path
A = Path("audits/2026-11-03"); B = Path("/Volumes/VERBATIM HD/Dark-MAGA-Investigation/data_v2")
R = list(csv.DictReader(open("etude_groupe/derived/table.csv")))
for g in ("principal_G1", "principal_G2", "principal_G3"):
    print(g, "med 49 lignes", st.median(float(r[g]) for r in R), "med 48 pairs", st.median(float(r[g]) for r in R if not r["pool"].startswith("CRSwXnfF")), "lignes", len(R))
g33 = set(json.load(open(B / "prevent_groups.json"))[0]["members"])
coord = Path("reports/COORDINATION.md").read_text().split("### Membres")[1]
print("membres table", len(set(re.findall(r"^\| `(\w+)` \|", coord, re.M)) & g33), len(re.findall(r"^\| `(\w+)` \|", coord, re.M)))
O = list(csv.DictReader(open(A / "work_G/g43_orders.csv")))
T0 = "2024-07-14 02:05:25"
print("ordres avant mint", sum(r["utc"] < T0 for r in O), round(sum(float(r["usd_sortis"]) for r in O if r["utc"] < T0), 2), "dont 33", sum(r["utc"] < T0 and r["wallet"] in g33 for r in O), round(sum(float(r["usd_sortis"]) for r in O if r["utc"] < T0 and r["wallet"] in g33), 2))
print("ordres 33 après mint", sum(r["utc"] >= T0 and r["wallet"] in g33 for r in O), round(sum(float(r["usd_sortis"]) for r in O if r["utc"] >= T0 and r["wallet"] in g33), 2))
print("ordres 33 sous 7 j de Musk", sum("2024-07-21 19:30:13" <= r["utc"] < "2024-07-28 19:30:13" and r["wallet"] in g33 for r in O), round(sum(float(r["usd_sortis"]) for r in O if "2024-07-21 19:30:13" <= r["utc"] < "2024-07-28 19:30:13" and r["wallet"] in g33), 2))
s = sorted(((float(r["usd_sortis"]), r["utc"], r["wallet"][:8], r["chain_id"]) for r in O), reverse=True)[:5]; print("top ordres", s)
print("ecart cible", round(sum(float(r["usd_sortis"]) for r in O) - 1018687.18, 2), [(r["utc"], r["wallet"][:8], r["usd_sortis"]) for r in O if abs(float(r["usd_sortis"]) - 5246.33) < 1])
print("non USDC", Counter(r["token_dst"][:10] for r in O).most_common(5))
FB = list(csv.DictReader(open(A / "work_G/flow_boundaries.csv")))
print("types", Counter(r["perimetre_source"] for r in FB))
EXCL = ("interne", "pool ou route", "balayage", "autre périmètre", "hors")
for nom, f in (("P2", lambda r: r["perimetre_source"].startswith("P2")), ("33 exacts", lambda r: r["wallet_source"] in g33)):
    d = defaultdict(float); dpre = defaultdict(float)
    for r in FB:
        if f(r):
            k = r["type_frontiere"].split(" [")[0]; d[k] += float(r["sol_eq"] or 0)
            if (r["date_fin"] or "") and r["date_fin"] < T0: dpre[k] += float(r["sol_eq"] or 0)
    den = sum(v for k, v in d.items() if not k.startswith(("interne", "pool ou route")))
    print(nom, "denominateur", round(den, 1), {k: (round(v, 1), round(100 * v / den, 1)) for k, v in sorted(d.items(), key=lambda kv: -kv[1])}, "entierement avant mint", {k: round(v, 1) for k, v in dpre.items()})
OD = list(csv.DictReader(open(A / "work_G/g52_orders.csv")))
p1 = [r for r in OD if r["p1"] == "True"]; print("DCA p1", len(p1), round(sum(float(r["jetons"]) for r in p1) / 1e6, 2), round(sum(float(r["encaisse_sol_eq"]) for r in p1), 1), "p1 et g33", [r["wallet"][:8] for r in OD if r["p1"] == "True" and r["g33"] == "True"], "g33 hors p1", sum(float(r["jetons"]) for r in OD if r["g33"] == "True" and r["p1"] != "True") / 1e6)
for l in open("data/x_posts.jsonl"):
    j = json.loads(l)
    if j.get("author") in ("koreanjewcrypto", "kanpai") and "dmaga" in (j.get("text") or "").lower() and (j.get("created_utc_metadata") or "") < "2024-07-17":
        print(j["author"], j["id"], j.get("created_utc_metadata"), j.get("created_utc_snowflake"), (j.get("text") or "")[:60].replace("\n", " "))
for f in (A / "work_E/x_posts_new.jsonl",):
    for l in open(f):
        j = json.loads(l)
        if j.get("author") in ("koreanjewcrypto", "kanpai") and "dmaga" in (j.get("text") or "").lower() and (j.get("created_utc_metadata") or j.get("created_utc") or "") < "2024-07-17":
            print("new", j.get("author"), j["id"], j.get("created_utc_metadata") or j.get("created_utc"), (j.get("text") or "")[:60].replace("\n", " "))
wb = [json.loads(l) for l in open(A / "work_E/wb_status_recovered.jsonl")]
print("wb lignes", len(wb), "avec texte", sum(bool(x.get("text")) for x in wb), Counter(x.get("account_in_url") for x in wb).most_common(3))
print("recovered", Counter(json.loads(l).get("account_in_url") or json.loads(l).get("author") for l in open("evidence/x_wayback/recovered.jsonl")).most_common(4))
