# Dark MAGA / deBridge : Base, BSC et retour Solana, version auditée (06/11/2026)

Jeton `7D7BRcBYepfi77vxySapmeqRNN1wsBBxnFPJGbH5pump`. Personne n'est accusé et aucune identité civile n'est présumée. Un nom d'exchange désigne un service, jamais une personne. On distingue toujours *même destination*, *même opérateur* et *même bénéficiaire effectif*. Heures en UTC.

Ce dossier reprend le dépôt privé `dmaga-debridge-next-trace` (commits `009157e` et `cd00015`, non republiés). Il a fait l'objet d'un audit contradictoire en trois volets :
- un recalcul Solana indépendant depuis les transactions brutes ;
- un recalcul EVM indépendant ;
- une revue du code.

Les corrections sont détaillées dans `AUDIT.md`.

**Niveaux** :
- **VERIFIED** : relu sur la chaîne, hash donné, rejoué hors ligne par `scripts/s99_selfcheck.py` (31 assertions) ou `tests/` ;
- **SUPPORTED** : plusieurs signaux indépendants concordent ;
- **EXPLORATORY** : un signal seul ;
- **UNRESOLVED** ;
- **REFUTED**.

Une **borne** est une quantité minimale garantie pour *toute* règle d'allocation qui conserve la valeur, sans FIFO. La démonstration est dans `scripts/s60_positions.py`.

**Hypothèse H** : la convention du dossier précédent (`s51_bounds.py`), qui suppose que le relais `0x4978cd7e…` ne transporte que des fonds de b947. L'audit montre que H n'est pas acquise (§3). Chaque borne est donc donnée **sous H** et **sans hypothèse**.

**Adresses** :
- b947 = `0xb947bf7f409e998b28f8e218802fc9575c3c8c57` ;
- b298 = `0xb29826d809aa04d2ead6f2310d8965a45b87fa67` ;
- relais = `0x4978cd7e5a3565cafcc88a105940b0ea01adc04d` ;
- `Ei5yGz8d` = `Ei5yGz8dPndr1aCeHZsfqJBcS3VBbz75VHEhxxJKLy3V`.

## 0. Ce qui change par rapport au dépôt privé

| Affirmation du dépôt privé | Après audit |
|---|---|
| « Au moins 23,7486 ETH des 24 ETH déposés chez Coinbase viennent de b947 » | **Sous H** : au moins 23,748588117 ETH. La valeur publiée incluait 459,67 gwei de frais. **Sans hypothèse** : 0 (§3) |
| « Au moins 100 067,30 USDC (54,82 %) des 182 548,80 USDC déposés chez MEXC viennent de b947 » | **Sous H** : au moins 100 027,93 USDC (54,80 %) au prorata, 99 383,28 USDC (54,44 %) en attribution stricte par pool. **Sans hypothèse** : 0 (§3) |
| Les deux bornes ensemble | **Nouveau, sans hypothèse** : les deux ordres du 12/11 portent ensemble au moins **100 028,638296 USDC venus de b947**, et les deux bornes ne peuvent pas être nulles en même temps (§3). Si l'on ne marque que l'USDC des exécutions deBridge reçues par b947 : au moins 50 015,307517 |
| « La dernière part (BONK) est exacte » | C'est un prorata. La vente passe par trois pools à des prix différents : en strict, 0,547621 au lieu de 0,551168 |
| 87 liens deBridge | **88** : l'ordre `0x1596c70d…` (06/08/2024), exécuté par un solver tiers, manquait. Les 88 sont authentifiés par l'orderId recalculé. Ce sont les 88 liens construits par `s52_links.py` : ordres entre Base et Ethereum, ordres d'Ethereum et de Base vers `Ei5yGz8d`, aller-retour BSC. Les 11 autres ordres exécutés de b298 et b947, dont les 9 d'`Ei5yGz8d` vers Ethereum, sont au dossier précédent (`dln_orders_evm.csv`) |
| 19 ordres DLN d'`Ei5yGz8d`, plus un vingtième échoué | **18 ordres réussis et 1 échoué** (refait 16 s plus tard) |
| `E72DuqDL` : 94,96 SOL en 18 virements | **95,061118054 SOL en 20 virements**. Le seuil de 0,1 SOL omettait deux envois, ainsi que `2aeEoq5n` et `Gcyg2jeL` |
| 289,03 SOL « produit des ventes » rendus à `Ei5yGz8d` | Le retour inclut 1,0 SOL de gaz. Revenu net des ventes : **288,029811170 SOL** |
| 06/11 : « 34,00 SOL → Jupiter DCA » | 33,00 SOL déposés, **10,56 exécutés**, 22,44 rendus 65 min plus tard |
| 17/11 : DCA de 482 SOL, destination inconnue | **Nouveau** : tout le FvgqHM acheté part vers un wallet neuf, `2aeEoq5n`, qui le vend 393,81 SOL nets (§7) |
| HIGHER = `0xbf0533…` (`NEXT_STEPS.md`) | Faux : ce jeton date de mai 2024. Le HIGHER de novembre est `0x0578d8a44db98b23bf096a382e016e29a5ce0ffe` |
| Soldes Ethereum relevés à la main | Remplacés par des lectures d'état archive en cache, publiées en fixtures. Les écarts étaient de −4, −3 272 et +5 wei |

## Couverture

| Lot | Statut | Chiffres |
|---|---|---|
| b298 sur Base | complet ; soldes ETH et USDC égaux à l'état archive | 897 tx signées sur 897 (nonces 0 à 896), 41 échouées, 2 349 transferts de jetons, 236 internes ; 42 points de contrôle, plus 4 recalculés par l'audit |
| `0x2ac17414…`, `0x34172888…` (Base) | complets | 49 et 11 mouvements |
| b298 sur BSC | fenêtre DMAGA complète | 108 changements d'état, 95 tx signées. Blocs 43950885 à 43951101 relus sur l'état archive (Tatum) : nonce 83 → 84, une seule tx |
| Solana | 18 historiques complets, sans rupture de solde | `Ei5yGz8d` (2 823 tx), 8 wallets du dépôt privé, plus `39dTXaMM`, `Hp2BtvnZ`, `5yYnURUv`, `CAX7f8ET`, `HGBiExZR`, `Gcyg2jeL`, `4wComYHQ`, `EB6NoHkA`, lus le 06/11 |
| Liens entre chaînes | VERIFIED | 88 ordres DLN. Pour chacun, l'orderId est recalculé (keccak256 de l'ordre) et égale celui émis par le contrat, avec le même maker, le même receveur et le même montant (`scripts/s13_orderid_check.py`) |

---

## 1. Base : 24 ETH vers le dépôt Coinbase de b298. Trajet VERIFIED ; part b947 : sous H seulement

**Chemin** : relais → b298 (Ethereum) → deBridge → b298 (Base) → `0x34172888e808debea84bb224bbfa8dcd6d78de7d` → Coinbase 14.

| Étape | Preuve |
|---|---|
| 12/11/2024 01:42:47 : le relais envoie 200 000 USDC à b298 | `0x6a7e85b547…` (`relay_4978_history.csv` du dossier précédent) |
| 01:44:23 : ordre Ethereum o1 de b298, 100 048,914457 USDC | `0x4b7c7a2fcda576c58c961dee9d35840fba0151a9156cc0c48a0282c2fb024e16`, orderId `0x001592b334c6954a3b309e123b7054a2ee882fb40a220df8cf8ee59a4e460da6` |
| 01:44:39 : exécution Base, 29,736346520245492451 ETH à b298. Solde avant : 0,250791022861465593 ETH | `0xf130eea66394f17d0e48bb7cf88926178504a1c9735fc659c673457e1882e996` (même orderId) |
| 01:48 → 07:46 : six achats de HIGHER et BOOMER, 4,0 ETH, plus 0,000036 ETH de gaz. Aucune entrée d'ETH entre-temps | grand livre Base |
| **08:57:51 : 24,0 ETH vers `0x34172888…`** | `0x52da33cb31aa36ecce1a05774dd7bc69bed8d0a9b555db97e8659771a4a00245` |
| 08:58:05 : balayage de 24,000049013061517 ETH vers `0x20fe51a9229eef2cf8ad9e89d91cab9312cf3b7a` (Coinbase 14, étiquette Blockscout) | `0x897371dbff83768c73d67a6c85fc59d947fd270cca6474e3f623e891c50f81fa` |

- **Borne** :
  - sous H : au moins **23,748588117 ETH** des 24 ETH ;
  - sans hypothèse : 0, parce que o1 peut ne porter que 46,81 USDC de b947 (§3).
- **Nature de `0x34172888…`** : adresse de dépôt Coinbase inférée, niveau SUPPORTED.
  - 5 entrées, de b298 (4) et de son satellite Base `0x4b6a508cd730434b4f9a0e32be3646f71b58a8d3` (1). Les deux s'envoient aussi de l'ETH directement sur Base (4 tx).
  - Chaque entrée est balayée en 14 à 62 s vers un portefeuille étiqueté Coinbase (14, 31, 41, 42, 55). Une sixième sortie, de 0,000399 ETH, va à Coinbase 55.
  - Coinbase 31 et 42 portent l'étiquette « Exchange », pas « Hot Wallet ».
  - Dépôts de b298 dès avril 2024 :
    - 0,3169 ETH, `0x20740a952f1d0ccae0e301070ec885453c188197235f7cacdcf5dd05ff10902e` ;
    - 1,36 ETH, `0xcd870f489367c9fddb0bd5d70af37cb3e35f66b8f2d16e9328bcdcb22e689b35` ;
    - 0,3155 ETH, `0x58bd127e981d07dd2b553a67b88f36202d72b17f9eb7e9bd7777ef6c68f724df`.
- **Empoisonnement** : 13 min après les 24 ETH, un faux jeton « ETH.. » affiche 24 ETH envoyés vers le sosie `0x34171a96…de7d`. La vraie transaction n'est pas affectée. Le modèle par actif isole quatre jetons de ce type, dont deux faux « UЅDС » en lettres cyrilliques (`evidence/s60_b298_base_positions.csv`).

## 2. Ethereum → BSC → Ethereum → Solana → MEXC. Trajet VERIFIED ; part b947 : sous H seulement

| Heure | Fait | Preuve |
|---|---|---|
| 12/11 17:40:23 | relais → b298, 100 000 USDC | `0xd6162abed83f1b28b3ba469999a52c163023f26a21c6c51e1e1227ea70253476` |
| 17:42:47 | ordre o2 de b298 vers BSC : 99 989,828367 USDC, 157,374799465747581520 BNB demandés | `0xca82377984453a77f40592a694c5ad4c8076acce66b64a25e7c43f119f3cf8a4`, orderId `0xc62af9cf7ef4814f579a97750dfbcb8f51a383377fda39423dcd8514957d51d2` |
| 17:43:04 | BSC, bloc 43950886 : +157,374799465747581520 BNB ; avant : 0,104137489195757021 BNB (archive) | `0x549e4bc55eb2310b903f087d439b16af35c9d4c17624873012443c4eb6730afe` |
| 17:53:49 | BSC, bloc 43951101, seule tx (nonce 83 → 84) : 157,457034124656041152 BNB échangés en ETH BEP-20 et ordre vers b298 (Ethereum) ; frais 0,010961472 BNB | `0x76ffdad7e00a284fc1041b7c045319741bac650d4fdf7d1767524ddad2204f6c`, orderId `0x5c2e547ffa26cbc17ddc5650d2346cbd23155c8734d0e6d08fb929a84b36285e` |
| 17:54:11 | Ethereum, bloc 21173224 : 29,845089109620802062 ETH à b298 ; solde avant 0,129393990562924666 ETH, après 29,974483100183726728, inchangé jusqu'au bloc 21174281 | `0xf9b44d3ac32c0ad76280d57f31277844e6b5384ec399b7509b287668e128b3cf` |
| 21:26:35 | ordre de b298 vers `Ei5yGz8d` : valeur 29,019784588402031094 ETH (échangés en 94 624,840194 USDC), 445,496439103 SOL demandés | `0x2fa91216ea9d4a935d757217e3845caaa93fa90933769161b3ba122a9f935f85`, orderId `0x801581949a8c0d476a1a188b249642555b3c2d1c88f34cca7ebbdd372719ffa7` |
| 21:26:38 | +445,496439103 SOL à `Ei5yGz8d` ; avant : 0,111726858 SOL | `2w9jzrFEv6zzinjDFGPhJ2oNMLR5Kg2hSyg83bt5i7E9g4NZGHCDsogXKqdXrYWCfRWzktjxAxjgE1LNJPeE1oRk` |
| 21:28:25 | 445,000000000 SOL échangés → 2 765 715 481,82 BONK (le reste du débit : loyer 0,00203928 et frais) | `4AQCaW4eNyTP1gVNHMVz4a9tsCjZLcXnAyWD3viNHaZRNEXYtSZab2XZspwggbhAXHE8njgaxYDqspuyBYFCWJ5B` |
| 21:34:51 | `GJRs4FwHtemZ5ZE9x3FNvJ8TMwitKTh21yxdRPqn7npE` (Coinbase : « Coinbase 3 » chez Dune, « Coinbase Hot Wallet 11 » chez Orb) → `Ei5yGz8d`, 2 252 204 192,14 BONK | `29E3ro5i5TuZ9x9Kine8tM6PGtP1CXhQoN9KH1y35a5hwujVf6XKdZYSBLtwPhhp8y5qyEcv4bniK8sUU9B2Nt4M` |
| 21:36:58 | `Ei5yGz8d` → `GV2w4YvXeYtEv8LkKFKpFbrqBnvn9HYLesjKgvMyJD5f`, 0,3 SOL, premier SOL du wallet | `5h4EjtBPXWTYfMAJcjaUVpNFaE8J5sfeGzhr44nJZ6R8jgtS2gYsm7dD3cQ7rkudfYCrFzGdUrUVJfViQ5sYtEGY` |
| 21:37:36 | 5 017 919 673,97 BONK vers `GV2w4YvX`, soit exactement l'achat plus le retrait Coinbase ; aucun BONK avant | `5EFJ9CWFdb1G9rTXTwE1CD6TKUC1ccETgq4Sbc9PU6iXgq6eCFc4FeQTbzLbBx9MgepXkMaFcLiVkv8bb4sSFmmS` |
| 13/11 00:27:18 | `GV2w4YvX` vend tout (poussière de 1 001 unités comprise) par trois pools : 859,506691511 SOL brut, 859,506528821 net | `5Z5eChWacMnYHkQE7EWbt6Gg6Vz6h3FGijr1Yn4dvkfzrJCNfSGt6ZHS2hhr2NKAhnsPJVEDJi6eXKqvDFadJG53` |
| 00:40:57 | 859,796535821 SOL → 182 548,799464 USDC. Ce SOL inclut 0,300007 SOL qui ne vient pas de la vente (gaz, poussière) | `4wW64PUDwBtVWtMC3GWK4oJHxn14QiBS5WuZuq3XfZvh4zLRMAWaSvg2SRC5HYLazbSyQLDKJYqBrp7GF51JAoKC` |
| **00:41:12** | **182 548,799464 USDC → `96W8V3toGu55gApT1cNFrZmkcGZwt5YGYotpWaK6fNAm`** | `4nFJRpmP8Keqdnif1wo7hVTwuKUEmQDwVtvwYH4VhUHDkNztXx51Fj4ALgU1YSmdytXJtKtCJPjWGifup4k14yof` |
| 00:45:06 → 00:45:31 | gaz de 0,6 SOL de `ASTyfSima4LLAdDgoFGkgqoKowG1LZFDr9fAQrg7iaJZ` (« MEXC 1 » chez Dune, « MEXC Exchange » chez Orb), puis balayage de 182 348,799464 USDC vers lui. Les 200 USDC restants partent le 18/01/2025, avec 363,021943 USDC d'un second déposant | `3BKdHuaYb8uzFQpAQdVaKXcQrXnopnJBcZ1iEgf1htcFW4xSmL77uhLSbk9QYuP919MDnbRUKTkmbgaWmr3W8FMc`, `BQXGPoQkSYuaA23KJPmybyqDFp5cxiSFzJjP3dxf1gTsk9xAdc1AbnrBZGuxSfa3f9DBQyuboKMpyDLkzRxopmT` |

- **Borne de bout en bout** (`scripts/s16_mexc_chain_bound.py`, fractions exactes, pire cas à chaque étape) :
  - sous H : au moins **100 027,93 USDC** (54,80 %) au prorata, **99 383,28 USDC** (54,44 %) en attribution stricte par pool ;
  - sans hypothèse : 0.
- **`96W8V3to` est une adresse de dépôt MEXC** (SUPPORTED) : deux étiquettes indépendantes, Dune et Orb, plus le schéma « gaz du hot wallet, puis balayage ».
- **Second déposant** : `9obNtb5GyUegcs3a1CbBkLuc5hEWynWfJC6gjz5uWQkE`, 363,021943 USDC le 13/12/2024. Ce wallet a 1 000 transactions pour la seule journée du 06/11/2026 : c'est un service, pas un lien.
- **Empoisonnement** : 3 s après, un sosie `9obNmoF6…` envoie 10 000 lamports au dépôt. À écarter.

## 3. Le relais n'est pas un conduit pur : borne commune et frontière. Niveau : VERIFIED (calcul), hypothèse H : non démontrée

`scripts/s15_relay_bounds.py`, `scripts/s17_joint_destinations.py`, sur les historiques publiés du dossier précédent.

- **Les flux réels du relais**, hors jetons d'empoisonnement :
  - entrées : 334 291,323945 USDC de b947 le 01/10/2024, **100 000 USDC de b298 le 06/10/2024 à 19:28:35** (`0x6407f6bccc370f06128fd95981f5c13475fc3be04922d6213d84d05c97944d8c`) et 0,011 USDC d'un sosie ;
  - sorties : 434 291,334945 USDC, toutes vers b298.
- **Le 06/10** :
  - 19:16:47, le relais envoie 100 000 USDC à b298 ;
  - 19:17:59, b298 envoie 100 000 USDC à `0xbcc66fc7…` ;
  - 19:25:11, b298 reçoit 100 088,752857 USDC de Rizzolver (UniswapX), produit d'une vente ;
  - 19:28:35, b298 renvoie 100 000 USDC au relais.
- **La contradiction de s51** : s51 donne lui-même **0** comme borne basse de la part b947 de ce renvoi, mais compte ensuite toute sortie du relais vers b298 comme 100 % b947. Au pire cas, le relais détient 100 000,011 USDC non marqués, qu'il peut rendre dans n'importe laquelle de ses sorties suivantes.
- **Première version de s51, rejouée** : sa règle (relais = b947) redonne ses 31 bornes. Avec le relais tracé selon la même règle :
  - o1 : au moins **46,814553 USDC** de b947 (sous H : 100 046,825553) ;
  - o2 : au moins **0** (sous H : 99 981,823743) ;
  - les bornes basses sommées passent de 472 143,22 à 137 938,74 USDC (`evidence/s15_s51_corrected.csv`).
  - **s51 est corrigé en conséquence** (dossier précédent, `FINDINGS.md` §10) : ses 31 bornes publiées égalent celles de `s15`, calculées par un second code (assertion dans `s15`), et l'optimum d'un programme linéaire exact (`s52_lp_check.py` du dossier précédent).
- **Borne commune sans hypothèse** : le non-marqué du relais est réparti de toutes les façons possibles entre ses sorties (pas de 1 %), o1 et o2 puisent d'abord dans le non-marqué. Dans toute allocation, **o1 et o2 portent ensemble au moins 100 028,638296 USDC venus de b947**. L'audit EVM trouve le même chiffre par un autre code ; le dossier précédent le démontre directement (`s51_bounds.py`, `joint_min`) et le recoupe par programme linéaire.
  - b947 n'a jamais détenu de DMAGA. Sur les 434 291,32 USDC qu'il envoie, 384 277,99 viennent des exécutions deBridge des makers DMAGA, 50 003,33 de b298 et 10 d'un sosie. En ne marquant que les premiers, la borne commune est d'au moins **50 015,307517 USDC**. Les seuils de nullité ci-dessous (23 492,94 USDC au plus) restent en dessous : les deux bornes ne peuvent pas non plus être nulles ensemble sous ce marquage.
- **Frontière entre les deux destinations** :

| Non-marqué du relais placé dans l'envoi qui paie o2 | Part b947 de o1 / o2 (USDC) | 24 ETH vers Coinbase | Dépôt MEXC (prorata / strict) |
|---|---|---|---|
| 0 % | 46,81 / 99 981,82 | ≥ 0 ETH | ≥ 100 027,93 / 99 383,28 USDC |
| 25 % | 25 046,82 / 74 981,82 | ≥ 1,4572 ETH | ≥ 74 149,58 / 73 627,74 |
| 50 % | 50 046,82 / 49 981,82 | ≥ 8,8877 ETH | ≥ 48 271,23 / 47 872,20 |
| 75 % | 75 046,82 / 24 981,82 | ≥ 16,3181 ETH | ≥ 22 392,88 / 22 176,83 |
| 100 % | 100 046,83 / 0 | ≥ 23,7486 ETH | ≥ 0 |

- **Les deux bornes ne peuvent pas être nulles ensemble** : il faudrait que o1 porte au plus 20 143,92 USDC marqués et o2 au plus 3 349,02, soit au plus 23 492,94 au total. C'est moins que les 100 028,64 garantis (dichotomie, assertion dans `s99_selfcheck.py`).
- **Lecture** : il est démontré, sans hypothèse, que des fonds issus de l'USDC de b947 atteignent le dépôt Coinbase de b298 *ou* le dépôt MEXC Solana, dans les proportions de la table. Laquelle des deux destinations en reçoit le plus n'est pas démontrable sans règle d'allocation.

## 4. `0x2ac17414…` : satellite Base de b298, aller-retour Solana → Base → Solana. Transactions VERIFIED ; même exploitation SUPPORTED

Adresse complète : `0x2ac17414e34c9a1f70f6eadb6230fa503301e878`.
- **09/10/2024 16:27:45** : premier mouvement, 0,1099 ETH de gaz venus de b298 (`0x04c7d2dabb957144a2782c6f5a3a428770928a474c40e2a6a76c15decfc82cbd`).
- **26/11/2024** : deux ordres d'`Ei5yGz8d` vers elle. Le maker est un champ de l'ordre, authentifié par l'orderId recalculé :
  - 0,727671 ETH, `0x15883e9dff356eaff46785a709a7e6c34768b4444dcdb993cb628f56f26bbb88` ;
  - 0,806007 ETH, `0x2545938bcac8ebeda9e5672a4a2c38f8604c9882ceeb224d853165fda668b08d`.
- **Retour 1** :
  - 27/11 18:40:41, 0,16 ETH vers b298 (`0xe7389f5a4d1065d644104a8920ee5978c8022b82b527eb6cb1553dc5c82ddd57`), dont au moins 0,150085454 ETH sont le reste des ordres d'`Ei5yGz8d` ;
  - 8 min plus tard, b298 envoie à `Ei5yGz8d` une tx de valeur 0,21162528 ETH (giveAmount 0,2105 ; `0xfa0e5a1a3355fe4b932e886895bcf9e5c02bc2d9e203aa224182a832afaa10ca`, orderId `0xd186a2daaad4f179414a33236a6cacdcdac7e85cf386472bb0c8b159de7244c8`), dont au moins 0,159342387 ETH sont les 0,16 ETH de `0x2ac17414`.
- **Retour 2** : le 09/12, vente de RUNNER 28 s après une vente de RUNNER de b298 dans le même pool (un indice seulement). Puis 0,1335 ETH vers b298, qui envoie 80 s plus tard 0,1303 ETH vers le dépôt MEXC inféré `0x311ef6b5…` (`0xc52c0f70502f14f38a0cf9970cf186dcab6f3239dced9e804dbe6d438552b483`).
- **Lecture** :
  - le gaz initial et les virements directs soutiennent une même exploitation ;
  - ces bornes ne dépendent pas du relais ;
  - flux net de `0x2ac17414` sur ses mèmes : −1,250000807 ETH.

## 5. Deux wallets de vente de la série du 22/07/2024. VERIFIED ; contrôle commun SUPPORTED

| Wallet | DMAGA reçu | Gaz d'`Ei5yGz8d` | Ventes du 23/07 | Revenu net des ventes | Rendu à `Ei5yGz8d` |
|---|---|---|---|---|---|
| `8kNKNiHKjbCPjaWGjoEEWeQ6X4jkZn2sDV7tz7azfL4t` | 3 000 000 de `HGBiExZRtD2TZdQLWHE9azkTSmE2z7ygKqZMtehJDKYU` | 0,5 SOL | 15 | 146,127827860 SOL | 146,627814060 SOL (`34QyqzQQqn3JN3wgqCBgufeG94D3PSTgigXw6BL72xXnugBgTNLyo1YDLUgXEsP9A2F4z4Z7sTRghiwgvpufApDp`) |
| `BdX9J5pQZ9SoH7PqwDCiiQ2rzaMiT4D9WZ8C1DiwXgyX` | 2 700 000 de `Gcyg2jeLfSY9gxxHf5za5QU74ijtxBb1dB2mdGSPZH3m` | 0,5 SOL | 26 | 141,901983310 SOL | 142,401969710 SOL (`3NT9TkccQmN9DKPPLFgTrMEq6eZQvME3mMusnBAGf8hfS55KYG5mQLvFQn7CE1Frgzo7DiMQVhpZUDVFjsQr6X1H`) |

- Les 289,029783770 SOL rendus se décomposent ainsi : revenu net des ventes 288,029811170, gaz rendu 1,0, poussière 2 600 lamports, moins 30 000 de frais.
- Il ne reste aucun DMAGA, rien n'est parti ailleurs, et le solde final est 0.
- Ce n'est pas un profit : le DMAGA leur a été donné, son coût d'acquisition est celui de `HGBiExZR` et de `Gcyg2jeL`.

## 6. Ce que fait `Ei5yGz8d` des fonds de b298. VERIFIED (correspondances) ; EXPLORATORY au-delà

- **43 exécutions de b298 vers `Ei5yGz8d` sur 43**, retrouvées par l'orderId des logs, au lamport près :
  - 21 depuis Ethereum pour 1 753,731619306 SOL, plus une de 48 960,807840 USDC ;
  - 21 depuis Base pour 206,221862497 SOL.
- **Ordres DLN émis par `Ei5yGz8d`** : 18 réussis, vers b298 (15), b947 (1, le 22/07/2024, 47 023,609816 USDC donnés) et `0x2ac17414` (2). S'y ajoute 1 échec, `3h7aLGGL…`, refait en `2YQXsbx…`. **Aucun tiers.**
- **Virements directs de SOL** (hors comptes propres, commissions de bot et pourboires Jito) : 17 wallets, 146,405754617 SOL.
  - `E72DuqDL` : 95,061118054 SOL en 20 virements, dont 63,44 rendus ;
  - `HGBiExZR` : 21,305620487 ;
  - `76DXe8SQ` : 11,22 ;
  - `2aeEoq5n` : 0,025808220, son premier SOL (§7).
- **DCA du 06/11** : compte `CWNz58zNodfqcgDHoaXYaZJQrt1kr62mwRXUK4YqBDJJ`, vers `Bz4MhmVRQENiCou7ZpJ575wpjNFjBjVBSiVhuNg1pump`. 33,00 SOL déposés, 10,56 exécutés, 22,44 rendus à la clôture (`63kwcJN2caW22Cmd8bEg1wo74KvGcqkejmYsz53vDAFiTpjz1tFUGwx1r2tMggcZdPQowA4BuuSXM8vnpTmXizAk`). Les 14 positions DCA décodées d'`Ei5yGz8d` et de `2aeEoq5n` vérifient toutes : dépôt = exécuté + non exécuté (`evidence/s34_dca_positions.csv`).
- **Aller-retour du 14/11** : 494,130709623 SOL reçus, SLERF acheté puis revendu 488,428 SOL, 490,317 SOL renvoyés à b298 en 26 min. Inchangé, VERIFIED.

## 7. Nouveau : le DCA de 482 SOL du 17/11/2024 aboutit dans un wallet neuf, `2aeEoq5n`. VERIFIED

`scripts/s34_dca_trace.py`, `scripts/jup_dca.py`.

| Heure | Fait | Preuve |
|---|---|---|
| 17/11 01:48:59 | ordre Ethereum de b298, 34,01071452 ETH | `0xdf0b6cf7dbf1f956b9fe2171acdd729ef41f4d1be1ce17e0cd6eb98b38126810`, orderId `0x097aef3d255cc54dcb470578933546871f4cbd828bad6e424cb3b419238c4917` |
| 01:49:15 | +482,634652095 SOL à `Ei5yGz8d` ; solde avant 0,018789476 SOL ; aucune autre entrée avant le DCA | `Z4XmFhZ8bUmqRYDW5T4LHSPH5HK1ULTZVjNckqMoRa6D5sdaCXrEHzDUnWbDBfipCtknZBMy3zPoXci4Vd16J9H` |
| 01:51:56 → 02:30:13 | DCA `G1fC4VgkodbFbsEwV8k8mzb2cMkngfqpiCNMGRZkCwvU` : 482,000000000 SOL → 3 018 194,265441 `FvgqHMfL9yn39V79huDPy3YUNDoYJpuLWng2JfmQpump`, 35 exécutions ; `Ei5yGz8d` n'en détenait pas avant | ouverture `4ZsTdUCfERWjfWgkEdiD24RnYujrc1DsPJjoKax2dGgBNvBphrppYnwJeSdhYt6WeYqaQAqN2gNe5FvKC6PzFjq2`, clôture `JV9unw1Cc11X9tB4Egq4butjHYNar5KhbriMcwsxxuXFLM91tkmbkAuHCvKLaesuLLgQkQjBbhZynUpn9Gq4Z6B` |
| 18/11 18:26:29 | `Ei5yGz8d` → `2aeEoq5n8Cip2raJsiWHBVKuoJL4rid7adepkVYnVzDm`, 0,025808220 SOL, première tx du wallet | `4WfkDUmKQzAvsNA3SAp6rUWiNtW53ecTwvQ3dp6pAf4CteFdoWdrJMipTgt5xgiraGcW1f7E3RvkXdz2e3x57M8S` |
| 18:26:55 (26 s après) | **tout le FvgqHM du DCA**, 3 018 194,265441, vers `2aeEoq5n` | `3ZousK8fdGScWUYDbfNdVWHKQdVhFCczi23tyPwBnAJnD4aA375qS9MrsW9xfNM8Smn9wsrfJ8z8UFruHg9GuyUx` |
| 20/11 23:41:00 | `2aeEoq5n` vend tout en une tx : +393,812873522 SOL nets (397,189388322 en sortie du pool, moins une commission de 3,376109800 SOL, 0,85 %, et 0,000405 de frais) | `sJyecugFxKoMBwaRgEEsDC5W14G7qj399iLueQFNUiG6S9rjShTmmkRjU5RxCahpkxpaBykyhoeyppd9XGcyZfP` |
| 21/11 00:54:40 → 05:12:51 | DCA `fAW4DxfedJY5nmDtiSXJ27j9dT9h1sPS1voqpJApSWv` : 393,000000000 SOL → 3 650 704,976691 `8tSeXYSXzFvaDX1nbWrEFFaFuPHuWqpzksKYxQPvpump`, 250 exécutions | `5vpv7XatzhbYcmis4U8AigGCx3N4BrVhiPtb2tdHY4hAQVNEsqc4Td4yMvgfwjfyrYQqHRreHAirjvbFAvv1JHB1`, `2kNiyhDKuAToAJGan6N1VCc1tmrHU7RWHCh8Y3JQL3LztzqPyhGd94HyxV7ahPNKLvenZF6ivc8xWQdKGmqxLaiw` |
| 22/11 → 04/01/2025 | ventes du 8tSeXY (dont +92,1096 SOL le 22/11, sur une position complétée le même jour par un achat de 17,0 SOL), puis trading de mèmes. Le wallet finit à 0 SOL | `data/sol_2aeEoq5n_txs.csv` |

- **Provenance** :
  - au moins 99,996 % du dépôt DCA vient de l'exécution b298 du 17/11 ;
  - le FvgqHM transféré est exactement la sortie de ce DCA ;
  - les 393,81 SOL de la vente proviennent donc, pour au moins 99,996 %, de l'exécution b298 du 17/11.
  - La part b947 de l'ordre `0xdf0b6cf7` n'est pas bornée : cet ordre donne de l'ETH, et l'historique Ethereum publié n'a pas les frais de gaz nécessaires au modèle par actif (`UNRESOLVED.md` §4).
- **Retours** :
  - 2,876076839 SOL à `Ei5yGz8d` (3 virements) et 2,0 SOL à `E72DuqDL` ;
  - les 0,51238 SOL versés à `25mYnjJ2…` ne sont pas un retour : ce sont 13 commissions d'environ 0,85 % prélevées dans des achats passés par le routeur `6m2CDdhR…` ;
  - une exécution deBridge de b298 vers `2aeEoq5n` le 24/11 (0,2114 ETH → 2,791 SOL), déjà au dossier précédent.
  - Le produit n'est pas reconsolidé : il est réinvesti, puis perdu en grande partie.
- **Le mécanisme se répète** : wallet neuf financé par `Ei5yGz8d` dans la minute, qui reçoit une position entière et la vend.
  - DMAGA, juillet 2024 : `8kNKNiHK`, `BdX9J5pQ`, produit rendu à `Ei5yGz8d` ;
  - BONK, 12/11/2024 : `GV2w4YvX`, produit déposé chez MEXC ;
  - FvgqHM, 18/11/2024 : `2aeEoq5n`, produit réinvesti.
  - Trois cas, trois jetons, trois sorties différentes. Aucun témoin apparié n'a été mesuré (`UNRESOLVED.md` §9).

## 8. Nouveau : `Ei5yGz8d` et `Hp2BtvnZ` créditent la même adresse de dépôt Coinbase. Transferts VERIFIED ; même compte SUPPORTED

| Heure | Fait | Preuve |
|---|---|---|
| 08/04/2024 18:46:03 | `Ei5yGz8d` → `39dTXaMMMy4AV6jhihEmfqdnAkhpwCpYpz9SnvP3y1h7`, 1,55 SOL, première tx de cette adresse | `2mzsArJC1DeWX7kwF7ypjy6WFSG4Dhwf2DzpFZr757JWvFnc9GNgGWJ25usjs2JUyB6TGhdth4PXmAB4SxNtvELF` |
| 18:47:39 (96 s) | `39dTXaMM`, signataire, balaie 1,549845 SOL vers `H8sMJSCQxfKiFTCfDR3DUMLPwcRbM61LGFJ8N4dK3WjS` (« Coinbase 1 », Dune) | `2y9Uzyc7NYrmZ6cq6zUWhQ9hFuwCsCgK7yx6ixh45WgDrjXynLP5Uey3kNaaewuhPsxUAMadx1NwkZ5TwperpTTn` |
| 07/05/2024 05:31:14 | retrait Coinbase (`GJRs4FwH…`, « Coinbase 3 ») de 7,183192683 SOL vers `Hp2BtvnZvw7YxbQvSehqb1LC5jBSX1aLApzHQnDVwf3q` | `29oeYYe62jgTDLTnWv6rQoE1uUDPCXgv85fKV3kit284Sz3cGt9B5PsYMr1axja3Pond3P8pt4BNXAHm9F2UwFX4` |
| 19:30:26 | `Hp2BtvnZ` → `39dTXaMM`, 3,27 SOL | `2bBTieYuFzmH45sNp8fjDYNM2MADoUxZLAoVtX7h9pQEXQT9JW6cKXi6ZeuzBCuNAcYWzzXpYt3odhxfVnXfcWTv` |
| 19:32:13 (107 s) | `39dTXaMM` balaie 3,269845 SOL vers `GJRs4FwH…` (« Coinbase 3 ») | `5iKFupiSMe4mj41RttkaPyovmbHbaTXofFjoKKTgXimRHCtX9TRwPeRV4rkNU1qdPEGQiAps5X1dvaQ4evdb8v5v` |
| 13/05/2024 03:23:09 | `Hp2BtvnZ` → `Ei5yGz8d`, 1,013173483 SOL | `3xZbhgX6rsJPdsJGQkUAvsmdnJ4NuGGNrAiUnvJn1cdRfxeKiZYD1sep2XiehfxRXDwTqfLubhdB` |

- **`39dTXaMM` est une adresse de dépôt Coinbase inférée** :
  - deux entrées seulement, chacune balayée en 96 à 107 s par l'adresse elle-même, avec les mêmes frais fixes (155 000 lamports), vers deux portefeuilles étiquetés Coinbase par le spellbook Dune (`evidence/labels/dune_cex_solana_addresses.sql` du dépôt) ;
  - solde ramené à 0 à chaque fois.
- **Une adresse de dépôt est attribuée à un seul compte client.** Deux déposants qui s'en servent créditent donc le même compte Coinbase. Seule exception : on peut payer quelqu'un sur son adresse de dépôt.
  - Ici, `Hp2BtvnZ` paie aussi `Ei5yGz8d` directement six jours plus tard.
  - Deux signaux indépendants, donc **SUPPORTED** : `Ei5yGz8d` et `Hp2BtvnZ` relèvent d'un même compte Coinbase et, probablement, d'une même exploitation.
- **`Hp2BtvnZ`** n'a que 17 tx :
  - un retrait Coinbase de 7,18 SOL ;
  - 7,0 SOL envoyés à `5yYnURUvXvqvt445QNk548ddofunNabeUujVhRAucjkp`, qui n'est financé que par lui, trade des mèmes par Photon et lui rend 4,9 SOL ;
  - le premier SOL de `CAX7f8ET5MC6BiU3Kxz86pvsoayUEuPX5xjpdXeQezSf` (0,8 SOL).
- **Ce que cela n'établit pas** :
  - aucune identité ;
  - aucun lien avec le dépôt Coinbase Base de b298 (`0x34172888`) : deux adresses de dépôt sur deux chaînes ne se relient pas sur la chaîne ;
  - montants faibles et antérieurs à DMAGA (avril-mai 2024).
- **Pistes testées et écartées** :
  - `AVUCZyuT35YSuj4RH7fwiyPu82Djn2Hfg7y2ND2XcnZH` reçoit de `5yYnURUv` et d'`E72DuqDL` dans des tx Photon. C'est un service à très fort volume, 1 000 tx en deux heures le 06/11/2026, compatible avec des frais Photon : pas un lien ;
  - `8rNJ1v4L…` vend le jeton `6h3MaAaQ…` contre du SOL à de nombreux acheteurs (134 tx), dont `HGBiExZR` et `CAX7f8ET` le 01/08/2024 : vendeur partagé, pas un lien ;
  - `9yj3zvLS…` est un coffre de pool.

## 9. Positions de mèmes de b298 sur Base. Calcul VERIFIED ; parts b947 sous H seulement

`scripts/s60_positions.py`, `evidence/s60_b298_base_positions.csv` et `evidence/s60_b298_base_out_bounds.csv`. Le modèle propage une borne basse à travers chaque échange, jeton par jeton ; l'ancien modèle comptait tout produit de vente comme non marqué.

| Sortie | Montant | Sous H, modèle par actif | Sous H, ancien modèle | Sans hypothèse |
|---|---|---|---|---|
| 12/11 08:57:51, dépôt Coinbase | 24 ETH | ≥ 23,748588117 ETH | 23,748588577 (frais compris) | 0 (frontière §3) |
| 06/11 21:20:53, ordre vers `Ei5yGz8d` | 6 424,431066 USDC | ≥ 6 378,333207 | identique | 0 |
| 08/11 06:21:51, ordre vers b298 (Ethereum) | 0,6026 ETH | ≥ 0,576743 | 0 | 0 |
| 18/11 07:37:39, ordre vers `Ei5yGz8d` | 2,5418 ETH | ≥ 0,750533 | 0 | 0 |
| 22/11 00:03:15, ordre vers `Ei5yGz8d` (vente de CLARK) | 0,3517 ETH | ≥ 0,334273 | 0 | 0 |
| 27/11 07:28:31, ordre vers le dépôt BloFin inféré `0xb1e5042f759dc67a2eed103cd4425a73b44e678e` | 7,0055 ETH | **≥ 1,154082** | 0 | 0 |
| 27/11 → 09/12, 6 ordres vers le dépôt MEXC Ethereum `0x311ef6b5…` | 10,54 ETH | 0 | 0 | 0 |

- **Positions** depuis le 01/10/2024, flux nets d'ETH sur les échanges, positions restantes non valorisées (ce ne sont pas des profits) :
  - HIGHER : 6,19 ETH dépensés, 11,50 reçus ;
  - BOOMER : 8,55 dépensés, 10,55 reçus ;
  - SYNDOG : 0,64 dépensés, 3,68 reçus ;
  - RUNNER : 1,18 dépensés, 0,39 reçus ;
  - CLARK : 4,67 dépensés, 0,34 reçus ;
  - CJ : 3,57 dépensés, 3,17 reçus.
- **Les ordres vers le dépôt MEXC Ethereum restent non bornés** : les positions HIGHER et BOOMER mêlent un stock ancien, non marqué, à l'ETH marqué.
- **Nature du dépôt BloFin** (SUPPORTED) :
  - 4 cycles sur 4 : gaz de `0x2703983059c7b60515B4faB6fB8b301F7781f5C6`, puis balayage complet vers `0x1cA5aa5b1dd8D948bB0971A5fB1762FE172E0040` ;
  - « BloFin » est une étiquette Blockscout sans source attribuée ;
  - la même adresse reçoit 996, 4 996 et 1 996 USDT de « MEXC 21 » (`0x9642b23Ed1E01Df1092B92641051881a322F5D4E`, étiquette OLI).

## 10. BSC, autres pistes, hypothèses

- **BSC** : dans la fenêtre DMAGA, seuls les blocs 43950886 et 43951101 du §2 changent l'état de b298, confirmé sur l'état archive. Les contreparties de 2021-2022 restent non étiquetées et sans lien daté (`UNRESOLVED.md` §3).
- **Écartés** :
  - `5tzFkiKscXHK5ZXCGbXZxdw7gTjjD1mBwuoFbhUvuAi9`, Binance chez Dune et chez Orb : pas un lien ;
  - aucun lien avec le réseau WOLF ;
  - b298 ne crée aucun jeton sur Base ;
  - `Ei5yGz8d` a créé un seul jeton pump.fun, `J6D4E67QLHxY85cLcdaJRQ9z9M7wrihvgfnyqK9ZXZE`, le 13/05/2024, revendu 33 min plus tard pour 0,049 SOL.

| Hypothèse | Statut | Pourquoi |
|---|---|---|
| Des fonds issus de l'USDC de b947 atteignent le dépôt Coinbase Base de b298 ou le dépôt MEXC Solana | **VERIFIED** (borne commune et frontière, §3) | Sans hypothèse d'allocation. La répartition entre les deux reste indéterminée |
| Les deux à la fois, à hauteur de 23,75 ETH et de 100 028 USDC | **Seulement sous H** | H non démontrée (§3) |
| `0x2ac17414` est opéré avec b298 | SUPPORTED (fort) | Gaz de b298, virements directs, retours réexpédiés en 8 et 1 min |
| `8kNKNiHK`, `BdX9J5pQ`, `GV2w4YvX` et `2aeEoq5n` sont des wallets temporaires d'`Ei5yGz8d` | SUPPORTED | Premier SOL d'`Ei5yGz8d` dans la minute, position entière reçue puis vendue (§5, §7) |
| `Hp2BtvnZ` et `Ei5yGz8d` relèvent d'un même compte Coinbase | SUPPORTED | Même adresse de dépôt et virement direct (§8) |
| Le BONK retiré de Coinbase le 12/11 vient des 24 ETH déposés chez Coinbase à 08:57 | EXPLORATORY | Même exchange, même jour, valeur comparable ; Coinbase est une boîte noire |
| Les dépôts MEXC Solana `96W8V3to` et Ethereum `0x311ef6b5` sont le même compte | UNRESOLVED | Même exchange seulement |
