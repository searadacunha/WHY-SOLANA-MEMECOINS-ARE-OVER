# Relecture adverse des constats G et X, enquête Dark MAGA

Agent I, 03/11/2026. Branche `audit-2026-11-03`. Jeton `7D7BRcBYepfi77vxySapmeqRNN1wsBBxnFPJGbH5pump`. Personne n'est accusé. Aucune identité civile n'est présumée. Un nom ENS public cité ici n'est pas une identité.

Méthode : parseur propre `i_lib.py`, écrit sans lire `g_lib.py`, sur les réponses brutes de `audits_work/C/net`, `audits_work/G/net`, `raw/flows`, `raw/full_*`, `raw/grp`, et sur les preuves de `work_E`. Tout chiffre vient d'un script gardé dans `work_I/`, sa sortie porte le même numéro. Autocontrôle des adresses et signatures : `i99_selfcheck.py`.

## Verdict global

**Aucun constat central ne tombe. Les liens et les flux tiennent sur le brut. Plusieurs phrases et chiffres sont faux ou mal placés, et une jonction a été manquée.**

Ce qui doit changer avant publication :
1. **G3 : 113,37 M n'est pas vendu.** C'est le total déposé dans les ordres. 64,63 M ont été rendus aux wallets. Vendu : 48,57 M.
2. **G3 : 1 292,4 SOL éq. oublie le SOL natif.** Total : 1 505,5 SOL éq. Et « rien avant » 19:30:13 est faux : 8,64 SOL.
3. **G3 : le test de permutation ne porte pas sur la séance du 26/01/2025.** Aucun des 8 wallets n'a son écart ce jour-là. Un test entre wallets différents soutient la séance, il faut citer celui-là.
4. **G8 : la « marge » de 9,44 SOL n'est pas une marge.** Elle part presque entière en pourboires. « Net de jetons nul » est faux pour le trésor : +3,05 M. Le mot sandwich reste mérité.
5. **G6 : une jonction manque**, par `7Gw3gL8m`, entre un wallet de la salve du 23/07, deux wallets de P1 et le gagnant n° 11, `9cfRU5RK`. Niveau C.
6. **G4 : l'exécution n'est plus « non vérifiée ».** 41 ordres sur 76, 92,5 % des USD, sont retrouvés au wei près sur Ethereum. Un 5e versement de 120 957,89 USDC vers `0xb947bf7f` n'a pas d'ordre connu.
7. **X : « contredit par toutes les dates objectives » dépasse les preuves.** Contredit pour le jeton, non tranché pour une préparation.
8. **Test `etude_groupe` : la lecture doit être nuancée.** Les services n'expliquent rien, mais la fenêtre compte : à fenêtre égale, 3 pairs sur 48 atteignent DMAGA, et non 6 ou 8.

| N° | Statut | Niveau proposé | Niveau mérité |
|---|---|---|---|
| G1 | CONFIRMÉ, témoin à réécrire | A, B, B pour même opérateur ou compte, C pour même bénéficiaire | Identique |
| G2 | CONFIRMÉ, portée de « tous » à limiter | A, B, B | Identique |
| G3 | CONFIRMÉ EN PARTIE, 3 chiffres et 1 test à corriger | A, B, B | Identique après correction |
| G4 | CONFIRMÉ, renforcé | A pour l'ordre, B | A aussi pour l'exécution de 41 ordres |
| G5 | CONFIRMÉ, renforcé | A, B, B | B, et lien EVM depuis 2022 |
| Table section 6 | CONFIRMÉE pour l'arithmétique, libellés à corriger | | |
| G6 | CONFIRMÉ EN PARTIE, jonction manquée | B dans chaque grappe | « Chaque grappe a sa sortie » à retirer |
| G7 | CONFIRMÉ | C | C, pas plus, « donnent » à remplacer |
| G8 | CONFIRMÉ EN PARTIE, marge fausse | A pour la forme, B pour le mot | Identique |
| `9PrmF8` et `H9Xezqfd` | CONFIRMÉ EN PARTIE, autre population | B, C | B, C, raisonnement différent de `9W9b` |
| X, posts et images | CONFIRMÉ | A | A |
| X, « deux jours avant Butler » | CONFIRMÉ EN PARTIE | D, contredit | A pour le jeton, non tranché pour le reste |
| Test `etude_groupe` | Recalcul CONFIRMÉ, lecture CONFIRMÉE EN PARTIE | | Verdict gelé inchangé |

## 1. G1, second dépôt

**Statut : CONFIRMÉ. Niveau mérité : celui proposé.**

**Faits refaits (`i01_summary.txt`, `i02_overlap.txt`).**
- `Caw4RrwkmxqtbLSFzgSs6id3XiFxWQxs2t1mrn5a3mME` : entrée 590 933,959267 USDC, sortie 590 933,959267 USDC. L'égalité exacte montre que l'historique USDC est complet.
- 35,627018 SOL en entrée, 85 tx signées, uniquement des virements et le budget de calcul.
- Sorties étiquetées : 329 553,64 USDC, 55,8 %. Le plus gros destinataire, `9obNtb5GyUegcs3a1CbBkLuc5hEWynWfJC6gjz5uWQkE`, 215 403,08 USDC, reste « famille présumée ».
- Expéditeurs : 48 et 55, communs 27. Ce dernier chiffre dépend du seuil, sans s'effondrer :

| Seuil sur la somme | `9W9b` | `Caw4` | Communs |
|---|---|---|---|
| Aucun | 83 | 120 | 38, dont poussière |
| 0,01 SOL, 1 USD | 48 | 55 | 27 |
| 0,05 SOL, 5 USD | 46 | 54 | 25 |
| 1 SOL, 100 USD | 38 | 54 | 22 |
| 5 SOL, 500 USD | 31 | 52 | 19 |

- Poids des 27 : 678,18 SOL sur 956,52, soit 70,9 %, et 420 561,50 USDC sur 590 933,95, soit 71,2 %. G ne donne pas ce poids, il vaut mieux que le compte.
- Des 55, retirer `59L2oxymiQQ9Hvhh92nt8Y7nDYjsauFkdb3SybdnsG6h`, que G écarte lui-même comme gaz de plate-forme. Le montant exact 8 640 880 lamports revient bien 3 fois chez les témoins (`i72.txt`). `5NmoD59DK5BvkCGsKVRq2xs9VN5s33TS4sr2sRazJsqg` entre par un programme tiers (`E4CKSsnjU9WXzrBJpNXnFi4gbb1kmLuavwZHd35TLeHs`) et un autre signataire, 4 tx en 2026, 1 130,84 USDC : à ne pas compter comme virement direct. Écrire 54 expéditeurs, dont un par programme.

**Le témoin « au plus 4 sur 7 140 » (`i03_ctrl.txt`).** Il est bien biaisé, mais son biais ne renverse pas le résultat.
- Le dénominateur est trompeur. Médiane de 4 expéditeurs par dépôt témoin. Seules 91 paires sur 7 140 peuvent atteindre 27 communs, et 1 485 peuvent atteindre 5.
- La bonne comparaison : 153 paires avec au moins 20 expéditeurs de chaque côté, maximum 2 communs, coefficient recouvrement/plus petit côté au plus 0,071. Ici 27/48 = 0,562.
- 40 témoins sur 120 sont coupés à 3 pages. Cela baisse le recouvrement témoin.
- **Il n'existe aucun témoin SOL contre USDC.** Seuls 9 témoins ont un expéditeur USDC, jamais plus d'un. La limite écrite par G est juste, le mot « témoin » ne couvre pas ce croisement.
- Le témoin compare des comptes tirés au hasard. Il dit que deux inconnus ne partagent pas de wallets. Il ne teste ni un trésorier, ni un OTC.

**Alternatives.**
- Trésorier ou compte tenu pour plusieurs personnes : reste possible. Le niveau C pour un même bénéficiaire est juste.
- OTC : un guichet aurait des clients sans lien entre eux. La séance du 26/01/2025 va contre, 22 versements de 22 wallets, un à la fois, 29 à 119 s d'écart dans chaque lot, USDC et SOL mêlés (`i72.txt`). Cela parle d'une main qui tient les clés, pas du bénéficiaire. Non exclu pour le reste de la période.
- Service de paie : un tel service distribue, ici tout converge. Peu plausible, non exclu.
- Hypothèse non vérifiée, à ne pas écrire comme un fait : Coinbase pourrait donner une adresse par actif. `9W9b` ne reçoit que du SOL, `Caw4` presque que de l'USDC. Cela expliquerait la paire pour un seul compte. La documentation de Coinbase n'a pas été lue.

**Correctif de texte.** Remplacer « Témoin, 7 140 paires de dépôts : maximum 4, aucune paire à 5 ou plus » par : « Témoin SOL contre SOL, 120 dépôts tirés au hasard, 3 pages : sur les 153 paires d'au moins 20 expéditeurs de chaque côté, maximum 2 communs. Aucun témoin SOL contre USDC n'existe. Les 27 communs portent 71 % des montants de chaque dépôt. »

## 2. G2, 14 sur 2 201

**Statut : CONFIRMÉ. Niveau mérité : celui proposé.**

**Comptage sans aucun filtre (`i05_g2.txt`).** Avec tous les expéditeurs bruts, 83 et 120, poussière comprise : 13 vers `9W9b`, 10 vers `Caw4`, 9 aux deux, 14 en tout. Aucun ajout. Tous entre 01:32:23 et 01:40:50.

**Contrôle brut.** Les 14 retraits existent dans l'historique de chaque wallet. Pour les 14, c'est la toute première transaction. Dans ces 507 s : 202 retraits vers 198 destinataires, pour une moyenne attendue de 176 retraits. Les 14 sont donc 7 % de la fenêtre.

**Entrée de `Fp6kgqHU`.** Le wallet est dans la série depuis C, avant la découverte de `Caw4` : il n'est pas choisi après coup. Il verse 0 SOL à `9W9b`, et 27 704,40 puis 62,40 USDC à `Caw4`. C'est le dépôt qui est choisi après coup : `Caw4` est retenu parce que la série y verse. La fenêtre de 2 h aussi, C le dit. Le chiffre 14 n'est donc pas une prédiction, mais l'écart est trop fort pour que cela change la lecture.

**Limite de « tous ».** « Tous dans les 507 s » vaut seulement pour la fenêtre de 2 h. Parmi les 76 expéditeurs, 26 ont pour premier financeur connu un des 3 hot wallets étiquetés, 25 hors `59L2oxym`, et 3 autres la famille présumée. 11 d'entre eux sont hors de la série.

**Le même geste revient à d'autres dates, G ne le dit pas.**
- 26/06/2024, 18 jours avant le mint : `9z697N4uVjBmSt6jL5kWAcuVdzQWGRb3k5HyJVw91J7S`, `FhTm6Rz9tMgvxaiDKcgTsmzsZJu4pCwwfmoTLvcgwecq`, `G9uiJWzsPUoDuZKXEWSBvEtCi5NtU6iCQc6SeBPSRScT` reçoivent environ 0,75 SOL chacun de `2AQdpHJ2JpcEgPiATUXjQxA8QmafFegfQwSLWSprPicm` de 23:37:51 à 23:40:16, et versent à `9W9b` le 27/06 de 05:48:46 à 05:49:58.
- 08/02/2025 : `Amu8s5w3JHbcUf5HupUs1P23hz1WAEn12pZA1pUbJynm` et `CBfWiMK41uMoMKv5WbSRM2HNaoa6nBURCVtiueSyC5bc` reçoivent 1 SOL de `D89hHJT5Aqyx1trP6EnGY9jJUB3whgnq3aUvvCqedvzf` à 59 s d'écart, puis versent à `9W9b` le 09/02 à 44 s d'écart.
- Le geste précède donc DMAGA. Cela renforce « même client », et affaiblit toute lecture qui ferait de la série un acte propre au lancement.

**Non vérifié.** Les 2 201 viennent de `cb_window.csv` de C, ses pages brutes n'ont pas été gardées. Refaire la fenêtre coûterait plus que mon budget.

**Correctif de texte.** Ajouter : « Le même geste, retrait Coinbase vers wallets neufs à moins d'une minute d'écart puis versement au même dépôt, se voit aussi le 26/06/2024 et le 08/02/2025. »

## 3. G3, DCA, salve, séance

**Statut : CONFIRMÉ EN PARTIE.**

**Vrai sur le brut.**
- 47 ordres ouvrant du DMAGA (`i07_dca2.txt`).
- 5 ordres de la série de 19:53:13 à 22:16:49 le 21/07/2024.
- Salve : 116 377,378515 USDC, de 05:22:29 à 05:24:16.
- **Plus fort que ce que G écrit :** 4 versements de la salve sur 5 égalent au micro-USDC près ce que le wallet a reçu du DCA depuis 19:00. Le 5e, `Fp6kgqHU`, dépasse de 193,21 USDC (`i73.txt`). Le lien vente, dépôt est donc direct pour ces wallets.
- Cours du jour contrôlés contre `raw/solusd` sur 3 jours.

**Faux 1 : « 113,37 M de jetons ».** Réconciliation ordre par ordre (`i08_recon.txt`, `i08_recon.csv`) :

| Jetons | M |
|---|---|
| Déposés à l'ouverture | 113,374 |
| Sortis par exécution | 48,571 |
| Rendus au wallet à la clôture | 64,629 |
| Reste | 0,175 |

Les jetons rendus sont rouverts dans d'autres ordres : `7FGoCB63` ouvre 13,55 M et se fait rendre 13,45 M. G additionne des dépôts. Le signe était visible : 11,4 SOL par M contre 45 SOL par M pour ses ventes directes.

**Faux 2 : « 1 292,4 SOL éq. ».** 218 621,81 USDC font bien 1 292,36 SOL éq. Mais 19 ordres sur 46 exécutés paient en SOL natif, 213,16 SOL pour 12,24 M (`i10_dca_sol.txt`). La requête de G, qui exige l'escrow comme contrepartie, ne les voit probablement pas. **Total : 1 505,51 SOL éq. pour 48,57 M** (`i11_dca_time.txt`). « Vend surtout par DCA » reste vrai : 71 % en SOL éq. et 78 % en jetons, contre les 619,1 SOL et 13,76 M de G, que je n'ai pas refaits.

**Faux 3 : « rien avant » 19:30:13.** `4pKFTQxs` ouvre un ordre de 2 M le 15/07 à 15:52:16 et reçoit 8,64 SOL par exécutions à partir de 15:59:19. C'est peu, et cet ordre figure dans la liste de G. 24 h après S : 639,69 SOL éq. confirmé, sans SOL natif.

**Le test de permutation (`i12_perm.txt`).**
- Stat refaite : 8 sur 27, moyenne 1,60 contre 1,59. P = 1/5001 = 0,0002, **c'est le plancher du tirage**. Écrire « P ≤ 0,0002, 5 000 tirages ».
- Tests regardés : le script de G en calcule 3, 15 min, 1 h, 24 h, et le texte n'en cite qu'un. Avec Bonferroni le résultat tient, et il tient de 60 s à 1 h dans mon calcul.
- **Le vrai défaut : il est placé sous « Séance commune », et il n'en parle pas.** Les 8 écarts tombent les 30/07, 04/08, 13/08, 23/08, 10/09 (2), 31/12/2024 et 26/08/2025. **Aucun le 26/01/2025.** Ce jour-là, 14 wallets communs versent, 9 à `9W9b`, 5 à `Caw4`, aucun aux deux. Sans cette journée la stat reste 8.
- Ce que le test établit : un wallet qui verse à un dépôt verse souvent à l'autre dans la minute. Une personne qui encaisse son SOL et son USDC ensemble fait pareil. Cela relie les 2 dépôts au niveau du wallet, pas plusieurs wallets entre eux.

**Le test qui parle de la séance.** Paires d'événements de wallets **différents**, à 15 min au plus, entre les deux dépôts, contre décalage circulaire du calendrier, 2 000 tirages : **73 paires, moyenne 0,2**, P au plancher 0,0005. Sans le 26/01/2025 : 22 paires, moyenne 0,2. Exploratoire, paires non indépendantes, une cause externe commune n'est pas testée. Mais c'est la bonne question.

**La séance elle-même (`i72.txt`).** Bornes de G exactes. Petites sommes : 3 086,99 USDC et 5,647 SOL. C'est un vidage de restes, pas une vente.

**Correctifs de texte.**
- G3 : « 47 ordres, 113,37 M déposés dont 64,63 M rendus, soit 48,57 M vendus, pour 1 505,5 SOL éq. (218 621,81 USDC et 213,16 SOL). »
- Section 1 : remplacer « DCA 1 292,4 SOL éq. pour 113,37 M » par « DCA 1 505,5 SOL éq. pour 48,57 M ». Remplacer « rien avant » par « 8,64 SOL avant, un seul ordre, du 15/07 ».
- Séance : retirer la phrase des 8 wallets et la permutation de ce paragraphe, ou la déplacer sous un titre propre. Écrire : « Sur le 26/01/2025, 22 versements de 22 wallets, aucun aux deux dépôts. Entre wallets différents, sur toute la période, 73 paires à moins de 15 min entre les deux dépôts, contre 0,2 attendu par décalage du calendrier (exploratoire). »

## 4. G4, G5, table des frontières

**Statut : CONFIRMÉ et renforcé. Libellés de la table à corriger.**

**Décodage (`i14_dln.py`, `i15_dln_sum.txt`).** Décodeur propre du journal `CreateOrderWithNonce` sur tout le brut, pile d'invocations suivie. 76 ordres, 0 erreur, 76 signatures communes avec G.
- Donné : USDC 76 fois sur 76. Les USD sont donc de vrais USDC nominaux.
- Somme, montant plus frais de 0,04 % : **1 018 687,18 USD**, identique à G. Le frais fixe de 0,015 SOL n'y est pas.
- Appel externe 0, bénéficiaire d'annulation 0, receveur égal à l'autorité d'ordre 76 fois sur 76, taker imposé 4.
- `g43_orders.csv` a 2 lignes fausses : `usd_sortis` 4 999,88 et 5 485,22 pour des ordres de 2 498,19 et 2 740,59. Sa colonne totalise 1 023 933,51. Le rapport a le bon total, pas le CSV.

**Ordre annulé compté ? Non, sur ce qui est vérifiable.** Aucune instruction d'annulation dans le brut, 5 `ClaimUnlock` seulement (`i14_other_ix.csv`). Surtout, **exécution vérifiée sur Ethereum**, ce que G laissait ouvert (`i21_evm_fill_part1.txt`, `i22_evm_rest.txt`) :

| Receveur | Ordres | USD | Retrouvés au wei près | Délai |
|---|---|---|---|---|
| `0x2d86499a410a9ac2139833ba8d6942b8a8700a7b` | 27 | 496 371,59 | 27 | 3 à 146 s |
| `0xb947bf7f409e998b28f8e218802fc9575c3c8c57` | 4 | 263 573,15 | 4 | 35 à 53 s |
| `0xb29826d809aa04d2ead6f2310d8965a45b87fa67` | 8 | 151 360,77 | 8 | 5 à 29 s |
| `0x86f99097c563e84dd5190f3e85f6a2988f1c47a5` | 2 | 31 228,81 | 2 | 17 à 57 s |
| **Total** | **41** | **942 534,32, 92,5 %** | **41** | |

Non vérifiés : 3 ordres Ethereum (3 868 USD) et 32 sur Base, BSC, Polygon, Arbitrum. Blockscout Base m'a répondu 403. Exemple d'exécution : `0xd6d1a685ec581d23818b15972416efa251dd15ce4f7b9277ac9df82a56ef6f0b`.

**Le receveur est-il un contrat ?** Non pour les 4 (`i20_evm.txt`, source Blockscout public).
- `0x2d86499a` : compte simple, nom ENS public `afk.eth`, **21 519 tx et 15 213 transferts de jetons**. C'est un wallet très actif, peut-être un service ou un opérateur intensif. La chaîne ne le tranche pas. Contrôle commun « non établi » reste juste.
- `0xb947bf7f` : compte simple, 21 tx propres depuis le 11/09/2022.
- **Lien EVM non vu par G :** `0xb29826d8` paie le gaz de `0xb947bf7f` depuis le 11/09/2022 et lui envoie 50 003,33 USDC le 25/07/2024. Deux receveurs, un même acteur, 22 mois avant DMAGA. **B pour un même opérateur côté EVM.**
- **Second receveur commun, absent de G5 :** `0xb29826d8` reçoit de `Ei5yGz8d` (15 ordres, 170 817,36 USD) et de `HGBiExZR` (1 ordre, 1 760,91 USD).
- **Un versement sans ordre connu :** `0xb947bf7f` reçoit 120 957,89 USDC du même contrat solveur `0x555ce236c0220695b68341bc48c68d52210cc35b` le 26/07/2024 à 05:56:11. Aucun des 76 ordres ne le produit. Soit un autre wallet Solana hors du périmètre lu, soit une autre chaîne. **Les 76 sont un plancher.**
- G5 : 263 573,15 USD en 9 min 36 s exacts. Le premier ordre vaut 16,54 USD, 9,99 USDC reçus : un essai, puis 60 443,99, 156 089,02 et 47 023,61 USD.

**Formulation à corriger.** « `C73Yv9iH` envoie 496 371,59 USD dès 22:53:42 » se lit comme un seul moment. 24 h après : 12 ordres, **296 074,50 USD**. Le reste s'étale jusqu'au 09/06/2025.

**Table de la section 6 (`i16_table.txt`, `i17_p1share.txt`, `i18_dbl.txt`, `i19_bridge_row.txt`).**
- Sommes et lignes reproduites depuis `flow_boundaries.csv`. 44,5 % et 86,6 % sont arithmétiquement justes.
- Double compte : aucun wallet dans 2 périmètres. Aucune ligne de la table vers un des 76 comptes d'ordre. Seul P2 vers P1, 28,2 SOL, compte des deux côtés, 0,1 %.
- **« 76 ordres, 21,3 % de la table » mélange deux choses.** La ligne compte 71 ordres de P1 et P2 (977 099,94 USD) plus `BrdgN2RP`, 7 855,50 USDC, autre programme, nom non vérifié, 31/03/2024. 5 ordres, 41 587,24 USD, sont hors périmètres et hors table. Sans `BrdgN2RP` : 21,1 % et 44,2 % pour P2.
- 18 ordres, 4 632,17 USD, précèdent le mint. Effet faible, à dire.
- **« P2 passe d'abord par des ponts » :** 4 wallets, `C73Yv9iH`, `Ei5yGz8d`, `HGBiExZR`, `Gcyg2jeL`, font 99,5 % des USD de P2 en ordres deBridge. Écrire « 4 wallets de P2 ».

**Le 86,6 % est-il circulaire ?** P1 est défini par les expéditeurs de `9W9b`, donc conditionné à sa sortie. Test sur le brut, virements purs seuls : numérateur identique, 3 138,6.

| Sous-ensemble | Dénominateur | Vers les 2 dépôts |
|---|---|---|
| P1 entier | 3 479,2 | 90,2 % |
| Après le mint | 3 066,6 | 93,8 % |
| Avant le mint | 412,6 | 63,6 % |
| **Série et créateur seuls, non définis par le dépôt** | **1 225,4** | **96,8 %** |
| Expéditeurs hors série | 2 253,8 | 86,6 % |

Le soupçon ne tient pas : la part monte quand on retire la sélection. Citer 96,8 %, en disant que `Caw4` a été retenu à cause de ces wallets.

**Correctif de texte.** G4 : « 76 ordres décodés, 1 018 687,18 USD en USDC, dont 41 ordres et 942 534,32 USD retrouvés au wei près sur Ethereum. 71 de ces ordres et `BrdgN2RP` forment la ligne pont de la table. » Section 6 : retirer « Exécution sur la chaîne d'arrivée : non vérifiée » et mettre le tableau ci-dessus.

## 5. G6, chaque grappe a sa sortie

**Statut : CONFIRMÉ EN PARTIE.**

**Croisement refait, 8 dépôts contre 8 (`i24_cross.txt`).** Au seuil de 0,01 SOL ou 1 USD : `9W9b` et `Caw4` 27 ; `9W9b` et `AQVgyg8P` 1, `G41vRrsH` ; `9W9b` et `By6Dao4Q` 1, `AtZjv3Du` ; plus les recouvrements internes aux comptes de `GXZvXsD6`. Sans seuil, le recouvrement monte partout, mais ce sont des adresses de poussière présentes partout. Salve du 23/07 : 4 wallets, 164 s, 31,9 SOL, exact.

**« Chaque grappe a sa sortie » est trop fort.** `H3QsBrri` n'a pas de sortie atteinte, G le dit lui-même. `AQVgyg8P` pèse 145 SOL et `By6Dao4Q` 343 SOL, face à 12 292 SOL éq. pour P2, dont la première sortie est le pont. Écrire : « Les 5 dépôts ont des expéditeurs disjoints, à 2 wallets près. Cela ne fait pas de chacun la sortie de sa grappe. »

**Jonction manquée : `7Gw3gL8mq7TSENSe9VZD9DgJiPQF9dHd6Auwk6PRkjhx`.** G la classe « wallet sondé » sur 3 lignes séparées et ne la lit pas. Recherche : toutes les sorties de `raw/flows` et du net, destinations partagées entre grappes, puis lecture (`i25_junction.txt`, `i27_cand.txt`, `i28_7gw.txt`, `i71.txt`).

| UTC | De | Vers | Montant | Signature |
|---|---|---|---|---|
| 15/05/2024 22:13:33 | `DfYyxDNEXBzZWVPuJrNfko1rDrtR8SiqWLeGUMmNn8DT`, P1 | `7Gw3gL8m` | 0,7 SOL | `3qmzf3oWcwQjKuR2HS51YbACxMfeiRzp9NGRTLabPP2Eqb7vD4237oqFyv3z7CWGpj8UB829WzScxPdGjx8FmC3h` |
| 03/08/2024 04:40:03 | `EGtyQEgMKGKXjppDqj9sYy97e9m7nvu1US4SfFXNakMy`, salve du 23/07 | `7Gw3gL8m` | 78,909373285 SOL | `MpbxCDghSqrbz5tu15EdHmYYQmGn1JjMSrNeCPPJj8irX5JCFC2xhpwSQ6iiThknUNBYWg11JdpBghv8ACj89jB` |
| 03/08/2024 04:40:32 | `7Gw3gL8m` | `EGtyQEgM` | 1,0 SOL, **29 s après** | `Zz3sQjpj3LbxybCThNEgEPDHYrv2J6WKbkuaXibHUNNTD3GWUueKszSBEFgzknApvzoSEeV7A9pMKyjW1dQ7qkc` |
| 03/08/2024 04:41:44 | `9cfRU5RKRjUKGumdVRAehiu9PtEY8vDd4wejkpdUP7vw` | `7Gw3gL8m` | 400 SOL | `2BfutoeRjJDZQmNMjcYEcpecQGn1BmkWUFyFBoZPRPCVarDM4H3ubXm2Qkj47rCyKGL9MRP22gsS6USJ2FEQJFNJ` |
| 20/07/2025 17:10:18 | `6ty9DM4s2mNvsMpMrcaXBDVguFHapfwK9g7WdD9DBLgM`, série | `7Gw3gL8m` | 1 000 USDC | `5Zu1ofkpmCS2Yjwdfq5vEGJeDXHURJ32UqgL1zuR3VPxWWJFn5r1TqzjTdwitP6oNMZZXFsfRjmy6biV5UmdeqE9` |

- `9cfRU5RK` est le n° 11 de `reports/TOP_TRADERS.md`, 729,2 SOL, « avant visuel », et un des 30 de la cohorte du test de groupe. `7Gw3gL8m` est son premier financeur connu, 0,5 SOL le 08/02/2024, et lui donne 4 SOL le 14/07/2024 à 02:18:29, 13 min après le mint. Il en reçoit 1 471,1 SOL de sorties lues.
- `7Gw3gL8m` est un vrai wallet : il signe, trade, et a 100 tx récentes. Ce n'est pas une courbe ni un pool.

**Niveaux.** Transaction A. Coordination C. Contrôle commun : **B entre `7Gw3gL8m` et `9cfRU5RK`**, financeur et aller-retour répété ; **C entre `EGtyQEgM` et `7Gw3gL8m`**, renvoi de gaz en 29 s ; **non établi au-delà**. Alternatives : paiement ou OTC vers un tiers actif, 3 versements espacés sur 14 mois. Population complète de `7Gw3gL8m` : non lue, 4 pages seulement. `9cfRU5RK` n'est pas un des 3 gagnants de C20, cette ligne ne bouge pas.

**Candidats vérifiés et rejetés.**
- `HFRc5NmwpP83MambL2i7M7hhTe24qQxKwVtp4Yn6naVG` : `C73Yv9iH` et `B252jsFK`, 3 versements en 192 s, montants ronds plus 1 lamport. Sonde : c'est une courbe pump.fun, 0 tx signée, ce sont des achats du même jeton. Le motif +1 lamport se voit chez 139 wallets, sans valeur (`i74.txt`).
- `75fXGTvc8BHKBXwNfqriso6dzLe52qMUzvGPu9DV8fog` : reçoit 1,93 M de jetons de `B252jsFK`, `EZXUvi4X`, `Fp6kgqHU`, et 1 000 USDC de `8SaiGWJn`. Trader très actif, 56 tx signées sur 72 lues en juillet 2024. Vente de gré à gré plausible. D, signalé seulement.
- `Cr8oGfjwRnrFyhVyFM4S3ygR2dKy4CgTpXgVwELbfsBg` : 11 expéditeurs en 2 semaines. Probable service, non lu.
- `9UsmwVmbV4VwEwv5q5iZh4y3THh6dn2cqjFpEUrGRzZJ` : réserve de pool, déjà connue.

**Correctif de texte.** Section 3 : garder « seule jonction par dépôt », et ajouter un paragraphe sur `7Gw3gL8m` avec ces 5 lignes, niveau C, en précisant que ce n'est pas un dépôt.

## 6. G7, jonction indirecte de `GXZvXsD6`

**Statut : CONFIRMÉ. Niveau C mérité, pas plus (`i29_g7.txt`).**

- Faits exacts. `ERMtiLod` 1,5 M vers `HW5MqvM1`. `GoPCTrS3` 1 M vers `HKzkNSH2`, et ce transfert est bien la première tx de ce wallet, signée par `GoPCTrS3`. Vente 28,9 SOL le 26/07. Versements à `8N4AvP9j` les 30/09 et 01/10 : 54,8 et 54 SOL.
- Aucun retour de valeur vu vers `ERMtiLod` ou `GoPCTrS3` (`i72.txt`), avec le seuil de collecte de 0,1 SOL et 100 USD.
- Trop haut ? La chaîne passe par des comptes partagés dont 2 sur 3 sont eux-mêmes au niveau C (`42MSVeV4`, `9kqTVnRU`), et `8N4AvP9j` a 19 expéditeurs. `GXZvXsD6` n'a aucune arête. B multiplié par C ne donne pas mieux que C. Pour `GXZvXsD6` lui-même, un contrôle commun n'est pas établi.
- Trop bas ? Non. `HW5MqvM1` utilise `8N4AvP9j` depuis le 31/01/2024, avant DMAGA. Seul `HKzkNSH2` est un wallet neuf créé par la série.

**Correctif de texte.** Remplacer « donnent » par « transfèrent » : le mot suppose l'absence de paiement, alors qu'une vente réglée ailleurs reste possible. Ajouter : « Contrôle commun : C entre ces wallets et les 2 receveurs, non établi jusqu'à `GXZvXsD6`. »

## 7. G8, `3GMsedVP`

**Statut : CONFIRMÉ EN PARTIE. Le mot sandwich est mérité. La marge et le net sont faux (`i35_a16c.txt`, `i36_a16d.txt`).**

**Refait sur le brut `raw/full_*`, tiers lus dans `data/trades.parquet`.**
- 3 826 tx, 1 913 blocs de 2 tx, 0 échec. Index distants de 2 dans 1 913 blocs sur 1 913. Même signataire entre les 2 jambes partout. Quantité **exactement** égale au niveau de l'acteur.
- 967 achat puis vente, le signataire porte les jetons. 946 vente puis achat, `4ToQp55m` les porte. 45 signataires.
- Tiers : présent dans 1 913 blocs sur 1 913, une seule transaction entre les jambes. Sens : achat dans le premier cas, 1 124 lignes contre 2 ; vente dans le second, 968 contre 1. 12 198 et 18 100 SOL.
- 832 tiers distincts, les 10 premiers font 20 %, aucun n'est signataire ni le trésor. Pas d'auto-sandwich visible.
- **Fait absent de G :** une tx de chaque bloc paie un compte de pourboire Jito, 1 913 sur 3 826, 24,57 SOL. Liste des 8 comptes prise de mémoire, non revérifiée. C'est le mécanisme d'un paquet atomique, et cela explique l'index exact.

**Arbitrage et tenue de marché écartés ?** Oui. Même pool, même quantité, sens opposés, un tiers de même sens toujours au milieu, paquet payé. Un arbitrage entre venues aurait une jambe ailleurs. Un teneur de marché ne ferait pas 1 913 blocs sans aucune exception. **Le mot est mérité, B reste prudent et juste.** L'intention n'est pas lue, le mécanisme l'est.

**Faux : « Marge 9,44 SOL », « Net de jetons nul », « Marge totale 194,85 SOL ».** Comptabilité complète d'un bloc de chaque forme :
- Forme achat, slot 278900503 : le trésor avance 115,897631 WSOL, le signataire reçoit 979 495,84 jetons. Au retour, le pool reçoit 956 783,53 jetons et rend 116,178839 WSOL. Le trésor récupère 115,897631 WSOL **et garde 22 712,31 jetons**. **Le surplus de 0,281199 SOL part au compte de pourboire.**
- Forme vente, slot 278900850 : le trésor reçoit 0,505046 SOL, le pourboire 0,026991 SOL.

| Forme | Blocs | Trésor, SOL et WSOL net | Trésor, jetons | Pourboires |
|---|---|---|---|---|
| Achat puis vente | 967 | **-0,24** | **+3,047 M**, environ 140 SOL au prix du bloc | 9,42 |
| Vente puis achat | 946 | +170,30 | 0 | 15,15 |

Donc les 9,44 SOL de G sont, pour l'essentiel, les pourboires et les frais, pas un gain. Le gain de la forme achat est en jetons, 967 fois sur 967. « Positif 967 fois sur 967 » est vrai pour les jetons, pas pour le SOL. Le net en jetons du trésor n'est pas nul sur ces blocs : +3,05 M, soit 0,3 % de l'offre. Il devrait être revendu ailleurs, je n'ai pas suivi.

**3,12 % :** je lis 24 723,72 SOL sur 788 864,76, soit 3,13 %. Écart sans portée. Non refaits : 4,44 %, 2,44 %, 3,92 %, le trésor à 292 787 SOL, les dates du programme.

**Correctif de texte.** Remplacer les 2 lignes de marge par : « Forme achat : gain en jetons, 3,05 M gardés par `4ToQp55m`, environ 140 SOL au prix du bloc, et 9,42 SOL de surplus entièrement versés en pourboire. Forme vente : 170,30 SOL au trésor et 15,15 SOL de pourboire. Produit total : environ 335 SOL éq., dont 24,57 SOL de pourboires. En SOL seul, le brut retrouve les 194,85 de G, mais il inclut ces pourboires. » Remplacer « Net de jetons nul » par « Net nul pour chaque signataire, +3,05 M pour le trésor ». « Ce n'est ni de l'accumulation ni de la distribution » reste vrai à cette échelle.

## 8. `9PrmF8` et `H9Xezqfd`

**Statut : CONFIRMÉ EN PARTIE. Autre population que `9W9b`. B et C restent justes (`i60_touch.txt`, `i61.txt`).**

- 904 tx, 10 expéditeurs, 8 touchent DMAGA, refait par 3 sources sans `d01_own`. 31 sur 48 et 22 sur 55 reproduits aussi. Pour `Caw4`, 16 expéditeurs n'ont aucune source lue : 22 est un plancher.
- **Le chiffre 8 sur 10 ne veut pas dire la même chose.** Première touche de DMAGA **avant Musk** :

| Dépôt | Touchent | Dont avant 19:30:13 le 21/07 | Dont en 2025 ou après |
|---|---|---|---|
| `9W9b` | 31 | 20 | 1 |
| `Caw4` | 22 | 12 | 3 |
| `AQVgyg8P` | 5 | 5 | 0 |
| `By6Dao4Q` | 6 | 4 | 0 |
| `H9Xezqfd` | 8 | **1, `9PrmF8` seul** | **4** |

- Les expéditeurs se succèdent : `9PrmF8` de 01/2024 à 10/2026, `8B5ekuLt` de 09/2024 à 11/2025, `ENvLw1g1` 02 à 03/2025, `DxTWPAXs` 12/2025 à 05/2026, `FPVpSxs7` 06 à 08/2026, `CRbvuSFo` 10/2026 à 11/2026. Aller-retour de SOL entre eux, densité de paires reliées 0,222, contre 0,072 pour `9W9b`, mesurée sur ce qui est lu.
- **Lecture :** une rotation de wallets d'un même détenteur, longue et sans salve, pas un réseau de lancement. Le témoin de 0,59 % écarte le hasard, il ne dit rien de plus. Le raisonnement « compte de dépôt partagé » vaut. La lecture « réseau autour du jeton dès le début » ne vaut pas. `9PrmF8` signe déjà des versements en janvier 2024.

**Correctif de texte.** Après « 8 sur 10 touchent DMAGA », ajouter : « Mais 1 seul avant Musk, 4 seulement à partir de 2025. C'est une rotation de wallets d'un détenteur durable, pas une population de lancement comme `9W9b`. »

## 9. X

**Posts et images : CONFIRMÉ (`i40_x.txt`, `i41_kiki900.txt`).** Heures par mon calcul du snowflake, clé du média lue dans la réponse brute, nom de fichier et URL d'archive du manifeste concordants.

| Post | Heure | Clé | Fichier | Contrôle |
|---|---|---|---|---|
| `1815006501896872388` | 12:50:45,899, média 12:50:21,641 | `GTAytGIW4AE9_93` | 900 x 900, sha256 `dc2bed87096844d67d765b631ade81a3d9d896067175dda44839d5916566d812` | Auteur `kikisknees`, « @pmarca Is Elon mooning with us? ». Musk, armure, sans drapeau |
| `1815054374982324401` | 16:00:59,732 | `GTBeVcVXAAAVa3o` | 1024 x 1024 | pHash 0 et dHash 0 avec l'avatar, DCT maison et `imagehash`. Vu à l'œil |
| `1815054158367432804` | 16:00:08,087 | `GTBeEjGXgAAbn4S` | sha256 `cce3b01b864a264dac2c02ceff2dce50365a7e0b2adaa0a39d471d30c3eecccb` | Même sha256 que `1813683527575302497` et `1814719737378607482`. Trump « dark maga ». Vu à l'œil |
| `1814063148917256375` | 18/07 22:22:13,022 | `GSzYuoTXgAA63zz` | 1125 x 1003 | Texte complet avec `$DMAGA`. Musk aux yeux laser, foule de Pepe |

**Détail de texte.** La liste de la partie 3 de `X_FOLLOWUP.md`, ligne de 22:22:13, coupe `$DMAGA` et la ligne plus bas l'a. Corriger la liste.

**Réponse antérieure de @kikisknees avec la même image ?** Aucune visible. Index de 1 485 statuts, 470 médias de posts propres avant 12:50:45. **Sur 165 images 900 x 900, 162 ne sont pas lues.** J'ai tenté 41 clés dans la Wayback, les plus proches d'abord : 4 lues, distance à V1 d'au moins 24, le reste en 429 ou 503 (`i42_wb900.txt`). « Plus ancienne connue » est la bonne formule, « plus ancienne » serait faux.

**« Sans drapeau = même composition que l'avatar » : tient à l'œil, pas par pHash.** pHash 14, au-dessus du seuil de 12, car le fond change tout. Mesure ajoutée, corrélation des contours sur la zone visage et armure, meilleur décalage (`i41_kiki900.txt`) :

| Image | r | Décalage |
|---|---|---|
| V2 de @FrancoAppr | 0,848 | 0, 0 |
| **V1 de @kikisknees** | **0,585** | **0, 1** |
| V0, foule de Pepe | 0,034 | au bord de la recherche |
| Trump | 0,002 | au bord de la recherche |

Même montage, même cadrage, fond différent. Niveau : A pour la date, B pour « même montage ». Écrire que le pHash ne le montre pas.

**Les lignes citées.**
- @XHEILIGX : texte exact, adresse complète, 106 jours avant le mint. **Élément omis par E :** l'offre de @pezitoken dit « drop your SOL address ». Cela soutient un peu la lecture « sa propre adresse ». Achat de `9PrmF8` le 14/07 à 02:28:56, 2,86 M, confirmé sur le brut. Test $PEZI proposé par E : 6 jetons reçus sans dépense de SOL du 30/03 au 31/05/2024 dans les 1 200 tx lues, dont 3 par transfert, nommés LENIS, NUKEY, PEPSOL. **Aucun $PEZI vu**, sans conclure : le mint de $PEZI n'est pas identifié, et l'offre a pu ne jamais être servie. C reste juste. Le profil lu est celui d'aujourd'hui, pas de 2024.
- @twicrates : texte exact. C'est une citation de « @twicrates You never bought yours anyway », pas une réponse. La phrase finit par « and dont plan on touching ». C pour le fait.
- Métadonnées IPFS : exactes, aucun lien social. A.
- Certificat de `dmaga.xyz` : 14/07/2024 02:41:38, GoDaddy, id 13729224712, exact. **Mais `rdap_dmaga.xyz.json` donne un enregistrement du 29/09/2025.** L'enregistrement de 2024 n'est pas dans les preuves. Un certificat date le certificat, pas l'achat du domaine.

**« Deux jours avant Butler : contredit » dépasse les preuves.**
- Vrai, niveau A : le jeton n'existe pas avant le tir. Mint à 02:05:25, Telegram 01:57:02, premier post 02:26:35, avatar du compte 01:51:10, 1 post et 7 abonnés à 02:45:55.
- Faux : « **toutes** les dates objectives lues ». La création du compte X, 11/06/2024 16:25:03, est objective et antérieure. E l'écrit lui-même en partie 5, le résumé l'oublie. Le projet `$DARKMAGA` du 09/05/2024 et l'adresse `DarkMAGAonSOL@proton.me` affichée par `dmaga.xyz` restent non tranchés.
- La phrase d'origine, « @kikisknees a lancé @DarkMagaCoin » puis « deux jours plus tard », ne dit pas « a créé le jeton ». Elle peut viser le compte, le groupe, l'esthétique. Et elle n'est connue que par Thread Reader, le thread étant supprimé.
- Le compteur de posts ne voit pas un post supprimé. 20 posts sur 187 de la fenêtre restent non lus. Le pseudo du compte a pu changer, non vérifié. Rien ne voit un groupe privé.

**Correctif de texte.** Remplacer le point 5 de la partie 1 et le verdict de la partie 5 par : « Lancement public du jeton deux jours avant Butler : contredit, niveau A, le mint et toutes ses traces suivent le tir. Préparation privée, ou lancement du compte ou du groupe plus tôt : non tranché. Le compte X existe depuis le 11/06/2024, et l'enregistrement de 2024 de `dmaga.xyz` n'est pas connu. »

## 10. Test `etude_groupe/`

**Recalcul : CONFIRMÉ. Lecture : CONFIRMÉE EN PARTIE. Aucune observation retirée, verdict gelé inchangé, rien écrit dans `etude_groupe/` (`i50_grp.txt`, `i51_grp2.txt`, `i52_grp3.txt`).**

**Table recalculée, graphe réécrit.** 47 lignes sur 49 identiques. Les 2 autres (`FDcq9Swb`, `9v5TRd1p`) diffèrent seulement sur G2, parce que `measures` garde la première composante en cas d'égalité : le choix dépend de l'ordre. 6 tokens ont une égalité, toujours 3 ou 4 wallets. Aucun effet sur le rang de DMAGA. La « médiane » de `ana_grp.py` est `ok[len(ok) // 2]`, une médiane haute : `results.md` écrit 3,77 % et 23, la médiane vraie vaut 3,56 % et 22,5. Mineur, à noter.

**Plan contre code.** Conformes, sauf un point. Le plan dit « chaque receveur reçoit au moins 1 M ». Le code garde les seuls gros receveurs et ne rejette pas la tx. Effet mesuré sur `raw/grp` : 21 arêtes sur 2 560, 3 tokens, DMAGA à 0, aucun rang changé. C'est un écart à déclarer, sans portée.

**Les 3 pairs les plus hauts sur G1, lus à la main.**

| Pair | G1, G2, fenêtre | Cohorte dans la composante | Ce que c'est |
|---|---|---|---|
| `BFUadco9hktp8wrLas34DL5jmVYE17qYmfxZykV7pump` | 77, 11,2 %, 27,6 j, extension plafonnée | **2 sur 30** | Montants ronds, 10 M et 5 M. `3obDjgKX` envoie 159,67 M à 13 wallets en 9 min, le 22/07. Le nœud central `GBPiMh9x` a 449 tx sur son compte de jetons : un trader très actif, peut-être un teneur de marché. À hub 5, G1 tombe à 7 |
| `iUTxa3m6JedGj6XTGwYEe324M5iWrBvnWzpUhXopump` | 65, 80,5 %, 33,1 j | 24 sur 30 | Réseau réel et très concentré, 41 arêtes avant le pool. **Un compte de programme, `5rbAq8M3`, 15 entrées, ne signe jamais, reste sous le seuil de 15.** Sans les comptes de programme : 49 |
| `4xqQAEBeMH1MJ85MsuWiVwRTc4F7AC2UikttcVvcpump` | 48, 17,4 %, 27,9 j, extension plafonnée | 12 sur 30 | 3 services déjà retirés, 57 arêtes avant le pool. Répartition réelle entre wallets peu actifs |

**Les services gonflent-ils les pairs ? Non, au sens large.**
- Aucune étiquette connue dans aucun graphe, 0 sur 49.
- Aucun airdrop visible sur ces 3 pairs : 0 tx à 3 receveurs ou plus.
- Comptes de programme : 24 pairs en ont. En les retirant de tous, 6 pairs restent au-dessus sur G1, rang inchangé.
- Limite : le seuil de 15 laisse passer un service à 14 voisins, et un teneur de marché n'est pas identifiable ainsi.

**Ce qui nuance vraiment : la fenêtre.** S moins création : DMAGA 7,7 j, pairs de 4 à 51 j. Les 3 pairs les plus hauts ont 28 à 33 j pour accumuler des arêtes. Spearman fenêtre et G1 : 0,29. Fenêtre et G3 : 0,33. Mêmes tokens, mêmes arêtes, en coupant à 7,7 j après la création pour tous :

| Mesure | DMAGA | Médiane des 48 | Maximum | Pairs ≥ DMAGA, plan | Pairs ≥ DMAGA, fenêtre égale |
|---|---|---|---|---|---|
| G1 | 34 | 8 | 77, puis 48 à fenêtre égale | 6 | **3** (48, 39, 38) |
| G3 | 50 | 22,5 | 114, puis 75 à fenêtre égale | 8 | **3** (75, 62, 58) |

Rang à fenêtre égale : 4e sur 49, p de rang 0,082, sans valeur de test. Parmi les 37 pairs de fenêtre inférieure à 15,4 j, **1 seul atteint G1 ≥ 34**. G2 ne se refait pas ainsi, les soldes manquent. Limite inverse : 2 des 3 pairs au-dessus à fenêtre égale sont plafonnés par l'extension, leur valeur peut être sous-estimée.

**Autre imprécision de la lecture.** `results.md` écrit « réseau de transferts directs entre gros acheteurs précoces ». Sur les 30 de la cohorte : **DMAGA 0 arête directe entre eux**, 21 pairs sur 48 en ont au moins une, médiane 0. Les composantes passent par l'extension. Wallets de la cohorte dans G1 : DMAGA 7, médiane 1,5, 5 pairs au-dessus. Le groupe de DMAGA n'est donc pas un réseau entre ses plus gros acheteurs, mais un réseau qui les touche.

**Correctif de texte pour `results.md`, décision de Benjamin, hors du gel car c'est de la lecture.** Remplacer la lecture par : « L'existence d'un réseau n'est pas atypique : 46 pairs sur 48 en ont un. Sa taille est dans le haut de la distribution, et plus nettement à fenêtre égale : 3 pairs sur 48 au-dessus de DMAGA sur G1 et sur G3 quand on coupe tout le monde à 7,7 jours, exploration hors plan. Ces réseaux relient peu les 30 plus gros acheteurs entre eux, DMAGA compris. Le test reste inconclusif et DMAGA n'est pas le maximum. » La phrase de la suite, « quelle que soit la suite, le verdict ne peut pas passer », reste juste au sens du plan.

## 11. Ce que je n'ai pas pu vérifier

- Les 2 201 destinataires : seuls les 14 sont contrôlés sur le brut. Pages brutes de C absentes.
- 35 ordres sur 76 côté arrivée, dont Base en 403. Identité du 5e versement à `0xb947bf7f`, chaîne d'origine inconnue.
- Ventes directes 619,1 SOL et 13,76 M, 4,44 %, 2,44 %, 3,92 %, flux du trésor à 292 787 SOL, dates du programme `3GMsedVP`, vidage du 21/08/2025, séquence du 29/09/2024, gestes du 21/07.
- Tiers de G8 lus dans `data/trades.parquet`, pas dans le brut. Comptes de pourboire Jito : liste de mémoire.
- Coinbase par actif : documentation non lue. Cause externe du 26/01/2025 : non testée.
- `7Gw3gL8m` : 4 pages sur un historique plus long. `G2` à fenêtre égale du test de groupe : impossible sans soldes.
- 162 images 900 x 900 de @kikisknees antérieures à V1. Wayback en 429 et 503.
- Rien sur les titulaires, comme il se doit. Aucune recherche d'identité. Le nom `afk.eth` est cité parce que Blockscout le rend, il ne désigne personne ici.

## 12. Budget et reproduction

Helius : 14 requêtes, dont 4 refus 429, soit 100 crédits au tarif de 10 par réponse, 140 au plus si les refus comptent. Plafond 500. Détail : `credits.csv`. Réseau hors Helius : Blockscout public, Wayback.

Scripts, depuis la racine, chacun sous `scripts/guard.py` ou `tools/heavy.py` : `i01` à `i03` dépôts et témoin, `i05` G2, `i06` à `i11` DCA, `i12` permutation, `i14` à `i19` ponts et table, `i20` à `i22` Ethereum, `i23` à `i28` et `i70` à `i74` jonctions et sondes, `i29` G7, `i31` à `i36` G8, `i40` à `i42` X, `i50` à `i52` test de groupe, `i60` à `i62` touches de DMAGA. Données intermédiaires : `audits_work/I/`. Aucun fichier écrit hors de `work_I/` et `audits_work/I/`. Pas d'entrée au `JOURNAL_AGENTS.md`, consigne d'écriture oblige.
