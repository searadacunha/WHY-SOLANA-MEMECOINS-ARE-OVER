# État de reprise : enquête Dark MAGA

Fichier mis à jour à chaque lot validé. Pour reprendre : lire ceci, puis `JOURNAL_AGENTS.md`.

## Où sont les choses
- Code, docs, rapports, petits livrables, preuves légères : `~/Projects/Dark-MAGA-Investigation`.
- Données brutes et gros parquet : `/Volumes/VERBATIM HD/Dark-MAGA-Investigation/{raw,data,logs,pylib}`.
- Python : `scripts/py.sh` (interpréteur 3.12 système + `pylib` sur le disque USB, FAT32 : pas de liens,
  4 Gio max par fichier, pas de base DuckDB persistante).
- Ne PAS utiliser `/Volumes/PHI-Data` pour ce projet : un renommage y a pris 174 s le 02/11 (image
  APFS saturée par un autre travail). `/Volumes/PHI-Data/Dark-MAGA-Investigation/` ne contient qu'un
  venv abandonné, supprimable.
- Disque interne : plancher diskguard 13,5 Go, il restait 0,64 Go utilisables le 02/11. Rien de gros ici.

## Clés
Lues à l'exécution dans `~/Downloads/.env` par `dmaga/config.py`, jamais écrites. Les 7 clés répondent.

## Étapes
1. Audit de l'environnement et ancien travail : FAIT, voir `docs/PRIOR_WORK.md`.
2. Accès Helius et sources X : FAIT. gTFA remonte à 2024. X par identifiant (fxtwitter, syndication).
   Grok sans crédit. Pas de recherche X native.
3. Liste exacte des signatures (`scripts/col_01_signatures.py`) : en cours. Reprise : relancer le script.
4. Téléchargement complet par tranches (`scripts/col_02_full.py`) : à lancer après 3.
5. Normalisation (`scripts/nrm_10_trades.py`), PnL, cohortes : à faire.
6. Financement et sorties des gagnants : à faire.
7. Réseau social : agent en arrière-plan, sortie `docs/SOCIAL_FINDINGS.md`.
8. Plan de tests gelé (`etude/`), puis tests d'anomalie : à faire. Rien calculé avant le gel.
9. Rapports et visualisations : à faire.

Lancer tout processus long avec `scripts/detach.py` (survit à la session, caffeinate lié au PID).
