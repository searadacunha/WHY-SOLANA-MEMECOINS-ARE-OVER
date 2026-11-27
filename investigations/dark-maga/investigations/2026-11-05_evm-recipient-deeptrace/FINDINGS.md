# Destinataires EVM des sorties Dark MAGA : constats (05/11/2026)

Jeton `7D7BRcBYepfi77vxySapmeqRNN1wsBBxnFPJGbH5pump`. Personne n'est accusé et aucune identité civile n'est présumée. Les noms ENS et les tags cités sont ceux que renvoient les sources publiques : ils ne désignent personne.

Niveaux : **VERIFIED** (relu sur la chaîne, script et hash fournis) ; **SUPPORTED** (plusieurs signaux indépendants concordent) ; **EXPLORATORY** (un seul signal, ou un signal faible) ; **UNRESOLVED** ; **REFUTED**.
On distingue toujours *même destination* ≠ *même opérateur* ≠ *même bénéficiaire effectif*.

Adresses : b947 = `0xb947bf7f409e998b28f8e218802fc9575c3c8c57`, b298 = `0xb29826d809aa04d2ead6f2310d8965a45b87fa67`, relais = `0x4978cd7e5a3565cafcc88a105940b0ea01adc04d`, `Ei5yGz8d` = `Ei5yGz8dPndr1aCeHZsfqJBcS3VBbz75VHEhxxJKLy3V`. Toutes les heures sont en UTC.
Autocontrôle hors ligne : `scripts/s99_selfcheck.py` (37 assertions, réseau coupé, sur 11 reçus figés dans `evidence/selfcheck_cache/`) ; `scripts/s98_verify_refs.py` relit sur la chaîne les 50 références Ethereum et les 9 signatures Solana citées ici (`evidence/s98_refs_check.csv`, 0 échec) rejoue chaque constat marqué « [sc] ».

---

## 1. Les 120 957,888072 USDC du 26/07/2024 : origine retrouvée. VERIFIED [sc]

Chaîne complète : **Solana → maker `GZXKYzwZPgWH8TwyY9f8dkCQ9EKK6nrPZADGcEwfAg7Y` → ordre DLN `0xc65ba1fa1b9d14301b5b0acaf159a5fd955a18899e4256a7604fd0af1f27a225` → taker `0x555ce236c0220695b68341bc48c68d52210cc35b` → b947**.

| Étape | Preuve |
|---|---|
| Création de l'ordre sur Solana, 2024-07-26 05:55:10 | sig `2SesFSiWhezf6a2RVvkRLua5obwjtBet5yaVFHooxnxubLsras6FKN4dkgHjVrSJrHa3Rwnc45uRnf7AiWRmiB8c`, signataire et payeur `GZXKYzwZ…`, programme `src5qyZHqTqecJV4aY6Cb6zDZLMDzrDKKezs22MPHr4`, −121 061,638928 USDC |
| Ordre (journal `FulfilledOrder` décodé sur Ethereum) | giveChainId 7565164 (Solana), giveToken USDC `EPjFWdd5…`, giveAmount 121 013,214273, makerOrderNonce 1721973287043, receiverDst = orderAuthorityDst = b947 |
| Exécution sur Ethereum, 2024-07-26 05:56:11, bloc 20388771 | tx `0x47e8da75f698f8c40419230c2274136c57666b92a91bef55c481e63a91758e14`, envoyée par `0x555ce236…` à DlnDestination `0xe7351fd770a37282b91d153ee690b63579d6dd7f`, 120 957,888072 USDC vers b947 |

- Décodeur maison sans dépendance (`scripts/dln.py`). Il lit les deux versions de `FulfilledOrder` : la v1 (`0xd281ee92`) et la v2 de 2026 (`0xc164aca3`), qui ajoute un mot avant `sender` (§10). **Contrôle positif :** l'ordre test connu de `Gcyg2jeL` (tx `0xdb07ade91b6ed02470a9283a346f7062ba45dbb65ea5030763dd1150b78d8b3d`) redonne bien maker `Gcyg2jeLfSY9gxxHf5za5QU74ijtxBb1dB2mdGSPZH3m` et 9,992001 USDC.
- `GZXKYzwZ` était déjà dans le corpus (`audits/2026-11-03/work_G/flow_boundaries.csv`, branche `audit-2026-11-03`, « wallet non suivi, aucun historique lu »). Son ordre deBridge ne l'était pas : il n'appartient à aucun des 76 ordres de `investigations/2026-11-05_debridge_winners/evidence/i14_orders.csv`.

## 2. `GZXKYzwZ` : wallet de vente jetable d'`Ei5yGz8d`, alimenté par neuf wallets en 100 secondes. VERIFIED (transactions) ; SUPPORTED (contrôle commun) [sc]

Relu sur Solana : 25 signatures, y compris celles des comptes de jetons (`evidence/s20_gzx_ledger.csv`).

**Création par `Ei5yGz8d`, le 22/07/2024 :**
- 17:26:27 : 3 000 000 DMAGA (sig `3hmS8e42ykBA1HRyxziaPZvkGnnMr8DFfCjec4MZwkhxUaNy8G9oURVHJ3HhAszN4Hyk5radGL1n7Ayph9PL9Ci2`) ;
- 17:26:45 : 0,5 SOL, son premier SOL (sig `3XdbSViYcY13x12DMFgWfCD6rc3PP4RYMwCoJ1GPpJtnYycqp253q115Pi6A1uUjqbjQLvf8AzJE4wzF2b58voL3`).

**Consolidation du 26/07/2024, de 05:40:37 à 05:42:17 :** un envoi toutes les 11 à 15 s, 29 295 679,868145 DMAGA au total. Signatures complètes dans `evidence/s20_gzx_ledger.csv`.

| Heure | Expéditeur | DMAGA | Statut |
|---|---|---|---|
| 05:40:37 | `EMucoi7yMoSdqLzUmUHwMtgLXVwXsfFkXHrkr7khFWrV` | 3 000 000 | parking, hors corpus |
| 05:40:52 | `38p6SEUodxnF7DQLSucpBGw8bT4tuBeBpYo7wdQRe8uB` | 3 000 000 | parking, hors corpus |
| 05:41:03 | `8ScA8t7QVamYihprGV63UQdAtjHhFpijdKYE8txXkVGD` | 4 000 000 | parking, hors corpus |
| 05:41:15 | `EMYihQ4kPn4W23J23fo1Rr4HZ9NNK8GcsdSce1rwAy1E` | 3 000 000 | parking, hors corpus |
| 05:41:27 | `5nxBz7Y9svhrXEyy8WNXGXZH3pMNhtCWXY2C1bBKzHxT` | 4 000 000 | parking, hors corpus |
| 05:41:38 | `4wComYHQbydc9DZHsDu3t2MaTLNe7Y3ukdymrkqh9ftC` | 4 000 000 | groupe des 33, sous-ensemble 1 |
| 05:41:53 | `Gcyg2jeLfSY9gxxHf5za5QU74ijtxBb1dB2mdGSPZH3m` | 2 400 000 | groupe des 33, sous-ensemble 1 |
| 05:42:04 | `HGBiExZRtD2TZdQLWHE9azkTSmE2z7ygKqZMtehJDKYU` | 3 050 000 | groupe des 33, sous-ensemble 1 |
| 05:42:17 | `Ei5yGz8d…` | 2 845 679,868145 | groupe des 33, sous-ensemble 1 |

**Vente et pont, le même matin :**
- 05:48:58 : vente de 29 095 679,868145 DMAGA contre 676,588596569 SOL (sig `5XQUEVdeEB9yrsUiU2g1kQx5Py8FqkVAgMbh3oXocpPQuoUoCc5nQu3hw1j5G1oz3WhaZHi6ag8cU6Czyq28FXGg`) ;
- 05:52:48 : swap de 687,405720630 SOL contre 121 068,641666 USDC (sig `3kHGkmsrrry7uyeGttFWPvneuGBWx1RYuHyEPmhwoa7WJmsRzzWH2c6KXUqGFhYBe2Uvu4GVsyK3BgzPn4eBW1sk`) ;
- 05:54:20 : **1 SOL de gaz venu d'`Ei5yGz8d`** (sig `31EdvCebjkPPtUCFbUbmnxBH1cWG1T8tV9CEiaBBkME2GDjkJC86Yy18PMTsjmwXUPQrTDQqSTTviKokRuFvQDHB`), 50 s avant l'ordre ;
- 05:55:10 : ordre deBridge vers b947.

**Restes rendus à `Ei5yGz8d` :** 3 000 000 DMAGA le 26/07 à 21:37:16 (sig `4E7My5f6LQDMHsqKTJ4ZABdv9PLPjxbxkdRBGZpP3UF6hJjwEBa1XXqxC2rUTHsL2u51kH54sCoLho77zKgS84ew`), puis 0,987450757 SOL le 28/09/2024 (sig `3SQcWCpxDnEu7QqrVcMuUhPXRvKPATfWtZrB92Ffxzo5smAc8sRnSWF7xVGKGKSNVENnQj96aYCWikE4pk2xLiTN`).

**Les cinq wallets de parking (`evidence/s21_*_ledger.csv`), tous créés le 22/07/2024 entre 17:17:17 et 17:25:22 :**

| Wallet | DMAGA reçu de | Gaz d'`Ei5yGz8d` | Retour du SOL à `Ei5yGz8d`, 29/07/2024 |
|---|---|---|---|
| `EMYihQ4k` | `Ei5yGz8d` (3 M) | 2 SOL, 24 s après | 21:06:23 |
| `5nxBz7Y9` | `HGBiExZR` (4 M) | 2 SOL, 24 s après | 21:06:09 |
| `8ScA8t7Q` | `Gcyg2jeL` (4 M) | 3 SOL, 33 s après | 21:06:35 |
| `38p6SEUo` | `HGBiExZR` (3 M) | 1 SOL, 22 s après | 21:06:48 |
| `EMucoi7y` | `Gcyg2jeL` (3 M) | 1 SOL, 17 s après | 21:06:58 |

- Chaque wallet de parking renvoie exactement son SOL moins les frais (par exemple 2,999987999 sur 3).
- **Nouveau :** `Ei5yGz8d` paie le gaz de wallets que `HGBiExZR` et `Gcyg2jeL` remplissent de DMAGA, 17 à 33 s après eux. C'est un lien opérationnel entre les trois, indépendant des transferts directs qui définissent le groupe des 33.
- Les dépôts de 1 000 lamports de `7wwNYSDQ…`, `He75wc4o…` et `9kDgyDEY…` (avec co-signataire `EdQNGBdJ…Ly3V`, sosie d'`Ei5yGz8d`) sont de l'empoisonnement d'adresse. Écartés.

## 3. b947 n'a jamais eu d'autonomie : relais de b298 depuis 2022. VERIFIED (faits) ; SUPPORTED (même opérateur) [sc]

Historique complet : `b947_full_history.csv` (78 lignes, 17 marquées empoisonnement). Relation : `b298_b947_relationship.csv`. Mesures : `evidence/s40_metrics.json`.

**a. Gaz.** b947 a reçu 0,037989 ETH en tout, **100 % de b298**, en 5 apports. Quatre apports sur cinq précèdent de 72 à 291 s une tx de b947 :

| Apport de b298 | ETH | Tx | Délai avant la tx suivante de b947 |
|---|---|---|---|
| 2022-09-11 18:50:18 | 0,002086 | `0xc7bd63d35a1bdf09bfe5ccb1ad859184a4903117813760a388334003957fad89` | 291 s |
| 2023-01-21 16:48:59 | 0,015066 | `0x97b2d2789a3f99592eb257e696f0f9adb36daeb2a64476447a63bc11a1b20a53` | 21 j |
| 2023-02-12 18:11:59 | 0,005190 | `0x0cb4cec60064b2b3b9ccf5586b658925491a99a21b240f258cf55dcfbff45abe` | 96 s |
| 2023-02-14 01:10:23 | 0,006660 | `0x51f636c057dc0c36e47814d4c15f87b34eca28634049ae60d3200287a1a334e2` | 72 s |
| 2024-10-01 15:44:11 | 0,008989 | `0x29caf14eebaa8f2d48c298786f829c398df238584318006059f99ff21e5c446d` | 120 s |

b947 a aussi rendu de l'ETH à b298 deux fois : `0x5f71dbe266a66528cb95184a568ef250e32fb8103aa5a235e5342f133a0b42b8` (2023-02-11) et `0x5a5fd279c08f734c0e689bc3e4f51a4a0a78508d7f46bdb980acd326ab3ae5d5` (2023-02-12).

**b. Février 2023 : cinq séances où b947 renvoie au micro-USDC près ce qu'il vient de recevoir.** Chaque séance part d'un solde nul. b947 reçoit en quelques minutes des retraits du hot wallet KuCoin 9 (`0xf16e9b0d03470827a95cdfd0cb8a8a3b46969b91`), du hot wallet MEXC 1 (`0x75e89d5979e4f6fba9f97c104c2f0afb3f1dcb88`) et un apport de b298. Il dépose ensuite la somme exacte sur `0x100a38ed14c25a5f456557e9e08298bbb14d4b98`, adresse de dépôt Stake.com inférée (§5).

| Sortie de b947 | Montant = somme exacte des entrées | Tx |
|---|---|---|
| 2023-02-11 22:38:47 | 52 024,577982 = 14 859,604656 + 11 174,51118 + **16 848,165698 (b298)** + 9 142,296448 | `0x7fac1dda0209e50fe372e56799356624b2d6495fc6418470a6c371482ec67ec5` |
| 2023-02-12 18:13:35 | 51 807,826429 | `0x7d2f8c246c6601ad1e4b1ccaf04e41e964d108a381b997f005abe3e6974240c5` |
| 2023-02-13 00:12:11 | 51 816,577897 | `0x6de41fa73a0b01443da16230682dd6cf6f132b557d8676d8764daac69d0f8fca` |
| 2023-02-13 21:17:35 | 99 562,11602 | `0x8f1f04421bdfe9ea3ce98de319d3818a160edb08fca0163dbcc8ba78c0f82c5e` |
| 2023-02-14 01:11:35 | 49 649,473128 = 13 762,845071 (KuCoin) + **35 886,628057 (b298, 01:09:59)**, gaz de b298 à 01:10:23 | `0x94be66a28a794006c99f69aba1f4c482859c9e5161187d9927ecbbce641a17ad` |

Les retraits de KuCoin et de MEXC vers b947, l'appoint et le gaz venus de b298, puis le dépôt de la somme exacte tombent dans les mêmes minutes. C'est compatible avec un seul opérateur qui pilote les comptes d'exchange et b298 ; ce n'en est pas la preuve.

**c. Juillet-octobre 2024 : l'USDC de b947 gardé 71 jours, puis vidé en entier vers b298.** b947 n'a jamais détenu de DMAGA : il reçoit de l'USDC.
- b947 reçoit 263 320,105094 USDC le 22/07 (4 ordres, 263 573,151396 USDC donnés côté Solana, frais compris), 50 003,330779 de b298 le 25/07 (tx `0xac4a12bd7eac6283bec6af0f43b3191c2964ee7c0f77dcefd8c29238566e1211`) et 120 957,888072 le 26/07 (§1). Soit 434 281,323945 USDC.
  - Seuls les 384 277,993166 USDC des cinq exécutions deBridge viennent de makers DMAGA (§1, §2, `evidence/s40_metrics.json`). Les 50 003,33 USDC de b298 n'en viennent pas.
  - Le 01/10 à 15:47:23, entre deux envois, b947 reçoit aussi 10 USDC réels d'un sosie. Il envoie donc 434 291,323945 USDC.
- Ces 50 003,33 USDC suivent de 4 min un retrait de 49 999,0 USDC du hot wallet Coinbase 10 vers b298 (2024-07-25 08:18:11, tx `0x2b3c8d6b557e9a700b20163ea548852fee49746d01871467d059049b051dbd2c`).
- **Aucune sortie** dans les 5 min, 1 h, 24 h ou 7 j qui suivent chaque arrivée (`b947_post_dmaga_flows.csv`).
- Le 01/10/2024, de 15:46:11 à 15:49:59, b947 vide son solde, gaz de b298 reçu 2 min avant :

| Tx | Montant | Destination |
|---|---|---|
| `0x18f8ac3febdc7b19804357b1f3cabd975ee96bb3434968046f42bad286d8bae2` | 10 USDC (test) | relais |
| `0x9a146cd8a1bb33292b37b87f972d14659941da8a1b39b6e13a0eff98a02e3ce9` | 200 000 USDC | relais |
| `0x2f71766658c7f4f23d9181e3088545d9993db1172fd9d5b9eac4274f2b96100e` | 100 000 USDC | **b298** |
| `0xd6b003093ce96d36cf55b9d4a7de162e561fc4919782412914954c6c5985b0bd` | 134 281,323945 USDC | relais |

  Solde final : 0,012 USDC, de la poussière d'empoisonneur [sc].
- **Le relais `0x4978cd7e…` est un satellite de b298** [sc]. Son seul gaz : 0,02 ETH de b298 le 06/10/2024 à 19:14:47 (tx `0x633dd2953a05217ba93d555a9122cb3572732bc693c28f906738c799358cb9b8`). Toutes ses sorties d'USDC vont à b298 : 434 291,334945 USDC en 6 transferts, du 06/10 au 15/11/2024. Ce montant égale les 334 291,323945 de b947, plus un aller-retour de 100 000 avec b298 et 0,011 de poussière. Il lui renvoie aussi 434 278 769,57 FLOKI le 17/11/2024.
- Les adresses `0x4978…c04d` et `0xb298…fa67` qui « envoient » de faux USDC (`UЅDC`, `ꓴꓢꓓꓚ`) à partir du 01/10 sont des sosies d'empoisonnement. Écartées (`flags` = `unsigned_out`, `lookalike`, `fake_token`).

## 4. Aller-retour b298 ↔ `Ei5yGz8d` par deBridge, de juillet à novembre 2024. VERIFIED (transactions) ; SUPPORTED (même acteur économique) [sc]

65 ordres DLN décodés sur Ethereum pour b947, b298 et 86f9 (`evidence/dln_orders_evm.csv`).

| Sens | Ordres | Montant | Période |
|---|---|---|---|
| `Ei5yGz8d` → b298 | 8 vers Ethereum (exécutés au wei près), plus 7 vers Base (corpus i14) | 151 300,22 USDC sur Ethereum | 16/07 → 14/11/2024 |
| b298 → `Ei5yGz8d` | **22** | 299 800,36 USDC et 34,1399 ETH cédés ; 1 753,732 SOL et 48 960,807840 USDC reçus | 27/07 → 21/11/2024 |
| b298 → `E72DuqDL2fkCw2Q8tyW2zWXpkRgK1p6FBJys6h6wpgVG` | 1 | 2 638,78 USDC, 17,91 SOL reçus | **01/07/2024, 13 jours avant la création du mint** |
| b298 → `2aeEoq5n8Cip2raJsiWHBVKuoJL4rid7adepkVYnVzDm` | 1 | 0,2114 ETH, 2,791 SOL reçus | 24/11/2024 |

- **24 ordres sur 24 de b298 vers Solana retrouvés côté Solana**, au montant exact, par le programme DLN destination, 0 à 16 s après leur création (`evidence/s22_sol_fills_check.csv`). Exemple : 48 960,807840 USDC le 27/07/2024 sur le compte USDC `137jHLiwamDjA5Q3TKwS9LzgxCq8bs5JWfhSWcwL1pee` d'`Ei5yGz8d`, sig `2rpmCqZuDFp7a3sPXzuGbT69qA7tEJ5guo9FhxJfKapf8KWRsgwm6439TkKmKjuyn4fFN6NPdV8UoSxwBnmUwpMA`.
- Les deux autres receveurs sont liés à `Ei5yGz8d` sur Solana (corpus `audits/2026-11-03/work_G/g04_ledger.csv`, branche `audit-2026-11-03`) :
  - `E72DuqDL` a reçu 21,11 SOL d'`Ei5yGz8d` en 6 transferts, du 30/03 au 06/05/2024 ;
  - `2aeEoq5n` reçoit 0,0258 SOL d'`Ei5yGz8d` le 18/11/2024, puis lui renvoie 2,876 SOL du 21/11/2024 au 04/01/2025.
- **Ping-pong du 14/11/2024 :** b298 envoie 106 223,140420 USDC à `Ei5yGz8d` à 01:36:23 (tx `0x36ebd7c93cd5bea78b1d13919c83bf0643dc223aa7392ab2c9b351d520c9151e`, 494,13 SOL reçus). À 05:38:23, `Ei5yGz8d` renvoie 106 180,900856 USDC à b298 (fill `0x2caa1b5cbc13a6d9b88a8ebcc633536fa7fe8e599b536461f9fe5ce0334eaf3b`, 32,82 ETH reçus).
- Sur Solana, `Ei5yGz8d` est le centre du sous-ensemble 1 du groupe des 33 : il envoie 20,1 M DMAGA à `HGBiExZR`, 20 M à `Gcyg2jeL` et 14 M à `4wComYHQ` entre le 15 et le 22/07/2024 (corpus `link_edges.parquet`, données lourdes hors dépôt).

## 5. Quatre adresses de dépôt d'exchange inférées, dont trois servent à la fois à b947 et à b298. SUPPORTED (nature des adresses) ; signal de contrôle commun, jamais utilisé seul

Inférence : gaz venu d'un hot wallet étiqueté de l'exchange, puis vidage vers un hot wallet étiqueté du même exchange. Aucune étiquette publique sur ces adresses (`UNRESOLVED.md` §2).

| Adresse | Exchange inféré | Preuve de la nature | Utilisée par |
|---|---|---|---|
| `0x311ef6b5953ae605dbe469e6566280f0514d3d2e` | MEXC | 2022-01-02 : 9 965 USDT reçus de KuCoin 11 à 05:06:34 ; 0,0152 ETH du hot wallet MEXC 1 à 05:12:51 (`0x89c1cc279e42cf26060774c050abac875a196b46e86c68bb1cc33f5e89d3bd3b`) ; vidage vers MEXC 2 à 05:15:45 (`0xd738822b0b93a620eda8d78b84833296d36765a734c98c8a22e2f1471c5dbdd9`) | **b947** (WOO et HOT, 11/09/2022 ; 30 000 USDC le 28/05/2023, `0x30b66b5577e89f901045b22aedb5ba0183ecb2dc7009926f4dfee661317bcd8b`) ; **b298** (0,13 ETH en 2022 ; 14 908,62 USDC le 17/10/2023 ; 176 404,6161 USDT le 27/11/2024, `0x827ac5d2fccef6c628aecc0cf89df9dbf9ab480ed05b7a3ed1fcbbd4d91d95d9` ; 6 ordres deBridge de b298 depuis Base, 35 781,16 USDT livrés) [sc] |
| `0x100a38ed14c25a5f456557e9e08298bbb14d4b98` | Stake.com | gaz du hot wallet Stake.com 2 (`0x974caa59e49682cda0ad2bbe82983419a2ecc400`, ex. `0xe3d19c06a622ccf84d8db0e4de4c5012bb971e226e70f6fb08359b310eb59744`) ; vidages vers ce hot wallet (ex. `0x801c1feb1497b8182caa9466da839add1cfb594d90d125e6d9f95e48af6cb9c1`) | **b947** (304 860,57 USDC du 11 au 14/02/2023 ; 50 000 le 28/04/2023 ; 354 860,57 au total) ; **b298** (5 dépôts, 51 006,81 USDC, et 27,72 ETH) |
| `0xe1daccdc81b6f18e18b6704e9214b6e03a0fef1c` | KuCoin (confiance plus faible) | vidages vers KuCoin 3 (`0xa1d8d972…`), puis hot wallet KuCoin 9 (`0xa27eb3305e043631183a74ff911adcfa263ceed643e82318a21ce9fef66b194d`) | **b947** (20 000 USDC le 28/05/2023, `0xb0ed7c91096d768a277e1511fed609f76e42fdfd7e2170339c6222a78fbf586c`) ; **b298** (15 000 USDC le 14/10/2021, `0x9a5e5307973d244cb8a529f567fc300ab6b666a6201cd71586ca506db1938c32`) ; `0x5388dbdee4e9644c823f93db0b8ff4a29b216930` |
| `0x0ff70a96ee2c4468cc5a0b2e2f5aa9f8ae88fc93` | Coinbase | gaz du hot wallet Coinbase 6 (`0x614b9b57d39fad5c31c7bc564a77c7606c032e388e73ef8ba317efaf898c8b65`) ; vidage vers Coinbase 10 2 min après (`0x7c7654a7617b4e957ad08ef19c7e89decc39f5e562cc59d247e55fb7b7cc95af`) | **b298** seul (dont 50 045,505423 et 25 000 USDC le 04/10/2024, `0x62526b8d786d8eb7f1993a8e98d7dfd24332b49cbe2a4c010a9840c4691fbd30` et `0x238a1e09b31f733ba64f98ae08f01c9ca14885e133a527bf8e3ce94940283ad9`) |

**Infrastructure antérieure à DMAGA.**
- `0x5388dbde…` (actif depuis novembre 2020, gaz initial depuis Binance 4) envoie à b298 0,5 ETH et 35 039,85 TRAC le 04/02/2021, puis de l'ETH en mai et octobre 2021.
- Le même wallet envoie à b947 69 539,61 WOO et 861 359,84 HOT le 02/05/2022 : c'est la toute première activité de b947. b947 les dépose le 11/09/2022 sur le dépôt MEXC inféré, avec un gaz de b298 reçu 5 min avant.
- Les trois wallets alimentent le même dépôt KuCoin inféré.

Contreparties non-service partagées : `evm_shared_counterparties.csv` (hubs de service retirés : CEX, routeurs, ponts, contrats de jetons, distributeurs d'airdrops).

## 6. Après les 263 573 USDC : où va l'argent. VERIFIED (trajet) ; bornes sans FIFO, relais tracé

**Rectification du 06/11/2026 :** la version fusionnée le 06/11 à 07:43 UTC présentait ce tableau sous l'hypothèse H (le relais `0x4978cd7e…` ne transporte que de l'USDC de b947), non démontrée : le relais avait aussi reçu 100 000 USDC de b298 le 06/10/2024. Le relais est maintenant tracé avec la même règle que b298, et les bornes ci-dessous valent sans cette hypothèse (§10). La provenance des fonds doit toujours être distinguée du simple montant transféré.

1. **b947** garde son USDC 71 jours, puis le vide vers b298, directement (100 000) ou par le relais (334 291,32). Comptabilité de stock : le solde tombe à 0,012, et tout ce que b947 envoie aboutit chez b298, sans hypothèse FIFO.
2. **b298** mélange ces fonds avec d'autres. `evidence/s51_b298_usdc_bounds.csv` encadre chaque sortie USDC entre une borne basse et une borne haute.
   - Marqué : l'USDC que b947 envoie à partir du 01/10/2024, directement ou par le relais. Tout le reste est non marqué.
   - Borne basse : la sortie moins le maximum d'argent non marqué disponible.
   - Borne haute : le minimum entre la sortie et le maximum d'argent marqué disponible.
   - Calcul en entiers bruts, autocontrôle borne basse ≤ borne haute.
   - **Le relais n'est pas un conduit pur.** b298 lui renvoie 100 000 USDC le 06/10/2024 à 19:28:35 (`0x6407f6bccc370f06128fd95981f5c13475fc3be04922d6213d84d05c97944d8c`), 3 min après avoir reçu 100 088,75 USDC de Rizzolver. La borne basse de la part marquée de ce renvoi est 0. Le relais est donc tracé avec la même règle que b298.
   - Les 31 bornes basses et hautes sont égales à l'optimum d'un programme linéaire exact sur les deux réservoirs (`scripts/s52_lp_check.py`).
   - **Correction du 06/11/2026** : la première version comptait toute sortie du relais comme 100 % b947 (§10). Ses bornes basses, 472 143,22 USDC en tout, ne valaient que sous cette hypothèse, non démontrée. Elles tombent à 137 938,74 USDC.

| Destination de l'USDC venu de b947 (à partir du 01/10/2024) | Au moins | Au plus |
|---|---|---|
| deBridge → **b298 lui-même sur Base** (3 ordres : 06/11, 12/11, 15/11) | 46,81 | 124 261,38 |
| deBridge → **b298 lui-même sur BSC** (12/11, 157,37 BNB reçus) | 0 | 99 989,83 |
| Ventes USDC → ETH par UniswapX et solveurs (`0x43ee35d5542f5b826fa92832bd97caff153675a8`, `0xbcc66fc7402daa98f5764057f95ac66b9391cd6b`, Rizzolver `0x225a38bc71102999dd13478bfabd7c4d53f2dc17`) | 137 712,91 | 259 955,49 |
| Dépôt Coinbase inféré `0x0ff70a96` (04/10) | 0 | 74 820,98 |
| Ordres USDC directs vers `Ei5yGz8d` | 0 | 16 483,03 |

   **Les deux ordres du 12/11/2024, pris ensemble.** o1 (`0x4b7c7a2fcda576c58c961dee9d35840fba0151a9156cc0c48a0282c2fb024e16`) donne 100 048,914457 USDC vers Base, o2 (`0xca82377984453a77f40592a694c5ad4c8076acce66b64a25e7c43f119f3cf8a4`) 99 989,828367 USDC vers BSC.
   - Pris seuls, ils ont pour bornes basses 46,814553 et 0.
   - Ensemble, ils portent au moins **100 028,638296 USDC venus de b947**, quelle que soit l'allocation (`scripts/s51_bounds.py`, `joint_min`) :
     - après le 06/11/2024 08:31:47 et jusqu'à o2, l'USDC non marqué que les deux ordres peuvent emporter se limite au solde de b298 et à ses autres entrées non marquées, 10,093528 USDC en tout ;
     - s'y ajoute ce que le relais peut lui rendre de non marqué : au plus 100 000,011 USDC, le renvoi de b298 et 0,011 d'un sosie ;
     - 200 038,742824 − 10,093528 − 100 000,011 = 100 028,638296. Le programme linéaire trouve le même minimum.
   - **Part des seules ventes.** Sur les 434 291,32 USDC envoyés par b947, 384 277,99 viennent des cinq exécutions deBridge des makers DMAGA, 50 003,33 de b298 et 10 d'un sosie.
     - Si l'on ne marque que les premiers, b947 peut lui aussi transmettre jusqu'à 50 013,330779 USDC non marqués.
     - La borne commune tombe alors à **50 015,307517 USDC**, même démonstration, même minimum au programme linéaire.

3. **Montants quasi identiques dans les minutes qui suivent :**
   - arrivée de 100 000 du relais le 12/11 à 17:40:23 → ordre vers b298 sur BSC à 17:42:47 (99 989,83, 144 s) ;
   - 14 291,33 le 15/11 à 19:53:11 → ordre vers Base 348 s plus tard (14 289,02) ;
   - 10 000 le 06/11 à 08:17:11 → ordre vers Base 876 s plus tard (9 923,45).
4. De l'ETH repart ensuite vers `Ei5yGz8d` sur Solana :
   - 12/11 21:26:35 : 29,02 ETH passés par le forwarder deBridge, 94 624,840194 USDC cédés, 445,496 SOL reçus (`0x2fa91216ea9d4a935d757217e3845caaa93fa90933769161b3ba122a9f935f85`) ;
   - 14/11 01:36:23 : 33,52 ETH par le forwarder, 106 223,140420 USDC cédés, 494,131 SOL reçus (`0x36ebd7c93cd5bea78b1d13919c83bf0643dc223aa7392ab2c9b351d520c9151e`) ;
   - 17/11 01:48:59 : 33,996 ETH cédés, 482,635 SOL reçus (`0xdf0b6cf7dbf1f956b9fe2171acdd729ef41f4d1be1ce17e0cd6eb98b38126810`).
   La part de ces ordres qui vient de b947 n'est pas bornée (`UNRESOLVED.md` §8).
5. Ce qui part sur Base revient en partie sur Ethereum vers le dépôt MEXC inféré (6 ordres de b298 depuis Base, du 27/11 au 09/12/2024).

## 7. L'autre branche : `C73Yv9iH` → 2d86 (afk.eth) et 86f9

- **86f9** (`0x86f99097c563e84dd5190f3e85f6a2988f1c47a5`). VERIFIED.
  - Il ne vit que pour DMAGA : 0 ligne avant le 22/07/2024, 71 pendant la période, 1 après.
  - Il reçoit 8,955 ETH de `C73Yv9iHmTaf8SU2XFnGLt7QXUDqbeWNtUYza9WJhkae` (2 ordres, 22 et 23/07), achète et revend le mème $SWAG (`0x36c7188d…`, 3 040 détenteurs).
  - Il sort 8,0 ETH (26/07 02:43:35, `0x612ccb94f9bb4b45b64045a833febd91583c86437bd6731a6c993a8a0e2ccd5a`) et 8,15 ETH (10:28:59, `0xa81b446ca76f71ecd371928bd0df6cbecd6a831a8cf48b3d4579691538b93258`). Chaque montant passe par une adresse à usage unique, vidée 72 s plus tard vers « FixedFloat: Hot Wallet 2 » (`0x4e5b2e1dc63f6b91cb6cd759936495434c7e972f`). Ce sont des dépôts FixedFloat, frontière de la trace.
  - Aucune contrepartie non-service partagée avec b298 ou b947. Que b298 ait aussi acheté $SWAG la même semaine reste EXPLORATORY : c'est un mème courant.
- **2d86** (`0x2d86499a410a9ac2139833ba8d6942b8a8700a7b`, ENS public afk.eth ; noms de tag Blockscout p90.eth et l0l.eth) : voir §7 bis.

## 7 bis. 2d86 : trader de mèmes outillé par bot, avec son propre coffre. VERIFIED (profil) ; aucun lien avec la branche b298

Historique complet relu : 41 648 lignes, 20 384 tx signées, 15 425 transferts de jetons et 4 730 internes (`evidence/2d86_full_history.csv`, profil dans `evidence/s90_profiles.json`).
- **Profil :**
  - actif depuis le 25/08/2021, avec 0,315 WETH et 0,0888 ETH de `0x6df15e94b43c7cb2091a3cd4e804232cb21551d1`, aussitôt passés par le vieux pont Avalanche ;
  - 21 391 tx signées en 2023 et 14 515 en 2024 ;
  - 5 835 contreparties et 4 400 jetons distincts ;
  - 6 253 interactions avec le routeur du bot Maestro, 516 entrées depuis le hot wallet Rollbit ;
  - nonces 2 196 sur Base, 620 sur BSC, 366 sur Arbitrum.
  Ce n'est ni un service ni un coffre : c'est un trader de mèmes à très haute fréquence.
- **deBridge :** 170 entrées d'ETH venues de DlnDestination (587,14 ETH, du 11/12/2023 au 04/10/2026). 392 ordres décodés sur Ethereum, 186 reçus et 206 émis (`evidence/dln_orders_evm.csv`, partiel par construction, `UNRESOLVED.md` §6). Les 74 exécutions reçues entre le 01/03 et le 04/10/2026 utilisent la v2 de `FulfilledOrder` ; elles manquaient à la première version (§10) :
  - entrants : 31 de `C73Yv9iH` (517 982,86 USD ; les 27 du corpus et 4 absents du corpus), 16 de `26kExMGtjfxhfXVGg1FaTRDuFiLkd1BgKS3UkxwAcHqR`, 2 de `CMr4kjktCaVZRYSkV3dPRcpH7kZBp4Cf64fZs7kjhBiQ`, 1 de `0xbf987dce9000bd7752ad22fc752c3f0ac6e89f16`, et 136 de 2d86 lui-même (Base 56, Arbitrum 34, Avalanche 18, identifiant de chaîne 4663 13, BSC 8, HyperEVM 4, autres 3) ;
  - sortants : 27 vers `C73Yv9iH` et 20 vers `26kExMGt` sur Solana, et le reste vers 2d86 lui-même (Base 71, Arbitrum 32, BSC 24, HyperEVM 10, Avalanche 7…).
  - Aller-retour répété avec `C73Yv9iH` : même schéma que b298 ↔ `Ei5yGz8d`, mais sur l'autre branche.
- **Nouveau, son coffre `coin-etf.eth`** (`0xebc71f680a785314c413baaa9722a9f85bb3316e`, nom tagué par Blockscout, pas un contrat) :
  - 2d86 lui envoie 1 338,64 ETH en 425 tx et en reçoit 1 298,53 ETH en 287 tx, d'avril 2023 à novembre 2026 ;
  - dans 26 des 27 fenêtres d'une heure qui suivent une arrivée venue de `C73Yv9iH`, 2d86 lui envoie de l'ETH en montants ronds (2 à 10 ETH par envoi). On compte 48 envois par fenêtre, avec recouvrements quand deux arrivées sont proches. Le 22/07/2024, l'écart tombe souvent sous deux minutes :

    | Fill de `C73Yv9iH` vers 2d86 | Envoi de 2d86 vers `coin-etf.eth` |
    |---|---|
    | 00:39:35, 10,307 ETH (`0x918e6057259537876e62dd4c15cdaf5594bb404c1dfc01e6b2666448a60c4986`) | 00:40:23, 10 ETH, `0x9dd2f67e88e71ffc5aba78fa3accf4e23996130e1022681de0b6a44e8212b729` |
    | 01:01:47, 7,693 ETH | 01:03:35, 8 ETH, `0x81187224304b7baefe69f947eee643355c9f0ed8df762412bd9dd33126105514` |
    | 01:56:47, 9,188 ETH | 01:58:35, 9 ETH, `0x453beb9e8b21a943a17572d8fe16e6439a37e9b104b4fc5062325efeefb42e65` |
    | 02:42:11, 10,247 ETH | 02:43:23, 10 ETH, `0x48af5155c9bd1d26a143f12bc28e189eeea57ba2e7caf5a8d80c6cd05716dc57` |
    | 03:17:11, 7,672 ETH | 03:17:59, 8 ETH, `0xa18e59d70b9c9cf10b03734f1d4221deaadbbabbcb400e360e8b9dee08db8299` |

    L'ETH de DMAGA ne fait donc que traverser 2d86 : sa destination suivante est `coin-etf.eth`. Second correspondant Solana régulier : `26kExMGtjfxhfXVGg1FaTRDuFiLkd1BgKS3UkxwAcHqR` (20 ordres de 2d86 vers lui et 16 dans l'autre sens, décodés sur Ethereum ; un traçage indépendant par l'API deBridge en compte davantage toutes chaînes confondues, non recompté ici) ;
  - schéma d'aller-retour coffre ↔ wallet de trading, sur trois ans et demi.
- **Séparation des branches :** aucune contrepartie non-service commune entre {2d86, 86f9} et {b947, b298, relais}, une fois retirés OpenSea Fees 3 et le Spoke Pool Across (`evm_shared_counterparties.csv`). `coin-etf.eth` ne touche aucune de ces adresses ni aucun des quatre dépôts inférés. La branche `C73Yv9iH` (sous-ensemble 0 des 33) et la branche `Ei5yGz8d` (sous-ensemble 1) ne se rejoignent pas sur Ethereum dans ce qui a été lu.

## 8. Hypothèses sur b947 / b298

| Hypothèse | Statut | Pourquoi |
|---|---|---|
| H1 même opérateur | **SUPPORTED (fort)** | Cinq signaux indépendants : 100 % du gaz de b947 vient de b298, juste à temps ; ETH rendu à b298 ; vidage total de l'USDC de b947 vers b298, en direct et par un relais gazé par b298 seul ; séances de 2023 où l'appoint de b298 et les retraits CEX vers b947 tombent dans les mêmes minutes ; trois adresses de dépôt par utilisateur communes (MEXC, Stake, KuCoin). Pas VERIFIED : aucune preuve de clé commune. |
| H2 client / prestataire | EXPLORATORY (faible) | Un prestataire qui garde les fonds d'un client ne les rapatrie pas tous chez lui. b298 a un usage personnel : mèmes, création de jetons via 20lab, Stake.com, Coinbase. Un prestataire OTC servant `Ei5yGz8d` reste théoriquement possible, mais b298 n'a qu'un seul maker DLN tiers : `Ei5yGz8d`. |
| H3 wallet principal + secondaire | **SUPPORTED (fort)** | Forme précise de H1 : b298 est le principal (2 355 jours, 270 contreparties, 134 jetons, 5 chaînes). b947 n'a signé que 16 tx, toutes payées avec de l'ETH venu de b298 ; 10 contreparties en tout. |
| H4 simple contrepartie historique | **REFUTED** | Le gaz, les vidages totaux et les dépôts communs dépassent de loin une contrepartie. |
| H5 service partagé | **REFUTED** | Ni b298 ni b947 n'a le profil d'un service (pas de tag, pas de contrat ; 10 contreparties pour b947). Les services partagés (MEXC, KuCoin, Stake, takers deBridge) sont retirés des signaux. |

**Lien Solana ↔ EVM** : `Gcyg2jeL`, `HGBiExZR`, `Ei5yGz8d` et `GZXKYzwZ` envoient vers b947. b947 est un satellite de b298, qui renvoie vers `Ei5yGz8d`. Ces makers ont aussi des liens Solana directs et un gaz commun (§2). C'est la convergence forte décrite dans la consigne : relation Solana + destination EVM commune + redistribution vers une destination commune (b298). Détail : `solana_to_evm_clusters.csv`.

## 9. Corrections de travaux antérieurs

- `investigations/2026-11-05_debridge_winners/TABLE_NEW_LINKS.md` donnait « `0x50003330779...` » comme hash du transfert de 50 003,33 USDC du 25/07/2024 : ce sont les chiffres du montant, pas un hash. La PR #13 l'a remplacé par « Non imprimé » ; cette PR y inscrit les hashes réels, `0xac4a12bd7eac6283bec6af0f43b3191c2964ee7c0f77dcefd8c29238566e1211` (50 003,330779 USDC) et `0xc7bd63d35a1bdf09bfe5ccb1ad859184a4903117813760a388334003957fad89` (premier gaz de b947), et rattache les 120 957,888072 USDC à leur ordre (§1). `RAPPORT_RESULTATS_NOUVEAUX.md` est mis à jour sur ce dernier point.
- Même fichier : la « toute première transaction » de b947 n'est pas celle du 11/09/2022. Sa première activité est l'entrée de WOO et HOT venue de `0x5388dbde` le 02/05/2022. Le 11/09/2022 est son premier gaz.
- `REFUTATION.md` §4 : « 21 tx propres depuis le 11/09/2022 » compte les tx de premier niveau (21, dont 16 signées par b947). Le compteur Blockscout « transactions_count 0 » de `i20_evm.txt` est périmé.
- **Échec silencieux de source :** Routescan `tokentx` omet les transferts ERC-20 antérieurs à juillet 2023 (vérifié sur b947 : `0x7fac1dda…` existe en reçu RPC, absent de `tokentx`). Tout historique pris là doit être recoupé (Blockscout v2 ou reçus).
- Ma propre première version écartait comme empoisonnement 16 vraies ventes d'USDC/USDT de b298 exécutées par UniswapX et des solveurs (286 217,93), dont le gaz est payé par un tiers. Corrigé dans `scripts/s10_history.py`. Le solde USDC reconstitué de b298 retombe à 0 et concorde avec `balanceOf` (0).

## 10. Corrections du 06/11/2026, après l'audit du dossier `2026-11-06_debridge_base_bsc_solana`

- **Bornes du relais (`scripts/s51_bounds.py`).**
  - La première version comptait toute entrée venue du relais `0x4978cd7e` comme 100 % b947. Or b298 lui renvoie 100 000 USDC le 06/10/2024, et la même règle donne 0 à la part marquée de ce renvoi.
  - Le relais est maintenant tracé avec la même règle. o1 passe de 100 046,825553 à 46,814553 USDC, o2 de 99 981,823743 à 0. Les bornes basses sommées passent de 472 143,22 à 137 938,74 USDC.
  - La borne commune de o1 et o2 (§6) est nouvelle. Les bornes hautes ne changent pas.
  - Autocontrôle : `s99_selfcheck.py` (F8), recoupement exact : `s52_lp_check.py`.
- **Décodeur DLN (`scripts/dln.py`).**
  - La première version ne reconnaissait que la v1 de `FulfilledOrder`. La v2 (`0xc164aca3`, signature `FulfilledOrder(Order, bytes32, uint256, address, address)`) a une tête de cinq mots ; son `uint256` égale le `takeAmount` de l'ordre dans les 78 cas du cache.
  - 74 exécutions vers 2d86, du 01/03 au 04/10/2026, manquaient à `evidence/dln_orders_evm.csv`. Les 4 autres événements v2 du cache vont à des receveurs hors périmètre, dans les mêmes tx.
  - Rejeu hors ligne : le CSV publié est d'abord reproduit à l'octet près avec l'ancien décodeur ; avec le nouveau, 74 lignes s'ajoutent, aucune ne change. Seuls les horodatages des 74 tx ont été lus sur le RPC public (148 appels).
  - Conséquence : la ligne `26kExMGt` → 2d86 de `solana_to_evm_clusters.csv` passe de 1 à 16 ordres (63 838,91 USD). Le reste du dossier ne lit pas les exécutions reçues par 2d86.
  - Autocontrôle : `s99_selfcheck.py` (F9), sur deux reçus v2 figés.
