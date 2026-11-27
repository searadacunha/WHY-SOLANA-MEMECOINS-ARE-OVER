# État de reprise : enquête Dark MAGA

Fichier mis à jour à chaque lot validé. Pour reprendre : lire ceci, puis `JOURNAL_AGENTS.md`, puis `docs/SOCIAL_FINDINGS.md`.

## Où sont les choses
- Code, docs, rapports, petits livrables, preuves légères : `~/Projects/Dark-MAGA-Investigation`.
- Données brutes et gros parquet : `/Volumes/VERBATIM HD/Dark-MAGA-Investigation/{raw,data,logs,pylib}` (BIG = `.../data`).
- Python : `scripts/py.sh` (interpréteur 3.12 système + `pylib` sur le disque USB, FAT32 : pas de liens,
  4 Gio max par fichier, pas de base DuckDB persistante, des fichiers `._*` apparaissent, à ignorer).
- Ne PAS utiliser `/Volumes/PHI-Data` : un renommage y a pris 174 s le 02/11. `/Volumes/PHI-Data/Dark-MAGA-Investigation/`
  ne contient qu'un venv abandonné.
- Disque interne : plancher diskguard 13,5 Go. Rien de gros ici. `curl` déclenche le hook : `diskguard.py run --need <taille réelle>`.
- Lancer tout processus long avec `scripts/detach.py <log> -- <cmd>` (survit à la session, caffeinate lié au PID).

## Clés
Pool de recherche (5 clés) lu à l'exécution par `dmaga/config.py`, empreintes dans `~/.config/forensics_v2/helius_sources.json`.
Jamais écrites. Les clés de `~/Downloads/.env` servent à des services : environ 45 min de collecte les ont utilisées
le 02/11 avant la bascule, à signaler à Benjamin. Une transcription du 02/08 contient une clé en clair.

## Avancement
1. Audit et ancien travail : FAIT, `docs/PRIOR_WORK.md`.
2. Accès : FAIT. gTFA remonte à 2024. X par identifiant (fxtwitter, syndication). Grok sans crédit. Wallet API Helius 403.
3. Signatures (`scripts/col_01_signatures.py`) : mint FINI 6 624 533 ; pool en cours (relancer reprend).
4. Téléchargement complet `scripts/run_full_batch.sh <since> <until>` : FAIT jusqu'à 1721779200 (24/07 00:00) pool+mint.
   À lancer sur la suite une fois sigs_pool fini : `run_full_batch.sh 1721779200 <fin>`.
5. Normalisation `scripts/nrm_10_trades.py --force` puis `chk_20_vault_chain.py`, `dis_05_venues.py`, `ana_20_pnl.py`, `ana_21_token_edges.py`.
6. Flux par wallet : `scripts/col_30_flows.py <csv owner,t_buy,t_sell> <workers> <rps>`, puis `ana_30_flows.py`. FAIT pour 5 graines + 12 nœuds.
7. Social : agent en arrière-plan, `docs/SOCIAL_FINDINGS.md`, `data/x_posts.jsonl`, `evidence/`.
8. Étude gelée `etude/` : plan et code écrits, contrôles positifs OK. Audit silent-failure en cours, gel à faire AVANT tout calcul réel.
   Comparateurs : `scripts/col_40_controls.py activity` en cours (`BIG/controls/activity.jsonl`), puis
   `etude/code/col_50_ctrl.py select`, `swaps`, `ana_10_table.py`, `ana_50_tests.py`, `ana_90_verdict.py`.
9. Rapports et visualisations : à faire.

## Faits établis (voir preuves dans les fichiers)
- Création : signature fePxr7ER…, slot 277417695, 14/07/2024 02:05:25 UTC, créateur 8YLEuUtZ4eFMJbf46oNb1CeG6dYFWGyxnQSh9hrgzBzR,
  achat 0,2 SOL pour 7,1 M. Financé 33 min avant par Coinbase 3 (0,5 SOL). Migration Raydium 02:15:31 UTC, signature 2zmB9nbU…
- Musk : fenêtre [19:03:27 ; 19:30:13] UTC le 21/07, id d'image 19:23:20,585 UTC. Chris Winig 16:02:29 UTC.
- Wallets résolus par préfixe, suffixe et montants, sans complétion : H3QsBrrivimFJmSpTXuvig2n1Bh7JuYxrriRSEszT6cc (@ashrobinqt,
  coût recalculé 1 087 $ contre 1 086 $ sur la capture), 5QhJJcFZu2ashyKyWSTGHcsyo6ZBCbpVuJqeutvQHScd (@0xRamonos, achats DCA Jupiter
  17-19/07 par keepers DCAK…), GXZvXsD6hxaLeFvQisWpdAwsayJxga7w9EeafhFZG2Ra (@ai_9684xtpa, 48,5 SOL, 14,69 M).

## Corrections déjà faites, à ne pas reproduire
- GJRs4FwH…, H8sMJSCQ…, 2AQdpHJ2… = Coinbase 3, 1, 2 (Dune spellbook) : financeur commun du créateur et de 9PrmF8 = pas un lien.
- 9UsmwVmb…, Eqe7fgb5…, D55ba7tz… etc. = réserves de pools (CLMM, DLMM, Orca), `dmaga/venues.py` : pas des destinataires.
- 3LoAYHuS, HFqp6ErW, GP8StUXN, 3CgvbiM3, 7iWnBRRh (+ FERjPVNE) : wallets d'exécution d'un service (pass-through dans la tx du swap,
  100 M+ dans chaque sens, centaines de contreparties, tous créés le 12/01/2024). PAS un groupe de personnes, PAS un lien entre
  wallets signalés. Le « cluster 5QhJJc/9PrmF8/H3QsBr » a été retiré pour cette raison.
- Habp5bnc… : envoie de la poussière de SOL à beaucoup d'adresses. Ses arêtes de SOL < 0,001 ne valent rien. Son arête DMAGA avec 5QhJJc (8 M) reste à expliquer.
- DuckDB héritait du fuseau de Lisbonne (UTC+1) : forcé en UTC dans `dmaga/db.py`.

## Pistes réelles à instruire
- Consolidation à la création : 6t2dz4jm, 8YrEVPQq, 99Xrt5uu, AW63YBXX → AtZjv3Du (210 sigs) → NxtXcmEW (41 M) → 5QhJJc (8 M), 74qFhHyp, 35nAuv6j, Akp46Dic.
- Autres gros précoces qui redistribuent : GFpqfj, Ei5yGz, BteHCe, 7GVCZA, 9SHtoD, 6b29tK, BNHsrnuv/2ZRM3G8 (aller-retour 30 M).
- Sorties de H3QsBr (USDC vers FpCMFDFG, 3HSYXe, 255yZg) et 9PrmF8 (H9Xezqfd, 2 052 SOL en 48 tx), GXZvX (Co3zTr2M, 8N4AvP9j, 42MSVe).
