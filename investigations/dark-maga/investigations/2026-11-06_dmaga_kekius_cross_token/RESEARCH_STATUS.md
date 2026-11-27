# État de reprise

Mis à jour le 06/11/2026. Branche `investigate/dmaga-kekius-cross-token`, base `main` `0f77f26`. Ce dossier ne touche ni au
README racine, ni aux études gelées, ni aux PR #15, #16 et #17. Le travail parallèle `investigation/creator-links-pump-detection-20261106`
(piste `B5fC3Dg4…`, détection Pump.fun) n'est pas dupliqué. `B5fC3Dg4…` et `FKtvVzBS…` sont seulement inclus dans l'univers du test ATA.

## Fait
- Unités 1 à 3 : tokens, chronologie, Ethereum complet, lancement XC78 (bundles Jito, opérateur `3oqARBND…`, bilan +618,65 SOL), 100 premiers acheteurs, revue d'outils (`TOOLS_REVIEW.md`).
- Test ATA complet : 14 304 couples (`data/ata_scan_summary.csv`), classement et relecture des candidats (`k18`, `data/ata_overlap.csv`). Réponse dans `FINDINGS.md` §8.
- 15 tests hors ligne.

## En cours
- Rien. `k37` (sorties de `3oqARBND…`) est terminé : 4 386 tx lues.

## Reprendre
1. Scripts reprenables : `cd investigations/2026-11-06_dmaga_kekius_cross_token/scripts && ../../../scripts/py.sh <script>`.
   - `scripts/py.sh` exige le disque de l'enquête d'origine ; sinon, utiliser `python3` avec `DMAGA_BIG` défini.
2. Pistes suivantes : `UNRESOLVED.md` U2, U5, U6, U9, U13 à U15.
3. Les reçus se régénèrent depuis `evidence/receipts_args.txt` : `tr '\n' '\0' < ../evidence/receipts_args.txt | xargs -0 ../../../scripts/py.sh k40_receipts.py`.

## Données hors dépôt (à recréer ou copier)
- `KEKIUS_EXT` (défaut `../raw` à côté du clone) :
  - `sol/raw/{km_curve,xc_curve}` (pages Helius) ;
  - `pub/` (cache RPC public) ;
  - `evm/` (cache Routescan et Blockscout) ;
  - `pool_first1000_sigs.json`.
- `DMAGA_BIG` : `data_v2/` de l'enquête d'origine (disque externe).
