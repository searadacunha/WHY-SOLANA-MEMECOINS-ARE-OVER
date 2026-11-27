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
