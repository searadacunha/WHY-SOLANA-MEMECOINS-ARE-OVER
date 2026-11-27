# Audit contradictoire du dossier (06/11/2026)

Le dépôt privé `dmaga-debridge-next-trace` (commits `009157e`, `cd00015`) n'avait jamais été audité. Avant sa migration, trois lectures indépendantes l'ont été :
- **Audit Solana** : recalcul depuis les transactions brutes, avec son propre code, sans utiliser les CSV ni les scripts de l'auteur, puis comparaison finale avec eux.
- **Audit EVM** : même règle, pour Ethereum, Base et BSC, avec des lectures d'état archive ajoutées.
- **Revue de migration** : code, chemins, recalcul des orderId, modèle par actif, contrôle de chaque correction des deux audits par un second code (`s15`, `s16`, `s34`).

Chaque correction ci-dessous est rejouée par `scripts/s99_selfcheck.py` ou `tests/test_offline.py`.

## 1. Corrections de chiffres
| # | Point | Dépôt privé | Après audit | Rejoué par |
|---|---|---|---|---|
| A1 | Part b947 des ordres du 12/11 | relais compté 100 % b947 (s51) | relais tracé : o1 ≥ 46,814553, o2 ≥ 0 ; ensemble ≥ 100 028,638296 USDC | `s15_relay_bounds.py` |
| A2 | Borne MEXC | 100 067,30 USDC (54,82 %), « borne certaine » | sous H : 100 027,93 (prorata) ou 99 383,28 (strict) ; sans hypothèse : 0. Sont corrigés le facteur de conversion (0,300007 SOL non issus de la vente), la part BONK (prorata, pas exacte ; trois pools) et le pire cas à chaque étape au lieu du produit de parts | `s16_mexc_chain_bound.py` |
| A3 | Borne Coinbase | 23,7486 ETH | sous H : 23,748588117 ETH (l'ancienne valeur portait sur la valeur et les frais) ; sans hypothèse : 0 ; frontière avec MEXC | `s60_positions.py`, `s17_joint_destinations.py` |
| A4 | Soldes Ethereum de b298 | relevés à la main par curl, non mis en cache | lectures d'état archive en cache, publiées en fixtures (écarts −4, −3 272, +5 wei) | `s16` |
| A5 | Liens deBridge | 87 | 88 : l'ordre `0x1596c70d…`, exécuté par un solver tiers, échappait au filtre de `s12`. Périmètre : les liens construits par `s52`, pas tous les ordres de ces wallets (`FINDINGS.md` §0) | `s12`, `s13` |
| A6 | Ordres DLN d'`Ei5yGz8d` | 19 + 1 échec | 18 + 1 échec | `SOLANA_RETURN_FLOWS.csv` (échec marqué) |
| A7 | Virements directs d'`Ei5yGz8d` | `E72DuqDL` 94,96 SOL en 18 | 95,061118054 SOL en 20 ; 17 wallets, 146,405754617 SOL, hors commissions de bot dans les échanges | `s53` (seuil 0,01 SOL, transferts hors échange) |
| A8 | Retours des wallets de vente | « 289,03 SOL produit des ventes » | revenu net 288,029811170 SOL, plus 1,0 SOL de gaz rendu | audit Solana |
| A9 | DCA du 06/11 | « 34,00 SOL → DCA » | 33,00 déposés, 10,56 exécutés, 22,44 rendus | `jup_dca.py`, `s34` |
| A10 | HIGHER | `0xbf0533…` | `0x0578d8a44db98b23bf096a382e016e29a5ce0ffe` | grand livre Base |
| A11 | Coinbase 31 et 42 | « hot wallets » | étiquette Blockscout « Exchange » | audit EVM |
| A12 | Ordre du 27/11 18:48 | 0,2105 ETH | giveAmount 0,2105 ; valeur de la tx 0,21162528 ETH | audit EVM |

## 2. Échecs silencieux trouvés dans le code
1. **`dln.py` (PR #15) ignore la seconde version de `FulfilledOrder` (`0xc164aca3`)** :
   - 78 exécutions de 2026, presque toutes vers `0x2d86…`, manquent à `dln_orders_evm.csv` de la PR #15, qui s'arrête au 24/01/2026 pour `0x2d86` ;
   - sans effet sur le périmètre de ce dossier (2024) ;
   - corrigé dans `dln.py` le 06/11 (§7) ; `s12` et `s21` passent par son décodeur.
2. **Filtre de `s12`** : seuls deux solvers étaient reconnus. Toute entrée d'USDC, de WETH ou d'ETH interne dans une tx non signée par le wallet est maintenant décodée (16 reçus de plus, 1 ordre retrouvé).
3. **`s51` (PR #15)** : le relais est compté comme un conduit pur, alors que la règle donne 0 à l'argent que b298 lui renvoie (A1). Corrigé le 06/11 (§7).
4. **`s53`** : un seuil de 0,1 SOL omettait les premiers virements de financement (A7).
5. **`s99`** : soldes en dur, flottants et facteurs multipliés (A2, A4).
6. **Récepteur local de collecte (`recv_server.py`)** : il acceptait les écritures de n'importe quelle origine web. Il n'accepte plus que la page qu'il sert, et ne relaie que des messages venus de `*.blockscout.com`.
7. **Chemins** : `nt_lib.py` dépendait de chemins absolus de la machine de collecte et d'un projet non publié. Il part désormais de son propre emplacement, lit les extraits publiés et des caches en lecture seule optionnels (`DMAGA_NT_RAW_RO`). Un test vérifie qu'aucun script ne contient de chemin de machine.

## 3. Contrôles qui tiennent
- **Complétude** :
  - 18 historiques Solana sans doublon ni rupture de solde, SOL et comptes de jetons ;
  - b298 sur Base : 897 tx signées, nonces sans trou, soldes ETH et USDC égaux à l'état archive sur 46 points ;
  - BSC : fenêtre DMAGA confirmée sur l'état archive.
- **Liens** : 550 événements DLN dans 947 reçus bruts, 550 orderId recalculés à l'identique ; 88 liens confirmés, maker, receveur et montant compris. Rejoué le 06/11 sur 948 reçus : mêmes 550 événements.
- **Empoisonnement** :
  - aucun sosie aux 4 premiers et 4 derniers caractères identiques parmi les contreparties des constats ;
  - les sosies partiels n'envoient que de la poussière ;
  - quatre faux jetons sont isolés sur Base.
- **Services** : les étiquettes ne servent jamais de lien. Le second déposant de `96W8V3to`, `AVUCZyuT`, `8rNJ1v4L` et les exécutants Jupiter sont des services ou des contreparties partagées.

## 4. Outils évalués
| Outil | Licence, état | Usage ici | Décision |
|---|---|---|---|
| `debridge-finance/dln-contracts` (`DlnOrderLib.sol`, commit `d54e94f`) | BUSL-1.1, dernier commit 06/2024 | format de l'orderId | format réimplémenté (`dln_orderid.py`), aucun code copié. Keccak-256 validé contre OpenSSL 3.6 sur 421 longueurs |
| `sevenlabs-hq/carbon`, `jupiter-dca-decoder` (commit `bebd108`) | MIT, maintenu (11/2026), généré par Codama depuis l'IDL | structures et discriminants des événements DCA | discriminants vérifiés (`jup_dca.py`), code non copié |
| `helius-labs/helius-sdk`, `shottah/tracer` | MIT ; MIT ou Apache-2.0 | | référence seulement (audit d'outils du 06/11, dépôt Polymarket) : le SDK n'ajoute rien à l'appel JSON-RPC direct ; tracer exige `debug_traceTransaction` |
| `debridge-finance/solana-tx-parser-public` | | | non retenu : les logs « Order Id » et le décodage par orderId suffisent |

## 5. Sources des extraits publiés
- `evidence/debridge_api_receivers_extract.csv` : 101 lignes sur 638 de `deBridge-Memecoin-Funding-Investigation/data/derived/s11_dmaga_receivers.csv`, sha256 `773477808f1e37d9b95f68d04dafb770e81daf29d59eda3b47574350cec80c00`.
- `evidence/debridge_api_orders_extract.csv` : 22 lignes sur 76 de `s01_orders_api.csv`, sha256 `506009d417e4ef10c0c474b79e66704141725f30be96919c98b45142eb42b3f9`.
- Lignes retenues : celles dont le maker, le receveur ou l'adresse demandée est b298, b947, le relais, `Ei5yGz8d` ou `0x2ac17414`. `s51_build.py`, `s52_links.py`, `s53_solana_flows.py` et `s54_bsc_flows.py` redonnent, avec ces extraits, des CSV identiques octet pour octet à ceux du dépôt privé. Les corrections A5 à A7 ont été appliquées ensuite.

## 6. Ce qui n'a pas été audité
- Les conclusions rédigées ont été relues le 06/11 par une revue indépendante limitée aux §5 à §7 et aux 88 liens (§7 ci-dessous). Le reste n'a pas été relu par un agent tiers.
- Les pages Orb ne sont pas archivées.
- Les contreparties BSC de 2021-2022.

## 7. Corrections du 06/11/2026, après la fusion des PR #15 et #16
- **Dossier précédent** (`../2026-11-05_evm-recipient-deeptrace/`, `FINDINGS.md` §10) :
  - `s51_bounds.py` trace le relais ; ses 31 bornes égalent celles de `s15` et l'optimum d'un programme linéaire exact. Il démontre aussi la borne commune de o1 et o2 ;
  - `dln.py` décode la v2 de `FulfilledOrder` : tête de cinq mots, `uint256` avant `sender`. 74 exécutions de 2026 vers 2d86 ajoutées à `dln_orders_evm.csv`, aucune ligne changée. Les 4 autres événements v2 du cache vont à des receveurs hors périmètre.
- **Ce dossier** :
  - les valeurs sous H ne sont plus lues dans le CSV de `s51`, qui trace désormais le relais. `s15` les recalcule avec la règle H (`from_b947_min_under_H`) et vérifie que `s51` corrigé égale son propre calcul. `s60` et `s51_build.py` les lisent là ;
  - `s15_s51_corrected.csv`, `s15_relay_bounds.csv` et `s15_joint_bound.json` ne changent que par le nom des colonnes et des clés (`under_H`). `BASE_FLOWS.csv` ne change que par son libellé `marker`, qui dit désormais « sous H ». `s16`, `s17` et `s60` redonnent des sorties identiques à l'octet près ;
  - `s12` passait les événements v2 au décodeur v1, qui lit alors le montant à la place de `sender`. Il passe maintenant par `dln.fills_in_receipt`. Aucune sortie publiée ne contenait d'événement v2.
- **Revue indépendante** (06/11, recalcul depuis les historiques bruts, sans réseau) :
  - DCA de 482 SOL, transfert vers `2aeEoq5n`, vente, wallets de vente du §5, 43 exécutions du §6 : chiffres confirmés ;
  - 88 liens : 88 orderId distincts, aucun doublon de transaction, et chacun a une exécution réussie côté destination ;
  - formulations corrigées : vente de 393,81 SOL nets (brut 397,189388322) ; les 0,51238 SOL vers `25mYnjJ2` sont des commissions, pas un retour ; provenance « au moins 99,996 % » ; périmètre des 88 liens ; ordre ETH `0x2fa91216` borné sous H (`UNRESOLVED.md` §4).

