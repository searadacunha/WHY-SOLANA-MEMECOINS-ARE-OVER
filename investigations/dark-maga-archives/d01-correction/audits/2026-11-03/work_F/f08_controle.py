"""Contrôle du livrable : chaque correction R01 à R26 se lit dans les rapports générés, et ce que CORRECTIONS.md interdit n'y est pas. Lecture seule. Sortie : f08_controle.txt."""
import re, sys
from pathlib import Path
def lire(p): return Path(p).read_text().replace(" ", " ")
CASE, COORD, ATTR, TOP, EARLY, MISS = (lire(p) for p in ("docs/CASE_REPORT.md", "reports/COORDINATION.md", "reports/ATTRIBUTION.md", "reports/TOP_TRADERS.md", "reports/EARLY_BUYERS.md", "reports/MISSING_EVIDENCE.md"))
TOUS = {"CASE": CASE, "COORD": COORD, "ATTR": ATTR, "TOP": TOP, "EARLY": EARLY, "MISS": MISS}
bad = 0
def c(ident, ok, quoi):
    global bad
    bad += not ok
    print(("OK  " if ok else "ECHEC"), ident, quoi)
def has(ident, doc, *mots):
    for m in mots: c(ident, m in doc, f"présent : {m}")
def non(ident, doc, *mots):
    for m in mots: c(ident, m not in doc, f"absent : {m}")
h2 = next(l for l in CASE.splitlines() if l.startswith("| H2,"))
has("R01", CASE, "Il n'apporte donc d'élément ni pour ni contre une connaissance préalable", "Verdict : **DMAGA NON DISTINGUABLE DE SES PAIRS**"); non("R01", CASE, "Aucune preuve d'achat informé", "Test gelé non significatif"); non("R01", h2, "Test gelé non significatif", "test sans puissance")
has("R02", CASE, "contrôle de la plomberie seulement", "3,3 % pour l'effet moyen", "7,5 % pour le fort"); has("R02", COORD, "contrôle de la plomberie seulement")
non("R03", CASE, "copie neuve", "tests.json` et `verdict.json` identiques"); non("R03", COORD, "copie neuve"); has("R03", CASE, "audits A, B et D")
has("R04", CASE, "Le verdict ne bascule que si DMAGA dépasse tous les pairs sur au moins une mesure", "M3 et M4 ne peuvent pas ouvrir", "Niveau réel 2,4 %")
c("R05", CASE.count("autour du créateur") == 1 and "Retirés après l'audit" in next(l for l in CASE.splitlines() if "autour du créateur" in l), "« autour du créateur » seulement dans la liste des retraits"); non("R05", COORD, "autour du créateur"); non("R05", ATTR, "autour du créateur"); has("R05", CASE, "Le groupe de 33, relié par des transferts", "Le périmètre du créateur, relié par une série")
has("R06", CASE, "13 des 2 201 destinataires", "B pour le même opérateur ou le même compte de dépôt, sur le créateur et 12 wallets"); non("R06", CASE, "Un hot wallet coupe la trace", "rupture de traçabilité"); has("R06", ATTR, "le créateur et 12 wallets")
has("R07", CASE, "est un compte de dépôt Coinbase", "un plancher", "31 de ses 48 expéditeurs", "8 sur 1 365"); has("R07", COORD, "c'est un plancher"); non("R07", COORD, "pas un service de masse", "non tranché"); non("R07", CASE, "non tranché")
has("R08", CASE, "BuHUkjUyWGTwz1suyWpqY6ZcYLX9rbfRsT5nnHFGXykc reçoit 6,576337507 SOL", "vaut B pour 2025, sans valeur pour le lancement"); non("R08", ATTR, "non interprété")
has("R09", CASE, "au moins 2,4 %", "2,9 % avec 3 destinataires", "37,3 % contre 40,8 à 43,7 %"); non("R09", COORD, "Résultat favorable à une lecture modeste")
has("R10", CASE, "sans étiquette 42,4 %, pools 22,1 %, Jupiter 20,6 %, échanges étiquetés 14,8 %", "189 échange, 184 sans étiquette, 114 Jupiter, 4 service", "borne basse", "du 14/07/2023 au mint"); c("R10", "**Surtout" not in CASE and "Surtout d'échanges" not in CASE, "« Surtout d'échanges » retiré de Q6")
has("R11", CASE, "100,78 SOL hors allers-retours", "145,44 SOL"); has("R11", EARLY, "Part des allers-retours sous 10 s, par fenêtre", "30,7 %")
bloc = TOP[TOP.index("## 100 plus gros acheteurs"):TOP.index("## Écartés des classements")]
for a in ("5V97uEb4ZNuXFudphU5nwUapRmt7a2V51TbULQvPJwnx", "AD65fgYti96iSSzSPaNazV9Bs29m7JbNomGjG4Cp5WFS", "BmanDqQELF7QY5uRPw8vg3eMjR74WZnszKmNbLJKkay3"): c("R11", a not in bloc, f"{a[:8]} retiré du classement des acheteurs")
bloc2 = EARLY[EARLY.index("## Plus gros acheteurs dans les 6 h"):EARLY.index("## Plus gros acheteurs dans la fenêtre")]
c("R11", "5V97uEb4" not in bloc2 and "AD65fgYt" not in bloc2, "bots retirés des deux tableaux d'avant Musk")
has("R12", CASE, "27 196 ruptures sur 1 168 comptes", "2 845 M")
has("R13", CASE, "09:01:46", "18 247 sur 53 960", "9 816 à plus de 0,1 SOL"); non("R13", CASE, "18 367", "09:00 UTC")
has("R14", EARLY, "Cohortes de premier achat", "## Plus gros acheteurs dans les 6 h avant le visuel", "## Plus gros acheteurs entre le visuel et la borne basse"); non("R14", EARLY, "Deux cohortes distinctes"); non("R14", CASE, "Les deux cohortes sont distinctes")
has("R15", COORD, "Acheté M, toute la vie", "SOL engagé, toute la vie")
has("R16", CASE, "de 16,0 à 17,7 %"); has("R16", COORD, "de 16,0 à 17,7 %")
has("R17", CASE, "34 wallets et 41 arêtes"); has("R17", COORD, "34 wallets et 41 arêtes")
has("R18", CASE, "11 à 12 dans le groupe selon le seuil, 11 G41vRrsH")
has("R19", CASE, "83,03 %", "90,18 %")
has("R20", CASE, "508 SOL au vault"); has("R20", EARLY, "402 SOL au lieu de 508")
has("R21", ATTR, "4 500 USDC", "7 397 559", "escrow"); has("R21", CASE, "le créateur déplace sa position"); non("R21", ATTR, "non vérifié)")
has("R22", CASE, "93 522 SOL éq.", "dont 12 tronqués", "82 194 SOL éq.")
has("R23", CASE, "71 706 wallets ici, 71 682"); has("R23", TOP, "71 682 wallets sur 71 706")
has("R24", CASE, "89,78 M détenus à S", "76,3 M de transferts nets", "dans l'heure de S, hors des mesures")
has("R25", CASE, "1 370 sur 1 719", "meilleur p = 0,148")
has("R26", CASE, "121 comparaisons", "hors du registre gelé")
for n in range(1, 18): c("N", f"| N{n:02d} |" in CASE, f"ligne N{n:02d} au rapport")
for nom, d in TOUS.items():
    c("encadré", "NON VALIDÉ tant que les décisions de Benjamin et un nouvel audit des conclusions manquent" in d and "audits/2026-11-03/" in d, f"{nom}")
for nom, d in TOUS.items():
    non("interdit", d, "845,72", "0,55 %", "B pour même bénéficiaire", "Dépôt partagé écarté", "9 contre 3", "68 %")
    c("style", "—" not in d and "–" not in d, f"{nom} sans tiret cadratin ni demi-cadratin")
    c("verbatim", "@@" not in d, f"{nom} sans jeton non injecté")
c("validée", all(re.findall(r"validée", d) == [] for k, d in TOUS.items() if k != "CASE") and CASE.count("validée") == 1 and "« validée » reste interdit" in CASE, "le mot n'apparaît que pour dire qu'il est interdit")
print("ÉCHECS", bad)
sys.exit(1 if bad else 0)
