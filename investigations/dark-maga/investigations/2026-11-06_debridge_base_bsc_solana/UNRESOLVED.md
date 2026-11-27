# Ce qui reste ouvert (06/11/2026, version auditée)

Pour chaque point : ce qui manque, pourquoi, et ce qui le fermerait. Rien ici n'est une conclusion.

## 1. Le relais : hypothèse H
- **Ce qui manque** : une raison, autre qu'une convention, de dire que les 100 000 USDC renvoyés par b298 au relais le 06/10/2024 à 19:28:35 sont des fonds de b947.
  - Contre H : b298 reçoit 100 088,75 USDC de Rizzolver 3 min avant, produit d'une vente.
  - Pour H : 12 min plus tôt, le relais lui avait envoyé 100 000 USDC.
- **Ce qui le fermerait** : une règle d'allocation documentée et assumée (FIFO, prorata), présentée comme telle et jamais comme une borne. Ou la provenance de l'ETH vendu à Rizzolver : si cet ETH vient lui-même de b947, sa part marquée remonte.
- **Corrigé le 06/11 dans le dossier précédent** : `s51` trace désormais le relais, et ses bornes publiées égalent celles de `s15`. Les valeurs sous H sont dans `evidence/s15_s51_corrected.csv` (`from_b947_min_under_H`).

## 2. Titulaires des comptes d'exchange
- **Dépôts identifiés** :
  - Coinbase : Base `0x34172888…`, Solana `39dTXaMM…` ;
  - MEXC : Solana `96W8V3to…`, Ethereum `0x311ef6b5…` ;
  - BloFin : Ethereum `0xb1e5042f…` ;
  - Stake, KuCoin et Coinbase Ethereum : dossier précédent.
- **Ce qui le fermerait** : une réquisition, hors de portée d'un travail on-chain.
- **Le retrait de BONK de Coinbase** du 12/11, 12 h 37 après le dépôt de 24 ETH, reste EXPLORATORY. Il faudrait un second cas du même gabarit, mesuré contre des témoins.

## 3. BSC : contreparties de 2021-2022
- Non étiquetées : `0xb1256d6b…`, `0xcd5f3c15…`, `0xe19fc479…`, `0x7d372fdb…`, `0xfa7fb26b…`. Sans lien daté avec DMAGA.
- La fenêtre DMAGA est confirmée sur l'état archive (nonce 83 → 84 entre les blocs 43950885 et 43951101).
- Les réponses « bsc batch » du cache d'origine n'enregistrent pas leur requête : elles ne peuvent pas servir de fixtures. Seules les lectures Tatum du 06/11 le sont.

## 4. Part b947 de l'ETH sur Ethereum
- **Le modèle par actif (`s60_positions.py`) ne tourne que sur Base.** L'historique Ethereum de b298 publié par la PR #15 n'a pas les frais de gaz. Sans eux, la borne basse pourrait être surestimée.
- **Conséquence** : hors l'ordre `0x2fa91216…` du 12/11, borné sous H seulement par `s16` (lectures d'état archive, aucun autre mouvement d'ETH entre l'arrivée et l'ordre), les ordres Ethereum de b298 payés en ETH n'ont pas de part b947 bornée, notamment `0xdf0b6cf7…` du 17/11, qui finance le DCA de 482 SOL (N12).
- **Ce qui le fermerait** : les reçus (gasUsed × effectiveGasPrice) des tx signées par b298 sur Ethereum, puis `s60` sur ce grand livre.

## 5. Positions de mèmes
- Les 6 ordres de Base vers le dépôt MEXC Ethereum (10,54 ETH) restent à 0 : les stocks de HIGHER et de BOOMER mêlent du non-marqué ancien.
- Une règle d'allocation par lot (FIFO) donnerait un chiffre. Ce ne serait pas une borne.

## 6. Étiquettes
- **Deux sources indépendantes**, le spellbook Dune publié dans le dépôt (`evidence/labels/`) et Orb, pour :
  - Coinbase `GJRs4FwH`, `H8sMJSCQ` ;
  - MEXC `ASTyfSima4` ;
  - Binance `5tzFkiKs`.
- **Une seule source**, Blockscout metadata, pour :
  - « BloFin », sans source attribuée ;
  - « MEXC 21 », source OLI ;
  - Coinbase 14, 31, 41, 42, 55 sur Base. Coinbase 31 et 42 sont étiquetés « Exchange ».
- Les pages Orb, lues dans un navigateur, ne sont pas archivées.

## 7. Wallets voisins
- `5yYnURUv`, `CAX7f8ET` (Hp2BtvnZ) et `E72DuqDL` : historiques complets lus. Aucun lien de plus que N11.
- `AVUCZyuT` (frais Photon probables) et `8rNJ1v4L` (vendeur de prévente) sont des services partagés.
- Les destinations restantes d'`E72DuqDL` (`8FNkAcoK…`, `6nteBih7…`, `54YboiYV…`) ne sont pas lues : moins de 10 SOL.

## 8. Activité récente
- `Ei5yGz8d` : 19 tx de février 2025 à mai 2026, non analysées une par une. `EB6NoHkA` reçoit le loyer d'un compte de jetons le 07/05/2026.
- `Hp2BtvnZ` reprend une activité le 01/02/2026 : USDT puis un échange.

## 9. Mesures non faites
- Pas de témoin apparié pour le schéma « wallet neuf financé dans la minute, qui reçoit une position entière et la vend ». Trois cas observés : sans taux de base, ce n'est qu'une répétition.
- Pas d'audit des conclusions par un agent tiers après ces corrections. Les deux audits indépendants ont porté sur les données et les calculs.
