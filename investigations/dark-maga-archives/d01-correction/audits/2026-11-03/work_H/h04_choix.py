"""Relecture des choix de l'agent F : K06, K04, K08. Lecture seule."""
import csv, gzip, json, os, re, time
from collections import Counter, defaultdict
from pathlib import Path
import duckdb
os.environ["TZ"] = "UTC"; time.tzset()
B = Path("/Volumes/VERBATIM HD/Dark-MAGA-Investigation/data_v2"); B0 = Path("/Volumes/VERBATIM HD/Dark-MAGA-Investigation/data"); RAW = Path("/Volumes/VERBATIM HD/Dark-MAGA-Investigation/raw")
con = duckdb.connect(":memory:", config={"memory_limit": "800MB", "threads": 2, "temp_directory": "/Volumes/VERBATIM HD/Dark-MAGA-Investigation/audits_work/H", "preserve_insertion_order": False})
con.execute("SET TimeZone='UTC'")
BT, P, WP, AC, ED, TR = (f"read_parquet('{B}/{n}.parquet')" for n in ("bots", "owner_programs", "wallets", "accounts", "token_edges", "trades"))
def rows(q): return con.execute(q).fetchall()
print("## K06")
print("motifs", rows(f"SELECT motif, count(*), sum(bought_sol) FROM {BT} WHERE bot_aller_retour GROUP BY 1"))
for r in rows(f"SELECT owner, bought_sol, aller_retour_sol, part_aller_retour, lignes, lignes_signataire, programme FROM {BT} WHERE motif LIKE 'jamais%'"): print("propre", r)
print("gros >=100 SOL", rows(f"SELECT count(*), sum(bought_sol), sum((lignes_signataire=0)::int), sum(CASE WHEN lignes_signataire=0 THEN bought_sol ELSE 0 END), sum((lignes_signataire=0 AND NOT bot_aller_retour)::int), sum(CASE WHEN lignes_signataire=0 AND NOT bot_aller_retour THEN bought_sol ELSE 0 END) FROM {BT} WHERE bought_sol>=100"))
print("non signataires non étiquetés, 12 premiers", rows(f"SELECT owner, round(bought_sol,1), round(part_aller_retour,3), lignes FROM {BT} WHERE bought_sol>=100 AND lignes_signataire=0 AND NOT bot_aller_retour ORDER BY bought_sol DESC LIMIT 12"))
con.execute(f"CREATE TEMP TABLE g AS SELECT owner a, bought_sol b FROM {BT} WHERE bought_sol>=100 AND lignes_signataire=0")
con.execute(f"CREATE TEMP TABLE uses AS SELECT program, count(DISTINCT owner) n_own FROM {P} GROUP BY 1")
con.execute(f"CREATE TEMP TABLE parts AS SELECT owner, program, count(DISTINCT signature) n FROM {P} WHERE owner IN (SELECT a FROM g) GROUP BY 1,2")
con.execute(f"CREATE TEMP TABLE tot AS SELECT owner, count(DISTINCT signature) n FROM {P} WHERE owner IN (SELECT a FROM g) GROUP BY 1")
base = {r[0] for r in rows(f"SELECT owner FROM {BT} WHERE bought_sol>=100 AND part_aller_retour>0.5")}
for share in (0.5, 0.8, 0.95):
    for no in (1, 3, 5, 10, 20, 50):
        p = {r[0]: r[1] for r in rows(f"SELECT parts.owner, g.b FROM parts JOIN tot USING(owner) JOIN uses USING(program) JOIN g ON g.a=parts.owner WHERE parts.n>={share}*tot.n AND uses.n_own<={no} GROUP BY 1,2")}
        new = {k: v for k, v in p.items() if k not in base}
        print("seuils", share, no, "ajouts", len(new), round(sum(new.values()), 1))
# rang si on ne retirait pas ces deux wallets : rangs par SOL acheté dans le top 100 publié
txt = Path("reports/TOP_TRADERS.md").read_text().split("## 100 plus gros acheteurs")[1].split("## Écartés")[0]
tb = re.findall(r"^\| (\d+) \| `(\w+)` \| ([\d ,]+) \|", txt, re.M)
vals = [(int(a), b, float(c.replace(" ", "").replace(",", "."))) for a, b, c in tb]
print("top acheteurs lignes", len(vals), "seuil rang 100", vals[-1][2], "rang 50", vals[49][2])
sig = [r["signer"] if "signer" in r else list(r.values())[0] for r in csv.DictReader(open("audits/2026-11-03/work_G/g42_signers.csv"))]
print("signataires 3GMsedVP", len(sig), "étiquetés bots", rows(f"SELECT count(*), coalesce(sum(bought_sol),0) FROM {BT} WHERE bot_aller_retour AND owner IN ({','.join(repr(x) for x in sig)})"), "non étiquetés", rows(f"SELECT count(*), coalesce(sum(bought_sol),0) FROM {BT} WHERE NOT bot_aller_retour AND owner IN ({','.join(repr(x) for x in sig)})"))
print("dans le top 100 publié", [(a, b[:8], c) for a, b, c in vals if b in set(sig) or b.startswith("4ToQp55m")])
print("4ToQp55m", rows(f"SELECT bought_sol, aller_retour_sol, part_aller_retour, lignes, lignes_signataire, bot_aller_retour FROM {BT} WHERE owner='4ToQp55myvfpeprgKuqGbDqyji9Ezm7CZg7QbcTpL33S'"))
print("## K04")
con.execute(f"CREATE TEMP TABLE fin AS SELECT owner, sum(p) v FROM (SELECT account, arg_max(owner,(slot,tx_index)) owner, arg_max(post,(slot,tx_index)) p FROM {AC} GROUP BY 1) GROUP BY 1")
print("wallets : somme solde seul", rows(f"SELECT sum(coalesce(f.v,0))/1e12, sum(w.residual_qty)/1e6, sum(w.residual_flux_qty)/1e6 FROM {WP} w LEFT JOIN fin f USING(owner)"))
print("écarts corrigé-solde seul", rows(f"SELECT sum((abs(w.residual_qty-coalesce(f.v,0)/1e6)>1e-6)::int), sum(CASE WHEN w.residual_qty<coalesce(f.v,0)/1e6 THEN coalesce(f.v,0)/1e6-w.residual_qty ELSE 0 END)/1e6, sum(CASE WHEN w.residual_qty>coalesce(f.v,0)/1e6 THEN w.residual_qty-coalesce(f.v,0)/1e6 ELSE 0 END)/1e6 FROM {WP} w LEFT JOIN fin f USING(owner)"))
print("top écarts", rows(f"SELECT w.owner, round(w.residual_flux_qty/1e6,2), round(coalesce(f.v,0)/1e12,2), round(w.residual_qty/1e6,2) FROM {WP} w LEFT JOIN fin f USING(owner) ORDER BY abs(w.residual_qty-coalesce(f.v,0)/1e6) DESC LIMIT 8"))
top25 = rows(f"SELECT w.owner, w.residual_qty/1e6, coalesce(f.v,0)/1e12, w.residual_flux_qty/1e6, w.n_ruptures FROM {WP} w LEFT JOIN fin f USING(owner) ORDER BY w.residual_qty DESC LIMIT 25")
print("top25 : somme", round(sum(r[1] for r in top25), 2), "solde seul", round(sum(r[2] for r in top25), 2), "flux", round(sum(r[3] for r in top25), 2), "avec rupture", sum(r[4] > 0 for r in top25), "dont écart >0,1 M", sum(abs(r[1] - r[2]) > 0.1 for r in top25))
traced = {p.name for p in (RAW / "flows").iterdir() if p.is_dir() and not p.name.startswith("._")}
print("wallets tracés", len(traced))
con.execute("CREATE TEMP TABLE tr(a VARCHAR)"); con.executemany("INSERT INTO tr VALUES (?)", [[a] for a in traced])
print("résiduel par classe (M) : tracé/non tracé × rupture", rows(f"SELECT owner IN (SELECT a FROM tr), n_ruptures>0, count(*), round(sum(residual_qty)/1e6,1) FROM {WP} GROUP BY 1,2 ORDER BY 1,2"))
print("multi-comptes touchés par transferts cachés", rows(f"""WITH x AS (SELECT e.src, e.dst, e.qty FROM {ED} e WHERE e.how='gtba' AND e.dst<>'(multiple)' AND NOT EXISTS (SELECT 1 FROM {TR} t WHERE t.signature=e.signature AND (t.owner=e.src OR t.owner=e.dst))),
   n AS (SELECT owner, count(DISTINCT account) k FROM {AC} GROUP BY 1) SELECT count(*), sum(qty), sum(CASE WHEN coalesce(n1.k,0)>1 OR coalesce(n2.k,0)>1 THEN 1 ELSE 0 END), sum(CASE WHEN coalesce(n1.k,0)>1 OR coalesce(n2.k,0)>1 THEN qty ELSE 0 END) FROM x LEFT JOIN n n1 ON n1.owner=x.src LEFT JOIN n n2 ON n2.owner=x.dst"""))
print("complétude", rows(f"SELECT completeness, count(*) FROM {WP} GROUP BY 1 ORDER BY 2 DESC LIMIT 6"))
print("## K08")
Y0, T0 = 1689292800, 1720922725
lv = json.loads((B0 / "trace_levels.json").read_text())
lab = dict(rows(f"SELECT src, any_value(CASE WHEN is_pool THEN 'pool' WHEN src_label IS NULL THEN 'sans' WHEN src_label LIKE 'Jupiter%' THEN 'jup' WHEN src_label LIKE 'Pont%' OR src_label LIKE 'Service%' THEN 'serv' ELSE 'ech' END) FROM read_parquet('{B}/funding_edges.parquet') GROUP BY 1"))
F, FIRST, RAWS = defaultdict(float), defaultdict(float), defaultdict(float)
n_rows = n_seen = 0; sol_seen = 0.0; n_multi = 0; sol_multi = 0.0; n_cross = 0; sol_cross = 0.0; n_cross_eq = 0
wallets = 0
for d in sorted(traced):
    p = RAW / "flows" / d / "in_before.json.gz"
    if not p.exists(): continue
    wallets += 1
    q = {}
    for name in ("in_before", "first_in"):
        pp = RAW / "flows" / d / f"{name}.json.gz"
        if not pp.exists(): continue
        J = json.load(gzip.open(pp)); seen = set(); byk = defaultdict(list)
        for x in J["rows"]:
            s = x.get("fromUserAccount")
            if not s: continue
            sol = int(x["amount"]) / 1e9
            if name == "in_before" and lv.get(d, 0) == 0 and Y0 <= x["blockTime"] < T0: RAWS[lab.get(s, "sans")] += sol
            if (x["signature"], s, sol) in seen:
                n_seen += 1; sol_seen += sol
                continue
            seen.add((x["signature"], s, sol)); byk[(x["signature"], s)].append((sol, x["blockTime"]))
            n_rows += 1
        q[name] = byk
    ib = q.get("in_before", {}); fi = q.get("first_in", {})
    for k, v in ib.items():
        tot = sum(a for a, _ in v)
        if len(v) > 1: n_multi += 1; sol_multi += tot - v[0][0]
        if lv.get(d, 0) == 0 and Y0 <= v[0][1] < T0:
            src = k[1]
            F[lab.get(src, "sans")] += max(tot, sum(a for a, _ in fi[k])) if k in fi else tot
            FIRST[lab.get(src, "sans")] += v[0][0]
        if k in fi:
            n_cross += 1; t2 = sum(a for a, _ in fi[k]); n_cross_eq += abs(t2 - tot) < 1e-9; sol_cross += min(tot, t2)
for nom, D in (("somme par clé (F)", F), ("première ligne par clé", FIRST), ("brut sans dédoublonnage", RAWS)):
    t = sum(D.values()); print(nom, round(t, 1), {k: round(100 * v / t, 3) for k, v in sorted(D.items())})
print("wallets lus", wallets, "lignes retenues", n_rows, "doublons (sig,src,montant) retirés", n_seen, round(sol_seen, 3), "clés à plusieurs virements in_before", n_multi, "SOL en plus", round(sol_multi, 3), "clés dans les deux requêtes", n_cross, "égales", n_cross_eq, "SOL commun", round(sol_cross, 1))
