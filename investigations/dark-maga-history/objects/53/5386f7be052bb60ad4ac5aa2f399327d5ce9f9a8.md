# État de reprise

Mis à jour le 06/11/2026. Branche `investigate/dmaga-kekius-cross-token`, base `main` `0f77f26`. Ce dossier ne touche ni au
README racine, ni aux études gelées, ni aux PR #15, #16 et #17. Le travail parallèle `investigation/creator-links-pump-detection-20261106`
(piste `B5fC3Dg4…`, détection Pump.fun) n'est pas dupliqué. `B5fC3Dg4…` et `FKtvVzBS…` sont seulement inclus dans l'univers du test ATA.

## Fait
- Unité 1 : identification des tokens, chronologie, Ethereum complet, lancement XC78, 100 premiers acheteurs, lien de bot DQmMnaki → FJkb8WnW (`FINDINGS.md`).

## En cours
- Test ATA : `scripts/k14_ata_scan.py` (RPC public, reprenable, écrit `data/ata_scan.jsonl`) et `scripts/k14h_ata_scan_reverse.py` (Helius, ordre inverse, `data/ata_scan_h.jsonl`).
  - Univers `data/dmaga_universe.csv` : 7 152 adresses, dont 354 ajoutées par `k19` après le lancement de `k14`.
  - **Relancer `k14` une fois terminé**, pour couvrir les couples ajoutés.
  - Les deux fichiers `.jsonl` ne sont pas publiés (signatures brutes), seule leur synthèse le sera.

## Reprendre
1. `cd investigations/2026-11-06_dmaga_kekius_cross_token/scripts && ../../../scripts/py.sh k14_ata_scan.py`
   - `scripts/py.sh` exige le disque de l'enquête d'origine ; sinon, utiliser `python3` avec `DMAGA_BIG` défini.
2. Classer les couples actifs avant 06:02:01 : bot, hub, ou wallet à faible activité. Relire les seconds au niveau de la transaction (achats, ventes, SOL).
3. Ajouter les lignes à `data/ata_overlap.csv`, puis lancer `k50_tables.py` et les tests.
4. Pistes suivantes : `UNRESOLVED.md` U2 à U7.

## Données hors dépôt (à recréer ou copier)
- `KEKIUS_EXT` (défaut `../raw` à côté du clone) :
  - `sol/raw/{km_curve,xc_curve}` (pages Helius) ;
  - `pub/` (cache RPC public) ;
  - `evm/` (cache Routescan et Blockscout) ;
  - `pool_first1000_sigs.json`.
- `DMAGA_BIG` : `data_v2/` de l'enquête d'origine (disque externe).
