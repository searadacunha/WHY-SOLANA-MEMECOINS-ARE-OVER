# DMAGA × Kekius Maximus : constats vérifiés

Enquête du 06/11/2026, branche `investigate/dmaga-kekius-cross-token`, base `main` `0f77f26`. Question : une même entité
financière a-t-elle participé à Dark MAGA (juillet 2024) et aux tokens Kekius Maximus (décembre 2024), en suivant les fonds ?

Statuts : **CONFIRMÉ** (transfert ou relation transactionnelle relue), **CORROBORÉ** (plusieurs indices indépendants),
**HYPOTHÈSE**, **REJETÉ** (service partagé, erreur ou explication alternative vérifiée). Un transfert confirmé ne démontre ni
une identité commune, ni une information privilégiée. Les reçus des transactions citées sont figés dans
`evidence/receipts/` et relus par `tests/test_selfcheck.py` (hors ligne).

**État de cette version : unité 2.** Le test de l'univers DMAGA (7 152 adresses × 2 mints Solana) est complet (§7). La réponse figure au §8.

## 1. Les tokens retenus

| Token | Chaîne | Adresse | Création (UTC) | Créateur | Lieux d'échange |
|---|---|---|---|---|---|
| KM « Kekius Maximus » | Solana, Pump.fun | `HuAncxDEsakCDgZS2Yfo9xJbHmtHXMnxxkT9jqdXnHhm` | 2024-12-10 07:29:00, sig `51W3rg9B…` | `4GUgVRftPkeqTNFc7nwZVRjqheBPMVToAhNYdkQVUz3e` | courbe `92d2Pput…`, migration à 07:31:01, Raydium `6R3yY5hpJ2RugzWx6ex4SVsoReK87jEoBu2hWh5XhuE2` |
| KEKIUS « Kekius Maximus » | Solana, Pump.fun | `XC78JjRHnSqaysrHiTrhR8eRngFbvX3rrHyRjWEpump` | 2024-12-29 16:33:45, sig `2xz9tgPB…` | `9dtGg97QAfxc2UF4LGaxLzYdB4MJpnNMK7Y2iUwGidoy` | courbe `8bHymiGn…`, migration à 16:36:01, Raydium `CjyDeB42w4QSFA5pwpKC85SEZh92zsG8ARULLw8bc4Lh` |
| KEKIUS « Kekius Maximus » | Ethereum, ERC-20 à taxe | `0x26e550ac11b26f78a04489d5f20f24e3559f7dd9` | 2024-12-14 02:29:35, bloc 21397776, tx `0x834a43c8…6c43` | `0xaa4f58e9aafd36b4b6446f6dc417c02908641a7c` | Uniswap V2 `0xfff8d5fff6ee3226fa2f5d7d5d8c3ff785be9c74` (ouverture 02:43:59), Uniswap V3 `0xa2542303c9a01c011da9106128d9b0838e6c3e57` |

- Les deux adresses de départ de la mission sont vérifiées : `0x26e5…7dd9` est bien le KEKIUS Ethereum que la presse cite (The Block), `HuAncx…` est KM.
- Le « token frère » noté dans `docs/PRIOR_WORK.md` (`XC78…pump`, wallet `Go5rFkwK…`) est le troisième.
- **Aucun des trois n'est créé après le changement de profil.** Chacun suit de près un post public de Musk : KM 4 s après « Amazing 🤩 » (10/12 07:28:56), KEKIUS Ethereum 24 min après « Kekius Maximus 😂 » (14/12 02:05:30), XC78 75 min après le post sur son personnage Path of Exile (29/12 15:18:03). Voir `TIMELINE.md`.
- L'autorité `TSLvdd1p…` commune à KM, XC78 et DMAGA est celle de Pump.fun : **REJETÉ** comme lien (déjà établi dans l'enquête d'origine).
- Les autres copies (autres mints Solana, Base, BSC) ne sont pas inventoriées : `UNRESOLVED.md`.
- Les « KEKIUS » et « KekiusMaximus » reçus par b298 sur Base (31/12/2024 et 01-03/01/2025, `0x87d206c2…`, `0xcfab7252…`, `0x0b3f4786…`) arrivent d'un « UniswapV2Pair » dans une même tx et pour le même montant vers d'autres adresses (`0x2ac17414…`). Ils ressemblent à un envoi groupé de jetons indésirables. **NON VÉRIFIÉ** au-delà de cette observation, et sans rapport avec `0x26e5…`.

## 2. Le changement de profil de Musk

Nom et avatar passent à « Kekius Maximus » le **31/12/2024 entre 06:02:01 et 06:08:54 UTC**.
- Borne basse : capture Wayback JSON d'un post de Musk.
- Borne haute : capture d'écran du profil postée par un tiers, recoupée par la chaîne de citations reprise par Musk à 06:35:12.
- Le retour à « Elon Musk » n'est borné que par la presse (avant le 02/01/2025 04:27:29).
- Toutes les analyses « avant l'événement » coupent à **06:02:01**, la borne basse : c'est le choix prudent (rien n'est compté « avant » qui pourrait être après).

Sur Ethereum, la réaction visible commence à la minute 06:07 (12 achats, 22,36 ETH). De 05:45 à 06:06, on compte 0 à 4 achats par minute. Aucune accumulation visible dans le quart d'heure qui précède.

## 3. Ethereum : aucun wallet DMAGA ne trade le KEKIUS Ethereum

- 292 326 transferts du contrat, du bloc 21397776 au bloc 21547396 (04/01/2025 00:00 UTC), source Routescan `tokentx`.
- 38 613 adresses, dont 35 256 acheteurs et 4 222 acheteurs avant 06:02:01.
- **CONFIRMÉ (absence)** : aucune des cinq adresses EVM issues des exécutions deBridge DMAGA n'apparaît dans ces transferts. Les cinq : b947 `0xb947bf7f409e998b28f8e218802fc9575c3c8c57`, b298 `0xb29826d809aa04d2ead6f2310d8965a45b87fa67`, 86f9 `0x86f99097c563e84dd5190f3e85f6a2988f1c47a5`, 2d86 `0x2d86499a410a9ac2139833ba8d6942b8a8700a7b`, relais `0x4978cd7e5a3565cafcc88a105940b0ea01adc04d`. Les historiques complets de b947, b298, 86f9 et 2d86 publiés par l'enquête du 05/11 le confirment de leur côté : aucun transfert de `0x26e5…`.
- Sur les 11 508 adresses EVM citées par les enquêtes deBridge, 9 apparaissent dans KEKIUS. Toutes sont **REJETÉES** comme lien (`WALLET_OVERLAP.csv`) :
  - solveur DLN `0x555ce236…` ;
  - bots MEV `0xfbeedcfe…` (étiquette Blockscout « MEV Bot », 911 346 tx) et `0x00000000009e50a7…` ;
  - portefeuille chaud MEXC 21 `0x9642b23e…` ;
  - routeur Sushi `0xf2614a23…` ;
  - quatre contreparties de jetons de 2d86 (`0x8526e4f2…`, `0xf081470f…`, `0xcf5540ff…`, `0x2052051a…`).
- 2d86 (afk.eth) trade des copies apparues après l'événement, TIBERIUS (02/01), BONKIUS (04/01) et FLAVIUS (05/01). Ce n'est **pas discriminant**.

## 4. XC78 : un lancement coordonné, confirmé par les transactions

Slot de création 310594124 (16:33:45), puis slot 310594130 (16:33:48). Reçus figés, test `test_go5_buy_then_split_to_ten_wallets`.

1. **CONFIRMÉ** : le créateur `9dtGg97Q…` n'achète que 354 jetons. Dans le même slot, `Go5rFkwKpTYGVck7emf4Uop81HBozmHHZfEhe2zJDY5u` achète 748 786 277,68 jetons (74,9 % de l'offre) pour 70,031366319 SOL (`5p39GsYP…`).
2. **CONFIRMÉ** : 3 secondes plus tard (`5GvjoEME…`, signataire unique Go5), Go5 revend tout. La courbe paie 69,41 SOL : Go5 garde 2,061527511 SOL et **chacun de 10 wallets reçoit exactement 6,655700950 SOL dans la même transaction** :
   - DcxRmDYU, 6CTNCLn7, EubFtsUh, DsPm2pXF ;
   - 3EcUR1sZ, F2jTjuYT, AMgtmMMF, 6vpKExvX ;
   - 8C9utWVQ, CF7MA2t9.
3. **CONFIRMÉ** : dans le même slot, 4 transactions **co-signées chacune par 4 wallets** achètent 673,91 M jetons (67,4 %) pour 16 wallets. Les 10 bénéficiaires du point 2 en font partie. Payeurs des frais : `DcxRmDYU…`, `3EcUR1sZ…`, `8C9utWVQ…`, `BmeKXuaj…`.
4. **CONFIRMÉ (index Jito), soumission commune** (`evidence/jito/`) :
   - La création `2xz9tgPB…`, signée par le créateur, et l'achat de 74,9 % par Go5 (`5p39GsYP…`) forment **un même bundle Jito**, `516a792e…` (slot 310594124, `blockIndex` 1621). **Go5 paie le pourboire** de 0,05 SOL.
   - Au slot 310594130, la vente-redistribution de Go5 et les 4 rachats co-signés forment **un seul bundle**, `6317153c…` (5 transactions), pourboire de 0,1 SOL payé par Go5.
   - Un bundle est envoyé d'un bloc par un seul expéditeur, qui détenait donc déjà les transactions signées du créateur, de Go5 et des 16 wallets. **Le créateur et l'opérateur agissent de concert : CORROBORÉ** (index hors chaîne, plus transferts et co-signatures sur la chaîne). Le créateur `9dtGg97Q…` n'échange en revanche aucun SOL avec Go5 ni avec `3oqARBND…` (point 6) : pas de flux de fonds entre eux.
   - Pour comparer : la création de KM est seule dans son bundle `b722456c…`, pourboire de 0,008 SOL payé par son créateur. L'achat DMAGA de `FJkb8WnW…` (14/07/2024) est lui aussi seul dans son bundle `b18117c9…`, pourboire de 0,01 SOL payé par FJkb8WnW : un geste de bot de sniping.
5. **CORROBORÉ, contrôle commun** de Go5 et de ces 16 wallets : Go5 paie 10 d'entre eux dans sa propre transaction. Signer à quatre une même transaction suppose que les clés étaient réunies au moment de la construire. Six des 16 acheteurs n'ont pas reçu de SOL de Go5 dans cette transaction : les 4 du groupe payé par `BmeKXuaj…`, plus `A7ZxBfBx…` et `7qnbEYhM…`. Comme les 10 autres, ils ont été **financés par `3oqARBND…`** (point 7).
6. **Créateur `9dtGg97Q…` : lanceur en série** (1 839 tx depuis mars 2024).
   - Il crée encore deux tokens Pump.fun sur des thèmes Musk : « Elon's Alterego Adrian Dittmann » `LYHrmUwemzqSKirX4LRX9tXVkx2HnraTgze8Zbepump` le 30/12 à 17:39:55 (sig `33Pw67cN…`), et « Trumpus Maximus » `WAJmwPfRFnuonu2SHy5YpZTAfwENGVAnECahSZPpump` le 31/12 à 12:10:25 (sig `3NkgZoab…`), après le changement de profil. Chacun migre en moins de 2 minutes, et le créateur touche chaque fois la prime de migration de 0,5 SOL, comme pour XC78.
   - Aucune de ses 52 transactions du 23/12 au 01/01 ne touche Go5, `3oqARBND…`, `5S1wWxWZ…`, `2sGCJ7Z3…` ou `C6UEzXJc…`.
   - Un lien de fonds entre le créateur et l'opérateur reste **NON VÉRIFIÉ** : il n'est pas trouvé dans cette fenêtre.
7. **CONFIRMÉ, financement de l'opération** : Go5 est un wallet neuf (24 tx en tout).
   - `3oqARBNDr56L2oWQ9aR2QzS7FeTMEubd8J2v29wP5N58` le crédite de 70,06 SOL à 16:31:42, 2 minutes avant la création.
   - Le 30/12, les fonds reviennent à `3oqARBND…` : 11,916 SOL dans une tx co-signée par Go5, `5S1wWxWZ…` et `2sGCJ7Z3…`, puis 1,976 SOL de Go5.
   - Chaque retour verse des frais à `C6UEzXJcTqqJHpAGUts2tA4s6E7MS5KoPzzfsrT6qCpL`, à un taux presque constant (6,957 % et 6,961 %) : service probable.
   - `3oqARBND…` naît le 23/12/2024 avec 86,08 SOL de `FBwXQAEb…`. Cette adresse n'a pas d'étiquette mais fait plus de 2 000 transactions en 12 jours : service probable, **traçabilité rompue**. `3oqARBND…` redistribue ensuite ses fonds à de nombreux wallets (16 virements le 25/12) et compte 4 386 tx jusqu'en 2026 : profil d'opérateur de lancements en série.
   - **CONFIRMÉ** : une seule transaction de `3oqARBND…` finance les 16 wallets des achats co-signés, **70,472 SOL** au total (de 1,346 à 14,379 SOL chacun), le 29/12 à **16:31:41** (`3UrcoNZA…`). C'est 1 s avant Go5, et 2 min 04 s avant la création.
   - Historiques complets des 16 wallets : 24 à 63 tx chacun, actifs du 29/12 16:31:41 au 31/12 09:33:11 (`data/xc_bundle_counterparties.csv`). Ils n'ont que 5 contreparties d'au moins 0,5 SOL :
     - le pool XC78 : 78 tx de vente, 816,64 SOL sortis du coffre WSOL ; 14 tx d'achat, 89,0 SOL ;
     - la courbe XC78 ;
     - `3oqARBND…` : 14 tx de retour, 745,29 SOL crédités ;
     - `C6UEzXJc…` : 7 tx, 40,41 SOL ;
     - `8Q7G3PuW…` : 5 tx, 9,54 SOL.
   - **Bilan de l'opérateur sur XC78** :
     - mise : 140,53 SOL engagés à 16:31:41-42 (70,472 vers les 16 wallets, 70,06 vers Go5) ;
     - retours vers `3oqARBND…` : 759,18 SOL (745,29 des 16 wallets, 13,89 de Go5) ;
     - frais versés à `C6UEzXJc…` et `8Q7G3PuW…` : 51,12 SOL ;
     - résultat net pour `3oqARBND…` : **+618,65 SOL**, frais déduits puisqu'ils ne lui reviennent pas.
   - Correction interne : une première version de `k36` additionnait la variation de la contrepartie ligne à ligne. Elle donnait « 1 129,01 SOL en 16 virements » et « 2 045,67 SOL en 38 virements », des chiffres gonflés : une même transaction était comptée une fois par wallet. Ces chiffres ont été **publiés à tort dans le commit `edfe2f9`** et sont corrigés ici.
   - `3oqARBND…`, `5S1wWxWZ…`, `2sGCJ7Z3…`, `C6UEzXJc…`, `FBwXQAEb…` et le payeur `43TVSaqF…` n'apparaissent dans **aucune** table DMAGA (wallets, financements, sorties, nœuds) : **aucun lien DMAGA trouvé** pour cet opérateur.
8. Ce montage (achat bloquant au slot de création, puis redistribution vers des wallets qui rachètent) est un schéma de lancement groupé. Il ne dit rien d'une connaissance du changement de profil de Musk, qui intervient 37 heures plus tard.

KM (10/12) : 133 acheteurs sur la courbe en 2 min 01 s. Les 100 premiers (`data/sol_first100_buyers_KM.csv`) n'ont que 2 tx co-signées, et aucune redistribution de ce type n'a été cherchée en détail (`UNRESOLVED.md`).

## 5. KEKIUS Ethereum : le wallet `0x33a57f4e88c9ceb0788eb41a407e51533d70cc4d`

Recalculé depuis les transferts et la jambe WETH des pools (test `test_0x33a5_pre_event`), sans reprendre de chiffre publié.

- **CONFIRMÉ** : 7 achats avant le changement, du 19/12 07:55:47 au 30/12 17:52:11, pour **8,4482 M KEKIUS contre 16,0 ETH**. Les montants sont ronds : 1, 1, 3, 3, 3, 3 et 2 ETH, via le Universal Router.
- **CONFIRMÉ** : 15 ventes le 01/01/2025, de 07:34:47 à 21:27:47, pour **285,71 ETH** jusqu'au 04/01. Rachat de 0,9151 M pour 40 ETH le 02/01. Il garde 5,66 M au 04/01.
- **Financement CONFIRMÉ, traçabilité rompue** :
  - tous les apports de 2024 viennent de portefeuilles chauds Binance (étiquettes Blockscout) : `0x4976a4a0…`, `0xdfd5293d…`, `0x28c6c062…`, `0x21a31ee1…`, `0x9696f59e…` ;
  - au départ (mars 2024), ils viennent de la rampe fiat Ramp Network `0x98db3a41…` ;
  - aucun financeur personnel n'est identifiable.
- **Destination CONFIRMÉE, traçabilité rompue** : le 05/01/2025, 5 puis 60 ETH vont à `0xecaa5a79369f147015a6c6f28ab4479f68994a8d`, qui les reverse au portefeuille chaud Binance `0x28c6c062…` en 5 min 24 s et 2 min 48 s (tx `0x2e63bc85…`, `0xd902cd0c…`). Ce comportement en fait une adresse de dépôt Binance **inférée** (elle n'a pas d'étiquette). Elle a déjà reçu 75 ETH en mai-juin 2024.
- Aucune interaction avec une adresse DMAGA ou deBridge connue.
- **Non distinctif** : 4 222 adresses achètent avant le changement. Par ETH dépensé entre le 20/12 et le changement, `0x33a5` n'est que 21e.
  - Beaucoup de premiers achats tombent le 27/12 vers 03:00-04:30 UTC, le moment où le personnage Path of Exile « Kekius Maximus » de Musk circule.
  - Ce wallet trade des memecoins Ethereum depuis mars 2024.
  - Ses achats sont compatibles avec un pari sur des signaux publics. Rien ici n'établit une information privilégiée.
- Depuis 2025, l'adresse délègue à `CaliburEntry` (EIP-7702, portefeuille Uniswap). C'est sans incidence sur 2024.

Créateur du KEKIUS Ethereum :
- `0xaa4f58e9…` est financé une seule fois, 1,47295009 ETH le 14/11/2024 depuis un portefeuille chaud ChangeHero : service d'échange, traçabilité rompue.
- Il apporte 1 ETH de liquidité, ouvre le trading puis renonce à la propriété en 1 min 24 s.
- 50 adresses achètent dans le bloc d'ouverture.
  - 44 n'ont reçu aucun ETH par une tx directe avant ce bloc : financement par transaction interne, ou adresses de destination de bots.
  - Les 6 autres ont pour premier financeur un portefeuille chaud Binance (4) ou une adresse non étiquetée (2) (`data/eth_open_block_funders.csv`).
  - Aucune n'est financée par le créateur. Le financement des 44 n'est **pas résolu**.

Plus gros vendeur sans achat : `0xb1b2d032aa2f52347fbcfd08e5c3cc55216e8404` vend 32,25 M contre 1 424,10 ETH jusqu'au 04/01.
- **CONFIRMÉ** : ses jetons viennent de retraits d'exchanges : MEXC 21 (23,42 M dès le 29/12, tx `0x68c52712…`), Gate.io (10,16 M le 02/01) et CoinEx 26 (1,60 M le 31/12).
- Profil d'arbitrage entre exchanges et DEX, ou de teneur de marché. **Traçabilité rompue** chez les exchanges.
- Aucun lien avec DMAGA.

## 6. Un lien DMAGA ↔ XC78 qui passe par un opérateur de bot

- **CONFIRMÉ** : `DQmMnakiKr1YNE2gcpggLCzBrauBwFbQkAaao2FTbjgp` → `FJkb8WnWocfuQYj4v4vg5VpZoST3LebjQk8WpuD7VbgC`, 1 SOL le 10/07/2024 (`3kXEwKY5…`) et 1,474847595 SOL le 11/07/2024 (`4dChb1EM…`), signataire unique.
- **CONFIRMÉ** : `FJkb8WnW…`, wallet DMAGA prioritaire, achète 12,29 M DMAGA pour 5 WSOL le 14/07/2024 à 02:15:33 (`meMfnP6C…`), 2 s après la migration. `DQmMnaki…` achète XC78 pour 1 WSOL le 29/12/2024 à 16:36:52 (`5xqzEckQ…`), 1 s après l'initialisation du pool. **Les deux passent par le même programme `9NLjj4Gj2fEYhujN7znkiLTVjDsiKi7h1mQvMdEffDTw`**, avec du WSOL préchargé.
- **CORROBORÉ** : même opérateur de bot de sniping de migration, par le transfert direct, le programme commun et le même geste à 1-2 s des migrations.
- **Interprétation** : ces deux adresses font chacune plus de 3 000 transactions par mois en 2026. Un bot qui achète chaque pool à l'ouverture se retrouve dans DMAGA comme dans XC78, sans rien savoir de Musk. Ce lien **n'est pas discriminant** pour la question posée.
- La part de ce programme dans l'ensemble des migrations n'est pas mesurée.

## 7. Univers DMAGA contre KM et XC78 : test complet

Méthode : `METHODOLOGY.md`, historique de l'ATA de chaque adresse pour chaque mint.
- Univers : **7 152 adresses × 2 mints = 14 304 couples, tous testés** (`data/ata_scan_summary.csv`).
- Fenêtre : de la création de chaque token au 04/01/2025. « Avant » veut dire avant 06:02:01 le 31/12.
- Résultat d'ensemble : 13 848 couples sans aucune activité. Restent 290 bots ou traders à haute fréquence (critère ATA ou DMAGA), 28 à haute fréquence au niveau du wallet, 41 services étiquetés et 97 couples peu actifs.

| Partie de l'univers DMAGA | Couples | Actifs dans la fenêtre | Actifs avant le changement | Nature des actifs avant le changement |
|---|---|---|---|---|
| Groupe des 33 | 66 | **0** | **0** | |
| Noyau nommé (créateur, gagnants `H3QsBrr…`, `GXZvXs…`, `9PrmF8…`, `5QhJJc…`, `Ei5yGz8d…` et les wallets deBridge, `B5fC3Dg4…`, `FKtvVzBS…`, `G41vRrs…`) | 88 | **0** | **0** | |
| Contreparties directes du noyau (468 financeurs et destinations de sortie, hubs exclus) | 936 | 2 | 1 | `DMJmb8aJ…`, trader à haute fréquence |
| Wallets prioritaires (857) | 1 714 | 95 | 37 | les 37 sont des bots ou traders à haute fréquence |
| Membres de clusters (3 508) | 7 016 | 195 | 32 | 27 haute fréquence, 5 peu actifs |
| Adresses citées par les rapports (3 429) | 6 858 | 176 | 96 | 66 haute fréquence, 28 services, 2 peu actifs |

**Aucun wallet du groupe des 33, du noyau ou des gagnants DMAGA ne touche KM ni XC78**, ni avant ni après le changement de profil, jusqu'au 04/01/2025.

Contreparties du noyau :
- **CONFIRMÉ** : `5QhJJcFZu2ashyKyWSTGHcsyo6ZBCbpVuJqeutvQHScd`, gagnant DMAGA lié au créateur, crée le compte USDC de `DMJmb8aJMzzNur1hAwQoArPEX8dLfbuuuYZnGn6jd8DL` puis lui transfère **7 000 USDC le 20/01/2025 à 05:35:54** (`4DWwAWbH…`, signataire unique).
- **CONFIRMÉ** : `DMJmb8aJ…` achète KM le 14/12/2024 à 02:18:17 (`5ZxEY11s…`), 12 min 47 s après le post « Kekius Maximus 😂 » de Musk. Il achète aussi XC78 à partir du 31/12 06:26:26, après le changement.
- **Chronologie incompatible avec le scénario « gains DMAGA → achat Kekius »** : le virement de 5QhJJc arrive 37 jours après l'achat KM, pas avant.
- `DMJmb8aJ…` est un trader à haute fréquence : environ 1 000 tx dans les 24 h avant son achat KM. Son premier achat DMAGA date du 20/01/2025 à 10:24:39 (10 SOL), 4 h 49 min après le virement de 5QhJJc. Le transfert est direct et personnel : 5QhJJc crée le compte de destination. **HYPOTHÈSE** : un même propriétaire, ou un paiement entre deux personnes. Rien ne départage les deux.

Les 7 couples peu actifs d'avant le changement (`data/ata_overlap.csv`) :
- **Calendrier des premiers achats Kekius** :
  - trois tombent le 14/12, entre 02:10:14 et 02:20:17, de 5 à 15 min après « Kekius Maximus 😂 » (02:05:30) : `DZwQ66i2…`, `EwPnMPtr…`, `CKMVA5xe…` ;
  - `aaYqdhGp…` achète le 10/12 à 07:37:46, 9 min après la création de KM ;
  - les trois autres achètent plus tard : `G2aZ6e8Q…` le 15/12, `G1Qo4NyE…` le 24/12, et `Ejh8nKp4…` sur XC78 le 29/12 à 22:31, 6 h après la création, puis en 48 allers-retours.
- **Deux seulement ont acheté DMAGA en juillet 2024**, et tous deux ont perdu :
  - `DZwQ66i2…` : 0,2475 SOL le 14/07, perte de 0,11 SOL. Sur KM, il fait 8 achats (21,61 SOL), dont le premier 284 s après le post de Musk (`5XENanVA…`) ;
  - `Ejh8nKp4…` : 0,562 SOL le 15/07, perte de 0,0035 SOL.
- **Les cinq membres de clusters** sont dans 5 petits clusters DMAGA différents. Quatre achètent DMAGA en octobre 2024 ; `G2aZ6e8Q…` n'a aucun achat DMAGA. **HYPOTHÈSE** : `CKMVA5xe…` et `aaYqdhGp…` achètent DMAGA pour la première fois à 94 s d'intervalle (05/10/2024 23:09:47 et 23:11:21), sans lien de fonds relu.

Correspondances directes avec les 100 premiers acheteurs KM et XC78 (`WALLET_OVERLAP.csv`) :
- `CaShxDq2…`, `DQeJQ91U…` et `ATomG2gR…` achètent DMAGA pour 0,0002 SOL à 02:15:44-45, 13 s après la migration. Leurs « financements » enregistrés viennent de l'autorité Raydium, c'est-à-dire de produits de swaps : bots d'arbitrage, **non discriminant**.
- `CH7MJuK5…` fait 8 639 virements vers 88 wallets, achète DMAGA 104 fois et touche KM 3 461 fois. `D2vZhPW1…` lui envoie 5 530 SOL. Hub ou bot, **REJETÉ** comme lien personnel.
- 8 adresses parmi les 100 premiers de KM ont tradé DMAGA, toutes après le changement de photo du 21/07/2024 ; la plus précoce, `7wYSQEU1…`, achète le 22/07 à 03:20. Même adresse, CONFIRMÉ, mais **non discriminant**.

## 8. Réponse à la question

**Aucune même entité financière n'est démontrée dans les deux opérations.** Le suivi des fonds donne :
1. **Nouvelles relations financières, toutes CONFIRMÉES** (`FUNDING_GRAPH.csv`) :
   - le montage XC78 : Go5 et l'opérateur `3oqARBND…`, la redistribution vers 10 wallets, les bundles Jito, les frais vers `C6UEzXJc…` ;
   - `DQmMnaki…` → `FJkb8WnW…`, deux wallets d'un même bot de sniping ;
   - `5QhJJc…` → `DMJmb8aJ…`, 7 000 USDC le 20/01/2025 ;
   - les flux Ethereum de `0x33a5…` et du créateur du KEKIUS Ethereum.
2. **Wallets présents dans les deux événements** :
   - des bots, des traders à haute fréquence et des services ;
   - quelques petits traders qui réagissent aux posts publics de Musk ;
   - aucun gagnant DMAGA de juillet 2024.
   - Le seul lien entre un gagnant DMAGA et un acheteur Kekius (5QhJJc → DMJmb8aJ) est postérieur à l'achat Kekius.
3. **Profits vérifiés** :
   - `0x33a5…` : 16,0 ETH d'achats avant le changement, 285,71 ETH de ventes jusqu'au 04/01 ;
   - `0xb1b2…` : 1 424,10 ETH de ventes, avec des jetons retirés d'exchanges ;
   - XC78 : l'opérateur `3oqARBND…` engage 140,53 SOL et en récupère 759,18, soit +618,65 SOL nets.
4. **Liens entre chaînes** :
   - aucun entre DMAGA et le KEKIUS Ethereum par les destinataires deBridge ;
   - aucun pont observé dans les flux relus ici.
5. **Explication la plus économe** : les trois tokens naissent de posts publics de Musk (10, 14 et 29/12). Les achats précoces suivent ces posts de quelques secondes à quelques minutes. L'accumulation avant le 31/12 est diffuse : sur Ethereum, 4 222 acheteurs. Les opérations coordonnées observées (lancement groupé de XC78, bots de sniping) sont des schémas de lancement, sans lien de fonds avec DMAGA.

Ce que ce résultat n'exclut pas :
- une même personne derrière des wallets **sans lien de fonds lisible**, parce que la traçabilité s'arrête aux exchanges, aux services ou aux bridges ;
- des achats par comptes de jetons non associés, que le test ATA ne voit pas ;
- d'autres copies Kekius non inventoriées.

Voir `UNRESOLVED.md`.
