# Audit A : intégrité des données et fuites

Auditeur A, 03/11/2026. Dépôt au commit `01ae5a4`. Token `7D7BRcBYepfi77vxySapmeqRNN1wsBBxnFPJGbH5pump`. Personne n'est accusé de quoi que ce soit. Les constats portent sur des fichiers et du code, pas sur des personnes.

**Verdict global : FAIL.** Le brut, les chaînes de soldes, les heures UTC et le test gelé tiennent et se reproduisent, mais les fichiers de synthèse et plusieurs tableaux des rapports contiennent des erreurs vérifiées (lignes doublées, swaps sans valeur, résiduels faux, bots affichés comme acheteurs) et 3 assertions A sur 15 sont fausses ou non établies (C34, C35, C50).

Le verdict gelé « DMAGA non distinguable de ses pairs » n'est touché par aucun constat de ce rapport : `compute`, `swaps/*.parquet` et `metrics.csv` sont reproduits à l'identique par mon parseur.

## Périmètre

**Relu et recalculé, avec mon parseur (aucun import de `dmaga/normalize.py` ni `dmaga/pnl.py`) :**
- 2 699 114 transactions de `raw/full_{curve,pool,mint,venue}` (`work_A/a02_full.py`).
- 15 852 824 transactions de `raw/ctrl_tx`, 245 pools (`work_A/a03_ctrl.py`).
- 16 500 297 signatures de `raw/sigs_{pool,mint,curve}` (`work_A/a01_sigs.py`).
- 101 702 transactions de `raw/ctrl_migrations` (`work_A/a40_migr.py`).
- M1 à M7 écrits depuis le texte du plan, sur les 877 lignes de `derived/metrics.csv` (`work_A/a04_metrics.py`).
- Coût moyen écrit depuis la description du rapport, sur 71 706 wallets (`work_A/a14_pnl.py`).

**Réseau :** 295 `getTransaction` au total par `dmaga.helius`, graine 20261103 (`a30_network.py`, `a31_network_hidden.py`, `a34_payout.py`), 12 sur `api.mainnet-beta.solana.com`, sans clé. Aucune clé n'est écrite dans `work_A/` (recherche du motif de clé : 0 fichier).

**Notes à l'aveugle :** `work_A/notes_aveugle.md` a été écrit après le plan et le code, avant l'ouverture de `tables/`, `results.md`, `docs/`, `reports/`. Ses hypothèses H1 à H23 ont servi de liste de travail.

**Pas vérifié :**
- L'empreinte des fichiers : relue à part, `work_integrity/raw_verify.json` donne 33 033 conformes, 0 différent, 0 manquant, et 16 548 fichiers de `ctrl_tx` hachés. Je cite ce rapport, je ne l'ai pas refait.
- La nature exacte des programmes `ChXs7eqj`, `sra4HHgw`, `5YBiKeEK`, `45wPVSFE`, `3GMsedVP` : je décris ce qu'ils font sur la chaîne, je ne les ai pas identifiés.
- La reproduction en copie neuve citée en C49 : aucune trace de cette exécution n'existe dans le dépôt.
- Les assertions de contenu X et les sorties à 3 sauts (C03, C04, C16 à C19, C22, C31 à C33, C37 à C39) : hors de mon angle.
- Les mouvements DMAGA par SPL `transfer` des wallets non tracés, faute de brut (voir A-05).

## Constats

### A-01, MAJEUR : `trades.parquet` contient 5 903 lignes en double, qui faussent `wallets.parquet`
- **Preuve :** `work_A/a11_trades_shape.py`, `a32_small.py`, `a13_reconcile.py`. 919 783 lignes, 913 880 uniques.
  - 3 626 lignes `swap` doublées, soit 6 762,78 SOL comptés deux fois (achats et ventes). Exemple : `4YrMzRFRgmNZcGjEHBjYAQstroDTMM8TqF8JoXaXW2Z4Uxq8NeLsxQVVEfACofqKzmfAaK5tMnwbPaJhL3ve9X66`.
  - Cause 1 : 4 966 lignes, toutes dans le chevauchement de `full_pool/t1721777789` et `full_pool/t1721779200` (20 189 s, du 24/07/2024 00:00:00 à 05:36:29 UTC). La tranche qui comble le trou de C26 fait 6 h et recouvre la tranche calendaire suivante. Le comblement a donc créé ce défaut.
  - Cause 2 : 937 lignes en source `venue`, une transaction présente dans deux historiques `full_venue`.
  - `dmaga/db.py` dédoublonne par (signature, source) et pas à l'intérieur d'une source. La vue `vault` a un `DISTINCT` : la chaîne de soldes ne pouvait donc rien voir.
  - Mon coût moyen appliqué tel quel retombe exactement sur `wallets.parquet` (0 écart sur 71 706). Sans les doublons : 954 wallets changent, 2 673,49 SOL d'écart absolu de réalisé, 3 151,39 SOL d'achats et 3 609,72 SOL de ventes en trop (`out/a14_pnl.txt`, `out/a14_pnl_diff.csv`).
- **Exemples :** `ET8ZG5zA` 359,1 devient 203,6 SOL ; `Akp46Dic` (groupe de 33) 364,5 devient 268,7 SOL ; `C7i9beNH` (groupe) 404,5 devient 378,0 ; `5FzhCSWL` 144,6 devient 187,9 (rang 91 du top 100) ; `retrait_plus_7j` 106 081,51 devient 102 944,34 SOL d'achats.
- **Impact :** C35 (18 367 devient 18 309), C23 pour le nombre de lignes, `reports/TOP_TRADERS.md`, `reports/EARLY_BUYERS.md`, `reports/COORDINATION.md` ligne 203, réalisé du groupe. Aucun effet sur C05, C06, C15, C21, C24, C29, ni sur le test gelé.
- **Correctif :** dédoublonner par (signature, kind, owner, venue, token_delta) dans `db.py`, retirer la tranche `t1721777789` au-delà de minuit, relancer `run_derive.sh` et les rapports. Ajouter une assertion « aucune ligne en double » à `chk_90_selfcheck.py`.

### A-02, MAJEUR : l'autorité partagée `GpMZbSM2` traitée comme une réserve donne des swaps sans valeur
- **Preuve :** `work_A/a15_named.py`, `a19_gaps.py`, `a35_residual.py`. `venues.load()` garde `GpMZbSM2GgvTKHJirzeGfMFoaZ8UR2X7F4v8vHTvxFbL` (Raydium CPMM). `_is_venue_account` compte alors le WSOL de tous ses pools, y compris sans rapport avec DMAGA. Le code fait pourtant cette exclusion pour l'autorité Raydium v4, pas pour celle-ci.
  - 1 550 lignes classées `swap_other`, valeur 0 SOL, alors que le vault Raydium a bougé : 2 630,8 SOL, 142,6 M de jetons. Exemple : `2WCiMw9Ss66aWTWteUja5Ma899fZQsXANpXKWjjeiaYkau7HGpixTrtBzMxh9rUsmZSKi68bz3hrghsUNPLTAupe`, `DswkYbBh` reçoit 730 546,5 jetons, le vault reçoit 80,62 SOL, `sol_lamports` = 0.
  - 1 279 lignes `swap` au SOL faux, 416,3 SOL d'écart absolu, toutes avec `GpMZbSM2` dans `venue`. Exemple : `3qgdJivjQaGixp2GDezHdagMzvTLYyeYXnQsJyPoR8DrCqgbJq7tjzmDEe6qGT8SeRVMopEY5r5p8zZAqpgRdCAo`, trades 3,54 SOL, vault 35,64 SOL.
- **Impact :** PnL de ces wallets (`DswkYbBh` 840 SOL hors comptes, `7Mjg8z2F` 116,7 SOL). 0,19 % du volume. Ni les 4 wallets nommés, ni C05, C06, C15, ni le test gelé (il lit le seul vault).
- **Correctif :** limiter cette autorité à ses comptes DMAGA et au WSOL de la paire DMAGA, comme pour `RAYDIUM_AUTH`, puis renormaliser.

### A-03, MAJEUR : « les fonds viennent surtout d'échanges et d'historiques antérieurs » n'est pas établi
- **Preuve :** `work_A/a19_gaps.py`, `funding_edges.parquet`, niveau 0, 12 mois avant le mint, décimales saines.

| Origine du SOL reçu | SOL | Part |
|---|---|---|
| Sans étiquette | 2 024 216 | 67,8 % |
| Pool, trading antérieur | 440 896 | 14,8 % |
| Compte Jupiter | 302 898 | 10,1 % |
| Échange étiqueté | 217 530 | 7,3 % |

  Premier financeur non pool, sur 747 wallets : 301 sans étiquette, 244 échange, 198 compte Jupiter, 4 service. Le rapport n'écrit aucun dénominateur.
- **Limite honnête :** plusieurs sources sans étiquette ressemblent à des échanges (`F5GkEY9zmFLaDtrJZAu8oojgczy2KW1siCtT1GDK8Yru` 152 wallets, `FpCMFDFGYotvufJ7HrFHsWEiiQCGbkLCtwHiDnh7o28Q` 68, `HVoJWyPbQn4XikG9BY2A8wP27HJQzHAoDnAs1SfsATes` 58, `Czfq3xZZDmsdGdUyrNLtRhGc47cXcZtLG4crryfu44zE` 39), mais rien dans le dépôt ne l'établit : le fichier Dune ne compte que 112 adresses, dont 3 Coinbase.
- **Impact :** C50, question 6 du rapport.
- **Correctif :** publier ce tableau et écrire « 22 % du SOL vient d'échanges étiquetés et de trading antérieur, 68 % de sources sans étiquette ».

### A-04, MAJEUR : les plus gros « acheteurs » des rapports sont des allers-retours de quelques secondes
- **Preuve :** `work_A/a24_roundtrip.py`, `a18_misc.py`, `a11_trades_shape.py`.
  - Première ligne du tableau « Ce sont les achats à regarder en premier » de `reports/EARLY_BUYERS.md` : `5V97uEb4ZNuXFudphU5nwUapRmt7a2V51TbULQvPJwnx`, 111,49 SOL achetés, 111,49 SOL revendus en 10 s au plus, 113,94 SOL vendus dans la fenêtre. Jamais signataire sur 2 110 lignes, programme `ChXs7eqj` à chaque fois, délai médian jusqu'à l'opération suivante 0 s.
  - « 100 plus gros acheteurs (SOL engagé) » de `reports/TOP_TRADERS.md`, rangs 1 à 3 : `5V97uEb4` 32 833 SOL (100 % d'allers-retours en 10 s au plus), `AD65fgYti96iSSzSPaNazV9Bs29m7JbNomGjG4Cp5WFS` 16 740 SOL (100 %), `BmanDqQELF7QY5uRPw8vg3eMjR74WZnszKmNbLJKkay3` 12 869 SOL (98,7 %).
  - Fenêtre de Musk : 44,7 des 148,7 SOL d'achats sont ces allers-retours, dont `AD65fgYt` 37,59 SOL, première ligne du tableau.
  - Sur toute l'histoire : 110 822 SOL sur 787 109, soit 14,1 % des achats. 15,2 % dans les 24 h après Musk.
  - Le plan les écarte du test (« nature non établie », ligne 31), les rapports les montrent sans le dire. `4ToQp55m` (rang 5 des acheteurs, rang 40 des réalisés) est classé `wallet` à 47 contreparties, 3 sous le seuil de `hub` : il reçoit le SOL de 45 signataires différents (A-16).
- **Impact :** C34, lecture de C05, questions 4 et 5, H2. Aucun effet sur le test gelé : M1 sans allers-retours p = 0,160, M2 p = 0,179 (`out/a42_roundtrip_peers.txt`).
- **Correctif :** ajouter une étiquette `bot_aller_retour` (non signataire à programme propre, ou plus de 50 % d'allers-retours en 10 s au plus), retirer ces adresses des classements d'acheteurs, publier la part d'allers-retours par fenêtre.

### A-05, MAJEUR : des mouvements de jetons absents du brut, et des résiduels faux
- **Preuve :** `work_A/a13b_accounts.py`, `a21_ruptures.py`, `a26_hidden.py`, `a31_network_hidden.py`, `a35_residual.py`, `a36_residual2.py`.
  - Chaîne de chacun des 71 818 comptes de jetons DMAGA : 27 183 ruptures sur 1 163 comptes, soit 2 844,7 M de jetons de mouvements absents du brut (entrées 1 507,8 M, sorties 1 336,9 M, un même transfert peut compter des deux côtés). 0 sur les réserves de venues.
  - Échantillon de 17 de ces transactions sur la chaîne : toutes sont des SPL `transfer`, le mint n'est jamais dans les clés. Elles ne peuvent donc apparaître ni dans `full_mint` ni dans `full_pool`.
  - `raw/flows` en rattrape 22 152 (2 126,3 M) pour 1 219 wallets tracés, avec `dmaga_all` tronqué pour 20 d'entre eux. 1 117 wallets non tracés portent 5 265 ruptures et 675,9 M.
  - Somme de `residual_qty` : 937,1 M, alors que l'offre hors pools vaut 567,7 M à la fin. `7gEQ6syDZmyPE4JdfJm4qatawnDqvqdh6i8jJjCXio6h`, premier des « 25 plus gros résiduels » : 122,28 M, dernier solde vu 0,0 M. `HGs9NdwD2c4mYHb9fYdgp2Due5gbaSEdUV871wAiCkTd`, deuxième : 34,35 M contre 0,04 M. Sur 146 wallets à au moins 1 M de résiduel, 37 s'écartent de plus de 10 %.
- **Ce qui tient :** avant Musk la comptabilité est complète. À la borne basse, les derniers soldes somment à 1 084,53 M, moins 84,54 M de transferts vus par les seuls flux, soit 1 000,0 M. Hors pools : 938,0 M, ce que le rapport écrit. Le top 100 « coût connu » n'a que 4 wallets touchés, pour moins de 0,15 M : le filtre de coût connu résiste.
- **Impact :** colonnes « Résiduel » et tableau des résiduels de `reports/TOP_TRADERS.md`, `completeness`, C27 (limite incomplète). Le rapport ne mentionne pas ces mouvements dans « Données et fiabilité ». Pas d'effet sur C11, C14, C15, C21.
- **Correctif :** publier le chiffre ; prendre le résiduel sur les soldes de comptes plutôt que sur les flux ; signaler « partiel » dès qu'un compte a une rupture ; lever le plafond de `dmaga_all` pour ces 20 wallets.

### A-06, MINEUR : deux définitions de « SOL acheté » dans le même rapport, sans le dire
- **Preuve :** `work_A/a25_s1.py`. 3 h avant Winig : 401,52 SOL au test (C45), 507,93 SOL au vault (`trades.parquet` aussi). 3 h avant l'envoi : 229,28 contre 236,56. L'écart est le SOL des non-signataires à deux côtés et des transactions sans bénéficiaire, écartés par le plan et gardés par `windows.csv`.
- **Effet sur les rangs :** nul sur S1 (p = 0,0357 et 0,069 dans les deux cas). M1 p = 0,165 et M2 p = 0,184 avec tout le vault. Part du SOL de 24 h sans ligne : DMAGA 11,1 %, pairs 5,0 %, rang p = 0,21 (`out/a05_sensitivity.txt`). Pas de biais qui change le verdict.
- **Impact :** C07 et C45 sont justes pour le test, mais « 402 SOL sur les 3 h » sous-estime de 21 % ce que le vault a reçu.
- **Correctif :** ajouter « selon la règle du plan, 508 SOL au vault » à côté du chiffre.

### A-07, MINEUR : « 118 échouées » cache 83 % de signatures échouées
- **Preuve :** `work_A/a01_sigs.py`, `a13_reconcile.py`. Pool : 8 199 964 échouées sur 9 875 478 (83,03 %). Mint : 5 974 078 sur 6 624 533 (90,18 %). Les 118 sont celles de la seule courbe, seul historique collecté sans filtre de statut. Le pic de 24 h compte 86,3 % d'échecs ; 6,3 % dans les 24 h avant S.
- **Effet sur les chiffres :** aucun volume ne bouge, les échouées ne changent aucun solde. Le filtrage est exact (A-19).
- **Impact :** C23 (chiffre exact, lecture trompeuse).
- **Correctif :** écrire les deux taux dans « Collecte ».

### A-08, MINEUR : le biais des pics d'échecs n'est pas symétrique
- **Preuve :** `work_A/a04_metrics.py`, `out/a04_spike_success.csv`, `a43_subset.py`. Sur DMAGA, S reste 19:00 sur les réussies seules (1 370 sur 1 719). Sur les 212 du principal : 50 ont moins de 500 réussies à S, part d'échec médiane 8,9 %, p90 66 %. S changerait pour 59 pools, dont 58 sans pic retrouvé dans la partie collectée. Le plan écrit que « le même biais touche tous les tokens » : il touche 24 % des comparateurs et pas DMAGA.
- **Effet :** faible. Parmi les 152 comparateurs au pic identique, meilleur p = 0,150 (M1). Parmi les 161 à au moins 500 réussies, meilleur p = 0,148.
- **Impact :** C48, à préciser.
- **Correctif :** ajouter ces deux lignes aux limites, sans toucher au test gelé.

### A-09, MINEUR : C34, les cohortes ne sont distinctes que par définition
- **Preuve :** `work_A/a15_named.py`. Par premier achat : 1 644, 77, 18, 53 790 (rapport 1 645, 76, 18, 53 889). Mais 107 des 184 acheteurs de [16:02:29, 19:03:27) avaient déjà acheté avant le visuel, 51 dans les 6 h précédentes. `reports/EARLY_BUYERS.md` n'a qu'un tableau pour les deux périodes, de 10:02:29 à 19:03:27.
- **Impact :** C34, question 4.
- **Correctif :** écrire « cohortes de premier achat » et séparer le tableau en deux.

### A-10, MINEUR : C35, heure ronde et réalisés de poussière
- **Preuve :** `work_A/a15_named.py`, `a20_time.py`, `a14_pnl.py`. Sommet 631 363,63 SOL de capitalisation à 09:01:46 UTC (`TIMELINE.md` juste), « 09:00 UTC » dans `CASE_REPORT.md` est le début de l'heure. Sur 18 309 réalisés positifs dédoublonnés, 877 valent 0,001 SOL au plus.
- **Impact :** C35.
- **Correctif :** écrire 09:01:46 et donner aussi le compte à plus de 0,1 SOL : 9 885.

### A-11, MINEUR : venues sans historique et programmes AMM absents de la liste
- **Preuve :** `work_A/out/a17_venues.txt`. `venues.json` a été écrit après `col_03_venues.py` : 6 venues de `load()` n'ont pas de dossier `full_venue` (`568uySHSGgRoverMfvg4qrxVVrBP21QT2qZV3FBa1KUq`, `8CsFJ63BkJMDJzMc5Th2yaVipbGfH2JBbUMMi4NB9ns6`, `CQkkQeH9W7RFLv2parJpMD7kyYCnFDGWFmd7dNxbDJCG`, `DLk2JC3GQNqGeiq5uwPFT3SKuobhrmaY5vHnPKDtgNza`, `HhPL3RsEX5qCYpYbuBJdBdaAAPgB8HFwd1WeEn7k4pcM`, `JCcrJNTHcse52S4AWPszUcpB8xutZCgfJitQYYJ29Ucr`, 29 transactions à deux côtés). Programmes hors de `AMM` parmi les candidats écartés, donc comptés comme traders : Saber (18), Lifinity (4), Obric (6), OpenBook (2).
- **Impact :** faible, ordre de quelques dizaines de transactions. C24 reste juste pour ce qui est collecté.
- **Correctif :** relancer `col_03` sur ces 6 adresses et compléter `AMM`.

### A-12, MINEUR : `uiAmount` à 0 décimale dans les flux de 2021
- **Preuve :** `work_A/a19_gaps.py`. 6 183 lignes de `raw/flows` ont `decimals = 0`, toutes de 2021. `funding_edges.sol` vaut donc 1e9 fois trop : 1 128 lignes dépassent 1 M et somment à 22 138 milliards de « SOL », `exit_flows.amount` aussi pour 5 000 lignes, sur 2 wallets.
- **Impact :** toute somme non filtrée de ces colonnes est absurde. `link_edges` n'est pas touché, son filtre part de 2024 (0 ligne au-dessus de 100 000 SOL). C50 recalculé en écartant ces lignes.
- **Correctif :** calculer `amount / 10**9` dans `ana_30_flows.py`, jamais `uiAmount`.

### A-13, MINEUR : classes d'étiquettes approximatives
- **Preuve :** `dmaga/labels.py`, `scripts/ana_22_nodes.py`, `out/a12_links_shape.txt`, `a39_links.py`.
  - `kind = cex` couvre 12 nœuds, dont 10 ne sont pas des échanges (6 exécutants DCA, 2 escrows, un compte Jupiter, un pont).
  - Le motif sur `jupiter_docs_submit.mdx` étiquette WSOL, USDC et ComputeBudget comme « Jupiter, compte documenté ». `nodes.label` est vide pour 11 comptes Jupiter ajoutés par la boucle des flux.
  - C51 parle de « comptes de pourboire », `COORDINATION.md` de « jambes de routage » : la source dit « tip receiver », DefiLlama dit autorités de frais.
  - `5V97uEb4` reste dans 84 arêtes `funder_commun`, qui ne fusionnent pas de clusters.
  - Sur le SQL Dune, le motif lit bien les 112 adresses sur 112.
- **Impact :** aucun sur les liens de C51. Lecture des rapports.
- **Correctif :** nommer la classe `service`, filtrer les mints du fichier Jupiter.

### A-14, MINEUR : contrôles de chaîne incomplets
- **Preuve :** code et `out/a04_compare.txt`.
  - `chk_20_vault_chain.py` juge « matériel » sur les 20 premières ruptures seulement. Sans effet aujourd'hui, il n'y en a qu'une.
  - `chk_21_venue_chain.py` ne contrôle que le côté DMAGA des réserves.
  - `col_50_ctrl.py` ne contrôle que le vault WSOL. Le vault jeton a 34 ruptures sur 30 pools, dont aucune sur la fenêtre de DMAGA. Une rupture du seul vault jeton ne signale pas un swap manquant, car le vault WSOL bougerait aussi.
- **Correctif :** retirer le `LIMIT` du calcul de `material`, ajouter le vault jeton au rapport d'étude comme compteur, sans changer le gel.

### A-15, MINEUR : flux tronqués
- **Preuve :** `work_A/a29_flows.py`. Sur 1 219 wallets : `sol_out_after` 318 tronqués, `usdc_out_after` 98, `usdt_out_after` 53, `in_before` 279, `first_in` 819 (premier reçu correct, tri croissant), `dmaga_all` 20. Les plafonds sont notés dans les fichiers.
- **Impact :** C37 est une borne basse, `exit_summary` n'est pas exhaustif. C36 tient (filtre poussière sans effet, 11 et 10).
- **Correctif :** écrire le nombre de wallets tronqués à côté de C37.

### A-16, INFO, piste : 45 signataires, un seul compte de SOL
- **Preuve :** `work_A/a34_payout.py`, `a36_residual2.py`, `a37_svc.py`. Dans 3 826 transactions du programme `3GMsedVPsXjWR7HYUvwm1YUpvBC2bTgSkXixm4gMXnPk`, 45 signataires échangent, et le SOL arrive dans un compte WSOL de `4ToQp55myvfpeprgKuqGbDqyji9Ezm7CZg7QbcTpL33S`. Exemple : `5au4mKnXzBtp64qHbD1bJvNaqPYko38F8Mp7J7D7cwcobW6KdP9sXtvjai1r6xEnMe4eHFGeNEbrKvXv8gAVgZbW`, le signataire vend 12,1 M, le vault paie 623,46 SOL, le signataire reçoit 0,004 SOL. Acheté 14 635 SOL, vendu 14 645 SOL, réalisé 9 SOL, 85 achats pour 85 ventes pour le premier. 24 537 SOL, soit 3,1 % des achats, 2,4 % des 24 h avant S, aucun membre du groupe de 33, aucun wallet nommé.
- **Lecture :** service ou opérateur unique, je ne tranche pas. La règle « vu par au moins 15 wallets = service » l'exclut des liens, ce qui serait une erreur si c'est un opérateur. Le rapport dit « volume artificiel non testé » : ceci en est le point de départ.
- **Suite :** identifier ce programme avant toute conclusion.

### A-17, INFO : petits écarts sans effet
- R3 garde la capitalisation de S20 − 1 h au lieu de S20 − 2 h (`ana_10_table.py`).
- La ligne du sommet de `TIMELINE.md` lit le prix de la transaction, pas celui d'avant (74,73 M$ contre 73,82 M$). Les 31 autres lignes de capitalisation sont à moins de 2 % (`out/a20_time.txt`).
- C05, heure suivante : 5 377,61 SOL au rapport, 5 377,79 au vault, une transaction classée `internal`, `4ooY57RTxbFJuvwjRzXKTmApAcWWTKAYFRYcfpfJ3Zhes7J5PrxrZEa9f8AHoWPpYP8ExiVevS1bbBQFa6MMqnSE`.
- 46 601 transactions sur 50 pools n'ont qu'un vault qui bouge, de petits dépôts directs de WSOL au vault d'après l'échantillon, écartées en `sans_vault`. `4GKStivb` en a 36 682 sur 78 940.
- Pools tronqués : 135 `tronque_sans_pic` exclus par le plan, 64 des 212 du principal tronqués après leur pic, DMAGA compris.

### A-18, INFO : pas de donnée synthétique dans `etude_final/`
- **Preuve :** `work_A/a06_registre.py`, `a04_metrics.py`. Registre : 25 lignes, chaînage sha256 intact, 15 réelles, 10 synthétiques bien étiquetées (`ctl_01_synth.py`, avant le gel), 33 comparaisons réelles. 17 empreintes du gel relues, conformes. Tous les pools de `metrics.csv` sont des migrations réelles, base58. Aucune référence à `etude/` dans le code gelé. `swaps/*.parquet` identiques ligne à ligne à mon parseur pour 243 pools sur 243. 6 139 valeurs de mesures comparées, 1 écart : une mesure R3 d'un pool sans achat en 24 h, où mon code rend NaN au lieu de 0,00017, écart de mon côté.

### A-19, INFO : complétude de la collecte vérifiée
- **Preuve :** `work_A/a13_reconcile.py`, `a02_cursors.jsonl`, `a03_pools.jsonl`, `a40_migr.py`, `a22_fdv.py`.
  - Pool : 1 675 514 réussies listées, toutes dans `full_pool`, aucune en plus, aucune échouée. 1 731 495 lignes, soit 55 981 du chevauchement A-01.
  - Mint : 650 455 listées, toutes dans `full_mint` (2 de plus, postérieures à la liste). Courbe : 286 sur 286.
  - 1 069 tranches complètes, lus = curseur, aucun trou entre tranches, 1 chevauchement. Listes de signatures et `ctrl_tx` sans désordre (slot, index).
  - 13 920 `initialize2` sur 101 702 transactions du compte de migration, toutes retenues.
  - 245 pools `ctrl_tx` complets, filtres conformes, 0 rupture du vault WSOL, comptes de rejet identiques à `selection_counts.json`.
  - Bande principale : 213 pools, tous `retenu_superset`. Aucun `reporte_budget` n'y entre : l'amendement 001 ne touche pas le principal. Les pics S20 et S10 se recalculent sans écart sur 13 920 pools. Capitalisation relue sur DMAGA et 30 pools tirés au hasard : 0 écart au-delà de 0,1 %.

### A-20, INFO : pas de fuite temporelle trouvée
- **Preuve :** lecture à l'aveugle, puis reproduction. `compute` coupe à `t < S` en première ligne. Les fenêtres sont celles du plan : M1 24 fenêtres, M2 3 fenêtres, sans chevauchement. Le pic de DMAGA (19:00) précède la borne basse (19:03:27). Toutes les valeurs de `metrics.csv` se retrouvent avec un code qui ne lit rien après S. Le prix de bande précède S − 1 h. Reste un conditionnement léger : `truncated` dépend du total listé, y compris après S, seuls les 135 `tronque_sans_pic` en dépendent, et le plan le déclare.

### A-21, INFO : le brut correspond à la chaîne, et les heures sont en UTC
- **Preuve :** `out/a30_network.json`, `out/a20_time.txt`.
  - 236 transactions tirées au hasard : identiques au RPC, soldes et clés compris. 40 signatures échouées tirées dans `sigs_pool` : erreur, slot et heure conformes. 12 sur 12 identiques au RPC public, sans clé.
  - `EARLY_BUYERS.md` : 1 000 lignes, 0 écart de `blockTime`. 40 signatures horodatées dans `docs/` et `reports/` : 0 écart. Snowflakes des événements : conformes.
  - Toutes les conversions du code passent par `timezone.utc` ou `gmtime`, `viz/index.html` par `toISOString`. Je n'ai trouvé aucun reste de Lisbonne.

### A-22, INFO : parseur et échelle
- **Preuve :** `out/a13_reconcile.txt`, `a38_scale.py`. 782 391 couples (signature, propriétaire) : 778 117 égaux à mon parseur, 4 274 exactement doublés (A-01), 0 autre. Lignes de swap communes : 599 814, quantité égale partout, SOL égal à 2 lamports près sauf les 1 279 de A-02. 99,17 % du SOL a une quantité à 1 % du vault. Multi-bénéficiaires : 264 lignes, 450 SOL. Non-signataires : 18 % des lignes, 14,4 % du SOL. Versions : 1 644 525 v0, 35 v1, 1 054 554 legacy, clés = soldes partout. Instructions de transfert et soldes des vaults : 0 écart. Décimales : 6 partout. Comptes de l'autorité Raydium sur DMAGA : un seul pool v4.

## Tableau des recalculs

| Assertion | Valeur du rapport | Valeur recalculée | Écart | Script |
|---|---|---|---|---|
| C01 | slot 277417695, 02:05:25 UTC | identique, signataire `8YLEuUtZ` | 0 | a15 |
| C02 | environ 3 h 54 | 3 h 54 min 25 s (22:11:00), 3 h 53 min 52 s (22:11:33) | 0 | a20 |
| C05 | 3,29 / 145,44 / 5 377,61 SOL | 3,291 / 145,440 / 5 377,608, vault 5 377,788 | 0,18 SOL | a15, a32 |
| C06 | 13,18 / 84,94 SOL | 13,177 / 84,941 | 0 | a15 |
| C07 | 229,3, médiane 6,2, p 0,069 | 229,28, 6,18, 0,069 ; vault 236,56 | 0 | a25 |
| C08 | k 211, p 0,156, 33e | 211, 0,1557, 33e | 0 | a07, a04 |
| C11 | 217 M, 938 M, 23 % | 217,036 M, 938,0 M, 23,1 % | 0 | a23, a21 |
| C15 | 4 525 SOL, 2,4 %, 190 551 | 4 524,9, 2,38 %, 190 479,6 | 0,04 % | a23 |
| C21 | 5 491, 990 744 $, 1 087 $ | 5 490,86, 990 744 $, 1 086,77 $ ; cash 5 490,86 | 0 | a14, a15 |
| C21 | GXZvX 2 540 | 2 540,10 ; cash 2 516,34 | 0 (0,9 % en cash) | a14, a15 |
| C21 | 9PrmF8 1 748 | 1 747,80 ; cash 1 794,58 | 0 (2,7 % en cash) | a14, a15 |
| C23 | 796 883, 919 783, 2 699 114 | identiques ; 913 880 lignes uniques | 5 903 lignes | a11, a13 |
| C23 | 9 875 478, 6 624 533, 118 | identiques ; 83 % et 90 % d'échecs | 0 | a01 |
| C24 | 681 308 et 0, 681 300 et 1 (0,39) | identiques, 389 935 unités | 0 | a13 |
| C24 | 83 réserves, 215 309, 0 | identiques (côté DMAGA) | 0 | a18 |
| C25 | 1 087 contre 1 086, 844 k$, 48,5 SOL, 14,69 M | 1 086,77, capture relue ; 843 932 $ ; 48,5 ; 14,6988 M | 0 | a15 |
| C29 | 17, 310,8 M, 11,9 SOL | 17, 310,824 M, 11,916 SOL ; 0 échouée | 0 | a15 |
| C35 | 74 SOL | 74,17 | 0 | a14 |
| C35 | 631 364, 09:00 | 631 363,63, 09:01:46 | heure ronde | a15 |
| C35 | 18 367 sur 53 893 | 18 309 sur 53 893 | 58 wallets | a14 |
| C43 | 13 920, 84 jours | 13 920, 84 | 0 | a40, a10 |
| C44 | M1 à M7 et p | identiques à 1e-9, primaire entier | 0 | a04, a07 |
| C45 | 402, 6,1, p 0,036, 27 | 401,52, 6,06, 0,0357, 27 ; vault 507,93 | 0 | a25 |
| C50 | « surtout » | 22,1 % du SOL, 33 % des premiers financeurs | non établi | a19 |

## Assertions

Détail dans `audits/2026-11-03/work_A/claims_A.csv`.

- **Assertions A (15) :** 12 PASS (C01, C02, C05, C06, C21, C23, C24, C25, C26, C27, C29, C51), 3 FAIL (C34, C35, C50).
- **Autres testées :** PASS pour C07, C08, C10, C11, C14, C15, C28, C36, C40, C41, C42, C43, C44, C45, C47, C48 ; INCONCLUSIVE pour C30 et C49.
- **PASS avec réserve écrite :** C23 (A-01, A-07), C27 (A-05), C51 (A-13, A-16).

## Reproductibilité

Depuis la racine du dépôt, dans l'ordre : `a01`, `a02`, `a03` sous `scripts/guard.py --rss-mo 300`, puis les autres sous `audits/2026-11-03/tools/heavy.py`. Sorties dans `work_A/out/`, gros intermédiaires dans `audits_work/A/` (3,4 Go au total, chaque fichier sous 4 Gio). `a13_reconcile.py` et une première version de `a15_named.py` ont été tués par le garde à environ 1 Go : leur suite est `a13b_accounts.py`, et `a15_named.py` a été réécrit avec des tables sur disque. Rien n'a été écrit hors des deux dossiers autorisés.
