#!/usr/bin/env python3
"""Auditeur D. Effet réel des doublons (A-01), de l'autorité partagée (A-02) et des allers-retours (A-04) sur les chiffres du rapport.
Lecture seule de trades.parquet et wallets.parquet. PnL réécrit depuis la description du rapport, trois modes : 'tel' (tel quel, doit retomber sur wallets.parquet),
'dedup' (lignes identiques retirées), 'fix' (dedup + SOL du vault pour les lignes GpMZbSM2, ESTIMATION). Sorties : d40_trades.txt, d40_wallets.parquet (audits_work/D), d40_top_changes.csv."""
import csv, json, os, sys, time, collections
import duckdb
import pyarrow as pa, pyarrow.parquet as pq
BIG = "/Volumes/VERBATIM HD/Dark-MAGA-Investigation/data"
D = "/Volumes/VERBATIM HD/Dark-MAGA-Investigation/audits_work/D"
OUT = "audits/2026-11-03/work_D/"
con = duckdb.connect(":memory:", config={"memory_limit": "800MB", "threads": 2, "temp_directory": D + "/duck", "preserve_insertion_order": False})
con.execute("SET TimeZone='UTC'")
sys.stdout = open(OUT + "d40_trades.txt", "w")
T = f"read_parquet('{BIG}/trades.parquet')"
def q(n, s):
    r = con.execute(s).fetchall(); print(n, r, flush=True); return r
LOW, ENV, HIGH, BIDEN, WINIG = 1721588607, 1721589800, 1721590213, None, 1721577749
G = json.load(open("data/prevent_groups.json"))[0]["members"]
con.execute("CREATE TEMP TABLE g(a VARCHAR)"); con.executemany("INSERT INTO g VALUES (?)", [[x] for x in G])
# 1. doublons
con.execute(f"""CREATE TEMP TABLE dup AS SELECT signature,kind,owner,venue,token_delta,sol_lamports,source,block_time,count(*) n FROM {T}
                GROUP BY ALL HAVING count(*)>1""")
q("lignes, signatures", f"SELECT count(*),count(DISTINCT signature) FROM {T}")
q("groupes en double, lignes en trop, n max", "SELECT count(*),sum(n-1),max(n) FROM dup")
q("en trop par kind, source, SOL absolu en trop", "SELECT kind,source,sum(n-1),round(sum((n-1)*abs(sol_lamports))/1e9,2),round(sum((n-1)*CASE WHEN token_delta>0 THEN -sol_lamports ELSE 0 END)/1e9,2) achats,round(sum((n-1)*CASE WHEN token_delta<0 THEN sol_lamports ELSE 0 END)/1e9,2) ventes FROM dup GROUP BY 1,2 ORDER BY 3 DESC")
q("en trop par jour et source", "SELECT strftime(to_timestamp(block_time),'%Y-%m-%d') j,source,sum(n-1),round(sum((n-1)*abs(sol_lamports))/1e9,2) FROM dup GROUP BY 1,2 ORDER BY 3 DESC LIMIT 15")
q("plage de la source pool", "SELECT strftime(to_timestamp(min(block_time)),'%Y-%m-%d %H:%M:%S'),strftime(to_timestamp(max(block_time)),'%Y-%m-%d %H:%M:%S'),sum(n-1) FROM dup WHERE source='pool'")
q("en trop avant la borne haute de Musk", f"SELECT kind,source,sum(n-1),round(sum((n-1)*abs(sol_lamports))/1e9,3) FROM dup WHERE block_time<{HIGH} GROUP BY 1,2")
q("en trop dans les 24 h après Musk", f"SELECT kind,source,sum(n-1),round(sum((n-1)*abs(sol_lamports))/1e9,3),round(sum(CASE WHEN kind='swap' AND token_delta<0 THEN (n-1)*sol_lamports ELSE 0 END)/1e9,3) FROM dup WHERE block_time>={HIGH} AND block_time<{HIGH+86400} GROUP BY 1,2")
q("membres du groupe touchés", "SELECT owner,kind,sum(n-1),round(sum((n-1)*abs(sol_lamports))/1e9,3) FROM dup WHERE owner IN (SELECT a FROM g) GROUP BY 1,2")
# 2. autorité GpMZbSM2
# 2b. vault lu dans MON parseur (d01_tx), pas dans trades
TX = f"read_parquet('{D}/d01_tx.parquet')"
con.execute(f"""CREATE TEMP TABLE gp AS WITH v AS (SELECT sig, any_value(vs_d) vs, any_value(vt_d) vt FROM {TX} WHERE vs_d<>0 AND vt_d<>0 GROUP BY 1)
   SELECT t.signature,t.owner,t.kind,t.venue,t.token_delta,t.sol_lamports,t.usdc_raw,t.block_time,v.vs,v.vt FROM (SELECT DISTINCT signature,owner,kind,venue,token_delta,sol_lamports,usdc_raw,block_time FROM {T}) t JOIN v ON v.sig=t.signature
   WHERE ((t.kind='swap_other' AND coalesce(t.sol_lamports,0)=0) OR (t.kind='swap' AND t.venue LIKE '%GpMZbSM2%')) AND (t.token_delta>0)=(v.vt<0) AND (v.vs>0)=(v.vt<0)""")
q("A-02 swap_other au vault mobile : n, SOL vault, M jetons", "SELECT count(*),count(DISTINCT signature),round(sum(abs(vs))/1e9,1),round(sum(abs(token_delta))/1e12,1) FROM (SELECT * FROM gp WHERE kind='swap_other')")
q("A-02 swap GpMZ : n, écart absolu |SOL ligne - vault|, n écart > 1 %", "SELECT count(*),round(sum(abs(abs(sol_lamports+coalesce(usdc_raw,0)*0)-abs(vs)))/1e9,1),sum((abs(abs(sol_lamports)-abs(vs))>0.01*abs(vs))::int) FROM gp WHERE kind='swap'")
q("A-02 exemples", "SELECT signature,owner,kind,token_delta/1e6,sol_lamports/1e9,vs/1e9 FROM gp WHERE kind='swap_other' ORDER BY abs(vs) DESC LIMIT 3")
q("A-02 part dans 24 h après Musk : swap_other, SOL vault, sens vente, sens achat", f"SELECT round(sum(abs(vs))/1e9,2),round(sum(CASE WHEN vs<0 THEN -vs ELSE 0 END)/1e9,2),round(sum(CASE WHEN vs>0 THEN vs ELSE 0 END)/1e9,2),count(*) FROM gp WHERE kind='swap_other' AND block_time>={HIGH} AND block_time<{HIGH+86400}")
q("A-02 part dans 24 h après Musk : swap GpMZ, écart signé vente", f"SELECT round(sum(CASE WHEN vs<0 THEN -vs-sol_lamports ELSE 0 END)/1e9,2),round(sum(CASE WHEN vs>0 THEN vs+sol_lamports ELSE 0 END)/1e9,2),count(*) FROM gp WHERE kind='swap' AND block_time>={HIGH} AND block_time<{HIGH+86400}")
q("A-02 avant Musk : n, SOL", f"SELECT count(*),round(sum(abs(vs))/1e9,2) FROM gp WHERE block_time<{HIGH}")
q("A-02 membres du groupe et nommés", f"SELECT owner,kind,count(*),round(sum(abs(vs))/1e9,2) FROM gp WHERE owner IN (SELECT a FROM g) GROUP BY 1,2")
q("A-02 plus gros propriétaires", "SELECT owner,kind,count(*),round(sum(abs(vs))/1e9,2) FROM gp GROUP BY 1,2 ORDER BY 4 DESC LIMIT 8")
# 3. PnL trois modes, flux trié
print("démarrage PnL", flush=True)
import zipfile, io, glob
from array import array
M0 = 1717200000 // 60; px = array("f", [float("nan")]) * 1400000
for z in sorted(glob.glob("/Volumes/VERBATIM HD/Dark-MAGA-Investigation/raw/solusd/SOLUSDT-1m-*.zip")):
    if "/._" in z: continue
    with zipfile.ZipFile(z) as f, f.open(f.namelist()[0]) as fh:
        for row in csv.reader(io.TextIOWrapper(fh)):
            if row and row[0].isdigit():
                ms = int(row[0]); ms = ms // 1000 if ms > 10**14 else ms
                i = ms // 60000 - M0
                if 0 <= i < len(px): px[i] = float(row[4])
con.execute(f"""CREATE TEMP TABLE x AS SELECT e.signature,e.slot,e.block_time,e.src,e.dst,CAST(round(e.qty*1e6) AS BIGINT) q FROM read_parquet('{BIG}/token_edges.parquet') e
   WHERE e.how='gtba' AND e.dst<>'(multiple)' AND NOT EXISTS (SELECT 1 FROM {T} t WHERE t.signature=e.signature AND (t.owner=e.src OR t.owner=e.dst))""")
print("transferts gtba ajoutés", con.execute("SELECT count(*) FROM x").fetchone(), flush=True)
from dmaga.venues import load as lv
EX = {"5Q544fKrFoe6tsEbD7S8EmxGTJYAKtTVhAW5Q5pge4j1", "87g44hEXP7R8ZxoAJtz941tsVftpEXC1LqAFTf2ZHtkH", "39azUYFWPz3VHgKCf3VChUwbpURdCHRxjWVowf5jUJjg", "PNLCQcVCD26aC7ZWgRyr5ptfaR7bBrWdTFgRWwu2tvF"} | set(lv())
cur = con.execute(f"""WITH t AS (SELECT owner,slot,tx_index,block_time,kind,token_delta,sol_lamports,signature,venue,usdc_raw,
      row_number() OVER (PARTITION BY signature,kind,owner,venue,token_delta,sol_lamports,usdc_raw ORDER BY source) rn FROM {T}
      WHERE kind IN ('swap','lp_add','lp_remove','transfer','fee_share','swap_other') AND owner IS NOT NULL)
    SELECT t.owner,t.slot,t.tx_index,t.block_time,t.kind,t.token_delta,t.sol_lamports,t.usdc_raw,g.vs,g.vt,t.rn FROM t LEFT JOIN (SELECT DISTINCT signature,owner,kind,token_delta,vs,vt FROM gp) g
       ON g.signature=t.signature AND g.owner=t.owner AND g.kind=t.kind AND g.token_delta=t.token_delta
    UNION ALL SELECT src,slot,2147483647,block_time,'transfer',-q,0,0,NULL,NULL,1 FROM x
    UNION ALL SELECT dst,slot,2147483647,block_time,'transfer',q,0,0,NULL,NULL,1 FROM x
    ORDER BY 1,2,3""")
class W:
    __slots__ = "qty cost rl bq bs sq ss tin tout nob fb n_b n_s".split()
    def __init__(s):
        s.qty = 0; s.cost = 0.0; s.rl = 0.0; s.bq = s.bs = s.sq = s.ss = s.tin = s.tout = s.nob = 0; s.fb = None; s.n_b = s.n_s = 0
    def ap(s, k, d, v, t):
        if k == "swap":
            if d > 0:
                s.qty += d; s.cost += -v; s.bq += d; s.bs += -v; s.n_b += 1
                if s.fb is None: s.fb = t
            else:
                q_ = -d; kn = min(q_, max(s.qty, 0)); ba = s.cost / s.qty * kn if s.qty > 0 else 0.0
                s.rl += v - ba; s.cost -= ba; s.qty -= kn; s.nob += q_ - kn; s.sq += q_; s.ss += v; s.n_s += 1
        elif k in ("lp_add", "lp_remove"):
            if d < 0:
                q_ = -d; kn = min(q_, max(s.qty, 0))
                if s.qty > 0: s.cost -= s.cost / s.qty * kn
                s.qty -= kn
            else: s.qty += d
        else:
            if d > 0: s.qty += d; s.tin += d
            else:
                q_ = -d; kn = min(q_, max(s.qty, 0))
                if s.qty > 0: s.cost -= s.cost / s.qty * kn
                s.qty -= kn; s.tout += q_
SCH = pa.schema([("owner", pa.string())] + [(f"{m}_{c}", pa.float64()) for m in ("tel", "dedup", "fix") for c in ("realized", "bought", "sold", "bq", "sq", "tin", "nob", "fb", "qty")])
wr = pq.ParquetWriter(D + "/d40_wallets.parquet", SCH, compression="zstd"); buf = []
def flush():
    global buf
    if buf: wr.write_table(pa.Table.from_pylist(buf, schema=SCH)); buf = []
def emit(o, st):
    r = {"owner": o}
    for m, w in st.items():
        for c, v in (("realized", w.rl / 1e9), ("bought", w.bs / 1e9), ("sold", w.ss / 1e9), ("bq", w.bq), ("sq", w.sq), ("tin", w.tin), ("nob", w.nob), ("fb", w.fb), ("qty", w.qty)):
            r[f"{m}_{c}"] = v
    buf.append(r)
    if len(buf) >= 5000: flush()
own = None; st = None; rows = 0
fixed = 0
while True:
    b = cur.fetchmany(20000)
    if not b: break
    for o, sl, ix, t, k, d, v, us, vs, vt, rn in b:
        if o in EX: continue
        if us:
            p_ = px[t // 60 - M0]
            if p_ == p_: v = (v or 0) + int(us / 1e6 / p_ * 1e9)
        if o != own:
            if own is not None: emit(own, st)
            own = o; st = {"tel": W(), "dedup": W(), "fix": W()}
        rows += 1
        st["tel"].ap(k, d, v or 0, t)
        if rn == 1:
            st["dedup"].ap(k, d, v or 0, t)
            k2, v2 = k, v or 0
            if vs:
                # shortcut: SOL du vault réparti au prorata des jetons de la ligne ; ESTIMATION, à remplacer par une renormalisation complète
                share = min(1.0, abs(d) / abs(vt))
                v2 = int(-vs * share); k2 = "swap"; fixed += 1
            st["fix"].ap(k2, d, v2, t)
if own is not None: emit(own, st)
flush(); wr.close()
print("lignes traitées", rows, "lignes corrigées en fix", fixed, flush=True)
W_ = f"read_parquet('{D}/d40_wallets.parquet')"
Wp = f"read_parquet('{BIG}/wallets.parquet')"
q("écart tel/wallets.parquet (doit être 0) : n, sum|réalisé|", f"SELECT count(*),round(sum(abs(a.tel_realized-b.realized_sol)),6),sum((abs(a.tel_realized-b.realized_sol)>1e-6)::int),sum((abs(a.tel_bought-b.bought_sol)>1e-6)::int) FROM {W_} a JOIN {Wp} b USING(owner)")
for m in ("dedup", "fix"):
    q(f"{m} : wallets touchés, Σ|Δ réalisé|, Δ acheté, Δ vendu", f"SELECT sum((abs({m}_realized-tel_realized)>1e-6)::int),round(sum(abs({m}_realized-tel_realized)),2),round(sum(tel_bought-{m}_bought),2),round(sum(tel_sold-{m}_sold),2) FROM {W_}")
    q(f"{m} : entrés après Musk ({HIGH}), réalisé > 0 ; n", f"SELECT sum(({m}_fb>{HIGH})::int),sum(({m}_fb>{HIGH} AND {m}_realized>0)::int),sum(({m}_fb>{HIGH} AND {m}_realized>0.1)::int),sum(({m}_fb>={HIGH} AND {m}_realized>0)::int),sum(({m}_fb>={HIGH})::int) FROM {W_}")
q("tel : idem", f"SELECT sum((tel_fb>{HIGH})::int),sum((tel_fb>{HIGH} AND tel_realized>0)::int),sum((tel_fb>={HIGH} AND tel_realized>0)::int),sum((tel_fb>={HIGH})::int) FROM {W_}")
NAM = {"7Mjg8z2FxJTcsLfqPxeiYkP6Sv1FxiPT1DUNDpM1hVk3", "H3QsBrrivimFJmSpTXuvig2n1Bh7JuYxrriRSEszT6cc", "GXZvXsD6hxaLeFvQisWpdAwsayJxga7w9EeafhFZG2Ra", "9PrmF8sfoD2YShtWUghrGEYgxwabpnzog8gT1V6LEtdq", "5QhJJcFZu2ashyKyWSTGHcsyo6ZBCbpVuJqeutvQHScd", "8YLEuUtZ4eFMJbf46oNb1CeG6dYFWGyxnQSh9hrgzBzR", "DswkYbBhvzYnAUm9dqBiRBYvW1YJyUvEg5eVNBGmZoTe", "ET8ZG5zAcEA4n1bNN5B5MkeStCGw7T1f6ZJwwH7G3rMB", "Akp46DicpTMb9aDtZozTViYydsYH5NhcZACWokpzLaNB", "C7i9beNHXYonZYB5riXE6kaLpFWLj9BPzh2FSBoUUePK", "5FzhCSWLT84QdgX9wYWWuWY1ZY3G9kMUu2fRifxLLhmx"}
print("nommés", [(r[0][:8], round(r[1], 2), round(r[2], 2), round(r[3], 2)) for r in con.execute(f"SELECT owner,tel_realized,dedup_realized,fix_realized FROM {W_} WHERE owner IN ({','.join(repr(x) for x in NAM)})").fetchall()])
q("groupe de 33 : réalisé tel, dedup, fix ; acheté", f"SELECT round(sum(tel_realized),1),round(sum(dedup_realized),1),round(sum(fix_realized),1),round(sum(tel_bought),1),round(sum(dedup_bought),1) FROM {W_} WHERE owner IN (SELECT a FROM g)")
q("plus gros écarts fix-tel", f"SELECT owner,round(tel_realized,1),round(dedup_realized,1),round(fix_realized,1) FROM {W_} ORDER BY abs(fix_realized-tel_realized) DESC LIMIT 12")
# classement coût connu : même règle que rep_70 (filtre 5 %), mêmes exclusions via liste du fichier nodes
con.execute(f"CREATE TEMP TABLE excl AS SELECT address a FROM read_parquet('{BIG}/nodes.parquet') WHERE kind<>'wallet'")
def top(m):
    return [r[0] for r in con.execute(f"""SELECT owner FROM {W_} WHERE owner NOT IN (SELECT a FROM excl) AND {m}_nob<=0.05*greatest({m}_sq,1) AND {m}_tin<=0.05*greatest({m}_bq+{m}_tin,1) ORDER BY {m}_realized DESC LIMIT 100""").fetchall()]
t0, t1, t2 = top("tel"), top("dedup"), top("fix")
print("top 100 : commun tel/dedup", len(set(t0) & set(t1)), "tel/fix", len(set(t0) & set(t2)), "top 10 identique dedup", t0[:10] == t1[:10], "fix", t0[:10] == t2[:10], "top 5 tel", [x[:8] for x in t0[:5]])
print("entrants dedup", [x[:8] for x in t1 if x not in t0], "sortants", [x[:8] for x in t0 if x not in t1])
print("entrants fix", [x[:8] for x in t2 if x not in t0], "sortants", [x[:8] for x in t0 if x not in t2])
w2 = csv.writer(open(OUT + "d40_top_changes.csv", "w", newline="")); w2.writerow("owner rang_tel rang_dedup rang_fix realise_tel realise_dedup realise_fix".split())
vals = {r[0]: r[1:] for r in con.execute(f"SELECT owner,tel_realized,dedup_realized,fix_realized FROM {W_}").fetchall() if r[0] in set(t0) | set(t1) | set(t2)}
for o in dict.fromkeys(t0 + t1 + t2):
    r = (t0.index(o) + 1 if o in t0 else "", t1.index(o) + 1 if o in t1 else "", t2.index(o) + 1 if o in t2 else "")
    if r[0] != r[1] or r[0] != r[2]:
        w2.writerow([o, *r, *[round(x, 2) for x in vals[o]]])
# 4. chiffres de fenêtre du rapport, tel quel, dédoublonné, corrigé
base = f"""(SELECT *, row_number() OVER (PARTITION BY signature,kind,owner,venue,token_delta,sol_lamports ORDER BY source) rn FROM {T} WHERE kind IN ('swap','swap_other'))"""
con.execute(f"CREATE TEMP VIEW b AS SELECT * FROM {base}")
def win(name, a, z):
    r = con.execute(f"""SELECT
      round(sum(CASE WHEN kind='swap' AND token_delta>0 THEN -sol_lamports ELSE 0 END)/1e9,3) ach_tel,
      round(sum(CASE WHEN kind='swap' AND token_delta<0 THEN sol_lamports ELSE 0 END)/1e9,3) ven_tel,
      round(sum(CASE WHEN rn=1 AND kind='swap' AND token_delta>0 THEN -sol_lamports ELSE 0 END)/1e9,3) ach_dedup,
      round(sum(CASE WHEN rn=1 AND kind='swap' AND token_delta<0 THEN sol_lamports ELSE 0 END)/1e9,3) ven_dedup,
      (SELECT round(coalesce(sum(CASE WHEN vs>0 THEN vs ELSE 0 END),0)/1e9,3) FROM gp WHERE kind='swap_other' AND block_time>={a} AND block_time<{z}) ach_manquant,
      (SELECT round(coalesce(sum(CASE WHEN vs<0 THEN -vs ELSE 0 END),0)/1e9,3) FROM gp WHERE kind='swap_other' AND block_time>={a} AND block_time<{z}) ven_manquant
      FROM b WHERE block_time>={a} AND block_time<{z}""").fetchone()
    print(name, dict(zip("ach_tel ven_tel ach_dedup ven_dedup ach_manquant ven_manquant".split(), r)), flush=True)
win("C05 borne basse -> envoi", LOW, ENV)
win("C05 envoi -> borne haute", ENV, HIGH)
win("C05 heure suivante", HIGH, HIGH + 3600)
win("C06 Biden -> borne basse", LOW - int(1.29 * 3600) - 300, LOW)
win("C15 24 h après Musk", HIGH, HIGH + 86400)
win("3 h avant envoi", ENV - 10800, ENV)
win("3 h avant Winig", WINIG - 10800, WINIG)
q("C15 groupe, ventes 24 h, tel et dedup", f"SELECT round(sum(CASE WHEN kind='swap' AND token_delta<0 THEN sol_lamports ELSE 0 END)/1e9,2),round(sum(CASE WHEN rn=1 AND kind='swap' AND token_delta<0 THEN sol_lamports ELSE 0 END)/1e9,2),round(sum(CASE WHEN rn=1 AND kind='swap' AND token_delta<0 THEN -token_delta ELSE 0 END)/1e12,3) FROM b WHERE block_time>={HIGH} AND block_time<{HIGH+86400} AND owner IN (SELECT a FROM g)")
