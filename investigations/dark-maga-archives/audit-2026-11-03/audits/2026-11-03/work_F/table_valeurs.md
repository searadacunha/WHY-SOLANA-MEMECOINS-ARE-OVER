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
