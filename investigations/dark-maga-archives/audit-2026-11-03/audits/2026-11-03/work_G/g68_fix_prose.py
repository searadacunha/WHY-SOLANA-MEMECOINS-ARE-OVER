#!/usr/bin/env python3
"""Corrections de relecture de g63_prose.md et de g61_refs.py. Chaque remplacement doit trouver exactement une occurrence."""
OUT = "audits/2026-11-03/work_G/"
def fix(path, pairs):
    s = open(path, encoding="utf-8").read()
    for a, b in pairs:
        assert s.count(a) == 1, (s.count(a), a)
        s = s.replace(a, b)
    open(path, "w", encoding="utf-8").write(s)
fix(OUT + "g63_prose.md", [
    ("plus 0,015 SOL de gaz.", "plus 0,015 SOL de gaz aux trois premiers."),
    ("Avec", "Avec") if False else ("`C73Yv9iH` : 57 ventes", "`C73Yv9iH` : 57 ventes"),
    ("Il envoie aussi 2 171,8 SOL à `RBsneDCL`, dont 1 624,8 lus en pur et 547,0 hors historique, de mai 2024 à janvier 2025.", "Avec `BuBXTWEC`, il envoie aussi 2 171,8 SOL à `RBsneDCL`, dont 1 624,8 lus en pur et 547,0 hors historique, de mai 2024 à janvier 2025."),
    ("`59L2oxym` lui verse 0,00864088 SOL trois fois juste après des dépôts en USDC, le même montant exact que dans 7 dépôts témoins sur 120. Le compte a besoin", "`59L2oxym` lui verse 0,00864088 SOL trois fois, juste après des dépôts en USDC. Il alimente aussi 7 dépôts témoins sur 120, et ce montant exact s'y retrouve. Le compte a besoin"),
    ("Gaz de plate-forme : il alimente aussi 7 dépôts témoins sur 120 au même montant. Faux lien.", "Gaz de plate-forme : il alimente aussi 7 dépôts témoins sur 120. Faux lien."),
    ("avec 52 et 42 expéditeurs (`g39.txt`)", "avec 52 et 42 expéditeurs sur ces pages (`g39.txt`)"),
    ("Transaction A, coordination B : 164 s, montants ronds, 3 grappes différentes.", "Transaction A, coordination B : 164 s, montants ronds, au moins 2 grappes d'avant le mint."),
    ("`AverrTRT`, qui rend 352,1 à `42MSVeV4`", "`AverrTRT`, qui verse 352,1 à `42MSVeV4`"),
    ("Aucun des 20 autres n'utilise ces comptes.", "Aucun des 20 autres n'utilise ces comptes, dans ce qui est lu."),
    ("8 sur 10 touchent DMAGA, tous sauf `9PrmF8sf` après le 21/07/2024.", "8 sur 10 touchent DMAGA. Hors `9PrmF8sf`, les 5 dont je lis les mouvements de jetons commencent tous après le 21/07/2024 (`g46.txt`)."),
    ("Ce périmètre est distinct : 0 expéditeur commun avec les 4 autres dépôts. Le rapport ne le présente pas.", "Ce périmètre est distinct : 0 expéditeur commun avec les 4 autres dépôts. L'audit C cite ce dépôt sans le mesurer."),
    ("fermé par le même le 10/10/2024 à 07:42:08 : 88 jours.", "fermé par le même le 10/10/2024 à 07:42:08 : 89 jours."),
    ("0 signataire dans les 33 (A).", "0 signataire dans les 33 (audit A, `a37_svc.txt`, repris)."),
    ("Paiements `SinglePayment` à 3 jambes de `H3QsBrri`, `C73Yv9iH`, `2VTfi1DK`, `A9PkAtBd`, de montants répétés 197,01 et 296,01 USDC : commerçant, pas un lien.", "Paiements `SinglePayment` à 3 jambes de `H3QsBrri`, `C73Yv9iH`, `2VTfi1DK`, aux montants répétés 197,01 et 296,01 USDC : commerçant, pas un lien."),
    ("La classe « pool » lit `reports/data_checks/venues.json`, modifié en parallèle par un autre agent : sert seulement à exclure, et 368,3 SOL éq. de P2 en dépendent au plus.", "La classe « pool » lit `reports/data_checks/venues.json`, modifié en parallèle par un autre agent : sert seulement à exclure, et 1 169,5 SOL éq. de pools et routes en dépendent au plus."),
    ("| G4 | Sorties par pont : 76 ordres inter-chaînes, 1 018 687,18 USD, 21 % des SOL éq. de la table.", "| G4 | Sorties par pont : 76 ordres inter-chaînes, 1 018 687,18 USD, 21,3 % des SOL éq. de la table."),
])
fix(OUT + "g61_refs.py", [
    ('''known |= {r[0] for r in csv.reader(open(OUT + "g42_signers.csv")) if r}''', '''known |= {r[0] for r in csv.reader(open(OUT + "g42_signers.csv")) if r}
known.add("7D7BRcBYepfi77vxySapmeqRNN1wsBBxnFPJGbH5pump")  # le jeton, donné par la consigne
import glob
for f_ in ["g55.csv", "g32_origin.csv"] + glob.glob(OUT + "probe_*.txt"):
    known |= set(re.findall(r"\\b[1-9A-HJ-NP-Za-km-z]{32,44}\\b", open(f_ if "/" in f_ else OUT + f_, encoding="utf-8").read()))'''),
])
print("ok")
