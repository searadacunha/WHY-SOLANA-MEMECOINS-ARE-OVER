#!/usr/bin/env python3
"""Résout les préfixes de la mission avec assertion d'unicité, et mesure la couverture du brut pour chaque wallet cible.
Sorties : work_G/targets.csv (wallet, rôles, net complet ?, flows ?), work_G/prefixes.txt."""
import csv, json, os, collections
ROOT = "audits/2026-11-03/"
NET = "/Volumes/VERBATIM HD/Dark-MAGA-Investigation/audits_work/C/net/"
FL = "/Volumes/VERBATIM HD/Dark-MAGA-Investigation/raw/flows/"
OUT = ROOT + "work_G/"
net = {f[:-9] for f in os.listdir(NET) if f.endswith(".jsonl.gz") and not f.startswith("._")}
flows = {d for d in os.listdir(FL) if not d.startswith("._")}
roles = collections.defaultdict(set)
for r in csv.DictReader(open(ROOT + "work_C/cb_series.csv")): roles[r["wallet"]].add("serie15")
for r in csv.DictReader(open(ROOT + "work_D/d20_senders.csv")): roles[r["sender"]].add("exp9W9b")
g = json.load(open("data/prevent_groups.json"))[0]
for a in g["members"]: roles[a].add("g33")
CRE = "8YLEuUtZ4eFMJbf46oNb1CeG6dYFWGyxnQSh9hrgzBzR"; roles[CRE].add("createur")
for a in ("H3QsBrrivimFJmSpTXuvig2n1Bh7JuYxrriRSEszT6cc", "GXZvXsD6hxaLeFvQisWpdAwsayJxga7w9EeafhFZG2Ra", "9PrmF8sfoD2YShtWUghrGEYgxwabpnzog8gT1V6LEtdq"): roles[a].add("gagnant")
known = set(roles) | net | flows
for r in csv.DictReader(open(ROOT + "work_C/sol_edges.csv")): known |= {r["src"], r["dst"]}
for r in csv.DictReader(open(ROOT + "work_C/edges40_replay.csv")): known |= {r["src"], r["dst"]}
with open(OUT + "prefixes.txt", "w") as f:
    for p in ("G41vRrsH", "74qFhHyp", "AtZjv3Du", "NxtXcmEW", "GFpqfjEQ", "H9Xezqfd", "9PrmF8", "GZXKYzwZ", "4ToQp55m", "5g7yNH", "BuHUkjUy", "FZLmLkf9", "HBsgbps"):
        hits = sorted(a for a in known if a.startswith(p))
        print(p, hits, file=f)
        assert len(hits) <= 1, (p, hits)
        if hits: roles[hits[0]].add("nomme")
with open(OUT + "targets.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow("wallet roles net net_n net_complete flows_dir flows_truncated".split())
    for a in sorted(roles):
        c = {}
        if a in net:
            c = json.load(open(NET + a + ".cursor.json")) if os.path.exists(NET + a + ".cursor.json") else {"n": "?", "complete": "?"}
        tr = ""
        if a in flows:
            import gzip
            tr = ";".join(q[:-8] for q in sorted(os.listdir(FL + a)) if not q.startswith("._") and json.load(gzip.open(FL + a + "/" + q, "rt")).get("truncated"))
        w.writerow([a, "|".join(sorted(roles[a])), a in net, c.get("n", ""), c.get("complete", ""), a in flows, tr])
print(open(OUT + "prefixes.txt").read())
rows = list(csv.DictReader(open(OUT + "targets.csv")))
print("cibles", len(rows), "net", sum(r["net"] == "True" for r in rows), "net incomplet", [ (r["wallet"], r["net_n"]) for r in rows if r["net"] == "True" and r["net_complete"] != "True"], "flows", sum(r["flows_dir"] == "True" for r in rows))
print("ni net ni flows", [r["wallet"] for r in rows if r["net"] != "True" and r["flows_dir"] != "True"])
print("sans net, roles", collections.Counter(r["roles"] for r in rows if r["net"] != "True"))
print("avec tronqué", [(r["wallet"][:8], r["flows_truncated"]) for r in rows if r["flows_truncated"]])
