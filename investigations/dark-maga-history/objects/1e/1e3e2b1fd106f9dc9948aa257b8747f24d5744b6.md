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

## Avancement (03/11 01:25 UTC)
1. Audit, accès, signatures : FAIT. Mint 6 624 533 signatures, pool 9 875 478.
2. Téléchargement complet pool + mint : FAIT, 514 + 476 tranches, trou du 23/07 23:36-minuit comblé.
3. Venues : `scripts/col_03_venues.py` (74 venues) : quasi fini, `raw/full_venue/`. Découverte des venues à relancer sur le brut complet si besoin.
4. Flux wallets : `scripts/col_30_flows.py "$V/tmp/prio3.csv" 6 6` en cours (856 wallets). Reprise : relancer, ce qui existe est sauté.
5. Comparateurs : sélection FAITE (523 superset, 213 bande principale, DMAGA retenu, S=21/07 19:00, 1,29 M$).
   `etude_final/code/col_50_ctrl.py swaps` en cours, principaux d'abord. Puis `ana_10_table.py`, `gel.py ajouter` de la table si voulu, `ana_50_tests.py`, `ana_90_verdict.py`.
6. Après venues et flux : `scripts/run_derive.sh` complet (dis_05, nrm_10 --force, chk_20, ana_20, ana_21, ana_22, ana_50), `scripts/chk_21_venue_chain.py`, `scripts/ana_19_export.py`, `ana_31_select.py`, flux des nouveaux, `ana_32_hops.py 1`, `ana_30_flows.py`, `ana_60_clusters.py`, `exp_70_funder_share.py`.
7. Rapports : `rep_65_social_links.py`, `rep_70_reports.py`, `rep_75_timeline.py`, `rep_80_viz.py`, `chk_90_selfcheck.py`. CASE_REPORT, COORDINATION, ATTRIBUTION, MISSING_EVIDENCE à écrire à la main sur ces sorties.
8. Dépôt GitHub privé `Dark-MAGA-Investigation` à créer et pousser une fois validé. Pas de données lourdes.

## Faits établis (voir preuves dans les fichiers)
- Création : signature fePxr7ER…, slot 277417695, 14/07/2024 02:05:25 UTC, créateur 8YLEuUtZ4eFMJbf46oNb1CeG6dYFWGyxnQSh9hrgzBzR,
  achat 0,2 SOL pour 7,1 M. Financé 33 min avant par Coinbase 3 (0,5 SOL). Migration Raydium 02:15:31 UTC, signature 2zmB9nbU…
- Musk : fenêtre [19:03:27 ; 19:30:13] UTC le 21/07, id d'image 19:23:20,585 UTC. Chris Winig 16:02:29 UTC.
- Wallets résolus par préfixe, suffixe et montants, sans complétion : H3QsBrrivimFJmSpTXuvig2n1Bh7JuYxrriRSEszT6cc (@ashrobinqt,
  coût recalculé 1 087 $ contre 1 086 $ sur la capture), 5QhJJcFZu2ashyKyWSTGHcsyo6ZBCbpVuJqeutvQHScd (@0xRamonos, achats DCA Jupiter
  17-19/07 par keepers DCAK…), GXZvXsD6hxaLeFvQisWpdAwsayJxga7w9EeafhFZG2Ra (@ai_9684xtpa, 48,5 SOL, 14,69 M).

## Corrections déjà faites, à ne pas reproduire
- Couverture : pool + mint ne voient pas les swaps directs CLMM ou Orca (GCvHhE vend 478 M sans achat visible). D'où `full_venue/`.
- `etude/` : registre contaminé par mon test e2e, lignes 9-22 synthétiques étiquetées réelles. Étude = `etude_final/`, gelée le 02/11 23:47 UTC.
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
