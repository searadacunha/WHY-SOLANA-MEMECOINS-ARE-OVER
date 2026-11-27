#!/usr/bin/env python3
"""Auditeur D. Recalcul des assertions restantes, sur mon parseur (d01_*) et les bruts. Sortie d46_claims.txt. Les chiffres vont dans CLAIM_VERIFICATION.csv."""
import csv, gzip, hashlib, json, os, statistics as st, sys, time, collections
import duckdb
D = "/Volumes/VERBATIM HD/Dark-MAGA-Investigation/audits_work/D"; BIG = "/Volumes/VERBATIM HD/Dark-MAGA-Investigation/data"; NET = "/Volumes/VERBATIM HD/Dark-MAGA-Investigation/audits_work/C/net/"
OUT = "audits/2026-11-03/work_D/"
con = duckdb.connect(":memory:", config={"memory_limit": "700MB", "threads": 2, "temp_directory": D + "/duck", "preserve_insertion_order": False})
con.execute("SET TimeZone='UTC'")
sys.stdout = open(OUT + "d46_claims.txt", "w")
def q(n, s):
    r = con.execute(s).fetchall(); print(n, r, flush=True); return r
iso = lambda t: time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(t))
AC = f"read_parquet('{D}/d01_acct.parquet')"; OW = f"read_parquet('{D}/d01_own.parquet')"; TX = f"read_parquet('{D}/d01_tx.parquet')"; TR = f"read_parquet('{BIG}/trades.parquet')"; EDG = f"read_parquet('{BIG}/token_edges.parquet')"; R = f"read_parquet('{D}/d42_rupt.parquet')"; WP = f"read_parquet('{BIG}/wallets.parquet')"
T0, CRE, S, LOW, ENV, HIGH, WIN = 1720922725, 1720923331, 1721588400, 1721588607, 1721589800, 1721590213, 1721577749
PG = json.load(open("data/prevent_groups.json"))[0]; GS = json.load(open("data/group_split.json"))
G = PG["members"]; con.execute("CREATE TEMP TABLE g(a VARCHAR)"); con.executemany("INSERT INTO g VALUES (?)", [[x] for x in G])
CR = "8YLEuUtZ4eFMJbf46oNb1CeG6dYFWGyxnQSh9hrgzBzR"; CURVE = "87g44hEXP7R8ZxoAJtz941tsVftpEXC1LqAFTf2ZHtkH"
VT, VS = "5HuEsLbebeuottMsFW3hHcXTrKVsu3WUNSQnSr6aX4eL", "3p7DbnWekWjtMQkey6fp1emdwXbAAxecnYuD5eU9ZZPH"
# C01
q("C01 première tx DMAGA", f"SELECT sig,slot,bt,payer FROM {TX} ORDER BY slot,idx LIMIT 1")
print("C02 écart depuis 22:11:33 UTC le 13/07", T0 - 1720908693, "s")
# C05 bis C06
for n_, a, z in (("C06 Biden 17:46:00 -> borne basse", 1721583960, LOW),):
    q(n_, f"SELECT round(sum(CASE WHEN token_delta>0 THEN -sol_lamports ELSE 0 END)/1e9,3),round(sum(CASE WHEN token_delta<0 THEN sol_lamports ELSE 0 END)/1e9,3),round(({z}-{a})/3600.0,3) FROM {TR} WHERE kind='swap' AND block_time>={a} AND block_time<{z}")
# C07, C45 : S1 depuis les swaps gelés
SW = f"read_parquet('{BIG}/controls/swaps/CRSwXnfF21yHDXdYBVWwCwQ5Ni2A4QuK3qGYis5k7x7k.parquet')"
for name, E in (("Winig", WIN), ("avatar", ENV)):
    a = con.execute(f"SELECT coalesce(sum(-sol),0)/1e9 FROM {SW} WHERE qty>0 AND t>={E-10800} AND t<{E}").fetchone()[0]
    lo = CRE + 96 * 3600
    n = (E - 10800 - lo) // 10800
    # fenêtres sans chevauchement, alignées sur E, de création + 96 h à E - 3 h
    vals = []
    for k in range(1, n + 1):
        z = E - 10800 * k; aa = z - 10800
        if aa < lo: break
        vals.append(con.execute(f"SELECT coalesce(sum(-sol),0)/1e9 FROM {SW} WHERE qty>0 AND t>={aa} AND t<{z}").fetchone()[0])
    c = sum(1 for v in vals if v >= a)
    print(f"S1 {name} : SOL {a:.2f}, fenêtres {len(vals)}, médiane {st.median(vals):.2f}, >= {c}, p {(1+c)/(len(vals)+1):.4f}, max passé {max(vals):.1f}")
# C10
ed = PG["edges_top"]; print("C10 arêtes", len(ed), "composante", len(G))
con.execute("CREATE TEMP TABLE ed(s VARCHAR,a VARCHAR,b VARCHAR,m DOUBLE)"); con.executemany("INSERT INTO ed VALUES (?,?,?,?)", [[e["sig"], e["src"], e["dst"], e["M"]] for e in ed])
q("  arêtes dans mon brut, montant opposé exact", f"""WITH d AS (SELECT DISTINCT sig,owner,d FROM {OW} WHERE sig IN (SELECT s FROM ed))
   SELECT count(*),sum((abs(x.d+y.d)<=1000 AND abs(abs(x.d)/1e12-ed.m)<0.002)::int) FROM ed JOIN d x ON x.sig=ed.s AND x.owner=ed.a JOIN d y ON y.sig=ed.s AND y.owner=ed.b""")
abs_ = set(); 
with gzip.open(NET + "absent_1M.jsonl.gz", "rt") as fh:
    for l in fh:
        j = json.loads(l); t = j.get("tx", j); abs_.add(t["transaction"]["signatures"][0])
hidden = con.execute(f"SELECT s FROM ed WHERE s NOT IN (SELECT DISTINCT sig FROM {OW})").fetchall()
print("  arêtes absentes de mon brut", len(hidden), "relues dans le brut réseau de C", sum(1 for h in hidden if h[0] in abs_))
# C11-C13
sub = {r["wallet"]: r for r in csv.DictReader(open("audits/2026-11-03/work_C/members_table.csv"))}
small = [m for s in GS["ponts_faibles"] if s["M"] == 15.0 for m in s["members"]]
BT = f"read_parquet('{D}/d42_bal_T.parquet')"
con.execute(f"""CREATE TEMP TABLE hid AS SELECT src,sum(qty*1e6) q FROM {EDG} WHERE how='gtba' AND block_time<{LOW} AND dst<>'(multiple)' AND src IN (SELECT a FROM g) AND signature NOT IN (SELECT DISTINCT sig FROM {OW} WHERE bt<{LOW}) GROUP BY 1""")
con.execute(f"CREATE TEMP TABLE ow AS SELECT b.owner,sum(b.bal) v FROM {BT} b WHERE b.owner IN (SELECT a FROM g) GROUP BY 1")
vals = {o: v - (con.execute("SELECT q FROM hid WHERE src=?", [o]).fetchone() or [0])[0] for o, v in con.execute("SELECT owner,v FROM ow").fetchall()}
print("C11 somme", round(sum(vals.values()) / 1e12, 3), "C13 4 wallets", [s[:8] for s in small], round(sum(vals.get(x, 0) for x in small) / 1e12, 3), "C12 29", round(sum(v for k, v in vals.items() if k not in small) / 1e12, 3), round(100 * sum(v for k, v in vals.items() if k not in small) / 938e12, 2))
# C14, C29
q("C14 membres avec achat en 1re heure", f"SELECT count(DISTINCT owner) FROM {OW} o WHERE d>0 AND bt<{T0+3600} AND owner IN (SELECT a FROM g) AND sig IN (SELECT sig FROM {TR} WHERE kind='swap' AND token_delta>0 AND block_time<{T0+3600})")
q("C29 acheteurs 60 s (lignes swap), M, SOL", f"SELECT count(DISTINCT owner),round(sum(token_delta)/1e12,3),round(sum(-sol_lamports)/1e9,3) FROM {TR} WHERE kind='swap' AND token_delta>0 AND block_time<{T0+60}")
q("C29 acheteurs dans le slot de création", f"SELECT owner,round(token_delta/1e12,3),round(-sol_lamports/1e9,4) FROM {TR} WHERE kind='swap' AND token_delta>0 AND slot=277417695")
q("C29 mon brut slot de création", f"SELECT owner,d/1e12 FROM {OW} WHERE slot=277417695 AND owner<>'{CURVE}'")
# C16
def tx(a, s):
    with gzip.open(NET + a + ".jsonl.gz", "rt") as fh:
        for l in fh:
            t = json.loads(l)
            if t["transaction"]["signatures"][0].startswith(s): return t
g1 = tx(CR, "Nfzx313V"); g2 = tx(CR, "2BUp8LXm")
print("C16 gaz", iso(g1["blockTime"]), [(i["parsed"]["info"]["source"][:8], i["parsed"]["info"]["destination"][:8], int(i["parsed"]["info"]["lamports"]) / 1e9) for i in g1["transaction"]["message"]["instructions"] if isinstance(i.get("parsed"), dict) and i["parsed"].get("type") == "transfer"], "ordre", iso(g2["blockTime"]), "écart s", g2["blockTime"] - g1["blockTime"], "progs ordre", sorted({i["programId"][:8] for i in g2["transaction"]["message"]["instructions"]}))
k = [x["pubkey"] for x in g1["transaction"]["message"]["accountKeys"]]; i = k.index(CR)
print("  solde créateur avant gaz", g1["meta"]["preBalances"][i] / 1e9, "signataires", [x["pubkey"][:8] for x in g1["transaction"]["message"]["accountKeys"] if x["signer"]])
# C20 SOL direct
FAMG = set(G) | {CR} | {r["sender"] for r in csv.DictReader(open(OUT + "d20_senders.csv"))} | {r["dest"] for r in csv.DictReader(open("audits/2026-11-03/work_C/cb_window.csv")) if "2024-07-14T01:32:20Z" <= r["utc"] <= "2024-07-14T01:40:51Z" and round(float(r["sol"]) * 1e9) in (500000000, 1000000000, 1050000000)}
print("C20 périmètre", len(FAMG))
for a in ("H3QsBrrivimFJmSpTXuvig2n1Bh7JuYxrriRSEszT6cc", "GXZvXsD6hxaLeFvQisWpdAwsayJxga7w9EeafhFZG2Ra", "9PrmF8sfoD2YShtWUghrGEYgxwabpnzog8gT1V6LEtdq"):
    p = NET + a + ".jsonl.gz"
    if not os.path.exists(p): print("  ", a[:8], "pas d'historique local"); continue
    n = 0; hits = []; mx = 0
    with gzip.open(p, "rt") as fh:
        for l in fh:
            t = json.loads(l); n += 1; mx = max(mx, t["blockTime"])
            seq = list(t["transaction"]["message"]["instructions"])
            for g_ in t["meta"].get("innerInstructions") or []: seq += g_["instructions"]
            for i_ in seq:
                q_ = i_.get("parsed")
                if i_.get("program") == "system" and isinstance(q_, dict) and q_.get("type") == "transfer":
                    x, y = q_["info"]["source"], q_["info"]["destination"]
                    if (x == a and y in FAMG) or (y == a and x in FAMG):
                        hits.append((iso(t["blockTime"]), x[:8], y[:8], int(q_["info"]["lamports"]) / 1e9))
    print("  ", a[:8], "tx", n, "dernière", iso(mx), "virements SOL avec le périmètre", hits[:5])
# C24
q("C24 ruptures sur le vault jeton Raydium (mon brut)", f"SELECT count(*),sum(gap) FROM {R} WHERE account='{VT}'")
q("C24 tx distinctes touchant les vaults", f"SELECT sum((vt_d<>0)::int),sum((vs_d<>0)::int) FROM (SELECT DISTINCT sig,vt_d,vs_d FROM {TX})")
# C23
q("C23 tx distinctes tout brut touchant DMAGA, échouées", f"SELECT count(DISTINCT sig),sum(failed::int) FROM {TX}")
q("C23 wallets", f"SELECT count(*) FROM {WP}")
# C28
q("C28 créateur : swaps vente", f"SELECT count(*) FROM {TR} WHERE owner='{CR}' AND kind='swap' AND token_delta<0")
q("C28 créateur : 1er achat", f"SELECT round(token_delta/1e12,3),round(-sol_lamports/1e9,4),block_time FROM {TR} WHERE owner='{CR}' AND kind='swap' ORDER BY slot LIMIT 1")
q("C28 créateur : premier delta négatif de mon brut", f"SELECT min(bt) FROM {OW} WHERE owner='{CR}' AND d<0")
# C34
q("C34 cohortes de premier achat (wallets.parquet)", f"""SELECT CASE WHEN first_buy_time<{WIN} THEN 'avant visuel' WHEN first_buy_time<{LOW} THEN 'avant Musk' WHEN first_buy_time<={HIGH} THEN 'fenêtre' ELSE 'après' END c,count(*) FROM {WP} WHERE first_buy_time IS NOT NULL GROUP BY 1""")
q("C34 acheteurs de [visuel, borne basse), dont déjà acheteurs avant le visuel, dont dans les 6 h", f"""WITH a AS (SELECT DISTINCT owner FROM {TR} WHERE kind='swap' AND token_delta>0 AND block_time>={WIN} AND block_time<{LOW}),
    b AS (SELECT DISTINCT owner FROM {TR} WHERE kind='swap' AND token_delta>0 AND block_time<{WIN}), c AS (SELECT DISTINCT owner FROM {TR} WHERE kind='swap' AND token_delta>0 AND block_time>={WIN-21600} AND block_time<{WIN})
    SELECT (SELECT count(*) FROM a),(SELECT count(*) FROM a WHERE owner IN (SELECT owner FROM b)),(SELECT count(*) FROM a WHERE owner IN (SELECT owner FROM c))""")
# C35 sommet
vf = [str(p) for p in __import__("pathlib").Path(BIG + "/vault_shards").glob("*.parquet") if not p.name.startswith("._")]
con.execute(f"CREATE TEMP VIEW v AS SELECT DISTINCT * FROM read_parquet({vf!r})")
print("colonnes vault", [c[0] for c in con.execute("DESCRIBE SELECT * FROM v").fetchall()])
q("C35 sommet", f"""WITH t AS (SELECT slot,tx_index,block_time,max(CASE WHEN vault='{VT}' THEN post END) tok,max(CASE WHEN vault='{VS}' THEN post END) sol FROM v WHERE block_time>=1721606400 AND block_time<1721692800 GROUP BY 1,2,3)
    SELECT round(sol*1.0/tok*1e12/1e9*1e6/1e6,2),block_time,strftime(to_timestamp(block_time),'%H:%M:%S') FROM t WHERE tok IS NOT NULL AND sol IS NOT NULL ORDER BY sol*1.0/tok DESC LIMIT 1""")
q("C35 5QhJJc réalisé, sortis", f"SELECT round(realized_sol,2),round(transfer_out_qty/1e6,2) FROM {WP} WHERE owner='5QhJJcFZu2ashyKyWSTGHcsyo6ZBCbpVuJqeutvQHScd'")
# C36
fund = {}
for a in G:
    p = NET + a + ".jsonl.gz"
    if not os.path.exists(p): print("  pas d'historique", a); continue
    best = None
    with gzip.open(p, "rt") as fh:
        for l in fh:
            t = json.loads(l)
            for i_ in t["transaction"]["message"]["instructions"]:
                q_ = i_.get("parsed")
                if i_.get("program") == "system" and isinstance(q_, dict) and q_.get("type") == "transfer" and q_["info"]["destination"] == a and int(q_["info"]["lamports"]) >= 1_000_000:
                    k = (t["slot"], t.get("transactionIndex") or 0)
                    if best is None or k < best[0]: best = (k, q_["info"]["source"])
    fund[a] = best[1] if best else None
gs_ = set(G); G41 = "G41vRrsHShLEvwMj58ruhqJycGfAtWXxtLD56uFExL8E"
print("C36 premier financeur (>=0,001 SOL, instruction de 1er niveau) : historiques", len(fund), "dans le groupe", sum(1 for v in fund.values() if v in gs_), "G41", sum(1 for v in fund.values() if v == G41), "aucun", sum(1 for v in fund.values() if v is None), "CZsBW8yC", [fund[k][:8] for k in fund if k.startswith("CZsBW8yC")])
# C40, C42
q("C40 mon brut, lignes du groupe de visuel à borne haute", f"SELECT count(*) FROM {OW} WHERE owner IN (SELECT a FROM g) AND bt>={WIN} AND bt<={HIGH}")
q("C42 mouvements du groupe le 21/07 avant visuel, par plage", f"SELECT strftime(to_timestamp(min(bt)),'%H:%M:%S'),strftime(to_timestamp(max(bt)),'%H:%M:%S'),count(DISTINCT sig),round(sum(CASE WHEN d>0 THEN d ELSE 0 END)/1e12,2) FROM {OW} WHERE owner IN (SELECT a FROM g) AND bt>=1721519999 AND bt<{WIN} GROUP BY (bt-1721520000)/3600 ORDER BY 1")
# C43
rows = [r for r in csv.DictReader(open("etude_final/derived/metrics.csv")) if r["variant"] == "primary"]
print("C43 jours de pic, k+1", len({int(r["S"]) // 86400 for r in rows}), "pairs seuls", len({int(r["S"]) // 86400 for r in rows if r["is_dmaga"] != "True"}), "migrations", sum(1 for _ in open(BIG + "/controls/selection.jsonl")))
# C46, C47
f = json.load(open("etude_final/tables/funder_share.json"))
cmp_ = f["comparateurs"]; v_ = [c["part"] for c in cmp_]
print("C46 part DMAGA", f["dmaga"]["part"], "k", len(v_), "médiane", st.median(v_), ">=", sum(1 for x in v_ if x >= f["dmaga"]["part"]), "p", (1 + sum(1 for x in v_ if x >= f["dmaga"]["part"])) / (len(v_) + 1))
reg = [json.loads(l) for l in open("etude_final/registre/tests.jsonl")]
print("C47 registre lignes", len(reg), "réelles", sum(1 for r in reg if r["donnees"] != "synthetiques"), "comparaisons réelles", sum(r.get("n_comparaisons") or 0 for r in reg if r["donnees"] != "synthetiques"), "Bonferroni", 0.05 / 33)
pr = "0" * 64; ok = True
for r in reg:
    if r["prec"] != pr: ok = False
    pr = None
    pr = r.get("sha") or r.get("hash") or r.get("cle") or r.get("self") or pr
print("  clés registre", list(reg[0].keys()))
# C49 : gel
lk = json.load(open("etude_final/PROTOCOL.lock")); good = 0
for k, v in lk["fichiers"].items():
    p = os.path.normpath(os.path.join("etude_final", k))
    good += hashlib.sha256(open(p, "rb").read()).hexdigest() == v
print("C49 verrou", good, "sur", len(lk["fichiers"]), "gelé", lk["gele_le_utc"], "ajouts", [a["t_utc"] for a in lk.get("ajouts", [])], "premier réel registre", next(r["t_utc"] for r in reg if r["donnees"] != "synthetiques"))
# C51
q("C51 arêtes de lien avec nœud non wallet", f"SELECT count(*) FROM read_parquet('{BIG}/link_edges.parquet') e WHERE e.src IN (SELECT address FROM read_parquet('{BIG}/nodes.parquet') WHERE kind<>'wallet') OR e.dst IN (SELECT address FROM read_parquet('{BIG}/nodes.parquet') WHERE kind<>'wallet')")
from dmaga.venues import load as lv
ve = list(lv())
q("C51 arêtes avec réserve", f"SELECT count(*) FROM read_parquet('{BIG}/link_edges.parquet') WHERE src IN ({','.join(repr(x) for x in ve)}) OR dst IN ({','.join(repr(x) for x in ve)})")
q("C51 arêtes des 33 dans une tx avec un vault qui bouge", f"SELECT count(*) FROM ed WHERE s IN (SELECT sig FROM {TX} WHERE vt_d<>0 OR vs_d<>0)")
# A-05 résiduels
q("A-05 somme résiduels (M), hors pool à la fin ?", f"SELECT round(sum(residual_qty)/1e6,1),count(*) FROM {WP}")
for a in ("7gEQ6syDZmyPE4JdfJm4qatawnDqvqdh6i8jJjCXio6h", "HGs9NdwD2c4mYHb9fYdgp2Due5gbaSEdUV871wAiCkTd"):
    r = con.execute(f"SELECT round(residual_qty/1e6,3) FROM {WP} WHERE owner='{a}'").fetchone()
    b = con.execute(f"SELECT round(sum(p)/1e12,3) FROM (SELECT account,arg_max(post,(slot,idx)) p FROM {AC} WHERE owner='{a}' GROUP BY 1)").fetchone()
    print("  ", a[:8], "résiduel", r, "dernier solde vu dans mon brut", b)
q("A-05 dernier solde des réserves à la fin (M)", f"SELECT round(sum(p)/1e12,2),round(sum(CASE WHEN o IN ({','.join(repr(x) for x in ve)},'5Q544fKrFoe6tsEbD7S8EmxGTJYAKtTVhAW5Q5pge4j1','{CURVE}') THEN p ELSE 0 END)/1e12,2) FROM (SELECT account,arg_max(owner,(slot,idx)) o,arg_max(post,(slot,idx)) p FROM {AC} GROUP BY 1)")
# B-06 : courbe, retrait des soldes périmés
stale = {"6t2dz4jm3S8vJZCkWPhBxHStxFTC8wNV9QttTzfQrG7M": 26.388, "8YrEVPQqhs1zNsGUS5inFFqy5ziHaWdnVZXqysLThAh": 23.409, "99Xrt5uuu2FdsgGzKo3wvs28Bw2KuUgxaeV5rTQZLkb": 19.032, "AW63YBXXsGcLPpsDTSrpBMdQ9QXtxTiHsTbcVkY6UFv5": 15.442}
early = {r[0] for r in con.execute(f"SELECT DISTINCT owner FROM {SW} WHERE qty>0 AND t<{CRE+86400}").fetchall()}
buyers = {r[0] for r in con.execute(f"SELECT DISTINCT owner FROM {TR} WHERE kind='swap' AND token_delta>0 AND block_time<{CRE}").fetchall()}
print("B-06 sources périmées hors M6", {k[:8]: k not in early and k in buyers for k in stale}, "AtZjv3Du acheteur courbe", "AtZjv3DuV9cLn3Jxm72TMSdTN4aM6CrBaGyxUC4c2wDk" in buyers, "dans M6", "AtZjv3DuV9cLn3Jxm72TMSdTN4aM6CrBaGyxUC4c2wDk" in early)
print("   retirer du solde hors M6 : ", sum(v for k, v in stale.items() if k not in early and k in buyers))
act = next(json.loads(l) for l in open(BIG + "/controls/activity.jsonl") if '"CRSwXnfF21yHDXdYBVWwCwQ5Ni2A4QuK3qGYis5k7x7k"' in l)
h = act["hist"]; print("type hist", type(h).__name__, str(h)[:120])
if isinstance(h, dict):
    for hr in (13, 14, 15, 16, 17, 18, 19, 20):
        tt = 1721520000 + hr * 3600
        print("   21/07", hr, [h.get(str(k)) for k in (tt // 3600, tt, (tt - CRE) // 3600)])
