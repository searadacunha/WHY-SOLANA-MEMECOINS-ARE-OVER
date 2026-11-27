#!/usr/bin/env python3
"""Sauts suivants du traçage. Lit raw/flows, écrit la prochaine liste à collecter.

usage: ana_32_hops.py <niveau> → BIG/hops_level<niveau>.csv (owner,t_buy,t_sell,raison), à passer à col_30_flows.py

Amont : financeurs non service, ≥ 1 SOL, dans les 7 jours avant le premier achat d'un wallet du niveau précédent.
Aval  : destinations non service recevant ≥ 20 SOL ou ≥ 3 000 USDC d'un wallet du niveau précédent.
Arrêt à toute frontière : échange étiqueté, pool, routeur, adresse vue par ≥ 15 wallets tracés. Plafond par niveau,
les adresses écartées par le plafond sont comptées dans BIG/hops_level<n>.json, jamais perdues en silence.
"""
import csv
import gzip
import json
import sys
from collections import defaultdict

from dmaga.config import BIG, RAW
from dmaga.db import connect
from dmaga.labels import label
from dmaga.venues import load as load_venues

FLOWS = RAW / "flows"
CAP = 150
level = int(sys.argv[1])
venues = set(load_venues())
con = connect()
con.execute(f"CREATE VIEW n AS SELECT * FROM read_parquet('{BIG}/nodes.parquet')")
service = {a for (a,) in con.execute("SELECT address FROM n WHERE kind <> 'wallet'").fetchall()} | venues
first_buy = dict(con.execute(f"SELECT owner, first_buy_time FROM read_parquet('{BIG}/wallets.parquet')").fetchall())
levels = json.loads((BIG / "trace_levels.json").read_text()) if (BIG / "trace_levels.json").exists() else {}

traced = {d.name for d in FLOWS.iterdir() if d.is_dir() and not d.name.startswith("._")}
for w in traced:
    levels.setdefault(w, 0)
seen_by = defaultdict(set)
for d in traced:
    for q in ("in_before", "sol_out_after", "usdc_out_after", "usdt_out_after"):
        p = FLOWS / d / f"{q}.json.gz"
        if p.exists():
            for x in json.load(gzip.open(p))["rows"]:
                other = x["toUserAccount"] if q != "in_before" else x["fromUserAccount"]
                if other:
                    seen_by[other].add(d)
popular = {a for a, s in seen_by.items() if len(s) >= 15}


def bad(a):
    return a is None or a in service or a in popular or label(a) is not None or a in traced


up = defaultdict(lambda: [0.0, None])  # adresse -> [montant, heure la plus tardive du virement]
down = defaultdict(lambda: [0.0, None])
stops = defaultdict(float)
for w in traced:
    if levels[w] != level - 1:
        continue
    p = FLOWS / w / "in_before.json.gz"
    if p.exists():
        ref = first_buy.get(w)
        for x in json.load(gzip.open(p))["rows"]:
            a, amt, t = x.get("fromUserAccount"), float(x["uiAmount"]), x["blockTime"]
            if amt >= 1 and (ref is None or ref - t <= 7 * 86400):
                if bad(a):
                    if a and a not in traced:
                        stops[f"amont:{label(a) or 'service ou populaire'}"] += amt
                else:
                    up[a][0] += amt
                    up[a][1] = max(up[a][1] or 0, t)
    for q, floor in (("sol_out_after", 20.0), ("usdc_out_after", 3000.0), ("usdt_out_after", 3000.0)):
        p = FLOWS / w / f"{q}.json.gz"
        if p.exists():
            for x in json.load(gzip.open(p))["rows"]:
                a, amt, t = x.get("toUserAccount"), float(x["uiAmount"]), x["blockTime"]
                if amt >= floor:
                    if bad(a):
                        if a and a not in traced:
                            stops[f"aval:{label(a) or 'service ou populaire'}"] += amt
                    else:
                        down[a][0] += amt / (1.0 if q == "sol_out_after" else 170.0)
                        down[a][1] = min(down[a][1] or t, t)

rows = sorted(({"a": a, "t": v[1], "amt": v[0], "dir": "amont"} for a, v in up.items()), key=lambda r: -r["amt"])
rows += sorted(({"a": a, "t": v[1], "amt": v[0], "dir": "aval"} for a, v in down.items()), key=lambda r: -r["amt"])
rows.sort(key=lambda r: -r["amt"])
keep, dropped = rows[:CAP], rows[CAP:]
with (BIG / f"hops_level{level}.csv").open("w", newline="") as f:
    w = csv.writer(f)
    for r in keep:
        # amont : on veut ce qui précède le virement ; aval : ce qui suit la réception. Les deux bornes = l'heure du virement.
        w.writerow([r["a"], r["t"], r["t"], f"saut {level} {r['dir']}, {r['amt']:.1f} SOL éq."])
        levels[r["a"]] = level
(BIG / "trace_levels.json").write_text(json.dumps(levels))
(BIG / f"hops_level{level}.json").write_text(json.dumps({"retenus": len(keep), "ecartes_par_plafond": len(dropped),
                                                         "montant_ecarte": sum(r["amt"] for r in dropped),
                                                         "arrets_frontiere": dict(stops)}, indent=1, ensure_ascii=False))
print(f"niveau {level}: retenus={len(keep)} écartés={len(dropped)} arrêts={len(stops)}")
for k, v in sorted(stops.items(), key=lambda kv: -kv[1])[:10]:
    print("  ", k, round(v, 1))
