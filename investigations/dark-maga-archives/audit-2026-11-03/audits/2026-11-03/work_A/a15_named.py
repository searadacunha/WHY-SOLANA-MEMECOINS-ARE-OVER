#!/usr/bin/env python3
"""Auditeur A. Assertions chiffrées sur le brut (a02) : fenêtres, création, 60 s, sommet, wallets nommés, cohortes, en parseur propre, sans trades.parquet sauf comparaison explicite."""
import csv, io, json, sys, zipfile
from pathlib import Path
import duckdb
A = "/Volumes/VERBATIM HD/Dark-MAGA-Investigation/audits_work/A"
B = "/Volumes/VERBATIM HD/Dark-MAGA-Investigation/data"
RAW = Path("/Volumes/VERBATIM HD/Dark-MAGA-Investigation/raw/solusd")
OUT = "REDACTED_HOME/Projects/Dark-MAGA-Investigation/audits/2026-11-03/work_A/out"
sys.path.insert(0, "REDACTED_HOME/Projects/Dark-MAGA-Investigation")
from dmaga.venues import load as lv
AUTH = "5Q544fKrFoe6tsEbD7S8EmxGTJYAKtTVhAW5Q5pge4j1"
CURVE = "87g44hEXP7R8ZxoAJtz941tsVftpEXC1LqAFTf2ZHtkH"
EXCL = {AUTH, CURVE, "39azUYFWPz3VHgKCf3VChUwbpURdCHRxjWVowf5jUJjg", "PNLCQcVCD26aC7ZWgRyr5ptfaR7bBrWdTFgRWwu2tvF"}
VEN = set(lv())
con = duckdb.connect(":memory:", config={"memory_limit": "450MB", "threads": 2, "temp_directory": A + "/duck15", "preserve_insertion_order": False})
con.execute("SET TimeZone='UTC'")
q = lambda s, *a: con.execute(s, *a).fetchall()
def show(n, s, *a):
    print(n, q(s, *a), flush=True)
con.execute("CREATE TEMP TABLE ven(a VARCHAR)")
con.executemany("INSERT INTO ven VALUES (?)", [[a] for a in VEN])
con.execute("CREATE TEMP TABLE ex(a VARCHAR)")
con.executemany("INSERT INTO ex VALUES (?)", [[a] for a in EXCL | VEN])
# tables de travail sur disque : les tables temporaires en mémoire ont fait tuer le script par le garde (1 021 Mo)
import os
def mat(name, sql):
    path = f"{A}/a15_{name}.parquet"
    if not os.path.exists(path):
        con.execute(f"COPY ({sql}) TO '{path}.tmp' (FORMAT parquet, COMPRESSION zstd)")
        os.replace(path + ".tmp", path)
    con.execute(f"CREATE OR REPLACE VIEW {name} AS SELECT * FROM read_parquet('{path}')")
mat("tx", f"""SELECT signature, any_value(slot) slot, any_value(tx_index) tx_index, any_value(block_time) t, any_value(failed) failed,
      any_value(vt_post-vt_pre) dt, any_value(vs_post-vs_pre) ds, any_value(payer) payer, any_value(fee) fee, any_value(progs) progs, any_value(signers) signers FROM read_parquet('{A}/a02_tx.parquet') WHERE n_dmaga>0 OR vs_pre IS NOT NULL GROUP BY 1""")
mat("ow", f"""SELECT signature, owner, any_value(slot) slot, any_value(tx_index) tx_index, any_value(block_time) t, any_value(dmaga) dmaga, any_value(wsol) wsol,
      any_value(stable) stable, any_value(native) native, any_value(is_signer) sg, any_value(is_payer) pay FROM read_parquet('{A}/a02_own.parquet') GROUP BY 1,2""")
# SOL et jeton côté venues, par signature : vault Raydium (exact) + propriétaires venues + courbe
mat("vside", f"""SELECT s.signature, coalesce(t.ds,0) + coalesce(sum(CASE WHEN s.owner IN (SELECT a FROM ven) THEN s.wsol END),0) + coalesce(max(CASE WHEN s.owner='{CURVE}' THEN s.native END),0) vsol,
          coalesce(t.dt,0) + coalesce(sum(CASE WHEN s.owner IN (SELECT a FROM ven) OR s.owner='{CURVE}' THEN s.dmaga END),0) vtok
   FROM ow s JOIN (SELECT signature, ds, dt FROM tx) t USING (signature) GROUP BY s.signature, t.ds, t.dt""")
# lignes d'achat et de vente au parseur propre (règle : le trader bouge en sens opposé des venues, parts >= 5 %, SOL réparti à la quantité)
mat("leg", """WITH c AS (SELECT o.signature, o.owner, o.dmaga, o.t, o.slot, o.tx_index, o.sg, v.vsol, v.vtok FROM ow o JOIN vside v USING (signature)
              WHERE o.owner NOT IN (SELECT a FROM ex) AND v.vtok<>0 AND v.vsol<>0 AND (v.vtok>0)<>(v.vsol>0) AND (o.dmaga>0)=(v.vtok<0)),
        f AS (SELECT *, sum(dmaga) OVER (PARTITION BY signature) fu FROM c),
        k AS (SELECT * FROM f WHERE abs(dmaga)>=0.05*abs(fu)),
        g AS (SELECT *, sum(dmaga) OVER (PARTITION BY signature) tot FROM k)
   SELECT signature, owner, t, slot, tx_index, sg, dmaga, CAST(-vsol*dmaga/tot AS DOUBLE) sol FROM g""")
show("lignes propres", "SELECT count(*), count(DISTINCT signature), sum(CASE WHEN dmaga>0 THEN -sol ELSE 0 END)/1e9, sum(CASE WHEN dmaga<0 THEN sol ELSE 0 END)/1e9 FROM leg")
mat("trd", f"SELECT DISTINCT signature, owner, token_delta, sol_lamports, usdc_raw, venue FROM read_parquet('{B}/trades.parquet') WHERE kind='swap'")
show("swaps trades dédoublonnés", "SELECT count(*), count(DISTINCT signature), sum(CASE WHEN token_delta>0 THEN -sol_lamports ELSE 0 END)/1e9, sum(CASE WHEN token_delta<0 THEN sol_lamports ELSE 0 END)/1e9 FROM trd")
show("comparaison lignes : commun, quantité égale, |SOL écart|<=2 lamports", """SELECT count(*), sum((t.token_delta=l.dmaga)::int), sum((abs(t.sol_lamports-l.sol)<=2)::int), sum(abs(t.sol_lamports-l.sol))/1e9 FROM trd t JOIN leg l ON t.signature=l.signature AND t.owner=l.owner""")
show("  écarts SOL par présence d'USDC", """SELECT (t.usdc_raw<>0) u, count(*), sum(abs(t.sol_lamports-l.sol))/1e9 FROM trd t JOIN leg l ON t.signature=l.signature AND t.owner=l.owner WHERE abs(t.sol_lamports-l.sol)>2 GROUP BY 1""")
show("  exemples d'écart hors USDC", """SELECT t.signature, t.owner, t.token_delta, t.sol_lamports, l.sol, t.venue FROM trd t JOIN leg l ON t.signature=l.signature AND t.owner=l.owner WHERE abs(t.sol_lamports-l.sol)>2 AND t.usdc_raw=0 ORDER BY abs(t.sol_lamports-l.sol) DESC LIMIT 8""")
show("seulement dans trades", """SELECT count(*), sum(abs(sol_lamports))/1e9, sum((usdc_raw<>0)::int), sum(abs(usdc_raw))/1e6 FROM trd t WHERE NOT EXISTS (SELECT 1 FROM leg l WHERE l.signature=t.signature AND l.owner=t.owner)""")
show("  exemples", """SELECT t.signature, t.owner, t.token_delta, t.sol_lamports, t.usdc_raw, t.venue FROM trd t WHERE NOT EXISTS (SELECT 1 FROM leg l WHERE l.signature=t.signature AND l.owner=t.owner) ORDER BY abs(sol_lamports) DESC LIMIT 6""")
show("seulement dans le propre", """SELECT count(*), sum(abs(sol))/1e9 FROM leg l WHERE NOT EXISTS (SELECT 1 FROM trd t WHERE l.signature=t.signature AND l.owner=t.owner)""")
show("  exemples", """SELECT l.signature, l.owner, l.dmaga, l.sol FROM leg l WHERE NOT EXISTS (SELECT 1 FROM trd t WHERE l.signature=t.signature AND l.owner=t.owner) ORDER BY abs(sol) DESC LIMIT 6""")
show("SOL de la ligne contre cash réel du wallet signataire, achats (hors USDC, un seul bénéficiaire)", """WITH x AS (SELECT l.signature, l.owner, l.dmaga, -l.sol cout, -(o.native+o.wsol+CASE WHEN o.pay THEN t.fee ELSE 0 END) cash FROM leg l JOIN ow o USING (signature, owner) JOIN tx t USING (signature) WHERE l.dmaga>0 AND o.sg AND o.native IS NOT NULL AND o.stable=0)
   SELECT count(*), sum(cout)/1e9, sum(cash)/1e9, median(cash*1.0/nullif(cout,0)), quantile_cont(cash*1.0/nullif(cout,0),0.9), quantile_cont(cash*1.0/nullif(cout,0),0.99), sum((cash>1.5*cout)::int), sum((cash<0.5*cout)::int) FROM x WHERE cout>0""")
show("idem, ventes", """WITH x AS (SELECT l.signature, l.owner, l.dmaga, l.sol rec, (o.native+o.wsol+CASE WHEN o.pay THEN t.fee ELSE 0 END) cash FROM leg l JOIN ow o USING (signature, owner) JOIN tx t USING (signature) WHERE l.dmaga<0 AND o.sg AND o.native IS NOT NULL AND o.stable=0)
   SELECT count(*), sum(rec)/1e9, sum(cash)/1e9, median(cash*1.0/nullif(rec,0)), quantile_cont(cash*1.0/nullif(rec,0),0.1), quantile_cont(cash*1.0/nullif(rec,0),0.01), sum((cash<0.5*rec)::int) FROM x WHERE rec>0""")
T0, MIG, S = 1720922725, 1720923331, 1721588400
LOW, ENV, HIGH, BIDEN, WINIG = 1721588607, 1721589800, 1721590213, 1721583960, 1721577749
for n, a, b in (("C05a borne basse à envoi", LOW, ENV), ("C05b envoi à borne haute incluse", ENV, HIGH + 1), ("C05c heure suivante", HIGH, HIGH + 3600), ("C06 Biden à borne basse", BIDEN, LOW), ("C07 3h avant envoi", ENV - 10800, ENV), ("C45 3h avant Winig", WINIG - 10800, WINIG)):
    show(n, f"SELECT round(sum(CASE WHEN dmaga>0 THEN -sol ELSE 0 END)/1e9,3), round(sum(CASE WHEN dmaga<0 THEN sol ELSE 0 END)/1e9,3), sum((dmaga>0)::int), sum((dmaga<0)::int), count(DISTINCT owner) FROM leg WHERE t>={a} AND t<{b}")
    show("   vault Raydium seul", f"SELECT round(sum(CASE WHEN ds>0 AND dt<0 THEN ds ELSE 0 END)/1e9,3), round(sum(CASE WHEN ds<0 AND dt>0 THEN -ds ELSE 0 END)/1e9,3), sum((ds>0 AND dt<0)::int), sum((ds<0 AND dt>0)::int) FROM tx WHERE t>={a} AND t<{b} AND NOT failed")
    show("   trades.parquet", f"SELECT round(sum(CASE WHEN token_delta>0 THEN -sol_lamports ELSE 0 END)/1e9,3), round(sum(CASE WHEN token_delta<0 THEN sol_lamports ELSE 0 END)/1e9,3), sum((token_delta>0)::int), sum((token_delta<0)::int) FROM read_parquet('{B}/trades.parquet') WHERE kind='swap' AND block_time>={a} AND block_time<{b}")
# création
show("première tx du mint", f"SELECT signature, slot, block_time, signers, payer FROM read_parquet('{A}/a02_tx.parquet') WHERE src IN ('curve','mint') AND NOT failed ORDER BY slot, tx_index LIMIT 3")
show("signature de création", "SELECT signature, slot, t, failed, signers, progs FROM tx WHERE signature='fePxr7ER3EDxtkXysbcbbCcaztCHMwKBESs2XQzQee8xkBH2u53ULZMP1gMSK9bgGJKj14NcGwpR64YJR3nPiw6'")
show("rangs DMAGA à la création", "SELECT owner, dmaga/1e6, wsol, native FROM ow WHERE signature='fePxr7ER3EDxtkXysbcbbCcaztCHMwKBESs2XQzQee8xkBH2u53ULZMP1gMSK9bgGJKj14NcGwpR64YJR3nPiw6'")
show("slot de création et suivant, acheteurs propres", "SELECT owner, slot, dmaga/1e12, -sol/1e9 FROM leg WHERE dmaga>0 AND slot<=277417696 ORDER BY slot")
show("C29 60 s", f"SELECT count(DISTINCT owner), sum(dmaga)/1e12, sum(-sol)/1e9, min(t), max(t) FROM leg WHERE dmaga>0 AND t<{T0 + 60}")
show("C29 trades", f"SELECT count(DISTINCT owner), sum(token_delta)/1e12, sum(-sol_lamports)/1e9 FROM read_parquet('{B}/trades.parquet') WHERE kind='swap' AND token_delta>0 AND block_time<{T0 + 60}")
show("C29 tx échouées dans les 60 s (courbe)", f"SELECT count(*) FROM tx WHERE failed AND t<{T0 + 60}")
show("migration", f"SELECT signature, slot, t, signers FROM tx WHERE signature='2zmB9nbUp6FJrymbnHJ8f4sxzqtkGTiaCCb3VHABS6UC9nkjvWb4mnbftzBtUoTxpNvwEuWC19hmfqhchEiCuTMc'")
# sommet
show("sommet du prix, chaîne propre", f"""WITH v AS (SELECT slot, tx_index, block_time t, any_value(vt_post) a, any_value(vs_post) b FROM read_parquet('{A}/a02_tx.parquet') WHERE vt_post IS NOT NULL AND vs_post IS NOT NULL AND vt_post<>vt_pre AND vs_post<>vs_pre AND NOT failed GROUP BY 1,2,3)
       SELECT t, slot, tx_index, a/1e6, b/1e9, (b/1e9)/(a/1e6)*1e9 cap FROM v WHERE a>0 ORDER BY cap DESC LIMIT 5""")
# cohortes
show("cohortes par premier achat", f"""WITH f AS (SELECT owner, min(t) t0 FROM leg WHERE dmaga>0 GROUP BY 1) SELECT sum((t0<{WINIG})::int), sum((t0>={WINIG} AND t0<{LOW})::int), sum((t0>={LOW} AND t0<={HIGH})::int), sum((t0>{HIGH})::int) FROM f""")
show("acheteurs en [10:02:29,16:02:29), en [16:02:29,19:03:27), dans les deux", f"""WITH a AS (SELECT DISTINCT owner FROM leg WHERE dmaga>0 AND t>={WINIG-6*3600} AND t<{WINIG}), b AS (SELECT DISTINCT owner FROM leg WHERE dmaga>0 AND t>={WINIG} AND t<{LOW})
   SELECT (SELECT count(*) FROM a), (SELECT count(*) FROM b), (SELECT count(*) FROM a JOIN b USING(owner))""")
show("acheteurs avant Winig, entre, dans les deux (toute l'histoire)", f"""WITH a AS (SELECT DISTINCT owner FROM leg WHERE dmaga>0 AND t<{WINIG}), b AS (SELECT DISTINCT owner FROM leg WHERE dmaga>0 AND t>={WINIG} AND t<{LOW})
   SELECT (SELECT count(*) FROM a), (SELECT count(*) FROM b), (SELECT count(*) FROM a JOIN b USING(owner))""")
# wallets nommés
NAMED = {"H3QsBr": "H3QsBrrivimFJmSpTXuvig2n1Bh7JuYxrriRSEszT6cc", "GXZvX": "GXZvXsD6hxaLeFvQisWpdAwsayJxga7w9EeafhFZG2Ra", "9PrmF8": "9PrmF8sfoD2YShtWUghrGEYgxwabpnzog8gT1V6LEtdq", "5QhJJc": "5QhJJcFZu2ashyKyWSTGHcsyo6ZBCbpVuJqeutvQHScd", "createur": "8YLEuUtZ4eFMJbf46oNb1CeG6dYFWGyxnQSh9hrgzBzR"}
for k, o in NAMED.items():
    rows = q(f"""SELECT o.signature, o.t, o.slot, o.tx_index, o.dmaga, o.wsol, o.stable, o.native, o.sg, o.pay, t.fee, t.dt, t.ds, t.progs, l.sol FROM ow o JOIN tx t USING (signature) LEFT JOIN leg l ON l.signature=o.signature AND l.owner=o.owner
                 WHERE o.owner=? ORDER BY o.slot, o.tx_index""", [o])
    with open(f"{OUT}/named_{k}.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["signature", "t", "slot", "tx_index", "dmaga", "wsol", "stable", "native", "signataire", "payeur", "fee", "dt", "ds", "progs", "sol_venue"])
        w.writerows(rows)
    bq = bs = sq = ss = cash_in = cash_out = 0
    qty = 0
    cost = 0.0
    real = 0.0
    real_cash = 0.0
    cqty = 0
    ccost = 0.0
    for r in rows:
        d, wsol, native, pay, fee, sol = r[4], r[5], r[7], r[9], r[10], r[14]
        cash = (native or 0) + (wsol or 0) + (fee if pay else 0)  # lamports reçus par le wallet, frais de réseau rendus
        if sol is None:  # transfert ou sans contrepartie
            if d > 0:
                qty += d; cqty += d
            else:
                k_ = min(-d, max(qty, 0))
                if qty > 0:
                    cost -= cost / qty * k_
                qty -= k_
                k2 = min(-d, max(cqty, 0))
                if cqty > 0:
                    ccost -= ccost / cqty * k2
                cqty -= k2
            continue
        if d > 0:
            bq += d; bs += -sol; qty += d; cost += -sol; cash_in += -cash; cqty += d; ccost += -cash
        else:
            sq += -d; ss += sol; cash_out += cash
            k_ = min(-d, max(qty, 0))
            basis = cost / qty * k_ if qty > 0 else 0
            real += sol - basis; cost -= basis; qty -= k_
            k2 = min(-d, max(cqty, 0))
            cb = ccost / cqty * k2 if cqty > 0 else 0
            real_cash += cash - cb; ccost -= cb; cqty -= k2
    print(k, o, "lignes", len(rows), "acheté M", round(bq / 1e12, 3), "SOL", round(bs / 1e9, 3), "vendu M", round(sq / 1e12, 3), "SOL", round(ss / 1e9, 3), "réalisé venue", round(real / 1e9, 2), "cash acheté", round(cash_in / 1e9, 3), "cash vendu", round(cash_out / 1e9, 3), "réalisé cash", round(real_cash / 1e9, 2), "reste M", round(qty / 1e12, 4), flush=True)
    show("   wallets.parquet", f"SELECT realized_sol, bought_sol, sold_sol, bought_qty/1e6, sold_qty/1e6, cost_usd, proceeds_usd, n_buys, n_sells, residual_qty/1e6, transfer_in_qty/1e6, transfer_out_qty/1e6, sold_no_basis_qty/1e6, completeness, first_buy_time FROM read_parquet('{B}/wallets.parquet') WHERE owner=?", [o])
    show("   comptes de jetons, ruptures de chaîne", f"""WITH a AS (SELECT DISTINCT account, signature, slot, tx_index, pre, post FROM read_parquet('{A}/a02_acct.parquet') WHERE owner=?), o AS (SELECT *, lag(post) OVER (PARTITION BY account ORDER BY slot, tx_index) pp FROM a)
       SELECT count(DISTINCT account), count(*), sum((pp IS NOT NULL AND pp<>pre)::int), sum(CASE WHEN pp IS NOT NULL AND pp<>pre THEN abs(pre-pp) ELSE 0 END)/1e6 FROM o""", [o])
# capitalisation à 13:38:12 et coût USD H3QsBr (validation externe)
px = {}
for z in ("SOLUSDT-1m-2024-07.zip",):
    with zipfile.ZipFile(RAW / z) as f, f.open(f.namelist()[0]) as fh:
        for row in csv.reader(io.TextIOWrapper(fh)):
            if row and row[0].isdigit():
                px[int(row[0]) // 60000] = float(row[4])
T = 1721569092
a = q(f"SELECT slot, tx_index, block_time, vt_post, vs_post FROM read_parquet('{A}/a02_tx.parquet') WHERE block_time<{T} AND vt_post<>vt_pre AND vs_post<>vs_pre AND NOT failed ORDER BY slot DESC, tx_index DESC LIMIT 1")[0]
print("C25 capitalisation à 13:38:12", a, "prix SOL/USD", px[T // 60], "cap USD", round((a[4] / 1e9) / (a[3] / 1e6) * 1e9 * px[T // 60]))
r = q(f"SELECT t, dmaga, sol FROM leg WHERE owner=? AND dmaga>0 ORDER BY t", [NAMED["H3QsBr"]])
print("C25 H3QsBr achats", r, "coût USD", round(sum(-x[2] / 1e9 * px[x[0] // 60] for x in r), 2), "M", sum(x[1] for x in r) / 1e12)
r = q(f"SELECT t, dmaga, sol FROM leg WHERE owner=? AND dmaga>0 ORDER BY t", [NAMED["GXZvX"]])
print("C25 GXZvX achats", r, "SOL", sum(-x[2] for x in r) / 1e9, "M", sum(x[1] for x in r) / 1e12)
