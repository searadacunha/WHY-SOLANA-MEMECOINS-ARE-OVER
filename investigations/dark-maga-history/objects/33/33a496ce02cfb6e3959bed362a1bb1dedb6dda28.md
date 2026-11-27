# DMAGA × Kekius Maximus : constats vérifiés

Enquête du 06/11/2026, branche `investigate/dmaga-kekius-cross-token`, base `main` `0f77f26`. Question : une même entité
financière a-t-elle participé à Dark MAGA (juillet 2024) et aux tokens Kekius Maximus (décembre 2024), en suivant les fonds ?

Statuts : **CONFIRMÉ** (transfert ou relation transactionnelle relue), **CORROBORÉ** (plusieurs indices indépendants),
**HYPOTHÈSE**, **REJETÉ** (service partagé, erreur ou explication alternative vérifiée). Un transfert confirmé ne démontre ni
une identité commune, ni une information privilégiée. Les reçus des transactions citées sont figés dans
`evidence/receipts/` et relus par `tests/test_selfcheck.py` (hors ligne).

**État de cette version : unité 1.** Tokens, chronologie, Ethereum complet, structure des lancements Solana et 100 premiers
acheteurs. Le test de l'univers DMAGA (7 152 adresses × 2 mints Solana) est **en cours** et n'est pas encore interprété ici (§7).

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
4. **CORROBORÉ, contrôle commun** de Go5 et de ces 16 wallets : Go5 paie 10 d'entre eux dans sa propre transaction. Signer à quatre une même transaction suppose que les clés étaient réunies au moment de la construire. Six des 16 acheteurs n'ont pas reçu de SOL de Go5 dans cette transaction : les 4 du groupe payé par `BmeKXuaj…`, plus `A7ZxBfBx…` et `7qnbEYhM…` du groupe payé par `8C9utWVQ…`. Leur financement est **NON VÉRIFIÉ**.
5. **NON VÉRIFIÉ** : un lien entre le créateur `9dtGg97Q…` (1 839 tx depuis mars 2024) et Go5 ou `3oqARBND…`.
6. **CONFIRMÉ, financement de l'opération** : Go5 est un wallet neuf (24 tx en tout).
   - `3oqARBNDr56L2oWQ9aR2QzS7FeTMEubd8J2v29wP5N58` le crédite de 70,06 SOL à 16:31:42, 2 minutes avant la création.
   - Le 30/12, les fonds reviennent à `3oqARBND…` : 11,916 SOL dans une tx co-signée par Go5, `5S1wWxWZ…` et `2sGCJ7Z3…`, puis 1,976 SOL de Go5.
   - Chaque retour verse des frais à `C6UEzXJcTqqJHpAGUts2tA4s6E7MS5KoPzzfsrT6qCpL`, à un taux presque constant (6,957 % et 6,961 %) : service probable.
   - `3oqARBND…` naît le 23/12/2024 avec 86,08 SOL de `FBwXQAEb…`. Cette adresse n'a pas d'étiquette mais fait plus de 2 000 transactions en 12 jours : service probable, **traçabilité rompue**. `3oqARBND…` redistribue ensuite ses fonds à de nombreux wallets (16 virements le 25/12) et compte 4 386 tx jusqu'en 2026 : profil d'opérateur de lancements en série.
   - `3oqARBND…`, `5S1wWxWZ…`, `2sGCJ7Z3…`, `C6UEzXJc…`, `FBwXQAEb…` et le payeur `43TVSaqF…` n'apparaissent dans **aucune** table DMAGA (wallets, financements, sorties, nœuds) : **aucun lien DMAGA trouvé** pour cet opérateur.
7. Ce montage (achat bloquant au slot de création, puis redistribution vers des wallets qui rachètent) est un schéma de lancement groupé. Il ne dit rien d'une connaissance du changement de profil de Musk, qui intervient 37 heures plus tard.

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

## 7. Univers DMAGA contre KM et XC78 : test en cours, non interprété

- **Méthode** : pour chaque adresse et chaque mint, historique du compte de jetons associé (ATA). 7 152 adresses :
  - 857 prioritaires ;
  - le groupe des 33 ;
  - 3 508 membres de clusters ;
  - 3 429 adresses citées par les rapports et enquêtes ;
  - le noyau de la mission (44) et 468 contreparties directes.
- **Avancement** : 10 058 couples sur 14 304 au moment de cette version.
- **Résultats partiels, à ne pas citer** : les premières adresses actives avant le changement sont surtout des bots à haute fréquence. Exemple : 7 wallets « ≥ 1 M avant l'avatar » de DMAGA, qui font 328 à 493 allers-retours de 0,2 à 0,5 SOL.
- Groupe des 33 : 48 couples sur 66 testés, **aucune activité** sur KM ni XC78.

Correspondances directes déjà vérifiées entre les 100 premiers acheteurs KM / XC78 et les 71 706 wallets DMAGA (`WALLET_OVERLAP.csv`) :
- `CaShxDq2…`, `DQeJQ91U…` et `ATomG2gR…` achètent DMAGA pour 0,0002 SOL à 02:15:44-45, 13 s après la migration. Leurs « financements » enregistrés viennent de l'autorité Raydium, c'est-à-dire de produits de swaps : bots d'arbitrage, **non discriminant**.
- `CH7MJuK5…` fait 8 639 virements vers 88 wallets, achète DMAGA 104 fois et touche KM 3 461 fois, et `D2vZhPW1…` lui envoie 5 530 SOL : hub ou bot, **REJETÉ** comme lien personnel.
- 8 adresses parmi les 100 premiers de KM ont tradé DMAGA, toutes après le changement de photo du 21/07/2024. La plus précoce, `7wYSQEU1…`, achète le 22/07 à 03:20. Même adresse, CONFIRMÉ, mais **non discriminant**. Trois d'entre elles (`GTvBQnRv…`, `xK5mDD8D…`, `8J9panvq…`) achètent pour la première fois DMAGA en moins de 14 minutes, entre le 05/11/2024 23:53:51 et le 06/11 00:07:29 : HYPOTHÈSE d'un même opérateur, `UNRESOLVED.md`.

## 8. Réponse provisoire à la question

Pas avant la fin du test du §7.
- À ce stade, **aucune entité n'est démontrée commune** aux deux opérations par un flux de fonds non mutualisé.
- Aucun flux DMAGA → Kekius n'est trouvé : ni sur Ethereum, ni par deBridge, ni par les 100 premiers acheteurs.
- Seul lien confirmé : un opérateur de bot de sniping, non discriminant.
