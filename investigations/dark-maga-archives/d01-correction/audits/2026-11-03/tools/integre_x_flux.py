#!/usr/bin/env python3
"""Intègre X, flux et test d'organisation aux générateurs. Échoue si un texte attendu manque : aucune substitution muette."""
from pathlib import Path


def patch(path, pairs):
    p = Path(path)
    s = p.read_text()
    for old, new in pairs:
        assert s.count(old) == 1, (path, s.count(old), old[:70])
        s = s.replace(old, new)
    p.write_text(s)


CAW = "Caw4RrwkmxqtbLSFzgSs6id3XiFxWQxs2t1mrn5a3mME"
ESS = f"""
8. **Un second compte de dépôt, et une sortie propre à chaque grappe (flux, 03/11, non audité à cette étape).** `{CAW}` reçoit 590 933,95 USDC et 35,63 SOL de 55 expéditeurs, dont 27 des 48 de 9W9b, et balaie vers Coinbase (B pour le type ; témoin : au plus 4 communs sur 7 140 paires). Avec lui, 14 et non 13 des 2 201 destinataires reversent à l'un des deux dépôts, tous dans les 507 s. Le périmètre du créateur vend surtout par ordres DCA (47 ordres, 113,37 M, 1 292,4 SOL éq.) et s'arrête à 86,6 % sur ces deux dépôts. Le bloc `G41vRrsH…`, le bloc `74qFhHyp…` et `9PrmF8…` ont chacun leur sortie : le contrôle commun entre grappes n'est **pas établi**, et une seule jonction par dépôt existe hors des 2 wallets déjà dans la série, 4 wallets, 31,9 SOL, le 23/07/2024. Détail : `audits/2026-11-03/work_G/FLOW_BOUNDARIES.md`.
9. **Les 33 sortent d'abord par des ponts, pas par Coinbase.** 76 ordres deBridge décodés, 1 018 687 USD. Ponts 44,5 % des SOL éq. tracés des 33, dépôts Coinbase 1,4 %. `C73Yv9iH…` envoie 496 372 USD vers un même receveur Ethereum dès 22:53:42 le 21/07/2024. `Ei5yGz8d…`, `Gcyg2jeL…`, `HGBiExZR…` désignent un même receveur, 263 573 USD en 9 min 36 s le 22/07/2024 (B pour un même opérateur ou compte). A pour l'ordre, exécution à l'arrivée non vérifiée.
10. **La chronologie du visuel recule.** Plus ancienne image connue de la composition : @kikisknees, 12:50:45 UTC le 21/07, sans drapeau. Image identique à l'avatar : @FrancoAppr, 16:00:59 UTC, 90 s avant @ChrisWinig. @kikisknees écrit à Musk le 18/07 à 22:22:13 UTC : « We are building an army for you for that purpose. $DMAGA », avec une autre image de Musk (A pour les posts ; rien ne montre que Musk les a vus). Cela établit une campagne publique visant Musk, pas une information venant de lui. Voir Q2 et `audits/2026-11-03/work_E/X_FOLLOWUP.md`.
11. **Un réseau de transferts entre premiers acheteurs n'est pas atypique à lui seul.** Test gelé `etude_groupe/` : verdict **INCONCLUSIF (collecte)**, k = 48 sur 59 requis. À titre descriptif, seuls 4,2 % de ces 48 tokens de juillet 2024 n'ont aucun réseau. DMAGA est haut (34 wallets, 87,5e centile ; 21,7 % de l'offre, 91,7e), sans être le maximum. Voir la section dédiée."""

patch("scripts/rep_90_case.py", [
    (", fourni par la mission, source sociale non retrouvée", ""),
    ("Leurs entrées précoces restent compatibles avec un pari spéculatif. Le contraire n'est pas exclu.",
     "Leurs entrées précoces restent compatibles avec un pari spéculatif. Le contraire n'est pas exclu. Indirectement : deux wallets de la série donnent 1,5 M et 1 M à deux wallets qui versent ensuite aux dépôts de `GXZvX…` (C, sans retour de SOL sous 7 jours, vente réglée ailleurs possible). `9PrmF8…` partage le dépôt `H9XezqfdXuv4ZCHAAZ92oMLSSAPB6Dgm4ZSrRythCbPi` avec 9 wallets, 8 sur 10 touchent DMAGA (B pour un même opérateur ou compte), sans recouvrement avec les autres dépôts."),
    ("Le DM à Musk reste revendiqué, non prouvé.\n", "Le DM à Musk reste revendiqué, non prouvé (D). Indice seulement : @XHEILIGX publie l'adresse de `9PrmF8…` le 30/03/2024, 106 jours avant le mint, et promeut ensuite $DMAGA (C : une adresse se copie, le compte n'est pas du noyau, il manque une revendication ou une signature)." + ESS + "\n"),
    ("reste non identifié, aucune conclusion sur lui (A-16).", "a la forme d'un sandwich sur 1 913 blocs sur 1 913 (A pour la forme, B pour un trésor unique, `4ToQp55m…`, identité inconnue) : 3,12 % des achats, net de jetons nul, marge 194,85 SOL, aucun lien vu avec les périmètres (G8, `audits/2026-11-03/work_G/FLOW_BOUNDARIES.md`)."),
    ("Plus ancienne image identique archivée : @ChrisWinig, 21/07 16:02:29 UTC, pHash à distance 0 de l'avatar de Musk (A).",
     "L'auteur du fichier n'est pas établi. Plus ancienne image connue de cette composition : @kikisknees, 21/07 12:50:45 UTC, réponse à @pmarca, téléversée à 12:50:21, rouge sans drapeau, pHash 14 de l'avatar, même visage et même armure à l'œil (A). Plus ancien envoi connu à Musk de cette variante : @GreatBambin0, 15:58:21 UTC (A). Plus ancienne image identique à l'avatar : @FrancoAppr, 16:00:59 UTC, pHash 0, puis @ChrisWinig, 16:02:29 UTC, pHash 0 (A). Une occurrence antérieure reste possible : la plupart des 164 images 900 x 900 de @kikisknees d'avant 12:51 n'ont pas été relues."),
    ("Une réponse de @kikisknees à Musk à 16:00:08 UTC a perdu son image : **on ne peut pas exclure qu'il ait publié le visuel 2 min 21 s plus tôt** (D).",
     "L'image de la réponse de @kikisknees à Musk de 16:00:08 UTC est retrouvée : c'est le Trump « dark maga » de @DarkMagaCoin, même sha256, pas le visuel de Musk (A). Une autre composition, Musk aux yeux laser dans une foule, circule dès le 16/07 (@FrancoAppr) et @kikisknees l'envoie à Musk le 18/07 à 22:22:13 UTC (A pour le post)."),
    ("Corpus partiel : pas de recherche X native.", "Le post du 20/07 à 20:46:54 de @pmarca reprend l'image d'une réponse de @kikisknees de 19:05:03, avec un lien vers ce statut (A). « Is Elon mooning with us? » répond à une plaisanterie sur la Lune, avec l'image de Musk jointe. Corpus partiel : 30 recherches natives en lecture seule le 03/11 et 1 249 textes Wayback de plus, mais 1 306 posts du 11/06 au 10/07 et 379 du 22 au 26/07 restent à lire."),
    ("Aucun lien de propriété documenté. Trois mentions de tiers, aucune adresse de wallet publiée par un compte du noyau (`reports/ATTRIBUTION.md`).",
     "Aucun lien de propriété documenté. Trois mentions de tiers, aucune adresse de wallet publiée par un compte du noyau dans ce qui est lu (`reports/ATTRIBUTION.md`). La source sociale de `9PrmF8…` est retrouvée : fils de tiers d'août 2024, et @XHEILIGX, indice C (point 7). @twicrates écrit le 23/07 « i was sent some », sans adresse (C)."),
    ("Le contenu de la réponse de 16:00:08 UTC ; le DM ;", "L'auteur du fichier du visuel ; le DM ;"),
    ("Volume artificiel non testé", "Volume artificiel : seule la forme de sandwich de A-16 est mesurée, 3,12 % des achats, pas de test général"),
    ("## État des relectures\n", """## Test d'organisation du groupe précoce (`etude_groupe/`)
Plan gelé le 03/11 à 10:53:59 UTC, avant toute lecture de transferts d'un comparateur, mesures choisies après avoir vu DMAGA. Population : tokens de la variante principale créés en juillet 2024, à pic tardif. Cohorte : 30 plus gros acheteurs nets, comptes de jetons lus avant S, extension par transfert retenu.

**Verdict du code : `INCONCLUSIF (collecte) : 48 comparateurs, il en faut 59`.** Le plafond de 60 000 crédits a arrêté la collecte. Le coût réel, environ 1 250 crédits par token, avait été sous-estimé. Prolonger ne servirait pas à conclure : à k = 115, seul un DMAGA au-dessus de tous ses pairs passerait, et 4 à 8 pairs le dépassent déjà.

| Mesure | DMAGA | Médiane des pairs | Maximum | Pairs au-dessus ou égaux | Centile | Pairs à zéro |
|---|---|---|---|---|---|---|
| G1, wallets de la plus grande composante | 34 | 8 | 77 | 6 | 87,5 | 4,2 % |
| G2, part de l'offre tenue à S | 21,70 % | 3,77 % | 80,5 % | 4 | 91,7 | 25,0 % |
| G3, paires reliées | 50 | 23 | 114 | 8 | 83,3 | 4,2 % |

**Lecture, descriptive :** un réseau de transferts entre gros acheteurs précoces est courant parmi ces tokens. Son existence ne suffit donc pas à rendre DMAGA atypique, ce n'est pas une équivalence, et ce test ne mesure ni la série de retraits Coinbase ni les dépôts communs. **Écart de protocole :** la table n'a été gelée qu'après les tests, à cause d'une erreur de shell, écrit dans le verrou et dans `etude_groupe/results.md`. 10 pairs ont une extension plafonnée, leur valeur peut être sous-estimée.

## État des relectures
**Ajoutés après la confrontation D :** flux (`audits/2026-11-03/work_G/`), enquête X (`audits/2026-11-03/work_E/`), test d'organisation. Ils passent par le nouvel audit des conclusions, voir `audits/2026-11-03/`.
"""),
])

patch("scripts/rep_72_links.py", [("fourni par la mission, source sociale non retrouvée", "fils de tiers d'août 2024 et @XHEILIGX, 30/03/2024, voir audits/2026-11-03/work_E/X_FOLLOWUP.md, partie 6")])

patch("scripts/rep_75_timeline.py", [
    ('for line in (DATA / "x_posts.jsonl").open():\n    r = json.loads(line)\n    posts.setdefault(r["id"], r)\n',
     'for src_ in (DATA / "x_posts.jsonl", Path("audits/2026-11-03/work_E/x_posts_new.jsonl")):\n    for line in src_.open():\n        r = json.loads(line)\n        posts.setdefault(r["id"], r)\n'),
    ('P(1814779160377602331, "@pmarca publie une image rouge aux yeux laser", "A", "Pas le visuel de Musk."),',
     'P(1813310692243480937, "@FrancoAppr répond à Musk avec une image de Musk aux yeux laser, autre composition", "A", "Lien avec l\'avatar : C."),\n    P(1814063148917256375, "@kikisknees à Musk : « We are building an army for you for that purpose. $DMAGA »", "A", "Même image que le post du 16/07, pHash 0. Rien ne montre que Musk l\'a vue."),\n    P(1814763940410499481, "@pmarca publie une image rouge aux yeux laser, avec un lien vers une réponse de @kikisknees", "A", "Pas le visuel de Musk. L\'id du corpus était celui d\'un repost."),'),
    ('P(1815004677160776126, "@pmarca, nouvelle image", "A"),', 'P(1814920352134537332, "@pmarca, nouvelle image", "A", "L\'id du corpus était celui d\'un repost."),'),
    ('P(1815006501896872388, "@kikisknees sollicite publiquement @pmarca sur Elon", "B"),',
     'P(1815006501896872388, "@kikisknees répond à @pmarca, plus ancienne image connue de la composition de Musk, sans drapeau", "A", "Contexte de plaisanterie sur la Lune."),'),
    ('P(1815054158367432804, "@kikisknees répond à Musk avec une image", "B", "Média perdu : impossible de dire si c\'est le visuel."),',
     'P(1815053713330876681, "@GreatBambin0 envoie à Musk la variante sans drapeau", "A", "Plus ancien envoi connu de cette composition à Musk."),\n    P(1815054158367432804, "@kikisknees répond à Musk avec une image", "A", "Image retrouvée : le Trump « dark maga » de @DarkMagaCoin, pas le visuel de Musk."),\n    P(1815054374982324401, "@FrancoAppr répond à Musk avec l\'image identique à l\'avatar", "A", "Plus ancienne image identique connue, pHash 0."),'),
    ('"Plus ancienne image identique au corpus (pHash distance 0 avec l\'avatar)."', '"pHash 0, 90 s après @FrancoAppr."'),
    ('P(1815107774113587625, "@ChrisWinig réagit", "A"),', 'P(1815107549903135205, "@ChrisWinig réagit", "A", "L\'id du corpus était celui d\'un repost."),'),
])

patch("scripts/chk_90_selfcheck.py", [
    ('known |= set(B58.findall(Path("docs/SOCIAL_FINDINGS.md").read_text()))',
     'known |= set(B58.findall(Path("docs/SOCIAL_FINDINGS.md").read_text()))\n# flux et enquête X du 03/11 : sorties écrites par script, chaque adresse copiée du brut\nfor extra in ("audits/2026-11-03/work_G/flow_boundaries.csv", "audits/2026-11-03/work_G/g43_orders.csv", "audits/2026-11-03/work_G/g30_in.csv", "audits/2026-11-03/work_E/x_posts_new.jsonl"):\n    known |= set(B58.findall(Path(extra).read_text()))\nknown.add("' + CAW + '")'),
])
print("ok")
