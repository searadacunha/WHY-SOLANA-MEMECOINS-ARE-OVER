"""Phase 2 : DMAGA, ce que le test écarte ou ne voit pas. Différence entre trades.parquet (enquête) et swaps du test sur [S−24 h, S) ;
acheteurs de la courbe classés « nouveaux » par M3 ; poids de la courbe et des transferts. Sortie : b21_exclus.txt."""
from pathlib import Path
import duckdb
HERE = Path(__file__).parent; ROOT = HERE.parents[2]
W = "/Volumes/VERBATIM HD/Dark-MAGA-Investigation/audits_work/B"
EXT = "/Volumes/VERBATIM HD/Dark-MAGA-Investigation"
L = []
def P(*a):
    s = " ".join(str(x) for x in a); L.append(s); print(s)
con = duckdb.connect()
con.execute(f"SET memory_limit='800MB'; SET threads=2; SET TimeZone='UTC'; SET temp_directory='{W}/duck_tmp'")
T = f"'{ROOT}/data/trades.parquet'"
SW = f"'{EXT}/data/controls/swaps/CRSwXnfF21yHDXdYBVWwCwQ5Ni2A4QuK3qGYis5k7x7k.parquet'"
S = 478219 * 3600; a24 = S - 86400; C = 1720923331
con.execute(f"""CREATE TEMP TABLE tr AS SELECT signature, owner, block_time t, token_delta q, sol_lamports s, source, venue, kind, n_owners, signers FROM {T} WHERE block_time < {S}""")
con.execute(f"CREATE TEMP TABLE sw AS SELECT signature, owner, t, qty q, sol s FROM {SW} WHERE t < {S}")
for name, lo in (("[S−24h,S)", a24), ("[S−96h,S)", S - 96 * 3600), ("[création,S)", 0)):
    r = con.execute(f"""
      with a as (select signature, owner, sum(-s)/1e9 sol from tr where source='pool' and venue='raydium' and kind='swap' and q>0 and s<0 and t>={lo} group by 1,2),
           b as (select signature, owner, sum(-s)/1e9 sol from sw where q>0 and s<0 and t>={lo} group by 1,2)
      select (select sum(sol) from a), (select sum(sol) from b), sum(case when b.owner is null then a.sol else 0 end), count(*) filter (where b.owner is null), count(distinct a.owner) filter (where b.owner is null),
             sum(case when b.owner is not null then a.sol-b.sol else 0 end)
      from a left join b using(signature, owner)""").fetchone()
    P(f"{name}: SOL acheté enquête {r[0]:.2f}, test {r[1]:.2f} ; lignes de l'enquête absentes du test : {r[3]} lignes, {r[4]} wallets, {r[2]:.2f} SOL ; écart sur lignes communes {r[5]:.2f}")
r = con.execute(f"""
  with a as (select signature, owner, sum(-s)/1e9 sol, any_value(signers) signers from tr where source='pool' and venue='raydium' and kind='swap' and q>0 and s<0 and t>={a24} group by 1,2),
       b as (select distinct signature, owner from sw)
  select a.owner, round(sum(a.sol),2) sol, count(*) n, any_value(a.signers) from a left join b using(signature, owner) where b.owner is null group by 1 order by 2 desc limit 8""").fetchall()
P("principaux lignes hors test sur 24 h :")
for x in r: P("  ", x[0], x[1], x[2], str(x[3])[:60], "signataire" if x[0] in str(x[3]) else "non signataire")
# transactions du test absentes de l'enquête (lignes ajoutées par le test)
r = con.execute(f"""with a as (select distinct signature, owner from tr where source='pool' and kind='swap'), b as (select signature, owner, -s/1e9 sol from sw where q>0 and s<0 and t>={a24})
   select count(*), round(sum(sol),2) from b left join a using(signature, owner) where a.owner is null""").fetchone()
P("lignes du test absentes de l'enquête sur 24 h :", r)
# courbe, transferts, M3
r = con.execute(f"""select round(sum(case when q>0 then q else 0 end)/1e12,2), count(distinct owner) from tr where source='curve' and kind='swap' and q>0""").fetchone()
P("courbe : jetons M reçus par achat", r[0], "acheteurs", r[1])
r = con.execute(f"""
  with w as (select owner, min(t) f from sw group by 1), buy as (select owner, -s/1e9 sol from sw where q>0 and s<0 and t>={a24}),
       nw as (select b.owner, sum(sol) sol from buy b join w using(owner) where f>={a24} group by 1),
       cur as (select distinct owner from tr where source='curve' and kind='swap' and q>0),
       oth as (select distinct owner from tr where kind='transfer' and q>0 and t<{a24})
  select round((select sum(sol) from buy),2), round(sum(sol),2), count(*), round(sum(case when owner in (select owner from cur) then sol else 0 end),2), count(*) filter (where owner in (select owner from cur)),
         round(sum(case when owner in (select owner from oth) then sol else 0 end),2), count(*) filter (where owner in (select owner from oth)) from nw""").fetchone()
P(f"M3 DMAGA : SOL 24 h {r[0]}, SOL de wallets « nouveaux » {r[1]} ({r[2]} wallets) ; dont déjà acheteurs sur la courbe {r[3]} SOL ({r[4]} wallets) ; dont déjà destinataires d'un transfert de jetons avant la fenêtre {r[5]} SOL ({r[6]} wallets)")
r = con.execute(f"select count(distinct owner), round(sum(q)/1e12,2) from tr where kind='transfer' and q>0 and t>={a24}").fetchone()
P("transferts de jetons reçus sur 24 h avant S : wallets", r[0], "M jetons", r[1])
# M6 : acheteurs de la courbe dans la mesure ?
r = con.execute(f"""with e as (select distinct owner from sw where q>0 and s<0 and t<{C}+86400), cur as (select owner, sum(q) qq from tr where source='curve' and kind='swap' and q>0 group by 1),
   ne as (select cur.owner, qq from cur where cur.owner not in (select owner from e))
   select (select count(*) from e), (select count(*) from cur), (select count(*) from ne), round((select sum(qq) from cur)/1e12,2), round((select sum(qq) from ne)/1e12,2)""").fetchone()
P(f"M6 : {r[0]} précoces Raydium ; {r[1]} acheteurs de la courbe, dont {r[2]} hors M6 ; jetons courbe {r[3]} M, dont hors M6 {r[4]} M")
(HERE / "b21_exclus.txt").write_text("\n".join(L) + "\n")
