# Journal des agents : dmaga-debridge-next-trace

## 2026-11-06 | Claude Code (Opus 5.5) | Traçage Base, BSC et retour Solana des fonds de b298
- **Actions** :
  - historique Base complet de b298, `0x2ac17414…` et `0x34172888…` (Blockscout Base lu depuis Chrome, onglet local) ;
  - soldes contrôlés sur l'état archive ;
  - 63 événements DLN décodés sur Base ;
  - dichotomie d'état de b298 sur BSC (108 changements) ;
  - historiques Solana complets d'`Ei5yGz8d` et de 8 wallets (Helius) ;
  - rapprochement des exécutions par orderId ;
  - bornes sans FIFO ;
  - livrables CSV et Markdown ;
  - autocontrôle hors ligne.
- **Résultats** :
  - VÉRIFIÉ, 24 ETH de b298 vers le dépôt Coinbase inféré `0x34172888…` le 12/11/2024 (au moins 23,7486 ETH issus de b947).
  - VÉRIFIÉ, circuit Ethereum → BSC → Ethereum → Solana → BONK → `GV2w4YvX…` → dépôt MEXC `96W8V3to…` : 182 548,80 USDC, dont au moins 100 067,30 USDC issus de b947.
  - VÉRIFIÉ, boucle `Ei5yGz8d` → `0x2ac17414` → b298 → `Ei5yGz8d`.
  - VÉRIFIÉ, `8kNKNiHK…` et `BdX9J5pQ…` rendent 289,03 SOL à `Ei5yGz8d`.
  - VÉRIFIÉ, 87 liens DLN par orderId.
  - VÉRIFIÉ, `5tzFkiKs…` = Binance Hot Wallet 2 (pas un lien) et aucun lien WOLF.
- **Sources** : `FINDINGS.md`, `NEW_CONNECTIONS.md`, `CROSSCHAIN_LINKS.csv`, `scripts/s99_selfcheck.py` (26 assertions).
- **Limites** :
  - BSC : 108 blocs sur 108 détaillés (95 tx signées sur 95) ; contreparties de 2021-2022 non étiquetées ;
  - part d'origine b947 non bornée après certains mèmes ;
  - Jupiter DCA non suivis ;
  - étiquettes d'exchange à source unique (Orb, Blockscout) ;
  - pas d'audit à l'aveugle.
  - Une requête SQD avec un en-tête modifié a été refusée par le contrôle des permissions, et ce refus n'a pas été contourné.
- **Suite** : `NEXT_STEPS.md`.

## 2026-11-06 | Claude Code (Opus 5.5) | Audit contradictoire, migration dans Dark-MAGA, nouvelles connexions
- **Actions** :
  - audits indépendants Solana et EVM depuis les données brutes ;
  - recalcul local de l'orderId DLN (keccak256, validé contre OpenSSL) ;
  - modèle de bornes par actif sur Base ;
  - relais tracé et borne commune ;
  - chaîne MEXC en fractions exactes ;
  - décodeur Jupiter DCA ;
  - historiques Solana de 9 wallets de plus ;
  - lectures d'état archive Ethereum et BSC mises en cache ;
  - fixtures et tests hors ligne ;
  - `nt_lib.py` sans chemin de machine.
- **Résultats** :
  - VÉRIFIÉ : o1 et o2 du 12/11/2024 portent ensemble au moins 100 028,638296 USDC de b947, et les bornes Coinbase et MEXC ne peuvent être nulles ensemble ;
  - les bornes individuelles du dépôt privé (23,7486 ETH, 100 067,30 USDC) ne valent que sous l'hypothèse H (relais = b947), non démontrée ;
  - VÉRIFIÉ : 88 liens DLN, et non 87 ;
  - VÉRIFIÉ : DCA de 482 SOL → FvgqHM → `2aeEoq5n` → 393,81 SOL ;
  - SUPPORTED : `Ei5yGz8d` et `Hp2BtvnZ` créditent la même adresse de dépôt Coinbase `39dTXaMM`.
- **Sources** : `FINDINGS.md`, `AUDIT.md`, `scripts/s99_selfcheck.py` (31 assertions), `tests/` (12 tests).
- **Limites** :
  - part b947 de l'ETH sur Ethereum non bornée (pas de frais de gaz dans l'historique publié) ;
  - pas de témoins pour le schéma des wallets neufs ;
  - pas d'audit des conclusions après correction.
- **Suite** : `REPRISE.md`.

## 2026-11-06 | Claude Code (Opus 5.5) | Corrections après la fusion des PR #15 et #16
- **Actions** :
  - constat : PR #15 et #16 fusionnées dans `main` à 07:43 et 07:47 UTC, après six commits de documentation qui qualifiaient les bornes de s51 « sous H » sans corriger le code ;
  - dossier précédent : `s51_bounds.py` trace le relais et démontre la borne commune (`joint_min`) ; `dln.py` décode la v2 de `FulfilledOrder` ; `dln_orders_evm.csv` régénéré hors ligne ; recoupement par programme linéaire exact (`s52_lp_check.py`) ; autocontrôle F8 et F9, chacun vérifié en échec sur l'ancienne version ;
  - ce dossier : valeurs sous H recalculées par `s15` au lieu d'être lues dans s51 ; `s60`, `s51_build.py` et `s17` adaptés ; `s12` passe par le décodeur commun ; formulations corrigées ;
  - revue indépendante par un agent tiers (Solana §5 à §7, 88 liens), depuis les historiques bruts, sans réseau.
- **Résultats** :
  - VÉRIFIÉ : o1 ≥ 46,814553 et o2 ≥ 0 seuls ; o1 + o2 ≥ 100 028,638296 USDC venus de b947 ; ≥ 50 015,307517 si l'on ne marque que les exécutions deBridge reçues par b947. Mêmes chiffres par la démonstration de s51, par s15 et par le programme linéaire ;
  - VÉRIFIÉ : 74 exécutions v2 de 2026 vers 2d86 ajoutées, aucune ligne existante changée (rejeu d'abord identique à l'octet près avec l'ancien décodeur) ;
  - VÉRIFIÉ : frontière et seuils de nullité de `s17` identiques avec les autres exécutions Base sous H ou sans hypothèse ;
  - VÉRIFIÉ par la revue : DCA de 482 SOL → `2aeEoq5n` → vente de 393,812873522 SOL nets ; 88 liens, 88 orderId distincts, tous exécutés ;
  - corrigé : vente nette (brut 397,189388322) ; 0,51238 SOL vers `25mYnjJ2` = commissions, pas un retour ; périmètre des 88 liens ; `UNRESOLVED.md` §4 contredisait le §2 (ordre `0x2fa91216` borné sous H).
- **Sources** : `AUDIT.md` §7, `FINDINGS.md` §0 et §3, `../2026-11-05_evm-recipient-deeptrace/FINDINGS.md` §6 et §10.
- **Limites** : le programme linéaire demande scipy et ne tourne pas en CI ; seules les sections §5 à §7 et les 88 liens ont été relues par un tiers ; 148 horodatages et un reçu lus sur le RPC public pendant le rejeu.
- **Suite** : PR de correction vers `main`, sans fusion automatique. Décision de Benjamin.

