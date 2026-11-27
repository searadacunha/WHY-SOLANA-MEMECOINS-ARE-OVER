# PR_NOTES — intégration de l'addendum ASTRA dans searadacunha/DARK-MAGA

Ce dossier a été préparé **hors dépôt**, sans aucune écriture Git. La publication est à faire par le propriétaire.

## 1. Placement (conventions AGENTS.md et `investigations/`)

Cible : `investigations/2026-11-18_astra_team_promoters_beneficiaries/`, sur la branche `main`. Le dossier a la même structure que `2026-11-06_historical_replay/` : README, rapports, `data/`, `evidence/receipts/`, `scripts/`, `tests/`.

| Source (`/workspace/dark-maga/astra/`) | Destination dans le dépôt |
|---|---|
| `README.md`, `FINAL_REPORT.md`, `TEAM_ATTRIBUTION.md`, `EARLIEST_PROMOTERS.md`, `FIRST_BUYERS.md`, `PROMOTER_WALLET_LINKS.md`, `FINANCIAL_BENEFICIARIES.md`, `UNRESOLVED_IDENTITIES.md`, `GRAPHS.md`, `REFUTATION.md`, `METHODOLOGY.md`, `SHA256SUMS.txt` | `investigations/2026-11-18_astra_team_promoters_beneficiaries/` |
| `data/**` (dont `data/derived/`) | `…/data/` |
| `evidence/**` (`receipts/`, `receipts/key/INDEX.json`, `x/`, `media/`, `web/`, `query_log.tsv`) | `…/evidence/` |
| `scripts/*.py` | `…/scripts/` |
| `tests/test_astra_offline.py` | `…/tests/` |
| `ci_wrapper/test_astra_launch_team.py` | **facultatif** : `tests/test_astra_launch_team.py` à la racine, pour que `forensic-pipeline-tests.yml` (`pytest -q tests`) exécute aussi ces tests |

**À ne pas livrer :**
- `raw/` (cache RPC d'environ 36 Mo, HTML 8kun, logs) : garder hors dépôt ;
- `ci_wrapper/` en tant que dossier ;
- `__pycache__/`.

**Lien facultatif** : une ligne dans `JOURNAL_AGENTS.md` et/ou dans `docs/EVIDENCE_INDEX_2026-11-18.md`, en mettant à jour les portes de preuve LN-xx. À faire **à la main** et relu.

Les « Required evidence gates » du README de `2026-11-18_launch_network_public_attribution` sont traités ainsi :

| Porte | État |
|---|---|
| 1. Image | octets et pixels comparés (pas identiques au pixel, pHash 0) ; recherche de source antérieure négative |
| 2. Reçus G41v + taux de base sniper | faits |
| 3. Post supprimé archivé | texte corroboré via le RT archivé de kiki |
| 4. Les 19 adresses Choupette | 9 hors groupe matérialisées dans `FIRST_BUYERS.md` § 4 |
| 5. Créateur ↔ G41v à deux sauts sans hubs | **non établi** ; nouveau lien créateur ↔ cluster via un motif CEX + collecteur (B) |
| 6. Déclarations tenues pour des affirmations | respecté |

## 2. Fichiers gelés et zones interdites

- `etude_final/**` : gel par `PROTOCOL.lock` (SHA-256). Les changements passent par `etude_final/amendements/` ; **aucun n'est nécessaire ici**.
- `dmaga/collect.py`, `dmaga/helius.py`, `dmaga/config.py`, `scripts/col_40_controls.py` : gelés par empreintes.
- `etude_groupe/` : gelé sur la branche `audit-2026-11-03`. Ne pas cibler cette branche avec cette PR.
- `etude/` : contaminé, conservé comme trace. Ne pas toucher.
- `README.md` racine : reste **identique** (`state/publication_baselines.json`). Ne pas modifier, ne pas mettre à jour l'ancre ni le blob.
- `reports/*.md` : générés par `rep_70` / `rep_72`. **Ne pas éditer.** Ce dossier les cite, il ne les remplace pas.
- `docs/historical/pass4/PUBLIC_X_ACTIVITY.md` : laissé intact comme trace historique. La nouvelle entrée Murray à 02:31:29 vit dans cet addendum.
- Commits de correction à préserver : main `771bae8…`, audit `16c2396…`.

## 3. Garde-fous et contrôles requis (AGENTS.md)

1. `git fetch origin` ; vérifier `git status` et le HEAD distant (attendu `643934a`, ou plus récent : dans ce cas, merge relu fichier par fichier).
2. Copier **uniquement** les chemins ci-dessus. Pas de copie globale d'arbre ni de branche.
3. `python3 scripts/check_publication.py --target main`
4. `python3 -m unittest discover -s tests -p test_publication_guard.py -v`
5. `python3 -I -m unittest discover -s investigations/2026-11-18_astra_team_promoters_beneficiaries/tests -v`
6. `python -m pytest -q tests --ignore=tests/test_publication_guard.py` (si le wrapper racine est ajouté)
7. `cd investigations/2026-11-18_astra_team_promoters_beneficiaries && sha256sum -c SHA256SUMS.txt`
8. `scripts/chk_90_selfcheck.py` ne vérifie que `docs/` et `reports/`. Les fichiers ASTRA n'y sont pas placés, donc ils ne sont pas concernés. Si une ligne est ajoutée dans `docs/EVIDENCE_INDEX_*`, n'y écrire que des formes tronquées en « … » ou des adresses déjà présentes dans les données, puis relancer le selfcheck.
9. Push normal ou PR. **Jamais `--force` ni `--force-with-lease`.** Avec l'API Git Data : partir de l'arbre du HEAD distant courant et revérifier le HEAD avant de mettre à jour la ref.
10. Contenu public : aucune donnée personnelle superflue (profils X minimisés : `name`, `location`, `description` retirés), aucune accusation, échelle A/B/C/D explicite partout.

## 4. Simulation locale effectuée (sans Git)

Copie du clone `643934a` dans `/tmp`, dépôt des fichiers aux chemins cibles, sans commit. Résultats :
- `check_publication.py --target main` ;
- tests du garde ;
- tests ASTRA via unittest et pytest.

Résultats obtenus le 2026-11-18 vers 17:58 UTC :
- `python3 scripts/check_publication.py --target main` → `PASS target=main candidate=643934a…; README unchanged; 17 frozen files preserved`. Le garde vérifie le HEAD commité : il faut **le relancer après le commit réel**.
- Tests du garde (`test_publication_guard.py`) : 21 OK.
- `python3 -I -m unittest discover -s investigations/2026-11-18_astra_team_promoters_beneficiaries/tests` : 14 OK, **sans réseau** (`unshare -n`).
- `pytest -q tests --ignore=tests/test_publication_guard.py` avec le wrapper racine et `requirements-test.txt` : **125 passed, 6 subtests passed**, sans réseau.
- `sha256sum -c SHA256SUMS.txt` : OK.

## 5. Résumé de PR proposé

**Titre** : `ASTRA addendum: launch team roles, earliest promoters, first buyers, beneficiaries (2024-07-14)`

**Corps :**
- Nouveau dossier `investigations/2026-11-18_astra_team_promoters_beneficiaries/`. Aucune modification de fichier existant, à part le wrapper de tests facultatif.
- **Nouveau (B)** : 11 retraits Coinbase 2/3 synchronisés (01:32–01:41) financent le wallet créateur et 10 wallets frais, qui consolident tous plus tard vers le collecteur rare `9W9b…`. Taux de base sur 607 retraits : 5/5 des retraits de 1,05 SOL. Deux de ces wallets appartiennent au groupe 33. Coinbase seul n'est pas un lien ; le niveau B repose sur la conjonction des indices.
- **Nouveau (A)** :
  - échecs de G41v décodés (`TooMuchSolRequired`, limites UI 0,5/0,4 SOL × 1,01²) ;
  - comparateur sniper sur 54 tokens (médiane 2 s) ;
  - rejeu complet de la phase pump.fun (436 tx) ;
  - premier visuel tiers « $DMAGA » de @Murray_Gothbard (ex-@ChristienPhoto) à 02:31:29.
- **Corrections** : pfp et image du token pas identiques au pixel (pHash 0, ré-encodage) ; `Last-Modified` 01:49:10 = artefact CDN, retenir 01:51:10.
- **Phase 4** : aucun compte promoteur relié à un wallet ou à un profit, donc « attribution non établie ».
- 14 tests hors réseau (stdlib), reçus figés (environ 1 Mo), `SHA256SUMS.txt`.
