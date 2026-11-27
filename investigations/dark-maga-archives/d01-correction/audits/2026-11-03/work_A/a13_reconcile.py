#!/usr/bin/env python3
"""Auditeur A. Réconciliation : signatures contre transactions, échecs, chaînes de soldes, comparaison à trades.parquet.
Tout passe par DuckDB (800 Mo, 2 fils). Entrées : parquets de a01 et a02 dans audits_work/A. Sortie : stdout, à rediriger vers out/."""
import duckdb, json
A = "/Volumes/VERBATIM HD/Dark-MAGA-Investigation/audits_work/A"
B = "/Volumes/VERBATIM HD/Dark-MAGA-Investigation/data"
VT, VS = "5HuEsLbebeuottMsFW3hHcXTrKVsu3WUNSQnSr6aX4eL", "3p7DbnWekWjtMQkey6fp1emdwXbAAxecnYuD5eU9ZZPH"
AUTH = "5Q544fKrFoe6tsEbD7S8EmxGTJYAKtTVhAW5Q5pge4j1"
S = 1721588400
con = duckdb.connect(":memory:", config={"memory_limit": "800MB", "threads": 2, "temp_directory": A + "/duck13", "preserve_insertion_order": False})
con.execute("SET TimeZone='UTC'")
q = lambda s: con.execute(s).fetchall()
def show(name, s):
    print(name, q(s), flush=True)
for n in ("curve", "pool", "mint"):
    show(f"sigs_{n} total/distinct/échouées/réussies", f"SELECT count(*), count(DISTINCT signature), sum(failed::int), sum((NOT failed)::int), round(100.0*sum(failed::int)/count(*),2), min(block_time), max(block_time) FROM read_parquet('{A}/sigs_{n}.parquet')")
    show(f"full_{n} lignes/distinct/échouées", f"SELECT count(*), count(DISTINCT signature), sum(failed::int), min(block_time), max(block_time) FROM read_parquet('{A}/a02_tx.parquet') WHERE src='{n}'")
    show(f"  réussies listées absentes de full_{n}", f"""SELECT count(*), min(block_time), max(block_time) FROM read_parquet('{A}/sigs_{n}.parquet') s WHERE NOT failed AND NOT EXISTS (SELECT 1 FROM read_parquet('{A}/a02_tx.parquet') t WHERE t.src='{n}' AND t.signature=s.signature)""")
    show(f"  full_{n} absentes de la liste", f"""SELECT count(DISTINCT t.signature), min(block_time), max(block_time) FROM read_parquet('{A}/a02_tx.parquet') t WHERE t.src='{n}' AND NOT EXISTS (SELECT 1 FROM read_parquet('{A}/sigs_{n}.parquet') s WHERE t.signature=s.signature)""")
    show(f"  échouées listées présentes dans full_{n}", f"""SELECT count(*) FROM read_parquet('{A}/sigs_{n}.parquet') s WHERE failed AND EXISTS (SELECT 1 FROM read_parquet('{A}/a02_tx.parquet') t WHERE t.src='{n}' AND t.signature=s.signature)""")
show("full_venue", f"SELECT count(*), count(DISTINCT signature), sum(failed::int), min(block_time), max(block_time) FROM read_parquet('{A}/a02_tx.parquet') WHERE src='venue'")
show("tous sources, lignes, distinct", f"SELECT count(*), count(DISTINCT signature), sum(failed::int) FROM read_parquet('{A}/a02_tx.parquet')")
show("version", f"SELECT version, count(*) FROM read_parquet('{A}/a02_tx.parquet') GROUP BY 1")
show("clés != balances", f"SELECT sum((n_keys<>n_prebal)::int) FROM read_parquet('{A}/a02_tx.parquet')")
show("tx_index nul", f"SELECT sum((tx_index IS NULL)::int) FROM read_parquet('{A}/a02_tx.parquet')")
show("décimales != 6", f"SELECT sum(decimals_bad::int) FROM read_parquet('{A}/a02_tx.parquet')")
show("conservation DMAGA != 0", f"SELECT count(DISTINCT signature), sum(dmaga_sum)/1e6, min(block_time), max(block_time) FROM read_parquet('{A}/a02_tx.parquet') WHERE dmaga_sum<>0")
show("  détail", f"SELECT DISTINCT signature, dmaga_sum/1e6, block_time FROM read_parquet('{A}/a02_tx.parquet') WHERE dmaga_sum<>0 ORDER BY abs(dmaga_sum) DESC LIMIT 8")
# échecs par fenêtre
for name, a, b in (("avant_S_24h", S - 86400, S), ("heure_S", S, S + 3600), ("S+1h", S + 3600, S + 7200), ("S+24h", S, S + 86400), ("créa-S", 1720923331, S), ("après 01/01/2025", 1735689600, 1800000000)):
    show(f"échecs sigs_pool {name} n, échouées, %", f"SELECT count(*), sum(failed::int), round(100.0*sum(failed::int)/nullif(count(*),0),1) FROM read_parquet('{A}/sigs_pool.parquet') WHERE block_time>={a} AND block_time<{b}")
show("type d'erreur top", f"SELECT err, count(*) FROM read_parquet('{A}/sigs_pool.parquet') WHERE failed GROUP BY 1 ORDER BY 2 DESC LIMIT 10")
show("heures autour de S, tout et réussies", f"SELECT block_time//3600*3600 h, count(*), sum((NOT failed)::int), sum(failed::int) FROM read_parquet('{A}/sigs_pool.parquet') WHERE block_time>={S-8*3600} AND block_time<{S+3*3600} GROUP BY 1 ORDER BY 1")
print("hist activity contre sigs_pool (heures différentes) :")
con.execute(f"CREATE TEMP TABLE hs AS SELECT block_time//3600 h, count(*) n, sum((NOT failed)::int) ok FROM read_parquet('{A}/sigs_pool.parquet') GROUP BY 1")
act = None
for line in open(f"{B}/controls/activity.jsonl"):
    if '"CRSwXnfF21yHDXdYBVWwCwQ5Ni2A4QuK3qGYis5k7x7k"' in line:
        act = json.loads(line)
        break
hist = {int(k): int(v) for k, v in act["hist"]}
hs = {r[0]: (r[1], r[2]) for r in q("SELECT h,n,ok FROM hs")}
print(" pages", act["pages"], "tronqué", act["truncated"], "n hist", sum(hist.values()), "dernière heure hist", max(hist), max(hist) * 3600)
bad = [(h, hist[h], hs.get(h, (0, 0))[0]) for h in sorted(hist) if hist[h] != hs.get(h, (0, 0))[0]]
print(" heures en écart", len(bad), bad[:5], bad[-3:])
# pic sur réussies seules (recalcul propre)
import statistics
ok = {h: v[1] for h, v in hs.items()}
cr = 1720923331
lo = (cr + 96 * 3600 + 3599) // 3600
hi = (cr + 60 * 86400) // 3600
sok = None
for h in range(lo, hi):
    n = ok.get(h, 0)
    if n >= 500 and n >= 20 * max(statistics.median([ok.get(x, 0) for x in range(h - 72, h)]), 5):
        sok = h * 3600
        break
print(" S sur réussies seules", sok, "contre S", S, "réussies à S", ok.get(S // 3600), "à S+1h", ok.get(S // 3600 + 1))
# chaînes
for name, v, thr in (("DMAGA", VT, 10**6), ("WSOL", VS, 10**7)):
    con.execute(f"""CREATE OR REPLACE TEMP TABLE c AS SELECT DISTINCT signature, slot, tx_index, block_time, pre, post FROM read_parquet('{A}/a02_acct.parquet') WHERE account='{v}'""")
    con.execute("CREATE OR REPLACE TEMP TABLE o AS SELECT *, lag(post) OVER (ORDER BY slot, tx_index) pp, row_number() OVER (ORDER BY slot, tx_index) rn FROM c")
    show(f"chaîne {name} tx, signatures, ruptures, min t, max t", "SELECT count(*), count(DISTINCT signature), sum((pp IS NOT NULL AND pp<>pre)::int), min(block_time), max(block_time) FROM o")
    show(f"  ruptures détail", "SELECT signature, slot, tx_index, block_time, pre, pp, pre-pp FROM o WHERE pp IS NOT NULL AND pp<>pre ORDER BY slot LIMIT 25")
    show(f"  première ligne", "SELECT signature, block_time, pre, post FROM o ORDER BY rn LIMIT 1")
    show(f"  dernière ligne", "SELECT signature, block_time, pre, post FROM o ORDER BY rn DESC LIMIT 1")
# instructions contre soldes
show("vault jeton : instructions != soldes", f"SELECT count(DISTINCT signature), sum(abs(ix_vt-(vt_post-vt_pre)))/1e6 FROM read_parquet('{A}/a02_tx.parquet') WHERE vt_pre IS NOT NULL AND NOT failed AND ix_vt<>(vt_post-vt_pre)")
show("vault SOL : instructions != soldes", f"SELECT count(DISTINCT signature), sum(abs(ix_vs-(vs_post-vs_pre)))/1e9 FROM read_parquet('{A}/a02_tx.parquet') WHERE vs_pre IS NOT NULL AND NOT failed AND ix_vs<>(vs_post-vs_pre)")
show("  exemples", f"SELECT DISTINCT signature, block_time, ix_vt, vt_post-vt_pre, ix_vs, vs_post-vs_pre FROM read_parquet('{A}/a02_tx.parquet') WHERE vt_pre IS NOT NULL AND NOT failed AND (ix_vt<>(vt_post-vt_pre) OR ix_vs<>(vs_post-vs_pre)) LIMIT 6")
# autres réserves de l'autorité Raydium sur DMAGA : un second pool v4 absent de la collecte ?
show("comptes DMAGA tenus par l'autorité Raydium", f"SELECT account, count(DISTINCT signature), min(block_time), max(block_time), sum(abs(post-pre))/1e6 FROM read_parquet('{A}/a02_acct.parquet') WHERE owner='{AUTH}' GROUP BY 1 ORDER BY 2 DESC")
# réconciliation par (signature, owner) : parseur propre contre trades
con.execute(f"CREATE OR REPLACE TEMP TABLE ow AS SELECT signature, owner, any_value(dmaga) dmaga, any_value(is_signer) sg FROM read_parquet('{A}/a02_own.parquet') GROUP BY 1,2")
show("propre : couples, signatures", "SELECT count(*), count(DISTINCT signature) FROM ow")
con.execute(f"""CREATE OR REPLACE TEMP TABLE tr AS SELECT signature, owner, sum(token_delta) td, count(*) n, sum(CASE WHEN kind='swap' THEN 1 ELSE 0 END) nsw FROM read_parquet('{B}/trades.parquet') WHERE owner IS NOT NULL AND kind<>'mint_supply' GROUP BY 1,2""")
show("trades : couples", "SELECT count(*), count(DISTINCT signature) FROM tr")
show("signatures à flux DMAGA propres absentes de trades", f"SELECT count(*) FROM (SELECT DISTINCT signature FROM ow) a WHERE NOT EXISTS (SELECT 1 FROM read_parquet('{B}/trades.parquet') t WHERE t.signature=a.signature)")
show("signatures de trades absentes du propre", f"SELECT count(*), sum(c) FROM (SELECT signature, count(*) c FROM read_parquet('{B}/trades.parquet') GROUP BY 1) a WHERE NOT EXISTS (SELECT 1 FROM ow WHERE ow.signature=a.signature)")
show("couples dans trades, delta égal, double, autre", """SELECT sum((t.td=o.dmaga)::int), sum((t.td=2*o.dmaga)::int), sum((t.td<>o.dmaga AND t.td<>2*o.dmaga)::int), count(*) FROM tr t JOIN ow o USING (signature, owner)""")
show("  écarts autres, exemples", """SELECT t.signature, t.owner, t.td, o.dmaga, t.n FROM tr t JOIN ow o USING (signature, owner) WHERE t.td<>o.dmaga AND t.td<>2*o.dmaga ORDER BY abs(t.td-o.dmaga) DESC LIMIT 10""")
show("couples dans trades sans propre", "SELECT count(*), sum(abs(td))/1e6 FROM tr t WHERE NOT EXISTS (SELECT 1 FROM ow o WHERE o.signature=t.signature AND o.owner=t.owner)")
show("couples propres sans trades (propriétaires non signataires surtout)", "SELECT sg, count(*), sum(abs(dmaga))/1e6 FROM ow o WHERE NOT EXISTS (SELECT 1 FROM tr t WHERE o.signature=t.signature AND o.owner=t.owner) GROUP BY 1")
show("  top propriétaires sans ligne trades", "SELECT owner, count(*), sum(abs(dmaga))/1e6 s FROM ow o WHERE NOT EXISTS (SELECT 1 FROM tr t WHERE o.signature=t.signature AND o.owner=t.owner) GROUP BY 1 ORDER BY s DESC LIMIT 25")
# chaînes de tous les comptes de jetons : transaction invisible = rupture
con.execute(f"""CREATE OR REPLACE TEMP TABLE ca AS SELECT DISTINCT account, any_value(owner) OVER (PARTITION BY signature, account) owner, signature, slot, tx_index, block_time, pre, post FROM read_parquet('{A}/a02_acct.parquet') WHERE account NOT IN ('{VS}')""")
con.execute("CREATE OR REPLACE TEMP TABLE oa AS SELECT *, lag(post) OVER (PARTITION BY account ORDER BY slot, tx_index) pp FROM ca")
show("comptes, lignes, ruptures, comptes rompus, jetons manquants", "SELECT count(DISTINCT account), count(*), sum((pp IS NOT NULL AND pp<>pre)::int), count(DISTINCT account) FILTER (WHERE pp IS NOT NULL AND pp<>pre), sum(CASE WHEN pp IS NOT NULL AND pp<>pre THEN abs(pre-pp) ELSE 0 END)/1e6 FROM oa")
show("  comptes ouverts avec un solde initial non nul (premier pre>0)", "WITH f AS (SELECT account, arg_min(pre,(slot,tx_index)) p0, sum((pp IS NOT NULL AND pp<>pre)::int) r FROM oa GROUP BY 1) SELECT count(*), sum(p0)/1e6 FROM f WHERE p0>0")
show("  top ruptures par propriétaire", "SELECT owner, count(*), sum(abs(pre-pp))/1e6 s FROM oa WHERE pp IS NOT NULL AND pp<>pre GROUP BY 1 ORDER BY s DESC LIMIT 25")
