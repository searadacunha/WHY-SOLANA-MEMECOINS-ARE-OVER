#!/usr/bin/env python3
"""Où est allé l'argent : sorties des gagnants au coût connu et du groupe de lancement, par saut, jusqu'à une frontière.

Une frontière arrête la trace : échange étiqueté, pool, compte Jupiter, adresse vue par beaucoup de wallets tracés. Aucune continuité
n'est créée à travers elle. Lit exit_flows.parquet par requêtes filtrées, mémoire plafonnée. Sortie : data/exit_summary.json.
"""
import json
from collections import defaultdict

from dmaga.config import BIG, DATA
from dmaga.db import connect
from dmaga.labels import label
from dmaga.venues import load as load_venues

USD = 170.0  # shortcut: stablecoin ramené en SOL au cours moyen de juillet 2024, pour l'ordre de grandeur seulement
venues = set(load_venues())
con = connect(mem="700MB", threads=2)
X = f"read_parquet('{BIG}/exit_flows.parquet')"
winners = [r[0] for r in con.execute(f"""SELECT owner FROM read_parquet('{BIG}/wallets.parquet') WHERE sold_no_basis_qty <= 0.05*greatest(sold_qty,1)
    AND transfer_in_qty <= 0.05*greatest(bought_qty+transfer_in_qty,1) ORDER BY realized_sol DESC LIMIT 40""").fetchall()]
core = json.loads((DATA / "prevent_groups.json").read_text())[0]["members"]
popular = {r[0] for r in con.execute(f"SELECT dst FROM {X} GROUP BY 1 HAVING count(DISTINCT wallet) >= 15").fetchall()}
traced = {r[0] for r in con.execute(f"SELECT DISTINCT wallet FROM {X}").fetchall()}


def out_rows(w):
    rows = con.execute(f"""SELECT dst, sum(CASE WHEN asset='SOL' THEN amount ELSE amount/{USD} END), bool_or(truncated)
                           FROM {X} WHERE wallet=? AND dst IS NOT NULL GROUP BY 1""", [w]).fetchall()
    return rows


def classify(a):
    if a in venues or a == "5Q544fKrFoe6tsEbD7S8EmxGTJYAKtTVhAW5Q5pge4j1":
        return "pool"
    lab = label(a)
    if lab:
        return lab
    return "service non nommé (vu par ≥ 15 wallets tracés)" if a in popular else None


def trace(w, depth=3):
    res = {"frontieres": defaultdict(float), "wallets": defaultdict(float), "tronque": False, "non_trace": 0.0}
    frontier = {w: None}
    seen = {w}
    for level in range(depth):
        nxt = defaultdict(float)
        for a, share in frontier.items():
            rows = out_rows(a)
            if not rows:
                if a != w:
                    res["non_trace"] += share or 0
                continue
            total = sum(r[1] for r in rows) or 1
            for dst, amt, tr in rows:
                res["tronque"] |= bool(tr)
                part = amt if a == w else share * amt / total  # au-delà du premier saut : part proportionnelle, approximative
                c = classify(dst)
                if c:
                    res["frontieres"][f"{level + 1}:{c}"] += part
                elif dst not in seen:
                    seen.add(dst)
                    if dst in traced and level < depth - 1:
                        nxt[dst] += part
                    else:
                        res["wallets"][dst] += part
        frontier = nxt
    return res


out = {}
for tag, lst in (("gagnants", winners), ("groupe_lancement", core)):
    for w in lst:
        r = trace(w)
        if r["frontieres"] or r["wallets"]:
            out[w] = {"groupe": tag, "frontieres": {k: round(v, 1) for k, v in sorted(r["frontieres"].items(), key=lambda kv: -kv[1])[:12]},
                      "wallets_non_etiquetes": {k: round(v, 1) for k, v in sorted(r["wallets"].items(), key=lambda kv: -kv[1])[:6]},
                      "tronque": r["tronque"], "part_non_tracee": round(r["non_trace"], 1)}
(DATA / "exit_summary.json").write_text(json.dumps(out, indent=1, ensure_ascii=False))
agg = defaultdict(float)
for w, v in out.items():
    for k, x in v["frontieres"].items():
        if "pool" not in k and "Jupiter" not in k:
            agg[k.split(":", 1)[1]] += x
print("wallets", len(out))
for k, v in sorted(agg.items(), key=lambda kv: -kv[1])[:14]:
    print(round(v), "SOL éq.", k)
