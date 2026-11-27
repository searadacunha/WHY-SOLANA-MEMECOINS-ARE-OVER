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

## Avancement (03/11 04:15 UTC)
Enquête livrée, verdict gelé rendu, audit des conclusions FAIL corrigé sans nouvel audit. Publié sur le dépôt privé.
Reste à décider par Benjamin : les 3 auditeurs à l'aveugle (fuites, statistiques, protocole) ; valider l'amendement 001 (amendement 002) ; un second audit des conclusions.
Pour tout recalcul : `scripts/run_derive.sh`, puis `ana_60`, `ana_61`, `ana_62`, `ana_64`, `ana_65`, puis `rep_65`, `rep_70`, `rep_72`, `rep_75`, `rep_80`, `rep_90`, `chk_63`, `chk_90`. Toujours sous `scripts/guard.py`.
`/Volumes/PHI-Data/Dark-MAGA-Investigation/` ne contient qu'un venv abandonné.

## Faits établis (voir preuves dans les fichiers)
- Création : signature fePxr7ER…, slot 277417695, 14/07/2024 02:05:25 UTC, créateur 8YLEuUtZ4eFMJbf46oNb1CeG6dYFWGyxnQSh9hrgzBzR,
  achat 0,2 SOL pour 7,1 M. Financé 33 min avant par Coinbase 3 (0,5 SOL). Migration Raydium 02:15:31 UTC, signature 2zmB9nbU…
- Musk : fenêtre [19:03:27 ; 19:30:13] UTC le 21/07, id d'image 19:23:20,585 UTC. Chris Winig 16:02:29 UTC.
- Wallets résolus par préfixe, suffixe et montants, sans complétion : H3QsBrrivimFJmSpTXuvig2n1Bh7JuYxrriRSEszT6cc (@ashrobinqt,
  coût recalculé 1 087 $ contre 1 086 $ sur la capture), 5QhJJcFZu2ashyKyWSTGHcsyo6ZBCbpVuJqeutvQHScd (@0xRamonos, achats DCA Jupiter
  17-19/07 par keepers DCAK…), GXZvXsD6hxaLeFvQisWpdAwsayJxga7w9EeafhFZG2Ra (@ai_9684xtpa, 48,5 SOL, 14,69 M).

## Corrections déjà faites, à ne pas reproduire
- « 28 h après Butler » était faux : 3 h 54. 3LoAYH et consorts = comptes publiés par Jupiter. JD25…, JD1d…, JD38…, DCAK… = exécutants Jupiter DCA. AYymVrc, sYBdq543 = escrows DCA.
- Le 03/11, `ana_60_clusters.py` version Python a monté à 2,3 Go, swap 10 Go, disque 7,77 Go, sous la pause de PolySentinel. Réécrit en DuckDB, 521 Mo. Plus aucun calcul lourd hors `guard.py`.
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

## Reprise après l'audit du 03/11 (2026-11-03 11:16 UTC)
Lire `audits/2026-11-03/AUDIT_FINAL.md` puis `CORRECTIONS.md`. Statut : NON VALIDÉE. Branche `audit-2026-11-03`. Les travaux `work_E`, `work_F`, `work_G` n'étaient pas rendus quand la limite d'usage a coupé la session : vérifier avant d'utiliser. `git diff` montre les corrections non relues de l'agent F. Dérivé corrigé prévu dans `VERBATIM HD/.../data_v2/`, l'ancien `data/` ne doit pas changer.

## Revue GitHub du 04/11/2026
Lire `docs/AUDIT_2026-11-04.md` pour le périmètre exact. Corrections du code vérifiées sur 53 tests offline ; 27 empreintes gelées conformes. README anglais et corrections ciblées de la synthèse, sans replay du brut ni validation générale. Les valeurs reprises des réaudits H/I sont distinguées du recalcul local des sommes de ponts. Aucun état d'une session Mac ni aucune disponibilité du disque externe ne sont certifiés par cette revue. Les autres remarques H/I, la synchronisation des tables et un rejeu avec les archives restent ouverts.
