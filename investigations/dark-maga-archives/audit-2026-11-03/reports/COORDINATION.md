# Coordination : tests et liens financiers

Généré par `scripts/rep_72_links.py`. **Audit du 03/11 : NON VALIDÉ tant que les décisions de Benjamin et un nouvel audit des conclusions manquent.** Voir `audits/2026-11-03/`. Une arête prouve qu'une transaction existe. Elle ne prouve ni un propriétaire unique ni une intention. Dérivé corrigé : `data_v2/`.

## 1. Test gelé : DMAGA contre les autres pics tardifs
Plan gelé le 02/11/2026 à 23:47 UTC avant le calcul des mesures (`etude_final/analysis_plan.md`, `PROTOCOL.lock`). Amendement 001 : R1 et R2 réduits, sans effet sur le verdict, décision de Benjamin en attente (amendement 002). L'installation du projet d'amendement 003 reste en attente aussi.

**Verdict calculé par le code : DMAGA NON DISTINGUABLE DE SES PAIRS**

Verdict du plan : "DMAGA NON DISTINGUABLE DE SES PAIRS". Cela signifie qu'aucune mesure ne dépasse tous les 211 pairs. DMAGA est du 74e au 85e centile sur 6 mesures sur 7. Sur les vraies données, ce test détecte 2,4 % sans effet, 3,3 % pour une accumulation de deux fois la réserve du pool, 7,5 % pour l'effet fort de ses contrôles. Il n'apporte donc d'élément ni pour ni contre une connaissance préalable.

Comptage : {"retenu_superset": 245, "pas_de_pic": 12809, "hors_bande": 453, "tronque_sans_pic": 135, "reporte_budget": 278, "moins_de_20_swaps_primary": 1, "moins_de_20_swaps_R3_S_moins_1h": 2, "moins_de_20_swaps_R1_10x": 1, "moins_de_20_swaps_R2_bande_large": 1, "swaps_manquants": 0}. Rejets du parseur : {"ruptures": 0, "tx": 15852824, "lp": 3458, "sens_opposes_ignores": 21559, "parts_de_frais": 469433, "swaps": 11878474, "sans_vault": 3581605, "non_signataire_deux_cotes": 394814, "sans_beneficiaire": 389287, "qty_differente_du_vault": 14461}.

| Mesure | Définition | DMAGA | Médiane pairs | P90 pairs | p de rang | k | Indéfinis | Passe Holm |
|---|---|---|---|---|---|---|---|---|
| M1 | Run-up 3 h | 39,867 | 3,755 | 163,089 | 0,1698 | 211 | 0 | non |
| M2 | Run-up 24 h | 9,371 | 1,464 | 64,565 | 0,1840 | 211 | 0 | non |
| M3 | Part des nouveaux wallets, 24 h | 0,680 | 0,450 | 0,863 | 0,2406 | 211 | 0 | non |
| M4 | Part des 5 premiers, 24 h | 0,308 | 0,347 | 0,784 | 0,5472 | 211 | 0 | non |
| M5 | Synchronisation, 24 h | 433,798 | 176,327 | 1115,392 | 0,2642 | 211 | 0 | non |
| M6 | Détention des précoces à S | 0,205 | 0,075 | 0,263 | 0,1557 | 211 | 0 | non |
| M7 | Plus gros achat / réserve, 24 h | 0,138 | 0,074 | 0,223 | 0,1792 | 211 | 0 | non |

Unité : le token. Fenêtres fixées par le pic S de chaque token (DMAGA : 21/07/2024 19:00 UTC). n effectif prudent : 84 jours de pic distincts. Le choix des mesures a pu être influencé par ce qui avait déjà été vu de DMAGA, jamais par les comparateurs. Variantes partielles, sans valeur de robustesse sur la bande, jamais utilisées pour conclure :
- **R1_10x**, k = 212 : M1 p=0,164, M2 p=0,183, M3 p=0,244, M4 p=0,531, M5 p=0,258, M6 p=0,160, M7 p=0,202
- **R2_bande_large**, k = 240 : M1 p=0,207, M2 p=0,216, M3 p=0,282, M4 p=0,556, M5 p=0,282, M6 p=0,141, M7 p=0,187
- **R3_S_moins_1h**, k = 210 : M1 p=0,142, M2 p=0,166, M3 p=0,205, M4 p=0,557, M5 p=0,249, M6 p=0,152, M7 p=0,157

### Puissance sur les vraies données (exploratoire, hors registre)
Simulation de l'audit D, chaque token cible à son tour (`audits/2026-11-03/work_D/d11_scenarios.csv`). Le verdict ne bascule que si DMAGA dépasse tous les pairs sur au moins une mesure. M3 et M4 ne peuvent pas ouvrir. Niveau réel 2,4 %.

| Scénario | Détection |
|---|---|
| nul | 2,4 % |
| 0,25 R, 1 wallet, 3 h | 2,4 % |
| 1 R, 1 wallet, 3 h | 2,4 % |
| 2 R, 1 wallet, 3 h | 3,3 % |
| 5 R, 1 wallet, 3 h | 100,0 % |
| 2 R, 25 wallets, 3 h | 3,3 % |
| 2 R, 25 wallets, moitié dans un slot | 11,3 % |
| 2 R, 5 wallets, 24 h | 3,3 % |
| moyen du contrôle (6 wallets, 6 x lognormale, moitié slot) | 3,3 % |
| fort du contrôle (18 wallets, 25 x lognormale, moitié slot) | 7,5 % |

### DMAGA contre son propre passé (secondaire, Holm séparé, peu discriminant)
| Événement | Heure E (UTC) | SOL acheté sur [E−3 h, E) | Médiane du passé | p | Nouveaux acheteurs | Médiane du passé | p | Fenêtres du passé |
|---|---|---|---|---|---|---|---|---|
| winig | 21/07/2024 16:02:29 | 401,5 | 6,1 | 0,036 | 44 | 1 | 0,036 | 27 |
| avatar | 21/07/2024 19:23:20 | 229,3 | 6,2 | 0,069 | 55 | 1 | 0,069 | 28 |

### Financeur commun
**Exploratoire, hors plan gelé.** Part des 50 premiers gros acheteurs qui partagent un financeur direct non service, dans les 72 h avant leur premier achat : DMAGA 0,08 (2 financeur(s) commun(s)), médiane des 40 comparateurs tirés au hasard 0,00, p de rang 0,073. Ce test n'entre pas dans le verdict et n'a pas de correction. Arithmétique juste, mesure non recalculable : les réponses réseau n'ont pas été gardées (C46).

### Chiffres descriptifs juste avant Musk
Voir `windows.csv` et `reports/EARLY_BUYERS.md`. Entre l'annonce de Biden et la borne basse du changement de photo (1,29 h) : 13,18 SOL d'achats contre 84,94 SOL de ventes, 3 nouveaux acheteurs. Le groupe ci-dessous fait 0 swap(s) entre le visuel et la borne haute. Ces chiffres ne départagent pas une connaissance préalable : un détenteur existant n'a pas besoin d'acheter.

## 2. Groupes reliés par transferts directs de DMAGA avant Musk
Règle : transfert direct d'au moins 1 M de jetons avant le 21/07/2024 19:03:27 UTC, sans passer par un service. Liens de SOL exclus de ce tableau. Jetons détenus par tous les non-pools à cette heure : 938 M. Les colonnes « toute la vie » couvrent tout l'historique des wallets, pas la période d'avant Musk.

| # | Wallets | Arêtes | Détenu avant Musk M | Part des jetons hors pools | Acheté M, toute la vie | SOL engagé, toute la vie | Réalisé SOL | Flux net SOL | P&L USD |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 33 | 40 | 217,0 | 23,1 % | 426,4 | 833,4 | 5 470 | 5 313 | 968 992 |
| 2 | 3 | 2 | 45,3 | 4,8 % | 59,2 | 18,0 | 22 | 6 | 1 009 |
| 3 | 2 | 1 | 36,8 | 3,9 % | 37,2 | 25,1 | 101 | 90 | 24 601 |
| 4 | 3 | 3 | 25,0 | 2,7 % | 25,2 | 33,1 | 6 | -27 | -4 399 |
| 5 | 5 | 4 | 18,3 | 1,9 % | 45,5 | 619,2 | 979 | 501 | 92 252 |
| 6 | 2 | 1 | 17,1 | 1,8 % | 24,6 | 1 216,5 | 1 500 | 1 299 | 236 640 |
| 7 | 2 | 1 | 14,2 | 1,5 % | 15,1 | 51,6 | 479 | 466 | 81 216 |
| 8 | 2 | 1 | 13,0 | 1,4 % | 18,7 | 205,2 | 754 | 715 | 125 330 |
| 9 | 3 | 2 | 11,5 | 1,2 % | 28,2 | 83,5 | 455 | 448 | 78 289 |
| 10 | 2 | 1 | 7,3 | 0,8 % | 7,5 | 22,4 | 159 | 158 | 28 415 |
| 11 | 2 | 1 | 3,3 | 0,4 % | 51,3 | 1 081,5 | 833 | 165 | 30 493 |
| 12 | 3 | 2 | 3,0 | 0,3 % | 3,6 | 21,0 | 207 | 186 | 34 297 |

## 3. Le premier groupe : 33 wallets, niveaux distincts
Descriptif, hors plan gelé : le seuil de 1 M a été choisi après avoir vu DMAGA. Le créateur n'en fait pas partie (voir plus bas).
- **A, les transferts :** 40 transferts directs d'au moins 1 M, chacun relu sur la chaîne, la source signe sans programme d'échange (`reports/data_checks/group_edges_check.json`). Ces 40 relectures datent du 03/11, elles n'ont pas été refaites : leurs signatures sont identiques à celles du dérivé corrigé.
- **Plafond, pas une mesure :** 217,04 M détenus avant Musk, 23,1 % des 938 M hors pools. Le groupe tient par une arête égale au seuil (`NxtXcmEW… → GFpqfj…`, 1,000 M). Au-dessus du seuil, il se coupe en 19 et 14 wallets. Achats réels avant 19:03:27 : 359,8 M pour 158,5 SOL.
- **B, 29 wallets, 166,1 M, de 16,0 à 17,7 % :** plusieurs éléments indépendants concordent : les transferts ; le financement de 0,5 SOL avant le mint par `G41vRrsHShLEvwMj58ruhqJycGfAtWXxtLD56uFExL8E` ; une sortie commune en salves de moins de 3 minutes (ci-dessous). Ce niveau est une moyenne : `9u5JKgWdLzj4xUiA4sFnaaJeKAJF8zBXExatxeSZHMkP` et `7mdCAs8CWYJxkWz2gfj3sRhDBmUi6Q9qvRGuKiv2Bazu` n'ont que des liens faibles, sans eux 149,7 M.
- **C, 4 wallets, 50,9 M :** autour de `Ei5yGz8…`, reliés au reste par une seule transaction.
- **C, un seul propriétaire pour les 33 :** non établi. Avant le mint, le SOL entre membres ne relie que 7 et 2 wallets, en 2 composantes séparées, dès le 17/05 et le 10/04/2024.
- **`Habp5bncMSsBC3vkChyebepym5dcTNRYeg2LVG464E96` :** il sort du groupe par la règle de service, à cause de ses envois de poussière. Avec la règle écrite, le groupe compte 34 wallets et 41 arêtes. Son solde à la borne basse vaut 0,00 M : les 217,04 M ne changent pas.
- **Tôt :** 15 des 33 achètent en première heure, 206,9 M pour 52,3 SOL. Les autres entrent plus tard ou reçoivent leurs jetons.
- **0 swap entre le visuel de Winig et la borne haute du changement de photo.** Ses gestes du jour précèdent le visuel : répartition 07:57-08:33 UTC, transfert à 11:10, regroupement de 25,5 M à 14:22-14:25.
- **Ventes :** 2 988,9 SOL dans les 6 h après Musk, 1 536,0 SOL dans les 18 h suivantes. Ces 4 525 SOL en 24 h font **au moins 2,4 % des 190 546 SOL vendus sur le marché, 2,9 % avec 3 destinataires** de ses 34 transferts sortants (32,1 M vers 16 wallets). Swaps plus transferts, base commune : 37,3 % du détenu contre 40,8 à 43,7 % pour les 110 autres détenteurs d'au moins 1 M (exploratoire). Sur les seuls swaps : 22,5 % contre 35,0 %, une comparaison asymétrique à ne pas lire seule.
- **Total sur la durée :** 1 113 261 $ reçus pour 144 269 $ dépensés.
- Contient `5QhJJc…`, le wallet de la capture de @ramonos (URL @0xRamonos).
- **Explications alternatives :** un groupe de personnes qui se partagent des jetons, sans propriétaire unique ; des ventes de gré à gré ; un même service de gestion. Aucun nom n'est établi.

### Financement avant le mint : `G41vRrsHShLEvwMj58ruhqJycGfAtWXxtLD56uFExL8E`
Wallet actif depuis 26/12/2023, financé par ses propres ventes et par des échanges de jetons. Mint créé le 14/07/2024 02:05:25 UTC. Virements d'au moins 0,05 SOL de ce wallet, de 24 h avant le mint à 1 h après :

| UTC | Vers | SOL | Dans le groupe | A acheté sur le marché | Signature |
|---|---|---|---|---|---|
| 13/07/2024 15:55:26 | `45ruCyfdRkWpRNGEqWzjCiXRHkZs8WXCLQ67Pnpye7Hp` | 0,191365646 | non | non | `4DDtLbJF8T9LvrbCgpWrrXq6EHrd1H2dPdm92h9jwwj7NhSZSTpiRdwXS3vE2zBKbArW9GE1oaaAjs5NsLccMVYh` |
| 14/07/2024 01:46:23 | `EZXUvi4X5k3Aj99rGzNQoBtAzFqzYUjGhHNu8A1Ty8s4` | 0,5 | oui | oui | `2raMmNDhdkps29twoAGY8XwVuWDJX5rhnuyb444MKqKXcfRAzkdBqgGL7uoUqUVbiNjRpprutBj439VLhcvzoC4h` |
| 14/07/2024 01:46:41 | `4upmFYy6SpmCwdSRfG9akN2gRRn3DksLpDyN5YAmohbx` | 0,5 | oui | oui | `3uPFrKc46ZnxkeABVdGy7yJEp1N6WJXdi98t7pajgx6pTPNYTMVWFk1k3sWUdfYANARtrkW6uoTpMrVNHZW53md5` |
| 14/07/2024 01:52:15 | `2mW45kXp4Wd4xRkF2mmh5rKdzjnjbJR2o53skWcxGa2d` | 0,5 | oui | oui | `46z6pt7wxxZE2jqopbLYnHBsTcGNGJjpkarAqDBwtM69F6NWJ2ieRSM64SiRR1wvBdERDJakUXwapN5qNydhpDoU` |
| 14/07/2024 01:52:34 | `HkFSNPjNFUVtdykP8kSyWCKhocY85k1S4MyjXHNqesvv` | 0,5 | oui | oui | `dm7hUBrEefnSyQHJQwTYebwZyoxDrx26bzny9zSu7H9wDKh7wJML1Rv3x7u4U57qmshG268oLx2ssHGbncy5kMw` |
| 14/07/2024 01:52:57 | `CZsBW8yCGAiWwQ16VAokXE7h7qYL8spMA582X7F7g2jW` | 0,5 | oui | oui | `4orBM3TXymFdtJLsdCvoi63wbj9UdCPWpan1adUAvuR21UyMDWeoHvxhUufqFtDeRvaeemm6uEcEnzNDKNmcuYMU` |
| 14/07/2024 01:58:48 | `ADnZ9NdL9rHg7CL6CnAjEhPTuLsJnvLXrY9kbkhML5Ft` | 0,5 | oui | oui | `UQ5VEv315ou5SrYNwa27i7En7iqkHYuxTnNnUMof7N4qfvwy7DUKLJeoEFMbZRyeAnSV74YrQ6KncDJQPXxhPsr` |
| 14/07/2024 02:00:51 | `2BLSXbea4abffYCbs6pkCvPDChe9D4VNsfxJTAauQZPT` | 0,5 | oui | non | `5nsFsCir8Gfcr22J4pYXwgQ6FRTm9iLpsKPadKiEq97DyzYChAFD5ee4xxnfEjVWn1sVcpUWNNrcLxqbqt8z4P8z` |
| 14/07/2024 02:01:18 | `HB16TNghDeEjrSJ7MZw7dTYddLhUq1RXJ3Kxf2RV5Qi8` | 0,5 | non | non | `4NhwYABFzmq12QnDSuqqqTiCovPGeSgj4hJngy3NVBkDjpA7234aTv1Zei94CED39atwQPtLapBbeBakFV16jEBF` |
| 14/07/2024 02:01:45 | `C3i6zfhv9Bvr1QxzNEURzasSvyXPLTeMipS9hJmjGu3L` | 0,5 | non | non | `hgnwXjWCUWLuVDzctQh225npk79MH1Ut5iHrggQH7ohcwgJAfGTkcJ1EXkv2xrBoSMHedhrY1ViqnDw3Xf8v4tQ` |
| 14/07/2024 02:02:18 | `8xjM4fGgPCqY4okN8Dsj4FXSPDp19d3sJYuTVGs2jkUv` | 0,5 | oui | non | `9nAp8gU9FdGHsUBcXhjJHx568fY3nWzSFQ5gQYuBGTk634ArCs6DhqRu5wPz9XVuUDr4Z22EsehTWus7ENRdi4K` |
| 14/07/2024 02:02:57 | `HKXb8LfyzxYUgL1hhP8gtnXMCPnbJm6vNWMbVsmvy6WV` | 0,5 | oui | non | `3HagJEswRbBdAjnUyQpfqLCaRJNddNbuGnxgnwA4z41j3k6D7KzmFJJpwxj5TnfND94LtoEycKyW2P3icmesmLff` |
| 14/07/2024 02:03:23 | `HkrGvxapoqp6625TKs8v8tEyu6eDwuPxmPinRaGH6i4a` | 0,5 | oui | non | `612aPJCvejBt3BLdwZtGJLLYmEJ2a5ZVJDJTLykLD2MmPy5MMhv6brMq9CkjAWwLHMmBEWStdJcdK6bTFzRCVzWg` |
| 14/07/2024 02:03:38 | `FjuV7mJUyjMbDg41RybRRrTJu8UTPK6suURavt6ZRBkV` | 0,5 | oui | non | `3EW9Lb9WeqX5Ltk8GB2f4mi3wVtzX8orfNBjNCU7kMKmut7BG9RVypG7Yp56QfF2k9hbQGSKFV9YbjWRc3PaWQoD` |
| 14/07/2024 02:06:57 | `GFpqfjEQFhXRbWEJCwUqKuNjSNTCgqAsANMbVyTGmi1p` | 5 | oui | oui | `vBwvyXoZo6CX5j2gsD5mvVxPaxXcYRgKSq32y9zaPCrT5ZLStr8mrZBvEctZNqyxp6feD8qBHWJwUh4Cv9HN1Jj` |
| 14/07/2024 02:11:17 | `AW63YBXXsGcLPpsDTSrpBMdQ9QXtxTiHsTbcVkY6UFv5` | 2 | oui | oui | `63f5Ajy4BND4ZxrkBdHft3pRricQM57MbrqpJaFgFqU8xbLLnUPimkryWkobxAf8fwjNgs8GX5NbY5NFgq1G9htj` |
| 14/07/2024 02:16:00 | `AW63YBXXsGcLPpsDTSrpBMdQ9QXtxTiHsTbcVkY6UFv5` | 4 | oui | oui | `nuYyo3G4b83qFYdVw8GbW5YjabUc85C9SsPrYY2LJteSE7HRiGZNB67NpvMNHoGZpjAWsJX91grpuYBmxKSD8Rs` |
| 14/07/2024 02:28:26 | `5Q544fKrFoe6tsEbD7S8EmxGTJYAKtTVhAW5Q5pge4j1` | 4 | non | non | `5LiTyoCxVPNULBHtKvAY8LkLweP9XvHgFaAacjxj5n93ucsmxUWt4DV9RBBDhq13wTuuoXH1rApcwdoYc1vmh782` |

Virements de 0,5 SOL rapprochés avant le mint vers des wallets sans historique : A pour les virements, **finalité non établie**. Une partie reçoit ensuite des jetons de `GFpqfj…` le 21/07 à 08:00 UTC, sans acheter sur le marché. Premier financeur des membres, sur 33 historiques complets : 11 à 12 dans le groupe selon le seuil, 11 G41vRrsH (CZsBW8yC manquait).

### Autres virements de SOL avant le lancement
| UTC | De | Vers | SOL | Signature |
|---|---|---|---|---|
| 14/07/2024 00:52:29 | `74qFhHypY1zi8oS2KahqmwLfV8zMVbBiJ8uDdki8xPEb` | `6t2dz4jm3S8vJZCkWPhBxHStxFTC8wNV9QttTzfQrG7M` | 6,338753581 | `5k22G8taueTD8PpGnL8TKxTQNePBvkTyZrxsBEfRs5BSg1NGjg97mLZjF8RYyQk2GGiq7naCNZVD4aquUV8DKvPh` |
| 14/07/2024 00:59:41 | `6t2dz4jm3S8vJZCkWPhBxHStxFTC8wNV9QttTzfQrG7M` | `8YrEVPQqhs1zNsGUS5inFFqy5ziHaWdnVZXqysLThAh` | 1,980417484 | `hiJ6Tcf3nAqJWyZKBYgp5wPFyAzgwDGBXJhjry6FxLLrH7uyRK64iG6tD8bVzG9aYxbYZ41G96AXqbvcCCXQF7W` |
| 14/07/2024 01:00:08 | `6t2dz4jm3S8vJZCkWPhBxHStxFTC8wNV9QttTzfQrG7M` | `99Xrt5uuu2FdsgGzKo3wvs28Bw2KuUgxaeV5rTQZLkb` | 2,088986109 | `mAC1B5aCBzxn6dEzkb5Q8ovgLUcp85hhLmGnsoso7mKAduWkKWz6GDxCH4cDbF52Kb5ZRjGLuUmYcwMnSzHpFBS` |
| 14/07/2024 01:31:26 | `6t2dz4jm3S8vJZCkWPhBxHStxFTC8wNV9QttTzfQrG7M` | `AtZjv3DuV9cLn3Jxm72TMSdTN4aM6CrBaGyxUC4c2wDk` | 1,48 | `2KfJYWtCYt3fD4thFrjzSGBo5FM1wwDzMxwuCgPPQNuMUjju6xeetheQ2hBupsyH7FaFfGPa8v3h6AX8pEEjtmdr` |
| 14/07/2024 01:52:25 | `AtZjv3DuV9cLn3Jxm72TMSdTN4aM6CrBaGyxUC4c2wDk` | `6t2dz4jm3S8vJZCkWPhBxHStxFTC8wNV9QttTzfQrG7M` | 1,5 | `5TjD684TrYsN74wiZCWNC4B5e4JiBgZJ5XuhAagLhepHXgGNow2ga2RsFzi6t2moXMZhW2WQyKxgD2MGAM7Ec3Yj` |

## 4. Le périmètre du créateur : la série Coinbase et le compte de dépôt
Deux périmètres à ne pas confondre : le groupe de 33 relié par transferts de jetons, et le périmètre du créateur relié par la série et le dépôt. Le créateur n'est pas dans les 33 et n'échange aucun jeton avec eux : 0 arête. 2 des 33 sont dans la série, 4 sont expéditeurs de `9W9b3zgHH9mCEHDhsdbnbEPHStm9vvXS4aia4DWHBxpL`.

### Série du 14/07/2024 (N01)
Le 14/07/2024, de 01:32:23 à 01:40:50 UTC, 13 des 2 201 destinataires de 3 hot wallets Coinbase sur 2 h reversent ensuite à 9W9b3zgHH9mCEHDhsdbnbEPHStm9vvXS4aia4DWHBxpL, dont le créateur et 5QhJJc. Aucun des 2 188 autres. 13 sur 2 201, tous dans 507 s ; CV des écarts 0,245, P 5e-05 ; témoin même matin, 44 wallets dans 4 fenêtres : au plus 3 sur une même destination par virement pur, contre 10 avec la même troncature, 13 sur l'historique complet. Limite : témoin de 4 fenêtres, un seul matin. Le filtre sur les montants a été choisi après avoir vu le créateur, mais le résultat n'en dépend pas.

| UTC | Hot wallet | Destinataire | SOL | Reverse ensuite à 9W9b | Dans le groupe | Signature |
|---|---|---|---|---|---|---|
| 01:32:23 | Coinbase3 | `8YLEuUtZ4eFMJbf46oNb1CeG6dYFWGyxnQSh9hrgzBzR` | 0,5 | oui | non | `5Ys6ggx4Fr3eYA4fdaDwowiuZg4HEbcRd6MYcPfspDX3g9KzLKMuKVh7ukUNVy3bpZwwhFT9ZLe2tQFMunHea4Dd` |
| 01:33:05 | Coinbase3 | `GoPCTrS3Ffz5wgWSP6Ef3U6NvZzJkUA3Qy8ZJ3rLMXHC` | 0,5 | oui | non | `4QxgQHNQtkWzir3nr5qZr6CfaWJf7ZUzw3wMoksBUUjLS8nofh9jGT3yDxSrDdMLt3fpUirEPehcHjkA13PKGYky` |
| 01:33:30 | Coinbase3 | `AFDkwJXJPCkZUjGo4mrrRZY53xU1vMSvXsyQiKdEZN93` | 0,5 | oui | non | `67gZiXkLDwerix8bnJCoPfY73SRAqK5DzyRALZjdWaz47zWTAoNd2HN7SN9rnNpELpZTaBjEaCG4W3kzGDqAd3PG` |
| 01:34:09 | Coinbase3 | `A52fNskQkLPD6oBdXFwznrmrT52jNdgvh2MCRWGqaiCW` | 1,0 | non | non | `4Nmd3bncho3u7aLQXcqFqbSTmRZ2fgd8qHWZZjogyo3ENdCLbgJxkRuRxg4YDQhexJp3hkvdQYq4gaCbeS9uStup` |
| 01:34:15 | Coinbase3 | `EEpSRR12vTrH3Wbf3Ke4vT4RkMfPTqFv5wfE948cr3Wa` | 0,5 | oui | non | `4918LwRUfs95omfpgBKMToNq7DYi98Fh1sVMWgo8zLVxTusHRoVZyoQhA65f7aRxwjowKnmSrDNGwLwSpSG4GaWh` |
| 01:35:00 | Coinbase1 | `6ty9DM4s2mNvsMpMrcaXBDVguFHapfwK9g7WdD9DBLgM` | 0,5 | oui | non | `21RBuWf1mKgUFfhUKBmtfKqi6nEGJeSqmM7FNGm8CBgASAy1S48ot45h6uQKypq3udmMoNSd8QvkmVAKUxEXpUoq` |
| 01:35:40 | Coinbase2 | `ERMtiLodeVKQ8sK1MBPgBHyJS6DT8j61z8aQJiKYqbCH` | 1,0 | oui | non | `5NUDHAsyv7tMN8wi6Tb4AvCHDo1uUhjeQbxB2v5E6zML8YizAVdPNxBxSVv49ZQbDPV9s6ASSurMszxPkZXvNWYF` |
| 01:36:14 | Coinbase2 | `HqwpWyvbCbGSbGuK1xFRptPdMYd8MHERqNJ3uACRCAmZ` | 1,0 | oui | non | `gUQjZXYWfo5paEpR8ep2zCk9EEeGuftqUL8cEyv1VkQrsrMYzPFjCZo7yWM4JLZfH18fPWzo729TMXyqC3CtKg1` |
| 01:36:57 | Coinbase1 | `6ZMaqHjPYpPdYor9qNGJP7bmunaFCuWcDVjDkR5H3b1J` | 1,0 | oui | non | `a8LwZn4nQUUA7j51Sc8pCCk4y2AZeH8GCMkaFHJqha8SePJxeSRi5Ttx2sy1gYCa9wUmguiKoThzt7vEAG74PE7` |
| 01:37:49 | Coinbase3 | `5s3ogzsq8cvwHtS1B6MhwUUp9CyzugJ6y3WqLPM9Ee3C` | 1,05 | oui | non | `3xgsew5Ua5zxFwZ7HcVLhDAvzBoGrSmha9dZQV9GzXe4Tpqw5bkAUP3CaKisGWghBf9drGJhFApgUyFBLsPTKpUY` |
| 01:38:21 | Coinbase1 | `Fp6kgqHUHFxdCVNRf1Z4bt4F1K5DK5Njq83PUNzUsGRt` | 1,05 | non | non | `3qnLH9qL4aUj6JLaP3vw8BetmFMYa9sowoivhRTJ2e64X4XPrAFLMJAmk1tQTttNSfUz7rhpvLvfVc8Mbwr9hn4j` |
| 01:38:58 | Coinbase3 | `7FGoCB63x3FAJNF25MMZG8pheR4rRtJbApQuynJRxLdE` | 1,05 | oui | oui | `2sPrsWKLgo452VgDLu7QJWFAF3VRHw2jmGJpB6ZLLsxHe9oyisyUkJ6H8WaLLWaR9UCJLFcdYu1zJ84rejJgDiKz` |
| 01:39:38 | Coinbase3 | `Gmc1EGGV4TQfS3Hs8qvNV6u9MMWoS6AJ6f6WLHS9VRjd` | 1,05 | oui | non | `4VdpfqKkCBzeEMF7LXibn4j7UydVsrpiCDLGDpS896HYMHHbXLwX9ENV61PZXPGmmudqMhdnLXbHa4pXJefyTkXg` |
| 01:40:13 | Coinbase2 | `4pKFTQxsc69nzioRwPuAwUm49MRP4KzBmvrfjRCpEe5g` | 1,05 | oui | non | `2r6gBypSxfzq8yT3Y7qQ5SNpqT3XiYs175BEthroK5ZtKnoGTewwaQhDqZeK12YzoBZhE7vzCHfApNuXKvEraNoG` |
| 01:40:50 | Coinbase2 | `5QhJJcFZu2ashyKyWSTGHcsyo6ZBCbpVuJqeutvQHScd` | 1,05 | oui | oui | `RpB7AKeKUJMiJ3rRKBtdxuuHsFvGrDN8gVKNxKFCaBQ64A5rxB2YuVVv5KnvWvw3asdg5ZGmq1KWob1wuhPPVdR` |

Exploratoire. Même habitude hors de la série : 3 wallets de 23:37:51 à 23:40:16 le 26/06/2024, 2 wallets le 23/08/2024, financés par Coinbase et reversant à 9W9b.

### `9W9b3zgHH9mCEHDhsdbnbEPHStm9vvXS4aia4DWHBxpL` : un compte de dépôt Coinbase (N02, N03)
Sur tout son historique : 88 entrées de 48 expéditeurs, 956,5 SOL entrés, 956,5 SOL sortis, dont 94,5 % vers Coinbase 1, 2 et 3 : c'est un plancher, 100 % avec les 6 adresses présumées de la même famille (`data_v2/collector.json`, liste séparée `evidence/labels/hot_presume.tsv`, jamais une étiquette vérifiée). Délai médian entre une entrée et la sortie suivante : 126 s.

- **B, le type de compte :** 100 % des sorties vers 3 hot wallets et 6 adresses qui balaient 53 dépôts témoins sur 120 ; 59 balayages signés par 9W9b ; 155 000 lamports en frais principal, comme 105 témoins sur 120.
- **B, un même compte de dépôt ; C, un même bénéficiaire :** 31 des 48 expéditeurs de 9W9b touchent DMAGA, contre 8 expéditeurs sur 1 365 dans 120 dépôts témoins. 31 sur 48 ; 16 sur 33 hors série et hors groupe ; témoin 8 sur 1 365, 7 dépôts, au plus 2 par dépôt. Un trésorier ou un opérateur pour plusieurs personnes reste possible. La rafale de 9 ne sépare 9W9b que sous le filtre choisi après coup : sans filtre, 4 témoins sur 120 atteignent 9 et le maximum vaut 18.
- **Limite :** un compte unique tenu pour plusieurs personnes, par un trésorier ou un opérateur payé pour un lancement, reste possible. Seule une réquisition de Coinbase trancherait.

| Salve | UTC | Expéditeur | SOL | Rôle | Signe | Signature |
|---|---|---|---|---|---|---|
| 23/07/2024 | 23/07/2024 02:14:06 | `EGtyQEgMKGKXjppDqj9sYy97e9m7nvu1US4SfFXNakMy` | 7,9 | autre | oui | `2mC7gPb89CVz5aZ2sn86v3XmFxYFxsWrTE5Nt2mF6WQdZz3R5k3joi9xMCUwUXg2DZrunuZ1DJdS8q5fNZ1Ubozg` |
| 23/07/2024 | 23/07/2024 02:15:07 | `G41vRrsHShLEvwMj58ruhqJycGfAtWXxtLD56uFExL8E` | 8 | autre | oui | `4e3Pg7TvkWucWVKUM5Mymc88jApjREYNsUGk9gSH9gqGWCSEBUQHPdaboYRoMTCP6hPEhw693BGh7iHnZsr3fgZN` |
| 23/07/2024 | 23/07/2024 02:16:17 | `C73Yv9iHmTaf8SU2XFnGLt7QXUDqbeWNtUYza9WJhkae` | 8 | groupe | oui | `25u4vvqJkg7CTmCnEZQSRwjXG6tbjBYMq4tLtZEQqWYg6r8HfqDAuUutacKtYs1PQgce8ikjHq9vREX7PtyGrGt6` |
| 23/07/2024 | 23/07/2024 02:16:50 | `AtZjv3DuV9cLn3Jxm72TMSdTN4aM6CrBaGyxUC4c2wDk` | 8 | groupe | oui | `KJDdVPyYmAUHioiv1Cf6ihJLLX6jhgieTqnUp7hobUWGEVbd5ysM2SXZY8ewBd8Mx7YBnm8gjFGYqXVJ9ZT9u73` |
| 26/01/2025 | 26/01/2025 16:11:24 | `8YLEuUtZ4eFMJbf46oNb1CeG6dYFWGyxnQSh9hrgzBzR` | 0,593 | créateur | oui | `65aNPjoC8nb4yUu3oD5HGzSvyC9DLJZEK1LrkDD8hEXPzdv8Y4FJRgJEXZXXbDuHtYi8UNU7XYdmycKwNi2BS3g2` |
| 26/01/2025 | 26/01/2025 16:12:33 | `EEpSRR12vTrH3Wbf3Ke4vT4RkMfPTqFv5wfE948cr3Wa` | 1,225 | autre | oui | `3g492tmEQGG1M923UHFHwia4DWVy5Ast2LHRocmuGmGdEcjEHgaTBUFRqQBe1R5ie8B5Cgcb8j7sNaEeo4xNc6Zo` |
| 26/01/2025 | 26/01/2025 16:13:10 | `7FGoCB63x3FAJNF25MMZG8pheR4rRtJbApQuynJRxLdE` | 0,1 | groupe | oui | `4geocgyKWbAfcV7rpgEMYU8G7zoKCYwGeRVwL3QEJUNbUQPTgpmoLGak87yF6nMUK8gsK6bWqF2TbrsHGbBxXXsZ` |
| 26/01/2025 | 26/01/2025 16:13:59 | `4pKFTQxsc69nzioRwPuAwUm49MRP4KzBmvrfjRCpEe5g` | 0,1 | autre | oui | `pqvUAXC3n51dFM1XsEjRo6ebiBhzwMAmquPZmDYB8N22wYUBNM2Kn9qYkUR6YJUHW6MdgczW21KAPhJUeFk5TRW` |
| 26/01/2025 | 26/01/2025 16:14:34 | `5QhJJcFZu2ashyKyWSTGHcsyo6ZBCbpVuJqeutvQHScd` | 0,125 | groupe | oui | `1Ae21aJQzoAv6aa6pxkUVAXaCYHXXah5sUopKdEBJ1n5rgtDkfveDvxvdJHW6awLo1PjTJ7ERBWNhp3EEEsTMmi` |
| 26/01/2025 | 26/01/2025 16:15:09 | `HBsgbpsM1j1YsNYqtCXcFU4mCRofwcor2qFwifNqddmH` | 0,322 | autre | oui | `YyU6PFfUJeS1Qz6s8a6ehWDJhic6gJJhMX9GjbQHN5mn1oJdpQ9T3ERPY5B4Xf95jcXvRz3tnHsRioV6x7XWjfS` |
| 26/01/2025 | 26/01/2025 17:13:19 | `9PoYaK2NZziWAswo5eNCaLbdqh6t28pq89qMnS5C3m5n` | 0,141 | autre | oui | `WQ44rsdxJorCnxxnh6QZExQ97Hb9y7cPLvxXsEAcqgxjU7PykSjNAXzZZwsr9cNucvzC1HyiJp8nEP3EAimFKrH` |
| 26/01/2025 | 26/01/2025 17:14:10 | `HR3oD1C3DX5CfKyZ13xBQF2pJFTWWYfgxadFiYuvJNeM` | 0,524 | autre | oui | `5i6xdmAmkBr7yg1edy5NyPJypSxAGm62k8czbtbxSja11sUmp3HnnUeoAcLKhq4GVS7CtLhBdxapfx5VdXPP4Znx` |
| 26/01/2025 | 26/01/2025 17:14:45 | `G9uiJWzsPUoDuZKXEWSBvEtCi5NtU6iCQc6SeBPSRScT` | 0,4 | autre | oui | `2cHX7CBv2pmAayFTUSYqL7nRf1tJeKDpFYr77KgCh1WbC3cG3tz2Lx1DNGFdtk3Fy4se5MJsQpmxC2gmpQ87AndW` |
| 26/01/2025 | 26/01/2025 17:15:24 | `9iDacNdyxnETd5FHGhzTF3TFmviy4dxKFnW7kgb9bwyQ` | 0,285 | autre | oui | `2ambyDw623xAQ7L1BjY3Q8c7iDf1dQNNLgZtNemXUNjCrrKniSR9ukvMwwD3wKRGBZNmeH4Dg2LM85aPSbWWQi4L` |
| 26/01/2025 | 26/01/2025 17:16:02 | `ERMtiLodeVKQ8sK1MBPgBHyJS6DT8j61z8aQJiKYqbCH` | 0,109 | autre | oui | `36b2qawqdK2zuSRt1mXriKA1zBdJh8ZFBFnJyBsntiLmxcGoryz29d3LtyzCb6bnNX2m7KGmjpX9Rr53kDNj8kfG` |
| 26/01/2025 | 26/01/2025 17:16:35 | `HqwpWyvbCbGSbGuK1xFRptPdMYd8MHERqNJ3uACRCAmZ` | 0,276 | autre | oui | `V9VJtMmbGG4Kdv8bWf8QQ3MJuQqRjvwae9matym1wM4zR8JV5n4HbrxNFz4ATd27A8xqewR1NoBv8yUxo79TBZA` |
| 26/01/2025 | 26/01/2025 17:17:13 | `6ZMaqHjPYpPdYor9qNGJP7bmunaFCuWcDVjDkR5H3b1J` | 1,07 | autre | oui | `42amhNKv2GCwHsHAETZiET45yXBbmuhEEH9DwytEX3wDvybrCwXsTGvfA9gRC8MJ9zjaaizHDKdHdexTPHuNtzFB` |
| 26/01/2025 | 26/01/2025 17:19:04 | `9Dxk6iLz9Dazwy6E8DEEjnGyDMSgj4DyfVERVfwXZMMo` | 0,139 | autre | oui | `hSnBpr3CPuqckzzzbvzpEkG6bHGMFUP5qBYPNQCyV52EUfkWbSnGqWFQu2ZgzgL9fyaJabA4N4NBHwH7GfR9uLr` |

### Deux périmètres, en jetons à la borne basse (N06)
33 wallets : 217,04 M. Série de 15 : 61,36 M. 48 expéditeurs : 92,08 M. Union de 79 adresses : 266,70 M, 28,4 %. A pour les soldes, C pour un seul acteur. L'union n'est pas un groupe : elle additionne des périmètres que rien ne relie à coup sûr.

### Transferts directs de DMAGA du groupe, par date
| UTC | De | Vers | Jetons M | Signature |
|---|---|---|---|---|
| 14/07/2024 02:27:51 | `6t2dz4jm3S8vJZCkWPhBxHStxFTC8wNV9QttTzfQrG7M` | `AtZjv3DuV9cLn3Jxm72TMSdTN4aM6CrBaGyxUC4c2wDk` | 13,194 | `58SeigZv41h279aBndachahiym3sg3MMW3EJAUTrHkmX3hP4YkJcvXBQEzYNvp1qS7iVXEEDJPfoNvNoBXQzkXxq` |
| 14/07/2024 02:42:13 | `6t2dz4jm3S8vJZCkWPhBxHStxFTC8wNV9QttTzfQrG7M` | `AtZjv3DuV9cLn3Jxm72TMSdTN4aM6CrBaGyxUC4c2wDk` | 13,194 | `25Rr8TxztffbE9bQ7gFTXq6fiTQodV4bipqzUgCBohVKzuziGgDWGTNfLUwi1dxHWuz5uBrLRauRvTt1tYVgCV1o` |
| 14/07/2024 02:42:55 | `AW63YBXXsGcLPpsDTSrpBMdQ9QXtxTiHsTbcVkY6UFv5` | `AtZjv3DuV9cLn3Jxm72TMSdTN4aM6CrBaGyxUC4c2wDk` | 15,442 | `3SPjHWiXAPwiZiyx48xDg5QX53fbREFAccALGSn91xwPUP21kEpcjQtzSgoGxFngVuZ8B4guYRz4AJyQRuMSuwrZ` |
| 14/07/2024 02:46:05 | `AtZjv3DuV9cLn3Jxm72TMSdTN4aM6CrBaGyxUC4c2wDk` | `NxtXcmEW3gQvrCdBEm5GYT3zaqMre3QiPUhnwViNsD7` | 41,000 | `dLnMuAksDjjA1ioFbB4SPDNPLFURnrp6bxwYjwBLFYvYLTRBEDUN8eFpQ2zwySyXdHu34UijFYN1Bcnv17ivDnM` |
| 14/07/2024 02:46:40 | `8YrEVPQqhs1zNsGUS5inFFqy5ziHaWdnVZXqysLThAh` | `AtZjv3DuV9cLn3Jxm72TMSdTN4aM6CrBaGyxUC4c2wDk` | 23,409 | `5PUhHWoEJFPKT8KZcQwvFwbryTBN7LukVLGveNZ5SbzPUMpUfJqNaThGNxiDygFHixkKrgedTmZSeuoAKU4PpRBA` |
| 14/07/2024 02:47:00 | `99Xrt5uuu2FdsgGzKo3wvs28Bw2KuUgxaeV5rTQZLkb` | `AtZjv3DuV9cLn3Jxm72TMSdTN4aM6CrBaGyxUC4c2wDk` | 19,032 | `yYbHzxm5fWkf5gn57NyvSeQ5pB7zcnj9YmYwNpzAiTD1vXVCepaZqtojy75NCg13E2dGrQ7UfZsW8LKwBBPjeva` |
| 14/07/2024 02:58:20 | `AtZjv3DuV9cLn3Jxm72TMSdTN4aM6CrBaGyxUC4c2wDk` | `35nAuv6jGTVMnr7qdiRAV5PbZ3QgTJcLzBFzxGFm6Xw8` | 1,000 | `23HGSm5eRfsiQ1WWC9FkFkCe7vRqW35MEWZDZpbodVFRwZ11K5euN3m8f2PJGwiTxCeaSVcsFFmfBU7TAmDfgRYe` |
| 14/07/2024 02:59:22 | `AtZjv3DuV9cLn3Jxm72TMSdTN4aM6CrBaGyxUC4c2wDk` | `35nAuv6jGTVMnr7qdiRAV5PbZ3QgTJcLzBFzxGFm6Xw8` | 20,000 | `3UyPx8AxE7mUp1ge1P5EhJfejZ3YoP3VWqEixFyBAVDvBN4DVNjTuzxQWYnDW68bvh9Qfn2Pz28kS3hQW44cujax` |
| 14/07/2024 03:47:53 | `AtZjv3DuV9cLn3Jxm72TMSdTN4aM6CrBaGyxUC4c2wDk` | `74qFhHypY1zi8oS2KahqmwLfV8zMVbBiJ8uDdki8xPEb` | 22,468 | `T2L2UReeEkCbsPgLBaw68VEf4Vd9qs46UgfiiHt6Ju8grEAi9dPTKjavrt5QH7FeCjGUirUsmoJGdd4cG6RGTEw` |
| 14/07/2024 15:59:18 | `5QhJJcFZu2ashyKyWSTGHcsyo6ZBCbpVuJqeutvQHScd` | `9u5JKgWdLzj4xUiA4sFnaaJeKAJF8zBXExatxeSZHMkP` | 2,500 | `3Dc3PHFXpiQC5DBPAEBCpHZrdpLddoegVLv7EXReGnbeHBd3PgyisbbiNndakAEDEK6ak6i7YUZMxqEAY9AsvgEN` |
| 15/07/2024 01:14:34 | `NxtXcmEW3gQvrCdBEm5GYT3zaqMre3QiPUhnwViNsD7` | `5QhJJcFZu2ashyKyWSTGHcsyo6ZBCbpVuJqeutvQHScd` | 8,000 | `2o4UXdGtAFqxWc9kGkLxfTFEyVX8vJDuebnk6eG7Umicp74VqVUpGwzZWXBeJeXds5SP52N6NRMYyxtEZbi6xd57` |
| 15/07/2024 08:31:02 | `Ei5yGz8dPndr1aCeHZsfqJBcS3VBbz75VHEhxxJKLy3V` | `HGBiExZRtD2TZdQLWHE9azkTSmE2z7ygKqZMtehJDKYU` | 20,000 | `4o5iDAKTDxsTfFZRGaDD4v1oMhdHaNg2rPsVcp9j376kEVWUQ3oTTsvFKohRCo9LzLjYkcqW2v9pL9Uobco5aHuS` |
| 15/07/2024 08:31:48 | `Ei5yGz8dPndr1aCeHZsfqJBcS3VBbz75VHEhxxJKLy3V` | `Gcyg2jeLfSY9gxxHf5za5QU74ijtxBb1dB2mdGSPZH3m` | 20,000 | `36ZAKhxA668TnJrwdtu1k4RLftbgsuneV4yqK6udP6m8wC66xWbzs7mE8WLAEYxF6uUFwv1kk97dDwyqaxinVeu2` |
| 16/07/2024 02:50:16 | `74qFhHypY1zi8oS2KahqmwLfV8zMVbBiJ8uDdki8xPEb` | `GPMYCuusSYfgdXXYHLyCBhBdhP9fJeXrSGUou6XAxHgm` | 3,000 | `3nAsMtixRcs8iFSLuFwKzycFqrD7sSkuezANziRLWaoq3mbWSDivWvNyWp46ZePmwkXwAumZVMeD6orz8kBoJzTR` |
| 16/07/2024 05:39:16 | `Ei5yGz8dPndr1aCeHZsfqJBcS3VBbz75VHEhxxJKLy3V` | `4wComYHQbydc9DZHsDu3t2MaTLNe7Y3ukdymrkqh9ftC` | 10,000 | `3DrUiH8LpUbfby6HqZwExUXKVXnv9m3DJeVDUEyJsdMCts3UwwmtUCg5wxvdATS375vUW2vT9eDd3az4RevHU4PE` |
| 16/07/2024 17:25:53 | `NxtXcmEW3gQvrCdBEm5GYT3zaqMre3QiPUhnwViNsD7` | `7FGoCB63x3FAJNF25MMZG8pheR4rRtJbApQuynJRxLdE` | 6,000 | `62tygY7itaqFGtzbgVFiakE6za6jkZ7UVXRUxYJ3LoGFH4zxcyKHGXjts2yjUHkjWopTV3MQLuDYrazEBpgNmjbX` |
| 18/07/2024 21:05:52 | `5QhJJcFZu2ashyKyWSTGHcsyo6ZBCbpVuJqeutvQHScd` | `7mdCAs8CWYJxkWz2gfj3sRhDBmUi6Q9qvRGuKiv2Bazu` | 18,000 | `2wxn47W59GaU8YcsTSVSJ1mufSe1g2xLjcAV3FJdu2RHx5zE6Sawncmw1W8A5PNw9u7qQpzZoxeiCGXYpC2zyTUB` |
| 18/07/2024 23:02:23 | `Gcyg2jeLfSY9gxxHf5za5QU74ijtxBb1dB2mdGSPZH3m` | `4wComYHQbydc9DZHsDu3t2MaTLNe7Y3ukdymrkqh9ftC` | 5,000 | `41Vk3oqdWv7FvH4Gv7DoL2MgAi2ouE5kUD7GfVfRpMB9KL78FgoHgMjqrVEGt6jwF3SjTf7KCFqppopJj5VCJ4DF` |
| 18/07/2024 23:12:43 | `4wComYHQbydc9DZHsDu3t2MaTLNe7Y3ukdymrkqh9ftC` | `74qFhHypY1zi8oS2KahqmwLfV8zMVbBiJ8uDdki8xPEb` | 15,000 | `1X9w8xLDu39Ti9TjHsJud4AMzcfFjso5KBo1WRrLoKep1PwZfQnrRuUL7hnR2QPn3SfngjKuLeqK3pKCP2o273G` |
| 18/07/2024 23:34:34 | `74qFhHypY1zi8oS2KahqmwLfV8zMVbBiJ8uDdki8xPEb` | `C7i9beNHXYonZYB5riXE6kaLpFWLj9BPzh2FSBoUUePK` | 4,960 | `3qNUwaAsFaTPBqSweMvHRqu7rcRyhhMp1EbkTbeXtauw5ooE9i48BzvGoLFWVJSqnZwQvKKvGdEMyB3x7uUn5BUy` |
| 20/07/2024 22:41:20 | `74qFhHypY1zi8oS2KahqmwLfV8zMVbBiJ8uDdki8xPEb` | `AtZjv3DuV9cLn3Jxm72TMSdTN4aM6CrBaGyxUC4c2wDk` | 9,000 | `4xQpXD9yRQpTtjH5HutQZRMioFDrj6tXcusVdhn3yWiuGnhH8e5qo1ArdfLsezQoCCVGiJexBadqCfG8JJxxeYnT` |
| 21/07/2024 07:57:16 | `GFpqfjEQFhXRbWEJCwUqKuNjSNTCgqAsANMbVyTGmi1p` | `FjuV7mJUyjMbDg41RybRRrTJu8UTPK6suURavt6ZRBkV` | 6,500 | `3veEUrS3QLEXT549REM6cwpvNbN88fYRmytscraZMmEfyJ19hHQ7J58vG8gjjpYgjxe3SY21sJ4zAx1fLzABvFpX` |
| 21/07/2024 08:05:08 | `GFpqfjEQFhXRbWEJCwUqKuNjSNTCgqAsANMbVyTGmi1p` | `HkrGvxapoqp6625TKs8v8tEyu6eDwuPxmPinRaGH6i4a` | 5,500 | `4dpeM7SmazH2Zcbg1KSYQat6koknDAVRaL4EfqFEcRpgwNJhoQ3VduTzo3XuRGXgdZM1HV2KfGoLvjh8jSmSnLTY` |
| 21/07/2024 08:15:06 | `GFpqfjEQFhXRbWEJCwUqKuNjSNTCgqAsANMbVyTGmi1p` | `HKXb8LfyzxYUgL1hhP8gtnXMCPnbJm6vNWMbVsmvy6WV` | 6,000 | `5WwzrXfzoGFbn1WDzgtNyLXLV4LazroRMfM92VJ7h2ak2mJGYPyif2GUZnAjh1vBCsyv6yDy9cgugL52xY454fJ6` |
| 21/07/2024 08:16:07 | `GFpqfjEQFhXRbWEJCwUqKuNjSNTCgqAsANMbVyTGmi1p` | `8xjM4fGgPCqY4okN8Dsj4FXSPDp19d3sJYuTVGs2jkUv` | 6,500 | `5Y8xw5RNMKw8VkyGtXNXQqzxo8o5BR7bNMLvJLuQaP9dBHzm8QmoKvpaiNsbLcBFRXydE54sn2C3dqnp7xE4WoE3` |
| 21/07/2024 08:17:04 | `GFpqfjEQFhXRbWEJCwUqKuNjSNTCgqAsANMbVyTGmi1p` | `ADnZ9NdL9rHg7CL6CnAjEhPTuLsJnvLXrY9kbkhML5Ft` | 4,500 | `4o48RsVcAk2vVxkGuDdJouKg8C1yrQVq5C4NrRiPPSdDbXb8YFhCfm8ZrnT7er9eZKm1oxYrGU8SAYtJZRoTz8D6` |
| 21/07/2024 08:18:58 | `GFpqfjEQFhXRbWEJCwUqKuNjSNTCgqAsANMbVyTGmi1p` | `2BLSXbea4abffYCbs6pkCvPDChe9D4VNsfxJTAauQZPT` | 4,000 | `4nZfXnxLLbAq6x6wcnePaGC1MtKgwpG9SQ8iCPQTBYAKMkof2zhQSomVfLo1CRKSgr8MnxNoEHfxTxvgoq9UXjN6` |
| 21/07/2024 08:24:02 | `GFpqfjEQFhXRbWEJCwUqKuNjSNTCgqAsANMbVyTGmi1p` | `ADnZ9NdL9rHg7CL6CnAjEhPTuLsJnvLXrY9kbkhML5Ft` | 6,500 | `4vrxTAL9rxMKNbCWKXdiS2i7K94ioiSpFjZBas9kLCic8FZiEoDANJpiRXyaL2T53UuJnKhRxSKH82WjjuZsiYcx` |
| 21/07/2024 08:25:14 | `ADnZ9NdL9rHg7CL6CnAjEhPTuLsJnvLXrY9kbkhML5Ft` | `CZsBW8yCGAiWwQ16VAokXE7h7qYL8spMA582X7F7g2jW` | 5,000 | `2SchdeAaMz6ENtrGSUy53dCT6RnmYWR5V1EaM5NGRLLem85dz4anmwsSC3sWLkfHRTJxpmoz3AxcAnrU2xem9omt` |
| 21/07/2024 08:27:31 | `GFpqfjEQFhXRbWEJCwUqKuNjSNTCgqAsANMbVyTGmi1p` | `HkFSNPjNFUVtdykP8kSyWCKhocY85k1S4MyjXHNqesvv` | 6,500 | `38k1RSPdjmDa5NtTPhycgoBZrwMGyhdqTTqt5ASuijaKs6EmP8yTS9uAX8yHGohwyVbipGA16soFL78d9vAH4Fax` |
| 21/07/2024 08:28:20 | `GFpqfjEQFhXRbWEJCwUqKuNjSNTCgqAsANMbVyTGmi1p` | `2mW45kXp4Wd4xRkF2mmh5rKdzjnjbJR2o53skWcxGa2d` | 6,000 | `sybo7NWx8CnNFZUBMHVF55dM1xCkReCKcqCstgjpaxxVRLW5CiR9EgFsxf65fdeJbKTwXUQE6b3oDbi25apxyGX` |
| 21/07/2024 08:30:38 | `GFpqfjEQFhXRbWEJCwUqKuNjSNTCgqAsANMbVyTGmi1p` | `4upmFYy6SpmCwdSRfG9akN2gRRn3DksLpDyN5YAmohbx` | 6,000 | `5VLZXvLgbZhFq9utwU3ew3HoWnoNj8sS27P5KHyRxBB4EfiGdjXuNadxpUt1Z1AYn3XfGF4FPw3WoamfX6eTehaZ` |
| 21/07/2024 08:32:13 | `GFpqfjEQFhXRbWEJCwUqKuNjSNTCgqAsANMbVyTGmi1p` | `EZXUvi4X5k3Aj99rGzNQoBtAzFqzYUjGhHNu8A1Ty8s4` | 5,200 | `5LT1iXn8RFaf8yCfGFxHNebbXmedJ2zVQ5nx5RxYAA2MBkqLRci9gxqqfVLxtdt8pwVZMfCW6aJGMTxpBF4wJm7P` |
| 21/07/2024 08:33:36 | `NxtXcmEW3gQvrCdBEm5GYT3zaqMre3QiPUhnwViNsD7` | `GFpqfjEQFhXRbWEJCwUqKuNjSNTCgqAsANMbVyTGmi1p` | 1,000 | `2epM63ZTNSNSmXDo87Xn7qrJKkRXLD1znE9awNj2u2QZkdS4VNNeAsBnkaBfJ1UK6YLh8UT9gQiStAHrZ6RcYa1R` |
| 21/07/2024 11:10:25 | `AtZjv3DuV9cLn3Jxm72TMSdTN4aM6CrBaGyxUC4c2wDk` | `Akp46DicpTMb9aDtZozTViYydsYH5NhcZACWokpzLaNB` | 6,000 | `3hksjHdcYBFMVG7FEhHL7t5Y6UHnV1d22RsrXECePeoCmpHbiXtH8TCLVEUo5uniJ7Tv87yCkXziEwgZ7tNMrsre` |
| 21/07/2024 14:22:00 | `FjuV7mJUyjMbDg41RybRRrTJu8UTPK6suURavt6ZRBkV` | `C73Yv9iHmTaf8SU2XFnGLt7QXUDqbeWNtUYza9WJhkae` | 6,500 | `27eg3oXLNmEsXVHiGGKX2iEgkrnAHNdLjmUHL8iKGcKjYx6SuSQ79b4tod2fghPjcwHWwqaFv91uUoRaNeQej9yu` |
| 21/07/2024 14:23:52 | `HkrGvxapoqp6625TKs8v8tEyu6eDwuPxmPinRaGH6i4a` | `C73Yv9iHmTaf8SU2XFnGLt7QXUDqbeWNtUYza9WJhkae` | 5,500 | `3Bo2GkFUGiaFY1tD1gN8Wg6mYLVN6zTcj1WkxSJ9KpHVPBf7F16UXUJe7onS6owxNWaErmeJVWwHCWPBeYr6XTBu` |
| 21/07/2024 14:24:21 | `HKXb8LfyzxYUgL1hhP8gtnXMCPnbJm6vNWMbVsmvy6WV` | `BuBXTWECG8Xk6wMgyvrK6LQdJBk1exhDaSqNa9nFnjx3` | 6,000 | `4jCSn4tyzEJsdKru3FNnkBGY9F78r5NrUaQMe88n4KZ1UuKUrjuf1W3xqkQbWJmwZDMkXF16cSq5g8Zz2cGVv45K` |
| 21/07/2024 14:24:45 | `8xjM4fGgPCqY4okN8Dsj4FXSPDp19d3sJYuTVGs2jkUv` | `BuBXTWECG8Xk6wMgyvrK6LQdJBk1exhDaSqNa9nFnjx3` | 6,500 | `2Suy76fcGaPbEyUg257C1RgWHCFBiGLbWFDZ81JMajd2yjpFVa62cN78qp1kG9v7urRB6Jh228on1GJmdw3AHfXN` |
| 21/07/2024 14:25:44 | `2BLSXbea4abffYCbs6pkCvPDChe9D4VNsfxJTAauQZPT` | `BuBXTWECG8Xk6wMgyvrK6LQdJBk1exhDaSqNa9nFnjx3` | 1,500 | `5fCYXrqB3SowvK43ZrJNn8bmg9EzqvrJ69V3xiTxAHMNc9Rw47aXMs262SDna9xaCZJda5NFUQRUSSApr4WnzGDN` |

### Membres
| Wallet | Acheté SOL, toute la vie | Acheté M, toute la vie | Réalisé SOL | Reçu par transfert M | Sorti par transfert M | 1er achat |
|---|---|---|---|---|---|---|
| `6t2dz4jm3S8vJZCkWPhBxHStxFTC8wNV9QttTzfQrG7M` | 2,05 | 26,65 | 0,0 | 0,0 | 26,7 | 14/07/2024 02:06:07 |
| `8YrEVPQqhs1zNsGUS5inFFqy5ziHaWdnVZXqysLThAh` | 1,00 | 23,41 | 0,0 | 0,0 | 23,4 | 14/07/2024 02:06:26 |
| `GFpqfjEQFhXRbWEJCwUqKuNjSNTCgqAsANMbVyTGmi1p` | 19,80 | 132,64 | 148,5 | 6,7 | 63,2 | 14/07/2024 02:07:26 |
| `99Xrt5uuu2FdsgGzKo3wvs28Bw2KuUgxaeV5rTQZLkb` | 2,50 | 19,03 | 0,0 | 0,0 | 19,0 | 14/07/2024 02:07:39 |
| `5QhJJcFZu2ashyKyWSTGHcsyo6ZBCbpVuJqeutvQHScd` | 53,36 | 40,27 | 74,2 | 37,8 | 76,3 | 14/07/2024 02:10:11 |
| `AW63YBXXsGcLPpsDTSrpBMdQ9QXtxTiHsTbcVkY6UFv5` | 5,74 | 15,44 | 0,0 | 0,0 | 15,4 | 14/07/2024 02:11:56 |
| `EZXUvi4X5k3Aj99rGzNQoBtAzFqzYUjGhHNu8A1Ty8s4` | 0,38 | 1,23 | 92,6 | 11,0 | 0,8 | 14/07/2024 02:12:27 |
| `7FGoCB63x3FAJNF25MMZG8pheR4rRtJbApQuynJRxLdE` | 1,00 | 1,41 | 35,3 | 19,5 | 19,7 | 14/07/2024 02:17:56 |
| `Ei5yGz8dPndr1aCeHZsfqJBcS3VBbz75VHEhxxJKLy3V` | 132,23 | 78,91 | 405,4 | 3,0 | 62,9 | 14/07/2024 02:18:03 |
| `4upmFYy6SpmCwdSRfG9akN2gRRn3DksLpDyN5YAmohbx` | 0,49 | 0,71 | 0,0 | 6,0 | 6,7 | 14/07/2024 02:20:36 |
| `2mW45kXp4Wd4xRkF2mmh5rKdzjnjbJR2o53skWcxGa2d` | 0,49 | 0,72 | 21,4 | 6,0 | 0,0 | 14/07/2024 02:21:01 |
| `HkFSNPjNFUVtdykP8kSyWCKhocY85k1S4MyjXHNqesvv` | 0,49 | 0,69 | 0,0 | 6,5 | 1,0 | 14/07/2024 02:21:49 |
| `CZsBW8yCGAiWwQ16VAokXE7h7qYL8spMA582X7F7g2jW` | 0,49 | 0,60 | 23,9 | 5,0 | 0,0 | 14/07/2024 02:22:41 |
| `AtZjv3DuV9cLn3Jxm72TMSdTN4aM6CrBaGyxUC4c2wDk` | 0,14 | 0,16 | 327,3 | 95,5 | 92,7 | 14/07/2024 02:25:33 |
| `C73Yv9iHmTaf8SU2XFnGLt7QXUDqbeWNtUYza9WJhkae` | 5,50 | 6,86 | 1 686,1 | 23,6 | 2,3 | 14/07/2024 02:43:33 |
| `74qFhHypY1zi8oS2KahqmwLfV8zMVbBiJ8uDdki8xPEb` | 3,50 | 11,49 | 4,8 | 37,5 | 26,5 | 14/07/2024 11:21:48 |
| `35nAuv6jGTVMnr7qdiRAV5PbZ3QgTJcLzBFzxGFm6Xw8` | 2,00 | 0,67 | 358,1 | 22,0 | 0,7 | 16/07/2024 02:12:04 |
| `7mdCAs8CWYJxkWz2gfj3sRhDBmUi6Q9qvRGuKiv2Bazu` | 339,50 | 62,18 | 43,0 | 18,0 | 1,0 | 23/07/2024 00:59:15 |
| `ADnZ9NdL9rHg7CL6CnAjEhPTuLsJnvLXrY9kbkhML5Ft` | 6,00 | 0,10 | 18,4 | 11,0 | 10,8 | 23/07/2024 15:20:24 |
| `HGBiExZRtD2TZdQLWHE9azkTSmE2z7ygKqZMtehJDKYU` | 248,00 | 3,02 | 681,8 | 20,1 | 13,1 | 27/07/2024 20:08:30 |
| `C7i9beNHXYonZYB5riXE6kaLpFWLj9BPzh2FSBoUUePK` | 8,74 | 0,19 | 378,0 | 5,2 | 0,0 | 05/10/2024 23:02:59 |
| `2BLSXbea4abffYCbs6pkCvPDChe9D4VNsfxJTAauQZPT` | 0,00 | 0,00 | 46,8 | 4,0 | 2,0 | n/d |
| `4wComYHQbydc9DZHsDu3t2MaTLNe7Y3ukdymrkqh9ftC` | 0,00 | 0,00 | 0,0 | 19,0 | 19,0 | n/d |
| `8xjM4fGgPCqY4okN8Dsj4FXSPDp19d3sJYuTVGs2jkUv` | 0,00 | 0,00 | 0,0 | 6,5 | 6,5 | n/d |
| `9u5JKgWdLzj4xUiA4sFnaaJeKAJF8zBXExatxeSZHMkP` | 0,00 | 0,00 | 0,0 | 2,5 | 0,0 | n/d |
| `Akp46DicpTMb9aDtZozTViYydsYH5NhcZACWokpzLaNB` | 0,00 | 0,00 | 268,7 | 8,0 | 0,3 | n/d |
| `BuBXTWECG8Xk6wMgyvrK6LQdJBk1exhDaSqNa9nFnjx3` | 0,00 | 0,00 | 31,4 | 14,2 | 14,0 | n/d |
| `FjuV7mJUyjMbDg41RybRRrTJu8UTPK6suURavt6ZRBkV` | 0,00 | 0,00 | 0,0 | 6,5 | 6,5 | n/d |
| `GPMYCuusSYfgdXXYHLyCBhBdhP9fJeXrSGUou6XAxHgm` | 0,00 | 0,00 | 434,9 | 3,9 | 0,0 | n/d |
| `Gcyg2jeLfSY9gxxHf5za5QU74ijtxBb1dB2mdGSPZH3m` | 0,00 | 0,00 | 339,1 | 20,0 | 17,1 | n/d |
| `HKXb8LfyzxYUgL1hhP8gtnXMCPnbJm6vNWMbVsmvy6WV` | 0,00 | 0,00 | 0,0 | 6,0 | 6,0 | n/d |
| `HkrGvxapoqp6625TKs8v8tEyu6eDwuPxmPinRaGH6i4a` | 0,00 | 0,00 | 0,0 | 5,5 | 5,5 | n/d |
| `NxtXcmEW3gQvrCdBEm5GYT3zaqMre3QiPUhnwViNsD7` | 0,00 | 0,00 | 50,3 | 41,2 | 19,0 | n/d |

## 5. État des relectures
- **Audit du 03/11 (A données, B statistiques, C attribution, D confrontation) :** `audits/2026-11-03/AUDIT_FINAL.md`. Sur 51 assertions : 44 PASS, 5 FAIL, 2 INCONCLUSIVE. Ces corrections ne sont pas auditées : un nouvel audit des conclusions manque.
- **Reproduction :** les valeurs du test sont retrouvées par trois voies, audits A, B et D. Aucune trace d'une reproduction en copie vierge n'a été trouvée dans le dépôt.
- **Contrôles positifs :** contrôle de la plomberie seulement. Sur les vraies données, nul 2,4 %, effet moyen 3,3 %, effet fort 7,5 %.
- **Fait avant l'audit :** audit des échecs silencieux avant le gel (5 bloquants, 8 majeurs, 8 mineurs, corrections appliquées, non re-auditées) ; un audit indépendant des conclusions, rendu FAIL.
- **En attente de Benjamin :** amendement 001, projet d'amendement 003, nouvel audit des conclusions.
- **Registre :** voir `python3 ~/.claude/skills/etude-gelee/scripts/registre.py compter etude_final`. Les comparaisons des audits sont exploratoires, hors registre gelé.

## 6. Faux liens écartés
| Lien apparent | Pourquoi il est écarté |
|---|---|
| Le créateur et `9PrmF8…` ont le même premier financeur `GJRs4FwHtemZ5ZE9x3FNvJ8TMwitKTh21yxdRPqn7npE` | Coinbase 3 selon Dune Spellbook. Un même hot wallet n'est pas un lien |
| `H3QsBr…` et `9PrmF8…` envoient des jetons à `9UsmwVmbV4VwEwv5q5iZh4y3THh6dn2cqjFpEUrGRzZJ` | Réserve d'un pool Raydium CLMM : ce sont des ventes |
| `3LoAYHuS…`, `HFqp6ErW…`, `GP8StUXN…`, `3CgvbiM3…`, `7iWnBRRh…` sont reliés à `5QhJJc…`, `9PrmF8…` et `H3QsBr…` | Comptes de pourboire et de frais publiés par Jupiter (`jup-ag/docs`, DefiLlama), archivés dans `evidence/labels/`, classe `service` |
| `Habp5bncMSsBC3vkChyebepym5dcTNRYeg2LVG464E96` envoie du SOL à presque tous | Poussière de 0,0000001 SOL. Reste son arête de 8 M de DMAGA avec `5QhJJc…`, voir section 3 |
| `5QhJJc…` et le créateur envoient des jetons vers `JD25qVdtd65FoiXNmR89JjmoJdYk9sjYQeSTZAALFiMy` | Exécutant de Jupiter DCA : signataire, programme `DCA265Vj`, `InitiateFlashFill`. Ce sont deux ordres DCA, pas un destinataire commun |
| Le « créateur » DAS `TSLvdd1pWpHVjahSpsvCXUbgwsL3JAcvokwaKt1eokM` commun avec Kekius | Autorité de mint de Pump.fun, présente sur tous ses tokens |
