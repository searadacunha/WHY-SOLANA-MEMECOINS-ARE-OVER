# État de la recherche : destinataires EVM des sorties Dark MAGA

> **Addendum du 06/11/2026 :** le modèle de bornes `s51_bounds.py` repose sur l'hypothèse H d'un relais contenant uniquement des USDC venus de b947. Cette hypothèse n'est pas démontrée et les minima ne doivent pas être présentés comme inconditionnels. Les nouveaux calculs et les traces Base/BSC/Solana sont dans la [PR #16](https://github.com/searadacunha/Dark-MAGA/pull/16).


**Date :** 05/11/2026. **Statut :** passe principale terminée. 2d86 est décrit mais pas tracé en aval ; l'activité de b298 sur Base et BSC n'est pas lue (`UNRESOLVED.md` §3).

Le dossier a été construit hors du dépôt local, puis publié depuis un clone neuf. Le dépôt local contient une étude gelée (`etude_final/`) et son verrou refuse `git worktree`. Rien dans `etude_final/` ni le README n'a été modifié.

## Livrables
| Fichier | Contenu |
|---|---|
| `FINDINGS.md` | Constats avec niveaux (VERIFIED, SUPPORTED, EXPLORATORY, UNRESOLVED, REFUTED), hashes complets, montants exacts |
| `UNRESOLVED.md` | Ce qui manque et ce qui le fermerait |
| `b947_full_history.csv` | Historique Ethereum complet de b947 : 78 lignes (ETH, internes, ERC-20, NFT). L'empoisonnement est marqué dans `flags`, pas supprimé |
| `b298_b947_relationship.csv` | 26 transferts entre b298 et b947, directs ou par le relais `0x4978cd7e…`, avec le contexte d'une heure avant et après |
| `b947_post_dmaga_flows.csv` | Arrivées sur b947 avec les sorties à 5 min, 1 h, 24 h et 7 j ; vidage, relais, sorties de b298 dans les 24 h |
| `evm_shared_counterparties.csv` | Contreparties communes aux wallets EVM ; les hubs de service sont marqués et exclus |
| `solana_to_evm_clusters.csv` | Makers Solana par destination EVM, avec les liens Solana directs entre eux |
| `evidence/` | Historiques de b298, 86f9, 2d86 et du relais ; ordres DLN décodés ; ledgers Solana ; contrôle des exécutions côté Solana ; bornes ; profils ; nonces sur les autres chaînes ; contrôle des références |
| `evidence/selfcheck_cache/` | Les 9 reçus RPC bruts nécessaires à l'autocontrôle hors ligne |

## Sources
- **Ethereum, sans clé :**
  - Blockscout v2 (`eth.blockscout.com/api/v2`) : source principale, complète, avec tags ;
  - Routescan (API compatible Etherscan, chaîne 1) : tx et internes ;
  - RPC public `ethereum-rpc.publicnode.com` : reçus et journaux.
- **Solana :** Helius, avec les clés du pool de recherche lues par `dmaga.config.helius_keys()`. Aucune clé n'est écrite dans un fichier publié.
- **Autres chaînes :** RPC publics publicnode (nonce, solde, code) pour Base, BSC, Arbitrum et Polygon.
- **Non utilisés :**
  - `stats-api.dln.trade` : refus Cloudflare 1015, non contourné ;
  - Blockscout Base, Arbitrum et Polygon : 403 anti-robot.

## Échecs silencieux trouvés et traités
1. **Routescan `tokentx` omet les transferts ERC-20 antérieurs à juillet 2023.** Trou repéré grâce aux appels `USDC.transfer` de b947 en 2023, qui n'avaient pas de transfert correspondant ; reçus RPC relus pour confirmer. Les jetons viennent donc de Blockscout.
2. **Ventes par des tiers prises pour de l'empoisonnement.** La règle écartait des ventes réelles exécutées par UniswapX ou des solveurs. Corrigé ; le solde USDC reconstitué de b298 concorde avec `balanceOf`.
3. **Comptes de jetons Solana.** L'arrivée de 48 960,81 USDC chez `Ei5yGz8d` manque dans ses signatures. Elle a été retrouvée sur son compte USDC, et le script cherche désormais aussi les comptes de jetons.
4. **Dédoublonnage des ordres.** Le corpus Solana donne le montant avec frais, les fills Ethereum le donnent sans frais : certains ordres étaient comptés deux fois. Corrigé en comparant le `giveAmount` brut exact.
5. **Bornes USDC réécrites.** Elles sont calculées sortie par sortie, en entiers, avec assertion. Une borne intermédiaire publiée dans une conversation (« au moins 27 498 USDC du dépôt Coinbase ») était fausse : la borne basse est 0.
6. **Arrondi.** La somme des bornes basses des ventes USDC → ETH vaut 247 663,99, et non 247 664,00. Erreur repérée par l'autocontrôle avant publication.

## Tests
Depuis `scripts/` :
```
python3 -I s99_selfcheck.py      # 31 assertions, réseau coupé, sur evidence/ et evidence/selfcheck_cache/
python3 -I s98_verify_refs.py    # réseau requis : relit sur la chaîne chaque hash et signature de FINDINGS.md
```
Les deux passent dans un clone neuf de cette branche, sous Python 3.12 et 3.14. `s98` a besoin d'un accès Helius pour les 9 signatures Solana.

## Reproduire la collecte (réseau)
Depuis `scripts/`, avec un cache local par défaut dans `../raw/`, ignoré par git :
```
python3 -I c01_collect.py ; python3 -I c02_blockscout.py <adresses>
python3 -I s30_dln_all.py b947 b298 86f9 ; EV_SKIP_BS_INTERNAL=1 python3 -I s30_dln_all.py 2d86
python3 -I s10_history.py <clé> <adresse> <sortie.csv> [--no-gas]
python3 -I s20_gzx.py [wallet] [sortie] ; python3 -I s22_ei5_fills.py
python3 -I s40_relationship.py ; python3 -I s50_post_flows.py ; python3 -I s51_bounds.py
python3 -I s60_crosschain.py ; python3 -I s80_shared.py ; python3 -I s90_profile.py
../../../scripts/py.sh s70_clusters.py   # Python du projet (duckdb) ; link_edges.parquet est hors dépôt (DMAGA_EXT)
```
