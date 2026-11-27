# Frontières des flux, enquête Dark MAGA

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

{{TABLE_FRONTIERES}}

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
