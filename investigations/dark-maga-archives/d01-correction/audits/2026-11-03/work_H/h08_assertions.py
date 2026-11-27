"""Contrôles par assertion restants, lecture seule."""
import csv, gzip, json, os, re, statistics as st, time
from collections import defaultdict, Counter
from pathlib import Path
import duckdb
os.environ["TZ"] = "UTC"; time.tzset()
A = Path("audits/2026-11-03"); B = Path("/Volumes/VERBATIM HD/Dark-MAGA-Investigation/data_v2"); B0 = Path("/Volumes/VERBATIM HD/Dark-MAGA-Investigation/data"); EXT = Path("/Volumes/VERBATIM HD/Dark-MAGA-Investigation")
con = duckdb.connect(":memory:", config={"memory_limit": "800MB", "threads": 2, "temp_directory": str(EXT / "audits_work/H"), "preserve_insertion_order": False})
con.execute("SET TimeZone='UTC'")
TR, WP, AC, ED, LE, ND, RU, WC = (f"read_parquet('{B}/{n}.parquet')" for n in ("trades", "wallets", "accounts", "token_edges", "link_edges", "nodes", "account_ruptures", "wallet_clusters"))
EV = {e["name"]: e["t"] for e in json.load(open(B / "events.json"))}
T0, LOW, ENV, HIGH, WIN = EV["creation_mint"], EV["musk_borne_basse"], EV["musk_envoi_image"], EV["musk_borne_haute"], EV["winig_visuel"]
g = json.load(open(B / "prevent_groups.json"))[0]; mem = set(g["members"]); IN = ",".join(repr(x) for x in mem)
H3, GX, P9, Q, CR = "H3QsBrrivimFJmSpTXuvig2n1Bh7JuYxrriRSEszT6cc", "GXZvXsD6hxaLeFvQisWpdAwsayJxga7w9EeafhFZG2Ra", "9PrmF8sfoD2YShtWUghrGEYgxwabpnzog8gT1V6LEtdq", "5QhJJcFZu2ashyKyWSTGHcsyo6ZBCbpVuJqeutvQHScd", "8YLEuUtZ4eFMJbf46oNb1CeG6dYFWGyxnQSh9hrgzBzR"
print("C03", json.load(open("evidence/web/profiles/fx_DarkMagaCoin.json")).get("user", {}).get("joined") if Path("evidence/web/profiles/fx_DarkMagaCoin.json").exists() else "absent")
print("C04 archives", [p.name for p in Path("evidence/web/wb_elonmusk").glob("*190327*")][:3] if Path("evidence/web/wb_elonmusk").exists() else "absent")
print("C10 arêtes>=1M groupe avant LOW", con.execute(f"SELECT count(*), count(DISTINCT signature), sum(qty)/1e6, count(DISTINCT src||dst) FROM {ED} WHERE src IN ({IN}) AND dst IN ({IN}) AND qty>=1e6 AND block_time<{LOW}").fetchall())
ck = json.load(open("reports/data_checks/group_edges_check.json")); print("C10 relues", {k: ck[k] for k in ck if k in ("relues", "directes", "n", "ok")}, list(ck)[:8]); print("C16", ck["gaz_vers_createur"]["montant"], ck["deplacement_createur"]["t"] - ck["gaz_vers_createur"]["t"])
col = json.load(open(B / "collector.json")); print("C18", col["expediteurs"], round(col["part_coinbase_pct"], 2), len(col.get("salves", [])), Counter(c["salve"] for c in col["salves"]))
big = f"('{H3}','{GX}','{P9}')"
print("C20 arêtes directes", con.execute(f"SELECT count(*) FROM {ED} WHERE (src IN {big} AND dst IN ({IN})) OR (dst IN {big} AND src IN ({IN})) OR (src IN {big} AND dst IN {big})").fetchall(), con.execute(f"SELECT type, count(*) FROM {LE} WHERE (src IN {big} AND dst IN ({IN})) OR (dst IN {big} AND src IN ({IN})) OR (src IN {big} AND dst IN {big}) GROUP BY 1").fetchall())
print("C22 social", con.execute(f"SELECT edge_type, count(*) FROM read_parquet('{B}/social_links.parquet') GROUP BY 1").fetchall())
adr = Counter()
for f in ("data/x_posts.jsonl", str(A / "work_E/x_posts_new.jsonl")):
    for l in open(f):
        j = json.loads(l)
        if j.get("author") in ("DarkMagaCoin", "kikisknees", "Aristos_Revenge", "ChrisWinig"):
            for a in re.findall(r"\b[1-9A-HJ-NP-Za-km-z]{32,44}\b", j.get("text") or ""):
                if not a.startswith("http"): adr[a] += 1
print("C22 adresses publiées par le noyau", adr.most_common(8))
print("C26 journaux", [(p.name, len(re.findall(r"\b9[67]\b", p.read_text(errors='ignore')))) for p in (EXT / "logs").glob("derive*.out")][:4])
print("C34", con.execute(f"""WITH a AS (SELECT owner, min(block_time) f FROM {TR} WHERE kind='swap' AND token_delta>0 GROUP BY 1), w AS (SELECT DISTINCT owner FROM {TR} WHERE kind='swap' AND token_delta>0 AND block_time>={WIN} AND block_time<{LOW})
   SELECT count(*), sum((a.f<{WIN})::int) FROM w JOIN a USING(owner)""").fetchall(), con.execute(f"""SELECT count(DISTINCT w.owner) FROM (SELECT DISTINCT owner FROM {TR} WHERE kind='swap' AND token_delta>0 AND block_time>={WIN} AND block_time<{LOW}) w JOIN {TR} t ON t.owner=w.owner AND t.kind='swap' AND t.token_delta>0 AND t.block_time>={WIN - 21600} AND t.block_time<{WIN}""").fetchall())
print("C35 Q", con.execute(f"SELECT realized_sol, transfer_out_qty/1e6, transfer_in_qty/1e6 FROM {WP} WHERE owner='{Q}'").fetchall())
print("C36", json.load(open(B / "group_split.json"))["premier_financeur"])
print("C38", con.execute(f"SELECT cluster, n_wallets, strength FROM {WC} ORDER BY n_wallets DESC LIMIT 2").fetchall())
print("C41 groupe sortants", con.execute(f"SELECT count(*), sum(qty)/1e6, count(DISTINCT dst) FROM {ED} WHERE block_time>={HIGH} AND block_time<{HIGH + 86400} AND src IN ({IN}) AND dst NOT IN ({IN}) AND dst<>'(multiple)'").fetchall())
print("C43", sum(v for k, v in json.load(open("etude_final/derived/selection_counts.json")).items() if isinstance(v, int) and k in ("retenu_superset", "pas_de_pic", "hors_bande", "tronque_sans_pic", "reporte_budget")))
print("C51 kinds", con.execute(f"SELECT n1.kind, n2.kind, count(*) FROM {LE} e LEFT JOIN {ND} n1 ON n1.address=e.src LEFT JOIN {ND} n2 ON n2.address=e.dst GROUP BY 1,2 ORDER BY 3 DESC LIMIT 6").fetchall())
print("N01 hot wallets")
cb = list(csv.DictReader(open(A / "work_C/cb_window.csv"))); sen = {r["sender"] for r in csv.DictReader(open(A / "work_D/d20_senders.csv"))}
dest = {r["dest"] for r in cb}; print("cb_window lignes", len(cb), "destinataires", len(dest), "dans 9W9b", len(dest & sen), min(r["utc"] for r in cb), max(r["utc"] for r in cb), "heures", sorted(r["utc"][11:19] for r in cb if r["dest"] in sen)[:1], sorted(r["utc"][11:19] for r in cb if r["dest"] in sen)[-1:])
print("N05", con.execute(f"SELECT count(*) FROM {ED} WHERE (src='{CR}' AND dst IN ({IN})) OR (dst='{CR}' AND src IN ({IN}))").fetchall())
for n, f, pat in (("N03", "work_D/d43_perim.txt", r"1 ?365|1365"), ("N04", "work_D/d21_match.txt", r"6\.5763"), ("N14", "work_A/out/a01_sigs.log", r"8199964|5974078"), ("N15", "work_D/d20_series.txt", r"2024-06-26"), ("N02", "work_D/d49_small.txt", r"155000|155 000")):
    p = A / f; t = p.read_text(errors="ignore") if p.exists() else ""; print(n, f, "occurrences", len(re.findall(pat, t)), (re.search(rf".*(?:{pat}).*", t).group(0)[:150] if re.search(pat, t) else ""))
print("X image 18:46:37", [str(p) for p in Path("audits/2026-11-03/work_E/evidence").rglob("GTCEEQ2WoAAm65s*")][:2])
print("X avatar", sorted(p.name for p in Path("audits/2026-11-03/work_E/evidence").rglob("*GTA*"))[:3])
wb = {}
for r in csv.DictReader(open(A / "work_E/derived/visual_wb.csv")): wb[r["file"]] = r
print("visual_wb lignes", len(wb), "fichier V3", [(k, v["avatar"], v["V1"], v["avatarV3"]) for k, v in wb.items() if k.startswith("GTCEEQ2")][:2], "V1", [(k, v["avatar"], v["V1"]) for k, v in wb.items() if v["V1"] == "0"][:4])
print("g31", (A / "work_G/g31_ctrl_overlap.txt").read_text(errors="ignore")[-400:])
print("# pics distincts etude_groupe")
S = {r["pool"]: int(r["S"]) for r in csv.DictReader(open("etude_final/derived/metrics.csv")) if r["variant"] == "primary"}
R = [r for r in csv.DictReader(open("etude_groupe/derived/table.csv")) if not r["pool"].startswith("CRSwXnfF")]
print("k", len(R), "avec S", sum(r["pool"] in S for r in R), "jours de pic", len({S[r["pool"]] // 86400 for r in R if r["pool"] in S}))
print("# anciens doublons")
print("N11 doublons ancien", con.execute(f"SELECT coalesce(sum(n-1),0) FROM (SELECT count(*) n FROM read_parquet('{B0}/trades.parquet') GROUP BY signature,kind,owner,venue,token_delta,source HAVING count(*)>1)").fetchall())
print("# allers-retours, code propre")
cur = con.execute(f"SELECT owner, slot, tx_index, block_time, token_delta, sol_lamports FROM {TR} WHERE kind='swap' ORDER BY owner, slot, tx_index")
tot_b = tot_rt = 0; win = defaultdict(float); bw = defaultdict(float); own_b = defaultdict(float); own_rt = defaultdict(float)
F = {"envoi_haute": (ENV, HIGH), "24h": (HIGH, HIGH + 86400)}
cur_o = None; pend = []
while True:
    ch = cur.fetchmany(50000)
    if not ch: break
    for o, sl, ix, t, d, v in ch:
        if o != cur_o: cur_o, pend = o, []
        if d > 0:
            sol = -v; tot_b += sol; own_b[o] += sol; pend.append([t, d, sol])
            for k, (a, z) in F.items():
                if a <= t < z: bw[k] += sol
        elif d < 0:
            pend = [p for p in pend if t - p[0] <= 10]
            for p in pend:
                if abs(-d - p[1]) <= 0.01 * p[1]:
                    tot_rt += p[2]; own_rt[o] += p[2]
                    for k, (a, z) in F.items():
                        if a <= p[0] < z: win[k] += p[2]
                    pend.remove(p); break
print("total", round(tot_b / 1e9, 1), "AR", round(tot_rt / 1e9, 1), round(100 * tot_rt / tot_b, 2), {k: (round(bw[k] / 1e9, 2), round(win[k] / 1e9, 2)) for k in F})
b100 = [o for o, v in own_b.items() if v >= 100e9 and own_rt[o] / v > 0.5]; print("plus de 50 % et 100 SOL", len(b100), round(sum(own_b[o] for o in b100) / 1e9, 1))
top = sorted(own_b, key=own_b.get, reverse=True)[:3]; print("top3", [(o[:8], round(own_b[o] / 1e9, 1), round(100 * own_rt[o] / own_b[o], 1)) for o in top])
