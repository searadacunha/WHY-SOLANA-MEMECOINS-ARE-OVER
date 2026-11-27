# État de sécurité : clés Helius

Relevé du 03/11/2026. Aucune clé n'est écrite ici. Une clé est désignée par `emp8`, les 8 premiers caractères de son SHA-256. Outils : `tools/scan_keys.py`, `tools/strict_keys.py`, `tools/check_pool.py`. Détail : `work_security/key_summary.tsv`.

## Verdict
- **GitHub : aucune clé connue ni clé en position de clé Helius**, sur les 7 dépôts du compte `searadacunha`, en clones miroir complets (réfs de PR comprises), gros objets compris.
- **Historiques git locaux (68 dépôts) : aucune clé réelle.** Les 677 lignes sont des faux positifs vérifiés par contexte masqué (voir plus bas).
- **Exposition réelle : locale.** Des clés sont en clair dans des transcriptions de `~/.claude/projects`, dans des fichiers de projet hors git et dans des journaux. **15 valeurs à traiter : 10 clés connues (5 du pool, 5 de service) et 5 de propriétaire non établi.** Rien ne montre une publication. Ces textes ont toutefois transité par les fournisseurs de modèle pendant les sessions. Une rotation est recommandée.

## Contrôle positif
Le même scanner, passé sur le fichier de clés du pool, retrouve les clés attendues avec leur empreinte. Un zéro du scanner a donc un sens. Limite : une clé qui n'est ni connue, ni nue en position de clé Helius, ni de forme UUID ne serait pas vue.

## Couverture

| Périmètre | Volume | Résultat |
|---|---|---|
| 7 dépôts GitHub en miroir | 468 Mo, objets jusqu'à 400 Mo | 0 ligne |
| 68 dépôts git locaux, objets jusqu'à 20 Mo, `~/.git` exclu (dépôt vide à ne pas toucher) | 677 lignes | 0 clé réelle |
| `~/.claude/projects`, `~/.codex/sessions`, `~/.codex/memories`, mémoire commune | environ 11 Go | clés réelles, table ci-dessous. `~/.codex/sessions` : aucune clé connue |
| Dépôt Dark MAGA : `evidence/`, `docs/`, `reports/`, `state/`, `scripts/` | | 0 clé réelle |
| Disque VERBATIM : `logs/`, `tmp/`, `project_snapshot_20261103.tar.gz` | | 0 ligne |
| Arbres de travail `~/Projects`, `~/Documents`, fichiers de 30 Mo au plus, sans médias, sans `.git` | 465 289 fichiers, 1 illisible | clés réelles, table ci-dessous |

Non couvert : le brut `raw/` (réponses RPC, sans URL de requête), les fichiers de plus de 30 Mo des arbres de travail, le reste de `~` hors de ces dossiers.

## Faux positifs écartés, lus en contexte masqué
- `bb38eca4`, `53ba6a27`, `489e89dd`, `45fed095` (`public-apis`) : identifiants de collections Postman.
- `01cbdeac` (`hermes-agent`) : identifiant de tâche dans un test.
- `d5daf620` : identifiant d'annonce Ashby dans une URL `jobs.ashbyhq.com/helius/`.
- `ba4d671d` : identifiant de thread Codex.
- `9c57d852`, `4a07c2d9` : valeurs de test dans `test_gpt_review.py`, dont le second est manifestement factice.

## Clés à traiter

| emp8 | Classe | Transcriptions | Autres fichiers en clair | Priorité |
|---|---|---|---|---|
| `668dcbcd` | pool | 24 | 10, tous dans `~/Documents/Bureau/pump_bundle_detector` (prompts et scripts `reverif_*`), hors git | 1 |
| `89b11db1` | service | 11 | `Crypto/bots/bot_helius_v2.py` (en dur), `.env.bak_20260728_avant_ajout_helius`, une note de sauvegarde mémoire | 1 |
| `c9b7d184` | service | 8 | `check_helius.py` (en dur), le même `.env.bak`, deux notes de sauvegarde mémoire | 1 |
| `541c134e` | service | 1 | le même `.env.bak` | 2 |
| `4ffc5871`, `1b41221e` | service | 1 chacune | aucun | 2 |
| `8d0837a9`, `d2ee2f02`, `4b1c52fc`, `5142ccc4` | pool | 1 chacune | le fichier de clés prévu (sauf `8d0837a9`) | 2 |
| `e3f9bc03` | inconnue | 3 | aucun. Collée dans un message, c'est la clé de la transcription du 02/08 | À identifier |
| `aeb8ab7b` | inconnue | 7 | aucun. Collée dans un message | À identifier |
| `4201833b` | inconnue | 1 | aucun. En dur dans un script montré à un agent | À identifier |
| `048735c3` | inconnue | 1 | `Why-Solana-Memecoins-Are-Over/.env`, ignoré par git, jamais commité | À identifier |
| `43f54e49` | inconnue | 0 | `pump_bundle_detector/logs/detector.log` et `run.out`, une URL de requête journalisée | À identifier |

« Inconnue » veut dire : ni dans le pool, ni dans les fichiers de service. Je ne les ai pas testées : leur propriétaire n'est pas établi par le fichier, et les utiliser sort de la consigne. Elles sont peut-être déjà révoquées.

## Les cinq clés du pool

| emp8 | 08:20 UTC | Après les audits A et C |
|---|---|---|
| `668dcbcd` | getHealth ok, gTFA ok | ok, ok |
| `4b1c52fc` | ok, ok | ok, ok |
| `d2ee2f02` | ok, ok | **HTTP 429 max usage reached**, gTFA ok |
| `5142ccc4` | ok, ok | **429, 429** |
| `8d0837a9` | ok, ok | **429, 429** |

**Le pool a perdu 3 clés sur 5 dans la journée.** Une autre session (`forensics_v2`) a noté la même chose. Part de chaque enquête non mesurée : les auditeurs ont compté leurs appels (A : 295 `getTransaction`, C : environ 11 400 crédits comptés à 10 par page, tarif non revalidé), l'autre session non vue d'ici. Les deux clés qui restent sont aussi les plus exposées pour `668dcbcd`. **Toute nouvelle collecte lourde est donc limitée**, et la rotation de `668dcbcd` retirera une des deux dernières clés valides si la nouvelle n'a pas de crédits.

## Autres points
- `~/.config/phi-backup/age-identity.txt` a une copie en clair sur `VERBATIM HD/PHI-recovery/`, le même disque que les paquets chiffrés qu'elle ouvre. Déjà connu, pas de copie hors site. Hors du périmètre Helius, signalé.
- `~/.env.example` contient un vrai token Telegram selon `~/INDEX.md`. Non revérifié ici.
- Les clés de `~/Downloads/.env` ont servi environ 45 min à la collecte du 02/11, avant la bascule sur le pool (journal du projet).
- Aucune clé n'a été affichée, copiée ou journalisée par cet audit. Les fichiers de service ont été lus en local pour calculer des empreintes, sans aucun appel réseau avec ces clés.

## Procédure de rotation, à exécuter par Benjamin
Elle demande le tableau de bord Helius et peut couper des services : je ne l'ai pas lancée.

1. **Identifier.** Pour relier une clé du tableau de bord à une empreinte, sans laisser de trace dans l'historique du shell :
   ```
   read -s K; printf %s "$K" | shasum -a 256 | cut -c1-8; unset K
   ```
2. **Créer** la nouvelle clé dans le même compte Helius, avant de révoquer l'ancienne.
3. **Remplacer, clés du pool :** fichiers listés dans `~/.config/forensics_v2/helius_sources.json`, puis mettre à jour `pool_fingerprints` dans ce même JSON. `dmaga/config.py` est gelé, mais il lit ce JSON : la rotation ne touche aucun fichier gelé.
4. **Remplacer, clés de service :** `~/Downloads/.env` (lu par une trentaine de scripts, dont des services en production). Recenser ce qui tourne avant : `launchctl list | grep benjamin`, bot, PolySentinel. Remplacer les valeurs en dur de `bot_helius_v2.py`, `check_helius.py` et des scripts `reverif_*` par une lecture d'environnement.
5. **Tester** : `scripts/py.sh audits/2026-11-03/tools/check_pool.py` depuis le dépôt, et relancer les services un par un.
6. **Révoquer** les anciennes clés dans le tableau de bord, seulement après l'étape 5.
7. **Nettoyer, à ta décision, rien n'est supprimé sans accord :** les `.env.bak`, `logs/detector.log`, `logs/run.out`, les notes de `~/Documents/Systeme/sauvegardes/2026-10-16_decision_6/memoire/claude_downloads/`. Pour les transcriptions de `~/.claude/projects`, une rotation rend l'effacement inutile.
8. **Vérifier :** relancer `tools/scan_keys.py` avec les nouvelles empreintes.

Ordre conseillé : `668dcbcd`, `89b11db1`, `c9b7d184`, puis le reste. Identifier d'abord les 5 inconnues : si elles n'existent plus dans le tableau de bord, il n'y a rien à faire.
