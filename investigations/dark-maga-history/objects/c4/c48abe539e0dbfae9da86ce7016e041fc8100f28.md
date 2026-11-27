# Coordination : tests et liens financiers

Généré par `scripts/rep_72_links.py`. Une arête prouve qu'une transaction existe. Elle ne prouve ni un propriétaire unique ni une intention.

## 1. Test gelé : DMAGA contre les autres pics tardifs
Plan gelé le 02/11/2026 à 23:47 UTC avant tout calcul (`etude_final/analysis_plan.md`, `PROTOCOL.lock`). Amendement 001 : R1 et R2 réduits, sans effet sur le verdict.

**Verdict calculé par le code : DMAGA NON DISTINGUABLE DE SES PAIRS**

Comptage : {"retenu_superset": 245, "pas_de_pic": 12809, "hors_bande": 453, "tronque_sans_pic": 135, "reporte_budget": 278, "moins_de_20_swaps_primary": 1, "moins_de_20_swaps_R3_S_moins_1h": 2, "moins_de_20_swaps_R1_10x": 1, "moins_de_20_swaps_R2_bande_large": 1, "swaps_manquants": 0}. Rejets du parseur : {"ruptures": 0, "tx": 15852824, "lp": 3458, "sens_opposes_ignores": 21559, "parts_de_frais": 469433, "swaps": 11878474, "sans_vault": 3581605, "non_signataire_deux_cotes": 394814, "sans_beneficiaire": 389287, "qty_differente_du_vault": 14461}.

| Mesure | Définition | DMAGA | Médiane pairs | P90 pairs | p de rang | k | Indéfinis | Passe Holm |
|---|---|---|---|---|---|---|---|---|
| M1 | Run-up 3 h | 39.867 | 3.755 | 163.089 | 0.1698 | 211 | 0 | non |
| M2 | Run-up 24 h | 9.371 | 1.464 | 64.565 | 0.1840 | 211 | 0 | non |
| M3 | Part des nouveaux wallets, 24 h | 0.680 | 0.450 | 0.863 | 0.2406 | 211 | 0 | non |
| M4 | Part des 5 premiers, 24 h | 0.308 | 0.347 | 0.784 | 0.5472 | 211 | 0 | non |
| M5 | Synchronisation, 24 h | 433.798 | 176.327 | 1115.392 | 0.2642 | 211 | 0 | non |
| M6 | Détention des précoces à S | 0.205 | 0.075 | 0.263 | 0.1557 | 211 | 0 | non |
| M7 | Plus gros achat / réserve, 24 h | 0.138 | 0.074 | 0.223 | 0.1792 | 211 | 0 | non |

Unité : le token. Fenêtres fixées par le pic S de chaque token (DMAGA : 21/07/2024 19:00 UTC). n effectif prudent : 84 jours de pic distincts. Le choix des mesures a pu être influencé par ce qui avait déjà été vu de DMAGA, jamais par les comparateurs. Variantes, jamais utilisées pour conclure :
- **R1_10x**, k = 212 : M1 p=0.164, M2 p=0.183, M3 p=0.244, M4 p=0.531, M5 p=0.258, M6 p=0.160, M7 p=0.202
- **R2_bande_large**, k = 240 : M1 p=0.207, M2 p=0.216, M3 p=0.282, M4 p=0.556, M5 p=0.282, M6 p=0.141, M7 p=0.187
- **R3_S_moins_1h**, k = 210 : M1 p=0.142, M2 p=0.166, M3 p=0.205, M4 p=0.557, M5 p=0.249, M6 p=0.152, M7 p=0.157

### DMAGA contre son propre passé (secondaire, Holm séparé)
| Événement | Heure E (UTC) | SOL acheté sur [E−3 h, E) | Médiane du passé | p | Nouveaux acheteurs | Médiane du passé | p | Fenêtres du passé |
|---|---|---|---|---|---|---|---|---|
| winig | 21/07/2024 16:02:29 | 401.5 | 6.1 | 0.036 | 44 | 1 | 0.036 | 27 |
| avatar | 21/07/2024 19:23:20 | 229.3 | 6.2 | 0.069 | 55 | 1 | 0.069 | 28 |

### Financeur commun
**Exploratoire, hors plan gelé.** Part des 50 premiers gros acheteurs qui partagent un financeur direct non service, dans les 72 h avant leur premier achat : DMAGA 0.08 (2 financeur(s) commun(s)), médiane des 40 comparateurs tirés au hasard 0.00, p de rang 0.073. Ce test n'entre pas dans le verdict et n'a pas de correction.

### Chiffres qui vont contre une ruée informée juste avant Musk
Voir `data/windows.csv` et `reports/EARLY_BUYERS.md`. Entre l'annonce de Biden et la borne basse du changement de photo (1.29 h) : 13.18 SOL d'achats contre 84.94 SOL de ventes, 3 nouveaux acheteurs. Le groupe ci-dessous fait 0 swap(s) entre le visuel et la borne haute.

## 2. Groupes reliés par transferts directs de DMAGA avant Musk
Règle : transfert direct d'au moins 1 M de jetons avant le 21/07/2024 19:03:27 UTC, sans passer par un service. Liens de SOL exclus de ce tableau. Jetons détenus par tous les non-pools à cette heure : 938 M.

| # | Wallets | Arêtes | Détenu avant Musk M | Part des jetons hors pools | Acheté M | SOL engagé | Réalisé SOL | Flux net SOL | P&L USD |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 33 | 40 | 217.0 | 23.1 % | 426.2 | 831.9 | 5,594 | 5,437 | 990,207 |
| 2 | 3 | 2 | 45.3 | 4.8 % | 59.2 | 18.0 | 22 | 6 | 1,009 |
| 3 | 2 | 1 | 36.8 | 3.9 % | 37.2 | 25.1 | 101 | 90 | 24,601 |
| 4 | 3 | 3 | 25.0 | 2.7 % | 25.2 | 33.1 | 6 | -27 | -4,399 |
| 5 | 5 | 4 | 18.3 | 1.9 % | 45.5 | 619.2 | 979 | 501 | 92,252 |
| 6 | 2 | 1 | 17.1 | 1.8 % | 24.6 | 1,219.5 | 1,499 | 1,296 | 236,123 |
| 7 | 2 | 1 | 14.2 | 1.5 % | 13.4 | 49.6 | 480 | 468 | 81,533 |
| 8 | 2 | 1 | 13.0 | 1.4 % | 18.7 | 206.1 | 763 | 731 | 128,033 |
| 9 | 3 | 2 | 11.5 | 1.2 % | 28.2 | 83.5 | 455 | 447 | 78,103 |
| 10 | 2 | 1 | 7.3 | 0.8 % | 7.5 | 22.4 | 159 | 158 | 28,415 |
| 11 | 2 | 1 | 3.3 | 0.3 % | 51.3 | 1,081.5 | 833 | 165 | 30,493 |
| 12 | 3 | 2 | 3.0 | 0.3 % | 3.6 | 21.0 | 207 | 186 | 34,297 |

## 3. Le groupe n° 1 : 33 wallets, niveau B
- **217.0 M de jetons avant Musk.** En première heure, le groupe achète 206.9 M de jetons pour 52.3 SOL.
- **0 swap entre le visuel de Winig et la borne haute du changement de photo.** Son geste du jour se fait avant : répartition le 21/07 entre 07:57 et 08:33 UTC.
- **Ventes :** 2,988.9 SOL dans les 6 h après Musk, 1,536.0 SOL dans les 18 h suivantes. Total sur la durée : 1,134,232 $ reçus pour 144,025 $ dépensés.
- Contient `5QhJJc…`, le wallet de la capture de @0xRamonos. Chacune des 40 arêtes a été relue sur la chaîne : la source signe, sans programme d'échange (`reports/data_checks/group_edges_check.json`).
- **Explications alternatives :** un groupe de personnes qui se partagent des jetons, sans propriétaire unique ; des ventes de gré à gré ; un chemin qui rassemble des wallets sans rapport par une ou deux arêtes, notamment `5QhJJc → 7mdCAs8C` ou `NxtXcm → GFpqfj`. Aucun nom n'est établi.

### Préparation : virements de SOL autour du lancement
Création du mint : 14/07/2024 02:05:25 UTC.

| UTC | De | Vers | SOL | Signature |
|---|---|---|---|---|
| 14/07/2024 00:52:29 | `74qFhHypY1zi8oS2KahqmwLfV8zMVbBiJ8uDdki8xPEb` | `6t2dz4jm3S8vJZCkWPhBxHStxFTC8wNV9QttTzfQrG7M` | 6.338753581 | `5k22G8taueTD8PpGnL8TKxTQNePBvkTyZrxsBEfRs5BSg1NGjg97mLZjF8RYyQk2GGiq7naCNZVD4aquUV8DKvPh` |
| 14/07/2024 00:59:41 | `6t2dz4jm3S8vJZCkWPhBxHStxFTC8wNV9QttTzfQrG7M` | `8YrEVPQqhs1zNsGUS5inFFqy5ziHaWdnVZXqysLThAh` | 1.980417484 | `hiJ6Tcf3nAqJWyZKBYgp5wPFyAzgwDGBXJhjry6FxLLrH7uyRK64iG6tD8bVzG9aYxbYZ41G96AXqbvcCCXQF7W` |
| 14/07/2024 01:00:08 | `6t2dz4jm3S8vJZCkWPhBxHStxFTC8wNV9QttTzfQrG7M` | `99Xrt5uuu2FdsgGzKo3wvs28Bw2KuUgxaeV5rTQZLkb` | 2.088986109 | `mAC1B5aCBzxn6dEzkb5Q8ovgLUcp85hhLmGnsoso7mKAduWkKWz6GDxCH4cDbF52Kb5ZRjGLuUmYcwMnSzHpFBS` |
| 14/07/2024 01:31:26 | `6t2dz4jm3S8vJZCkWPhBxHStxFTC8wNV9QttTzfQrG7M` | `AtZjv3DuV9cLn3Jxm72TMSdTN4aM6CrBaGyxUC4c2wDk` | 1.48 | `2KfJYWtCYt3fD4thFrjzSGBo5FM1wwDzMxwuCgPPQNuMUjju6xeetheQ2hBupsyH7FaFfGPa8v3h6AX8pEEjtmdr` |
| 14/07/2024 01:52:25 | `AtZjv3DuV9cLn3Jxm72TMSdTN4aM6CrBaGyxUC4c2wDk` | `6t2dz4jm3S8vJZCkWPhBxHStxFTC8wNV9QttTzfQrG7M` | 1.5 | `5TjD684TrYsN74wiZCWNC4B5e4JiBgZJ5XuhAagLhepHXgGNow2ga2RsFzi6t2moXMZhW2WQyKxgD2MGAM7Ec3Yj` |
| 14/07/2024 02:06:57 | `G41vRrsHShLEvwMj58ruhqJycGfAtWXxtLD56uFExL8E` | `GFpqfjEQFhXRbWEJCwUqKuNjSNTCgqAsANMbVyTGmi1p` | 5 | `vBwvyXoZo6CX5j2gsD5mvVxPaxXcYRgKSq32y9zaPCrT5ZLStr8mrZBvEctZNqyxp6feD8qBHWJwUh4Cv9HN1Jj` |
| 14/07/2024 02:11:17 | `G41vRrsHShLEvwMj58ruhqJycGfAtWXxtLD56uFExL8E` | `AW63YBXXsGcLPpsDTSrpBMdQ9QXtxTiHsTbcVkY6UFv5` | 2 | `63f5Ajy4BND4ZxrkBdHft3pRricQM57MbrqpJaFgFqU8xbLLnUPimkryWkobxAf8fwjNgs8GX5NbY5NFgq1G9htj` |
| 14/07/2024 02:16:00 | `G41vRrsHShLEvwMj58ruhqJycGfAtWXxtLD56uFExL8E` | `AW63YBXXsGcLPpsDTSrpBMdQ9QXtxTiHsTbcVkY6UFv5` | 4 | `nuYyo3G4b83qFYdVw8GbW5YjabUc85C9SsPrYY2LJteSE7HRiGZNB67NpvMNHoGZpjAWsJX91grpuYBmxKSD8Rs` |

### Transferts directs de DMAGA du groupe, par date
| UTC | De | Vers | Jetons M | Signature |
|---|---|---|---|---|
| 14/07/2024 02:27:51 | `6t2dz4jm3S8vJZCkWPhBxHStxFTC8wNV9QttTzfQrG7M` | `AtZjv3DuV9cLn3Jxm72TMSdTN4aM6CrBaGyxUC4c2wDk` | 13.194 | `58SeigZv41h279aBndachahiym3sg3MMW3EJAUTrHkmX3hP4YkJcvXBQEzYNvp1qS7iVXEEDJPfoNvNoBXQzkXxq` |
| 14/07/2024 02:42:13 | `6t2dz4jm3S8vJZCkWPhBxHStxFTC8wNV9QttTzfQrG7M` | `AtZjv3DuV9cLn3Jxm72TMSdTN4aM6CrBaGyxUC4c2wDk` | 13.194 | `25Rr8TxztffbE9bQ7gFTXq6fiTQodV4bipqzUgCBohVKzuziGgDWGTNfLUwi1dxHWuz5uBrLRauRvTt1tYVgCV1o` |
| 14/07/2024 02:42:55 | `AW63YBXXsGcLPpsDTSrpBMdQ9QXtxTiHsTbcVkY6UFv5` | `AtZjv3DuV9cLn3Jxm72TMSdTN4aM6CrBaGyxUC4c2wDk` | 15.442 | `3SPjHWiXAPwiZiyx48xDg5QX53fbREFAccALGSn91xwPUP21kEpcjQtzSgoGxFngVuZ8B4guYRz4AJyQRuMSuwrZ` |
| 14/07/2024 02:46:05 | `AtZjv3DuV9cLn3Jxm72TMSdTN4aM6CrBaGyxUC4c2wDk` | `NxtXcmEW3gQvrCdBEm5GYT3zaqMre3QiPUhnwViNsD7` | 41.000 | `dLnMuAksDjjA1ioFbB4SPDNPLFURnrp6bxwYjwBLFYvYLTRBEDUN8eFpQ2zwySyXdHu34UijFYN1Bcnv17ivDnM` |
| 14/07/2024 02:46:40 | `8YrEVPQqhs1zNsGUS5inFFqy5ziHaWdnVZXqysLThAh` | `AtZjv3DuV9cLn3Jxm72TMSdTN4aM6CrBaGyxUC4c2wDk` | 23.409 | `5PUhHWoEJFPKT8KZcQwvFwbryTBN7LukVLGveNZ5SbzPUMpUfJqNaThGNxiDygFHixkKrgedTmZSeuoAKU4PpRBA` |
| 14/07/2024 02:47:00 | `99Xrt5uuu2FdsgGzKo3wvs28Bw2KuUgxaeV5rTQZLkb` | `AtZjv3DuV9cLn3Jxm72TMSdTN4aM6CrBaGyxUC4c2wDk` | 19.032 | `yYbHzxm5fWkf5gn57NyvSeQ5pB7zcnj9YmYwNpzAiTD1vXVCepaZqtojy75NCg13E2dGrQ7UfZsW8LKwBBPjeva` |
| 14/07/2024 02:58:20 | `AtZjv3DuV9cLn3Jxm72TMSdTN4aM6CrBaGyxUC4c2wDk` | `35nAuv6jGTVMnr7qdiRAV5PbZ3QgTJcLzBFzxGFm6Xw8` | 1.000 | `23HGSm5eRfsiQ1WWC9FkFkCe7vRqW35MEWZDZpbodVFRwZ11K5euN3m8f2PJGwiTxCeaSVcsFFmfBU7TAmDfgRYe` |
| 14/07/2024 02:59:22 | `AtZjv3DuV9cLn3Jxm72TMSdTN4aM6CrBaGyxUC4c2wDk` | `35nAuv6jGTVMnr7qdiRAV5PbZ3QgTJcLzBFzxGFm6Xw8` | 20.000 | `3UyPx8AxE7mUp1ge1P5EhJfejZ3YoP3VWqEixFyBAVDvBN4DVNjTuzxQWYnDW68bvh9Qfn2Pz28kS3hQW44cujax` |
| 14/07/2024 03:47:53 | `AtZjv3DuV9cLn3Jxm72TMSdTN4aM6CrBaGyxUC4c2wDk` | `74qFhHypY1zi8oS2KahqmwLfV8zMVbBiJ8uDdki8xPEb` | 22.468 | `T2L2UReeEkCbsPgLBaw68VEf4Vd9qs46UgfiiHt6Ju8grEAi9dPTKjavrt5QH7FeCjGUirUsmoJGdd4cG6RGTEw` |
| 14/07/2024 15:59:18 | `5QhJJcFZu2ashyKyWSTGHcsyo6ZBCbpVuJqeutvQHScd` | `9u5JKgWdLzj4xUiA4sFnaaJeKAJF8zBXExatxeSZHMkP` | 2.500 | `3Dc3PHFXpiQC5DBPAEBCpHZrdpLddoegVLv7EXReGnbeHBd3PgyisbbiNndakAEDEK6ak6i7YUZMxqEAY9AsvgEN` |
| 15/07/2024 01:14:34 | `NxtXcmEW3gQvrCdBEm5GYT3zaqMre3QiPUhnwViNsD7` | `5QhJJcFZu2ashyKyWSTGHcsyo6ZBCbpVuJqeutvQHScd` | 8.000 | `2o4UXdGtAFqxWc9kGkLxfTFEyVX8vJDuebnk6eG7Umicp74VqVUpGwzZWXBeJeXds5SP52N6NRMYyxtEZbi6xd57` |
| 15/07/2024 08:31:02 | `Ei5yGz8dPndr1aCeHZsfqJBcS3VBbz75VHEhxxJKLy3V` | `HGBiExZRtD2TZdQLWHE9azkTSmE2z7ygKqZMtehJDKYU` | 20.000 | `4o5iDAKTDxsTfFZRGaDD4v1oMhdHaNg2rPsVcp9j376kEVWUQ3oTTsvFKohRCo9LzLjYkcqW2v9pL9Uobco5aHuS` |
| 15/07/2024 08:31:48 | `Ei5yGz8dPndr1aCeHZsfqJBcS3VBbz75VHEhxxJKLy3V` | `Gcyg2jeLfSY9gxxHf5za5QU74ijtxBb1dB2mdGSPZH3m` | 20.000 | `36ZAKhxA668TnJrwdtu1k4RLftbgsuneV4yqK6udP6m8wC66xWbzs7mE8WLAEYxF6uUFwv1kk97dDwyqaxinVeu2` |
| 16/07/2024 02:50:16 | `74qFhHypY1zi8oS2KahqmwLfV8zMVbBiJ8uDdki8xPEb` | `GPMYCuusSYfgdXXYHLyCBhBdhP9fJeXrSGUou6XAxHgm` | 3.000 | `3nAsMtixRcs8iFSLuFwKzycFqrD7sSkuezANziRLWaoq3mbWSDivWvNyWp46ZePmwkXwAumZVMeD6orz8kBoJzTR` |
| 16/07/2024 05:39:16 | `Ei5yGz8dPndr1aCeHZsfqJBcS3VBbz75VHEhxxJKLy3V` | `4wComYHQbydc9DZHsDu3t2MaTLNe7Y3ukdymrkqh9ftC` | 10.000 | `3DrUiH8LpUbfby6HqZwExUXKVXnv9m3DJeVDUEyJsdMCts3UwwmtUCg5wxvdATS375vUW2vT9eDd3az4RevHU4PE` |
| 16/07/2024 17:25:53 | `NxtXcmEW3gQvrCdBEm5GYT3zaqMre3QiPUhnwViNsD7` | `7FGoCB63x3FAJNF25MMZG8pheR4rRtJbApQuynJRxLdE` | 6.000 | `62tygY7itaqFGtzbgVFiakE6za6jkZ7UVXRUxYJ3LoGFH4zxcyKHGXjts2yjUHkjWopTV3MQLuDYrazEBpgNmjbX` |
| 18/07/2024 21:05:52 | `5QhJJcFZu2ashyKyWSTGHcsyo6ZBCbpVuJqeutvQHScd` | `7mdCAs8CWYJxkWz2gfj3sRhDBmUi6Q9qvRGuKiv2Bazu` | 18.000 | `2wxn47W59GaU8YcsTSVSJ1mufSe1g2xLjcAV3FJdu2RHx5zE6Sawncmw1W8A5PNw9u7qQpzZoxeiCGXYpC2zyTUB` |
| 18/07/2024 23:02:23 | `Gcyg2jeLfSY9gxxHf5za5QU74ijtxBb1dB2mdGSPZH3m` | `4wComYHQbydc9DZHsDu3t2MaTLNe7Y3ukdymrkqh9ftC` | 5.000 | `41Vk3oqdWv7FvH4Gv7DoL2MgAi2ouE5kUD7GfVfRpMB9KL78FgoHgMjqrVEGt6jwF3SjTf7KCFqppopJj5VCJ4DF` |
| 18/07/2024 23:12:43 | `4wComYHQbydc9DZHsDu3t2MaTLNe7Y3ukdymrkqh9ftC` | `74qFhHypY1zi8oS2KahqmwLfV8zMVbBiJ8uDdki8xPEb` | 15.000 | `1X9w8xLDu39Ti9TjHsJud4AMzcfFjso5KBo1WRrLoKep1PwZfQnrRuUL7hnR2QPn3SfngjKuLeqK3pKCP2o273G` |
| 18/07/2024 23:34:34 | `74qFhHypY1zi8oS2KahqmwLfV8zMVbBiJ8uDdki8xPEb` | `C7i9beNHXYonZYB5riXE6kaLpFWLj9BPzh2FSBoUUePK` | 4.960 | `3qNUwaAsFaTPBqSweMvHRqu7rcRyhhMp1EbkTbeXtauw5ooE9i48BzvGoLFWVJSqnZwQvKKvGdEMyB3x7uUn5BUy` |
| 20/07/2024 22:41:20 | `74qFhHypY1zi8oS2KahqmwLfV8zMVbBiJ8uDdki8xPEb` | `AtZjv3DuV9cLn3Jxm72TMSdTN4aM6CrBaGyxUC4c2wDk` | 9.000 | `4xQpXD9yRQpTtjH5HutQZRMioFDrj6tXcusVdhn3yWiuGnhH8e5qo1ArdfLsezQoCCVGiJexBadqCfG8JJxxeYnT` |
| 21/07/2024 07:57:16 | `GFpqfjEQFhXRbWEJCwUqKuNjSNTCgqAsANMbVyTGmi1p` | `FjuV7mJUyjMbDg41RybRRrTJu8UTPK6suURavt6ZRBkV` | 6.500 | `3veEUrS3QLEXT549REM6cwpvNbN88fYRmytscraZMmEfyJ19hHQ7J58vG8gjjpYgjxe3SY21sJ4zAx1fLzABvFpX` |
| 21/07/2024 08:05:08 | `GFpqfjEQFhXRbWEJCwUqKuNjSNTCgqAsANMbVyTGmi1p` | `HkrGvxapoqp6625TKs8v8tEyu6eDwuPxmPinRaGH6i4a` | 5.500 | `4dpeM7SmazH2Zcbg1KSYQat6koknDAVRaL4EfqFEcRpgwNJhoQ3VduTzo3XuRGXgdZM1HV2KfGoLvjh8jSmSnLTY` |
| 21/07/2024 08:15:06 | `GFpqfjEQFhXRbWEJCwUqKuNjSNTCgqAsANMbVyTGmi1p` | `HKXb8LfyzxYUgL1hhP8gtnXMCPnbJm6vNWMbVsmvy6WV` | 6.000 | `5WwzrXfzoGFbn1WDzgtNyLXLV4LazroRMfM92VJ7h2ak2mJGYPyif2GUZnAjh1vBCsyv6yDy9cgugL52xY454fJ6` |
| 21/07/2024 08:16:07 | `GFpqfjEQFhXRbWEJCwUqKuNjSNTCgqAsANMbVyTGmi1p` | `8xjM4fGgPCqY4okN8Dsj4FXSPDp19d3sJYuTVGs2jkUv` | 6.500 | `5Y8xw5RNMKw8VkyGtXNXQqzxo8o5BR7bNMLvJLuQaP9dBHzm8QmoKvpaiNsbLcBFRXydE54sn2C3dqnp7xE4WoE3` |
| 21/07/2024 08:17:04 | `GFpqfjEQFhXRbWEJCwUqKuNjSNTCgqAsANMbVyTGmi1p` | `ADnZ9NdL9rHg7CL6CnAjEhPTuLsJnvLXrY9kbkhML5Ft` | 4.500 | `4o48RsVcAk2vVxkGuDdJouKg8C1yrQVq5C4NrRiPPSdDbXb8YFhCfm8ZrnT7er9eZKm1oxYrGU8SAYtJZRoTz8D6` |
| 21/07/2024 08:18:58 | `GFpqfjEQFhXRbWEJCwUqKuNjSNTCgqAsANMbVyTGmi1p` | `2BLSXbea4abffYCbs6pkCvPDChe9D4VNsfxJTAauQZPT` | 4.000 | `4nZfXnxLLbAq6x6wcnePaGC1MtKgwpG9SQ8iCPQTBYAKMkof2zhQSomVfLo1CRKSgr8MnxNoEHfxTxvgoq9UXjN6` |
| 21/07/2024 08:24:02 | `GFpqfjEQFhXRbWEJCwUqKuNjSNTCgqAsANMbVyTGmi1p` | `ADnZ9NdL9rHg7CL6CnAjEhPTuLsJnvLXrY9kbkhML5Ft` | 6.500 | `4vrxTAL9rxMKNbCWKXdiS2i7K94ioiSpFjZBas9kLCic8FZiEoDANJpiRXyaL2T53UuJnKhRxSKH82WjjuZsiYcx` |
| 21/07/2024 08:25:14 | `ADnZ9NdL9rHg7CL6CnAjEhPTuLsJnvLXrY9kbkhML5Ft` | `CZsBW8yCGAiWwQ16VAokXE7h7qYL8spMA582X7F7g2jW` | 5.000 | `2SchdeAaMz6ENtrGSUy53dCT6RnmYWR5V1EaM5NGRLLem85dz4anmwsSC3sWLkfHRTJxpmoz3AxcAnrU2xem9omt` |
| 21/07/2024 08:27:31 | `GFpqfjEQFhXRbWEJCwUqKuNjSNTCgqAsANMbVyTGmi1p` | `HkFSNPjNFUVtdykP8kSyWCKhocY85k1S4MyjXHNqesvv` | 6.500 | `38k1RSPdjmDa5NtTPhycgoBZrwMGyhdqTTqt5ASuijaKs6EmP8yTS9uAX8yHGohwyVbipGA16soFL78d9vAH4Fax` |
| 21/07/2024 08:28:20 | `GFpqfjEQFhXRbWEJCwUqKuNjSNTCgqAsANMbVyTGmi1p` | `2mW45kXp4Wd4xRkF2mmh5rKdzjnjbJR2o53skWcxGa2d` | 6.000 | `sybo7NWx8CnNFZUBMHVF55dM1xCkReCKcqCstgjpaxxVRLW5CiR9EgFsxf65fdeJbKTwXUQE6b3oDbi25apxyGX` |
| 21/07/2024 08:30:38 | `GFpqfjEQFhXRbWEJCwUqKuNjSNTCgqAsANMbVyTGmi1p` | `4upmFYy6SpmCwdSRfG9akN2gRRn3DksLpDyN5YAmohbx` | 6.000 | `5VLZXvLgbZhFq9utwU3ew3HoWnoNj8sS27P5KHyRxBB4EfiGdjXuNadxpUt1Z1AYn3XfGF4FPw3WoamfX6eTehaZ` |
| 21/07/2024 08:32:13 | `GFpqfjEQFhXRbWEJCwUqKuNjSNTCgqAsANMbVyTGmi1p` | `EZXUvi4X5k3Aj99rGzNQoBtAzFqzYUjGhHNu8A1Ty8s4` | 5.200 | `5LT1iXn8RFaf8yCfGFxHNebbXmedJ2zVQ5nx5RxYAA2MBkqLRci9gxqqfVLxtdt8pwVZMfCW6aJGMTxpBF4wJm7P` |
| 21/07/2024 08:33:36 | `NxtXcmEW3gQvrCdBEm5GYT3zaqMre3QiPUhnwViNsD7` | `GFpqfjEQFhXRbWEJCwUqKuNjSNTCgqAsANMbVyTGmi1p` | 1.000 | `2epM63ZTNSNSmXDo87Xn7qrJKkRXLD1znE9awNj2u2QZkdS4VNNeAsBnkaBfJ1UK6YLh8UT9gQiStAHrZ6RcYa1R` |
| 21/07/2024 11:10:25 | `AtZjv3DuV9cLn3Jxm72TMSdTN4aM6CrBaGyxUC4c2wDk` | `Akp46DicpTMb9aDtZozTViYydsYH5NhcZACWokpzLaNB` | 6.000 | `3hksjHdcYBFMVG7FEhHL7t5Y6UHnV1d22RsrXECePeoCmpHbiXtH8TCLVEUo5uniJ7Tv87yCkXziEwgZ7tNMrsre` |
| 21/07/2024 14:22:00 | `FjuV7mJUyjMbDg41RybRRrTJu8UTPK6suURavt6ZRBkV` | `C73Yv9iHmTaf8SU2XFnGLt7QXUDqbeWNtUYza9WJhkae` | 6.500 | `27eg3oXLNmEsXVHiGGKX2iEgkrnAHNdLjmUHL8iKGcKjYx6SuSQ79b4tod2fghPjcwHWwqaFv91uUoRaNeQej9yu` |
| 21/07/2024 14:23:52 | `HkrGvxapoqp6625TKs8v8tEyu6eDwuPxmPinRaGH6i4a` | `C73Yv9iHmTaf8SU2XFnGLt7QXUDqbeWNtUYza9WJhkae` | 5.500 | `3Bo2GkFUGiaFY1tD1gN8Wg6mYLVN6zTcj1WkxSJ9KpHVPBf7F16UXUJe7onS6owxNWaErmeJVWwHCWPBeYr6XTBu` |
| 21/07/2024 14:24:21 | `HKXb8LfyzxYUgL1hhP8gtnXMCPnbJm6vNWMbVsmvy6WV` | `BuBXTWECG8Xk6wMgyvrK6LQdJBk1exhDaSqNa9nFnjx3` | 6.000 | `4jCSn4tyzEJsdKru3FNnkBGY9F78r5NrUaQMe88n4KZ1UuKUrjuf1W3xqkQbWJmwZDMkXF16cSq5g8Zz2cGVv45K` |
| 21/07/2024 14:24:45 | `8xjM4fGgPCqY4okN8Dsj4FXSPDp19d3sJYuTVGs2jkUv` | `BuBXTWECG8Xk6wMgyvrK6LQdJBk1exhDaSqNa9nFnjx3` | 6.500 | `2Suy76fcGaPbEyUg257C1RgWHCFBiGLbWFDZ81JMajd2yjpFVa62cN78qp1kG9v7urRB6Jh228on1GJmdw3AHfXN` |
| 21/07/2024 14:25:44 | `2BLSXbea4abffYCbs6pkCvPDChe9D4VNsfxJTAauQZPT` | `BuBXTWECG8Xk6wMgyvrK6LQdJBk1exhDaSqNa9nFnjx3` | 1.500 | `5fCYXrqB3SowvK43ZrJNn8bmg9EzqvrJ69V3xiTxAHMNc9Rw47aXMs262SDna9xaCZJda5NFUQRUSSApr4WnzGDN` |

### Membres
| Wallet | Acheté SOL | Acheté M | Réalisé SOL | Reçu par transfert M | Sorti par transfert M | 1er achat |
|---|---|---|---|---|---|---|
| `6t2dz4jm3S8vJZCkWPhBxHStxFTC8wNV9QttTzfQrG7M` | 2.05 | 26.65 | 0.0 | 0.0 | 26.7 | 14/07/2024 02:06:07 |
| `8YrEVPQqhs1zNsGUS5inFFqy5ziHaWdnVZXqysLThAh` | 1.00 | 23.41 | 0.0 | 0.0 | 23.4 | 14/07/2024 02:06:26 |
| `GFpqfjEQFhXRbWEJCwUqKuNjSNTCgqAsANMbVyTGmi1p` | 19.80 | 132.64 | 148.5 | 6.7 | 63.2 | 14/07/2024 02:07:26 |
| `99Xrt5uuu2FdsgGzKo3wvs28Bw2KuUgxaeV5rTQZLkb` | 2.50 | 19.03 | 0.0 | 0.0 | 19.0 | 14/07/2024 02:07:39 |
| `5QhJJcFZu2ashyKyWSTGHcsyo6ZBCbpVuJqeutvQHScd` | 53.36 | 40.27 | 74.2 | 37.8 | 76.3 | 14/07/2024 02:10:11 |
| `AW63YBXXsGcLPpsDTSrpBMdQ9QXtxTiHsTbcVkY6UFv5` | 5.74 | 15.44 | 0.0 | 0.0 | 15.4 | 14/07/2024 02:11:56 |
| `EZXUvi4X5k3Aj99rGzNQoBtAzFqzYUjGhHNu8A1Ty8s4` | 0.38 | 1.23 | 92.6 | 11.0 | 0.8 | 14/07/2024 02:12:27 |
| `7FGoCB63x3FAJNF25MMZG8pheR4rRtJbApQuynJRxLdE` | 1.00 | 1.41 | 35.3 | 19.5 | 19.7 | 14/07/2024 02:17:56 |
| `Ei5yGz8dPndr1aCeHZsfqJBcS3VBbz75VHEhxxJKLy3V` | 132.23 | 78.91 | 405.4 | 3.0 | 62.9 | 14/07/2024 02:18:03 |
| `4upmFYy6SpmCwdSRfG9akN2gRRn3DksLpDyN5YAmohbx` | 0.49 | 0.71 | 0.0 | 6.0 | 6.7 | 14/07/2024 02:20:36 |
| `2mW45kXp4Wd4xRkF2mmh5rKdzjnjbJR2o53skWcxGa2d` | 0.49 | 0.72 | 21.4 | 6.0 | 0.0 | 14/07/2024 02:21:01 |
| `HkFSNPjNFUVtdykP8kSyWCKhocY85k1S4MyjXHNqesvv` | 0.49 | 0.69 | 0.0 | 6.5 | 1.0 | 14/07/2024 02:21:49 |
| `CZsBW8yCGAiWwQ16VAokXE7h7qYL8spMA582X7F7g2jW` | 0.49 | 0.60 | 23.9 | 5.0 | 0.0 | 14/07/2024 02:22:41 |
| `AtZjv3DuV9cLn3Jxm72TMSdTN4aM6CrBaGyxUC4c2wDk` | 0.14 | 0.16 | 327.3 | 95.5 | 92.7 | 14/07/2024 02:25:33 |
| `C73Yv9iHmTaf8SU2XFnGLt7QXUDqbeWNtUYza9WJhkae` | 5.50 | 6.86 | 1,686.1 | 23.6 | 2.3 | 14/07/2024 02:43:33 |
| `74qFhHypY1zi8oS2KahqmwLfV8zMVbBiJ8uDdki8xPEb` | 3.50 | 11.49 | 4.8 | 37.5 | 26.5 | 14/07/2024 11:21:48 |
| `35nAuv6jGTVMnr7qdiRAV5PbZ3QgTJcLzBFzxGFm6Xw8` | 2.00 | 0.67 | 358.1 | 22.0 | 0.7 | 16/07/2024 02:12:04 |
| `7mdCAs8CWYJxkWz2gfj3sRhDBmUi6Q9qvRGuKiv2Bazu` | 338.03 | 62.04 | 44.8 | 18.1 | 1.1 | 23/07/2024 00:59:15 |
| `ADnZ9NdL9rHg7CL6CnAjEhPTuLsJnvLXrY9kbkhML5Ft` | 6.00 | 0.10 | 18.4 | 11.0 | 10.8 | 23/07/2024 15:20:24 |
| `HGBiExZRtD2TZdQLWHE9azkTSmE2z7ygKqZMtehJDKYU` | 248.00 | 3.02 | 681.8 | 20.1 | 13.1 | 27/07/2024 20:08:30 |
| `C7i9beNHXYonZYB5riXE6kaLpFWLj9BPzh2FSBoUUePK` | 8.74 | 0.19 | 404.5 | 5.2 | 0.0 | 05/10/2024 23:02:59 |
| `2BLSXbea4abffYCbs6pkCvPDChe9D4VNsfxJTAauQZPT` | 0.00 | 0.00 | 46.8 | 4.0 | 2.0 | n/d |
| `4wComYHQbydc9DZHsDu3t2MaTLNe7Y3ukdymrkqh9ftC` | 0.00 | 0.00 | 0.0 | 19.0 | 19.0 | n/d |
| `8xjM4fGgPCqY4okN8Dsj4FXSPDp19d3sJYuTVGs2jkUv` | 0.00 | 0.00 | 0.0 | 6.5 | 6.5 | n/d |
| `9u5JKgWdLzj4xUiA4sFnaaJeKAJF8zBXExatxeSZHMkP` | 0.00 | 0.00 | 0.0 | 2.5 | 0.0 | n/d |
| `Akp46DicpTMb9aDtZozTViYydsYH5NhcZACWokpzLaNB` | 0.00 | 0.00 | 364.5 | 8.0 | 0.3 | n/d |
| `BuBXTWECG8Xk6wMgyvrK6LQdJBk1exhDaSqNa9nFnjx3` | 0.00 | 0.00 | 31.4 | 14.2 | 14.0 | n/d |
| `FjuV7mJUyjMbDg41RybRRrTJu8UTPK6suURavt6ZRBkV` | 0.00 | 0.00 | 0.0 | 6.5 | 6.5 | n/d |
| `GPMYCuusSYfgdXXYHLyCBhBdhP9fJeXrSGUou6XAxHgm` | 0.00 | 0.00 | 434.9 | 3.9 | 0.0 | n/d |
| `Gcyg2jeLfSY9gxxHf5za5QU74ijtxBb1dB2mdGSPZH3m` | 0.00 | 0.00 | 339.1 | 20.0 | 17.1 | n/d |
| `HKXb8LfyzxYUgL1hhP8gtnXMCPnbJm6vNWMbVsmvy6WV` | 0.00 | 0.00 | 0.0 | 6.0 | 6.0 | n/d |
| `HkrGvxapoqp6625TKs8v8tEyu6eDwuPxmPinRaGH6i4a` | 0.00 | 0.00 | 0.0 | 5.5 | 5.5 | n/d |
| `NxtXcmEW3gQvrCdBEm5GYT3zaqMre3QiPUhnwViNsD7` | 0.00 | 0.00 | 50.3 | 41.2 | 19.0 | n/d |

## 4. Faux liens écartés
| Lien apparent | Pourquoi il est écarté |
|---|---|
| Le créateur et `9PrmF8…` ont le même premier financeur `GJRs4FwHtemZ5ZE9x3FNvJ8TMwitKTh21yxdRPqn7npE` | Coinbase 3 selon Dune Spellbook. Rupture de traçabilité, pas un lien |
| `H3QsBr…` et `9PrmF8…` envoient des jetons à `9UsmwVmbV4VwEwv5q5iZh4y3THh6dn2cqjFpEUrGRzZJ` | Réserve d'un pool Raydium CLMM : ce sont des ventes |
| `3LoAYHuS…`, `HFqp6ErW…`, `GP8StUXN…`, `3CgvbiM3…`, `7iWnBRRh…` sont reliés à `5QhJJc…`, `9PrmF8…` et `H3QsBr…` | Comptes publiés par Jupiter (`jup-ag/docs`, DefiLlama), archivés dans `evidence/labels/`. Ce sont des jambes de routage |
| `Habp5bncMSsBC3vkChyebepym5dcTNRYeg2LVG464E96` envoie du SOL à presque tous | Poussière de 0,0000001 SOL. Reste son arête de 8 M de DMAGA avec `5QhJJc…` |
| `5QhJJc…` et le créateur envoient des jetons vers `JD25qVdtd65FoiXNmR89JjmoJdYk9sjYQeSTZAALFiMy` | Exécutant de Jupiter DCA : signataire, programme `DCA265Vj`, `InitiateFlashFill`. Ce sont deux ordres DCA, pas un destinataire commun |
| Le « créateur » DAS `TSLvdd1pWpHVjahSpsvCXUbgwsL3JAcvokwaKt1eokM` commun avec Kekius | Autorité de mint de Pump.fun, présente sur tous ses tokens |
