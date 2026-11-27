# Relations financières établies ou corrigées (06/11/2026, version auditée)

Détails, hashes et bornes : `FINDINGS.md`.
- **H** : hypothèse « le relais ne transporte que des fonds de b947 », non démontrée (`FINDINGS.md` §3).
- Les liens entre chaînes de `CROSSCHAIN_LINKS.csv` (88 ordres) sont authentifiés par l'orderId recalculé. Ce sont les 88 liens construits par `s52_links.py` : ordres entre Base et Ethereum, ordres d'Ethereum et de Base vers `Ei5yGz8d`, aller-retour BSC. Les 11 autres ordres exécutés de b298 et b947, dont les 9 d'`Ei5yGz8d` vers Ethereum, sont au dossier précédent (`dln_orders_evm.csv`).

| # | Relation | Montant | Date (UTC) | Preuve clé | Niveau |
|---|---|---|---|---|---|
| N1 | b298 (Base) → dépôt Coinbase inféré `0x34172888e808debea84bb224bbfa8dcd6d78de7d` → Coinbase 14 | 24,0 ETH ; part b947 ≥ 23,748588117 ETH **sous H**, 0 sans hypothèse | 2024-11-12 08:57:51 | `0x52da33cb31aa36ecce1a05774dd7bc69bed8d0a9b555db97e8659771a4a00245` | trajet VERIFIED ; dépôt SUPPORTED |
| N2 | b298 → BSC → b298 (Ethereum) → `Ei5yGz8d` → BONK → `GV2w4YvX` → dépôt MEXC `96W8V3to` | 182 548,799464 USDC ; part b947 ≥ 100 027,93 (prorata) ou 99 383,28 (strict) **sous H**, 0 sans hypothèse | 2024-11-12 17:42:47 → 2024-11-13 00:45:31 | orderId `0xc62af9cf…51d2`, `0x5c2e547f…285e`, `0x80158194…ffa7` | trajet VERIFIED ; dépôt SUPPORTED |
| N1+N2 | **Borne commune** : les ordres o1 (vers Base) et o2 (vers BSC) portent ensemble au moins 100 028,638296 USDC venus de b947 (50 015,307517 en ne marquant que les exécutions deBridge reçues par b947) ; les bornes de N1 et N2 ne peuvent être nulles ensemble | voir la frontière | 2024-11-12 | `scripts/s15_relay_bounds.py`, `scripts/s17_joint_destinations.py` | **VERIFIED, sans hypothèse** |
| N3 | `Ei5yGz8d` finance `GV2w4YvX` (0,3 SOL, premier SOL) puis lui transfère 5 017 919 673,97 BONK | | 2024-11-12 21:36:58, 21:37:36 | `5h4EjtBP…`, `5EFJ9CWF…` | VERIFIED |
| N4 | `GJRs4FwH…` (Coinbase, Dune et Orb) → `Ei5yGz8d`, BONK fondu dans N3 | 2 252 204 192,14 BONK | 2024-11-12 21:34:51 | `29E3ro5i…` | VERIFIED ; lien avec N1 EXPLORATORY |
| N5 | b298 → `0x2ac17414` (gaz) ; `Ei5yGz8d` → `0x2ac17414` (2 ordres) ; `0x2ac17414` → b298 → `Ei5yGz8d` ou dépôt MEXC Ethereum | 0,1099 ; 1,534 ; 0,16 et 0,1335 ETH | 2024-10-09 → 2024-12-09 | `0x04c7d2da…`, `0xe7389f5a…` | VERIFIED ; même exploitation SUPPORTED |
| N6 | `HGBiExZR` → `8kNKNiHK` (3 M DMAGA), gaz d'`Ei5yGz8d`, ventes, 146,627814060 SOL rendus (revenu net 146,127827860) | | 2024-07-22 → 07-23 | `34QyqzQQ…` | VERIFIED |
| N7 | `Gcyg2jeL` → `BdX9J5pQ` (2,7 M DMAGA), gaz, ventes, 142,401969710 SOL rendus (revenu net 141,901983310) | | 2024-07-22 → 07-23 | `3NT9Tkcc…` | VERIFIED |
| N8 | b298 (Base) → dépôt BloFin inféré `0xb1e5042f759dc67a2eed103cd4425a73b44e678e` | 23 882,887021 USDT ; part b947 ≥ 1,154082 ETH des 7,0055 ETH **sous H**, 0 sans hypothèse | 2024-11-27 07:28:31 | orderId `0x09a61c84…75b5` | trajet VERIFIED ; dépôt SUPPORTED |
| N9 | 21 ordres de b298 depuis Base vers `Ei5yGz8d`, retrouvés sur Solana au lamport près | 206,221862497 SOL | 2024-10-16 → 11-27 | `evidence/s33_sol_dln_Ei5yGz8d.csv` | VERIFIED |
| N10 | Ethereum → BSC → Ethereum en 11 min (12/11) | 99 989,83 USDC → 29,845 ETH | 2024-11-12 | orderId `0xc62af9cf…`, `0x5c2e547f…` | VERIFIED |
| **N11** | **`Ei5yGz8d` et `Hp2BtvnZvw7YxbQvSehqb1LC5jBSX1aLApzHQnDVwf3q` déposent sur la même adresse de dépôt Coinbase inférée `39dTXaMMMy4AV6jhihEmfqdnAkhpwCpYpz9SnvP3y1h7`, et `Hp2BtvnZ` paie `Ei5yGz8d` directement** | 1,55 et 3,27 SOL ; 1,013173483 SOL | 2024-04-08, 2024-05-07, 2024-05-13 | `2mzsArJC…`, `2bBTieYu…`, `3xZbhgX6…` | transferts VERIFIED ; même compte Coinbase SUPPORTED |
| **N12** | **b298 → `Ei5yGz8d` (482,63 SOL) → DCA Jupiter `G1fC4Vgk…` → 3 018 194,265441 FvgqHM → wallet neuf `2aeEoq5n` (premier SOL d'`Ei5yGz8d` 26 s avant) → vente** | 482 SOL → 393,812873522 SOL nets | 2024-11-17 → 2024-11-20 | `Z4XmFhZ8…`, `4ZsTdUCf…`, `3ZousK8f…`, `sJyecugF…` | VERIFIED ; part b947 non bornée |
| **N13** | 88e lien deBridge : ordre Ethereum `0x3554eb6d…` de b298 → b298 sur Base, exécuté par le solver tiers `0xef1ec136…` | 11 996,910295 → 11 990,401920 USDC | 2024-08-06 18:57:27 | fill `0xb2ea0181c3dda0d1cf08bcd4675389e166fdfdad5b4125918c0ec616bdb15ab1`, orderId `0x1596c70d…` | VERIFIED |

## Ce que ces relations établissent
- **Sans hypothèse d'allocation** : des fonds issus de l'USDC de b947 atteignent le compte Coinbase de b298 sur Base *ou* un compte MEXC par Solana, au minimum dans les proportions de la frontière (`FINDINGS.md` §3).
- **Sous H** : les deux à la fois, ainsi que BloFin et plusieurs retours vers `Ei5yGz8d`.
- **Un même schéma**, répété sur trois jetons (DMAGA, BONK, FvgqHM) : `Ei5yGz8d` alimente un wallet neuf qui reçoit une position entière et la vend.
- **`Ei5yGz8d` utilise un compte Coinbase**, partagé avec `Hp2BtvnZ` (N11).

## Ce qu'elles n'établissent pas
- Aucune identité.
- Pas que les comptes Coinbase, MEXC ou BloFin des différentes chaînes soient les mêmes : il faudrait une réquisition.
- Pas que l'ETH de N1 et le BONK de N4 soient les mêmes fonds.
- Aucun lien avec le réseau WOLF.
