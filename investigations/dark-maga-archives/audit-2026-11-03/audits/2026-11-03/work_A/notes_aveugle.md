# Notes à l'aveugle, auditeur A, 03/11/2026

Écrites après lecture de `etude_final/analysis_plan.md`, `etude_final/code/{metrics,ana_10_table,ana_50_tests,ana_90_verdict,col_50_ctrl,chainutil,registre}.py`,
`scripts/col_*`, `dmaga/{collect,helius,normalize,pnl,labels,venues,db}.py`, `scripts/{nrm_10,chk_20,chk_21,dis_05,ana_19,ana_20,ana_21,ana_22}`.
Aucun fichier de `etude_final/tables/`, `etude_final/results.md`, `docs/`, `reports/`, `state/`, `JOURNAL_AGENTS.md`, `derived/`, `amendements/` n'a été ouvert à ce stade.
La seule chose vue du plan sur DMAGA : ce que le plan écrit lui-même (S = 21/07 19:00 UTC, 1 719 signatures, environ 1,3 M$ et 382 SOL une heure avant).

## Constats de lecture sur la fuite temporelle

1. `metrics.compute` coupe bien `t < S` en première ligne, sur toutes les colonnes. Aucune mesure M1 à M7 ne lit après S, par lecture du code. À tester par perturbation sur données réelles.
2. Fenêtres. M1 : 24 fenêtres de 3 h sur [S-75 h, S-3 h), alignées sur la fin. M2 : 3 fenêtres de 24 h sur [S-96 h, S-24 h). Bornes conformes au plan. Pas de chevauchement avec la fenêtre testée.
3. `spike_hour` : histogramme par heure UTC ronde, 72 h précédentes exclusives de h. La première heure candidate est ceil((créa+96 h)/1 h). Conforme. L'histogramme démarre à créa+24 h, donc les 72 h glissantes de la première candidate ne lisent pas avant créa+24 h (une tranche partielle au plus).
4. S est conditionné au futur du run-up par construction : sélection sur un pic postérieur aux fenêtres de mesure. C'est le design déclaré, pas une fuite. Mais :
   - premier pic obligatoire, donc un run-up qui atteint lui-même 20x et 500 signatures en h-1 devient le S. M1 et M2 sont donc tronqués par le haut, à l'identique sur tous les tokens. À regarder : les heures 16 h à 18 h du 21/07 sur DMAGA.
   - `truncated` dépend du nombre total de signatures listées depuis créa+24 h, y compris après S : conditionnement léger sur le futur. Un pool tronqué sans pic trouvé sort.
5. La bande de capitalisation est centrée sur DMAGA, avec une valeur lue avant le gel (plan, ligne 6). Déclaré. Le prix est lu avant S-1 h, à la minute de la dernière transaction, clôture Binance de la minute : fuite maximale de moins d'une minute, sans effet sur une bande large.
6. `fdv_at` : prix tiré du premier enregistrement qui a les deux réserves dans ses deltas. Il n'exige pas que ce soit un swap (peut être un LP). Sans effet attendu sur une bande à un facteur 10. Il demande `limit=200` sur `details=full` : à vérifier si l'API plafonne à 100 (écart au plan, 200 écrit).
7. R3 : S décalé d'une heure, mais la capitalisation n'est pas relue : elle reste celle de S20-1 h au lieu de S20-2 h. Écart mineur au plan (variante, jamais utilisée pour choisir).
8. S1 : `first` (premier swap) est calculé sur toutes les données jusqu'à AVATAR+1, mais c'est un minimum, donc sans effet futur. DMAGA a une fenêtre étendue de collecte qui n'entre pas dans `compute`. `CREATED = 1720923331` en dur : à vérifier contre le brut, comme `WINIG` et `AVATAR`.
9. `col_50_ctrl.swaps` : collecte jusqu'à S+1 h, jamais au-delà sauf DMAGA, `compute` coupe. Aucun champ futur dans `metrics.csv` sauf `fdv_usd` (S-1 h).

## Hypothèses de bug à tester sur le brut (pas encore testées)

H1. `parse_swaps` attribue tout le SOL du vault au bénéficiaire même si sa quantité diffère du vault (`qty_differente_du_vault` seulement compté, jamais écarté). Une transaction d'arbitrage (achat Raydium v4, revente sur un autre venue dans la même transaction) laissant un petit reste de jetons devient un « achat » de plein montant SOL pour une petite quantité. Touche M1, M2, M3, M4, M7. À mesurer : part de SOL dans les lignes où |qty|/|delta vault| < 0,99 pour DMAGA contre les comparateurs.
H2. Écarter les « non signataires à deux côtés » retire aussi les escrows DCA et les wallets gérés par programme, qui sont de vrais acheteurs. Comptés mais effet non mesuré. Le plan le déclare. À mesurer sur le brut : SOL écarté.
H3. Sans bénéficiaire (`sans_beneficiaire`) et frais : SOL perdu, à mesurer par token. Un biais différentiel DMAGA contre pairs compte plus qu'un taux absolu.
H4. `transactionIndex` absent devient 0 (`or 0`) : l'ordre intra-slot serait celui de `pre`. À compter dans le brut. Si présent partout, sans objet.
H5. Chaîne de soldes : `chain` lit uniquement le vault WSOL, pas le vault jeton. Elle ne teste que les transactions présentes, pas le début avant `created` ni la fin. Chaîne du vault jeton à refaire.
H6. `chk_20_vault_chain.py` : `material` est calculé sur `examples LIMIT 20`, trié par slot. Une rupture matérielle après les 20 premières ruptures de poussière passerait sans alerte. À recalculer sur toutes les ruptures.
H7. `slices_from_sigs` : trou déjà reconnu (23/07 23:36 à minuit). Les tranches viennent de runs différents (`--since/--until`, puis `--calendar`), elles peuvent se chevaucher ou laisser un trou. `db.py` déduplique par (signature, source) et non à l'intérieur d'une même source : un chevauchement de tranches d'une même source laisserait des doublons dans `trades.parquet`. À tester.
H8. `sigs_*` ne couvre que les adresses listées. `full_mint` ne voit pas les transferts SPL sans référence au mint. `completeness = "complet sur le pool et la courbe"` peut être faux. Les venues hors liste deviennent des « traders ». À tester : plus gros `owner` jamais signataires, non présents dans VENUES.
H9. `dis_05` exclut comme venue toute adresse qui a signé une fois. `venues.load` exige un programme AMM à 80 %. Un pool dont le programme n'est pas dans `AMM` (par exemple Meteora DAMM v2, Lifinity, Aldrin, GooseFX, Saber, Invariant, Crema, Openbook) reste un trader. À tester sur les propriétaires à deux côtés non signataires.
H10. Temps : seuls `rep_*` et `db.py` touchent au temps. Tout est passé par `timezone.utc` ou `gmtime`. Mais un fichier produit par une session DuckDB d'avant le correctif peut rester daté en local (`data/price_hourly.csv`, `reports/data_checks/`, `docs/TIMELINE.md`, rapports écrits à la main). À tester sur chaque fichier versionné : tout horaire UTC doit reproduire le `blockTime` brut. Un rapport écrit à la main (`docs/`) n'est pas protégé par `db.py`.
H11. `ana_22_nodes.py` : `kind="cex"` dès qu'un label existe et ne commence pas par Raydium, Pump.fun, DMAGA. Un Jupiter ou un service de swap est donc classé `cex` : erreur d'étiquette sans effet sur les clusters, à vérifier dans les rapports. Seuils routeur (20 contreparties et 50 % de passage) et hub (50) : un petit service reste `wallet`, faux lien possible.
H12. Regex de `labels.py` sur le SQL Dune : à vérifier qu'elle lit bien toutes les lignes et les bons champs (adresse, `cex_name`, `distinct_name`). Compter les lignes du SQL contre le dictionnaire.
H13. Le pic S compte les échouées. Le plan le dit. À chiffrer : ratio d'échec dans `sigs_pool` à l'heure S et dans les heures d'avant, S recalculé sur les seules réussies.
H14. Échecs à la collecte : `details=signatures` sans filtre de statut, `full` avec `status=succeeded`. À vérifier : égalité des ensembles, par tranche. `full_curve` sans filtre : `err` testé dans le parseur.
H15. `activity` : filtre sur [créa+24 h, créa+60 j), plafond 150 pages. Le test `n_late >= 500` lit la première page d'une requête de 1 000 signatures : correct si `limit` est respecté. `tronque_sans_pic` à compter, DMAGA n'est peut-être pas à égalité.
H16. `selection.jsonl` et `swaps_stats.jsonl` sont en ajout : doublons de pool possibles. `ana_10_table.main` lève pour `selection`, garde la dernière ligne pour `swaps_stats`.
H17. `ctrl_tx` : pool retenu sans `cursor.complete` ? `verify` contrôle cela. Parquet de swaps sauté s'il existe : une relance ne le refait pas. Vérifier un échantillon par mon propre parseur.
H18. Registre : les lignes synthétiques sont marquées `donnees="synthetiques"`. Le plan décrit le registre contaminé de `etude/`. Vérifier `etude_final/registre/tests.jsonl` et son chaînage, et que les valeurs réelles de `metrics.csv` viennent de pools existants du brut.
H19. Double attribution d'une transaction multi-bénéficiaires : `round(-delta*v/total)` : somme fidèle à 1 lamport près par ligne.
H20. `M3` lit « aucun swap Raydium antérieur » : les acheteurs de la courbe Pump.fun sont donc « nouveaux » : défaut identique pour tous les tokens, à noter comme limite d'interprétation.
H21. Dans `parse_tx`, `quote = venue_s if venue_s else venue_u` : quand les deux varient, le SOL et l'USDC sont répartis ensemble mais le test de sens utilise SOL seul. À regarder dans les multi-venues.
H22. `parse_tx` prend `sol_delta(BONDING_CURVE)` en lamports natifs, frais et loyers inclus côté courbe : à recouper avec le prix par jeton sur la courbe.
H23. Échelle : `qty/1e6` dans `ana_21` et `ana_20` suppose 6 décimales. Les décimales sont dans chaque balance : à vérifier.

## Ordre de travail fixé maintenant

1. Registre et `metrics.csv` (synthétique ?).
2. Complétude sigs contre full, échecs.
3. Chaîne de soldes par mon parseur, sur le brut, puis reconstruction des swaps.
4. Comparateurs.
5. Temps, étiquettes.
6. Assertions de `CLAIMS_INPUT.csv`.
