#!/usr/bin/env python3
"""Table des frontières en Markdown depuis flow_boundaries.csv. Dénominateur : flux sortants hors interne, hors pools et routes. Écrit g64_table.md."""
import csv, collections
OUT = "audits/2026-11-03/work_G/"
PER = ["P1 créateur et dépôt 9W9b", "P2 groupe de 33 et salve du 23/07", "H3QsBr", "GXZvX", "9PrmF8"]
GROUP = [("compte de dépôt balayé vers Coinbase", "Dépôt balayé vers Coinbase (B)"), ("compte balayé vers autre plate-forme", "Compte balayé vers autre plate-forme (B ou C)"), ("pont, ordre inter-chaînes", "Pont, ordre inter-chaînes (B)"), ("hot wallet ou service étiqueté", "Hot wallet ou service étiqueté (A)"), ("famille de hot wallets présumée", "Famille présumée (C)"), ("service ou pool non nommé", "Service ou pool non nommé (C)"), ("wallet sondé", "Wallet sondé, trace arrêtée (C)"), ("wallet non suivi", "Wallet non suivi, aucun historique (D)"), ("autre périmètre", "Autre périmètre (A)")]
T = collections.defaultdict(collections.Counter); uncert = collections.defaultdict(collections.Counter); inte = collections.Counter(); pool = collections.Counter(); dm = collections.defaultdict(collections.Counter)
for r in csv.DictReader(open(OUT + "flow_boundaries.csv", encoding="utf-8")):
    p = r["perimetre_source"]; t = r["type_frontiere"]; v = float(r["sol_eq"])
    if p not in PER: continue
    if r["actif"] == "DMAGA":
        dm[p][t.split(" [")[0]] += float(r["montant"]); continue
    if t.startswith("interne"): inte[p] += v; continue
    if t.startswith("pool ou route"): pool[p] += v; continue
    k = next(g for g, _ in GROUP if t.startswith(g))
    T[k][p] += v
    if "[" in t: uncert[k][p] += v
D = {p: sum(T[g][p] for g, _ in GROUP) for p in PER}
L = ["| Frontière (niveau de la qualification) | " + " | ".join(p.split()[0] for p in PER) + " | Total | Part |", "|---|" + "---|" * (len(PER) + 2)]
tot = sum(D.values())
for g, name in GROUP:
    row = [f"{T[g][p]:.1f}" + (f" (dont {uncert[g][p]:.1f} hors historique)" if uncert[g][p] >= 0.05 else "") for p in PER]
    s = sum(T[g][p] for p in PER)
    L.append(f"| {name} | " + " | ".join(row) + f" | {s:.1f} | {100 * s / tot:.1f} % |")
L.append("| **Dénominateur** | " + " | ".join(f"**{D[p]:.1f}**" for p in PER) + f" | **{tot:.1f}** | 100 % |")
L.append("| Interne, hors dénominateur | " + " | ".join(f"{inte[p]:.1f}" for p in PER) + f" | {sum(inte.values()):.1f} | |")
L.append("| Pools et routes, hors dénominateur | " + " | ".join(f"{pool[p]:.1f}" for p in PER) + f" | {sum(pool.values()):.1f} | |")
open(OUT + "g64_table.md", "w", encoding="utf-8").write("\n".join(L) + "\n")
print("\n".join(L))
print("DMAGA transférés, M", {p: {k: round(v / 1e6, 2) for k, v in dm[p].most_common(5)} for p in PER})
