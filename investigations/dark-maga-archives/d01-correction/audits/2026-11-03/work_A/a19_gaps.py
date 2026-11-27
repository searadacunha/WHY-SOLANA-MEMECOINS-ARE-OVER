#!/usr/bin/env python3
"""Auditeur A. Écarts entre parseur propre et trades, ventes sans SOL reçu, rangs touchés par les doublons, décimales aberrantes des flux."""
import csv, gzip, json, os, re, collections, sys
import duckdb
A = "/Volumes/VERBATIM HD/Dark-MAGA-Investigation/audits_work/A"
B = "/Volumes/VERBATIM HD/Dark-MAGA-Investigation/data"
ROOT = "REDACTED_HOME/Projects/Dark-MAGA-Investigation"
con = duckdb.connect(":memory:", config={"memory_limit": "450MB", "threads": 2, "temp_directory": A + "/duck19", "preserve_insertion_order": False})
con.execute("SET TimeZone='UTC'")
def show(n, s, *a):
    print(n, con.execute(s, *a).fetchall(), flush=True)
for n in ("tx", "ow", "vside", "leg", "trd"):
    con.execute(f"CREATE VIEW {n} AS SELECT * FROM read_parquet('{A}/a15_{n}.parquet')")
T = f"read_parquet('{B}/trades.parquet')"
con.execute(f"COPY (SELECT l.signature, l.owner, l.dmaga, l.sol, l.t FROM leg l ANTI JOIN trd t ON l.signature=t.signature AND l.owner=t.owner) TO '{A}/a19_only_own.parquet' (FORMAT parquet)")
OO = f"read_parquet('{A}/a19_only_own.parquet')"
show("seulement propre : kind de la ligne trades du même (signature, owner)", f"""SELECT coalesce(k.kind,'(aucune)'), count(*), round(sum(abs(o.sol))/1e9,1), round(sum(abs(o.dmaga))/1e12,2) FROM {OO} o LEFT JOIN (SELECT DISTINCT signature, owner, kind FROM {T}) k ON o.signature=k.signature AND o.owner=k.owner GROUP BY 1 ORDER BY 3 DESC""")
show("  exemples lp", f"""SELECT o.signature, o.owner, o.dmaga, o.sol, k.kind, k.venue, k.sol_lamports, k.pool_sol_delta, k.pool_token_delta, x.ds, x.dt FROM {OO} o JOIN (SELECT signature, owner, kind, venue, sol_lamports, pool_sol_delta, pool_token_delta FROM {T}) k ON o.signature=k.signature AND o.owner=k.owner JOIN tx x ON x.signature=o.signature ORDER BY abs(o.sol) DESC LIMIT 6""")
show("  top owners", f"SELECT owner, count(*), round(sum(abs(sol))/1e9,1) s FROM {OO} GROUP BY 1 ORDER BY s DESC LIMIT 10")
# ventes : SOL de la ligne reçu ou non par le wallet signataire
con.execute(f"""COPY (SELECT l.signature, l.owner, l.sol rec, o.native+o.wsol+CASE WHEN o.pay THEN x.fee ELSE 0 END cash, o.stable, a.other_opp FROM leg l JOIN ow o USING (signature, owner) JOIN (SELECT signature, fee FROM tx) x USING (signature)
     JOIN (SELECT signature, owner, any_value(other_opp) other_opp FROM read_parquet('{A}/a02_own.parquet') GROUP BY 1,2) a USING (signature, owner) WHERE l.dmaga<0 AND o.sg AND o.native IS NOT NULL) TO '{A}/a19_sell.parquet' (FORMAT parquet)""")
S = f"read_parquet('{A}/a19_sell.parquet')"
show("ventes signataire : n, SOL ligne, SOL reçu, sans stable", f"SELECT count(*), round(sum(rec)/1e9), round(sum(cash)/1e9) FROM {S}")
show("  cash<50 % de la ligne : stable, autre jeton opposé, rien", f"""SELECT CASE WHEN stable>0 THEN 'stable reçu' WHEN other_opp<>'' THEN 'autre jeton reçu' ELSE 'rien de visible' END c, count(*), round(sum(rec)/1e9,1), round(sum(cash)/1e9,1) FROM {S} WHERE cash<0.5*rec AND rec>0 GROUP BY 1 ORDER BY 3 DESC""")
show("  exemples 'rien de visible'", f"SELECT signature, owner, rec/1e9, cash/1e9 FROM {S} WHERE cash<0.5*rec AND rec>0 AND stable<=0 AND other_opp='' ORDER BY rec DESC LIMIT 6")
show("  top owners 'rien de visible'", f"SELECT owner, count(*), round(sum(rec)/1e9,1) s FROM {S} WHERE cash<0.5*rec AND rec>0 AND stable<=0 AND other_opp='' GROUP BY 1 ORDER BY s DESC LIMIT 10")
# rangs touchés par les doublons
diff = {}
for r in csv.DictReader(open(ROOT + "/audits/2026-11-03/work_A/out/a14_pnl_diff.csv")):
    diff[r["owner"]] = r
txt = open(ROOT + "/reports/TOP_TRADERS.md").read()
sec = txt.split("## 100 plus gros réalisés")[1].split("\n## ")[0]
top = re.findall(r"\| (\d+) \| `(\w+)` \| ([\d ,-]+) \|", sec)
print("TOP 100 réalisés lus", len(top))
ch = [(int(i), o, x, diff[o]["realise_tel"], diff[o]["realise_dedup"]) for i, o, x in top if o in diff]
print("lignes du top 100 touchées par les doublons", len(ch), ch[:14])
g = json.load(open(ROOT + "/data/prevent_groups.json"))
mem = g[0]["members"]
print("membres du groupe de 33 touchés", [(o, diff[o]["realise_tel"], diff[o]["realise_dedup"], diff[o]["vendu_tel"], diff[o]["vendu_dedup"]) for o in mem if o in diff], "réalisé du groupe rapporté", g[0]["realized_sol"])
# décimales aberrantes des flux
F = "/Volumes/VERBATIM HD/Dark-MAGA-Investigation/raw/flows"
c = collections.Counter()
mx = {}
yr = collections.Counter()
rows_bad = 0
for d in os.listdir(F):
    if d.startswith("._"):
        continue
    for name in ("first_in", "in_before", "sol_out_after"):
        p = f"{F}/{d}/{name}.json.gz"
        if not os.path.exists(p):
            continue
        with gzip.open(p) as fh:
            j = json.load(fh)
        for x in j["rows"]:
            c[(name, x.get("decimals"))] += 1
            if x.get("decimals") != 9:
                rows_bad += 1
                yr[(name, x["blockTime"] // 31536000 + 1970)] += 1
                mx[name] = max(mx.get(name, 0), x["blockTime"])
print("décimales par requête", dict(c))
print("lignes décimales != 9 par année", dict(yr), "dernière date", mx)
show("funding_edges sol>1e6, par an", f"SELECT block_time//31536000+1970, count(*), round(sum(sol)) FROM read_parquet('{B}/funding_edges.parquet') WHERE sol>1000000 GROUP BY 1 ORDER BY 1")
show("funding_edges sol>1000 hors échange, 2024 et après", f"SELECT src, wallet, sol, block_time, query FROM read_parquet('{B}/funding_edges.parquet') WHERE sol>5000 AND block_time>1704067200 ORDER BY sol DESC LIMIT 6")
show("exit_flows SOL>1e5", f"SELECT count(*), max(amount), min(block_time) FROM read_parquet('{B}/exit_flows.parquet') WHERE asset='SOL' AND amount>100000")
show("link_edges sol_direct montant > 1e5", f"SELECT count(*), max(amount), min(block_time) FROM read_parquet('{B}/link_edges.parquet') WHERE type LIKE 'sol%' AND amount>100000")
# C50 refait en SOL, décimales corrigées par filtre de bon sens (avant 2024 exclu du SOL)
show("C50, niveau 0, SOL reçu 12 mois avant le 14/07/2024 par classe", f"""SELECT CASE WHEN is_pool THEN 'pool, trading antérieur' WHEN src_label IS NULL THEN 'sans étiquette' WHEN src_label LIKE 'Jupiter%' THEN 'compte Jupiter' WHEN src_label LIKE 'Pont%' OR src_label LIKE 'Service%' THEN 'service' ELSE 'échange étiqueté' END c,
      count(*), count(DISTINCT wallet), round(sum(sol)), round(100.0*sum(sol)/sum(sum(sol)) OVER (),1) FROM read_parquet('{B}/funding_edges.parquet') WHERE level=0 AND query='in_before' AND block_time>=1689292800 AND sol<1000000 GROUP BY 1 ORDER BY 4 DESC""")
show("C50, premier financeur non pool, classes larges (≥0,01 SOL, décimales saines)", f"""WITH f AS (SELECT wallet, arg_min(src, block_time) s, arg_min(src_label, block_time) l FROM read_parquet('{B}/funding_edges.parquet') WHERE level=0 AND NOT is_pool AND sol>=0.01 AND sol<1000000 GROUP BY 1)
   SELECT CASE WHEN l IS NULL THEN 'sans étiquette' WHEN l LIKE 'Jupiter%' THEN 'compte Jupiter' WHEN l LIKE 'Pont%' OR l LIKE 'Service%' THEN 'service' ELSE 'échange étiqueté' END c, count(*) FROM f GROUP BY 1 ORDER BY 2 DESC""")
