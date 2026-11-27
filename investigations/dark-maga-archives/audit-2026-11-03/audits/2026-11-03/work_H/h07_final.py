import json, os, time
from pathlib import Path
import duckdb
from dmaga.venues import load
os.environ["TZ"] = "UTC"; time.tzset()
B = Path("/Volumes/VERBATIM HD/Dark-MAGA-Investigation/data_v2")
con = duckdb.connect(":memory:", config={"memory_limit": "500MB", "threads": 2, "temp_directory": "/Volumes/VERBATIM HD/Dark-MAGA-Investigation/audits_work/H"})
con.execute("SET TimeZone='UTC'")
WP, ND, FE, EX, ED = (f"read_parquet('{B}/{n}.parquet')" for n in ("wallets", "nodes", "funding_edges", "exit_flows", "token_edges"))
ve = list(load()) + ["5Q544fKrFoe6tsEbD7S8EmxGTJYAKtTVhAW5Q5pge4j1", "87g44hEXP7R8ZxoAJtz941tsVftpEXC1LqAFTf2ZHtkH", "39azUYFWPz3VHgKCf3VChUwbpURdCHRxjWVowf5jUJjg"]
print("venues", len(ve))
print("en-tête", con.execute(f"SELECT count(*), sum(bought_sol), sum(sold_sol), sum(realized_sol) FROM {WP} WHERE owner NOT IN ({','.join(repr(x) for x in ve)}) AND owner NOT IN (SELECT address FROM {ND} WHERE kind IN ('router','venue','cex','service'))").fetchall())
for n, a in (("H3", "H3QsBrrivimFJmSpTXuvig2n1Bh7JuYxrriRSEszT6cc"), ("GX", "GXZvXsD6hxaLeFvQisWpdAwsayJxga7w9EeafhFZG2Ra"), ("P9", "9PrmF8sfoD2YShtWUghrGEYgxwabpnzog8gT1V6LEtdq"), ("Q", "5QhJJcFZu2ashyKyWSTGHcsyo6ZBCbpVuJqeutvQHScd")):
    print(n, "entrées étiquetées", con.execute(f"SELECT src_label, round(sum(sol),2), count(*) FROM {FE} WHERE wallet='{a}' AND src_label IS NOT NULL AND NOT is_pool GROUP BY 1 ORDER BY 2 DESC LIMIT 4").fetchall(), "sorties étiquetées", con.execute(f"SELECT dst_label, asset, round(sum(amount),2), count(*) FROM {EX} WHERE wallet='{a}' AND terminal GROUP BY 1,2 ORDER BY 3 DESC LIMIT 4").fetchall())
g = json.load(open(B / "prevent_groups.json"))[0]
print("groupe edges n", g["edges"], g["n"], list(g.keys())[:12])
print("gel M6 p", json.load(open("etude_final/tables/tests.json"))["variants"]["primary"]["mesures"]["M6"]["p"])
