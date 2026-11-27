# Enquête Dark MAGA ($DMAGA)

Enquête forensique on-chain et X sur `7D7BRcBYepfi77vxySapmeqRNN1wsBBxnFPJGbH5pump`. Dépôt privé uniquement. Rien de ce dépôt
n'accuse une personne : l'échelle A, B, C, D du rapport s'applique à chaque constat.

## Reprise
1. Lire `state/STATE.md`, puis `JOURNAL_AGENTS.md`, puis `docs/CASE_REPORT.md`.
2. `git status` et `ps -ax | grep scripts/` pour voir ce qui tourne.
3. Données lourdes sur `/Volumes/VERBATIM HD/Dark-MAGA-Investigation/` (FAT32 direct, disque USB mécanique). Python : `scripts/py.sh`.
4. Étude gelée dans `etude_final/` : ne jamais écrire dans ses fichiers gelés ni dans `../dmaga/{collect,helius,config}.py` et
   `../scripts/col_40_controls.py` (gel par empreintes). Tout changement passe par `etude_final/amendements/`.
   `etude/` est un dossier contaminé conservé comme trace, voir `etude/CONTAMINATION_E2E.md`.

## Pièges propres à ce projet
- Clés : pool de recherche seulement (`dmaga/config.py`), jamais `~/Downloads/.env`.
- Ne jamais relier deux wallets par un service : échanges (Dune), réserves de pools (`dmaga/venues.py`), routeurs (`ana_22_nodes.py`),
  poussière de SOL. Deux faux liens ont déjà été retirés dans cette enquête, voir `state/STATE.md`.
- Heures en UTC : `dmaga/db.py` force le fuseau.
- Toute référence d'un rapport passe par `scripts/chk_90_selfcheck.py`.

## Publication par plusieurs sessions — 4 novembre 2026

Les deux branches ont des périmètres différents. Garder leurs corrections et leurs README respectifs :

| Cible | Commit de correction à conserver dans l'historique |
|---|---|
| `main` | `771bae81ed81fee309f024f027d60a6934938491` |
| `audit-2026-11-03` | `16c2396ddb8b80ea109c4f59a03822c1e7a6864e` |

`state/publication_baselines.json` fixe les blobs des README et les protocoles de chaque cible. Le gel de `etude_groupe/`, présent sur la branche audit, s'ajoute au gel de `etude_final/` ; conserver aussi leurs fichiers externes au dossier d'étude.

Avant chaque envoi :

1. Identifier la cible et conserver les travaux de la session sur une branche dédiée. Faire `git fetch origin`, puis vérifier `git status` et le HEAD distant de cette cible. Un clone incomplet doit récupérer l'historique nécessaire ; une référence absente est une erreur, jamais un contrôle ignoré.
2. Intégrer les nouveaux commits de la même cible par un merge relu avant publication. Ne pas recopier globalement un arbre, un dossier ou les fichiers d'une autre branche. Relire les conflits fichier par fichier en préservant les corrections déjà acceptées. Ne pas résoudre le README en choisissant aveuglément une ancienne version.
3. Après intégration et avant le push, refaire le fetch et lancer le garde pour la cible choisie : `python3 scripts/check_publication.py --target main` ou `python3 scripts/check_publication.py --target audit-2026-11-03`. Le garde utilise `origin/<cible>` localement ; il ne contacte pas GitHub et ne rafraîchit pas cette référence lui-même. Relire ensuite le diff destiné à cette cible.
4. Utiliser un push normal ou une PR. Ne jamais utiliser `--force` ou `--force-with-lease`. Ne jamais pousser l'historique d'un snapshot local synthétique. Avec l'API Git Data, partir de l'arbre du HEAD distant courant, ne remplacer que les chemins explicitement relus et revérifier le HEAD avant de mettre à jour sa référence.

Les README racine restent identiques à leurs versions acceptées, sauf demande explicite de l'utilisateur. Une nouvelle version autorisée doit faire l'objet d'une révision documentée de l'ancre et du blob de la cible ; ne pas mettre à jour ces références automatiquement pour faire passer un contrôle. Un nouveau dossier de recherche peut avoir son propre README sans remplacer celui du dépôt.

La PR #1 `audit/dedup-readme-20261104` reste draft et sans fusion automatique. Ses correctifs, basés sur un ancien `main`, ne doivent pas remplacer globalement les versions audit : conserver notamment `dmaga.paths`, `exige_v2()`, `DMAGA_BIG`, `nrm_11_accounts.py`, `ana_21_token_edges.py` avant `ana_20_pnl.py`, puis roundtrip et flows.

La CI vérifie l'historique de la cible, le README et les fichiers gelés, puis les tests du garde. Sur audit seulement, elle installe `requirements-test.txt` et exécute aussi les tests hors ligne existants, dont les 27 empreintes des deux protocoles. Elle ne lance aucune collecte ni dérivation métier. Le selfcheck des rapports et le replay brut restent des vérifications distinctes, à documenter lorsqu'ils ne peuvent pas être exécutés.

Ces consignes et cette CI ne sont pas une protection serveur. Au relevé du 4 novembre, GitHub indiquait `protected: false` et les rulesets étaient indisponibles pour le plan privé du dépôt. Ne pas présenter un contrôle de publication réussi comme la garantie qu'un autre accès GitHub ne peut pas contourner ces consignes.
