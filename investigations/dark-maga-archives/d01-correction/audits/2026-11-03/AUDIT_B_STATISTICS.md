# Audit B : statistiques de l'étude gelée DMAGA

Date : 03/11/2026. Commit audité : `01ae5a4`. Scripts et sorties : `audits/2026-11-03/work_B/`. Aucun appel réseau, aucune écriture hors de `work_B/`, de ce fichier et de `audits_work/B/`.

## 1. Verdict global

**INCONCLUSIVE.** Le calcul est exact et reproduit, mais le test ne peut ni confirmer ni écarter une accumulation informée : sur la distribution réelle des pairs, son taux de détection reste proche de son taux nul pour tout effet crédible.

En clair :
- **Ce qui tient.** « Aucune mesure ne passe Holm » est vrai. S, population, rangs et p sont retrouvés à l'identique par une chaîne écrite sans lire le code de l'étude.
- **Ce qui ne tient pas.** « DMAGA NON DISTINGUABLE DE SES PAIRS » dit plus que le test. Les contrôles positifs (100 % de détection) ne valent pas pour les vraies données (3,3 % et 7,1 %).
- **Amendement 001.** Il ne change pas le résultat principal et ne peut pas masquer une significativité. Recommandation : le conserver, texte corrigé, sous réserve de la décision de Benjamin.

Bilan : 0 BLOQUANT, 6 MAJEUR, 10 MINEUR, 5 INFO. Assertions : 8 PASS, 1 FAIL, 1 INCONCLUSIVE.

## 2. Ce qui a été fait

**À l'aveugle** (sceau `work_B/SEAL.txt`, 2026-11-03T09:32:00 UTC, sans lire le code, les tables ni les résultats) :
- pic S20 et S10 sur les 13 920 lignes d'`activity.jsonl` (`b01_peak.py`) ;
- parseur de swaps indépendant sur les **249 dossiers de `raw/ctrl_tx`, soit 16 172 824 transactions, volume complet, aucun tirage** (`b02_parse.py`, tests intégrés) ;
- M1 à M7, capitalisation à S−1 h, filtre 20 swaps, variantes R1 et R3, rangs et Holm (`b03_metrics.py`, `b04_blind_out.py`) ;
- 22 ambiguïtés du plan notées (`blind_ambiguites.md`).

Écart à la règle d'aveugle, à signaler : j'ai lu `scripts/py.sh` (5 lignes, le lanceur Python) et listé les noms de fichiers de `data/controls/` avant le sceau. Aucun contenu d'analyse n'a été lu. `scripts/guard.py` a été exécuté sans être lu.

**Recalculé à découvert** : comparaison token par token, Holm à la main, registre, gel, S1, R1, R2, R3, bornes de l'amendement, puissance sur données réelles, reproduction de `metrics.csv` avec le code gelé (`b10` à `b26`).

**Non fait, ou impossible hors réseau** :
- capitalisation de 731 tokens (453 `hors_bande`, 278 `reporte_budget`) : le brut n'a pas été gardé (B-14) ;
- créateurs des comparateurs : donnée absente du disque ;
- R1 et R2 sur les tokens reportés : seules des bornes sont données ;
- financeurs du test exploratoire : aucun brut (B-16) ;
- `parse_swaps` gelé relancé sur 4 tokens seulement, les autres sont couverts par mon parseur ;
- transcriptions de l'agent : non lues.

**Limite de ma chaîne aveugle, sans effet** : 3 tokens à curseur incomplet (`5jG2h6zF`, `acaDbR5Q`, `EUr4qeHV`) sont sortis chez moi sous `moins_20_swaps` ou `cap_hors_bande` à cause du brut coupé, pas d'un vrai filtre. Ils sont hors bande principale dans `selection.jsonl`. Aucun fichier `_v2` n'a été nécessaire.

## 3. Comparaison M1 à M7

### DMAGA (`b11_dmaga_table.csv`, `b10_compare.txt`)

| Mesure | Étude | B | Écart | Médiane pairs | P90 | Max pairs | Pairs ≥ DMAGA | p (étude et B) | Rang /212 | Percentile | IC 95 % du quantile |
|---|---|---|---|---|---|---|---|---|---|---|---|
| M1 | 39,867 | 39,893 | +0,066 % | 3,755 | 163,09 | 26 825 | 35 | 0,1698 | 36 | 83,4 % | 77,7 à 88,2 % |
| M2 | 9,371 | 9,376 | +0,056 % | 1,464 | 64,56 | 17 041 | 38 | 0,1840 | 39 | 82,0 % | 76,1 à 86,9 % |
| M3 | 0,6797 | 0,6800 | +0,048 % | 0,450 | 0,863 | 1 | 50 | 0,2406 | 51 | 76,3 % | 70,0 à 81,9 % |
| M4 | 0,3079 | 0,3083 | +0,147 % | 0,347 | 0,784 | 1 | 115 | 0,5472 | 116 | 45,5 % | 38,6 à 52,5 % |
| M5 | 433,80 | 433,80 | 0 | 176,33 | 1 115 | 16 291 | 55 | 0,2642 | 56 | 73,9 % | 67,5 à 79,7 % |
| M6 | 0,2046 | 0,2047 | +0,045 % | 0,075 | 0,263 | 0,474 | 32 | 0,1557 | 33 | 84,8 % | 79,3 à 89,4 % |
| M7 | 0,1379 | 0,1379 | 0 | 0,074 | 0,223 | 4,977 | 37 | 0,1792 | 38 | 82,5 % | 76,6 à 87,3 % |

### Écarts sur les comparateurs (`b10_compare.txt`, population principale, 212 tokens)

| Mesure | Écart relatif médian | P95 | Max | > 1 % | > 10 % | Spearman |
|---|---|---|---|---|---|---|
| M1 | 0,08 % | 0,47 % | 1,9 % | 1 | 0 | 0,99999 |
| M2 | 0,06 % | 0,31 % | 2,3 % | 1 | 0 | 0,99999 |
| M3 | 0,04 % | 0,27 % | 3,6 % | 1 | 0 | 0,99995 |
| M4 | 0,07 % | 0,25 % | 2,4 % | 1 | 0 | 0,99996 |
| M5 | 0 | 0,40 % | 13,3 % | 8 | 1 | 0,99999 |
| M6 | 0,31 % | 4,2 % | 102 % | 71 | 4 | 0,99950 |
| M7 | 0 | 0,85 % | 25,8 % | 5 | 2 | 0,99921 |

### Résultat de la comparaison
- S20 et S10 : identiques sur 13 920 tokens sur 13 920.
- Population principale : 212 tokens communs sur 212.
- **Ensemble des pairs au-dessus de DMAGA : différence symétrique 0 sur chacune des 7 mesures** (`b13_power.txt`).
- Les 28 rangs (principal, R1, R2, R3) sont identiques (`b26_variants.txt`).
- Capitalisation : écart médian 0,10 %, max 5,6 %. J'ai pris la minute de S−1 h, l'étude celle du swap. Aucun effet sur la bande.

### Cause des écarts non négligeables (`b17_diff_cause.txt`, `b24_divers.txt`)
- **SOL.** L'étude répartit tout le SOL du vault entre les bénéficiaires retenus. Moi, part × SOL, sans renormaliser. Cela fait environ 0,05 à 0,1 % sur les sommes, et cela explique M1 à M4.
- **M7 de `Ew6WHMMF` (0,059 contre 0,074).** Deux achats quasi égaux, 10,53 et 10,44 SOL : la répartition change lequel est le plus gros. M7 est sensible à cet ordre.
- **M6 de `9ny2CD5P` (0,390 contre 0,241).** Le `qty` de l'étude compte tout le gain de l'owner, y compris hors du vault : 863,8 M jetons chez elle, 70,7 M chez moi (B-13).
- **M5 de `HVTX1Kcd` (17 acheteurs contre 16).** Une ligne `CpoD6tWA` existe seulement chez l'étude, à cause de la base du seuil de 5 % (B-13).

## 4. Constats

### B-01, MAJEUR : la puissance réelle est proche du taux nul
- **Preuve** (`b13_power.py`, `b13_scenarios.csv`) : chaque token est pris tour à tour comme cible contre les 211 autres, avec une accumulation injectée. Taux nul empirique : 5/212 = 2,4 %. 1× la réserve en un wallet sur 3 h : 2,8 %. 2× la réserve : 3,3 %. 25 wallets, 2× la réserve : 3,3 %. Seule la synchronisation dans un slot atteint 10 à 11 %.
- **DMAGA** : 855,8 SOL de plus en un wallet sur 3 h, soit 3,5 fois les 246,7 SOL observés, ne font pas basculer le verdict. Il faut un achat unique de 2 130 SOL environ, 5 fois la réserve.
- **Rapport de vraisemblance d'un résultat non significatif** (`b28_verifs.txt`) : 0,995 à 1× la réserve, 0,990 à 2×, 0,908 pour le scénario synchronisé. Le verdict ne déplace presque pas la croyance.
- **Impact** : C08, C09, C49, et l'usage du test dans la ligne H2 du rapport et dans C39.
- **Correctif** : écrire la table de puissance réelle à côté du verdict. Toute refonte du test passe par un amendement décidé par Benjamin.

### B-02, MAJEUR : les contrôles positifs sont trop faciles
- **Monde synthétique sans rapport avec le réel** (`b19_controls.txt`) :

| Mesure | Médiane synthétique | Médiane réelle | Max / médiane synthétique | Max / médiane réelle |
|---|---|---|---|---|
| M1 | 0,85 | 3,75 | 12 | 7 145 |
| M2 | 0,80 | 1,46 | 3,1 | 11 643 |
| M3 | 0,01 | 0,45 | 32 | 2,2 |
| M5 | 0 | 176 | sans objet | 92 |
| M6 | 0,63 | 0,075 | 1,2 | 6,3 |

- Le fond synthétique n'a presque pas de nouveaux wallets ni d'achats dans le même slot. Toute injection sort donc du lot : la cible « moyen » dépasse déjà le **maximum** du fond sur M1 (× 1,43), M3 (× 2,0) et M5 (× 2,1).
- **Sur données réelles, les mêmes effets** : « moyen » (6 wallets, environ 64 SOL) 3,3 %, « fort » (18 wallets, environ 804 SOL) 7,1 % (`b13_scenarios.csv`). Le rapport dit 100 %.
- **Nul à 5 %** : 2/40, IC 95 % de 0,6 à 16,9 %. Je retrouve 2/40. Avec plus de graines : 6/150 à k = 150, 8/150 à k = 211. Valeurs attendues si les mesures sont indépendantes : 4,5 % et 3,3 %. Sur vraies données : 2,4 %. Le 5 % n'est pas une calibration, c'est un petit échantillon.
- Le contrôle de bout en bout ne teste que nul, fort (15 wallets à environ 40 SOL) et rupture.
- **Impact** : C49.
- **Correctif** : remplacer « effets détectés » par « contrôle de la plomberie seulement », et citer 3,3 % et 7,1 %.

### B-03, MAJEUR : `INCONCLUSIF (puissance)` teste la possibilité, pas la puissance
- **Preuve** : le plan exige k ≥ 139. C'est le k pour lequel un p de 1/(k+1) peut passer 0,05/7, pas celui qui donne une puissance. À k = 211, la première marche exige c = 0 (`b06_power_analytic.txt`). Puissance sur une mesure : 12 % si le quantile vrai est 99 %, 35 % à 99,5 %, 81 % à 99,9 %.
- **Conséquence** : une étude presque sans puissance sort quand même un verdict affirmatif. Le texte `INCONCLUSIF (puissance)` ne pouvait pas se déclencher ici.
- **Impact** : C08, C47.
- **Correctif** : proposé à Benjamin pour une prochaine étude, ajouter un seuil de puissance sur données réelles. Ne pas réécrire ce plan.

### B-04, MAJEUR : M3 et M4 ne peuvent pas ouvrir Holm
- **Preuve** (`b25_seuils.txt`) : 5 pairs ont M3 = 1 et 3 pairs ont M4 = 1, à cause d'un plafond atteint. p minimal de DMAGA : 0,0283 sur M3, 0,0189 sur M4, contre un seuil de 0,00714. Multiplier les cotes par 10 000 ne change rien (`b13_facteurs.csv`).
- **Conséquences** : on paie Holm pour 7 tests, mais 5 seulement peuvent ouvrir. Niveau réel : 5/212 = 2,4 %, pas 5 %. Le contrôle « baleine » annonce M4 : 40/40, alors que M4 ne peut pas ouvrir sur les vraies données. M4 suit surtout le nombre d'acheteurs (Spearman −0,80).
- **Impact** : C47, C49.
- **Correctif** : à écrire dans les limites.

### B-05, MAJEUR : le libellé et plusieurs phrases disent plus que le test
- **Preuve** (`b11_tests.txt`) : DMAGA est au-dessus de la médiane des pairs sur 6 mesures sur 7, et au-dessus du P75 sur 5 sur 7. Aucun pair n'est ≥ DMAGA sur les 7, et 7 pairs le sont sur 6. EXPLORATOIRE : centile moyen 75,6 %, 8 pairs sur 211 au-dessus, p = 0,0425 sans correction (voir B-20). Ce n'est pas une anomalie établie, mais ce n'est pas non plus « comme ses pairs ».
- **Passages concernés** : `docs/CASE_REPORT.md`, point 3 de l'essentiel, le test gelé placé sous « Aucune preuve d'achat informé » ; ligne H2, « Test gelé non significatif » listé en appui ; `reports/COORDINATION.md`, « Plan gelé [...] avant tout calcul », alors que le plan liste ce qui avait été vu de DMAGA.
- **Impact** : C08, C09 et C39 (C39 relève de l'auditeur C).
- **Correctif** : garder le texte gelé, entre guillemets, et ajouter la phrase de la section 6.

### B-06, MAJEUR : ce que les mesures ne voient pas, chiffré sur DMAGA
- **Courbe de lancement** (`b21_exclus.txt`) : 1 193,18 M jetons achetés par 106 wallets. 76 de ces wallets, soit 845,72 M, sont hors de M6, qui ne regarde que les précoces sur Raydium.
- **Transferts** : 114,96 M jetons reçus par 35 wallets sur les 24 h avant S, contre 182,96 M achetés par swap (`b20_venues.txt`). Invisibles par construction.
- **Fenêtre de M1** : elle commence à 16:00, 2,5 min avant le post de Winig. Le pic d'achats de 13:00 à 16:00 (400,5 SOL sur [Winig−3 h, Winig)) est hors du numérateur de M1, mais dans M2.
- **Cause** : 14:00 fait 269 signatures, soit 38 fois la médiane, mais reste sous le plancher de 500. S tombe donc à 19:00 (`b14_selection.txt`).
- **Heure de S** : les 2 756 SOL achetés de 19:00 à 20:00 (parseur du test, `b16_s1.txt`) n'entrent dans aucune mesure, c'est voulu.
- **Sensibilité EXPLORATOIRE** (`b16_s1.txt`) : ancré sur Winig, M1 = 66,1, p = 0,1415. Les deux côtés décalés de 3 h : p = 0,099 (`b13_power.txt`). Le verdict ne change pas.
- **Autres venues** : pour DMAGA avant S, 6 398,8 SOL sur Raydium v4, 1,02 SOL sur `Eqe7fgb5`, 128,39 SOL sur la courbe. Angle mort faible sur DMAGA. Non mesuré sur les pairs.
- **Impact** : C09. Le rapport ne parle que du détenteur existant.
- **Correctif** : ajouter le tableau de la section 5.4 aux limites.

### B-07, MINEUR : le test S1 sur le passé du token n'a pas de valeur discriminante
- **Preuve** (`b24_divers.txt`) : 61 pairs sur 211 (28,9 %) ont [S−3 h, S) au-dessus de leurs 24 fenêtres passées, et 79 (37,4 %) ont au plus une fenêtre au-dessus. DMAGA à S en a une. « Inhabituel pour DMAGA » est vrai, mais c'est fréquent chez les tokens qui explosent.
- p = 0,036 est le **minimum possible** (1/28). Pour l'avatar, la seule fenêtre au-dessus est [13:23, 16:23) avec 386,9 SOL, soit le même épisode que Winig. Les 4 tests ne sont donc pas indépendants.
- **Impact** : C07, C45 (les chiffres sont justes).
- **Correctif** : écrire ces pourcentages à côté de p.

### B-08, MINEUR : le texte de l'amendement 001 est inexact
- « L'ordre d'activité [...] sans lien avec les mesures » : l'ordre est en fait **chronologique** (Spearman position / création = +1,000 sur 310 tokens, `b14_selection.txt`). Les 29 pairs ajoutés à R2 sont tous créés du 15 au 23 juin, et leur capitalisation va de 10 324 $ à 94 498 $. Aucun au-dessus de 10 M$.
- R2 n'est donc pas un test de la bande large : 211 de ses 240 pairs sont déjà dans le principal.
- Ajouts contre principal : M1 17,3 contre 3,75, M3 0,76 contre 0,45, M6 0,047 contre 0,075. Ces écarts tiennent peut-être à la taille plus qu'à la date.
- Décision prise sans Benjamin, signalée dans l'amendement 002.
- **Impact** : section 7. **Correctif** : corriger le texte, renommer R2 « partielle ».

### B-09, MINEUR : les exclusions de tronqués sont liées à l'activité
- **Preuve** (`b08_trunc.txt`) : 135 `tronque_sans_pic`, dont **127 dont le listing n'atteint jamais 96 h** (couverture médiane 1,63 j, max horaire médian 44 960). Leur pic tardif n'a pas pu être testé.
- Sens probable : les tronqués retenus (63 sur 211) ont M1 et M2 plus bas (2,05 contre 4,58 et 1,12 contre 1,83, `b14_selection.txt`). Les ajouter rapprocherait plutôt DMAGA du haut.
- **Borne** : à c = 32, il faudrait k ≥ 4 619 pour passer Holm. L'univers complet n'a que 954 pics. **Aucune valeur des exclus ne peut changer le verdict.**
- Écart au plan : le compteur `tronque_sans_S20` (5 tokens, tous `reporte_budget`) est absent de `selection_counts.json`.
- **Correctif** : publier ces 5 et la phrase sur les 127.

### B-10, MINEUR : les queues sont fixées par des tokens quasi morts
- **Preuve** (`b25_seuils.txt`, `b13_power.txt`) : le plus haut M1 a un dénominateur de 0 et le plus haut M2 aussi. Plancher actif : 25 pairs sur M1, 15 sur M2 ; dénominateur nul : 21 et 13. Le plus haut M6 n'a que 2 acheteurs sur 24 h. Le plus haut M5 a 55 acheteurs pour 92 SOL.
- M5 vaut 176 fois le hasard chez le pair médian, et M5 ≥ 1 chez 171 pairs sur 211 : c'est une structure de marché, pas une coordination isolée.
- EXPLORATOIRE : sans plancher, avec des acheteurs ou une capitalisation comparables, le plus petit p est 0,085 (`b13_power.txt`). Pas d'effet sur le verdict.
- **Correctif** : à dire dans les limites.

### B-11, MINEUR : S à l'heure pleine, rampe et rôle de R3
- **Preuve** (`b13_power.txt`, `tests.json`) : le M1 médian des pairs passe de 3,76 à S, à 2,01 à S−1 h, 1,87 à S−2 h, 1,56 à S−3 h, 1,05 à S−6 h. Près de la moitié du run-up médian tombe dans la dernière heure : M1 mesure en partie le début du pic.
- Le plan dit que R3 « borne » le spam. C'est faux : S−1 h reste collé à un S déclenché par du spam.
- **Spam mesuré** (`b25_seuils.txt`) : 11 pairs sur 211 ont moins de 20 % de transactions réussies touchant le vault dans l'heure S. DMAGA : 79,7 %. EXPLORATOIRE sans ces 11 : p inchangés à 0,02 près.
- **Impact** : C48. **Correctif** : retirer « R3 le borne » des lectures futures, citer les 11.

### B-12, MINEUR : bande de capitalisation lue après le run-up
- **Preuve** (`b13_power.txt`, `b14_selection.txt`) : DMAGA 1,29 M$ à S−1 h, 514 k$ à S−24 h (× 2,51, médiane des pairs × 1,17), 380 k$ à S−96 h. Pairs : médiane 270 k$, quartiles 152 k$ à 551 k$. La bande est centrée sur DMAGA mais pas sur la population : 62 pairs seulement sont à un facteur 3 de lui.
- EXPLORATOIRE, à un facteur 3 à S−1 h ou à S−96 h : aucun p sous 0,09.
- **Correctif** : à dire dans les limites.

### B-13, MINEUR : deux imprécisions du parseur de l'étude
- `qty` n'est pas borné par le flux du vault. 14 374 lignes sur 11 294 554 communes (0,13 %) dépassent de plus de 1 %. Effet sur M6 : 71 tokens à plus de 1 %, 4 à plus de 10 %. Le plan dit que seul Raydium v4 compte.
- Le seuil de 5 % porte sur la somme des owners d'un côté, pas sur le swap. Une ligne de frais peut alors recevoir tout le SOL quand le reste part vers une réserve. 419 lignes chez l'étude seule et 22 chez moi seul sur 11,29 M, 88,8 SOL sur 5,18 M de SOL (max 3,6 SOL, souvent `CpoD6tWA`).
- **Impact** : aucun sur les rangs de DMAGA (différence symétrique 0). **Correctif** : à noter. Toute correction passe par un amendement.

### B-14, MINEUR : la sélection n'est pas reproductible depuis le brut
- `fdv_at` lit 200 transactions sans les garder. Pour 731 tokens, la capitalisation n'existe que dans `selection.jsonl`, qui n'est pas dans le verrou (dernière écriture 03:24:24 UTC). Sur les 245 tokens vérifiables, tout concorde.
- **Borne** : retirer ou ajouter des pairs reste sans effet tant que c = 32 sur M6 (voir B-09).
- **Correctif** : archiver ces réponses à la prochaine collecte, et mettre l'empreinte de `selection.jsonl` au verrou.

### B-15, MINEUR : C47 est imprécise
« Une mesure ne passe Holm que si DMAGA dépasse tous les comparateurs » vaut pour la première marche. Les c maximaux sont 0, 0, 1, 1, 2, 4, 9 selon le rang de Holm (`b06_power_analytic.txt`). Formulation juste : « le verdict ne bascule que si DMAGA dépasse tous les comparateurs sur au moins une mesure ».

### B-16, MINEUR : le test du financeur commun n'est pas recalculable
- Arithmétique vérifiée : 3/41 = 0,0732, k = 40, médiane 0, 7 pairs non nuls sur 40, 2 ≥ 0,08 (`b24_divers.txt`).
- La mesure ne se recalcule pas : `getTransfersByAddress` n'a pas de brut sur le disque.
- « Service » dépend de l'activité **récente** de l'adresse au moment de l'appel, en 2026, pas en 2024. p minimal 1/41.
- **Impact** : C46. **Correctif** : à l'écrire, et archiver les réponses.

### B-17, INFO : l'exactitude du calcul est confirmée
- `metrics.csv` reproduit avec `metrics.compute` gelé sur les swaps gelés : 877 lignes, 6 134 valeurs, écart 0 (`b23_repro.txt`).
- `parse_swaps` gelé sur le brut de 4 tokens : parquets identiques.
- `tests.json` recalculé à la main : identique, Holm compris (`b11_tests.txt`).
- Verrou : 17 empreintes conformes sur 17. Registre : 25 lignes, chaîne continue, témoin externe conforme (`n` = 25, tête `b5c2f087`, `b15_gel.txt`).
- Mes comptes : 12 267 761 swaps au sens des vaults, égaux à 11 878 474 + 389 287 de l'étude.
- SOL/USD : 263 520 minutes présentes sur 263 520. WSOL : 0 rupture sur les 245 tokens complets.
- Migrations : 13 920 `initialize2` sur 101 702 transactions brutes (`b24_divers.txt`).

### B-18, INFO : indépendance des comparateurs (`b11_tests.txt`, `b18_buyers.txt`)
- 84 jours de pic, 12 tokens au plus par jour. 7 pairs le même jour que DMAGA, 1 à la même heure.
- ICC par jour de pic : de −0,16 à 0,15. k effectif de 172 à 211. La première marche reste à c = 0.
- Wallets vus sur au moins 2 tokens : 29,6 % du SOL chez le pair médian, 41,6 % chez DMAGA. 146 wallets sur 20 tokens ou plus.
- Corrélations de Spearman : jusqu'à 0,62 (M1, M2). Nombre effectif de tests : 6 à 6,5 sur 7.
- Créateurs : **non vérifié**, donnée absente.

### B-19, INFO : les ambiguïtés du plan n'ont pas changé le verdict
22 notées à l'aveugle (`blind_ambiguites.md`). L'étude et moi avons fait le même choix sur presque toutes. Écarts : minute USD (A05), base du seuil de 5 % (A08), répartition du SOL (A09). Lectures possibles d'une même phrase : M6 par wallet, p = 0,429 au lieu de 0,156 ; M7 au ratio maximal, p = 0,123 au lieu de 0,179 ; M3 au premier achat, p = 0,316 au lieu de 0,241 (`b25_seuils.txt`). Aucune n'approche le seuil.

### B-20, INFO : comparaisons exploratoires de cet audit
121 comparaisons, jamais substituées au verdict : 5 combinaisons, 63 sous-groupes, 21 décalages, 1 ratio de capitalisation, 14 ancrages sur Winig, 7 lignes remises, 7 hors spam, 3 variantes. Plus petit p : 0,0425. Bonferroni à 121 : 0,00041. Aucune ne passe. Elles ne sont pas au registre, car je n'y écris pas : à ajouter si ce rapport est repris.

Lignes remises (`b22_reinstate.txt`) : `5V97uEb4` et `AD65fgYt` ont un solde net de 0 jeton sur la période. Leur exclusion est donc défendable. Remises chez DMAGA seul, M7 passerait à 0,292, p = 0,0755.

### B-21, INFO : petits restes de comptabilité
4 dossiers `ctrl_tx` incomplets (320 000 transactions, statut `reporte_budget`) ne sont pas mentionnés dans la comptabilité. 34 ruptures sur le vault jeton dans 30 tokens : non exclues, le plan ne regarde que le WSOL.

## 5. Puissance

### 5.1 Calcul exact, k = 211 (`b06_power_analytic.txt`)
p minimal 1/212 = 0,00472. Seuil de la première marche 0,00714. 2/212 = 0,00943 ne passe pas. Une mesure doit donc être strictement au-dessus de tous les pairs.

| Quantile vrai de la cible | 1 mesure | 3 mesures indép. | 7 mesures indép. |
|---|---|---|---|
| 95 % | 0,00 % | 0,01 % | 0,01 % |
| 97,5 % | 0,5 % | 1,4 % | 3,3 % |
| 99 % | 12,0 % | 31,8 % | 59,1 % |
| 99,5 % | 34,7 % | 72,2 % | 94,9 % |
| 99,9 % | 81,0 % | 99,3 % | 100 % |

Puissance de 80 % sur une mesure : quantile 99,894 %, soit z = 3,07.

### 5.2 Seuils de bascule de DMAGA (`b25_seuils.txt`)

| Mesure | À dépasser | Facteur | En unités du token |
|---|---|---|---|
| M1 | 26 825 | × 673 | 165 872 SOL sur 3 h, observé 246,7 |
| M2 | 17 041 | × 1 819 | 1 735 592 SOL sur 24 h, observé 954,9 |
| M3 | impossible | sans objet | 5 pairs à 1,0, p minimal 0,028 |
| M4 | impossible | sans objet | 3 pairs à 1,0, p minimal 0,019 |
| M5 | 16 291 | × 37,6 | 3 117 paires dans un slot, observé 83 |
| M6 | 0,4744 | × 2,32 (cotes × 3,51) | 943,6 M jetons de plus détenus, 94,4 % de l'offre |
| M7 | 4,977 | × 36,1 | 1 achat de 2 130 SOL, observé 51,6 |

### 5.3 Sur la distribution réelle, chaque token cible à son tour (`b13_facteurs.csv`)
Une mesure multipliée par le facteur (sur les cotes pour M3, M4, M6). Taux de verdict « inhabituel », taux nul 2,4 % :

| Facteur | M1 | M2 | M3 | M4 | M5 | M6 | M7 | Toutes |
|---|---|---|---|---|---|---|---|---|
| 2 | 2,4 | 3,3 | 2,4 | 2,4 | 2,4 | 9,9 | 2,8 | 11,3 |
| 10 | 4,7 | 6,6 | 2,4 | 2,4 | 10,4 | 49,5 | 5,7 | 55,7 |
| 100 | 9,4 | 9,4 | 2,4 | 2,4 | 51,4 | 97,6 | 78,3 | 100 |
| 1 000 | 21,2 | 17,5 | 2,4 | 2,4 | 81,1 | 99,1 | 99,1 | 100 |

Scénarios injectés (`b13_scenarios.csv`), R = réserve SOL (428 SOL sur 3 h pour DMAGA) :

| Scénario | Détection | p minimal médian | Sur DMAGA |
|---|---|---|---|
| Nul | 2,4 % | sans objet | ne passe pas |
| 0,25 R, 1 wallet, 3 h | 2,8 % | 0,085 | ne passe pas |
| 1 R, 1 wallet, 3 h | 2,8 % | 0,024 | ne passe pas |
| 2 R, 1 wallet, 3 h | 3,3 % | 0,014 | ne passe pas |
| 5 R, 1 wallet, 3 h | 100 % | 0,005 | M7 seule, mécanique car 5 > 4,977 |
| 2 R, 25 wallets, 3 h | 3,3 % | 0,099 | ne passe pas |
| 2 R, 25 wallets, 3 h, moitié dans un slot | 11,3 % | 0,068 | ne passe pas |
| 2 R, 5 wallets, 24 h | 2,4 % | 0,101 | ne passe pas |
| Contrôle « moyen » de l'étude | 3,3 % | 0,118 | ne passe pas |
| Contrôle « fort » de l'étude | 7,1 % | 0,061 | ne passe pas |

Limite de cette simulation : calcul incrémental, impact de prix ignoré, réserve lue avant l'injection. Il est vérifié identique à `b03` sur l'effet nul pour les 212 tokens.

### 5.4 Ce que voit chaque profil

| Profil | Ce qui bouge | Effet sur DMAGA |
|---|---|---|
| Détenteur passif, courbe | Rien | Invisible : 845,72 M jetons hors M6 |
| Détenteur passif, 1res 24 h Raydium | M6 seule | 30 % de l'offre en plus : M6 = 0,316, p = 0,0755, ne passe pas |
| Initié 1 wallet | M1, M2, M3, M4, M7 | M7 p = 0,024 à 1 R, ne passe pas |
| Initié multi-wallet | M1, M2, M3 montent, M4 baisse | 2 R sur 25 wallets : M1 p = 0,104, M4 p = 0,844 |
| Autre venue que Raydium v4 | Rien | Faible sur DMAGA avant S : 1,02 SOL |
| Achat dans l'heure de S | Rien, par construction | 2 756 SOL non vus |
| Transferts entre wallets | Rien | 114,96 M jetons sur 24 h, non vus |

## 6. Interprétation

**Ce qu'on peut dire**, parmi ces 211 pics tardifs :
- aucune mesure ne passe Holm ;
- DMAGA n'est au-dessus de tous les pairs sur aucune mesure ;
- à 95 %, son quantile vrai reste sous 88,2 % (M1), 86,9 % (M2), 81,9 % (M3), 52,5 % (M4), 79,7 % (M5), 89,4 % (M6), 87,3 % (M7), si les pairs sont échangeables. Avec k effectif de 172 à 211, ces bornes s'élargissent un peu.

**Ce qu'on ne peut pas exclure** :
- qu'il soit dans le P80 à P89 de ses pairs ;
- un effet réel de grande taille sur ces mesures : 2 R n'est pas détecté ;
- un détenteur passif, un initié passé par la courbe, des transferts, des achats dans l'heure de S ;
- que les pairs contiennent eux-mêmes des initiés, ce qui réduit le contraste. Aucun groupe sans pic n'a été collecté, donc l'effet de « a explosé » sur chaque mesure n'est pas estimable. Seul indice : le M1 médian retombe à 1,05 à S−6 h et le M2 médian à 0,87.

**« Non distinguable » n'est pas « équivalent ».** Aucune marge d'équivalence n'a été fixée, aucun test d'équivalence n'a été fait.

**Texte proposé** à côté du verdict gelé : « Verdict du plan : "DMAGA NON DISTINGUABLE DE SES PAIRS". Cela signifie qu'aucune mesure ne dépasse tous les 211 pairs. DMAGA est au 74e à 85e percentile sur 6 mesures sur 7. Ce test détecte presque uniquement des écarts extrêmes : sur les vraies données, une accumulation de deux fois la réserve du pool n'est détectée qu'environ 3 fois sur 100, comme sans effet. Il n'apporte donc pas d'élément contre une connaissance préalable, et n'en apporte pas pour. »

## 7. Amendements 001 et 002

### Chiffres (`b14_selection.txt`, `b14_r_bornes.csv`, `b26_variants.txt`)

| Variante | k réel | k maximal sans 001 | Part déjà dans le principal | Meilleur p | Passe Holm |
|---|---|---|---|---|---|
| Principal | 211 | 211 | 100 % | 0,1557 (M6) | aucune |
| R1 | 212 | 231 | 209/212 | 0,1596 (M6) | aucune |
| R2 | 240 | 498 | 211/240 | 0,1411 (M6) | aucune |
| R3 | 210 | 210 | non concerné par 001 | 0,1422 (M1) | aucune |

**Collectés contre reportés, hors bande principale des deux côtés (32 contre 278)** :
- date de création 18/06 contre 22/07, p = 2e−20 ;
- S20 09/07 contre 06/08, p = 4e−11 ;
- activité totale 13 280 contre 27 150 signatures, p = 0,03 ;
- capitalisation 48,9 k$ contre 34,9 k$, p = 0,17 ;
- signatures à S 802 contre 995, p = 0,18 ;
- médiane 72 h 2 contre 1, p = 0,63.

**L'ordre de collecte n'est donc pas neutre en date.** Il l'est à peu près en taille et en forme de pic. Lien faible entre date et mesures : Spearman de −0,16 à +0,06 sur R2.

La comparaison 245 contre 278 n'a pas de sens directe : les 213 principaux sont choisis dans la bande, d'où 233 k$ contre 35 k$.

### Réponses
1. **L'amendement modifie-t-il le résultat principal ? Non.** Les 213 tokens S20 dans la bande sont tous collectés (`b10_compare.txt`). Population, S et rangs sont identiques dans ma chaîne, où l'amendement ne joue aucun rôle.
2. **Réduit-il seulement la robustesse ? Oui.** R2 ne couvre que 29 des 287 tokens hors bande principale (10,1 %), tous créés en juin. R1 perd 19 tokens. Le percentile de M6 sous R2 pourrait aller de 41,6 % à 93,4 %.
3. **Peut-il masquer une faiblesse importante ? Pas sur le verdict.** Même si tous les reportés sont sous DMAGA, le meilleur p de R2 reste 0,068, et aucune des 14 lignes ne passe sous 0,05. À c constant sur M6 (c = 33 sous R2), il faudrait k ≥ 4 759. Si les 258 reportés ressemblent aux 29 ajoutés : M6 p = 0,086, autres mesures de 0,215 à 0,589. DMAGA semblerait alors moins inhabituel, sauf sur M6. Ce que 001 retire : la lecture sur les petites capitalisations, et le côté 10 à 50 M$ (0 collecté, 3 reportés).

### `resultats_vus: non` : crédible, non prouvé (`b15_gel.txt`)
- Pour : `001` date de 02:46:05 UTC, la collecte en était à environ 150 sur 523, `metrics.csv` date de 03:25:19, première ligne réelle du registre 03:25:36.
- Limites : `001` n'entre au dépôt qu'à 03:46:09, **dans le même commit que les résultats**. Le verrou ne contient pas les amendements. Une date de fichier se modifie.
- Le plan lui-même reconnaît que les données de DMAGA avaient été vues. Aucune trace de mesure antérieure trouvée. Transcriptions non lues.
- `002` ne change aucune méthode. Sa recette de reprise ajouterait des lignes au registre.

### Recommandation
**Conserver 001 pour le verdict**, sous réserve de la décision de Benjamin. Conditions : corriger « ordre d'activité, sans lien avec les mesures » en « ordre chronologique, lien non testé au moment de la décision » ; appeler R1 et R2 « partielles » dans les rapports. Si une vraie lecture de robustesse est voulue, tirer au hasard, à graine notée et par tranche de capitalisation, dans les 258 tokens reportés, plutôt que de continuer dans l'ordre chronologique. Ce serait un nouvel amendement.

## 8. Assertions

Détail : `work_B/claims_B.csv`.

| Id | Verdict | En bref |
|---|---|---|
| C07 | PASS | 229,28 SOL, médiane 6,18, p = 2/29. B : 229,14 |
| C08 | PASS | k = 211, meilleur p 0,1557, 33e sur 212 |
| C09 | PASS | Vrai, et même trop modeste : voir B-01, B-06 |
| C43 | PASS | 13 920 du 15/06 00:02:43 au 31/08 23:49:56 ; 84 jours |
| C44 | PASS | 21 valeurs conformes, B à moins de 0,15 % sur DMAGA |
| C45 | PASS | 401,52 SOL, 6,06, p = 1/28, 27 fenêtres |
| C46 | INCONCLUSIVE | Arithmétique juste, mesure non recalculable |
| C47 | PASS | Vrai à la première marche (B-15), 33 et 0,00152 justes |
| C48 | PASS | Plan, code et données concordent |
| C49 | FAIL | Gel vrai. Chiffres des contrôles vrais, leur portée non : 100 % contre 3,3 et 7,1 % sur vraies données |

## 9. Sceau

`work_B/SEAL.txt` couvre `blind_metrics.csv`, `blind_selection.csv`, `b04_ranks_blind.csv`, `b03_r1.csv`, `b03_r3.csv`, `b02_stats.jsonl`, `blind_ambiguites.md` et les 4 scripts. Ces fichiers n'ont pas été touchés après le sceau. Les parquets par token sont dans `audits_work/B/tok/`.
