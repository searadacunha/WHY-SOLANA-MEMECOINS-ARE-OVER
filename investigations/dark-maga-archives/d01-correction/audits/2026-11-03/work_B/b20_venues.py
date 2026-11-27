"""Phase 2 : DMAGA avant S, volumes par venue, depuis data/trades.parquet (table de l'enquête, pas recalculée ici depuis le brut).
Répond à : que voit le test (Raydium v4 seul) de ce qui s'achète avant S ? Sortie : b20_venues.txt."""
from pathlib import Path
import duckdb, json
HERE = Path(__file__).parent; ROOT = HERE.parents[2]
W = "/Volumes/VERBATIM HD/Dark-MAGA-Investigation/audits_work/B"
L = []
def P(*a):
    s = " ".join(str(x) for x in a); L.append(s); print(s)
con = duckdb.connect()
con.execute(f"SET memory_limit='800MB'; SET threads=2; SET TimeZone='UTC'; SET temp_directory='{W}/duck_tmp'")
T = f"'{ROOT}/data/trades.parquet'"
S = 478219 * 3600
P("colonnes", [x[0] for x in con.execute(f"DESCRIBE SELECT * FROM {T}").fetchall()])
for name, a, b in (("[S−24h,S)", S - 86400, S), ("[S−96h,S)", S - 96 * 3600, S), ("[S−3h,S)", S - 3 * 3600, S), ("[création,S)", 0, S), ("[S,S+1h)", S, S + 3600)):
    r = con.execute(f"""select source, venue, kind, count(*) n, count(distinct owner) w, round(sum(case when token_delta>0 and sol_lamports<0 then -sol_lamports else 0 end)/1e9,2) sol_achete,
       round(sum(case when token_delta>0 then token_delta else 0 end)/1e12,3) jetons_M_recus, round(sum(case when token_delta<0 and sol_lamports>0 then sol_lamports else 0 end)/1e9,2) sol_vendu
       from {T} where block_time>={a} and block_time<{b} group by 1,2,3 order by sol_achete desc limit 12""").fetchall()
    P(f"\n{name} (source, venue, kind, lignes, wallets, SOL acheté, M jetons reçus côté acheteur, SOL vendu) :")
    for x in r: P("  ", x)
(HERE / "b20_venues.txt").write_text("\n".join(L) + "\n")
