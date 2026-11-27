# deBridge : Base, BSC et retour Solana (Dark MAGA, 06/11/2026)

Suite du dossier `../2026-11-05_evm-recipient-deeptrace/` (PR #15) : où vont, au-delà d'Ethereum, les fonds que b298 reçoit de b947 et du relais. Ce dossier consolide le dépôt privé `dmaga-debridge-next-trace`, après un audit contradictoire. Personne n'est accusé. Un nom d'exchange désigne un service.

## Résultats en bref
- **Sans hypothèse d'allocation (VERIFIED)** :
  - des fonds issus de l'USDC de b947 atteignent soit le dépôt Coinbase de b298 sur Base, soit un dépôt MEXC par BSC et Solana ;
  - les deux ordres du 12/11/2024 en portent ensemble au moins 100 028,64 USDC venus de b947 (50 015,31 si l'on ne marque que l'USDC des exécutions deBridge reçues par b947) ;
  - les deux bornes ne peuvent pas être nulles en même temps (`FINDINGS.md` §3).
- **Sous l'hypothèse H** (le relais ne transporte que des fonds de b947, convention de la première version du dossier précédent, non démontrée) :
  - 24 ETH vers Coinbase, dont au moins 23,748588117 ETH de b947 ;
  - 182 548,80 USDC vers MEXC, dont au moins 100 027,93 (prorata) ou 99 383,28 (strict).
  - Le dépôt privé publiait 23,7486 ETH et 100 067,30 USDC, présentés comme des bornes certaines.
- **Nouveau** :
  - le DCA de 482 SOL du 17/11/2024 aboutit dans un wallet neuf, `2aeEoq5n`, qui revend la position 393,81 SOL nets. Ce sont des fonds de b298 ; leur part b947 n'est pas bornée ;
  - `Ei5yGz8d` et `Hp2BtvnZ` créditent la même adresse de dépôt Coinbase ;
  - un 88e lien deBridge, exécuté par un solver tiers.
- **Corrections** : `FINDINGS.md` §0, `AUDIT.md`.

## Fichiers
| Fichier | Contenu |
|---|---|
| `FINDINGS.md` | Constats, preuves, niveaux, bornes sous H et sans hypothèse |
| `NEW_CONNECTIONS.md` | Relations N1 à N13 |
| `UNRESOLVED.md` | Questions ouvertes et ce qui les fermerait |
| `AUDIT.md` | Audit contradictoire : méthode, corrections, outils évalués |
| `REPRISE.md` | Reprise : état, commandes, caches, prochaines recherches |
| `FLOW_GRAPH.md` | Graphe Mermaid des flux |
| `CROSSCHAIN_LINKS.csv` | 88 ordres DLN reliés par orderId, authentifiés par recalcul (périmètre de `s52_links.py`, voir `FINDINGS.md` §0) |
| `BASE_FLOWS.csv`, `BSC_FLOWS.csv`, `SOLANA_RETURN_FLOWS.csv` | Flux par chaîne (bornes de l'ancien modèle, sous H) |
| `evidence/s60_*`, `s15_*`, `s16_*`, `s17_*`, `s13_*`, `s34_*` | Bornes par actif, relais, chaîne MEXC, frontière, orderId recalculés, positions DCA |
| `evidence/fixtures/` | Réponses brutes minimales (231 réponses RPC, 8 fichiers Solana, 4,2 Mo) avec `MANIFEST.json` |
| `evidence/debridge_api_*_extract.csv` | Extraits de l'API deBridge (projet deBridge non publié), limités aux ordres de ce dossier ; empreintes des fichiers sources dans `AUDIT.md` |
| `data/` | Grands livres Base et Solana, changements d'état BSC |
| `MANIFEST.json` | sha256 de chaque fichier publié du dossier |

## Reproduire, hors ligne, depuis un clone neuf
Python 3.12 ou 3.14, bibliothèque standard seulement.

```
python -m unittest discover -s investigations/2026-11-06_debridge_base_bsc_solana/tests -v   # 12 tests, réseau coupé, fixtures seules
python -I investigations/2026-11-06_debridge_base_bsc_solana/scripts/s99_selfcheck.py      # 31 assertions, réseau coupé
python -I investigations/2026-11-05_evm-recipient-deeptrace/scripts/s99_selfcheck.py        # 31 contrôles du dossier précédent
```

Les collectes et les reconstructions complètes, qui relisent les grands caches locaux non publiés, sont décrites dans `REPRISE.md`.
