#!/usr/bin/env python3
"""Auditeur D. B-06 (angles morts, net contre brut), C30 (virements G41vRrsH relus dans son historique brut), grappes antérieures de C-02, A-03 (origine des fonds). Sortie d44_misc.txt."""
import csv, gzip, json, os, sys, time, collections
import duckdb
D = "/Volumes/VERBATIM HD/Dark-MAGA-Investigation/audits_work/D"; BIG = "/Volumes/VERBATIM HD/Dark-MAGA-Investigation/data"; NET = "/Volumes/VERBATIM HD/Dark-MAGA-Investigation/audits_work/C/net/"
OUT = "audits/2026-11-03/work_D/"
con = duckdb.connect(":memory:", config={"memory_limit": "700MB", "threads": 2, "temp_directory": D + "/duck", "preserve_insertion_order": False})
con.execute("SET TimeZone='UTC'")
sys.stdout = open(OUT + "d44_misc.txt", "w")
def q(n, s):
    r = con.execute(s).fetchall(); print(n, r, flush=True); return r
AC = f"read_parquet('{D}/d01_acct.parquet')"; OW = f"read_parquet('{D}/d01_own.parquet')"; TR = f"read_parquet('{BIG}/trades.parquet')"; EDG = f"read_parquet('{BIG}/token_edges.parquet')"
SW = f"read_parquet('{BIG}/controls/swaps/CRSwXnfF21yHDXdYBVWwCwQ5Ni2A4QuK3qGYis5k7x7k.parquet')"
T0, CRE, S, LOW, HIGH = 1720922725, 1720923331, 1721588400, 1721588607, 1721590213
iso = lambda t: time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(t))
G = json.load(open("data/prevent_groups.json"))[0]["members"]
con.execute("CREATE TEMP TABLE g(a VARCHAR)"); con.executemany("INSERT INTO g VALUES (?)", [[x] for x in G])
CURVE = "87g44hEXP7R8ZxoAJtz941tsVftpEXC1LqAFTf2ZHtkH"
# B-06 courbe
con.execute(f"""CREATE TEMP TABLE cu AS SELECT owner,sum(CASE WHEN d>0 THEN d ELSE 0 END) b,sum(CASE WHEN d<0 THEN -d ELSE 0 END) s FROM (SELECT DISTINCT sig,owner,d FROM {OW} WHERE src='curve' AND owner<>'{CURVE}') GROUP BY 1""")
q("courbe : wallets avec delta DMAGA, achat brut M, vente brute M", "SELECT count(*),sum((b>0)::int),round(sum(b)/1e12,2),round(sum(s)/1e12,2) FROM cu")
con.execute(f"""CREATE TEMP TABLE curvebuy AS SELECT owner,sum(token_delta) b,count(*) n FROM (SELECT DISTINCT signature,owner,token_delta FROM {TR} WHERE kind='swap' AND token_delta>0 AND block_time<{CRE}) GROUP BY 1""")
q("achats avant migration (trades) : wallets, M brut", "SELECT count(*),round(sum(b)/1e12,2) FROM curvebuy")
con.execute(f"CREATE TEMP TABLE early AS SELECT DISTINCT owner FROM {SW} WHERE qty>0 AND t<{CRE+86400}")
con.execute(f"""CREATE TEMP TABLE bal_S AS SELECT owner,sum(bal) v FROM (SELECT account,arg_max(owner,(slot,idx)) owner,arg_max(post,(slot,idx)) bal FROM (SELECT DISTINCT sig,slot,idx,bt,account,owner,pre,post FROM {AC} WHERE bt<{S}) GROUP BY 1) GROUP BY 1""")
q("acheteurs courbe hors M6 : n, achat brut M, solde à S M ; dans M6 : n, brut, solde", """SELECT (c.owner IN (SELECT owner FROM early)) m6,count(*),round(sum(c.b)/1e12,2),round(sum(coalesce(s.v,0))/1e12,2) FROM curvebuy c LEFT JOIN bal_S s USING(owner) GROUP BY 1""")
q("  dont solde à S >= 1 M, hors M6", """SELECT count(*),round(sum(v)/1e12,2) FROM curvebuy c JOIN bal_S s USING(owner) WHERE c.owner NOT IN (SELECT owner FROM early) AND v>=1e12""")
q("  groupe de 33 parmi eux : n, solde", """SELECT count(*),round(sum(v)/1e12,2) FROM curvebuy c JOIN bal_S s USING(owner) WHERE c.owner NOT IN (SELECT owner FROM early) AND c.owner IN (SELECT a FROM g)""")
# mais l'intervention de transferts : solde à S corrigé des 84,5 M périmés de 4 sources
q("  sources périmées dans cet ensemble (transferts vers AtZjv3Du) : solde", "SELECT owner,round(v/1e12,2) FROM bal_S WHERE owner IN ('6t2dz4jm3S8vJZCkWPhBxHStxFTC8wNV9QttTzfQrG7M','8YrEVPQqhs1zNsGUS5inFFqy5ziHaWdnVZXqysLThAh','99Xrt5uuu2FdsgGzKo3wvs28Bw2KuUgxaeV5rTQZLkb','AW63YBXXsGcLPpsDTSrpBMdQ9QXtxTiHsTbcVkY6UFv5')")
# transferts reçus 24 h avant S : brut contre net
con.execute(f"""CREATE TEMP TABLE xf AS SELECT DISTINCT signature,owner,token_delta d,kind FROM {TR} WHERE kind='transfer' AND block_time>={S-86400} AND block_time<{S}""")
q("transferts 24 h avant S, reçus : M, wallets ; envoyés M", "SELECT round(sum(CASE WHEN d>0 THEN d ELSE 0 END)/1e12,2),count(DISTINCT CASE WHEN d>0 THEN owner END),round(sum(CASE WHEN d<0 THEN -d ELSE 0 END)/1e12,2) FROM xf")
q("  solde net positif par wallet (M), wallets", "SELECT round(sum(n)/1e12,2),count(*) FROM (SELECT owner,sum(d) n FROM xf GROUP BY 1) WHERE n>0")
q("  part reçue par le groupe, envoyée par le groupe", "SELECT round(sum(CASE WHEN d>0 AND owner IN (SELECT a FROM g) THEN d ELSE 0 END)/1e12,2),round(sum(CASE WHEN d<0 AND owner IN (SELECT a FROM g) THEN -d ELSE 0 END)/1e12,2) FROM xf")
q("  net par wallet, top", "SELECT owner,round(sum(d)/1e12,2) n FROM xf GROUP BY 1 ORDER BY n DESC LIMIT 6")
# heure de S, S-5h activité
sel = next(json.loads(l) for l in open(BIG + "/controls/selection.jsonl") if '"CRSwXnfF21yHDXdYBVWwCwQ5Ni2A4QuK3qGYis5k7x7k"' in l)
act = next(json.loads(l) for l in open(BIG + "/controls/activity.jsonl") if '"CRSwXnfF21yHDXdYBVWwCwQ5Ni2A4QuK3qGYis5k7x7k"' in l)
H = {int(k): v for k, v in act["hist"].items()} if isinstance(act["hist"], dict) else {}
hs = sorted(H)
print("activité: heures listées", len(H), "exemple clés", hs[:2])
for h in range(0, 24):
    t = 1721520000 + h * 3600
    for key in (t // 3600, t):
        if key in H: print("  21/07", f"{h:02d}:00", H[key], end=";")
print()
q("achats [S,S+1 h) swaps gelés SOL", f"SELECT round(sum(-sol)/1e9,1),count(*) FROM {SW} WHERE qty>0 AND t>={S} AND t<{S+3600}")
# C30 : historique brut de G41vRrsH
G41 = "G41vRrsHShLEvwMj58ruhqJycGfAtWXxtLD56uFExL8E"
out = []
seen = set()
with gzip.open(NET + G41 + ".jsonl.gz", "rt") as fh:
    for l in fh:
        t = json.loads(l); s = t["transaction"]["signatures"][0]
        if s in seen: continue
        seen.add(s)
        for i in t["transaction"]["message"]["instructions"]:
            p = i.get("parsed")
            if i.get("program") == "system" and isinstance(p, dict) and p.get("type") == "transfer" and p["info"]["source"] == G41:
                out.append((t["blockTime"], p["info"]["destination"], int(p["info"]["lamports"]), s))
out.sort()
five = [x for x in out if x[2] == 500_000_000]
print("G41 virements système", len(out), "exacts 0,5 SOL", len(five), "fenêtre 01:46-02:04 :", sum(1 for x in five if T0 - 1200 <= x[0] < T0))
win = [x for x in five if T0 - 1200 <= x[0] < T0]
print("  premier", iso(win[0][0]), "dernier", iso(win[-1][0]), "autres 0,5", [iso(x[0]) for x in five if x not in win])
con.execute("CREATE TEMP TABLE w13(a VARCHAR)"); con.executemany("INSERT INTO w13 VALUES (?)", [[x[1]] for x in win])
q("  destinataires distincts", "SELECT count(DISTINCT a) FROM w13")
buy = con.execute(f"SELECT owner,sum(token_delta)/1e12,count(*) FROM (SELECT DISTINCT signature,owner,token_delta FROM {TR} WHERE kind='swap' AND token_delta>0 AND owner IN (SELECT a FROM w13)) GROUP BY 1").fetchall()
print("  ayant un achat swap (trades)", len(buy), "donc sans achat", len({x[1] for x in win}) - len(buy))
oo = con.execute(f"SELECT DISTINCT owner FROM {OW} WHERE d>0 AND owner IN (SELECT a FROM w13)").fetchall()
print("  recevant du DMAGA de quelque façon dans mon brut", len(oo))
nb = [x[1] for x in win if x[1] not in {b[0] for b in buy}]
print("  sans achat :", nb)
print("  créateur, membres ? dans groupe", sum(1 for x in win if x[1] in set(G)))
# 2 wallets financés 65 minutes avant
tab = {r["wallet"]: r for r in csv.DictReader(open("audits/2026-11-03/work_C/members_table.csv"))}
# financement antérieur : 74qFhHyp -> 6t2dz4jm 00:52:29, 8YrEVPQq, 99Xrt5uu
for a in ("6t2dz4jm3S8vJZCkWPhBxHStxFTC8wNV9QttTzfQrG7M", "8YrEVPQqhs1zNsGUS5inFFqy5ziHaWdnVZXqysLThAh", "99Xrt5uuu2FdsgGzKo3wvs28Bw2KuUgxaeV5rTQZLkb"):
    r = []
    with gzip.open(NET + a + ".jsonl.gz", "rt") as fh:
        for l in fh:
            t = json.loads(l)
            for i in t["transaction"]["message"]["instructions"]:
                p = i.get("parsed")
                if i.get("program") == "system" and isinstance(p, dict) and p.get("type") == "transfer" and p["info"]["destination"] == a and int(p["info"]["lamports"]) >= 1_000_000:
                    r.append((t["blockTime"], p["info"]["source"], int(p["info"]["lamports"]) / 1e9))
    r.sort()
    print("  premiers reçus", a[:8], [(iso(x[0]), x[1][:8], x[2]) for x in r[:3]], "avant mint s", T0 - r[0][0] if r else None)
# grappes antérieures : SOL entre membres avant le 13/06/2024
ge = collections.Counter(); first = {}
Gs = set(G)
for a in G:
    p = NET + a + ".jsonl.gz"
    if not os.path.exists(p): print("pas d'historique", a); continue
    with gzip.open(p, "rt") as fh:
        for l in fh:
            t = json.loads(l)
            if t["blockTime"] >= T0: continue
            for i in t["transaction"]["message"]["instructions"]:
                q_ = i.get("parsed")
                if i.get("program") == "system" and isinstance(q_, dict) and q_.get("type") == "transfer":
                    s_, d_, v_ = q_["info"]["source"], q_["info"]["destination"], int(q_["info"]["lamports"])
                    if s_ in Gs and d_ in Gs and v_ >= 1_000_000:
                        k = tuple(sorted((s_[:8], d_[:8]))); ge[k] += 1; first[k] = min(first.get(k, 9e12), t["blockTime"])
print("liens SOL entre membres avant le mint (>=0,001 SOL), paires", len(ge))
for k, v in sorted(first.items(), key=lambda kv: kv[1])[:14]: print("  ", iso(v), k, ge[k])
adj = collections.defaultdict(set)
for k in ge: adj[k[0]].add(k[1]); adj[k[1]].add(k[0])
seen_ = set(); comps = []
for x in adj:
    if x in seen_: continue
    st = [x]; cc = set()
    while st:
        y = st.pop()
        if y in cc: continue
        cc.add(y); st += adj[y]
    seen_ |= cc; comps.append(sorted(cc))
print("composantes SOL pré-mint", [len(c) for c in comps], comps)
# A-03
FE = f"read_parquet('{BIG}/funding_edges.parquet')"
Y0 = T0 - 365 * 86400
q("financement niveau 0, 12 mois avant le mint, décimales saines : classe, n, SOL, part", f"""WITH t AS (SELECT DISTINCT wallet,src,sol,block_time,signature,src_label,is_pool FROM {FE} WHERE level=0 AND block_time>={Y0} AND block_time<{T0} AND sol<1e6),
  c AS (SELECT *, CASE WHEN is_pool THEN 'pool' WHEN src_label IS NULL OR src_label='' THEN 'sans_etiquette' WHEN regexp_matches(lower(src_label),'jupiter') THEN 'jupiter' WHEN regexp_matches(lower(src_label),'binance|coinbase|okx|bybit|kucoin|mexc|kraken|gate|bitget|huobi|htx|crypto.com|bitfinex|cex|exchange') THEN 'echange' ELSE 'autre:'||src_label END k FROM t)
  SELECT regexp_replace(k,':.*',''),count(*),count(DISTINCT wallet),round(sum(sol)),round(100*sum(sol)/(SELECT sum(sol) FROM c),1) FROM c GROUP BY 1 ORDER BY 4 DESC""")
FAM = ["FpwQQhQQoEaVu3WU2qZMfF1hx48YyfwsLoRgXG83E99Q", "D89hHJT5Aqyx1trP6EnGY9jJUB3whgnq3aUvvCqedvzf", "9obNtb5GyUegcs3a1CbBkLuc5hEWynWfJC6gjz5uWQkE", "DPqsobysNf5iA9w7zrQM8HLzCKZEDMkZsWbiidsAt1xo", "4NyK1AdJBNbgaJ9EsKz3J4rfeHsuYdjkTPg3JaNdLeFw", "8JUEoHNMbWM4eegcMvx6ZQJt3V3fbo8JNjpWiCtJgxfF", "5g7yNHyGLJ7fiQ9SN9mf47opDnMjc585kqXWt6d7aBWs"]
L = ",".join(repr(x) for x in FAM)
q("sans étiquette : SOL depuis la famille Coinbase non étiquetée (C-03 et D)", f"SELECT round(sum(sol)),count(DISTINCT wallet) FROM (SELECT DISTINCT wallet,src,sol,block_time,signature FROM {FE} WHERE level=0 AND block_time>={Y0} AND block_time<{T0} AND sol<1e6 AND src IN ({L}) AND NOT is_pool)")
q("sans étiquette : sources à >= 15 wallets, 2024 : n sources, SOL ; part de la classe", f"""WITH t AS (SELECT DISTINCT wallet,src,sol,signature FROM {FE} WHERE level=0 AND block_time>={Y0} AND block_time<{T0} AND sol<1e6 AND NOT is_pool AND (src_label IS NULL OR src_label='')), a AS (SELECT src,count(DISTINCT wallet) w,sum(sol) s FROM t GROUP BY 1)
   SELECT count(*),round(sum(s)),round(100*sum(s)/(SELECT sum(s) FROM a),1) FROM a WHERE w>=15""")
q("  top sources sans étiquette (wallets, SOL)", f"""WITH t AS (SELECT DISTINCT wallet,src,sol,signature FROM {FE} WHERE level=0 AND block_time>={Y0} AND block_time<{T0} AND sol<1e6 AND NOT is_pool AND (src_label IS NULL OR src_label='')) SELECT src,count(DISTINCT wallet) w,round(sum(sol)) s FROM t GROUP BY 1 ORDER BY w DESC LIMIT 8""")
q("  top sources sans étiquette par SOL", f"""WITH t AS (SELECT DISTINCT wallet,src,sol,signature FROM {FE} WHERE level=0 AND block_time>={Y0} AND block_time<{T0} AND sol<1e6 AND NOT is_pool AND (src_label IS NULL OR src_label='')) SELECT src,count(DISTINCT wallet) w,round(sum(sol)) s FROM t GROUP BY 1 ORDER BY s DESC LIMIT 6""")
