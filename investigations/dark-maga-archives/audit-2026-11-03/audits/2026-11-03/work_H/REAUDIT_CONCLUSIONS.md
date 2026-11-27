# Nouvel audit des conclusions, rapport corrigé

Auditeur H, 03/11/2026. Branche `audit-2026-11-03`, commit `b280ed4`, dérivé `data_v2/`. Personne n'est accusé. Aucune identité civile n'est présumée. Rien n'a été modifié hors de `work_H/` et de `CLAIM_VERIFICATION_V2.csv`.

## 1. Verdict global : FAIL

Les chiffres tiennent, le texte ne suit pas partout. Le rapport ne peut pas être dit validé.
- **0 BLOQUANT, 10 MAJEUR, 22 MINEUR.**
- **Ce qui tient :** R01 à R26 appliquées, N01 à N17 présentes avec leur niveau, verdicts gelés mot pour mot, test gelé retiré des appuis de H2, aucune identité civile, aucun lien X vers wallet affirmé. Environ 90 chiffres recalculés sur `data_v2/` et les tables gelées retombent juste.
- **Ce qui ne tient pas :** les ajouts de la dernière étape (flux, X) n'ont pas été propagés ni bornés. L'essentiel 9 mélange des populations, la chronologie du visuel n'a reculé qu'à moitié, deux formules dépassent leurs sources.
- **Assertions :** 73 PASS, 15 FAIL, 11 INCONCLUSIVE sur 99 (`CLAIM_VERIFICATION_V2.csv`). Sur les 51 d'origine : 43 PASS, 5 FAIL, 3 INCONCLUSIVE. FAIL devenus PASS : C19, C34, C35, C49, C50. PASS devenus FAIL : C31, C32, C33, C40, C42.

## 2. Table par critère

| Critère | Verdict | Preuve |
|---|---|---|
| 1. R01 à R26, « À ne pas reprendre », N01 à N17 | **PASS** | Section 3 ; `h02_tables.txt`, partie N01 à N17 |
| 2. Remontée des chiffres | **FAIL** | D01, D11 ; le reste retombe, section 4 |
| 3. Dénominateurs, exploratoire, puissance, limites, verdict | **FAIL** | D01, D08, D17, D21. Verdict et puissance : PASS |
| 4. Portée des conclusions | **FAIL** | D02, D04, D05, D06. Identité et X vers wallet : PASS |
| 5. Cohérence interne | **FAIL** | D03, D07, D09, D10, D18, D30, D31 ; 13 et 14 : cohérents, section 6 |
| 6. Choix de l'agent F | **PASS avec réserves** | Section 7 ; D25 |

Grille à 10 points :

| Point | Verdict | Preuve |
|---|---|---|
| 1. Traçabilité | FAIL | 1 018 687 USD introuvable, 25,5 M faux, D01, D11 |
| 2. Dénominateurs | FAIL | 44,5 % porte sur P2 et non les 33, 86,6 % sans fraction, D01, D21 |
| 3. n effectif | FAIL | Test gelé : 84 jours écrits. `etude_groupe` : 48 tokens, 30 jours de pic, non écrit, D16 |
| 4. Tests multiples | FAIL | `compter` : 33 et 0,00152, justes. Audit A oublié, total hors registre non chiffré, D17 |
| 5. p non résolus | PASS | `compter` : 0 sur les deux études |
| 6. Confirmatoire contre exploratoire | FAIL | D08, D17 |
| 7. Puissance | PASS | 2,4 ; 3,3 ; 7,5 % écrits ; à k = 115 seul un DMAGA au-dessus de tous passerait |
| 8. Portée | FAIL | D02, D06 |
| 9. Déviations | PASS | 001, 002 et l'ajout dans `etude_final/results.md` ; gel tardif et plafond dans `etude_groupe/results.md`. Empreintes : 17 sur 17, 10 sur 10 |
| 10. Forme | PASS | 0 tiret cadratin, 0 demi-cadratin dans les 7 rapports |

## 3. Critère 1 : corrections et formules interdites

**R01 à R26 : toutes présentes, sans déformation.** R10, R13, R22, R24 portent des valeurs recalculées et différentes de `CORRECTIONS.md`, ce qui est juste : 42,4 ; 20,6 ; 184 ; 114 ; 18 247 sur 53 960 ; 9 816 ; 93 522 ; 12 ; 89,78 M, tous retrouvés. R26 suit sa lettre, mais n'a pas vu l'audit A (D17).

**« À ne pas reprendre » : absent.** Recherche dans les 7 rapports : « 68 % », « 12 mois », « 845,7 », « 90,05 », « 0,55 % », « B pour même bénéficiaire », « Dépôt partagé écarté », « 9 contre 3 », « copie neuve », « non tranché » : 0. « autour du créateur » : une seule fois, `docs/CASE_REPORT.md:150`, liste des retraits.

**N01 à N17 : niveaux identiques à `CLAIM_VERIFICATION.csv` sur 17.** Texte identique pour 11. N10 à N13, N16, N17 changent par recalcul, comme l'annonce `docs/CASE_REPORT.md:125`.

## 4. Critère 2 : recalculs

Scripts et sorties : `work_H/h01_recalc`, `h02_tables`, `h03_small`, `h05_misc`, `h06_divers`, `h08_assertions`, `h10_reste`. Requêtes réécrites, sans importer les scripts du rapport, sauf `dmaga.venues` pour la liste des réserves.

| Bloc | Résultat |
|---|---|
| Essentiel 2 | 3,291 ; 145,440 ; 44,66 d'allers-retours par code propre ; 100,78 ; 5 377,788 ; 13,177 ; 84,941 ; 1,291 h ; 236,56 |
| Essentiel 3, test gelé | k 211 ; 84 jours ; M1 à M7, médianes et p depuis `metrics.csv` ; centiles 83,4 ; 82,0 ; 76,3 ; 45,5 ; 73,9 ; 84,8 ; 82,5 ; S1 ; 33 ; 0,00152 |
| Essentiel 4 | 33 ; 40 ; 217,037 ; 23,14 % de 937,765 ; 29 ; 166,111 ; 149,711 ; 15,96 à 17,71 % ; 50,926 ; 15, 206,87 M, 52,27 SOL ; 4 524,91 ; 190 546,47 ; 2,3747 % ; 973,33 ; 2,886 % |
| Essentiel 5 | 2 517 lignes, 2 201 destinataires, 13 ; 01:32:23 à 01:40:50, 507 s ; CV 0,245 ; 31 sur 48 ; 94,46 % ; 7 397 559 |
| Essentiel 6 | 5 490,86 ; 990 743,77 ; 1 086,77 ; 2 540,10 ; 1 747,80 ; 1,5 M et 1 M ; 10 expéditeurs, 8 touchent DMAGA |
| Essentiel 8 | 590 933,95 ; 35,63 ; 55 ; 27 ; 14 ; 47, 113,37 M, 1 292,4 ; 3 138,6 sur 3 626,0, 86,6 % ; 31,9 ; 4 sur 7 140 |
| Essentiel 9 | 76 lignes ; **somme 1 023 933,51 et non 1 018 687** ; 496 371,60 ; 263 573,16 ; 9 min 36 s ; 44,5 % et 1,4 % sur P2 |
| Essentiel 11, `etude_groupe` | k 48 ; 34, 21,70 %, 50 ; max 77, 80,5 %, 114 ; 6, 4, 8 ; centiles 87,5 ; 91,7 ; 83,3 ; zéro 4,2 ; 25,0 ; 4,2. **Médianes exactes 3,56 % et 22,5, voir D16** |
| Données | 913 880 ; 796 883 ; 0 doublon ; 5 903 sur l'ancien ; 71 706 ; 27 196 ; 1 168 ; 1 508,5 + 1 336,9 ; 5 ruptures, 84,737 M ; 243, 3,98 M ; 656,04 ; 567,82 ; chaînes 681 308, 681 300, 83, 215 309, 40, 214 910, 22, 1,23 |
| Allers-retours | 106 254,0 sur 787 109,5, 13,50 % ; 103 wallets, 106 047,8 ; 105 avec 2 de plus, 106 492,6 ; rangs 1 à 3 |
| Q4, Q5 | 184 ; 107 ; 51 ; 53 960 ; 18 247 ; 9 816 ; 631 363,6 à 09:01:46 ; TOP_TRADERS 71 682, 788 319, 783 935, 97 097 |
| Q6, N13 | 1 316 494 ; 42,44 ; 22,14 ; 20,55 ; 14,80 ; 189, 184, 114, 4 |
| Q7, N16 | 65 ; 12 ; 93 521,6 ; 24 485,4 ; 25 765,7 ; 5 échanges |
| N06, N07, N17 | 61,357 ; 92,079 ; 266,697 ; 28,44 % ; 37,28 ; 40,78 ; 43,70 ; 76 ; 845,72 ; 158,88 ; 69,09 ; 89,78 ; 114,96 ; 110,2 ; 76,30 ; 2 762,2 |
| Frise | 36 capitalisations recalculées, 0 écart, dates des ids égales sauf @kanpai, D09. Avatar 19:23:20 |
| Membres, cohortes | 33 lignes égales au groupe ; 97 lignes lues sur les 100 du top des réalisés, égales à `wallets.parquet` ; 100 acheteurs, 0 bot |

**Non recalculés, repris d'une sortie :** puissance de D (`d11_scenarios.csv` relu, simulation non relancée), lecture des captures (C25), textes et images X, sauf les pHash de `visual_new.csv` et `visual_wb.csv`. Brut des flux hors de mon angle.

**Chiffres anciens écrits à la main dans le gabarit.** Aucun ancien chiffre PASS n'aurait dû bouger avec `data_v2/`.

| Chiffre | Lieu | Sur `data_v2/` | État |
|---|---|---|---|
| 33 minutes, 0,5 SOL | `rep_90_case.py:153` | 01:32:23 à 02:05:25, 33 min 02 s | Juste |
| 7,1 M pour 0,2 SOL | `rep_90_case.py:153` | 7,106 M, 0,2012 SOL | Juste |
| 1 087 $ contre 1 086 $ | `rep_90_case.py:146` | 1 086,77 | Juste |
| 844 k$ | `rep_90_case.py:146` | 844 k$ à 13:38:12 | Juste |
| 48,5 SOL, 14,69 M | `rep_90_case.py:146` | 48,5 ; 14,6988, tronqué | Juste, post non relu |
| 0,39 jeton | `rep_90_case.py:145` | 389 935 unités | Juste |
| 112 adresses | `rep_90_case.py:163` | 112 uniques | Juste, 117 ailleurs, D13 |
| 65 minutes, 7 et 2 wallets, 97 ruptures, 5 h 36 | `rep_90_case.py:147,153,167` | Tableau ou audit_facts cohérents | Juste |
| 3,12 %, 194,85, 1 913 | `rep_90_case.py:149` | 24 537,38 sur 787 109,5 ; `g53.txt` | Juste |
| Essentiels 6 à 11 | `rep_90_case.py:134-139` | Voir table, sauf 1 018 687 | Écrits à la main, D01 |
| **25,5 M** | `rep_72_links.py:139` | **26,0 M** | Faux depuis l'origine, D11 |
| **« média perdu », « plus ancienne image identique »** | `rep_70_reports.py:169-170` | Corrigés au rapport principal | Périmés, D03 |
| **« Média perdu » à 18:46:37** | `rep_75_timeline.py:101` | Image retrouvée | Périmé, D10 |
| **117, 208, 17, 972** | `reports/MISSING_EVIDENCE.md`, à la main | 112 ; 1 249 de plus ; 946 chez G | Périmés, D13 |
| **`pmarca_image_rouge` 21:47:23** | `data_v2/events.json` | 20:46:54 | Périmé, D31 |

## 5. Défauts

### MAJEUR

| Id | Défaut | Preuve | Correctif précis |
|---|---|---|---|
| D01 | **Essentiel 9 mélange les populations.** « Les 33 » reçoit 76 ordres et 1 018 687 USD de toutes sources. 8 ordres ne sont pas des 33, dont 2 de `8YSi5yNR`, aval de `H3QsBr…`, que l'essentiel 6 dit sans lien. 44,5 % et 1,4 % portent sur P2 : les 33 moins `5QhJJc…` et `7FGoCB63…`, plus `G41vRrsH…` et `EGtyQEgM…`. La somme ne remonte à aucune sortie | `docs/CASE_REPORT.md:18` ; `g43_orders.csv` : 76 lignes, 1 023 933,51 ; 33 : 68 ordres, 979 324,28, dont 15 avant le mint pour 1 610,19 ; P1 : 3, 3 022,00 ; autres : 5, 41 587,23 ; `work_G/g40_boundaries.py:22` ; `work_H/h02_tables.txt`, `h03_small.txt` | `rep_90_case.py:137` : « 68 ordres deBridge des 33, 979 324 USD, dont 15 avant le mint. Sur les 33 exacts : ponts 5 468,8 SOL éq. sur 12 133,8, 45,1 % ; dépôts Coinbase 165,7, 1,4 %. » Agent G à relire : 1 018 687,18 n'existe que dans sa prose |
| D02 | **« Pas par Coinbase » dépasse la table.** La table s'arrête au premier saut. 29,0 % vont à des wallets sondés et 21,0 % à des wallets non suivis : la suite est inconnue. Le titre fait d'une part 44,5 % une affirmation négative | `work_G/FLOW_BOUNDARIES.md:190,209-212` ; `h03_small.txt` | Titre : « Pour les 33, le pont est la première frontière identifiée. » Ajouter : « Environ la moitié des flux s'arrête sur des wallets dont la suite n'est pas lue : rien n'exclut Coinbase plus loin. » |
| D03 | **La chronologie du visuel n'a reculé qu'à moitié.** L'essentiel 10 place la plus ancienne image à 12:50:45. H2, Q12, COORDINATION et C42 écrivent encore « avant le visuel » pour 14:22-14:25, soit 1 h 31 après. « Le groupe ne trade pas entre le visuel et la bascule » n'est vrai que depuis 16:00:59 : depuis 12:50:45, 3 ventes de `7mdCAs8C`, 12,34 SOL, de 13:26:46 à 14:01:34, et 5 transferts. EARLY_BUYERS garde Winig comme « plus ancienne image identique » et 16:00:08 comme « média perdu », contre Q2 | `docs/CASE_REPORT.md:19,36,56,63` ; `reports/COORDINATION.md:84` ; `reports/EARLY_BUYERS.md:5-6` ; `reports/TOP_TRADERS.md:16` ; `h01_recalc.txt` | Nommer partout trois repères : image de la composition 12:50:45, image identique 16:00:59, borne gelée Winig 16:02:29. H2 et Q12 : « gestes avant l'image identique, le regroupement suit la plus ancienne image de la composition ». Garder les cohortes sous le nom « borne Winig, gelée ». Réécrire `rep_70_reports.py:103,169-170` et `rep_72_links.py:139` |
| D04 | **Le niveau B des 29 ne dit pas ce qu'il note, et s'appuie sur une « sortie commune » que l'essentiel 8 nie.** Les salves du dépôt contiennent 2 des 33 le 23/07 et 2 le 26/01. G conclut « chaque grappe a sa sortie », « contrôle commun non établi » | `reports/COORDINATION.md:79,160-177` ; `docs/CASE_REPORT.md:13,17,64` ; `work_G/FLOW_BOUNDARIES.md:18,135-138` | `rep_72_links.py:134` : retirer « une sortie commune ». Écrire aux trois endroits : « A pour les transferts, B pour une coordination dans chaque bloc, non établi entre blocs, C pour un seul propriétaire ». Séparer les trois colonnes de G |
| D05 | **Le tableau H3 ignore le seul comparatif sur le groupe.** « Soutenue » reste sans témoin, alors que la médiane des pairs vaut 8 wallets, 6 pairs sur 48 atteignent 34, et M6 tient le 84,8e centile. L'essentiel 11 et H3 ne se parlent pas. Le récit de synthèse en penche vers la coordination | `docs/CASE_REPORT.md:20,64,109-113` ; `h02_tables.txt` | Ajouter à la colonne « Ce qui va contre » de H3 : « un réseau de transferts existe chez 46 pairs sur 48, descriptif, test inconclusif ; M6 84,8e centile, non distinguable ; ces mesures ne couvrent ni la série ni les dépôts » |
| D06 | **« Cela établit une campagne publique visant Musk » et « une campagne existe » prêtent une intention.** X_FOLLOWUP écrit : « Toutes sont publiques, aucune n'établit un plan de l'équipe ». @GreatBambin0 et @FrancoAppr ne sont reliés à aucune équipe. H1 reste B | `docs/CASE_REPORT.md:19,61` ; `work_E/X_FOLLOWUP.md:84` | Essentiel 10 : « Cela montre des envois publics répétés à Musk par plusieurs comptes, dont @kikisknees (A). Un plan d'équipe n'est pas établi. Aucune information venant de Musk n'est montrée. » H0 : « une promotion publique existe, sa coordination vaut B » |
| D07 | **deBridge : trois passages contredisent l'essentiel 9.** « Rien dans ces données » et « une adresse deBridge récurrente n'est documentée » alors que `C73Yv9iH…` passe 27 ordres vers un même receveur, 496 371,60 USD | `reports/ATTRIBUTION.md:54` ; `docs/CASE_REPORT.md:153` ; `reports/MISSING_EVIDENCE.md:41` | Séparer : « deBridge : ordres et receveurs récurrents documentés, `work_G/`. Le récit d'une équipe, Ansem, la Solana Foundation : rien dans ces données. » `rep_72_links.py:250`, `rep_90_case.py:250`, édition à la main |
| D08 | **Témoins faits après coup, non étiquetés, alors qu'ils portent le niveau B.** 31 sur 48 contre 8 sur 1 365, 27 contre au plus 4 sur 7 140, 8 sur 10, CV et P 5e-05. G écrit : « Les tests de la section 3 sont exploratoires ». Les limites du témoin de 7 140 paires manquent : SOL seul, 3 pages, USDC en face | `docs/CASE_REPORT.md:14,15,17` ; `reports/ATTRIBUTION.md:38` ; `reports/COORDINATION.md:129,155` ; `work_G/FLOW_BOUNDARIES.md:126,259` | Ajouter « exploratoire, hors plan, périmètre posé après avoir vu les faits » à côté de chacun, et les trois limites à l'essentiel 8 |
| D09 | **Frise : une méthode fausse et une date fausse.** « Dans tous les cas lus, elle égale la métadonnée » : 372 lignes sur 5 155 diffèrent. @kanpai à 16/07 00:14:58 est l'id d'un repost, l'original date du 15/07 à 22:56:01, à 667 k$ et non 556 k$. Q3 écrit « dès le 16/07 » | `docs/TIMELINE.md:4,18` ; `docs/CASE_REPORT.md:38` ; `h02_tables.txt`, `h06_divers.txt`, `h10_reste.txt` | `rep_75_timeline.py:88,125` : id `1812984492157771825`. Méthode : « 372 lignes sur 5 155 portent l'id d'un repost, la date est lue sur l'id d'origine ». Q3 : « dès le 15/07 » |
| D10 | **18:46:37 : « média perdu » alors que l'image est retrouvée.** @kikisknees envoie à Musk la variante V3, 37 minutes avant l'envoi de l'avatar. Le rapport l'omet, dans le sens qui minore le fait | `docs/TIMELINE.md:32` ; `docs/CASE_REPORT.md:38` ; `work_E/X_FOLLOWUP.md:45,233` ; `work_E/evidence/x_media_wb_new/GTCEEQ2WoAAm65s_20240723081618.png` ; `visual_wb.csv` | `rep_75_timeline.py:101` : niveau A, « image retrouvée, V3 ». Q3 : 18:46:37 avec V3 (A), seul 18:55:15 a un média perdu. Dire que rien ne montre que Musk l'a vue |

### MINEUR

| Id | Défaut | Preuve | Correctif |
|---|---|---|---|
| D11 | « Regroupement de 25,5 M » : le tableau voisin donne 26,0 M | `reports/COORDINATION.md:84,220-224` ; `h05_misc.txt` | `rep_72_links.py:139` : 26,0 M, injecté |
| D12 | « Tête au coût connu » saute le rang 3, `FTKTNFqe…`, 2 046 SOL. `9PrmF8…` est 4e | `docs/CASE_REPORT.md:42` ; `reports/TOP_TRADERS.md`, top 100 | « Trois gagnants signalés », et citer `FTKTNFqe…` |
| D13 | MISSING_EVIDENCE périmé : 117 adresses contre 112 ; 208 textes et « la Wayback a refusé la suite » contre 1 249 de plus ; 972 tx contre 946 chez G | `reports/MISSING_EVIDENCE.md:9,30,38` | Reprendre ces valeurs, trancher 972 ou 946 |
| D14 | « Deux jours avant Butler » reste sans le verdict D de X_FOLLOWUP | `docs/CASE_REPORT.md:10,34` ; `work_E/X_FOLLOWUP.md:145` | Ajouter : « D, contredit par les dates lues, une préparation privée reste possible » |
| D15 | Titre de l'essentiel 11 plus fort que la source : « n'est pas atypique » contre « interdit seulement d'écrire » atypique | `docs/CASE_REPORT.md:20` ; `etude_groupe/results.md:19` | « Son existence ne suffit pas à rendre DMAGA atypique, sur un test inconclusif » |
| D16 | `etude_groupe` : 3,77 % et 23 sont la 25e valeur sur 48, médianes exactes 3,56 % et 22,5 ; « 4 à 8 pairs le dépassent », G3 a 7 au-dessus et 1 égal ; 34 contre 33 sans explication ; 48 tokens sur 30 jours de pic, non écrit | `etude_groupe/code/ana_grp.py:75` ; `h02_tables.txt`, `h03_small.txt`, `h08_assertions.txt` | Garder la sortie gelée, ajouter une note : valeur haute de médiane, 4 à 8 « égalent ou dépassent », 34 = 33 + `Habp5bnc…`, n effectif prudent 30 jours |
| D17 | « Comparaisons des audits » oublie l'audit A (`a05`, `a42`, `a43`), dont p 0,150 et 0,148, cités sans étiquette. Le seuil 0,00152 ignore au moins 121 comparaisons | `docs/CASE_REPORT.md:92,98,102` ; `AUDIT_A_DATA.md:72,99` | Ajouter A, étiqueter ces p, écrire : « au moins 154 comparaisons avec celles de B, soit 0,00032 ou moins, sans effet sur le verdict » |
| D18 | TOP_TRADERS : `3GMsedVP…` « non identifié, aucune conclusion », le rapport principal tranche la forme. Commentaire du script : les 45 signataires hors étiquette, or 44 sont étiquetés, 14 478,8 SOL. `4ToQp55m…` reste 2e acheteur sans marque | `reports/TOP_TRADERS.md:283` ; `scripts/ana_23_roundtrip.py:8` ; `h04_choix.txt` | `rep_70_reports.py:121` : renvoyer à G8, marquer `4ToQp55m…` « trésor du sandwich, net de jetons nul » |
| D19 | L'argument des 155 000 lamports reste au niveau B de 9W9b, G le rejette | `reports/COORDINATION.md:154` ; `reports/ATTRIBUTION.md:40` ; `work_G/FLOW_BOUNDARIES.md:223,240` | Retirer, ou écrire « non discriminant » |
| D20 | « Non audité » sur l'essentiel 8 seul, alors que 6, 7, 9, 10, 11 ont le même statut. Pas d'encadré dans la frise | `docs/CASE_REPORT.md:17` ; `docs/TIMELINE.md:1-5` | Marquer ces points, ajouter l'encadré |
| D21 | Taux sans fraction : 86,6 % (3 138,6 sur 3 626,0), 3,12 % (24 537 sur 787 110), 2,9 % (973,3 SOL) | `docs/CASE_REPORT.md:13,17,30` | Écrire numérateur et dénominateur |
| D22 | H2 : la colonne « Ce qui va contre » liste des indices pour. « Inhabituel » et « bien réveillé » pour des p de 0,069 et 0,036 non corrigés, dans un test peu discriminant | `docs/CASE_REPORT.md:63,88` | Colonne : « Indices en sens contraire de la conclusion ». Retirer ces deux mots |
| D23 | H3 : « seule la forme de sandwich est mesurée », alors que N10 mesure 13,5 % d'allers-retours | `docs/CASE_REPORT.md:30,64` | « Mesuré : 13,5 % d'allers-retours, dont 3,12 % de forme sandwich, pas de test général » |
| D24 | Q3 ne cite que 1 306 et 379 posts à lire. Restent aussi 20 avant Butler, puis 54, 8 et 11, soit 73 du 14/07 au 22/07 à 07:00 | `docs/CASE_REPORT.md:38` ; `work_E/X_FOLLOWUP.md:76-82` | Citer les 6 fenêtres |
| D25 | « L'écart restant vient de comptes de wallets non tracés » n'est pas établi : 42,68 M viennent de `ARu4n5mF…`, tracé, classé routeur, 0 ligne de compte. Colonne « Dernier solde vu » trompeuse pour ces cas | `docs/CASE_REPORT.md:29` ; `reports/TOP_TRADERS.md:14` ; `h04_choix.txt`, `h05_misc.txt` | Section 7 |
| D26 | Q7 : 25 511,5 des 25 765,7 SOL éq. de hot présumés viennent de `FaQQATa1…` seul | `h01_recalc.txt` ; `work_F/CORRECTIONS_APPLIQUEES.md:223` | Le dire |
| D27 | N12 : 84,537 M compensés sur 84,737 ; 15 ruptures à cheval, 1,01 M, omises. N17 : « 76,3 M nets, dont 110,2 M » n'est pas une part | `docs/CASE_REPORT.md:29,96,140,145` | « Dont 84,5 M compensés, 1,01 M à cheval » ; « 110,2 M des 114,96 M bruts vont au groupe, 76,3 M nets » |
| D28 | « `C73Yv9iH…` envoie 496 372 USD dès 22:53:42 » se lit comme un envoi : 27 ordres jusqu'au 09/06/2025 | `h02_tables.txt` | Ajouter le nombre et la fin |
| D29 | H1 cite l'outil de pfp, annoncé après l'avatar | `docs/CASE_REPORT.md:62` ; `work_E/X_FOLLOWUP.md:139` | Préciser « après l'adoption » |
| D30 | 13 et 14 non reliés hors de l'essentiel 8. COORDINATION et ATTRIBUTION ne citent jamais `Caw4Rrwk…` : `Fp6kgqHU…` y reste « non » sans suite. ATTRIBUTION écrit « rien ne le soutient », contre G7 et @XHEILIGX | `docs/CASE_REPORT.md:34,64` ; `reports/COORDINATION.md:143` ; `reports/ATTRIBUTION.md:16` | Une phrase de lien, et « indices C seulement » |
| D31 | Fenêtres `avant_pmarca`, `pmarca_a_winig` sur 20/07 21:47:23, id de repost, la frise dit 20:46:54 | `reports/EARLY_BUYERS.md:14-15` ; `data_v2/events.json` | Corriger l'événement dans le dérivé, ou nommer « repost » |
| D32 | Tableau des salves : 14 lignes pour 15 versements, `Cv3p9Wu1…` à 17:21:56 manque. « En réalité » est un reste du fichier d'audit | `reports/COORDINATION.md:164-177` ; `reports/ATTRIBUTION.md:40` ; `h10_reste.txt` | Compléter, reformuler |

## 6. Critère 5 : les incohérences signalées

**Essentiel 5 (13 sur 2 201) et essentiel 8 (14 sur 2 201) : cohérents.** 13 vers 9W9b, 10 vers Caw4, 9 aux deux, 14 en union. `Fp6kgqHU…` est le 14e, `A52fNskQ…` ne verse à aucun, la série de 15 s'en déduit. `work_G/g66.txt`, `h02_tables.txt`. Seul le lien écrit manque (D30).

**`TIMELINE.md` contre Q2 :** même dates pour 12:50:45, 15:58:21, 16:00:59, 16:02:29, 16:00:08. Écarts : @kanpai (D09), 18:46:37 (D10).

**Chiffres répétés :** 33, 40, 217,04, 166,1, 16,0 à 17,7, 4 525, 2,4 ; 2,9 ; 37,3 ; 40,8 à 43,7 ; 13 ; 31 ; 48 ; 94,5 ; 508 ; 402 ; 105 ; 106 493 : égaux d'une section à l'autre. Écarts : D03, D07, D11, D13, D18, D31.

**Récit global.** Il ne pousse pas vers une connaissance préalable : H2 reste « ni établie ni écartée », avec les bonnes réserves. Il penche un peu vers une équipe organisée : D04, D05, D06, D02 vont dans ce sens. En sens inverse, D10 et l'omission de la séance commune du 26/01/2025 minorent des faits. Le fond tient, ce sont les formules de synthèse à ajuster.

## 7. Critère 6 : les choix de l'agent F

| Choix | Jugement | Sensibilité | Chiffres publiés qui en dépendent |
|---|---|---|---|
| **K06, programme propre** | **Défendable, enjeu faible.** Les 2 wallets ont déjà 42,2 % et 49,7 % d'allers-retours, 0 ligne signataire sur 54 et 24 | Parts de 50 à 95 % et propriétaires de 3 à 10 : mêmes 2 wallets, 444,8 SOL. À 20 propriétaires : +2, 5 157,2 SOL, `Bya5eBy9…` et `9VrLXkFP…`, à 0 % d'allers-retours, parce que `675kPX9M…`, programme Raydium AMM v4 de connaissance générale, n'y compte que 17 propriétaires. La règle reste juste jusqu'à 10 et devient fausse au-delà : le nombre de propriétaires vus ne prouve pas à lui seul qu'un programme est propre (`h11_k06.txt`) | Seulement « 105 wallets, 106 493 SOL », sinon 103 et 106 047,8. Rang 100 des acheteurs à 667,8 SOL : ces 2 wallets n'y entrent pas, et 0 ligne dans `EARLY_BUYERS.md` |
| **K04, résiduel complété** | **Défendable pour retirer, à revoir pour ajouter.** Il corrige de vrais soldes périmés : `6t2dz4jm…` 26,65 M, `8YrEVPQq…` 23,41, `99Xrt5uu…` 19,03, `AW63YBXX…` 15,44, à 0. Mais il crédite 42,68 M à un routeur sans aucun compte vu | Solde seul 739,26 M. 86 wallets corrigés : -132,45 et +49,24, soit 656,04 M. Sans les ajouts : 606,8 M, excédent 39,0 M et non 88,2 M, pour 567,82 M d'offre. Raccourci par propriétaire : 54 transferts sur 22 853, 19,86 M sur 2 175,74 M | 656,0 M, écart de 88 M, colonnes Résiduel de `TOP_TRADERS.md` et `EARLY_BUYERS.md`, 502 wallets passés en partiel. Aucune conclusion n'en dépend. **Le groupe, les 217 M et les ventes de 24 h n'en dépendent pas.** Correctif : ne créditer que si le propriétaire a un compte vu, et remplacer la phrase sur l'origine de l'écart par « origine non décomposée » |
| **K08, virements additionnés** | **Défendable.** Mon relevé sur le brut confirme : 14 738 clés dans les deux requêtes, 14 700 égales, 38 différentes. Le code additionne dans une requête et garde le maximum entre requêtes, donc pas de double compte | Somme de F 1 316 494,1 ; brut sans dédoublonnage 1 316 494,0 ; première ligne par clé 1 314 636,0. Écart au plus 0,08 point : pools 22,14 ou 22,16, soit 22,1 ou 22,2 à l'affichage | Q6, N13. Premier financeur inchangé. Hors de la fenêtre : 2 624 lignes de même signature, source et montant retirées, 1 102,9 SOL, sans effet sur un chiffre publié. Dire « maximum entre requêtes » dans `CORRECTIONS_APPLIQUEES.md` |

Limite de K06 à écrire : 13 wallets jamais signataires d'au moins 100 SOL, 10 337,6 SOL, restent classés, dont `Bya5eBy9…` rang 3 et `CnZzdTH1…` rang 9. Ce ne sont pas des allers-retours, mais pas forcément des acheteurs humains. Les seuils de 80 % et de 5 propriétaires n'apparaissent pas dans `TOP_TRADERS.md`.

## 8. Analyses hors registre

- `compter` : `etude_final` 33 comparaisons, 1 exploratoire, 0 p non résolu ; `etude_groupe` 9, 0, 0.
- Lisent les tables gelées hors registre : audit A (`a03` à `a07`, `a10`, `a22`, `a25`, `a42`, `a43`), B (`b04` à `b26`), C (`c33`, `c64`), D (`d02`, `d10`, `d11`, `d30`, `d46`, `d90`), F (`f08`, relecture de présence). Le rapport cite B et D seulement (D17).
- `etude_groupe/derived/table.csv` : aucun script d'audit trouvé qui en tire un test. `h02`, `h03`, `h08` la relisent ici en description, sans p publié.
- 7 transcriptions de `~/.claude/projects/-Users-benjamindacunha/` citent ces tables, non relues ligne à ligne. Aucun script `.py` ne les cite dans le bloc-notes de session ni dans `audits_work/`.

## 9. Non vérifié

Captures et lecture à l'œil des images. Texte des posts X, sauf ids, dates et pHash. Brut des flux de `work_G`, objet de l'autre relecture. Simulation de puissance non relancée. `viz/index.html`, `docs/SOCIAL_FINDINGS.md`, hors périmètre : la phrase fausse de D09 y figure aussi, ligne 11. Heure de Butler et de l'annonce de Biden, comme écrit au rapport.
