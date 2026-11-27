"""Contrôles sans calcul lourd : étude gelée, test d'organisation, sorties work_G, frise, N01 à N17, verrous."""
import csv, json, re, hashlib, statistics as st
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
A = Path("audits/2026-11-03"); B = Path("/Volumes/VERBATIM HD/Dark-MAGA-Investigation/data_v2")
def dt(s): return datetime.fromtimestamp(s, timezone.utc).strftime("%d/%m/%Y %H:%M:%S")
print("## verrous")
for e in ("etude_final", "etude_groupe"):
    L = json.load(open(f"{e}/PROTOCOL.lock"))
    bad = [f for f, h in L["fichiers"].items() if not Path(e, f).exists() or hashlib.sha256(Path(e, f).read_bytes()).hexdigest() != h]
    print(e, "gele", L.get("gele_le_utc"), "fichiers", len(L["fichiers"]), "non conformes", bad, "ajouts", [(x.get("date") or x.get("le_utc") or x.get("gele_le_utc"), x.get("fichiers")) for x in L.get("ajouts", [])])
print("## metrics principal")
rows = [r for r in csv.DictReader(open("etude_final/derived/metrics.csv")) if r["variant"] == "primary"]
tg = next(r for r in rows if r["is_dmaga"] == "True"); pe = [r for r in rows if r["is_dmaga"] != "True"]
print("k", len(pe), "pics distincts", len({int(r['S']) // 86400 for r in pe}), len({int(r['S']) // 86400 for r in rows}))
for m in ("M1", "M2", "M3", "M4", "M5", "M6", "M7"):
    v = [float(r[m]) for r in pe]; d = float(tg[m]); ge = sum(x >= d for x in v)
    print(m, round(d, 3), "med", round(st.median(v), 3), "p", round((1 + ge) / (len(v) + 1), 4), "centile", round(100 * sum(x < d for x in v) / len(v), 1), "pairs>=", ge)
T = json.load(open("etude_final/tables/tests.json"))
print("S1", {k: {x: T["S1"][k][x] for x in ("sol_achete", "mediane_sol_passe", "p_sol", "n_fenetres_passees")} for k in ("winig", "avatar")})
fs = json.load(open("etude_final/tables/funder_share.json")); print("funder", fs["dmaga"]["part"], fs["mediane_comparateurs"], fs["p_rang"], fs["k"])
print("## etude_groupe")
R = list(csv.DictReader(open("etude_groupe/derived/table.csv")))
dg = next(r for r in R if r["pool"].startswith("CRSwXnfF")); pg = [r for r in R if r is not dg]
print("k", len(pg), "ext plafonnee", sum(r["extension_plafonnee"] == "True" for r in pg), "courbe tronquee", sum(r["courbe_tronquee"] == "True" for r in pg))
for g in ("principal_G1", "principal_G2", "principal_G3"):
    v = [float(r[g]) for r in pg]; d = float(dg[g])
    print(g, d, "med", st.median(v), "max", max(v), "strict>", sum(x > d for x in v), "egaux", sum(x == d for x in v), "centile", round(100 * sum(x < d for x in v) / len(v), 1), "zero", round(100 * sum(x == 0 for x in v) / len(v), 1))
print("## ordres de pont")
g33 = set(json.load(open(B / "prevent_groups.json"))[0]["members"])
O = list(csv.DictReader(open(A / "work_G/g43_orders.csv")))
ser = {r["dest"] for r in csv.DictReader(open(A / "work_C/cb_window.csv")) if "2024-07-14T01:32:20Z" <= r["utc"] <= "2024-07-14T01:40:51Z" and round(float(r["sol"]) * 1e9) in (500000000, 1000000000, 1050000000)}
sen = {r["sender"] for r in csv.DictReader(open(A / "work_D/d20_senders.csv"))}
SALVE = {"EGtyQEgMKGKXjppDqj9sYy97e9m7nvu1US4SfFXNakMy", "G41vRrsHShLEvwMj58ruhqJycGfAtWXxtLD56uFExL8E", "C73Yv9iHmTaf8SU2XFnGLt7QXUDqbeWNtUYza9WJhkae", "AtZjv3DuV9cLn3Jxm72TMSdTN4aM6CrBaGyxUC4c2wDk"}
CR = "8YLEuUtZ4eFMJbf46oNb1CeG6dYFWGyxnQSh9hrgzBzR"
P1 = (ser | sen | {CR}) - SALVE; P2 = (g33 | SALVE) - P1
print("tailles P1", len(P1), "P2", len(P2), "33 hors P2", sorted(x[:8] for x in g33 - P2), "P2 hors 33", sorted(x[:8] for x in P2 - g33))
tot = sum(float(r["usd_sortis"]) for r in O); print("ordres", len(O), round(tot, 2))
cl = Counter(); nb = Counter()
for r in O:
    k = "33" if r["wallet"] in g33 else ("P2hors33" if r["wallet"] in P2 else ("P1" if r["wallet"] in P1 else "autre"))
    cl[k] += float(r["usd_sortis"]); nb[k] += 1
print("par population usd", {k: round(v, 2) for k, v in cl.items()}, "ordres", dict(nb))
print("wallets autres", Counter(r["wallet"][:8] for r in O if r["wallet"] not in g33 and r["wallet"] not in P2))
print("dates", min(r["utc"] for r in O), max(r["utc"] for r in O), "avant 01/08/2024 usd", round(sum(float(r["usd_sortis"]) for r in O if r["utc"] < "2024-08-01"), 2))
c = [r for r in O if r["wallet"].startswith("C73Yv9iH") and r["receiver_dst"].startswith("0x2d86499a")]; print("C73", len(c), round(sum(float(r["usd_sortis"]) for r in c), 2), min(r["utc"] for r in c), max(r["utc"] for r in c))
b = [r for r in O if r["receiver_dst"].startswith("0xb947bf7f")]; print("0xb947", Counter(r["wallet"][:8] for r in b), round(sum(float(r["usd_sortis"]) for r in b), 2), min(r["utc"] for r in b), max(r["utc"] for r in b))
FB = list(csv.DictReader(open(A / "work_G/flow_boundaries.csv")))
print("perimetres", Counter(r["perimetre_source"] for r in FB))
for nom, S_ in (("P2 comme la table", lambda r: r["perimetre_source"] == "P2"), ("33 exacts", lambda r: r["wallet_source"] in g33)):
    d = defaultdict(float)
    for r in FB:
        if S_(r): d[r["type_frontiere"]] += float(r["sol_eq"] or 0)
    print(nom, {k: round(v, 1) for k, v in d.items()})
print("## dépôts")
I = list(csv.DictReader(open(A / "work_G/g30_in.csv")))
for dep in ("9W9b", "Caw4"):
    r = [x for x in I if x["depot"].startswith(dep)]
    print(dep, "lignes", len(r), "exped", len({x["sender"] for x in r}), {a: round(sum(float(x["amount"]) for x in r if x["asset"] == a), 2) for a in {x["asset"] for x in r}}, "sol_eq", round(sum(float(x["sol_eq"]) for x in r), 2))
ca = {x["sender"] for x in I if x["depot"].startswith("Caw4")}; w9 = {x["sender"] for x in I if x["depot"].startswith("9W9b")}
print("communs", len(ca & w9), "9W9b vs d20", len(w9 & sen), len(w9), len(sen), "serie∩Caw4", len(ser & ca), "serie∩9W9b", len(ser & w9), "union", len(ser & (ca | w9)))
print("salve 23/07", sorted((x["sender"][:8], float(x["amount"])) for x in I if x["depot"].startswith("9W9b") and x["utc"].startswith("2024-07-23") and x["utc"][11:16] in ("02:14", "02:15", "02:16")))
OD = list(csv.DictReader(open(A / "work_G/g52_orders.csv")))
print("DCA tous", len(OD), round(sum(float(r["jetons"]) for r in OD) / 1e6, 2), round(sum(float(r["encaisse_sol_eq"]) for r in OD), 1), "p1", sum(r["p1"] == "True" for r in OD), "g33", sum(r["g33"] == "True" for r in OD))
print("## frise")
tl = Path("docs/TIMELINE.md").read_text().splitlines()
posts = {}
for f in ("data/x_posts.jsonl", str(A / "work_E/x_posts_new.jsonl")):
    for l in open(f):
        j = json.loads(l); posts.setdefault(j["id"], j)
for f in ("evidence/x_wayback/recovered.jsonl", str(A / "work_E/wb_status_recovered.jsonl")):
    for l in open(f):
        j = json.loads(l); posts.setdefault(j["id"], j)
for l in tl:
    m = re.search(r"\bid (\d{18,20})", l)
    if not m or not l.startswith("|"): continue
    i = int(m.group(1)); sn = (i >> 22) + 1288834974657; shown = l.split("|")[1].strip()
    p = posts.get(m.group(1), {}); md = p.get("created_utc_metadata") or p.get("created_at") or ""
    s = datetime.fromtimestamp(sn // 1000, timezone.utc).strftime("%d/%m/%Y %H:%M:%S")
    flag = "" if s == shown else "ECART_ID"
    md2 = ""
    if md and len(md) >= 19 and md[:2] == "20":
        md2 = datetime.fromisoformat(md.replace("Z", "+00:00")[:19]).strftime("%d/%m/%Y %H:%M:%S")
        if md2 != shown: flag += " ECART_META"
    if flag: print(shown, m.group(1), "snow", s, "meta", md2, flag, p.get("author"))
n = 0; d = 0
for l in open("data/x_posts.jsonl"):
    j = json.loads(l); n += 1
    if j.get("created_utc_metadata") and j.get("created_utc_snowflake") and j["created_utc_metadata"] != j["created_utc_snowflake"]: d += 1
print("corpus", n, "dates différentes", d)
print("avatar snowflake", dt(((1815105297410666496 >> 22) + 1288834974657) // 1000))
print("## N01 à N17")
cv = {r["id"]: r for r in csv.DictReader(open(A / "CLAIM_VERIFICATION.csv"))}
case = Path("docs/CASE_REPORT.md").read_text()
for i in range(1, 18):
    k = f"N{i:02d}"; m = re.search(rf"^\| {k} \| (.+?) \| (.+?) \|$", case, re.M); asr = cv[k]["assertion"]
    lv, tx = re.match(r"\[(.+?)\] (.*)", asr).groups()
    print(k, "niveau_egal", lv == m.group(1), "texte_egal", tx == m.group(2).replace("`", ""), "" if lv == m.group(1) else (lv, m.group(1)))
print("## chiffre sériel")
times = [1 * 0]
hms = ["01:32:23", "01:33:05", "01:33:30", "01:34:15", "01:35:00", "01:35:40", "01:36:14", "01:36:57", "01:37:49", "01:38:58", "01:39:38", "01:40:13", "01:40:50"]
t = [int(x[:2]) * 3600 + int(x[3:5]) * 60 + int(x[6:]) for x in hms]; g = [b - a for a, b in zip(t, t[1:])]
print("n", len(t), "duree", t[-1] - t[0], "CV", round(st.pstdev(g) / st.mean(g), 3), round(st.stdev(g) / st.mean(g), 3))
