# Frontières des flux, enquête Dark MAGA

> **Erratum du 03/11.** Ce rapport a été relu sur le brut par un relecteur adverse : aucun constat central ne tombe, mais plusieurs chiffres et phrases sont faux ou trop forts (G3, G6, G8, `9PrmF8`, ponts). `audits/2026-11-03/work_I/REFUTATION.md` fait foi. Le rapport d'origine n'est pas réécrit.

Agent G, 03/11/2026. Jeton `7D7BRcBY`. Branche `audit-2026-11-03`, commit de référence des audits `01ae5a4`. Personne n'est accusé. Aucune identité civile n'est présumée. Un wallet cité n'est mis en cause en rien.

Niveaux : A vérifié directement, B fortement corroboré, C indice, D non vérifié. Chaque lien sépare trois questions : une transaction, une coordination, un contrôle commun. Un compte de dépôt ou un pont arrête la trace : aucune continuité n'est supposée au-delà.

Les préfixes renvoient à l'annexe, écrite par script, qui donne les adresses et les signatures complètes. Les SOL équivalents convertissent les stables au cours journalier Binance SOLUSDT de `raw/solusd` (`sol_daily.csv`). Budget : 2 020 crédits sur 5 000, 202 pages, aucun refus « max usage » vu, seulement des réponses 429 relancées.

## 0. Ce qui est nouveau

| N° | Constat | Transaction | Coordination | Contrôle commun | Sources |
|---|---|---|---|---|---|
| G1 | Second compte de dépôt du périmètre créateur : `Caw4Rrwk` reçoit 590 933,95 USDC et 35,63 SOL de 55 expéditeurs, dont 27 des 48 de `9W9b3zgH`, et balaie vers Coinbase | A | B | B pour un même opérateur ou compte, C pour un même bénéficiaire | `g22_all.txt`, `g30.txt` |
| G2 | Sur 2 201 destinataires de retraits Coinbase en 2 h, 14 versent à l'un de ces deux dépôts, tous dans les 507 s de la série. `Fp6kgqHU`, écrit « ne revient pas », verse 155,12 SOL éq. à `Caw4Rrwk` | A | B | B | `g66.txt` |
| G3 | Le périmètre créateur vend surtout par ordres DCA : 47 ordres, 113,37 M de jetons, 1 292,4 SOL éq. Cinq ordres de la série sont ouverts de 19:53:13 à 22:16:49 le 21/07/2024. Salve de 116 377,38 USDC vers `Caw4Rrwk` le 22/07 de 05:22:29 à 05:24:16 | A | B | B sur ces wallets | `g52.txt`, `g30.txt` |
| G4 | Sorties par pont : 76 ordres inter-chaînes, 1 018 687,18 USD, 21,3 % des SOL éq. de la table. `C73Yv9iH` envoie 496 371,59 USD vers `0x2d86499a` dès 22:53:42 le 21/07/2024 | A pour l'ordre | B | Non établi | `g43.txt`, `g43_orders.csv` |
| G5 | `Ei5yGz8d`, `Gcyg2jeL`, `HGBiExZR` désignent le même receveur `0xb947bf7f` sur Ethereum : 263 573,15 USD en 9 min 36 s, le 22/07/2024 | A pour l'ordre | B | B pour un même opérateur ou compte | `g43_orders.csv` |
| G6 | Chaque grappe a sa sortie : `9W9b3zgH` et `Caw4Rrwk` pour le périmètre créateur, `AQVgyg8P` pour le bloc `G41vRrsH`, `By6Dao4Q` pour le bloc `74qFhHyp`, `H9Xezqfd` pour `9PrmF8sf`. Recouvrement entre eux : 2 wallets réels, 8 SOL chacun | A | B dans chaque grappe | B dans chaque grappe, non établi entre elles | `g30_overlap.csv` |
| G7 | Jonction indirecte de `GXZvXsD6` : `ERMtiLod` et `GoPCTrS3`, de la série, donnent 1,5 M et 1 M de jetons à `HW5MqvM1` et `HKzkNSH2`, qui revendent et versent aux dépôts de `GXZvXsD6` | A | C | C | `g48.txt`, `g49.txt` |
| G8 | Piste A-16 tranchée sur le mécanisme : 1 913 blocs sur 1 913 ont la forme d'un sandwich. Trésor unique visible, aucun lien avec les périmètres | A pour la forme | Sans objet | B pour un trésor unique | `g53.txt`, `g42.txt`, `g47.txt` |

## 1. Créateur et périmètre créateur

Périmètre P1, défini avant calcul : créateur, 15 wallets de la série, 48 expéditeurs de `9W9b3zgH`, moins les 4 wallets de la salve du 23/07 traités avec les 33. Soit 46 wallets, dont 2 des 33 (`5QhJJcFZ`, `7FGoCB63`). Détail par wallet : `g40_p1_wallets.csv`.

**Créateur `8YLEuUtZ` (A, historique complet de 946 tx).**
- Entrées de SOL : 0,5 de Coinbase 3 le 14/07/2024 à 01:32:23, 0,03 de `5QhJJcFZ` le 06/07/2025.
- Jetons : 7,106 M achetés au mint pour 0,2 SOL, vendus par DCA le 06/07/2025 pour 4 598,77 USDC. Le 13/07/2025, ordre d'achat de 4 500 USDC, 7,398 M reçus, puis tous transférés à `BuHUkjUy`.
- Sorties : 0,593 SOL vers `9W9b3zgH`, 0,03 SOL vers `AYtWa3rL`, 98,77 USDC vers `7rMagzrQ`. Ces deux derniers versent eux-mêmes à `Caw4Rrwk`.
- Lecture : le créateur encaisse presque rien en propre. Ses restes s'arrêtent à une frontière de dépôt, directement ou à un saut.

**Série de 15 (A pour les flux).** 13 versent à `9W9b3zgH` (312,2 SOL éq.), 10 à `Caw4Rrwk` (873,6 SOL éq.), 9 aux deux. Seul `A52fNskQ` ne verse à aucun. Le dépôt en USDC pèse donc 2,8 fois celui en SOL pour ces wallets. Exemple lu ligne à ligne : `HqwpWyvb` reçoit 1 SOL de Coinbase 2, achète 1,32 M pour 0,95 SOL le 14/07, ouvre un DCA de tout son stock le 21/07 à 21:38:25, reçoit de l'USDC par tranches toutes les 2 à 4 min, puis verse 31 525,13 USDC à `Caw4Rrwk` le 22/07 à 05:23.

**Entrées et sorties de P1.**
- Entrées pures externes : 703,2 SOL éq. de hot wallets étiquetés (Coinbase 1 334,3 ; Coinbase 2 322,5 ; Coinbase 3 31,4 ; Binance 1 15,0), 639,0 de la famille présumée, 573,2 sans étiquette. Avant le mint : 171,4 étiquetés, 151,6 sans étiquette (`g59.txt`).
- Encaissements liés à DMAGA : ventes directes 619,1 SOL éq. pour 13,76 M de jetons, DCA 1 292,4 SOL éq. pour 113,37 M. Achats : 344,9 SOL éq. (`g51.txt`, `g52.txt`).
- Autres jetons : 812,6 SOL éq. vendus, 1 039,2 achetés. Les dépôts de P1 ne viennent donc pas tous de DMAGA.
- Sorties : 86,6 % des 3 626,0 SOL éq. externes s'arrêtent sur les deux dépôts (section 6).
- Dans les 24 h après 19:30:13, le DCA de la série encaisse 639,7 SOL éq., rien avant. Rapport à 190 532 SOL de marché : 0,34 %, ordre de grandeur seulement, car je n'ai pas vérifié si ce total compte ces exécutions.

**5QhJJc agit dans P1 (B pour la coordination).** Le 29/09/2024, de 07:48:23 à 07:51:57, 7 wallets de P1 lui envoient 21,23 M de jetons. De 09:36 à 09:41, il envoie 10 M chacun à `D8syomxN`, `HQzyBQN8`, `Cv3p9Wu1`, `7VtkbUQm`, plus 0,015 SOL de gaz aux trois premiers. De 12:08:51 à 12:14:33, six wallets versent 83,5 SOL à `9W9b3zgH`.

**Séance commune sur les deux dépôts (B pour la coordination).** Le 26/01/2025, de l'USDC arrive sur `Caw4Rrwk` de 16:06:38 à 16:09:25 et de 17:18:05 à 17:20:43, du SOL sur `9W9b3zgH` de 16:11:24 à 16:15:09 et de 17:13:19 à 17:21:56. Sur les 27 wallets communs, 8 ont un écart minimal de 15 min au plus entre les deux dépôts. Permutation des wallets à calendrier fixe, 5 000 tirages : moyenne 1,59, P = 0,0002.

**Vidage du 21/08/2025 (B pour la coordination).** 32 wallets versent leur reste à `ET7a91Ee` de 06:05:00 à 06:55:29, 1,22 SOL au total, 18 sont expéditeurs de l'un des deux dépôts (`g43.txt`). Ce wallet renvoie 1,19 SOL vers `A7JYFhNe`, que je n'ai pas suivi.

**`BuHUkjUy` referme la boucle (B).** Déjà relié à `9W9b3zgH` par le montant apparié de N04, il verse lui-même 7 377,35 USDC à `Caw4Rrwk` les 03/08 et 21/08/2025.

**Alternatives testées.** Hot wallet commun : écarté, le retour se mesure sur les dépôts. Hasard du calendrier : écarté par la permutation. Trésorier ou opérateur tenant un compte pour plusieurs personnes : reste possible, la chaîne ne le tranche pas.

**Inconnu.** Le titulaire du compte. Ce qui suit l'entrée chez Coinbase.

## 2. Premiers financeurs et distributeurs

Préfixes résolus avec assertion d'unicité : `prefixes.txt`. Flux purs d'au moins 0,01 SOL avant le mint, en SOL (`g32.txt`, `g32_origin.csv`).

| Wallet | Premier financeur | Entrées | Principales sources | Sorties | Principales destinations |
|---|---|---|---|---|---|
| `G41vRrsH` | MEXC 1, 26/12/2023, 3,97 | 41,32 | `4EishudC` 21,76 ; MEXC 1 5,95 | 57,40 | `AQVgyg8P` 23,0 ; `Fbyt3nao` 8,0 ; `NxtXcmEW` 8,0 ; `GFpqfjEQ` 5,0 |
| `NxtXcmEW` | MEXC 1, 26/03/2024, 1,36 | 12,28 | `G41vRrsH` 8,0 ; `GFpqfjEQ` 2,92 | 34,98 | `GFpqfjEQ` 12,5 ; `Fbyt3nao` 10,4 ; `AQVgyg8P` 6,0 |
| `GFpqfjEQ` | `NxtXcmEW`, 10/04/2024, 1,0 | 17,50 | `NxtXcmEW` 12,5 ; `G41vRrsH` 5,0 | 2,92 | `NxtXcmEW` 2,92 |
| `74qFhHyp` | `45i7PmS9`, 11/03/2024, 0,13 | 118,75 | `DYH5edZK` 79,02 ; `AtZjv3Du` 20,84 ; Binance 1 8,48 | 214,50 et 2 820 USDC | `9FTWDMJz` 65,22 ; `DYH5edZK` 61,73 ; `By6Dao4Q` 54,0 |
| `AtZjv3Du` | `74qFhHyp`, 05/06/2024, 0,01 | 21,11 et 2 820 USDC | `74qFhHyp` seul | 50,18 | `74qFhHyp` 20,84 ; `DYH5edZK` 10,3 ; `6t2dz4jm` 10,29 |

**Trois signatures de plate-forme (A pour chaque flux, C pour le sens).** Bloc `G41vRrsH` : entrée MEXC, sortie Coinbase par `AQVgyg8P`. Bloc `74qFhHyp` : entrée Binance et sans étiquette, sortie `By6Dao4Q` vers un service qui balaie vers Binance 1. Périmètre créateur : entrée et sortie Coinbase. Cela va contre un compte unique d'échange, sans exclure une même personne à plusieurs comptes.

**Quand les grappes se rejoignent (`g32_merge.csv`).** Seuils : 0,05 SOL, 5 USD, 100 000 jetons.
- Avant le mint, composantes de 31, 5 et 2 wallets. La plus grande réunit le bloc `G41vRrsH` et le bloc `DfYyxDNE`, par une seule chaîne : `NxtXcmEW` vers `2VTfi1DK` 1,3317 SOL le 11/06/2024, puis `2VTfi1DK` vers `DfYyxDNE` 0,78 SOL le 21/06. **Niveau C, fragile :** une seule arête, sans financement initial, et `2VTfi1DK` a déjà 8,14 SOL d'autres sources.
- 14/07/2024 à 02:40:26 : `AtZjv3Du` vers `NxtXcmEW`, 130 000 jetons, joint le bloc `74qFhHyp`. Les 41 M de C suivent.
- 15/07 à 01:14:34 : `NxtXcmEW` vers `5QhJJcFZ`, 8 M.
- 15/07 de 23:41:49 à 23:42:03 : `Fp6kgqHU` et `7FGoCB63`, de la série, paient de l'USDC à `B252jsFK`, joignant la série au bloc `DfYyxDNE`, en 14 s.
- 18/07 à 23:12:43 : `4wComYHQ` vers `74qFhHyp`, 15 M, joint le bloc `Ei5yGz8d`.
- À Musk, 50 des 88 cibles forment une composante. Cela prouve des transactions, pas un contrôle commun. Plusieurs arêtes peuvent être des ventes de gré à gré.

**Gestes du 21/07/2024 (`g32_gestes.csv`, A pour les transactions).**
- 07:57:16 à 08:32:13 : `GFpqfjEQ` répartit vers 10 wallets. 08:25:14 : `ADnZ9NdL` vers `CZsBW8yC`, 5 M. 08:33:36 : `NxtXcmEW` vers `GFpqfjEQ`, 1 M. 11:10:25 : `AtZjv3Du` vers `Akp46Dic`, 6 M.
- 14:22:00 à 14:25:44 : `FjuV7mJU` et `HkrGvxap` vers `C73Yv9iH`, 12 M ; `HKXb8Lfy`, `8xjM4fGg`, `2BLSXbea` vers `BuBXTWEC`, 14 M.
- Sur 7 jours, ceux qui restent tenus : `2mW45kXp`, `4upmFYy6`, `EZXUvi4X`, `HkFSNPjN`, `CZsBW8yC` ne vendent rien.

**Ce que ces gestes ont financé.**
- `C73Yv9iH` : 57 ventes en 7 jours, 19,88 M de jetons, 1 466,07 SOL. Il vendait déjà de petites quantités depuis le 15/07 à 17:05:40. Dès 22:53:42 le 21/07, ordres vers `0x2d86499a` (section 6). Avec `BuBXTWEC`, il envoie aussi 2 171,8 SOL à `RBsneDCL`, dont 1 624,8 lus en pur et 547,0 hors historique, de mai 2024 à janvier 2025.
- `AtZjv3Du` : 3 M vendus pour 327,33 SOL, 8 M vers `Akp46Dic`. `Akp46Dic` : 7,7 M vendus pour 268,7 SOL.
- Wallets neufs juste après Musk, financés par ce bloc : `72Pgt5Mr` (21/07 à 20:37), `7SEoKiBL` (21:42), `7zycfr97` (23:21), puis `B1KEP1nu`, `7TQBJhqb`, `4Tqy4SPN` (24/07), `ASWgowZA` (25/07), `4aJ4oko7` (26/07), `J2EuNwCS` (08/08). Ils se paient du gaz entre eux et convertissent en USDC. **B pour un même opérateur** sur ce sous-ensemble, histoire partielle : une page lue pour la plupart. Deux ordres de pont : `J2EuNwCS` 20 462,51 USD vers Base, `7SEoKiBL` 11 211,90 USD vers Arbitrum.

**Inconnu.** Si `DYH5edZK` et `4EishudC` sont des wallets ou des services : pages partielles. Ce que `Fbyt3nao` a reçu avant le mint : non suivi.

## 3. Collecteurs

**Test de dépôt, adresse par adresse (`g22_all.txt`).** Témoin de C et D : 8 expéditeurs sur 1 365 touchent DMAGA dans 120 dépôts Coinbase témoins, soit 0,59 %.

| Adresse | Tx lues | Expéditeurs réels | Touchent DMAGA | Sorties | Destination | Signées par l'adresse | Délai médian |
|---|---|---|---|---|---|---|---|
| `9W9b3zgH` | 285, complet | 48 | 31 | 956,51 SOL | Coinbase étiqueté 94,5 %, famille présumée 5,5 % | 59 sur 59 | 126 s |
| `Caw4Rrwk` | 508, complet | 55 | 22 | 590 933,96 USD, 35,62 SOL | USD : étiqueté 55,8 %, famille présumée 44,2 % | 85 sur 85 | 120 s |
| `AQVgyg8P` | 93, complet | 6 | 5 | 116,04 SOL, 5 400 USDC | SOL : étiqueté 62,3 %, famille présumée 37,7 % | 16 sur 16 | 115 s |
| `H9Xezqfd` | 904, complet | 10 | 8 | 3 135,76 SOL | Étiqueté 86,3 %, reste surtout famille présumée | 161 sur 161 | 142 s |
| `By6Dao4Q` | 88, complet | 8 | 6 | 343,36 SOL | `6hXrioEs` 192,30 ; `33RuC2ig` 151,06 | 18 sur 18 | 1 478 s |
| `42MSVeV4` | 75, complet | 6 | 3 | 2 067,85 SOL | `94xmX5J9` 100 % | 19 sur 19 | 233 s |
| `9kqTVnRU` | 49, complet | 7 | 3 | 316,66 SOL | `94xmX5J9` 100 % | 11 sur 11 | 166 s |
| `8N4AvP9j` | 400, partiel | 19 | 6 | 2 109,31 SOL, 131 569,31 USD | MEXC 1 : 2 063,32 SOL, 124 040,80 USD | 62 sur 62 | 308 s |

La famille présumée n'est jamais une étiquette vérifiée. Elle se définit ainsi : destinations balayées aussi par des dépôts témoins (`g31_ctrl_overlap.txt`).

**Type, niveau.**
- `9W9b3zgH`, `Caw4Rrwk`, `AQVgyg8P`, `H9Xezqfd` : compte de dépôt balayé vers Coinbase, **B**. Aucune de ces adresses ne signe de programme, toutes ne signent que des balayages (`g57.txt`).
- Preuve supplémentaire pour `Caw4Rrwk` : `59L2oxym` lui verse 0,00864088 SOL trois fois, juste après des dépôts en USDC. Il alimente aussi 7 dépôts témoins sur 120, et ce montant exact s'y retrouve. Le compte a besoin de gaz pour balayer des jetons : c'est une infrastructure de la plate-forme (B).
- `8N4AvP9j` : compte balayé vers MEXC 1, **B**, histoire incomplète.
- `42MSVeV4`, `9kqTVnRU` : relais à 100 % vers `94xmX5J9`, hot wallet non nommé, **C**. Aucun dépôt témoin Coinbase ne balaie vers lui (0 sur 120).
- `By6Dao4Q` : relais vers `6hXrioEs` puis `33RuC2ig`, qui balaie à 100 % vers Binance 1 sur sa première page (2023) et sa dernière (2026), avec 52 et 42 expéditeurs sur ces pages (`g39.txt`). **C**, service non nommé, frontière posée sur `6hXrioEs` et `33RuC2ig`.

**Tout ce qui entre, par date, par wallet.** Fichiers complets : `g30_in.csv` (chaque entrée), `g30_by_month.csv`, `g30_by_wallet.csv`.
- `9W9b3zgH`, SOL par mois : 04/2024 0,1 ; 05 33,9 ; 06 196,6 ; 07 109,4 ; 08 365,2 ; 09 154,5 ; 11 5,0 ; 12 17,5 ; 01/2025 17,2 ; 02 8,9 ; 03 16,8 ; 05 22,1 ; 07 6,6 ; 08 2,6.
- `Caw4Rrwk`, SOL éq. par mois : 07/2024 744,8 ; 08 176,8 ; 09 191,8 ; 10 367,8 ; 11 201,0 ; 12 70,8 ; 01/2025 634,8 ; 02 5,1 ; 04 89,7 ; 05 11,8 ; 07 192,7 ; 08 549,2 ; puis de 3,9 à 39,5 par mois jusqu'au 05/08/2026.

**Part liée au jeton (`g30.txt`), en SOL éq.** Le plancher ne compte que ce que le wallet a lui-même encaissé de DMAGA avant ce versement, DCA compris. Le plafond compte tout versement après le mint d'un wallet qui touche DMAGA. La vérité est entre les deux, car l'argent passe de wallet à wallet.

| Dépôt | Total | Avant le mint, non lié | Plancher lié | Plafond lié | Après le mint, expéditeur sans DMAGA |
|---|---|---|---|---|---|
| `9W9b3zgH` | 956,52 | 230,61 (24,1 %) | 335,34 (35,1 %) | 595,26 (62,2 %) | 130,65 (13,7 %) |
| `Caw4Rrwk` | 3 438,04 | 43,89 (1,3 %) | 1 323,00 (38,5 %) | 2 521,84 (73,4 %) | 872,31 (25,4 %) |
| `AQVgyg8P` | 145,00 | 29,00 | 103,00 | 116,00 | 0,01 |
| `By6Dao4Q` | 343,36 | 56,00 | 139,86 | 139,86 | 147,50 |
| `H9Xezqfd` | 3 135,77 | 85,21 | 1 983,95 | 3 050,57 | 0,00 |

**Dépôt commun entre deux périmètres : le test (`g30_overlap.csv`).**
- `9W9b3zgH` et `Caw4Rrwk` : 27 expéditeurs communs. Témoin, 7 140 paires de dépôts : maximum 4, aucune paire à 5 ou plus (`g31_ctrl_overlap.txt`). Limites du témoin : SOL seulement, 3 pages par dépôt, et l'autre côté est ici de l'USDC.
- `9W9b3zgH` et `AQVgyg8P` : `G41vRrsH` seul. `9W9b3zgH` et `By6Dao4Q` : `AtZjv3Du` seul. `Caw4Rrwk` et `AQVgyg8P` : `59L2oxym` seul, écarté (section 8).
- Tous les autres couples, gagnants compris : 0 pour les 5 dépôts des périmètres, hors les 3 de `GXZvXsD6` entre eux.

**Ce qui pourrait réfuter un même compte pour `9W9b3zgH` et `Caw4Rrwk`.**
- Des expéditeurs étrangers. Résultat : sur les 26 expéditeurs réels hors P1 et hors 33, 20 ont une arête directe au périmètre créateur, 822,89 SOL éq. sur 925,45. Les 6 autres (102,5 SOL éq.) n'ont pas d'arête vue, dont `FeompFnD` pour 66,4, avec historique partiel (`g50.txt`). Seuls 9 ont un historique lu : une absence d'arête n'est pas une preuve.
- Un service de masse. Résultat : 55 expéditeurs, dont 22 touchent DMAGA, contre 0,59 % au témoin.
- Une réquisition de Coinbase trancherait seule. Je maintiens **C pour un même bénéficiaire**.

**La seule jonction par dépôt entre les 33 et le périmètre créateur (hors `5QhJJcFZ` et `7FGoCB63`, déjà dans la série).** Le 23/07/2024 de 02:14:06 à 02:16:50, `EGtyQEgM` 7,9 SOL, `G41vRrsH` 8,0, `C73Yv9iH` 8,0, `AtZjv3Du` 8,0 versent à `9W9b3zgH`, soit 31,9 SOL, 3,3 % de ses entrées.
- Transaction A, coordination B : 164 s, montants ronds, au moins 2 grappes d'avant le mint.
- Contrôle commun **non établi**. Contre lui : `G41vRrsH` verse 36 SOL à son propre dépôt `AQVgyg8P`, y compris 4 jours après, `AtZjv3Du` 7 SOL à `By6Dao4Q`, et `C73Yv9iH` passe par `RBsneDCL` et un pont. Soldes non vidés.
- Lecture la plus simple : un paiement vers le titulaire de `9W9b3zgH`. **C, non démontré.** Autre lecture possible : une même main à plusieurs comptes.

**`H9Xezqfd`.** 10 expéditeurs, 8 touchent DMAGA. Compte actif jusqu'au 03/11/2026. Reçoit aussi 2,5 M de jetons de `EGzN5Gfc` le 03/12/2025, jamais balayés dans 904 tx.

## 4. Les 3 gros gagnants

Aucun transfert direct entre eux, ni avec le périmètre P (série, 33, expéditeurs des 4 dépôts) pour `H3QsBrri` et `9PrmF8sf` et leurs wallets suivants (`g46.txt`). Une absence d'arête n'est pas une preuve d'absence.

**`H3QsBrri` (A pour les flux, frontière non atteinte).** 16,82 M vendus pour 5 498,1 SOL. Sorties pures : `8YSi5yNR` 2 840 SOL du 24 au 31/07/2024, puis `E1wDwfkh`, `AGG2Fsrp`, `BZ2UcCuj`, `5QbApAqu` environ 300 SOL chacun en 45 min le 24/07.
- Ces 5 wallets, lus sur 137 à 600 tx : aucun hot wallet étiqueté en destination (`g55.csv`). Ils tradent, gardent de gros soldes et alimentent `nbL5GccM`, `rzCo83Ve`, `5vgqBABn`, `A3EQhVTu`.
- Seule frontière vue : `8YSi5yNR` passe deux ordres de pont le 20/03/2025, 9 912,83 USD vers BSC, receveur `0xfb2ec4e5`.
- Hors historique, 642,2 SOL éq. vers des wallets non suivis : `H3QsBrri` reste tronqué au 10/11/2024.
- Jonctions : aucune retenue (section 8). **Inconnu :** la sortie finale de 79,7 % de ses SOL éq.

**`GXZvXsD6` (B pour les dépôts, C pour la jonction).** 14,70 M vendus pour 2 565,2 SOL.
- Directement : `8N4AvP9j` 518,87 SOL, `42MSVeV4` 459,26, `9kqTVnRU` 145,02.
- Par relais : `Co3zTr2M` 1 530,33 SOL le 23/07/2024, puis 1 060,1 vers `42MSVeV4` et 310 vers `AverrTRT`, qui verse 352,1 à `42MSVeV4`.
- Frontières : MEXC 1 et `94xmX5J9`, service non nommé.
- **Même compte ou opérateur (B) :** `GXZvXsD6`, `HW5MqvM1` et `FB8241Dx` partagent ces comptes. `HW5MqvM1` en utilise 3 sur 3. `GXZvXsD6` envoie 10 SOL à `FB8241Dx` le 14/07/2024 à 01:23:33, 42 min avant le mint.

**Jonction indirecte avec la série.** Deux arêtes directes sur 24 wallets de ce côté, aucune vers `GXZvXsD6` lui-même.
- `ERMtiLod` donne 1,5 M à `HW5MqvM1` le 15/07/2024 à 18:39:06. Aucun SOL en retour sous 7 jours. `HW5MqvM1` vend tout pour 92,68 WSOL le 23/07, puis verse 95 SOL à `42MSVeV4` le 25/07, le compte où `GXZvXsD6` a versé 359,76 SOL trois jours plus tôt.
- `GoPCTrS3` donne 1 M à `HKzkNSH2` le 21/07/2024 à 23:00:23, payant le compte de jetons, première tx de ce wallet. Vente le 26/07 pour 28,9 WSOL. `HKzkNSH2` verse ensuite 108,8 SOL à `8N4AvP9j`.
- Base de comparaison : ces 2 wallets sont parmi 22 destinataires externes de la série, 45,42 M de jetons (`g49.txt`). Aucun des 20 autres n'utilise ces comptes, dans ce qui est lu.
- Transaction A. Coordination C. Contrôle commun C : indice seul.
- **Explications alternatives, retenues comme possibles :** paiement en jetons à des tiers qui partagent un compte, vente de gré à gré réglée ailleurs, trésorier. `GXZvXsD6` a acheté son stock au pool, pas auprès de la série. `HW5MqvM1` utilise `8N4AvP9j` depuis le 31/01/2024, bien avant DMAGA.

**`9PrmF8sf` (B pour le compte de dépôt, frontière atteinte).** 81,76 M vendus pour 2 011,6 SOL. 98,8 % de ses sorties vont à `H9Xezqfd` : 2 051,9 SOL, du 31/01/2024 au 27/10/2026. Il retire 430,0 SOL de hot wallets Coinbase.
- Il partage ce compte avec 9 autres expéditeurs, dont `8B5ekuLt` (73,63 M de jetons reçus et sortis à partir du 30/08/2024), `EGzN5Gfc` (31,83 M), `ENvLw1g1` (20,51 M). 8 sur 10 touchent DMAGA. Hors `9PrmF8sf`, les 5 dont je lis les mouvements de jetons commencent tous après le 21/07/2024 (`g46.txt`).
- **B pour un même opérateur ou compte, C pour un même bénéficiaire.** Ce périmètre est distinct : 0 expéditeur commun avec les 4 autres dépôts. L'audit C cite ce dépôt sans le mesurer.

**Autres contreparties rares communes : 6, toutes rejetées** (section 8, `g46_common.csv`).

## 5. Piste A-16

**Mécanisme (A pour la forme, `g53.txt`).** Les 3 826 tx DMAGA de `3GMsedVP` forment 1 913 blocs, chacun avec exactement 2 jambes de même quantité à 1 % près et exactement une jambe de tiers entre les deux, à des index distants de 2 dans le bloc (`g67.txt`).
- 967 blocs : un signataire achète, un tiers achète, le signataire revend. Achats de tiers intercalés : 12 068,1 SOL. Marge : 9,44 SOL, positive 967 fois sur 967.
- 946 blocs : `4ToQp55m` vend, un tiers vend, `4ToQp55m` rachète. Ventes de tiers intercalées : 17 954,8 SOL. Marge : 185,41 SOL.
- Forme d'un sandwich. Niveau B pour le mot : je lis la forme, pas l'intention. Arbitrage ordinaire écarté, car un tiers figure entre les jambes dans 1 913 blocs sur 1 913.

**Service ou opérateur unique (B pour un trésor unique, identité inconnue).**
- 45 signataires sur 45 échangent du SOL avec `4ToQp55m`. Vu dans `raw/flows` : 54 546,42 SOL vers eux, 292 787,77 SOL en retour, tous jetons. Hors pool, seuls 2 expéditeurs de poussière en plus. Aucun client visible (`g42.txt`).
- Programme créé le 13/07/2024 à 14:14:06 par `FyC5nr3W`, fermé par le même le 10/10/2024 à 07:42:08 : 89 jours. Il n'est pas signataire sur DMAGA, il l'est sur d'autres jetons.
- Pages lues : 25 et 42 mints distincts. Il travaille sur de nombreux jetons, pas sur DMAGA seul. `4ToQp55m` bouge dans 79 et 99 tx sur 100.
- Reste possible : `4ToQp55m` mis en commun par plusieurs personnes.

**Rôle réel dans le volume (A).** 24 537,38 SOL d'achats, 3,12 % du total sur toute l'histoire ; 4,44 % sur 3 h avant S ; 2,44 % sur 24 h avant S ; 3,92 % sur 24 h après 19:30:13. Net de jetons nul. Marge totale 194,85 SOL. Ce n'est ni de l'accumulation ni de la distribution.

**Lien avec les périmètres : aucun.** 0 arête directe avec les cibles (`g47.txt`), 0 signataire dans les 33 (audit A, `a37_svc.txt`, repris). **N'en rien déduire d'autre.**

## 6. Table des frontières

Unité : SOL éq. Sont comptés les virements purs d'au moins 0,01 SOL ou 1 USD sortant de chaque périmètre, et les ordres inter-chaînes décodés. Dénominateur : hors interne, pools et routes. Les swaps ne sont pas des sorties. « Hors historique » : ligne de `raw/flows` au-delà d'un historique tronqué, pureté inconnue. La table s'arrête au premier saut : un wallet sondé n'est pas une frontière, mais le point où la trace s'arrête.

| Frontière (niveau de la qualification) | P1 | P2 | H3QsBr | GXZvX | 9PrmF8 | Total | Part |
|---|---|---|---|---|---|---|---|
| Dépôt balayé vers Coinbase (B) | 3138.6 | 176.9 (dont 29.0 hors historique) | 0.0 | 0.0 | 2051.9 (dont 26.5 hors historique) | 5367.5 | 20.9 % |
| Compte balayé vers autre plate-forme (B ou C) | 0.0 | 143.0 | 0.0 | 1123.1 | 0.0 | 1266.1 | 4.9 % |
| Pont, ordre inter-chaînes (B) | 22.1 | 5464.9 | 0.0 | 0.0 | 0.0 | 5487.0 | 21.3 % |
| Hot wallet ou service étiqueté (A) | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 % |
| Famille présumée (C) | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 % |
| Service ou pool non nommé (C) | 30.8 | 334.6 (dont 304.0 hors historique) | 382.9 (dont 382.9 hors historique) | 0.0 | 0.0 | 748.2 | 2.9 % |
| Wallet sondé, trace arrêtée (C) | 6.2 | 3561.9 (dont 547.0 hors historique) | 4038.9 | 1530.3 | 0.0 | 9137.3 | 35.5 % |
| Wallet non suivi, aucun historique (D) | 428.3 | 2582.8 (dont 714.5 hors historique) | 648.8 (dont 642.2 hors historique) | 16.0 | 25.1 (dont 7.5 hors historique) | 3701.0 | 14.4 % |
| Autre périmètre (A) | 0.0 | 28.2 | 0.0 | 0.0 | 0.0 | 28.2 | 0.1 % |
| **Dénominateur** | **3626.0** | **12292.2** | **5070.6** | **2669.5** | **2077.0** | **25735.4** | 100 % |
| Interne, hors dénominateur | 827.7 | 510.6 | 0.0 | 0.0 | 0.0 | 1338.2 | |
| Pools et routes, hors dénominateur | 0.0 | 368.3 | 774.3 | 0.0 | 26.9 | 1169.5 | |

Lecture :
- P1 s'arrête à 86,6 % sur ses deux dépôts.
- P2 passe d'abord par des ponts, 5 464,9 sur 12 292,2, soit 44,5 %. Dépôts Coinbase : 1,4 %. Ce n'est pas la même sortie que P1.
- `RBsneDCL` pèse 2 171,8 SOL éq. de la ligne « wallet sondé » de P2. Il renvoie à `RBHdGVfD` et reçoit aussi d'autres expéditeurs. `RBHdGVfD` signe 100 tx en 23 min le 03/11/2026 (`g56.txt`). Service ou gros opérateur non nommé, **C**.
- Les 5 wallets de `H3QsBrri` pèsent 4 038,9 SOL éq. de cette ligne : non résolus.
- Environ 14,4 % restent sur des wallets sans aucun historique lu : niveau D, ce n'est pas une frontière.

**Ponts (A pour l'ordre, B pour la sortie).** Programme `src5qyZH`, journal `CreateOrderWithNonce`. C'est le DlnSource de deBridge d'après sa [documentation officielle](https://docs.debridge.com/dln-details/overview/deployed-contracts). Champs décodés cohérents : chaînes 1, 56, 137, 8453, 42161, adresses USDC connues, montants égaux aux jetons sortis. Aucun remboursement vu dans les historiques. Exécution sur la chaîne d'arrivée : **non vérifiée**, je m'arrête là. Liste complète : annexe et `g43_orders.csv`. S'y ajoute `BrdgN2RP`, journal `SwapAndBridge`, 7 855,50 USDC de `Ei5yGz8d` le 31/03/2024, nom non vérifié.

**Aucun mixeur** parmi les programmes des sorties sans contrepartie, 6 575,5 SOL éq. lus (`g45.txt`). Limite : historiques partiels.

## 7. Ce qui change par rapport à `CLAIM_VERIFICATION.csv`

| Ligne | Écrit aujourd'hui | Changement proposé | Preuve |
|---|---|---|---|
| N01 | 13 sur 2 201, `Fp6kgqHU` ne revient pas (section 4.2 de l'audit final) | 14 sur 2 201, tous dans les 507 s, en comptant le dépôt USDC. Niveaux inchangés | `g66.txt` |
| N02 | 9W9b compte de dépôt, frais de 155 000 lamports comme argument | Ajouter `Caw4Rrwk`, `AQVgyg8P`, `H9Xezqfd`. Retirer l'argument des frais : `42MSVeV4` paie 155 000 lamports 19 fois sur 19 vers une adresse balayée par 0 dépôt témoin. Ajouter le gaz de `59L2oxym` | `g22_all.txt`, `g43.txt` |
| N03 | 31 sur 48 | Ajouter 22 sur 55 pour `Caw4Rrwk`, 27 communs. Niveaux inchangés | `g30.txt` |
| N04 | Lien en 2025, niveau B | Inchangé, renforcé : `BuHUkjUy` verse 7 377,35 USDC à `Caw4Rrwk` | `g30_in.csv` |
| N05 | Le créateur n'échange aucun jeton avec les 33 | Inchangé pour le créateur. Préciser que `5QhJJcFZ` travaille dans P1, le 29/09/2024 | `g33_bridge.csv` |
| C18 | 94,5 % vers Coinbase | 94,5 % sur étiquettes, 100 % avec la famille présumée, à écrire comme présumée | `flow_boundaries.csv` |
| C20 | 3 gagnants sans lien direct avec les 33 | PASS maintenu. Ajouter G7, indirect, niveau C, et le périmètre `H9Xezqfd` | `g46.txt`, `g49.txt` |
| C37, N16 | 6 échanges, service non nommé 175 427 SOL éq. | Ajouter les ponts, absents. Des comptes d'ordre à 2 tx (`ERm6ztBi`, `Hiz7GLUw`, `6d8vRyKP`, `H4TnZyc9`, `DEuwaZcb`) ressemblent à des destinations sans étiquette. Je n'ai pas décomposé les 175 427 : **à revérifier** | `g43_orders.csv`, `g55.csv` |
| C50 | FAIL, un hot wallet ne coupe pas tout | Renforcé par G2 | `g66.txt` |
| C51 | Escrows DCA retirés des liens | PASS maintenu : correct pour les liens. Mais les ventes de P1 passent par eux : les mesures de swaps seuls les sous-estiment | `g52.txt` |
| N07 | Ventes élargies du groupe | Inchangé pour les 33. Ajouter à part 639,7 SOL éq. de DCA de la série sur 24 h : `5QhJJcFZ` et `7FGoCB63` n'y comptent pour rien | `g59.txt` |
| A-16, section 8 de l'audit final | Nature non identifiée | Forme de sandwich, trésor unique, aucun lien | `g53.txt` |

Aucun FAIL nouveau. Je ne modifie ni `CLAIM_VERIFICATION.csv` ni un rapport : décision du coordinateur.

## 8. Liens faux ou trop fragiles écartés

- **`59L2oxym`, seul commun entre `Caw4Rrwk` et `AQVgyg8P`.** Gaz de plate-forme : il alimente aussi 7 dépôts témoins sur 120. Faux lien.
- **Frais de 155 000 lamports.** Pas une empreinte de Coinbase (voir N02).
- **`Habp5bnc`, `FLiPggWY` et familles.** Poussière présente dans 71 et 70 dépôts témoins sur 120 (`g43.txt`). Aucun lien par là.
- **Adresses imitées autour de `By6Dao4Q`, `AQVgyg8P`, `Co3zTr2M`, `8YSi5yNR`.** Virements d'empoisonnement à zéro ou presque, comptés à 0.
- **`5ndLnEYq`.** Finance `H3QsBrri` (26,88 SOL en 03/2024) et `C73Yv9iH` (11,62 SOL le 22/07/2024). 58 expéditeurs et 36 destinataires en 100 tx sur sa première page : trop actif pour relier qui que ce soit. D.
- **`GMgh4NtW`, `83v8iPyZ`, `7oFfdxSk`, `9yj3zvLS`.** Jamais ou presque signataires, nombreux jetons : pools ou routes.
- **`23vEM5NA`.** Paiements `SinglePayment` à 3 jambes de `H3QsBrri`, `C73Yv9iH`, `2VTfi1DK`, aux montants répétés 197,01 et 296,01 USDC : commerçant, pas un lien.
- **`FJ9LmErk`.** 0,05 SOL de `5QhJJcFZ` et de `H3QsBrri` le 22/07/2024. Trader à 90 tx signées en 32 min. Rejeté.
- **`25WYn7Jr`, `42mepa9x`.** Contreparties rares communes, faible montant, aucune structure. Rejetées.
- **`8SaiGWJn` et `Ej5Qv3UB` le 15/03/2025.** Même minute, mais la réception de 4,9 M est la fin d'un DCA. Coïncidence.
- **`C7qEaB6a`.** 12 wallets lui versent 14 M par tranches de 1 M du 16 au 20/11/2024, dont `NxtXcmEW` 2 M et `7mdCAs8C` 1 M. Puis `Ej5Qv3UB`, puis `94Q76Saa`. Mise en commun de détenteurs possible. **Pas un contrôle commun, non interprété.**
- **`NxtXcmEW` vers `2VTfi1DK`.** Gardé comme indice C seulement. À ne pas présenter comme la preuve d'une grappe unique avant le mint.
- **Reliquat de `AVUCZyuT`, `9yMwSPk9`.** Comptes de frais de terminaux, déjà écartés par C-15.

## 9. Limites

- **Historiques tronqués.** `C73Yv9iH` lu jusqu'au 05/11/2024, `H3QsBrri` jusqu'au 10/11/2024, `8N4AvP9j` 400 tx. Limite de C à 1 200 tx pour `7mdCAs8C`, `8SaiGWJn`, `9PrmF8sf`, `BuHUkjUy`, `DfYyxDNE`, `EZXUvi4X`, `GFpqfjEQ`. Une page à six pour les sondés. Complets : les 5 dépôts des périmètres, `42MSVeV4`, `9kqTVnRU`, `Ei5yGz8d`.
- **Pureté.** Flux au-delà de la troncature repris de `raw/flows`, marqués dans la table et dans le CSV. Virements médiés exclus, sauf ponts.
- **Sources.** `data/trades.parquet` et `wallets.parquet` non utilisés. Tables A et D relues pour les jambes et « touche DMAGA » (`d01_own`). La classe « pool » lit `reports/data_checks/venues.json`, modifié en parallèle par un autre agent : sert seulement à exclure, et 1 169,5 SOL éq. de pools et routes en dépendent au plus.
- **Hors chaîne.** Titulaires, destination des fonds après Coinbase, MEXC et Binance, exécution des ordres sur les chaînes d'arrivée : non vérifiés.
- **Découpage.** Le périmètre P1 a été posé d'après les audits, après avoir vu les faits. Les tests de la section 3 sont exploratoires, et aucun seuil n'est gelé.
- **Interruptions.** Limite d'usage à 11:16 UTC, coupure réseau à 14:02 UTC. Rien de partiel n'a été repris sans contrôle : `g32*` relu entier puis recalculé, `g36` relancé, `g22_all`, `g40`, `g64` contrôlés, chaîne recalculée dans l'ordre (`run_chain.sh`).
- **Journal.** Consigne d'écriture limitée à `work_G` : `JOURNAL_AGENTS.md` n'a pas reçu d'entrée de ma part.

Reproduire : `run_chain.sh`, puis `g59_inflows.py`, `g64_table.py`, `g66_window.py`, `g61_refs.py`, `g62_check.py`, depuis la racine du dépôt. Sans appel réseau, les réponses restant dans `audits_work/G/net/`.

## Annexe : références complètes, écrites par script

### Salve USDC vers Caw4Rrwk, 22/07/2024

| UTC | expéditeur | actif | montant | signature |
|---|---|---|---|---|
| 2024-07-22 05:22:29 | Fp6kgqHUHFxdCVNRf1Z4bt4F1K5DK5Njq83PUNzUsGRt | USDC | 27704.404132 | tdaQJroJTPvETEjoLMsKeCddGhhc1ohT1NXdKMuriPEj2D8t98iN5ucuVf5MHWqqe7Z2WsMNTPizcfxoxissjpi |
| 2024-07-22 05:22:53 | 5s3ogzsq8cvwHtS1B6MhwUUp9CyzugJ6y3WqLPM9Ee3C | USDC | 18345.630776 | 3mxBGmotEZxFUaQzi8QuTGWk24SmLA45Jqu1uqZnvEtwCQDnxtj4EMQcBhK1zehkRpKv7dvkpkJ7DQnTFMSGQmfS |
| 2024-07-22 05:23:21 | HqwpWyvbCbGSbGuK1xFRptPdMYd8MHERqNJ3uACRCAmZ | USDC | 31525.13151 | 4qqNEGnK8VUxW63DudWDzLcCdm8gkeRwZbgpNUmL6fXE6EBbYmmgpVrmRUDe4fVzJ3qXt8UU8rAqA4HuKuK2Gafe |
| 2024-07-22 05:23:43 | ERMtiLodeVKQ8sK1MBPgBHyJS6DT8j61z8aQJiKYqbCH | USDC | 2980.358826 | SzT3L8i6ScJ9T7bDLndQsemWm9GkDxCEHC4t4GixtecGCkB1vGfgufLRfbWv4q78oG4zy4AUChuimKFEVuCX9en |
| 2024-07-22 05:24:04 | EEpSRR12vTrH3Wbf3Ke4vT4RkMfPTqFv5wfE948cr3Wa | USDC | 35821.854271 | 3fHcnJBuiHbMAvGxgiKntGuQxmWP9jtKjACpJZP4dk9sixX43rVP6bexwmor8zd6DJHN43DMV4mgjpD7bP1Uq2Kb |
| 2024-07-22 05:24:16 | 59L2oxymiQQ9Hvhh92nt8Y7nDYjsauFkdb3SybdnsG6h | SOL | 0.00864088 | 5c3zkHBNTaH6447MQnTUUW3qruqgFY6bt5f4gBzEHg7bqP5QcYrEJmrdHqLz3Tg9rrmP38WYLxbZb2gNpQFMB9h7 |

### Versements de 8 SOL vers 9W9b, 23/07/2024

| UTC | expéditeur | SOL | signature |
|---|---|---|---|
| 2024-07-23 02:14:06 | EGtyQEgMKGKXjppDqj9sYy97e9m7nvu1US4SfFXNakMy | 7.9 | 2mC7gPb89CVz5aZ2sn86v3XmFxYFxsWrTE5Nt2mF6WQdZz3R5k3joi9xMCUwUXg2DZrunuZ1DJdS8q5fNZ1Ubozg |
| 2024-07-23 02:15:07 | G41vRrsHShLEvwMj58ruhqJycGfAtWXxtLD56uFExL8E | 8.0 | 4e3Pg7TvkWucWVKUM5Mymc88jApjREYNsUGk9gSH9gqGWCSEBUQHPdaboYRoMTCP6hPEhw693BGh7iHnZsr3fgZN |
| 2024-07-23 02:16:17 | C73Yv9iHmTaf8SU2XFnGLt7QXUDqbeWNtUYza9WJhkae | 8.0 | 25u4vvqJkg7CTmCnEZQSRwjXG6tbjBYMq4tLtZEQqWYg6r8HfqDAuUutacKtYs1PQgce8ikjHq9vREX7PtyGrGt6 |
| 2024-07-23 02:16:50 | AtZjv3DuV9cLn3Jxm72TMSdTN4aM6CrBaGyxUC4c2wDk | 8.0 | KJDdVPyYmAUHioiv1Cf6ihJLLX6jhgieTqnUp7hobUWGEVbd5ysM2SXZY8ewBd8Mx7YBnm8gjFGYqXVJ9ZT9u73 |

### Gaz de 59L2oxym vers les dépôts

| UTC | dépôt | SOL | signature |
|---|---|---|---|
| 2024-07-02 18:12:17 | Caw4RrwkmxqtbLSFzgSs6id3XiFxWQxs2t1mrn5a3mME | 0.00864088 | 3d8NKTTvcuS65AjVjxs6XYA3CGDBZ4grEgtQTsdcdtdgs2uBrgWvqWLxSuwJN1jynoGqoXA6yXPQgWSPTik6aehj |
| 2024-07-22 05:24:16 | Caw4RrwkmxqtbLSFzgSs6id3XiFxWQxs2t1mrn5a3mME | 0.00864088 | 5c3zkHBNTaH6447MQnTUUW3qruqgFY6bt5f4gBzEHg7bqP5QcYrEJmrdHqLz3Tg9rrmP38WYLxbZb2gNpQFMB9h7 |
| 2024-08-04 19:29:03 | Caw4RrwkmxqtbLSFzgSs6id3XiFxWQxs2t1mrn5a3mME | 0.00864088 | 46yn772Tr5ye32xaf8uLThbunich86iW9gLNpPLoTamrXyhQpgfZ4JnGYe1S4EceBR88eGCzamiAKJdtBeK8mQXi |
| 2025-08-04 16:34:52 | AQVgyg8P5Yh5YcAqAMQRRGzDegy1R58gN4Qh87QsJAF1 | 0.005112732 | jM8ELxKdu86vLXpwLYdx2irYrD6jNpyftNWSD26nF7GxstYtVGeqvxUu5oZydfNYoaCjf5SH2j1Ewcx2GJnGVYD |

### HW5MqvM1, HKzkNSH2 et leurs dépôts

| UTC | expéditeur | dépôt | SOL | signature |
|---|---|---|---|---|
| 2024-01-31 20:49:57 | HW5MqvM1kDySFUtynMtzsWCU6VcFfpeCXsbRyLq6iHk6 | 8N4AvP9j5BditSQMk2WrTNxthhgpncGVzLKrYP4xdEqx | 28.0 | BHeHW9YCDNfwCS9tghaWW165Ntkibg5fP8pnBNfU8ioh8ZZyod1muyHjc3LGPdSqUjvxLYatmT6FvVoaWAJthXx |
| 2024-01-31 21:13:30 | HW5MqvM1kDySFUtynMtzsWCU6VcFfpeCXsbRyLq6iHk6 | 8N4AvP9j5BditSQMk2WrTNxthhgpncGVzLKrYP4xdEqx | 59.5 | 2mTPbfcWgzxrWhrgAv2vWLmL87bqjy1rCvJHBh3ktKysiEjFDz1LPSRiqDP3o3aAFDkwW7BqPVNWvNGZJ48r4Jsm |
| 2024-02-05 14:51:52 | HW5MqvM1kDySFUtynMtzsWCU6VcFfpeCXsbRyLq6iHk6 | 8N4AvP9j5BditSQMk2WrTNxthhgpncGVzLKrYP4xdEqx | 58.0 | 3kkWPwTiTVSXqSb2cvfeFvZe7tQeNHZufR1kzjsBLiQLewrZk5f3jB8xv2hroxeKaWsNUvokGtJWnHySpCHh8DC1 |
| 2024-07-25 14:11:03 | HW5MqvM1kDySFUtynMtzsWCU6VcFfpeCXsbRyLq6iHk6 | 42MSVeV4YbESE7mNW7DfQrfd8E4RG6njxXZLAWTmXemv | 95.0 | 2gh2nvDNTab6im9PJqL6HCebM6MtHm74KKvQZL9hqxwfYguDMaLQxeZbVvgK9WMxKY9KTY5odxSiQte6tKaUDG4M |
| 2024-08-28 23:31:54 | HW5MqvM1kDySFUtynMtzsWCU6VcFfpeCXsbRyLq6iHk6 | 9kqTVnRUkVTFD7na9BTWcoG9piL4XpVTtS9kqVCV56tV | 50.5 | 5t22KmgGFLePZtGhc73UmzaiG1XwrGdsSaDsh9whiY3BaQhGKji4ciSNy1bsiQuAKz89n1ZAXTzENoCbZGaLk7TA |
| 2024-08-30 15:31:23 | HW5MqvM1kDySFUtynMtzsWCU6VcFfpeCXsbRyLq6iHk6 | 9kqTVnRUkVTFD7na9BTWcoG9piL4XpVTtS9kqVCV56tV | 24.8 | 4vwM5LoovipkM4suMoHee8hnYoMU1k2sz4neCg6Hg8gbpJZyNPcQVoVhAThujiQ1ugTndPHcnfPN6b24cgL9NZ8F |
| 2024-09-30 03:13:01 | HKzkNSH2DmfyowntFnoa1xdUuVH4Yh6bg7z8fer4JSRP | 8N4AvP9j5BditSQMk2WrTNxthhgpncGVzLKrYP4xdEqx | 54.8 | 2Jkz5aWG2a87AMCUnzcQ1hFfiAtz3BxLzaShtCEHR25wa17gywQvSev9NWhLmwb4KpFVkFSngnZHxne5Mbe6pUE5 |
| 2024-10-01 14:54:50 | HKzkNSH2DmfyowntFnoa1xdUuVH4Yh6bg7z8fer4JSRP | 8N4AvP9j5BditSQMk2WrTNxthhgpncGVzLKrYP4xdEqx | 54.0 | 3H3DVGf5AXq1DvESdJDHDLxZDQTJR6TiU9gUJBBb3xsmpX5sY8XjHff3TSCcyrwz1oiAaXNs2V2RChhhvTBxwdDR |
| 2024-10-20 15:13:57 | HW5MqvM1kDySFUtynMtzsWCU6VcFfpeCXsbRyLq6iHk6 | 9kqTVnRUkVTFD7na9BTWcoG9piL4XpVTtS9kqVCV56tV | 6.2 | 3u68q79TBJLu3jkSV6f2GKCNsHr2oXCgniqXeiPFSdFmHoQdJXhmEi5Yj6nZJ9wraWkqEUUdHtc2y9Dq89qwzo4Z |
| 2024-12-31 21:25:16 | HW5MqvM1kDySFUtynMtzsWCU6VcFfpeCXsbRyLq6iHk6 | 8N4AvP9j5BditSQMk2WrTNxthhgpncGVzLKrYP4xdEqx | 6.9 | 2CYQofL8s6s2XaVppcXpS9GMNnxvXqRGsSerBNsa6QfSU3ffRB178WUNyqCMWrVgxT7jC2udWPfYiVYGt8TkmXtj |

### GXZvX vers ses dépôts

| UTC | dépôt | SOL | signature |
|---|---|---|---|
| 2024-07-05 03:27:32 | 8N4AvP9j5BditSQMk2WrTNxthhgpncGVzLKrYP4xdEqx | 19.736782181 | 5koUtsgPU3koZEKS2ZDoi1NqRUTPyWryfgvZjp13GCnzJJffofsk73MkWJEVHYApD3MiCtmuRw8rBBj3TEP2bZhL |
| 2024-07-05 11:40:21 | 42MSVeV4YbESE7mNW7DfQrfd8E4RG6njxXZLAWTmXemv | 99.5 | 5v2UaWNY6wZ6Y8jMPhX9MoAcuZDhiKAtLqtotYMdYSM4JwVfG9WJVAnknQwe6MMAHKcDo6jpB4aduafJD7edPUkq |
| 2024-07-21 18:11:13 | 42MSVeV4YbESE7mNW7DfQrfd8E4RG6njxXZLAWTmXemv | 19.399085623 | 3hZFAuMh4nXDEtFCugeHBFdXjLv3hocxSgxkQ6NRQ8Ncu7A52FSKxwt1ouXw2oSztSqVHuBx3VBkfejmpucvneTs |
| 2024-07-22 00:03:10 | 42MSVeV4YbESE7mNW7DfQrfd8E4RG6njxXZLAWTmXemv | 340.363743671 | 5tKPeX4XRK1zrKzsep271CLeJJDZXDFQgAoejG54E6qwAZ8XRbWzfz62vkTPKfv7qhEsvBSKpq4cmfqAshKvKm31 |
| 2024-07-22 11:34:30 | 8N4AvP9j5BditSQMk2WrTNxthhgpncGVzLKrYP4xdEqx | 499.131551515 | 54hrrrcyBoJmk3F5aGprsNJw8TQMVbr4ueKkmFHpxYRhebT8DNzjWV7Zc8X7DYrd7X6smHytg9B4xiY4oWqhvXSe |
| 2024-10-06 00:37:09 | 9kqTVnRUkVTFD7na9BTWcoG9piL4XpVTtS9kqVCV56tV | 120.0 | 63Ze2oLUUo47tjn4pyTu5CCRm3SVQhcJ1SrzWYvw4huygWbV6auNQBpZ9ccXBA4utaNzGXdziDq1Grw545YgXy66 |
| 2024-10-06 00:38:26 | 9kqTVnRUkVTFD7na9BTWcoG9piL4XpVTtS9kqVCV56tV | 25.018234663 | 4eF53SP48z7PKngKn5Kw9N3zbfoKATUbYsgZiqVFm4L3nQkufqdT3Ji4fmeWBSR1D62qy44QkRVHcqZiVFqPjaqD |

### BuHUkjUy vers Caw4Rrwk

| UTC | USD | signature |
|---|---|---|
| 2025-08-03 12:54:45 | 1770.605163 | 32miVeqaSX3wr6ZGdcj4sZNSE8oeXGd4fmgVRu7dXvCEaRWbqMGzhg1TNv8xR2TTfctLW1CU58W3gev5Gc8sTy2R |
| 2025-08-03 12:55:19 | 50.226561 | 3GPvntPo1EWPLdhRFhcVjtLPzAVgGdbZehVLpNMjjpMoHRmAua5qfB35uBSyU1eQnJWYnjMxMFB2SxZoDM7hrqZX |
| 2025-08-03 12:57:12 | 400.655066 | yHzviVMNGs7Q9CmotdTscw9PHTiqVehydb1DJqsAhRwAfXt7VMZ3n9XQsYtBGGYDGyWjFCp7fFTU3BtdRCMHak3 |
| 2025-08-21 03:06:13 | 5155.860981 | 5x4bf2X2ZwMkeHyTx9UWYUjpHomSn9aC2oNwQggJF6vBqrNa5daqsQY79vLo5JmutDTGGe81EJjqZxsv6kHbam6g |

### Ordres inter-chaînes : premier ordre par wallet et receveur

| UTC | wallet | chaîne | receveur | USD | signature |
|---|---|---|---|---|---|
| 2024-07-22 01:00:34 | HGBiExZRtD2TZdQLWHE9azkTSmE2z7ygKqZMtehJDKYU | 1 | 0xb947bf7f409e998b28f8e218802fc9575c3c8c57 | 156089.016395 | 45PnZWjKkx7c1yeEx2rr1HFCggW5J5Pr1BFz9bkb8ScKf77SQiMEL4DocKcExRsQxFmmADWvyu1r55adNUdaPuC2 |
| 2024-11-14 05:38:07 | Ei5yGz8dPndr1aCeHZsfqJBcS3VBbz75VHEhxxJKLy3V | 1 | 0xb29826d809aa04d2ead6f2310d8965a45b87fa67 | 106223.390212 | GmMeZg3GrwdQEfaexudc4gNrPnHmgjvJyjcmLeEYt3ZoLt5qxh2P1fUDR4sgtjqzPkRxtDfovQ1TV3evnkiNQZM |
| 2024-07-22 01:04:12 | Ei5yGz8dPndr1aCeHZsfqJBcS3VBbz75VHEhxxJKLy3V | 1 | 0xb947bf7f409e998b28f8e218802fc9575c3c8c57 | 47023.609816 | 4kW2yTLkXKzbb6i23StE6wswpcTr8oGNyVKa2ZBK2vTSi5nN9DXiX5YQShcjAP2LyEwNpEAFbQpRPCWEBvXCz8o8 |
| 2024-07-22 10:01:50 | C73Yv9iHmTaf8SU2XFnGLt7QXUDqbeWNtUYza9WJhkae | 1 | 0x86f99097c563e84dd5190f3e85f6a2988f1c47a5 | 17834.146969 | pDTA7K1fynUvYYtbLvK1hmW32gjDJDz4Ug4amTPvBrQJMqAbNfxYbdirgJgXZEeDUais9ToADCTivYCEbMc1ELs |
| 2024-10-25 01:31:33 | C73Yv9iHmTaf8SU2XFnGLt7QXUDqbeWNtUYza9WJhkae | 1 | 0x2d86499a410a9ac2139833ba8d6942b8a8700a7b | 17521.976128 | 5v9fu8jebs12ka1SSDq66qsyCpmu4unidffnkzu78dwCeLegsomAbcsX86T7tuirsUc8HCwGvJ9Pr21rkuSZu9xw |
| 2025-01-18 09:43:43 | 7SEoKiBLaGhZxr5V8JYGdiV55ZhkgC727ftSYDST148i | 42161 | 0x703bf8c292b72efdd60243b17be782b58cd61ce0 | 11211.903142 | 2ttZ9oZtMGEqjeLZUEpxqsWu7mZVrVDqiNCo2qiR2NjssFSZ6sNhncRZsWZX2bnWsf2zjWw2jYWovKJabSVyyRtU |
| 2024-07-26 02:10:39 | Ei5yGz8dPndr1aCeHZsfqJBcS3VBbz75VHEhxxJKLy3V | 8453 | 0xb29826d809aa04d2ead6f2310d8965a45b87fa67 | 3001.213492 | 4zQG62gTESbr4S8NJVdTQS2c6hJrC57wDsZ5QUFhEaWyKDWaNNcxW3DLtvucZHmxmb2MhpEoh3HJtwyC8GVaV2y4 |
| 2024-08-21 01:41:30 | EZXUvi4X5k3Aj99rGzNQoBtAzFqzYUjGhHNu8A1Ty8s4 | 1 | 0xe8293b6bd3a4ac365257d11c71ed55cf1fb6bc27 | 2843.000052 | 2FQU7gCh7pvyJKti4onEAETGdFt979bBtBsTgbsDrpx2kEpddF4qzeUfbtgNRUAzTHwjXXvs69jQNCcBfip7AWLz |
| 2024-11-26 05:19:21 | Ei5yGz8dPndr1aCeHZsfqJBcS3VBbz75VHEhxxJKLy3V | 8453 | 0x2ac17414e34c9a1f70f6eadb6230fa503301e878 | 2498.188909 | 4XdVBn29AL81NEDSYF2sbZpwnC5dAMtaaqNsPPo3twG78zw8Bhuh9ePDEHJ2ouead5nwGeUTD2xSLLLwui5gLGbG |
| 2024-05-21 22:17:10 | DfYyxDNEXBzZWVPuJrNfko1rDrtR8SiqWLeGUMmNn8DT | 8453 | 0x21f3a0e26d33cb48e114c4f58019463cc79799fd | 1914.737586 | 5qpRg9EZjCcfSsYC8ERaTFS6ohwKAe1wmGkjvR1fgMpMATUQF4mmi23asy1j3k6eSyBDpCcc1ZCZHUdvdBqNq4QS |
| 2024-10-11 23:42:52 | HGBiExZRtD2TZdQLWHE9azkTSmE2z7ygKqZMtehJDKYU | 8453 | 0xb29826d809aa04d2ead6f2310d8965a45b87fa67 | 1760.90575 | 5isRg9GHDtXjqLnMPNtYJHAvKN3PM8eaqT1fy3mLYno7ppDV6P3X6Dcjk3VQL4JJWrfDuwJySSdYuyWCUBNtbkL9 |
| 2025-03-20 20:38:25 | 8YSi5yNRN2KMbGU7Q3i5w9W6fTRxnk1qatQ5YmzS5da7 | 56 | 0xfb2ec4e51680198f4d0351d67702d4eebdfa625f | 971.613389 | 3bi9qiVpVZdsjgxrTebvHdPbxenKbeiS3s2fjXZRyn49nNCTposWdMp5UkZCxXRinggda1roEfqmbLdVXcvFfXvT |
| 2024-07-16 23:59:53 | 5QhJJcFZu2ashyKyWSTGHcsyo6ZBCbpVuJqeutvQHScd | 1 | 0x93822e77a68835355279af1eb10164c1922cc448 | 634.175727 | 4tXziqpEk3FgBnDqtdXX43cJpDcRj7kmNGiusKDaKjDbGu8QXV7aesZ7NM8xoc5hGsJADSCchPvAjyzZB22KJitE |
| 2024-05-07 18:57:51 | DfYyxDNEXBzZWVPuJrNfko1rDrtR8SiqWLeGUMmNn8DT | 8453 | 0xe8e9b172f2b8cb77d8aad7ce5035abcb870b9035 | 606.398042 | 4CABkRUyXzEE5WNkoUkvt3YfkxEM2E47gQXNchoKgSxBvf1aNoWynwEmzeaFwk62Re1JgKs5hmbNujBUhaF9d5ZY |

### Tous les receveurs des 76 ordres inter-chaînes

| receveur | chaîne | ordres | USD | premier | dernier | wallets |
|---|---|---|---|---|---|---|
| 0x2d86499a410a9ac2139833ba8d6942b8a8700a7b | 1 | 27 | 496371.59 | 2024-07-21 22:53:42 | 2025-06-09 20:19:03 | C73Yv9iHmTaf8SU2XFnGLt7QXUDqbeWNtUYza9WJhkae |
| 0xb947bf7f409e998b28f8e218802fc9575c3c8c57 | 1 | 4 | 263573.15 | 2024-07-22 00:54:36 | 2024-07-22 01:04:12 | Ei5yGz8dPndr1aCeHZsfqJBcS3VBbz75VHEhxxJKLy3V Gcyg2jeLfSY9gxxHf5za5QU74ijtxBb1dB2mdGSPZH3m HGBiExZRtD2TZdQLWHE9azkTSmE2z7ygKqZMtehJDKYU |
| 0xb29826d809aa04d2ead6f2310d8965a45b87fa67 | 1 | 8 | 151360.77 | 2024-07-16 09:05:01 | 2024-11-14 05:38:07 | Ei5yGz8dPndr1aCeHZsfqJBcS3VBbz75VHEhxxJKLy3V |
| 0x86f99097c563e84dd5190f3e85f6a2988f1c47a5 | 1 | 2 | 31228.81 | 2024-07-22 10:01:50 | 2024-07-23 00:04:54 | C73Yv9iHmTaf8SU2XFnGLt7QXUDqbeWNtUYza9WJhkae |
| 0xb29826d809aa04d2ead6f2310d8965a45b87fa67 | 8453 | 8 | 21217.5 | 2024-07-26 02:10:39 | 2024-11-26 03:06:54 | Ei5yGz8dPndr1aCeHZsfqJBcS3VBbz75VHEhxxJKLy3V HGBiExZRtD2TZdQLWHE9azkTSmE2z7ygKqZMtehJDKYU |
| 0xe2f040200a9b3af83fb40d3092613832a05e7647 | 8453 | 2 | 20462.51 | 2024-09-01 22:26:14 | 2024-09-01 22:28:39 | J2EuNwCSDfFGUhmpWdnoEgZKA17b4dgE9PQVY3jMFiQ3 |
| 0x703bf8c292b72efdd60243b17be782b58cd61ce0 | 42161 | 1 | 11211.9 | 2025-01-18 09:43:43 | 2025-01-18 09:43:43 | 7SEoKiBLaGhZxr5V8JYGdiV55ZhkgC727ftSYDST148i |
| 0xfb2ec4e51680198f4d0351d67702d4eebdfa625f | 56 | 2 | 9912.83 | 2025-03-20 20:38:25 | 2025-03-20 20:39:05 | 8YSi5yNRN2KMbGU7Q3i5w9W6fTRxnk1qatQ5YmzS5da7 |
| 0x2ac17414e34c9a1f70f6eadb6230fa503301e878 | 8453 | 2 | 5238.78 | 2024-11-26 05:19:21 | 2024-11-26 09:33:16 | Ei5yGz8dPndr1aCeHZsfqJBcS3VBbz75VHEhxxJKLy3V |
| 0xe8293b6bd3a4ac365257d11c71ed55cf1fb6bc27 | 1 | 1 | 2843.0 | 2024-08-21 01:41:30 | 2024-08-21 01:41:30 | EZXUvi4X5k3Aj99rGzNQoBtAzFqzYUjGhHNu8A1Ty8s4 |
| 0x21f3a0e26d33cb48e114c4f58019463cc79799fd | 8453 | 2 | 2415.59 | 2024-05-21 22:17:10 | 2024-05-25 20:20:40 | DfYyxDNEXBzZWVPuJrNfko1rDrtR8SiqWLeGUMmNn8DT |
| 0x93822e77a68835355279af1eb10164c1922cc448 | 1 | 1 | 634.18 | 2024-07-16 23:59:53 | 2024-07-16 23:59:53 | 5QhJJcFZu2ashyKyWSTGHcsyo6ZBCbpVuJqeutvQHScd |
| 0xe8e9b172f2b8cb77d8aad7ce5035abcb870b9035 | 8453 | 1 | 606.4 | 2024-05-07 18:57:51 | 2024-05-07 18:57:51 | DfYyxDNEXBzZWVPuJrNfko1rDrtR8SiqWLeGUMmNn8DT |
| 0x221c4998a69276545e63ccf451d52524266619b1 | 1 | 1 | 391.17 | 2024-06-17 23:38:59 | 2024-06-17 23:38:59 | EZXUvi4X5k3Aj99rGzNQoBtAzFqzYUjGhHNu8A1Ty8s4 |
| 0x08a5736fee0e30f6804d19910572bbdaeec672b8 | 8453 | 4 | 171.22 | 2024-05-26 04:37:03 | 2024-06-03 01:19:00 | C7i9beNHXYonZYB5riXE6kaLpFWLj9BPzh2FSBoUUePK |
| 0x921b31352a3cdc15f50ae831aa5bbfcb90b38b56 | 8453 | 2 | 161.73 | 2024-05-07 20:06:51 | 2024-05-07 20:08:16 | 74qFhHypY1zi8oS2KahqmwLfV8zMVbBiJ8uDdki8xPEb |
| 0xc7be71142998061600c7d75541554f6c5c4822cc | 8453 | 1 | 160.32 | 2024-05-07 20:15:25 | 2024-05-07 20:15:25 | 74qFhHypY1zi8oS2KahqmwLfV8zMVbBiJ8uDdki8xPEb |
| 0xae7f704743d56a61d1d4152dc2a915a76317b047 | 8453 | 1 | 152.77 | 2024-05-07 20:13:14 | 2024-05-07 20:13:14 | 74qFhHypY1zi8oS2KahqmwLfV8zMVbBiJ8uDdki8xPEb |
| 0xf1b0fb9828c0b8266704ab5bfd125be4a2395b72 | 8453 | 1 | 152.74 | 2024-05-07 20:10:18 | 2024-05-07 20:10:18 | 74qFhHypY1zi8oS2KahqmwLfV8zMVbBiJ8uDdki8xPEb |
| 0x059091a39be3516eecba8b873d91edb244c13060 | 8453 | 1 | 137.76 | 2024-05-07 20:11:39 | 2024-05-07 20:11:39 | 74qFhHypY1zi8oS2KahqmwLfV8zMVbBiJ8uDdki8xPEb |
| 0xbc411c5778ce68c957aab13e92df014fa35f6872 | 8453 | 1 | 137.52 | 2024-05-07 20:09:08 | 2024-05-07 20:09:08 | 74qFhHypY1zi8oS2KahqmwLfV8zMVbBiJ8uDdki8xPEb |
| 0xb805b3bf748bea7cd07bcf8868400c0dde61fe63 | 8453 | 1 | 107.36 | 2024-05-07 20:14:09 | 2024-05-07 20:14:09 | 74qFhHypY1zi8oS2KahqmwLfV8zMVbBiJ8uDdki8xPEb |
| 0x73df8d2907ca88de24bb469b0e647e6f08281909 | 137 | 2 | 37.59 | 2024-06-01 00:51:32 | 2024-06-01 00:52:36 | C7i9beNHXYonZYB5riXE6kaLpFWLj9BPzh2FSBoUUePK |

### Les trois ordres vers le receveur commun 0xb947

| UTC | wallet | USD | signature |
|---|---|---|---|
| 2024-07-22 01:04:12 | Ei5yGz8dPndr1aCeHZsfqJBcS3VBbz75VHEhxxJKLy3V | 47023.609816 | 4kW2yTLkXKzbb6i23StE6wswpcTr8oGNyVKa2ZBK2vTSi5nN9DXiX5YQShcjAP2LyEwNpEAFbQpRPCWEBvXCz8o8 |
| 2024-07-22 00:54:36 | Gcyg2jeLfSY9gxxHf5za5QU74ijtxBb1dB2mdGSPZH3m | 16.536704 | 3SrZnJG88Ja3GPKzW424pPMTPisjpNyCPKfSuDwyiF4DEbjk6K7Nq2nQA7cad19XUkZjHiTpLjrogQR58svwSmiY |
| 2024-07-22 00:57:18 | Gcyg2jeLfSY9gxxHf5za5QU74ijtxBb1dB2mdGSPZH3m | 60443.988481 | 7pHaeuMNtNPyQzVxT24yK8thFDn5cnHkK7X5L2KAvMoy1GqD1SdHoBqtH9jBU86gbmvpBHeJ5b8mzq3PUL4csWX |
| 2024-07-22 01:00:34 | HGBiExZRtD2TZdQLWHE9azkTSmE2z7ygKqZMtehJDKYU | 156089.016395 | 45PnZWjKkx7c1yeEx2rr1HFCggW5J5Pr1BFz9bkb8ScKf77SQiMEL4DocKcExRsQxFmmADWvyu1r55adNUdaPuC2 |

### Ordres DCA vendant DMAGA ouverts jusqu'au 22/07/2024

| ouverture | wallet | jetons | escrow | signature |
|---|---|---|---|---|
| 2024-07-15 15:52:16 | 4pKFTQxsc69nzioRwPuAwUm49MRP4KzBmvrfjRCpEe5g | 2000000.0 | 5w2evcxFzfUnCSJDRdwS3Z3Uu2DwtwjZ5NhwbQR3yeAS | 3pHR5fXim4ryaSkVaswQq9F7pUzb1jX32S1KiaK1ehuNHSF3TEM2VndNfbP27UdquBnQDETNbjB2q8Y5o621thxL |
| 2024-07-21 19:53:13 | Fp6kgqHUHFxdCVNRf1Z4bt4F1K5DK5Njq83PUNzUsGRt | 1423861.861594 | 5y6CwbRpbWBtXXVKWkUd7Rby5ksfg1AwknHk6ncH4SkG | kVYYDiVXcgxiq2J7z1iwTfF6ipFZ3iNEer5jDaBrioUMd3fTnLhArcAstv2EFpph2WN1nXVMxeXBaCozgX1iLJQ |
| 2024-07-21 21:21:17 | 5s3ogzsq8cvwHtS1B6MhwUUp9CyzugJ6y3WqLPM9Ee3C | 1322582.724444 | 2KWDPwxV1xck334ucPH8bJTeWrX3r2sjjympv6viAYcm | DZ5GHazgCs2ycg8Bj3tyTpN23WD1P57Sk2gs4WgNhUhY2ChKsBjSRn9xdQz6HepvbRauTquCtXUX6Koo3gmG5RD |
| 2024-07-21 21:38:25 | HqwpWyvbCbGSbGuK1xFRptPdMYd8MHERqNJ3uACRCAmZ | 1321860.66861 | CQkBiUn2XQVrnxhTgzptpTGL1duz6GD5tFejC9fCvVGH | 4eS5vZCgHpm2sCmqQWe9miQvdkkar3SiDLnCWW2PU8cwbE2brNLUDPQopeHFzyHM3YfPqawAgs5VTo9nkFcHdqk4 |
| 2024-07-21 22:07:30 | ERMtiLodeVKQ8sK1MBPgBHyJS6DT8j61z8aQJiKYqbCH | 254069.935959 | 5MTXWxtiGWz89cRtLhHqGY4Daf3GgqnJwwRQCJqYog9Y | 528JUCND1PtQtpBoNevzR2bxXo6gNcfriL9pi5APGUCttjjsHnP5kVFCfXVVg93x3ud9ZaBaFfDtWCv1Tf5arRkn |
| 2024-07-21 22:16:49 | EEpSRR12vTrH3Wbf3Ke4vT4RkMfPTqFv5wfE948cr3Wa | 2458311.527859 | 98UuAvDDcu1wE84APygjCWijKQGRP1Lga3FvFwpoJCuc | 4arWAn5YViLE5K8aJurTzZSRqeNSV3XXAVGv2yF57A2ftMnhXD7B4GSZ8rD2V22iDgdNVhByYD5H9DrS23oozLDR |

### Arêtes entre les 33 et le périmètre créateur citées

| UTC | source | destination | actif | montant | signature |
|---|---|---|---|---|---|
| 2024-06-11 23:49:10 | NxtXcmEW3gQvrCdBEm5GYT3zaqMre3QiPUhnwViNsD7 | 2VTfi1DKeDphzdSGhoobQYpW4N48fZAkS4BktPpdPU2Y | SOL | 1.331707438 | 4JKvDwWipZDNyEDbaNLmJKw63zSQwjpgDvP6SgQftByhjn6WCR4TVScjQT5XjV9WTzUgjwkJuFeLbWghbdx9JGV6 |
| 2024-07-15 23:42:03 | 7FGoCB63x3FAJNF25MMZG8pheR4rRtJbApQuynJRxLdE | B252jsFK2BKMfHRFzrHcxyVayPvC32h4ZXU8jmsm4Gsp | USDC | 748.728921 | 4HHGw5z2B9MmxqJoztPagnFheLizAjqpzghpKXiYnfMJqa1cLfjioMfqjSM4oPQepiTsdpWf7utXoxn6PLXNR8oC |
| 2024-09-29 07:48:23 | 4pKFTQxsc69nzioRwPuAwUm49MRP4KzBmvrfjRCpEe5g | 5QhJJcFZu2ashyKyWSTGHcsyo6ZBCbpVuJqeutvQHScd | DMAGA | 8000000.680308 | R2xR4gsDQZajT6XA637gWPS3DESfLy2utQ3xFaZxPxv1kn1Ec24QTkf2cKPvALEPKG8ddB4mbK7Fab4Rhajc1nU |
| 2024-09-29 07:49:12 | 6ty9DM4s2mNvsMpMrcaXBDVguFHapfwK9g7WdD9DBLgM | 5QhJJcFZu2ashyKyWSTGHcsyo6ZBCbpVuJqeutvQHScd | DMAGA | 4000000.723756 | 3o2ky1WF2TmHAGAFVvyFXo7WqcMzk2DL55xKDCYbpZRgRRzzY6JCCHEJQR5MLtCDcxTF78xthBYavM8gJ9BckyVa |
| 2024-09-29 07:49:50 | EEpSRR12vTrH3Wbf3Ke4vT4RkMfPTqFv5wfE948cr3Wa | 5QhJJcFZu2ashyKyWSTGHcsyo6ZBCbpVuJqeutvQHScd | DMAGA | 403234.99999 | 3QWMvA9bv4jkp9qyarGgBqz5jzGJs4QrFeLFVTvUpev7EhHHFw6PHxaLu1HvzmzKiw7jeCxyT9QHbUAFtnCBJpeU |
| 2024-09-29 07:50:15 | GoPCTrS3Ffz5wgWSP6Ef3U6NvZzJkUA3Qy8ZJ3rLMXHC | 5QhJJcFZu2ashyKyWSTGHcsyo6ZBCbpVuJqeutvQHScd | DMAGA | 3086392.444992 | 3X23XGd9rAwbWFPW9mq12gb7LNpiHjDta9Z1nPVkmVwSPq5WeQPiGECmpKFtT68dHZ2TZZagX1rL8YipAawbWkyk |
| 2024-09-29 07:50:35 | B252jsFK2BKMfHRFzrHcxyVayPvC32h4ZXU8jmsm4Gsp | 5QhJJcFZu2ashyKyWSTGHcsyo6ZBCbpVuJqeutvQHScd | DMAGA | 3674290.263992 | 2RkhRY5u9M66EWRTSMDmE5SnSy672xNAtFpeicRS4VZY4faWJFwr9jhxd3tAuinPuKYn5cKMvDL3APgcA9vdiNpX |
| 2024-09-29 07:51:01 | 9PoYaK2NZziWAswo5eNCaLbdqh6t28pq89qMnS5C3m5n | 5QhJJcFZu2ashyKyWSTGHcsyo6ZBCbpVuJqeutvQHScd | DMAGA | 1052393.722818 | 2JbfjkoCPqosD9PMzUhT3nbuCiVCBDrhzYGMdmJGXyXccUNTCVDWd4TC4U5xmGAsJQg1NsmmnEz916fe21FBpj9T |
| 2024-09-29 07:51:57 | 2k3AwMQcFL5bRe2e3i2LUEhf26n2XxUbmGbJQSCBmRDY | 5QhJJcFZu2ashyKyWSTGHcsyo6ZBCbpVuJqeutvQHScd | DMAGA | 1014609.704109 | 2diN7TB5FDDRPBcy8czp6e9C6DfDMkfo9cqZBjzZs7xG2rRTQ5cFGMyszLaQeaHiZw7McV6trXNvkMhyUP899pwJ |
| 2024-09-29 09:36:24 | 5QhJJcFZu2ashyKyWSTGHcsyo6ZBCbpVuJqeutvQHScd | D8syomxNoztm1v7kKzkHyDZiGNqtH3S1wnpMKZ2cRgmW | DMAGA | 10000000.0 | 4FBWB1uhLov498H5tvSqfyHvhymxA9ASu1dDMyyr9CjZhy6wyvr9TT1RD9n82sDcCU8h4jCCGfoCmbrCQHWXBqUP |
| 2024-09-29 09:37:55 | 5QhJJcFZu2ashyKyWSTGHcsyo6ZBCbpVuJqeutvQHScd | HQzyBQN8XVcGBRyAaRat96tkrfdzma9aLmesPiL8wqwA | DMAGA | 10000000.0 | 2e8rRWTcvPA7qY44m29UipQF9UmDX1Auk2PPnJmgXag6GeC4WbSMBpFdvy5QCUG6iNGX9Xsx5ajxiMZkqDKRwAMJ |
| 2024-09-29 09:39:23 | 5QhJJcFZu2ashyKyWSTGHcsyo6ZBCbpVuJqeutvQHScd | Cv3p9Wu1Ftib8Xm9vwWnR7d9tCYSMrHbFRLpT1pqQ5Cd | DMAGA | 10000000.0 | 4GGcrNtCMb57vKdaNeaPYBuLaDc4nmqRGRdtAjyvbvJs5jU48PfLpv5QFLtnqN2icYeVruFFKmpqrkTbnF1diYA2 |
| 2024-11-17 16:45:36 | NxtXcmEW3gQvrCdBEm5GYT3zaqMre3QiPUhnwViNsD7 | C7qEaB6aqkqRxW3BvVKiShjumPUNXRKR9pWYToNqD1QN | DMAGA | 1000000.0 | 3AoDymzTfy9ZEoRgkQiVKphTPvnqXMA2pLFFEncK3w1KDduNHMxWUhLr3RzKbpUjJ4pTZsvx76t2RMD6yveJ8vPQ |
| 2024-11-20 17:22:54 | NxtXcmEW3gQvrCdBEm5GYT3zaqMre3QiPUhnwViNsD7 | C7qEaB6aqkqRxW3BvVKiShjumPUNXRKR9pWYToNqD1QN | DMAGA | 1000000.0 | 4mL1Sso6PDnUYa8m4D2bkxfn8fHcmSk8ft9BN8r8DnNN2Ku9Q7emb7L3W6ndRwaGZ2q3Aahzy5Vg3bB2VobzSAr |

### Fusions citées, seuil 0,05 SOL, 5 USD, 100 000 jetons

| UTC | a | b | actif | montant | signature |
|---|---|---|---|---|---|
| 2024-06-11 23:49:10 | NxtXcmEW3gQvrCdBEm5GYT3zaqMre3QiPUhnwViNsD7 | 2VTfi1DKeDphzdSGhoobQYpW4N48fZAkS4BktPpdPU2Y | SOL | 1.3317 | 4JKvDwWipZDNyEDbaNLmJKw63zSQwjpgDvP6SgQftByhjn6WCR4TVScjQT5XjV9WTzUgjwkJuFeLbWghbdx9JGV6 |
| 2024-06-21 17:19:35 | 2VTfi1DKeDphzdSGhoobQYpW4N48fZAkS4BktPpdPU2Y | DfYyxDNEXBzZWVPuJrNfko1rDrtR8SiqWLeGUMmNn8DT | SOL | 0.78 | 5fa6uBWyXqchm3h2qYGRrPNJvPsLGgWw8ksbyorRXmxcCuYAyMAFmSejctaLGNfLQxJk3YrahrMmyuj5JLpGjUAN |
| 2024-07-14 02:40:26 | AtZjv3DuV9cLn3Jxm72TMSdTN4aM6CrBaGyxUC4c2wDk | NxtXcmEW3gQvrCdBEm5GYT3zaqMre3QiPUhnwViNsD7 | DMAGA | 130000.0 | 4mJtzuHKCtRzUUf9QFJodDAcXVNukSoLrdZu4GKGr3CzbF9pRiMaMSu93z3XrPKdZE7GPqVVzdfcoTTWkn2sUcnm |
| 2024-07-15 01:14:34 | NxtXcmEW3gQvrCdBEm5GYT3zaqMre3QiPUhnwViNsD7 | 5QhJJcFZu2ashyKyWSTGHcsyo6ZBCbpVuJqeutvQHScd | DMAGA | 8000000.0 | 2o4UXdGtAFqxWc9kGkLxfTFEyVX8vJDuebnk6eG7Umicp74VqVUpGwzZWXBeJeXds5SP52N6NRMYyxtEZbi6xd57 |
| 2024-07-15 23:41:49 | Fp6kgqHUHFxdCVNRf1Z4bt4F1K5DK5Njq83PUNzUsGRt | B252jsFK2BKMfHRFzrHcxyVayPvC32h4ZXU8jmsm4Gsp | USDC | 365.7847 | 2WeozFreYMhA928mkWaU2Q1UUg1uucohd9CcWPfL5aoTjsWGRT2RfD33FnW3cLwQuX82kPK5xHKnL77tgFbYMach |
| 2024-07-15 23:42:03 | 7FGoCB63x3FAJNF25MMZG8pheR4rRtJbApQuynJRxLdE | B252jsFK2BKMfHRFzrHcxyVayPvC32h4ZXU8jmsm4Gsp | USDC | 748.7289 | 4HHGw5z2B9MmxqJoztPagnFheLizAjqpzghpKXiYnfMJqa1cLfjioMfqjSM4oPQepiTsdpWf7utXoxn6PLXNR8oC |
| 2024-07-18 23:12:43 | 4wComYHQbydc9DZHsDu3t2MaTLNe7Y3ukdymrkqh9ftC | 74qFhHypY1zi8oS2KahqmwLfV8zMVbBiJ8uDdki8xPEb | DMAGA | 15000000.0 | 1X9w8xLDu39Ti9TjHsJud4AMzcfFjso5KBo1WRrLoKep1PwZfQnrRuUL7hnR2QPn3SfngjKuLeqK3pKCP2o273G |

### Transferts de la série vers HW5MqvM1 et HKzkNSH2

| UTC | jetons | signature |
|---|---|---|
| 2024-07-15 18:39:06 | 1500000.0 | 4HEH3WcanD16CFvbym5NwzxojkgmfpshSXMa3MEsmamaTYc4M9b8hwdsegGvtUBXQhhY5QC5tmbMZJsP7L4R9C1c |
| 2024-07-21 23:00:23 | 1000000.0 | 2bHLM1r9t7YAih6rp2QQ8V7Kk4sXYFxGMqfSByj6aHr7KP8wawojaDNDRTLxbVa4rqt9HQCHpS1dbzK3aKERT4uZ |

### Programme 3GMsedVP : déploiement et fermeture

| UTC | signataire | signature |
|---|---|---|
| 2024-07-13 14:14:06 | FyC5nr3WJAir6cntnwwQRuurq4JUCWvsH2VS5p4vYZ8k | 39VeLqqgaucVNCFLznaLH5RfrHmUcX6waPuZAmXq39yi3phd7fAvtsmPBVUxazaejH8p5pdHZ9M8XAkWzLGRGRYq |
| 2024-10-10 07:42:08 | FyC5nr3WJAir6cntnwwQRuurq4JUCWvsH2VS5p4vYZ8k | 3pENHTDXXS7GKi6W6U8pzSjKGN4mepP3aeDoqq6wwTCggzJVrzCEQyHw9ooiWCXFWGbjBD7X2qPzNyHwZdVFNxCa |

### Exemple de bloc du programme : jambe, propriétaire, slot, index, jetons, SOL

| signature | propriétaire | slot | index | jetons | SOL |
|---|---|---|---|---|---|
| 28hD6bSnbyhZPqXSXsavq7gGsU2iTECmmd8SFfwUXaPdPLuLTuExeEXe7TtMU1YpuUXHzwhrxxZhbSC1fKthjaXf | 4AVe3VMDWnfwxo3Ydi4N8m411TvPwe3BjXmPnRg4GU4a | 289361337 | 351 | 12108788.527231 | -623.427113362 |
| 5au4mKnXzBtp64qHbD1bJvNaqPYko38F8Mp7J7D7cwcobW6KdP9sXtvjai1r6xEnMe4eHFGeNEbrKvXv8gAVgZbW | 4AVe3VMDWnfwxo3Ydi4N8m411TvPwe3BjXmPnRg4GU4a | 289361337 | 353 | -12108788.527231 | 623.462848329 |

### Le tiers intercalé du même bloc

| signature | propriétaire | index | jetons | SOL |
|---|---|---|---|---|
| 2rtRvNXEB64KaXgwxwK8jw7KLccg8bhNGKQ6JEBunokQzFD8AKngqVgKt5f66BRwsHcekVxQC6CV1JWyiY436WqK | 5vzA6PjBFnAimFFQiFLag7iz1JyTgrHamajZZC8hekhy | 352 | 79936.014769 | -5.841691828 |

### DMAGA reçus par H9Xezqfd

| UTC | source | destination | jetons | signature |
|---|---|---|---|---|
| 2025-12-03 15:44:00 | EGzN5GfcyLdqXP21AeLevwnitSgLXBbET4B6NxZfvdZM | H9XezqfdXuv4ZCHAAZ92oMLSSAPB6Dgm4ZSrRythCbPi | 2500000.0 | 4xuF8r2ZU7ncZ6CfcVKxvAehRagzvnZ7hSFXBHrKSXz4BXRwcie8mF1A8eetgW9EgThfhEdJA2Ya6k9gZ7JhLSc5 |

### Premiers financeurs, dans l'ordre G41vRrsH, 74qFhHyp, AtZjv3Du, NxtXcmEW, GFpqfjEQ

| UTC | financeur | étiquette | SOL | signature |
|---|---|---|---|---|
| 2023-12-26 17:17:02 | ASTyfSima4LLAdDgoFGkgqoKowG1LZFDr9fAQrg7iaJZ | MEXC 1 | 3.97 | 3BRXqbdMivoxordf9XkfWotkA3cTU7hausrP4twYFrpaGinyGGa8kqVCAV6NwyQHCD2cdaDtyR764GoiC5Sxbjrj |
| 2024-03-11 23:00:55 | 45i7PmS9TvZAsrDjJY5sGo6ATiD8aPi2jCxCyaGMVTHy | None | 0.13 | 45iPEm8cdYi3m4Ho4iEN731MHs4gpuSZXaYjVyd6zJ6iwgzuJ3Tr9ejtk5F8pm4urfnU1wQfsX38hcWynCSAfago |
| 2024-06-05 10:13:44 | 74qFhHypY1zi8oS2KahqmwLfV8zMVbBiJ8uDdki8xPEb | None | 0.01 | 28AmwGWw8ziizsFUAUxmdG7o3mZX7jnCJjwjfqF2dxxuTa3sjbVP4Wv7Mg2q2ESLbm4xEpYYtZrYnPvHZo9mPKSd |
| 2024-03-26 00:37:02 | ASTyfSima4LLAdDgoFGkgqoKowG1LZFDr9fAQrg7iaJZ | MEXC 1 | 1.36 | 2sVqDmXywVbcN4c9vHwkkkLGSEm4htnq9VjrA2Ukr5iTAj5baXxH4a8CmSVdBhAhjBvQRayy1XEaxa6XWYdasF34 |
| 2024-04-10 17:02:43 | NxtXcmEW3gQvrCdBEm5GYT3zaqMre3QiPUhnwViNsD7 | None | 1.0 | 2PZpeHJCpqgoaDjdVphfanCvrXAjD94Pv3mjHx8hktNNXM3JEEqfMLfNTd3N7cv4BSHYXbi4YE94fyJceVnEyD1Z |

### Préfixes cités et adresses complètes

| préfixe | adresse |
|---|---|
| 0x2d86499a | 0x2d86499a410a9ac2139833ba8d6942b8a8700a7b |
| 0xb947bf7f | 0xb947bf7f409e998b28f8e218802fc9575c3c8c57 |
| 0xfb2ec4e5 | 0xfb2ec4e51680198f4d0351d67702d4eebdfa625f |
| 23vEM5NA | 23vEM5NAmK68uBHFM52nfNtZn7CgpHDSmAGWebsjg5ft |
| 25WYn7Jr | 25WYn7JrXy4EnsX3nvWTc4fUET1beY2jp6CeJCVW7NoT |
| 2BLSXbea | 2BLSXbea4abffYCbs6pkCvPDChe9D4VNsfxJTAauQZPT |
| 2VTfi1DK | 2VTfi1DKeDphzdSGhoobQYpW4N48fZAkS4BktPpdPU2Y |
| 2mW45kXp | 2mW45kXp4Wd4xRkF2mmh5rKdzjnjbJR2o53skWcxGa2d |
| 33RuC2ig | 33RuC2ig9ZtdDUHj9YWs3Qbi2pSqQGd4dxs7NuNGemZw |
| 3GMsedVP | 3GMsedVPsXjWR7HYUvwm1YUpvBC2bTgSkXixm4gMXnPk |
| 42MSVeV4 | 42MSVeV4YbESE7mNW7DfQrfd8E4RG6njxXZLAWTmXemv |
| 42mepa9x | 42mepa9xLCtuerAEnnDY43KLRN5dgkrkKvoCT6nDZsyj |
| 45i7PmS9 | 45i7PmS9TvZAsrDjJY5sGo6ATiD8aPi2jCxCyaGMVTHy |
| 4EishudC | 4EishudCwVJaoy6tvrxDvUGkHFa5EXSTVYbP9VnfrWi7 |
| 4ToQp55m | 4ToQp55myvfpeprgKuqGbDqyji9Ezm7CZg7QbcTpL33S |
| 4Tqy4SPN | 4Tqy4SPNJjD1RPPqqiyf7faReBXF5XqesoTchZn1e9DF |
| 4aJ4oko7 | 4aJ4oko7JKQnCAc76FwfjRcWskUZDzRc7wDyD8LMV6bp |
| 4upmFYy6 | 4upmFYy6SpmCwdSRfG9akN2gRRn3DksLpDyN5YAmohbx |
| 4wComYHQ | 4wComYHQbydc9DZHsDu3t2MaTLNe7Y3ukdymrkqh9ftC |
| 59L2oxym | 59L2oxymiQQ9Hvhh92nt8Y7nDYjsauFkdb3SybdnsG6h |
| 5QbApAqu | 5QbApAquHTJ2waLG2VXNctdF1a1QUvsmwTHew4pmnwG5 |
| 5QhJJcFZ | 5QhJJcFZu2ashyKyWSTGHcsyo6ZBCbpVuJqeutvQHScd |
| 5ndLnEYq | 5ndLnEYqSFiA5yUFHo6LVZ1eWc6Rhh11K5CfJNkoHEPs |
| 5vgqBABn | 5vgqBABnvmNGzsFgRUAhaKTKvyvm3hCK2hCrYYRFStqZ |
| 6d8vRyKP | 6d8vRyKP3CsWgFdAa9yLmbDPAJKJww3hieKZo1gy7gJi |
| 6hXrioEs | 6hXrioEsSShDPJ6fFzA9YUErimddZUVWYvwiwbffgZLW |
| 6t2dz4jm | 6t2dz4jm3S8vJZCkWPhBxHStxFTC8wNV9QttTzfQrG7M |
| 72Pgt5Mr | 72Pgt5MregKZXqkJcYUVvf1vJBH7xun3L3SQfRUBba5Y |
| 74qFhHyp | 74qFhHypY1zi8oS2KahqmwLfV8zMVbBiJ8uDdki8xPEb |
| 7D7BRcBY | 7D7BRcBYepfi77vxySapmeqRNN1wsBBxnFPJGbH5pump |
| 7FGoCB63 | 7FGoCB63x3FAJNF25MMZG8pheR4rRtJbApQuynJRxLdE |
| 7SEoKiBL | 7SEoKiBLaGhZxr5V8JYGdiV55ZhkgC727ftSYDST148i |
| 7TQBJhqb | 7TQBJhqbhGFsKdgGuXsFAU4mHDm2zxsXz8YTb7EAo4Tv |
| 7VtkbUQm | 7VtkbUQmUjxKvRScwQi1MnVr3Vrs96LEixA76LAxZ6gk |
| 7mdCAs8C | 7mdCAs8CWYJxkWz2gfj3sRhDBmUi6Q9qvRGuKiv2Bazu |
| 7oFfdxSk | 7oFfdxSkLazHFBZz1MMbmZUyBvGQMvjmSijGB8HJcWp |
| 7rMagzrQ | 7rMagzrQ4vCvA4QdZp1MBW1P63g8z4s3xYAAP2wLmjcL |
| 7zycfr97 | 7zycfr97z815o7Bo9MWN47WJR8yv5WF1FcVGj3jL6pK7 |
| 83v8iPyZ | 83v8iPyZihDEjDdY8RdZddyZNyUtXngz69Lgo9Kt5d6d |
| 8B5ekuLt | 8B5ekuLtBXypSiGq8xugLtk5UHq4JiW2U3haYJPi3u7p |
| 8N4AvP9j | 8N4AvP9j5BditSQMk2WrTNxthhgpncGVzLKrYP4xdEqx |
| 8SaiGWJn | 8SaiGWJnpcMNbnqa84op76MuRVkJPx4uZN77mZDb9g5F |
| 8YLEuUtZ | 8YLEuUtZ4eFMJbf46oNb1CeG6dYFWGyxnQSh9hrgzBzR |
| 8YSi5yNR | 8YSi5yNRN2KMbGU7Q3i5w9W6fTRxnk1qatQ5YmzS5da7 |
| 8xjM4fGg | 8xjM4fGgPCqY4okN8Dsj4FXSPDp19d3sJYuTVGs2jkUv |
| 94Q76Saa | 94Q76SaacQsrCKViUi8vRHR8z6a3AXvnf2CmEs8dgmYK |
| 94xmX5J9 | 94xmX5J92nZLanLvRstmxhgiS8kN8SVfFQ2zPKYB3Ynb |
| 9FTWDMJz | 9FTWDMJzzt3kt8tRoHBQRATwSdx9uMTwrumm4YMd8bjE |
| 9PrmF8sf | 9PrmF8sfoD2YShtWUghrGEYgxwabpnzog8gT1V6LEtdq |
| 9W9b3zgH | 9W9b3zgHH9mCEHDhsdbnbEPHStm9vvXS4aia4DWHBxpL |
| 9kqTVnRU | 9kqTVnRUkVTFD7na9BTWcoG9piL4XpVTtS9kqVCV56tV |
| 9yMwSPk9 | 9yMwSPk9mrXSN7yDHUuZurAh1sjbJsfpUqjZ7SvVtdco |
| 9yj3zvLS | 9yj3zvLS3fDMqi1F8zhkaWfq8TZpZWHe6cz1Sgt7djXf |
| A3EQhVTu | A3EQhVTu5Bzsc2EXU5aDGTBv6AuByh7pq4PcsSpPWhLE |
| A52fNskQ | A52fNskQkLPD6oBdXFwznrmrT52jNdgvh2MCRWGqaiCW |
| A7JYFhNe | A7JYFhNeHWXAJA6utQSdCmnXfJuW8Vb2S7YkKU18amF5 |
| ADnZ9NdL | ADnZ9NdL9rHg7CL6CnAjEhPTuLsJnvLXrY9kbkhML5Ft |
| AGG2Fsrp | AGG2FsrpP4wN6hjptovXH3sykfdMt6ESADJGLxMYKcJZ |
| AQVgyg8P | AQVgyg8P5Yh5YcAqAMQRRGzDegy1R58gN4Qh87QsJAF1 |
| ASWgowZA | ASWgowZA74nBJM4UGZk7eAKnGqp2kvi5jzT7zwkrxj4W |
| AVUCZyuT | AVUCZyuT35YSuj4RH7fwiyPu82Djn2Hfg7y2ND2XcnZH |
| AYtWa3rL | AYtWa3rLenfXkZJ4U9LjcRMP1qX8iTfRqwRk2DZzcLc2 |
| Akp46Dic | Akp46DicpTMb9aDtZozTViYydsYH5NhcZACWokpzLaNB |
| AtZjv3Du | AtZjv3DuV9cLn3Jxm72TMSdTN4aM6CrBaGyxUC4c2wDk |
| AverrTRT | AverrTRTKkP8SH4LHCiRKyvEMHoJGyCpkG1Bk2RJQYSp |
| B1KEP1nu | B1KEP1nunxUGrCoWZPZzoFJZ2wvLAXuVyNQrycYKRJ91 |
| B252jsFK | B252jsFK2BKMfHRFzrHcxyVayPvC32h4ZXU8jmsm4Gsp |
| BZ2UcCuj | BZ2UcCujoCr4XYZE2s23xTWYJMgiFSQoYopYrr1B2QmA |
| BrdgN2RP | BrdgN2RPzEMWF96ZbnnJaUtQDQx7VRXYaHHbYCBvceWB |
| BuBXTWEC | BuBXTWECG8Xk6wMgyvrK6LQdJBk1exhDaSqNa9nFnjx3 |
| BuHUkjUy | BuHUkjUyWGTwz1suyWpqY6ZcYLX9rbfRsT5nnHFGXykc |
| By6Dao4Q | By6Dao4QMNeBxmdUrqsoQA8dCGbHz7xWj57CdHV5M47r |
| C73Yv9iH | C73Yv9iHmTaf8SU2XFnGLt7QXUDqbeWNtUYza9WJhkae |
| C7qEaB6a | C7qEaB6aqkqRxW3BvVKiShjumPUNXRKR9pWYToNqD1QN |
| CZsBW8yC | CZsBW8yCGAiWwQ16VAokXE7h7qYL8spMA582X7F7g2jW |
| Caw4Rrwk | Caw4RrwkmxqtbLSFzgSs6id3XiFxWQxs2t1mrn5a3mME |
| Co3zTr2M | Co3zTr2M8huMY5os2wuvKGP4x3S3q4D9fzAoMZeGSMbb |
| Cv3p9Wu1 | Cv3p9Wu1Ftib8Xm9vwWnR7d9tCYSMrHbFRLpT1pqQ5Cd |
| D8syomxN | D8syomxNoztm1v7kKzkHyDZiGNqtH3S1wnpMKZ2cRgmW |
| DEuwaZcb | DEuwaZcbpdop5jbSKCHngkzYSqnjwpd2GQmBVXbKqCyG |
| DYH5edZK | DYH5edZKxWPnDZLyvkct5bachAu1NH7utb5GoYwqK9DM |
| DfYyxDNE | DfYyxDNEXBzZWVPuJrNfko1rDrtR8SiqWLeGUMmNn8DT |
| E1wDwfkh | E1wDwfkh1ySipYTgqx6DtCQrri2L8KCwzECC3arUMXyK |
| EGtyQEgM | EGtyQEgMKGKXjppDqj9sYy97e9m7nvu1US4SfFXNakMy |
| EGzN5Gfc | EGzN5GfcyLdqXP21AeLevwnitSgLXBbET4B6NxZfvdZM |
| ENvLw1g1 | ENvLw1g1cpeumqm6B8t5PZueEUiqTpa7q4Me85x9rSuH |
| ERMtiLod | ERMtiLodeVKQ8sK1MBPgBHyJS6DT8j61z8aQJiKYqbCH |
| ERm6ztBi | ERm6ztBisNcxRYyaxzbxKbj7XZ7Aj2MfqoWeUytTwkjg |
| ET7a91Ee | ET7a91EepfVmKgFdHA6vrxgb1LZtjfKK13ZxCJFgQ98E |
| EZXUvi4X | EZXUvi4X5k3Aj99rGzNQoBtAzFqzYUjGhHNu8A1Ty8s4 |
| Ei5yGz8d | Ei5yGz8dPndr1aCeHZsfqJBcS3VBbz75VHEhxxJKLy3V |
| Ej5Qv3UB | Ej5Qv3UBQYTuX1dnJ5Fvgx8H9JUSZ6zWgqyDhPzPCwgA |
| FB8241Dx | FB8241Dxskd2CiSsNC3aB6gsSMPmsxpJKwJRaUj4G2o5 |
| FJ9LmErk | FJ9LmErkELZr96VKkUEMFXN1vX4XtEVPH59rTT39UE13 |
| FLiPggWY | FLiPggWYQyKVTULFWMQjAk26JfK5XRCajfyTmD5weaZ7 |
| Fbyt3nao | Fbyt3naoJnA6hCBDMk6LFN2TPzU2wQo6svE6noXPXktr |
| FeompFnD | FeompFnDtr7NY2jiF9Rp8PTxZmbNCT1QDuNYAopcPmZU |
| FjuV7mJU | FjuV7mJUyjMbDg41RybRRrTJu8UTPK6suURavt6ZRBkV |
| Fp6kgqHU | Fp6kgqHUHFxdCVNRf1Z4bt4F1K5DK5Njq83PUNzUsGRt |
| FyC5nr3W | FyC5nr3WJAir6cntnwwQRuurq4JUCWvsH2VS5p4vYZ8k |
| G41vRrsH | G41vRrsHShLEvwMj58ruhqJycGfAtWXxtLD56uFExL8E |
| GFpqfjEQ | GFpqfjEQFhXRbWEJCwUqKuNjSNTCgqAsANMbVyTGmi1p |
| GMgh4NtW | GMgh4NtWrGaUf1RR2kcXD7LY1jou1qFAuSsQeKp5ow4a |
| GXZvXsD6 | GXZvXsD6hxaLeFvQisWpdAwsayJxga7w9EeafhFZG2Ra |
| Gcyg2jeL | Gcyg2jeLfSY9gxxHf5za5QU74ijtxBb1dB2mdGSPZH3m |
| GoPCTrS3 | GoPCTrS3Ffz5wgWSP6Ef3U6NvZzJkUA3Qy8ZJ3rLMXHC |
| H3QsBrri | H3QsBrrivimFJmSpTXuvig2n1Bh7JuYxrriRSEszT6cc |
| H4TnZyc9 | H4TnZyc95YNU23F9Mv5fMf85VB1oeuCXrXJSuB1WCnCc |
| H9Xezqfd | H9XezqfdXuv4ZCHAAZ92oMLSSAPB6Dgm4ZSrRythCbPi |
| HGBiExZR | HGBiExZRtD2TZdQLWHE9azkTSmE2z7ygKqZMtehJDKYU |
| HKXb8Lfy | HKXb8LfyzxYUgL1hhP8gtnXMCPnbJm6vNWMbVsmvy6WV |
| HKzkNSH2 | HKzkNSH2DmfyowntFnoa1xdUuVH4Yh6bg7z8fer4JSRP |
| HQzyBQN8 | HQzyBQN8XVcGBRyAaRat96tkrfdzma9aLmesPiL8wqwA |
| HW5MqvM1 | HW5MqvM1kDySFUtynMtzsWCU6VcFfpeCXsbRyLq6iHk6 |
| Habp5bnc | Habp5bncMSsBC3vkChyebepym5dcTNRYeg2LVG464E96 |
| Hiz7GLUw | Hiz7GLUwrjnyQ6VyKnZQv94v1RKVkFK3TBLFBtocMgEG |
| HkFSNPjN | HkFSNPjNFUVtdykP8kSyWCKhocY85k1S4MyjXHNqesvv |
| HkrGvxap | HkrGvxapoqp6625TKs8v8tEyu6eDwuPxmPinRaGH6i4a |
| HqwpWyvb | HqwpWyvbCbGSbGuK1xFRptPdMYd8MHERqNJ3uACRCAmZ |
| J2EuNwCS | J2EuNwCSDfFGUhmpWdnoEgZKA17b4dgE9PQVY3jMFiQ3 |
| NxtXcmEW | NxtXcmEW3gQvrCdBEm5GYT3zaqMre3QiPUhnwViNsD7 |
| RBHdGVfD | RBHdGVfDfMjfU6iUfCb1LczMJcQLx7hGnxbzRsoDNvx |
| RBsneDCL | RBsneDCLZHmbTd3iuNyF2bJkiAoap2yiLuPQSkcAmaz |
| nbL5GccM | nbL5GccMxEgEJECJ5C4SqhLWuyXW2GbW13ctLF9JXGQ |
| rzCo83Ve | rzCo83Vef2toNrm2qepxRGFz7Shk6F2N4NE4oZjcsJz |
| src5qyZH | src5qyZHqTqecJV4aY6Cb6zDZLMDzrDKKezs22MPHr4 |
