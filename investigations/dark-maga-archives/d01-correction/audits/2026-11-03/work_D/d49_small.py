#!/usr/bin/env python3
"""Auditeur D. Derniers contrôles : wallets touchés par les doublons selon la définition, GXZvX, part de 9W9b vers la famille, écart entre rapports. Sortie d49_small.txt."""
import gzip, json, sys, collections
import duckdb
D = "/Volumes/VERBATIM HD/Dark-MAGA-Investigation/audits_work/D"; BIG = "/Volumes/VERBATIM HD/Dark-MAGA-Investigation/data"; NET = "/Volumes/VERBATIM HD/Dark-MAGA-Investigation/audits_work/C/net/"
sys.stdout = open("audits/2026-11-03/work_D/d49_small.txt", "w")
con = duckdb.connect(":memory:", config={"memory_limit": "300MB", "threads": 1})
W = f"read_parquet('{D}/d40_wallets.parquet')"
print("doublons : réalisé change", con.execute(f"SELECT sum((abs(dedup_realized-tel_realized)>1e-6)::int),sum((abs(dedup_realized-tel_realized)>1e-6 OR abs(dedup_bought-tel_bought)>1e-6 OR abs(dedup_sold-tel_sold)>1e-6 OR dedup_tin<>tel_tin OR dedup_qty<>tel_qty)::int) FROM {W}").fetchone())
print("somme réalisé", con.execute(f"SELECT round(sum(tel_realized),1),round(sum(dedup_realized),1),round(sum(fix_realized),1),round(sum(tel_bought),1),round(sum(dedup_bought),1),round(sum(tel_sold),1),round(sum(dedup_sold),1) FROM {W}").fetchone())
print("GXZvX", con.execute(f"SELECT round(first_buy_qty/1e6,4),round(first_buy_sol,3),round(cost_usd,2) FROM read_parquet('{BIG}/wallets.parquet') WHERE owner='GXZvXsD6hxaLeFvQisWpdAwsayJxga7w9EeafhFZG2Ra'").fetchone())
print("H3QsBr", con.execute(f"SELECT round(cost_usd,2),round(proceeds_usd,0),round(bought_qty/1e6,3) FROM read_parquet('{BIG}/wallets.parquet') WHERE owner='H3QsBrrivimFJmSpTXuvig2n1Bh7JuYxrriRSEszT6cc'").fetchone())
W9 = "9W9b3zgHH9mCEHDhsdbnbEPHStm9vvXS4aia4DWHBxpL"
FAM = {"FpwQQhQQoEaVu3WU2qZMfF1hx48YyfwsLoRgXG83E99Q", "D89hHJT5Aqyx1trP6EnGY9jJUB3whgnq3aUvvCqedvzf", "9obNtb5GyUegcs3a1CbBkLuc5hEWynWfJC6gjz5uWQkE", "DPqsobysNf5iA9w7zrQM8HLzCKZEDMkZsWbiidsAt1xo", "4NyK1AdJBNbgaJ9EsKz3J4rfeHsuYdjkTPg3JaNdLeFw", "8JUEoHNMbWM4eegcMvx6ZQJt3V3fbo8JNjpWiCtJgxfF"}
HOT = {"H8sMJSCQxfKiFTCfDR3DUMLPwcRbM61LGFJ8N4dK3WjS", "2AQdpHJ2JpcEgPiATUXjQxA8QmafFegfQwSLWSprPicm", "GJRs4FwHtemZ5ZE9x3FNvJ8TMwitKTh21yxdRPqn7npE"}
o = collections.Counter(); seen = set()
with gzip.open(NET + W9 + ".jsonl.gz", "rt") as fh:
    for l in fh:
        t = json.loads(l); s = t["transaction"]["signatures"][0]
        if s in seen: continue
        seen.add(s)
        for i in t["transaction"]["message"]["instructions"]:
            p = i.get("parsed")
            if i.get("program") == "system" and isinstance(p, dict) and p.get("type") == "transfer" and p["info"]["source"] == W9:
                o[p["info"]["destination"]] += int(p["info"]["lamports"])
tot = sum(o.values())
print("sorties 9W9b : hot", round(100 * sum(v for k, v in o.items() if k in HOT) / tot, 3), "famille 6", round(100 * sum(v for k, v in o.items() if k in FAM) / tot, 3), "autres", [(k, v / 1e9) for k, v in o.items() if k not in HOT | FAM])
