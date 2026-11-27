# Corrections appliquées après l'audit du 03/11

Agent F, 03/11/2026, branche `audit-2026-11-03`. Rien n'est committé : tout est dans l'arbre de travail. **Ces corrections ne sont pas auditées. L'enquête reste NON VALIDÉE.**

Dérivé corrigé : `/Volumes/VERBATIM HD/Dark-MAGA-Investigation/data_v2/`, 3 231 fichiers, 826 Mo, manifeste `evidence/DATA_V2_MANIFEST.tsv`. Commande de lecture : `DMAGA_BIG=<data_v2> scripts/py.sh ...`. Sans cette variable, les scripts lisent l'ancien dérivé, et ceux qui écrivent du dérivé s'arrêtent.

## 1. Code dérivé (partie B)

| Id | Fait | Fichiers | Vérification |
|---|---|---|---|
| K01 | Oui | `dmaga/db.py`, `scripts/nrm_10_trades.py` | `tests/test_k01_k03.py` (2 tests). 919 783 lignes deviennent 913 880, 796 883 signatures inchangées. 55 981 transactions hors tranche écartées à la normalisation, 2 699 114 lues, comme le curseur. Les 4 966 lignes coupées existent toutes dans la tranche suivante (`f00_checks.py`). `ana_19_export.py` passe par la même vue |
| K02 | Oui | `scripts/chk_90_selfcheck.py` | Sur l'ancien dérivé : 5 903 doublées, code 1. Sur `data_v2` : 0, code 0 |
| K03 | Oui | `dmaga/normalize.py` | `tests/test_k01_k03.py` (2 tests). `swap_other` avec un vault Raydium qui bouge : 1 708 chez D, 0 ici. `DswkYbBh` 4,41 SOL, estimation de D confirmée. Écart à la consigne : DMAGA n'a qu'un pool CPMM, contre un autre jeton et pas contre WSOL (`f01_gpmz.py`, 629 transactions sur 629). Sa réserve appariée `CEkWPZejSNbVyWpabrKxN5zd9H1p8GuqFSqzobvBq2Wx` reste comptée, sinon ces échanges passeraient pour de la liquidité |
| K04 | Oui, avec un ajout | `scripts/ana_20_pnl.py`, `scripts/nrm_11_accounts.py` (nouveau), `dmaga/pnl.py`, `tests/test_pnl.py` | 27 196 ruptures sur 1 168 comptes, comme D. `7gEQ6syD` 122,28 M sur flux, 0 ici. 502 wallets passent de complet à partiel. Ajout : le solde seul donnait 26,65 M à `6t2dz4jm`, vidé par un transfert connu des seuls flux. Ces transferts sont donc appliqués après le dernier solde vu. Somme 656,0 M, offre hors pools 567,8 M : le résiduel surestime encore de 88 M |
| K05 | **Non** | Aucun | Demande du réseau. Le plafond est publié au rapport : `dmaga_all` tronqué pour 20 wallets, recompté dans le brut |
| K06 | Oui | `scripts/ana_23_roundtrip.py` (nouveau), `scripts/rep_70_reports.py` | Plus de 50 % et 100 SOL ou plus : 103 wallets, 106 047,8 SOL, comme D. 2 de plus par programme propre (`AojsMucu`, `AzWs3s1W`). Ma règle de « programme propre » : au moins 80 % des lignes, au plus 5 propriétaires, 100 SOL ou plus. Elle n'est pas dans l'audit et reste à relire. L'étiquette ne touche ni `nodes.parquet` ni les liens. **`3GMsedVP` non identifié** : pas de réseau, aucune conclusion, `4ToQp55m` reste classé |
| K07 | Oui | `scripts/ana_30_flows.py` | Financements à 1 M de SOL ou plus : 1 130 avant, 0 après. Sorties : 5 000 avant, 0 après. Restent 3 financements de 100 000 à 150 000 SOL, aux montants ronds crédibles |
| K08 | Oui, autrement | `scripts/ana_30_flows.py` | 0 clé doublée. Écart à la consigne : les 214 paires de D ne sont presque jamais un doublon entre requêtes (38 seulement, `f00_checks.py`), ce sont deux virements d'une même transaction. Ils sont additionnés. Un simple dédoublonnage aurait perdu de l'argent. N13 ne bouge pas de ce fait |
| K09 | Oui | `scripts/chk_20_vault_chain.py`, `scripts/chk_21_venue_chain.py`, `scripts/nrm_10_trades.py` | `LIMIT` retiré. Côté WSOL : 40 réserves, 214 910 transactions, 22 ruptures, 1,23 SOL. Autorité CPMM exclue de ce côté |
| K10 | **Non** | Aucun | Demande du réseau. Écrit dans `reports/MISSING_EVIDENCE.md` |
| K11 | **En partie** | `scripts/ana_22_nodes.py`, `scripts/rep_70_reports.py` | Classe `service` faite : `cex` passe de 12 à 2 nœuds. **Filtre des mints du fichier Jupiter non fait : `dmaga/labels.py` est gelé par `etude_groupe`, `protocol_guard` a refusé l'édition. Je me suis arrêté sur ce point, sans contournement.** WSOL, USDC et ComputeBudget gardent une étiquette Jupiter dans `load()` : 0 effet mesuré, ce ne sont pas des propriétaires du graphe |
| K12 | Oui | `dmaga/hot_presume.py` (nouveau), `evidence/labels/hot_presume.tsv` (nouveau), `scripts/ana_60_clusters.py`, `scripts/ana_62_exits.py` | 7 adresses relues dans des sorties complètes (`f02_hot_presume.py`), hors de `labels.py`, jamais une étiquette vérifiée. Groupe de 33 identique : mêmes membres, mêmes 40 signatures |

Autres changements nécessaires :
- `dmaga/paths.py` : `DMAGA_BIG`, sans éditer `config.py`. `exige_v2()` empêche d'écraser l'ancien dérivé.
- `scripts/run_derive.sh` : `ana_21` passe avant `ana_20`, sinon un dossier neuf perd 22 853 transferts au PnL sans erreur. Seule sa syntaxe est testée (`zsh -n`) : le recalcul a été lancé étape par étape, sous le verrou.
- `scripts/rep_90_case.py` n'écrit plus `etude_final/results.md`, fichier gelé qu'il réécrivait à chaque lancement.
- `dmaga/frfmt.py` : « 0,032 SOL » sortait en « 0 032 SOL » dans le rapport du commit, et les nombres négatifs gardaient leur point. Corrigé.
- `scripts/ana_66_collector_local.py` (nouveau) et `reports/data_checks/rep72_reseau.json` (nouveau) : réponses réseau archivées, voir la section 3.
- `scripts/ana_70_audit_facts.py`, `dmaga/audit_txt.py` (nouveaux) : les chiffres de l'audit recalculés sur `data_v2`, et ses textes repris mot pour mot.

## 2. Rapport (partie A)

Vérification commune : `work_F/f08_controle.py` relit les rapports générés, 167 contrôles, 0 échec, `work_F/f08_controle.txt`. Il couvre aussi les lignes N01 à N17, l'encadré d'état sur les 6 rapports, l'absence de tiret cadratin et les formules à ne pas reprendre des audits. Il contrôle la présence des formules, pas la justesse du raisonnement.

| Id | Fait | Fichier généré, générateur | Ce qui est contrôlé |
|---|---|---|---|
| R01 | Oui | `CASE_REPORT`, `COORDINATION` ; `rep_90`, `rep_72` | Verdict mot pour mot, texte de la section 4.3 lu dans `AUDIT_FINAL.md`, retiré de H2 |
| R02 | Oui | Idem | « plomberie seulement », 2,4 ; 3,3 ; 7,5 % depuis `d11_scenarios.csv` |
| R03 | Oui | Idem | « copie neuve » absent, reproduction par A, B et D |
| R04 | Oui | `CASE_REPORT` | Trois phrases présentes |
| R05 | Oui | `CASE_REPORT`, `COORDINATION`, `ATTRIBUTION` | Expression seulement dans la liste des retraits, deux périmètres |
| R06 | Oui | Idem | N01, niveaux scindés, 12 wallets |
| R07 | Oui | Idem | Compte de dépôt niveau B, 31 sur 48, plancher, rafale non présentée comme unique |
| R08 | Oui | `CASE_REPORT`, `ATTRIBUTION` | N04, B pour 2025 |
| R09 | Oui | `CASE_REPORT`, `COORDINATION` | 2,4 ; 2,9 ; 37,3 ; 40,8 à 43,7 % |
| R10 | Oui, valeurs recalculées | `CASE_REPORT` | 42,4 ; 22,1 ; 20,6 ; 14,8 % ; 189, 184, 109 devenu 114, 4. Écart à D en section 4 |
| R11 | Oui | `CASE_REPORT`, `TOP_TRADERS`, `EARLY_BUYERS` ; `rep_90`, `rep_70` | 100,78 SOL, table par fenêtre, 3 premiers rangs retirés |
| R12 | Oui | `CASE_REPORT` | N12 |
| R13 | Oui, valeurs recalculées | `CASE_REPORT` | 09:01:46 ; 18 247 sur 53 960 ; 9 816. `CORRECTIONS.md` écrivait 18 309, sans K03 |
| R14 | Oui | `EARLY_BUYERS` | Deux tableaux séparés |
| R15 | Oui | `COORDINATION` | Colonnes « toute la vie » |
| R16 | Oui | `CASE_REPORT`, `COORDINATION` | 16,0 à 17,7 % |
| R17 | Oui | Idem | 34 wallets, 41 arêtes, recalculés |
| R18 | Oui | `CASE_REPORT`, `COORDINATION` | 11 à 12 sur 33, 11 `G41vRrsH`, repris de D |
| R19 | Oui | `CASE_REPORT` | 83,03 et 90,18 % |
| R20 | Oui | `CASE_REPORT`, `EARLY_BUYERS` | 508 SOL au vault |
| R21 | Oui | `CASE_REPORT`, `ATTRIBUTION` | 4 500 USDC, 7 397 559 jetons, « non vérifié » retiré |
| R22 | Oui, valeurs recalculées | `CASE_REPORT` | 93 522 SOL éq., 12 tronqués sur 65. **`CORRECTIONS.md` écrivait 175 427 et 14**, écart en section 4 |
| R23 | Oui | `CASE_REPORT`, `TOP_TRADERS` | 71 682 et 71 706 |
| R24 | Oui, valeurs recalculées | `CASE_REPORT` | 89,78 M et non 90,05 M |
| R25 | Oui | `CASE_REPORT` | Deux lignes de A-08, lues dans l'audit |
| R26 | Oui | `CASE_REPORT`, `COORDINATION` | 121 comparaisons, hors registre gelé |

Hors générateur : `reports/MISSING_EVIDENCE.md` n'a pas de script, édité à la main (encadré, ligne sur la traversée des échanges, K10). `scripts/rep_75_timeline.py` : une ligne, « rupture de traçabilité » retiré.

## 3. Réseau : ce qui n'a pas été lancé

| Script | Décision | Conséquence |
|---|---|---|
| `chk_63_group_edges.py` | **Non lancé**, il appelle `getTransaction` | Aucune sortie neuve. `reports/data_checks/group_edges_check.json` reste celui du 03/11 (40 relues, 40 directes). Ses 40 signatures sont identiques à celles de `data_v2` (`groupe_inchange` dans `audit_facts.json`) |
| `ana_65_collector.py` | **Non lancé**, fichier inchangé | `ana_66` ne rafraîchit que les champs locaux de `collector.json` |
| `ana_64_group_split.py` | Réseau retiré | Lit `g41` dans le `data/group_split.json` du dépôt |
| `rep_72_links.py` | Réseau retiré | Lit `rep72_reseau.json`, tiré par script des rapports du commit `01ae5a4` |

Le code de collecte retiré de `ana_64` et `rep_72` reste dans l'historique git. Relancer ces collectes demandera de le reprendre.

## 4. Valeurs : commit, D, final

| Chiffre | Commit 01ae5a4 | Valeur D | Finale, data_v2 | Écart final moins commit | Explication |
|---|---|---|---|---|---|
| Lignes de `trades.parquet` | 919 783 | 913 880 uniques | 913 880 | -5 903 | K01. K03 change le type de certaines lignes, pas leur nombre : même total que D |
| Lignes doublées retirées | 5 903 | 5 903 | 5 903 | 0 | Recomptées sur l'ancien fichier, en lecture seule |
| Signatures distinctes | 796 883 | 796 883 | 796 883 | 0 | Le filtre K01 ne doit retirer aucune transaction |
| C15, marché 24 h (SOL) | 190 551,17 | 190 532,13 ; 190 537,65 avec A-02 (estimation) | 190 546,47 | -4,70 | 12 lignes `swap_other` redeviennent des ventes, +14,34 SOL sur le dédoublonné. D répartissait selon le sens du vault (5,52) ; le parseur suit le sens du wallet. 0,008 % du marché, négligeable |
| C15, ventes du groupe (SOL) | 4 524,91 | 4 524,91 | 4 524,91 | 0,00 |  |
| C15, part du groupe (%) | 2,3746 | 2,3749 | 2,3747 | 0,0001 | Négligeable |
| C15, avec 3 destinataires (%) | absent | 2,886 | 2,886 |  |  |
| C35, réalisés positifs entrés après Musk | 18 367 | 18 309 ; 18 259 avec A-02 (estimation) | 18 247 | -120 | K01 et K03. Écart à l'estimation de D : 12, négligeable |
| C35, wallets entrés après Musk | 53 893 | 53 893 ; 53 968 avec A-02 (estimation) | 53 960 | 67 | K03 donne un premier achat à 67 wallets. Écart à l'estimation de D : 8, négligeable |
| C35, à plus de 0,1 SOL | absent | 9 885 ; 9 827 avec A-02 | 9 816 |  | Écart à l'estimation de D : 11, négligeable |
| C35, heure du sommet | 09:00 | 09:01:46 | 09:01:46 |  |  |
| C35, capitalisation au sommet (SOL) | 631 364 | 631,36 milliers | 631 364 | -0 |  |
| Réalisé du groupe de 33 (SOL) | 5 594,0 | 5 471,7 ; 5 469,8 avec A-02 | 5 469,8 | -124,2 | Estimation de D confirmée |
| Réalisé cumulé, tous wallets | 100 128,3 | 98 189,9 ; 97 278,3 avec A-02 | 97 163,1 | -2 965,2 | K01 et K03. Écart à l'estimation de D : 115 SOL, 0,12 % |
| Acheté, tous wallets | 790 223,1 | 787 071,7, doublons seuls | 788 489,3 | -1 733,8 | K01 retire 3 151 SOL, K03 rend 1 418 SOL à des swaps sans valeur. La valeur de D ne contient que K01 |
| Vendu, tous wallets | 785 853,8 | 782 244,1, doublons seuls | 784 000,8 | -1 853,0 | K01 retire 3 610 SOL, K03 rend 1 757 SOL. La valeur de D ne contient que K01 |
| Réalisé `ET8ZG5zA` | 359,14 | 203,63 | 203,63 | -155,51 |  |
| Réalisé `Akp46Dic` | 364,49 | 268,70 | 268,70 | -95,79 |  |
| Réalisé `C7i9beNH` | 404,55 | 378,01 | 378,01 | -26,54 |  |
| Réalisé `5FzhCSWL` | 144,58 | 187,91 | 187,91 | 43,33 |  |
| Réalisé `DswkYbBh` | 93,61 | 93,6 ; 4,4 avec A-02 (estimation) | 4,41 | -89,20 | Estimation de D confirmée |
| Réalisé `H3` | 5 490,86 | 5 490,86 | 5 490,86 | 0,00 |  |
| Réalisé `GX` | 2 540,10 | 2 540,10 | 2 540,10 | 0,00 |  |
| Réalisé `P9` | 1 747,80 | 1 747,80 | 1 747,80 | 0,00 |  |
| Réalisé `Q` | 74,17 | 74,17 | 74,17 | 0,00 |  |
| Top 100, communs avec l'ancien | 100 | 97 | 97 | -3 | entre 7uRDe43i rang 16, entre BBcYhznj rang 32, entre CQQqZgro rang 94 ; sort D4zVhwuU rang 98, sort 9Q2iQTt6 rang 99, sort CtXRQVs2 rang 100 |
| Top 10 identique | oui | oui | oui |  |  |
| C05, 19:03:27 à 19:23:20 (SOL) | 3,290 | 3,291 | 3,291 | 0,001 |  |
| C05, 19:23:20 à 19:30:13 (SOL) | 145,440 | 145,440 | 145,440 | -0,000 |  |
| C05, hors allers-retours (SOL) | absent | 100,78 | 100,78 |  |  |
| C05, heure suivante (SOL) | 5 377,61 | 5 377,608 ; +0,361 avec A-02 | 5 377,79 | 0,18 | K03. Égal à la valeur au vault de A-17. D estimait +0,361, le parseur donne +0,18 |
| C06, achats Biden à borne basse (SOL) | 13,18 | 13,177 | 13,18 | 0,00 |  |
| C06, ventes Biden à borne basse (SOL) | 84,94 | 84,941 | 84,94 | 0,00 |  |
| C41, sortie du groupe, base commune (%) | 22,5 | 37,3 | 37,3 | 14,8 | Ancienne valeur : swaps seuls |
| C41, autres, base commune, bas (%) | 35,0 | 40,8 | 40,8 | 5,8 | Ancienne valeur : swaps seuls |
| C41, autres, base commune, haut (%) | 35,0 | 43,7 | 43,7 | 8,7 | Ancienne valeur : swaps seuls |
| C50, part sans étiquette (%) | 67,8 | 42,5 | 42,4 | -25,4 | L'ancien parquet datait d'avant les étiquettes des exécutants DCA : 7 sources passent de sans étiquette à Jupiter. Sans lien avec K07 et K08 |
| C50, part pools (%) | 14,8 | 22,1 | 22,1 | 7,3 | Ancienne valeur : table de A-03, à ne pas reprendre |
| C50, part Jupiter (%) | 10,1 | 20,5 | 20,6 | 10,5 | Même cause |
| C50, part échanges (%) | 7,3 | 14,8 | 14,8 | 7,5 | Ancienne valeur : table de A-03, à ne pas reprendre |
| C50, premier financeur avant le mint, échange | absent | 189 | 189 |  |  |
| C50, premier financeur avant le mint, sans étiquette | absent | 189 | 184 |  | Même cause : 5 premiers financeurs changent de classe |
| C50, premier financeur avant le mint, Jupiter | absent | 109 | 114 |  | Même cause |
| C50, premier financeur avant le mint, service | absent | 4 | 4 |  |  |
| B-06, solde vu à S hors M6 (M) | 845,72 (achat brut, B) | 158,88 | 158,88 |  |  |
| B-06, stock à S hors M6 (M) | absent | 90,05 | 89,78 |  | D retirait une liste écrite à la main, sans le transfert caché de 0,267 M de `6t2dz4jm` : 69,09 M retirés et non 68,83 M |
| B-06, transferts 24 h, reçus (M) | 114,96 | 114,96 | 114,96 | -0,00 |  |
| B-06, transferts 24 h, nets (M) | absent | 76,3 | 76,3 |  |  |
| B-06, reçus par le groupe (M) | absent | 110,2 | 110,2 |  |  |
| Achats de l'heure de S (SOL) | absent | 2 762,2 | 2 762,2 |  |  |
| A-04, part des allers-retours (%) | 14,1 (A) | 13,52 | 13,50 |  | K03 ajoute des achats au dénominateur. Valeur de A sur une autre règle |
| A-04, 19:23:20 à 19:30:13, allers-retours (SOL) | absent | 44,66 | 44,66 |  |  |
| A-04, wallets à plus de 50 %, 100 SOL et plus | absent | 103 ; 106 047,8 SOL | 103 ; 106 047,8 SOL |  |  |
| C37, service non nommé (SOL éq.) | « beaucoup » | 175 427 | 93 522 |  | Sélection : `4ToQp55m` (82 194) et `7dY2yLDb` (612) sortent des 40 gagnants tracés, `7uRDe43i` (1 146) et `BBcYhznj` (1) entrent. Sur les 63 wallets communs : 92 621 avant, 92 375 après. Écart important, à lire avec la liste |
| C37, 6 échanges (SOL éq.) | 24 933 | 24 933 | 24 485 | -448 | OKX 16 (446) disparaît : K12 arrête la trace sur un hot présumé, le 3e saut n'existe plus |
| C37, wallets tronqués sur 65 | absent | 14 | 12 |  | Même effet de sélection |
| A-05, ruptures | absent | 27 196 | 27 196 |  |  |
| A-05, comptes touchés | absent | 1 168 | 1 168 |  |  |
| A-05, entrées + sorties (M) | absent | 2 845 | 2 845 |  |  |
| A-05, avant la borne basse (M) | absent | 84,737 | 84,737 |  |  |
| A-05, 24 h après Musk (M) | absent | 3,98 | 3,98 |  |  |
| A-05, somme des résiduels (M) | 937,1 | 937,1 sur flux | 656,0 | -281,1 | K04, plus les transferts vus par les seuls flux. Reste 88 M au-dessus de l'offre hors pools à la fin, 567,8 M : comptes non tracés jamais revus |
| C11, groupe à la borne basse (M) | 217,040 | 217,037 | 217,037 | -0,003 |  |
| C12, cœur 29 wallets (M) | 166,100 | 166,111 | 166,111 | 0,011 | Arrondi de l'ancien rapport |
| C12, sans 2 liens faibles (%) | absent | 16,0 | 16,0 |  |  |
| C13, 4 wallets (M) | 50,900 | 50,926 | 50,926 | 0,026 | Arrondi de l'ancien rapport |
| N06, série de 15 (M) | absent | 61,36 | 61,36 |  |  |
| N06, 48 expéditeurs (M) | absent | 92,08 | 92,08 |  |  |
| N06, union (M) | 260,4 élargis | 266,70 | 266,70 |  |  |
| N03, expéditeurs touchant DMAGA | absent | 31 sur 48 | 31 |  |  |
| N03, hors série et hors groupe | absent | 16 sur 33 | 16 sur 33 |  |  |
| C34, déjà acheteurs avant le visuel | absent | 107 des 183 ; 51 en 6 h | 107 des 184 ; 51 en 6 h |  | K03 donne un acheteur de plus. A écrivait 184, D 183 |
| R17, avec Habp5bnc : wallets, arêtes | 33 ; 40 | 34 ; 41 (C-07) | 34 ; 41 |  |  |
| C-10, jetons rachetés le 13/07/2025 | 7,40 M | 7 397 559 (C) | 7 397 559 |  |  |
| `token_edges`, arêtes | 108 057 | absent | 103 394 | -4 663 | 4 663 arêtes `gtba`, toutes avec un exécutant DCA : l'ancien parquet datait d'avant leur étiquette. 22 853 transferts au PnL des deux côtés, groupe de 33 identique |
| `funding_edges`, lignes | 216 130 | une ligne par clé | 215 178 | -952 | K08 : 0 clé doublée. Deux virements d'une même transaction s'additionnent au lieu de se perdre |
| Financements à 1 M de SOL ou plus | 1 130 | décimales fausses | 0 | -1 130 | K07 |
| Sorties SOL à 1 M de SOL ou plus | 5 000 | décimales fausses | 0 | -5 000 | K07 |
| `swap_other` avec un vault Raydium qui bouge | 1 708 | 1 708 | 0 | -1 708 | K03 |
| Nœuds `cex` | 12 | 10 à tort | 2 | -10 | K11. 4 passent en `service`, 6 exécutants DCA sortent du graphe faute d'arête |

**Écarts qui comptent :**
1. **C37, 175 427 devient 93 522 SOL éq.** Ce n'est pas une baisse des flux. `4ToQp55m` portait à lui seul 82 194 SOL éq. et sort des 40 gagnants tracés après la correction du PnL. Sur les 63 wallets communs : 92 621 avant, 92 375 après. Ce chiffre dépend donc de la liste, le rapport le dit. La phrase N16 de l'audit ne se lit plus telle quelle.
2. **C50, 42,5 et 20,5 deviennent 42,4 et 20,6 ; 189 et 109 deviennent 184 et 114.** L'ancien `funding_edges` n'étiquetait pas 7 sources (exécutants et escrow DCA), qui passent à Jupiter. L'antériorité de l'ancien parquet est déduite de ces étiquettes vides et des dates de fichiers.
3. **B-06, 90,05 devient 89,78 M.** D retirait une liste écrite à la main, qui oubliait un transfert caché de 0,267 M de `6t2dz4jm`.
4. **Estimations « avec A-02 » :** vraies valeurs données par le parseur. Réalisé du groupe et `DswkYbBh` : confirmés. Marché 24 h : 190 546,47 contre 190 537,65, 0,005 %. C35 : 18 247 sur 53 960 contre 18 259 sur 53 968. Réalisé cumulé : 97 163,1 contre 97 278,3.
5. **Inchangés :** H3QsBr, GXZvX, 9PrmF8, 5QhJJc, groupe de 33, 217,037 M, 40 arêtes, ventes de 24 h du groupe, top 10.

Le code n'a jamais été ajusté pour retomber sur une valeur de D. Détail : `work_F/f06_ecarts.txt`, `work_F/f07_edges.txt`.

## 5. Sorties finales des contrôles (03/11, 14:12 UTC)

`python3 ~/.claude/skills/etude-gelee/scripts/gel.py verifier etude_final`, code 0 :
```
protocole intact : 17 fichiers conformes au gel du 2026-11-02 23:47:06 UTC, 1 ajout(s), registre sous gels connus
```
`scripts/chk_90_selfcheck.py` sur `data_v2`, code 0 :
```
lignes de trades doublées : 0 (groupes 0)
références vérifiées: 1707, absentes des données: 0
garde : fini, code 0, pic 508 Mo
```
`scripts/chk_63_group_edges.py` : **non lancé, aucune sortie**, voir la section 3.

Tests, `scripts/py.sh -m pytest -q -p no:cacheprovider tests/test_normalize.py tests/test_pnl.py tests/test_k01_k03.py` :
```
22 passed in 5.05s
```
Contrôle de K02, fin de `log_05_manifests.txt`, `chk_90` lancé exprès sur l'**ancien** dérivé, sans `DMAGA_BIG` :
```
lignes de trades doublées : 5903 (groupes 5903)
références vérifiées: 1707, absentes des données: 7
code chk_90 ancien: 1
```
Ce code 1 est le résultat attendu : le contrôle doit échouer sur l'ancien fichier. Les 7 références absentes sont des programmes cités par les nouveaux rapports, connus du seul `owner_programs.parquet` de `data_v2`. Ce n'est pas une panne.

Autres : `work_F/f09_verify_v2.py` : 3 231 lignes, 3 231 fichiers, 0 non conforme. `gel.py verifier etude_groupe` : intact, 10 fichiers, seul son statut a été lu. Garde : aucun code 75, plus haut pic 972 Mo (`rep_75`).

## 6. `evidence/RAW_MANIFEST.tsv`

```
manifeste : 33033 lignes ; data/ avec empreinte : 3472 ; raw/ en taille seule : 29561 ; data/*.parquet à la racine : 8 sur 8 conformes
non conformes : 0
```
**Aucune ligne non conforme.** Limite : `raw/` n'est contrôlé qu'en taille, 91 Go sur un disque mécanique, et aucun de mes scripts n'y écrit. `git status` ne montre aucun changement sur `data/`, `etude_final/`, `dmaga/config.py`, `dmaga/collect.py`, `dmaga/helius.py`, `dmaga/labels.py`, `scripts/col_40_controls.py`, `JOURNAL_AGENTS.md`, `state/STATE.md`.

`reports/data_checks/venues.json` : `dis_05` a changé l'ordre de valeurs à égalité, `venues.load()` reste identique (83 venues). Octets du dernier commit remis, par copie.

## 7. Ce qui reste ouvert

**Décisions de Benjamin :** amendement 001, projet d'amendement 003, nouvel audit des conclusions, auditeurs à l'aveugle. Rien n'a été fait là-dessus.

**Non fait :**
- K05 et K10 : réseau.
- K11, filtre des mints : `dmaga/labels.py` gelé par `etude_groupe`.
- `3GMsedVP` non identifié.
- `chk_63` et `ana_65` non relancés.

**À relire au prochain audit :**
- La règle du programme propre de K06 et l'ajout à K04 sont de moi.
- Les exemples par virement de K08 s'écartent de la lettre de `CORRECTIONS.md`.
- La liste `hot_presume` vient d'une déduction de D. Elle classe 25 766 SOL éq., dont 25 511 pour un seul wallet.

**Limites :**
- Le résiduel surestime encore de 88 M sur l'offre hors pools.
- Des chiffres narratifs anciens, jugés PASS par l'audit (33 minutes, 7,1 M, 1 087 $, 844 k$...), restent écrits dans le gabarit, sans injection.
- `evidence/MANIFEST.sha256` n'est pas régénéré : `mk_manifest.py` réécrirait `RAW_MANIFEST.tsv`. `hot_presume.tsv` et `DATA_V2_MANIFEST.tsv` n'y figurent pas.
- Les liens de `data/` pointent toujours vers l'ancien dérivé. Basculer vers `data_v2` reste une décision à prendre.

**Hors de mon travail :** les résultats de l'enquête X et des flux des autres agents ne sont pas dans ces rapports, sur consigne du coordinateur.
