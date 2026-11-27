#!/usr/bin/env python3
"""Auditeur D. A-03 : part des sources de financement, avec et sans doublons first_in / in_before, et sensibilité au plafond de montant. Sortie d45_funding.txt."""
import sys, os
import duckdb
D = "/Volumes/VERBATIM HD/Dark-MAGA-Investigation/audits_work/D"; BIG = "/Volumes/VERBATIM HD/Dark-MAGA-Investigation/data"
con = duckdb.connect(":memory:", config={"memory_limit": "600MB", "threads": 2, "temp_directory": D + "/duck", "preserve_insertion_order": False})
sys.stdout = open("audits/2026-11-03/work_D/d45_funding.txt", "w")
FE = f"read_parquet('{BIG}/funding_edges.parquet')"
T0 = 1720922725; Y0 = T0 - 365 * 86400
def q(n, s):
    r = con.execute(s).fetchall(); print(n, r, flush=True); return r
q("lignes, signatures distinctes, par query", f"SELECT query,count(*),count(DISTINCT signature),round(sum(CASE WHEN sol<1e6 THEN sol END)) FROM {FE} GROUP BY 1")
q("niveaux", f"SELECT level,count(*),count(DISTINCT wallet) FROM {FE} GROUP BY 1 ORDER BY 1")
K = "CASE WHEN is_pool THEN 'pool' WHEN src_label IS NULL OR src_label='' THEN 'sans_etiquette' WHEN regexp_matches(lower(src_label),'jupiter') THEN 'jupiter' WHEN regexp_matches(lower(src_label),'dex|raydium|orca|meteora') THEN 'dex' WHEN regexp_matches(lower(src_label),'binance|coinbase|okx|bybit|kucoin|mexc|kraken|gate|bitget|huobi|htx|crypto.com|bitfinex|cex|exchange') THEN 'echange' ELSE 'autre' END"
for name, base in (("A : toutes lignes, sans dédoublonner", f"SELECT * FROM {FE} WHERE level=0 AND block_time>={Y0} AND block_time<{T0} AND sol<1e6"),
                   ("D : une ligne par (wallet, signature, src)", f"SELECT DISTINCT ON (wallet,signature,src) * FROM {FE} WHERE level=0 AND block_time>={Y0} AND block_time<{T0} AND sol<1e6"),
                   ("D : idem, sans montants >= 1000 SOL hors échange", f"SELECT DISTINCT ON (wallet,signature,src) * FROM {FE} WHERE level=0 AND block_time>={Y0} AND block_time<{T0} AND sol<1000")):
    q(name, f"WITH c AS ({base}), k AS (SELECT *,{K} kl FROM c) SELECT kl,count(*),count(DISTINCT wallet),round(sum(sol)),round(100*sum(sol)/(SELECT sum(sol) FROM k),1) FROM k GROUP BY 1 ORDER BY 4 DESC")
q("doublons entre query : (wallet,signature,src) à 2 lignes", f"SELECT count(*),round(sum(sol)) FROM (SELECT wallet,signature,src,any_value(sol) sol,count(*) c FROM {FE} WHERE level=0 AND block_time>={Y0} AND block_time<{T0} AND sol<1e6 GROUP BY 1,2,3 HAVING count(*)>1)")
q("transactions à plusieurs lignes même query", f"SELECT query,count(*) FROM (SELECT query,wallet,signature,src,count(*) c FROM {FE} WHERE level=0 GROUP BY 1,2,3,4 HAVING count(*)>1) GROUP BY 1")
q("plus gros sans étiquette dédoublonné", f"WITH c AS (SELECT DISTINCT ON (wallet,signature,src) * FROM {FE} WHERE level=0 AND block_time>={Y0} AND block_time<{T0} AND sol<1e6 AND NOT is_pool AND (src_label IS NULL OR src_label='')) SELECT wallet,src,round(sum(sol)),count(*) FROM c GROUP BY 1,2 ORDER BY 3 DESC LIMIT 6")
# premier financeur par wallet, non pool
q("premier financeur non pool, >=0,01 SOL, sur 12 mois", f"WITH c AS (SELECT wallet,arg_min(src,block_time) s,arg_min({K},block_time) kl FROM {FE} WHERE level=0 AND block_time<{T0} AND sol<1e6 AND sol>=0.01 AND NOT is_pool GROUP BY 1) SELECT kl,count(*) FROM c GROUP BY 1 ORDER BY 2 DESC")
print("--- réplique de la requête de A et variantes de date", flush=True)
A_K = "CASE WHEN is_pool THEN 'pool' WHEN src_label IS NULL THEN 'sans_etiquette' WHEN src_label LIKE 'Jupiter%' THEN 'jupiter' WHEN src_label LIKE 'Pont%' OR src_label LIKE 'Service%' THEN 'service' ELSE 'echange' END"
q("A exact : in_before, >= 14/07/2023, sans borne haute", f"SELECT {A_K} k,count(*),count(DISTINCT wallet),round(sum(sol)),round(100.0*sum(sol)/sum(sum(sol)) OVER (),1) FROM {FE} WHERE level=0 AND query='in_before' AND block_time>=1689292800 AND sol<1000000 GROUP BY 1 ORDER BY 4 DESC")
q("borne haute réelle de ces lignes : min, max, part après le mint", f"SELECT strftime(to_timestamp(min(block_time)),'%Y-%m-%d'),strftime(to_timestamp(max(block_time)),'%Y-%m-%d'),round(100.0*sum(CASE WHEN block_time>={T0} THEN sol ELSE 0 END)/sum(sol),1) FROM {FE} WHERE level=0 AND query='in_before' AND block_time>=1689292800 AND sol<1000000")
q("in_before, 14/07/2023 au mint", f"SELECT {A_K} k,count(*),count(DISTINCT wallet),round(sum(sol)),round(100.0*sum(sol)/sum(sum(sol)) OVER (),1) FROM {FE} WHERE level=0 AND query='in_before' AND block_time>=1689292800 AND block_time<{T0} AND sol<1000000 GROUP BY 1 ORDER BY 4 DESC")
q("in_before, avant la borne haute de Musk", f"SELECT {A_K} k,count(*),count(DISTINCT wallet),round(sum(sol)),round(100.0*sum(sol)/sum(sum(sol)) OVER (),1) FROM {FE} WHERE level=0 AND query='in_before' AND block_time>=1689292800 AND block_time<1721590213 AND sol<1000000 GROUP BY 1 ORDER BY 4 DESC")
q("premier financeur non pool, requête exacte de A", f"WITH f AS (SELECT wallet,arg_min(src,block_time) s,arg_min(src_label,block_time) l FROM {FE} WHERE level=0 AND NOT is_pool AND sol>=0.01 AND sol<1000000 GROUP BY 1) SELECT CASE WHEN l IS NULL THEN 'sans étiquette' WHEN l LIKE 'Jupiter%' THEN 'compte Jupiter' WHEN l LIKE 'Pont%' OR l LIKE 'Service%' THEN 'service' ELSE 'échange étiqueté' END c,count(*) FROM f GROUP BY 1 ORDER BY 2 DESC")
q("  idem, premier reçu avant le mint seulement", f"WITH f AS (SELECT wallet,arg_min(src,block_time) s,arg_min(src_label,block_time) l FROM {FE} WHERE level=0 AND NOT is_pool AND sol>=0.01 AND sol<1000000 AND block_time<{T0} GROUP BY 1) SELECT CASE WHEN l IS NULL THEN 'sans étiquette' WHEN l LIKE 'Jupiter%' THEN 'compte Jupiter' WHEN l LIKE 'Pont%' OR l LIKE 'Service%' THEN 'service' ELSE 'échange étiqueté' END c,count(*) FROM f GROUP BY 1 ORDER BY 2 DESC")
