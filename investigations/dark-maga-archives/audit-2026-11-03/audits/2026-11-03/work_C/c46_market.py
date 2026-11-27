#!/usr/bin/env python3
"""Detentions a T_LOW depuis les post-soldes bruts (ta.parquet), offre totale, reserves, 938 M, autres detenteurs >=1 M et leurs ventes et transferts en 24 h, depuis trades.parquet et mes tables.
Ecrit holdings_Tlow.csv (top 500) et market_check.txt."""
import duckdb, json, csv, sys
from dmaga.venues import load as lv
W="/Volumes/VERBATIM HD/Dark-MAGA-Investigation/audits_work/C"
B="/Volumes/VERBATIM HD/Dark-MAGA-Investigation/data"
ROOT='REDACTED_HOME/Projects/Dark-MAGA-Investigation/audits/2026-11-03/work_C/'
REPO='REDACTED_HOME/Projects/Dark-MAGA-Investigation/'
TL,TH=1721588607,1721590213
M=json.load(open(REPO+'data/prevent_groups.json'))[0]['members']
con=duckdb.connect(); con.execute(f"SET memory_limit='800MB'; SET threads=2; SET TimeZone='UTC'; SET temp_directory='{W}/tmp'; SET preserve_insertion_order=false;")
con.execute(f"""CREATE TEMP TABLE h AS SELECT token_account, coalesce(nullif(arg_max(owner_post,x),''),arg_max(owner_pre,x)) owner, arg_max(post,x) bal FROM (
   SELECT a.token_account,a.owner_post,a.owner_pre,a.post,t.slot*100000+t.txidx x FROM '{W}/ta.parquet' a JOIN (SELECT tid,slot,txidx,bt FROM '{W}/tx.parquet' WHERE bt<{TL}) t USING(tid)) GROUP BY 1""")
print('comptes',con.execute("SELECT count(*), sum(bal)/1e12 FROM h").fetchone())
ven=lv()
con.execute("CREATE TEMP TABLE svc(a VARCHAR, k VARCHAR)")
con.executemany("INSERT INTO svc VALUES (?,?)",[(a,'venue') for a in ven])
con.execute(f"INSERT INTO svc SELECT address, kind FROM '{B}/nodes.parquet' WHERE kind<>'wallet'")
con.execute("INSERT INTO svc VALUES ('5Q544fKrFoe6tsEbD7S8EmxGTJYAKtTVhAW5Q5pge4j1','raydium'),('87g44hEXP7R8ZxoAJtz941tsVftpEXC1LqAFTf2ZHtkH','curve'),('39azUYFWPz3VHgKCf3VChUwbpURdCHRxjWVowf5jUJjg','migration')")
print('par proprietaires services',con.execute("SELECT s.k, count(DISTINCT h.owner), sum(bal)/1e12 FROM h JOIN (SELECT DISTINCT a,k FROM svc) s ON s.a=h.owner GROUP BY 1").fetchall())
print('top proprietaires',con.execute("SELECT owner,sum(bal)/1e12 v FROM h GROUP BY 1 ORDER BY v DESC LIMIT 12").fetchall())
nonp=con.execute("SELECT sum(bal)/1e12 FROM h WHERE owner NOT IN (SELECT a FROM svc WHERE k IN ('raydium','curve','venue','migration'))").fetchone()[0]
print('non pools (brut, hors raydium, courbe, venues, migration)',nonp)
print('non pools hors tous services',con.execute("SELECT sum(bal)/1e12 FROM h WHERE owner NOT IN (SELECT a FROM svc)").fetchone()[0])
con.execute("CREATE TEMP TABLE m(a VARCHAR)"); con.executemany("INSERT INTO m VALUES (?)",[(x,) for x in M])
print('groupe brut (ta)',con.execute("SELECT count(DISTINCT owner),sum(bal)/1e12 FROM h WHERE owner IN (SELECT a FROM m)").fetchone())
print('report trades pos',con.execute(f"SELECT sum(greatest(p,0))/1e6, sum(p)/1e6 FROM (SELECT owner, sum(token_delta)/1e6 p FROM '{B}/trades.parquet' WHERE block_time<{TL} AND kind IN ('swap','transfer','fee_share','swap_other','lp_add','lp_remove') AND owner IN (SELECT a FROM m) GROUP BY 1)").fetchone())
# vente marche : somme trades sur fenetre par venue, et double compte eventuel
print('ventes marche trades',con.execute(f"SELECT venue,count(*),count(DISTINCT signature),sum(sol_lamports)/1e9,sum(usdc_raw)/1e6 FROM '{B}/trades.parquet' WHERE kind='swap' AND token_delta<0 AND block_time>={TH} AND block_time<{TH+86400} GROUP BY 1 ORDER BY 4 DESC").fetchall())
print('tx multi-lignes',con.execute(f"SELECT sum(c>1),sum(CASE WHEN c>1 THEN s ELSE 0 END)/1e9 FROM (SELECT signature,count(*) c,sum(sol_lamports) s FROM '{B}/trades.parquet' WHERE kind='swap' AND token_delta<0 AND block_time>={TH} AND block_time<{TH+86400} GROUP BY 1)").fetchone())
print('sol vault raydium trades',con.execute(f"SELECT sum(pool_sol_delta)/1e9 FROM (SELECT DISTINCT signature,pool_sol_delta FROM '{B}/trades.parquet' WHERE kind='swap' AND venue='raydium_v4' AND token_delta<0 AND block_time>={TH} AND block_time<{TH+86400})").fetchone())
print('achats meme fenetre',con.execute(f"SELECT sum(-sol_lamports)/1e9 FROM '{B}/trades.parquet' WHERE kind='swap' AND token_delta>0 AND block_time>={TH} AND block_time<{TH+86400}").fetchone())
# ventes des >=1 M a T_LOW, swaps et transferts sortants 24 h
con.execute(f"""CREATE TEMP TABLE o AS SELECT owner a, sum(bal)/1e12 held FROM h WHERE owner NOT IN (SELECT a FROM svc) GROUP BY 1 HAVING sum(bal)>=1000000000000""")
print('detenteurs >=1 M hors services',con.execute("SELECT count(*),sum(held), sum(CASE WHEN a IN (SELECT a FROM m) THEN held END), sum(a IN (SELECT a FROM m)::int) FROM o").fetchone())
res=con.execute(f"""WITH t AS (SELECT owner, kind, sum(CASE WHEN token_delta<0 THEN -token_delta ELSE 0 END)/1e12 outq, sum(CASE WHEN token_delta>0 THEN token_delta ELSE 0 END)/1e12 inq FROM '{B}/trades.parquet'
     WHERE block_time>={TH} AND block_time<{TH+86400} AND owner IN (SELECT a FROM o) GROUP BY 1,2)
   SELECT (o.a IN (SELECT a FROM m)) grp, t.kind, sum(outq), sum(inq), count(DISTINCT t.owner) FROM t JOIN o ON o.a=t.owner GROUP BY 1,2 ORDER BY 1,2""").fetchall()
print('24h par groupe/kind (sorties, entrees, wallets)',res)
print('held par groupe',con.execute("SELECT (a IN (SELECT a FROM m)), count(*), sum(held) FROM o GROUP BY 1").fetchall())
# ecart par wallet : autres detenteurs, part vendue + transferee, top 10
top=con.execute(f"""SELECT o.a,o.held,
   coalesce((SELECT sum(-token_delta)/1e12 FROM '{B}/trades.parquet' t WHERE t.owner=o.a AND kind='swap' AND token_delta<0 AND block_time>={TH} AND block_time<{TH+86400}),0) s,
   coalesce((SELECT sum(-token_delta)/1e12 FROM '{B}/trades.parquet' t WHERE t.owner=o.a AND kind='transfer' AND token_delta<0 AND block_time>={TH} AND block_time<{TH+86400}),0) x
   FROM o WHERE o.a NOT IN (SELECT a FROM m) ORDER BY o.held DESC LIMIT 15""").fetchall()
for r in top: print(r[0][:10],round(r[1],2),round(r[2],2),round(r[3],2))
