# Méthode et limites

## Sources

| Donnée | Source | Clé | Remarque |
|---|---|---|---|
| Transactions Solana des courbes Pump.fun (KM, XC78) | Helius `getTransactionsForAddress`, jsonParsed, tri croissant, jusqu'au 04/01/2025 | pool de recherche (`dmaga/config.py`), jamais affichée | pages brutes hors dépôt (`KEKIUS_EXT`) |
| 1 000 premières signatures des pools Raydium | Helius, idem | idem | `KEKIUS_EXT/pool_first1000_sigs.json` |
| Autres transactions Solana | RPC public `api.mainnet-beta.solana.com` (`getTransaction`, `getSignaturesForAddress`) | aucune | cache par signature |
| Transferts KEKIUS Ethereum et jambe WETH des pools | Routescan, API compatible Etherscan, `tokentx` par contrat | aucune | publiés : `data/eth_kekius_transfers.csv.gz`, `data/eth_kekius_pool_weth.csv.gz` |
| Historiques d'adresses Ethereum | Routescan `txlist`, `txlistinternal`, `tokentx` | aucune | `data/eth_history/` |
| Étiquettes Ethereum | `metadata.services.blockscout.com`, Blockscout v2 | aucune | une étiquette d'exchange suffit à classer « service » |
| Wallets, flux et clusters DMAGA | `data_v2/*.parquet` de l'enquête d'origine (disque externe, non publiés en entier) | — | `wallets`, `trades`, `funding_edges`, `exit_flows`, `wallet_clusters`, `nodes` |
| Profil X de Musk | Wayback CDX et captures, fxtwitter, presse | aucune | `evidence/social/MUSK_PROFILE_TIMELINE.md` |

## Règles de calcul

- **Solana, mouvement d'un propriétaire** : `postTokenBalances − preTokenBalances` par `owner` pour le mint, SOL natif du compte signataire (frais inclus). Aucun montant n'est déduit d'un log. Les lieux d'échange (courbe, autorité Raydium `5Q544fKr…`, compte de migration `39azUYFW…`) ne sont jamais des propriétaires.
- **Ethereum, livre par wallet** (`k32`) :
  - delta net KEKIUS par adresse et par transaction, sans compter les pools, le contrat du jeton (qui encaisse la taxe), le FeeCollector Uniswap, le Universal Router, 1inch v5, 0x Settler et FlashWallet, ni le Spender MetaMask ;
  - le delta net WETH des pools vaut le coût (achat) ou le produit (vente) ;
  - une transaction avec plusieurs receveurs nets ne reçoit pas de montant ETH : **33 003 lignes ambiguës** ;
  - `data/eth_kekius_wallets.csv` contient encore des contrats de routage et des bots, `0x1f2f10d1…` par exemple, avec des montants impossibles pour un seul wallet. Ce n'est pas une liste de personnes ;
  - les chiffres cités pour `0x33a5…` sont exacts : chaque transaction a un seul receveur net.
- **Avant et après l'événement** : coupure à 2024-12-31 06:02:01 UTC, borne basse vérifiée du changement de nom. Rien n'est compté « avant » qui pourrait se situer après.
- **100 premiers acheteurs** : ordre (slot, ordre de lecture) des transactions réussies où le solde du propriétaire monte ; courbe complète, puis premières transactions Raydium. Sur Ethereum, ordre (bloc, index de transaction) des achats.

## Test de l'univers DMAGA par compte de jetons associé (ATA)

- **Principe** : un wallet qui achète un jeton SPL le reçoit, dans la quasi-totalité des cas, sur son ATA. L'adresse `PDA(owner, Tokenkeg, mint)` est déterministe, et son historique de signatures reste lisible même une fois le compte fermé. Un appel par couple (wallet, mint).
- **Contrôle de la dérivation** : 797 comptes de jetons sur 797 dans les transactions des deux courbes sont l'ATA dérivée (`tests/test_ata.py`).
- **Limite** : un bot qui achète via un compte de jetons non associé échappe à ce test. L'activité d'une ATA n'est pas forcément un achat : poussière, airdrop, création par un tiers. Chaque candidat retenu est relu au niveau de la transaction.
- **Changement de source en cours de collecte** : à partir du 7 394e couple, le pool Helius a répondu « max usage reached ». La suite passe par le RPC public. **Contrôle** : 30 couples déjà lus via Helius, 15 actifs et 15 vides, ont été relus via le RPC public, avec **30/30 ensembles de signatures identiques** (`data/ata_backend_check.json`).
- **Piège écarté** : `solana-rpc.publicnode.com` répond `[]`, sans erreur, pour une ATA qui a un historique (constaté le 06/11/2026). Il n'est pas utilisé.
- **Seuil de hub** : une contrepartie de sortie ou de financement qui touche plus de 25 wallets DMAGA est exclue du noyau (`k19`).
- **Bot ou trader à haute fréquence** : critères de `k18`, chacun suffisant :
  - plus de 50 opérations DMAGA ;
  - plus de 100 transactions sur l'ATA Kekius dans la fenêtre ;
  - au moins 1 000 signatures sur l'ATA ;
  - au moins 200 transactions du wallet entier dans les 24 h avant son premier mouvement Kekius. Ce critère est ajouté après la relecture de `DMJmb8aJ…`, environ 1 000 tx par jour : le volume sur l'ATA ne suffit pas à le voir.

  Ses correspondances sont non discriminantes.

## Classement d'une relation

- **CONFIRMÉ** : transaction relue, reçu figé ou ligne publiée, montants et heure recalculés.
- **CORROBORÉ** : plusieurs indices indépendants (transfert direct, programme commun, co-signature, geste identique).
- **HYPOTHÈSE** : co-temporalité ou similitude sans flux.
- **REJETÉ** : exchange, routeur, solveur DLN, bot MEV, autorité Pump.fun, réserve de pool ou hub.

Un transfert confirmé ne prouve ni une identité civile, ni la propriété des clés, ni une information privilégiée.

## Reproductibilité

- `tests/` : 9 tests hors ligne (`python3 -I -m unittest discover -s investigations/2026-11-06_dmaga_kekius_cross_token/tests`).
  - Ils relisent les reçus figés, recalculent `0x33a5…` depuis les transferts publiés et vérifient chaque ligne Ethereum de `FUNDING_GRAPH.csv`.
  - Passés le 06/11/2026 sous Python 3.12 et 3.14.
- Les collectes (`k10`, `k14`, `k30`, `k31`, `k33`) sont reprenables et mises en cache. Elles demandent le réseau ; `k10` et `k14h` demandent aussi le pool Helius.
- Les tableaux se régénèrent avec `k17`, `k32`, `k34` et `k50`.

## Limites connues

- **Couverture Solana** : aucune collecte complète des pools Raydium. KM compte plus de 600 000 transactions jusqu'au 31/12, XC78 plus de 600 000 jusqu'au 31/12. Il n'y a donc ni liste complète des acheteurs Solana d'avant l'événement, ni « 100 premiers bénéficiaires » Solana. Le croisement Solana passe par le test ATA de l'univers DMAGA, pas par l'inverse.
- **Pas de taux de base** : une adresse présente dans DMAGA et dans Kekius est fréquente chez les traders actifs de memecoins. Aucune correspondance n'est présentée comme anormale sans cette mesure.
- **Programme `9NLjj4Gj…`** : sa part dans l'ensemble des migrations Raydium n'est pas mesurée.
- **Wayback** : vers 11:24 UTC, la Wayback a renvoyé 429 sur les captures brutes (`id_`), avec le message « suspected abusive bot traffic ».
  - L'agent de chronologie a lu une capture, le JSON de 06:02:01, par la relecture standard, ce qui contournait de fait ce filtre ; il l'a noté dans ses limites.
  - Une tentative suivante avec des en-têtes de navigateur a été refusée par le classificateur de permissions.
  - Aucune requête vers archive.org n'a suivi. Ce qui reste à lire est listé dans `MUSK_PROFILE_TIMELINE.md` §5.
- **Presse et images** : les articles complets et les images de tiers restent hors du dépôt public (droits d'auteur). Seuls les URL, les heures de publication et les citations courtes sont publiés.
