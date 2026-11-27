#!/usr/bin/env python3
"""Point 2. Origine du SOL des 5 financeurs, receveurs, fusion des grappes dans le temps, gestes du 21/07/2024 et suite. Lit net_flows, net_txs, edges40_replay. Sorties g32.txt, g32_merge.csv, g32_gestes.csv, g32_origin.csv."""
import csv, sys, time, collections, json
import duckdb
from dmaga.labels import label
OUT = "audits/2026-11-03/work_G/"; G = "/Volumes/VERBATIM HD/Dark-MAGA-Investigation/audits_work/G/"
sys.stdout = open(OUT + "g32.txt", "w")
MINT_T = 1720922725; MUSK = 1721588607
con = duckdb.connect(":memory:", config={"memory_limit": "600MB", "threads": 2, "temp_directory": G + "duck"})
con.execute(f"CREATE TABLE f AS SELECT * FROM read_parquet('{G}net_flows.parquet')")
con.execute("SET TimeZone='UTC'")
iso = lambda t: time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(t))
F5 = ["G41vRrsHShLEvwMj58ruhqJycGfAtWXxtLD56uFExL8E", "74qFhHypY1zi8oS2KahqmwLfV8zMVbBiJ8uDdki8xPEb", "AtZjv3DuV9cLn3Jxm72TMSdTN4aM6CrBaGyxUC4c2wDk", "NxtXcmEW3gQvrCdBEm5GYT3zaqMre3QiPUhnwViNsD7", "GFpqfjEQFhXRbWEJCwUqKuNjSNTCgqAsANMbVyTGmi1p"]
w = csv.writer(open(OUT + "g32_origin.csv", "w", newline="")); w.writerow("wallet phase dir asset cp label n montant premier dernier signature".split())
for A in F5:
    print("==", A)
    for ph, cond in (("avant_mint", f"bt<{MINT_T}"), ("mint_a_musk", f"bt>={MINT_T} AND bt<{MUSK}")):
        for dr in ("in", "out"):
            rows = con.execute(f"""SELECT cp,asset,count(*),sum(amt),min(bt),max(bt),min(sig) FROM f WHERE owner=? AND dir='{dr}' AND pure=1 AND asset IN ('SOL','USDC','USDT') AND amt>=0.01 AND {cond} GROUP BY 1,2 ORDER BY 2,4 DESC""", [A]).fetchall()
            tot = collections.Counter()
            for r in rows:
                tot[r[1]] += r[3]; w.writerow([A, ph, dr, r[1], r[0], label(r[0]) or "", r[2], round(r[3], 4), iso(r[4]), iso(r[5]), r[6]])
            print(f"  {ph} {dr} {dict((k, round(v, 2)) for k, v in tot.items())} contreparties {len(rows)} ; top", [(r[0][:8], (label(r[0]) or "")[:10], r[2], round(r[3], 2)) for r in rows[:7]])
    r = con.execute("SELECT min(bt) FROM f WHERE owner=?", [A]).fetchone()
    fi = con.execute("SELECT bt,cp,amt,sig FROM f WHERE owner=? AND dir='in' AND asset='SOL' AND amt>=0.001 ORDER BY bt LIMIT 1", [A]).fetchone()
    print("  premier financeur", iso(fi[0]), fi[1], label(fi[1]), fi[2], fi[3])
# fusion des grappes
T = {r["wallet"]: r["roles"] for r in csv.DictReader(open(OUT + "targets.csv"))}
con.execute("CREATE TABLE t(a VARCHAR)"); con.executemany("INSERT INTO t VALUES (?)", [[a] for a in T])
E = con.execute(f"""SELECT bt,owner,cp,asset,amt,sig,dir FROM f WHERE owner IN (SELECT a FROM t) AND cp IN (SELECT a FROM t) AND pure=1 AND bt<{MUSK} AND ((asset='SOL' AND amt>=0.05) OR (asset IN ('USDC','USDT') AND amt>=5) OR asset='DMAGA' AND amt>=100000) ORDER BY bt""").fetchall()
par = {a: a for a in T}
def fd(x):
    while par[x] != x:
        par[x] = par[par[x]]; x = par[x]
    return x
size = collections.Counter({a: 1 for a in T})
mg = csv.writer(open(OUT + "g32_merge.csv", "w", newline="")); mg.writerow("utc a b actif montant signature taille_avant_a taille_avant_b taille_apres avant_mint".split())
seen = set()
for bt, o, c, asset, amt, s, dr in E:
    a, b = (o, c) if dr == "out" else (c, o)
    if (s, a, b) in seen: continue
    seen.add((s, a, b))
    ra, rb = fd(a), fd(b)
    if ra != rb:
        mg.writerow([iso(bt), a, b, asset, round(amt, 4), s, size[ra], size[rb], size[ra] + size[rb], bt < MINT_T])
        par[ra] = rb; size[rb] += size[ra]
comp = collections.Counter(fd(a) for a in T)
print("composantes à Musk (cibles, pur SOL>=0,05, USD>=5, DMAGA>=100k)", sorted(comp.values(), reverse=True)[:12])
for a in F5: print("  ", a[:8], "taille comp.", size[fd(a)])
# état avant mint seulement
par = {a: a for a in T}; size = collections.Counter({a: 1 for a in T})
for bt, o, c, asset, amt, s, dr in E:
    if bt >= MINT_T: break
    a, b = (o, c) if dr == "out" else (c, o)
    ra, rb = fd(a), fd(b)
    if ra != rb: par[ra] = rb; size[rb] += size[ra]
groups = collections.defaultdict(list)
for a in T: groups[fd(a)].append(a[:8])
print("composantes avant mint", sorted((sorted(v) for v in groups.values() if len(v) > 1), key=len, reverse=True))
# gestes du 21/07
E40 = [r for r in csv.DictReader(open("audits/2026-11-03/work_C/edges40_replay.csv")) if r["utc"].startswith("2024-07-21")]
print("arêtes du 21/07 dans les 40", len(E40))
g = csv.writer(open(OUT + "g32_gestes.csv", "w", newline="")); g.writerow("utc src dst tokens_M signature".split())
for r in E40: g.writerow([r["utc"], r["src"], r["dst"], r["tokens_M"], r["sig"]]); print("  ", r["utc"][11:19], r["src"][:8], "->", r["dst"][:8], r["tokens_M"], r["sig"][:12])
# suite : ce que les wallets des gestes font ensuite, 7 jours, jetons vendus, SOL sortants
W = sorted({r["src"] for r in E40} | {r["dst"] for r in E40})
t0 = min(int(time.mktime(time.strptime(r["utc"], "%Y-%m-%dT%H:%M:%SZ"))) - time.timezone for r in E40)
con.execute("CREATE TABLE w(a VARCHAR)"); con.executemany("INSERT INTO w VALUES (?)", [[a] for a in W])
con.execute(f"CREATE TABLE tx AS SELECT * FROM read_csv('{G}net_txs.csv.gz',header=true,types={{'sig':'VARCHAR','owner':'VARCHAR','programs':'VARCHAR','signers':'VARCHAR','payer':'VARCHAR'}}) WHERE owner IN (SELECT a FROM w)")
print("wallets des gestes", len(W))
for a in W:
    sell = con.execute(f"SELECT count(*),sum(dmaga_delta)/1e6,sum(native_delta+wsol_delta)/1e9,sum(usdc_delta+usdt_delta)/1e6 FROM tx WHERE owner=? AND dmaga_delta<0 AND pure=0 AND bt>={t0} AND bt<{t0+7*86400}", [a]).fetchone()
    out = con.execute(f"SELECT cp,asset,sum(amt),min(bt) FROM f WHERE owner=? AND dir='out' AND pure=1 AND asset IN ('SOL','USDC','USDT','DMAGA') AND bt>={t0} AND bt<{t0+7*86400} AND amt>=(CASE WHEN asset='DMAGA' THEN 100000 WHEN asset='SOL' THEN 0.1 ELSE 10 END) GROUP BY 1,2 ORDER BY 3 DESC LIMIT 6", [a]).fetchall()
    print(" ", a[:8], "ventes 7 j : n", sell[0], "jetons M", round(sell[1] or 0, 3), "SOL", round(sell[2] or 0, 2), "USD", round(sell[3] or 0, 1), "| sorties", [(x[0][:8], x[1], round(x[2], 1)) for x in out])
