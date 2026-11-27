"""Explique les écarts entre data_v2, l'ancien dérivé et les valeurs de D. Lecture seule. Sortie : f06_ecarts.txt."""
import json, sys
from collections import defaultdict
from pathlib import Path
import duckdb
OLD = "/Volumes/VERBATIM HD/Dark-MAGA-Investigation/data"; NEW = OLD + "_v2"; TMP = "/Volumes/VERBATIM HD/Dark-MAGA-Investigation/tmp/duck"
con = duckdb.connect(":memory:", config={"memory_limit": "600MB", "threads": 2, "temp_directory": TMP, "preserve_insertion_order": False})
sys.stdout = open("audits/2026-11-03/work_F/f06_ecarts.txt", "w")
def q(n, s):
    r = con.execute(s).fetchall(); print(n, r, flush=True); return r
TF, TZ, CRE, LOW = 1721590213, 1721590213 + 86400, 1720923331, 1721588607
to, tn = f"read_parquet('{OLD}/trades.parquet')", f"read_parquet('{NEW}/trades.parquet')"
print("--- a. marché 24 h : lignes dédoublonnées de l'ancien contre data_v2")
con.execute(f"CREATE TEMP TABLE a AS SELECT DISTINCT signature, owner, kind, venue, token_delta, sol_lamports FROM {to} WHERE block_time>={TF} AND block_time<{TZ}")
con.execute(f"CREATE TEMP TABLE b AS SELECT signature, owner, kind, venue, token_delta, sol_lamports FROM {tn} WHERE block_time>={TF} AND block_time<{TZ}")
q("ventes ancien dédoublonné, nouveau", "SELECT (SELECT sum(sol_lamports)/1e9 FROM a WHERE kind='swap' AND token_delta<0),(SELECT sum(sol_lamports)/1e9 FROM b WHERE kind='swap' AND token_delta<0)")
q("achats ancien dédoublonné, nouveau", "SELECT (SELECT sum(-sol_lamports)/1e9 FROM a WHERE kind='swap' AND token_delta>0),(SELECT sum(-sol_lamports)/1e9 FROM b WHERE kind='swap' AND token_delta>0)")
q("différences sur ventes par (kind ancien, kind nouveau) : n, SOL ancien, SOL nouveau", """SELECT coalesce(x.kind,'absent'),coalesce(y.kind,'absent'),count(*),round(sum(coalesce(CASE WHEN x.kind='swap' THEN x.sol_lamports END,0))/1e9,3),round(sum(coalesce(CASE WHEN y.kind='swap' THEN y.sol_lamports END,0))/1e9,3)
   FROM (SELECT * FROM a WHERE token_delta<0) x FULL JOIN (SELECT * FROM b WHERE token_delta<0) y USING (signature,owner,token_delta)
   WHERE coalesce(x.kind,'')<>coalesce(y.kind,'') OR coalesce(x.sol_lamports,0)<>coalesce(y.sol_lamports,0) GROUP BY 1,2 ORDER BY 5 DESC""")
q("plus gros écarts de vente", """SELECT y.signature,y.owner,x.kind,y.kind,round(coalesce(x.sol_lamports,0)/1e9,3),round(y.sol_lamports/1e9,3) FROM (SELECT * FROM a WHERE token_delta<0) x FULL JOIN (SELECT * FROM b WHERE token_delta<0) y USING (signature,owner,token_delta)
   WHERE y.kind='swap' AND coalesce(x.sol_lamports,0)<>y.sol_lamports ORDER BY abs(coalesce(x.sol_lamports,0)-y.sol_lamports) DESC LIMIT 5""")
print("--- b. noeuds")
q("ancien cex", f"SELECT address,label,kind FROM read_parquet('{OLD}/nodes.parquet') WHERE kind='cex' ORDER BY 1")
q("nouveau cex et service", f"SELECT address,label,kind FROM read_parquet('{NEW}/nodes.parquet') WHERE kind IN ('cex','service') ORDER BY 3,1")
q("présents avant, absents après", f"SELECT address,kind,label,n_tx,qty_moved FROM read_parquet('{OLD}/nodes.parquet') WHERE address NOT IN (SELECT address FROM read_parquet('{NEW}/nodes.parquet')) ORDER BY 1")
q("présents après, absents avant", f"SELECT address,kind,label,n_tx,qty_moved FROM read_parquet('{NEW}/nodes.parquet') WHERE address NOT IN (SELECT address FROM read_parquet('{OLD}/nodes.parquet')) ORDER BY 1")
q("arêtes token_edges ancien, nouveau", f"SELECT (SELECT count(*) FROM read_parquet('{OLD}/token_edges.parquet')),(SELECT count(*) FROM read_parquet('{NEW}/token_edges.parquet'))")
print("--- c. étiquettes de financement, ancien contre nouveau")
fo, fn = f"read_parquet('{OLD}/funding_edges.parquet')", f"read_parquet('{NEW}/funding_edges.parquet')"
q("lignes ancien, nouveau", f"SELECT (SELECT count(*) FROM {fo}),(SELECT count(*) FROM {fn})")
q("sources dont l'étiquette change (sources, ancienne, nouvelle)", f"""SELECT count(DISTINCT o.src),o.l,n.l FROM (SELECT DISTINCT src, src_label l FROM {fo}) o JOIN (SELECT DISTINCT src, src_label l FROM {fn}) n USING (src) WHERE o.l IS DISTINCT FROM n.l GROUP BY 2,3""")
q("exemples", f"""SELECT o.src,o.l,n.l FROM (SELECT DISTINCT src, src_label l FROM {fo}) o JOIN (SELECT DISTINCT src, src_label l FROM {fn}) n USING (src) WHERE o.l IS DISTINCT FROM n.l LIMIT 8""")
print("--- d. sorties à 3 sauts, par wallet")
ol = json.load(open("data/exit_summary.json")); ne = json.load(open(NEW + "/exit_summary.json"))
def serv(x, m): return sum(v for k, v in x["frontieres"].items() if m in k)
print("wallets sortis du résumé", [(k[:8], ol[k]["groupe"], round(serv(ol[k], "service")), round(sum(v for a, v in ol[k]["frontieres"].items() if "OKX" in a))) for k in ol if k not in ne])
print("wallets entrés", [(k[:8], ne[k]["groupe"], round(serv(ne[k], "service"))) for k in ne if k not in ol])
print("somme service ancien, nouveau, hot présumé", round(sum(serv(x, "service") for x in ol.values())), round(sum(serv(x, "service") for x in ne.values())), round(sum(serv(x, "hot") for x in ne.values())))
com = [k for k in ol if k in ne]
print("sur les wallets communs : service ancien, service nouveau, hot nouveau", len(com), round(sum(serv(ol[k], "service") for k in com)), round(sum(serv(ne[k], "service") for k in com)), round(sum(serv(ne[k], "hot") for k in com)))
d = sorted(((serv(ol[k], "service") - serv(ne[k], "service") - serv(ne[k], "hot"), k[:8]) for k in com), reverse=True)[:6]
print("plus gros écarts sur les communs (ancien service - nouveau service - hot)", [(round(a), b) for a, b in d])
print("tronqués ancien, nouveau", sum(x["tronque"] for x in ol.values()), sum(x["tronque"] for x in ne.values()))
print("--- e. transferts cachés avant la borne basse")
AC = f"read_parquet('{NEW}/accounts.parquet')"; ED = f"read_parquet('{NEW}/token_edges.parquet')"
con.execute(f"CREATE TEMP TABLE seen AS SELECT DISTINCT signature s FROM {AC} WHERE block_time<{LOW}")
con.execute(f"CREATE TEMP TABLE curvebuy AS SELECT DISTINCT owner FROM {tn} WHERE kind='swap' AND token_delta>0 AND block_time<{CRE}")
con.execute(f"CREATE TEMP TABLE early AS SELECT DISTINCT owner FROM read_parquet('{OLD}/controls/swaps/CRSwXnfF21yHDXdYBVWwCwQ5Ni2A4QuK3qGYis5k7x7k.parquet') WHERE qty>0 AND t<{CRE+86400}")
q("cachés : src, dst, M, acheteur courbe hors M6", f"SELECT src,dst,round(qty/1e6,3),src IN (SELECT owner FROM curvebuy) AND src NOT IN (SELECT owner FROM early) FROM {ED} WHERE how='gtba' AND block_time<{LOW} AND dst<>'(multiple)' AND signature NOT IN (SELECT s FROM seen) ORDER BY 3 DESC")
print("--- f. offre hors pools à la fin")
from dmaga.venues import load as lv
ve = list(lv()) + ["5Q544fKrFoe6tsEbD7S8EmxGTJYAKtTVhAW5Q5pge4j1", "87g44hEXP7R8ZxoAJtz941tsVftpEXC1LqAFTf2ZHtkH", "39azUYFWPz3VHgKCf3VChUwbpURdCHRxjWVowf5jUJjg"]
q("derniers soldes : total, pools", f"SELECT round(sum(p)/1e12,2),round(sum(CASE WHEN o IN ({','.join(repr(x) for x in ve)}) THEN p ELSE 0 END)/1e12,2) FROM (SELECT account,arg_max(owner,(slot,tx_index)) o,arg_max(post,(slot,tx_index)) p FROM {AC} GROUP BY 1)")
print("--- g. financement d'au moins 100 000 SOL, pour vérifier K07")
q("funding", f"SELECT wallet,src,sol,query,strftime(to_timestamp(block_time),'%Y-%m-%d') FROM {fn} WHERE sol>=100000 ORDER BY sol DESC")
q("sortie", f"SELECT wallet,dst,amount,asset,strftime(to_timestamp(block_time),'%Y-%m-%d') FROM read_parquet('{NEW}/exit_flows.parquet') WHERE amount>=100000 AND asset='SOL' ORDER BY amount DESC")
q("ancien funding >= 1e6", f"SELECT count(*) FROM {fo} WHERE sol>=1e6")
q("ancien exit SOL >= 1e6", f"SELECT count(*) FROM read_parquet('{OLD}/exit_flows.parquet') WHERE amount>=1e6 AND asset='SOL'")
