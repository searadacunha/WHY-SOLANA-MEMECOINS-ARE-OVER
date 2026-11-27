# Reprise du dossier

À lire d'abord : `README.md`, `FINDINGS.md` §0 et §3, `UNRESOLVED.md`, puis `AUDIT.md`.

## État au 06/11/2026
- Migration du dépôt privé `dmaga-debridge-next-trace` terminée. Ce dépôt ne reçoit plus de commits : son archivage est à décider par Benjamin.
- Tests hors ligne :
  - ce dossier : `tests/` (12 tests), `scripts/s99_selfcheck.py` (31 assertions) ;
  - dossier précédent : `../2026-11-05_evm-recipient-deeptrace/scripts/s99_selfcheck.py` (31 contrôles).
- Dépendance : ce dossier importe `ev_lib`, `sol_lib` et `dln` du dossier précédent (PR #15). La PR qui l'ajoute est empilée sur la branche de la PR #15.
- PR #15 et #16 fusionnées le 06/11. Les corrections de `s51` (relais tracé) et de `dln.py` (v2 de `FulfilledOrder`) sont faites dans le dossier précédent (`AUDIT.md` §7).

## Caches
- **Publiés** : `evidence/fixtures/`, `MANIFEST.json`. Lus en premier par `nt_lib.py`.
- **Locaux, non publiés** (centaines de Mo) :
  - le `raw/` de la collecte d'origine (Blockscout Base, RPC, Helius) ;
  - le `raw/` du dossier précédent (Ethereum) ;
  - le `raw/` de ce dossier : collectes du 06/11, soldes archive BSC et Ethereum, historiques Solana des nouveaux wallets.
- Pour relire ces caches sans réseau, déclarer leurs emplacements :
```
export DMAGA_NT_RAW_RO=<raw de la collecte d'origine>:<raw du dossier précédent>
```

## Commandes (depuis `scripts/`)
```
python3 -I s13_orderid_check.py                 # orderId recalculés sur tous les reçus en cache, contrôle des liens
python3 -I s15_relay_bounds.py                  # s51 rejoué, relais tracé, borne commune
python3 -I s16_mexc_chain_bound.py              # chaîne MEXC, sous H et au pire cas
python3 -I s17_joint_destinations.py            # frontière Coinbase / MEXC, seuils de nullité
python3 -I s60_positions.py                     # bornes par actif sur Base, positions de mèmes
python3 -I s34_dca_trace.py                     # positions Jupiter DCA, circuit FvgqHM
python3 -I s51_build.py ; python3 -I s52_links.py ; python3 -I s53_solana_flows.py ; python3 -I s54_bsc_flows.py
python3 -I s98_fixtures.py                      # reconstruit evidence/fixtures (caches locaux requis)
python3 -I s99_selfcheck.py                     # autocontrôle, réseau coupé
```
- **Collecte (réseau)** :
  - `s30_sol_hist.py <wallet>` : Helius `getTransactionsForAddress`, clés du pool de recherche par `dmaga.config` ;
  - `s31_sol_ledger.py <wallet>` ;
  - `s10_base_ledger.py`, alimenté par `recv_server.py <port>` et `collector.js` dans un onglet local : Blockscout Base refuse les scripts ;
  - `s11_base_balances.py` ;
  - `s20_bisect.py`, `s23_bsc_blocks.py` : BSC sur l'état archive.
- Toute nouvelle réponse va dans `raw/` de ce dossier, ignoré par git.

## Prochaines recherches, par valeur attendue
1. **Frais de gaz de b298 sur Ethereum** (reçus de ses tx signées), puis `s60` sur Ethereum. On saurait alors borner la part b947 de l'ETH qui paie le DCA de 482 SOL (N12) et les autres ordres ETH vers `Ei5yGz8d`.
2. **Provenance de l'ETH vendu à Rizzolver le 06/10/2024.** Si cet ETH vient de b947, l'hypothèse H devient en partie démontrable (`UNRESOLVED.md` §1).
3. **Témoins** : taux de base du schéma « wallet neuf, position entière reçue puis vendue », mesuré sur des wallets comparables avant d'en tirer quoi que ce soit.
4. **Adresses de dépôt partagées** : appliquer la règle de N11 à tous les destinataires des wallets du groupe des 33, avec les étiquettes Dune du dépôt.
5. ~~Corriger la PR #15~~ : fait le 06/11 (`AUDIT.md` §7).

## Pièges rencontrés
- Le grand livre Ethereum publié n'a pas les frais de gaz : n'y appliquer aucune borne par actif.
- Un récepteur local qui accepte les écritures cross-origin est une porte d'injection dans les preuves.
- Les faux jetons « UЅDС » et « ETH », et les sosies `GV2w…`, `9obN…`, `Ei5y…`, se mêlent aux historiques réels. Filtrer par adresse de contrat, jamais par symbole.
- Tatum (BSC archive) limite fortement le débit : une lecture toutes les 20 s.
