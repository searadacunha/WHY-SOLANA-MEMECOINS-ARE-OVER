#!/usr/bin/env python3
"""Annexe du rapport, écrite par script depuis les fichiers de sortie : signatures complètes des événements cités et table des préfixes. Écrit g61_refs.md. Assemble FLOW_BOUNDARIES.md = g63_prose.md + annexe. Aucune référence n'est recopiée à la main."""
import csv, gzip, json, re, sys, time, collections, os
sys.path.insert(0, "audits/2026-11-03/work_G")
from g_lib import history, parse
OUT = "audits/2026-11-03/work_G/"
iso = lambda t: time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(t))
L = []
def tab(title, head, rows):
    L.append(f"\n### {title}\n")
    L.append("| " + " | ".join(head) + " |"); L.append("|" + "---|" * len(head))
    for r in rows: L.append("| " + " | ".join(str(x) for x in r) + " |")
inp = list(csv.DictReader(open(OUT + "g30_in.csv")))
pick = lambda d, a, b: [r for r in inp if r["depot"].startswith(d) and a <= r["utc"] <= b and float(r["amount"]) > 0]
tab("Salve USDC vers Caw4Rrwk, 22/07/2024", "UTC expéditeur actif montant signature".split(), [(r["utc"], r["sender"], r["asset"], r["amount"], r["signature"]) for r in pick("Caw4", "2024-07-22 05:00", "2024-07-22 06:00")])
tab("Versements de 8 SOL vers 9W9b, 23/07/2024", "UTC expéditeur SOL signature".split(), [(r["utc"], r["sender"], r["amount"], r["signature"]) for r in pick("9W9b", "2024-07-23 02:00", "2024-07-23 03:00")])
tab("Gaz de 59L2oxym vers les dépôts", "UTC dépôt SOL signature".split(), [(r["utc"], r["depot"], r["amount"], r["signature"]) for r in inp if r["sender"].startswith("59L2oxym")])
tab("HW5MqvM1, HKzkNSH2 et leurs dépôts", "UTC expéditeur dépôt SOL signature".split(), [(r["utc"], r["sender"], r["depot"], r["amount"], r["signature"]) for r in inp if r["sender"].startswith(("HW5MqvM1", "HKzkNSH2"))])
tab("GXZvX vers ses dépôts", "UTC dépôt SOL signature".split(), [(r["utc"], r["depot"], r["amount"], r["signature"]) for r in inp if r["sender"].startswith("GXZvXsD6")])
tab("BuHUkjUy vers Caw4Rrwk", "UTC USD signature".split(), [(r["utc"], r["amount"], r["signature"]) for r in inp if r["sender"].startswith("BuHUkjUy") and r["depot"].startswith("Caw4")])
o = list(csv.DictReader(open(OUT + "g43_orders.csv")))
first = {}
for r in o: first.setdefault((r["receiver_dst"], r["chain_id"], r["wallet"]), r)
tab("Ordres inter-chaînes : premier ordre par wallet et receveur", "UTC wallet chaîne receveur USD signature".split(), [(r["utc"], r["wallet"], r["chain_id"], r["receiver_dst"], int(r["give_raw"]) / 1e6, r["signature"]) for r in sorted(first.values(), key=lambda r: -int(r["give_raw"]))[:14]])
gr = collections.defaultdict(lambda: [0, 0.0, "z", "", set()])
for r in o:
    e = gr[(r["receiver_dst"], r["chain_id"])]; e[0] += 1; e[1] += int(r["give_raw"]) / 1e6; e[2] = min(e[2], r["utc"]); e[3] = max(e[3], r["utc"]); e[4].add(r["wallet"])
tab("Tous les receveurs des 76 ordres inter-chaînes", "receveur chaîne ordres USD premier dernier wallets".split(), [(k[0], k[1], e[0], round(e[1], 2), e[2], e[3], " ".join(sorted(e[4]))) for k, e in sorted(gr.items(), key=lambda kv: -kv[1][1])])
tab("Les trois ordres vers le receveur commun 0xb947", "UTC wallet USD signature".split(), [(r["utc"], r["wallet"], int(r["give_raw"]) / 1e6, r["signature"]) for r in o if r["receiver_dst"].startswith("0xb947")])
d = [r for r in csv.DictReader(open(OUT + "g52_orders.csv")) if r["ouverture"] < "2024-07-23"]
tab("Ordres DCA vendant DMAGA ouverts jusqu'au 22/07/2024", "ouverture wallet jetons escrow signature".split(), [(r["ouverture"], r["wallet"], r["jetons"], r["escrow"], r["signature"]) for r in d])
br = list(csv.DictReader(open(OUT + "g33_bridge.csv")))
sel = [r for r in br if r["src"].startswith("NxtXcmEW") and r["dst"].startswith("2VTfi1DK")] + [r for r in br if r["utc"].startswith("2024-07-15 23:4")] + [r for r in br if r["utc"].startswith("2024-09-29") and r["asset"] == "DMAGA"] + [r for r in br if r["src"].startswith("NxtXcmEW") and r["dst"].startswith("C7qEaB6a")]
tab("Arêtes entre les 33 et le périmètre créateur citées", "UTC source destination actif montant signature".split(), [(r["utc"], r["src"], r["dst"], r["asset"], r["amount"], r["signature"]) for r in sel])
m = [r for r in csv.DictReader(open(OUT + "g32_merge.csv")) if r["utc"] >= "2024-06-01"]
keep = [r for r in m if r["a"].startswith(("NxtXcmEW", "2VTfi1DK", "AtZjv3Du", "Fp6kgqHU", "7FGoCB63", "4wComYHQ", "Ei5yGz8d")) and r["utc"] < "2024-07-20" and (r["b"].startswith(("2VTfi1DK", "DfYyxDNE", "NxtXcmEW", "5QhJJcFZ", "B252jsFK", "74qFhHyp")))]
tab("Fusions citées, seuil 0,05 SOL, 5 USD, 100 000 jetons", "UTC a b actif montant signature".split(), [(r["utc"], r["a"], r["b"], r["actif"], r["montant"], r["signature"]) for r in keep])
ev = []
for l in open(OUT + "g48.txt"):
    k = re.match(r"\s+transfert (\S+ \S+) (\S+) (\w+) signataires", l)
    if k: ev.append((k.group(1), k.group(2), k.group(3)))
tab("Transferts de la série vers HW5MqvM1 et HKzkNSH2", "UTC jetons signature".split(), ev)
ev = []
for l in open(OUT + "g42.txt"):
    k = re.match(r"\s+tx du chargeur (\S+ \S+) (\w+) signataires \['(\w+)'", l)
    if k: ev.append((k.group(1), k.group(3), k.group(2)))
tab("Programme 3GMsedVP : déploiement et fermeture", "UTC signataire signature".split(), ev)
ev = [(g, ) for g in re.findall(r"\('(\w{80,90})', '(\w+)', (\d+), (\d+), ([-\d.e]+), ([-\d.e]+)\)", open(OUT + "g59.txt").read())]
rows = [e[0] for e in ev]
tab("Exemple de bloc du programme : jambe, propriétaire, slot, index, jetons, SOL", "signature propriétaire slot index jetons SOL".split(), rows)
ev = re.findall(r"\('(\w{80,90})', '(\w+)', (\d+), ([-\d.e]+), ([-\d.e]+)\)", open(OUT + "g59.txt").read())
tab("Le tiers intercalé du même bloc", "signature propriétaire index jetons SOL".split(), ev)
h = "H9XezqfdXuv4ZCHAAZ92oMLSSAPB6Dgm4ZSrRythCbPi"
ev = [(iso(x["bt"]), s, d, r / 1e6, x["sig"]) for t in history(h) for x in [parse(t)] for k, a, m_, s, d, r, dc in x["moves"] if a == "DMAGA"]
tab("DMAGA reçus par H9Xezqfd", "UTC source destination jetons signature".split(), ev)
g = {}
for l in open(OUT + "g32.txt"):
    k = re.match(r"\s+premier financeur (\S+ \S+) (\w+) (.+?) ([\d.]+) (\w{80,90})", l)
    if k: g[k.group(5)] = k.groups()
tab("Premiers financeurs, dans l'ordre G41vRrsH, 74qFhHyp, AtZjv3Du, NxtXcmEW, GFpqfjEQ", "UTC financeur étiquette SOL signature".split(), list(g.values()))
# table des préfixes cités dans la prose
prose = open(OUT + "g63_prose.md", encoding="utf-8").read()
known = set()
for f in ("targets.csv", "flow_boundaries.csv", "g30_in.csv", "g32_merge.csv", "g33_bridge.csv", "g10_dest.csv", "g52_orders.csv", "g43_orders.csv", "g55.csv"):
    for r in csv.reader(open(OUT + f, encoding="utf-8")):
        for c in r[:3]:
            if re.fullmatch(r"[1-9A-HJ-NP-Za-km-z]{32,44}|0x[0-9a-f]{40}", c): known.add(c)
known |= {r[0] for r in csv.reader(open(OUT + "g42_signers.csv")) if r}
known.add("7D7BRcBYepfi77vxySapmeqRNN1wsBBxnFPJGbH5pump")  # le jeton, donné par la consigne
import glob
for f_ in ["g55.csv", "g32_origin.csv"] + glob.glob(OUT + "probe_*.txt"):
    known |= set(re.findall(r"\b[1-9A-HJ-NP-Za-km-z]{32,44}\b", open(f_ if "/" in f_ else OUT + f_, encoding="utf-8").read()))
known |= {r["dst"] for r in csv.DictReader(open(OUT + "g10_dest.csv"))}
for f in ("g37.txt", "g43.txt", "g45.txt", "g42.txt", "g46.txt", "g47.txt", "g48.txt", "g49.txt", "g39.txt", "g56.txt", "prefixes.txt", "g31_ctrl_overlap.txt", "g41_a16_look.txt"):
    known |= set(re.findall(r"\b[1-9A-HJ-NP-Za-km-z]{32,44}\b|0x[0-9a-f]{40}", open(OUT + f, encoding="utf-8").read()))
ps = sorted(set(re.findall(r"`([1-9A-HJ-NP-Za-km-z]{5,12}|0x[0-9a-f]{4,10})`", prose)))
rows = []; miss = []
for p in ps:
    h = sorted(a for a in known if a.startswith(p))
    if len(h) == 1: rows.append((p, h[0]))
    else: miss.append((p, len(h)))
tab("Préfixes cités et adresses complètes", "préfixe adresse".split(), rows)
assert not miss, miss
open(OUT + "g61_refs.md", "w", encoding="utf-8").write("\n".join(L) + "\n")
prose = prose.replace("{{TABLE_FRONTIERES}}", open(OUT + "g64_table.md", encoding="utf-8").read().rstrip())
assert "{{" not in prose
open(OUT + "FLOW_BOUNDARIES.md", "w", encoding="utf-8").write(prose.rstrip() + "\n\n## Annexe : références complètes, écrites par script\n" + "\n".join(L) + "\n")
print("préfixes", len(rows), "non résolus", miss)
