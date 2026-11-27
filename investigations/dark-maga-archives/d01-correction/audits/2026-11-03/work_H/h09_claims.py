"""Écrit CLAIM_VERIFICATION_V2.csv : état des assertions sur le rapport corrigé, commit b280ed4."""
import csv
from collections import Counter
from pathlib import Path
A = Path("audits/2026-11-03")
V1 = list(csv.DictReader(open(A / "CLAIM_VERIFICATION.csv")))
H = "work_H/"
# id : (verdict, valeur_rapport, valeur_verifiee, preuve, correction)
U = {
"C01": ("PASS", "02:05:25, slot 277417695, signature et créateur", "première ligne du créateur à 14/07/2024 02:05:25, slot 277417695, seul acheteur du slot ; signature reprise de D", H+"h05_misc.txt", "aucune"),
"C02": ("PASS", "environ 3 h 54", "14 065 s depuis 22:11:00, 14 032 s depuis 22:11:33 de A ; heure de Butler non revérifiée, écrit au rapport", H+"h01_recalc.txt", "aucune"),
"C03": ("PASS", "compte du 11/06/2024 ; thread cité", "joined Tue Jun 11 16:25:03 +0000 2024 ; le verdict D de X_FOLLOWUP sur « deux jours avant Butler » manque au rapport", H+"h08_assertions.txt ; work_E/X_FOLLOWUP.md partie 5", "D14 : ajouter D, contredit par les dates lues"),
"C04": ("PASS", "19:03:27 à 19:30:13 ; image 19:23:20", "archive twitter.com_20240721190327.html présente ; snowflake de l'avatar 19:23:20 ; id de 19:30:13 égal à la frise", H+"h02_tables.txt ; h08_assertions.txt", "aucune"),
"C05": ("PASS", "3,29 ; 145,44 ; 100,78 ; 5 377,79", "3,291 ; 145,440 ; 44,66 d'allers-retours par code propre, 100,78 ; 5 377,788", H+"h01_recalc.txt ; h08_assertions.txt", "aucune"),
"C06": ("PASS", "13,18 ; 84,94 ; 1,29 h", "13,177 ; 84,941 ; 1,291 h", H+"h01_recalc.txt", "aucune"),
"C07": ("PASS", "229,3 ; 6,2 ; p 0,069 ; 236,56 au vault", "229,28 ; 6,18 ; 2/29 = 0,069 ; 236,56", H+"h01_recalc.txt ; h02_tables.txt", "D22 : retirer « inhabituel » de H2 ou le qualifier"),
"C08": ("PASS", "non distinguable, k 211, 0,156, 33e", "verdict.json mot pour mot ; k 211 ; M6 0,1557 ; 32 pairs au-dessus", H+"h02_tables.txt", "aucune"),
"C09": ("PASS", "absence d'anomalie non probante, table de puissance", "phrase présente, d11_scenarios.csv relu, simulation non relancée", H+"h06_divers.txt", "aucune"),
"C10": ("PASS", "33 wallets, 40 transferts, relus ; seuil choisi après coup ; Habp5bnc", "40 lignes de token_edges, 40 signatures, 37 paires ; group_edges_check.json n = 40, relectures du 03/11 non refaites", H+"h08_assertions.txt", "aucune"),
"C11": ("PASS", "217 M, 23 % de 938 M", "217,037 M ; 937,765 M ; 23,14 %", H+"h01_recalc.txt", "aucune"),
"C12": ("PASS", "29 wallets, 166,1 M, 16,0 à 17,7 %", "166,111 M ; 149,711 M ; 15,96 et 17,71 %", H+"h01_recalc.txt", "D04 : dire de quoi B est le niveau"),
"C13": ("PASS", "4 wallets, 50,9 M", "50,926 M", H+"h01_recalc.txt", "aucune"),
"C14": ("PASS", "15 des 33", "15, 206,87 M, 52,27 SOL", H+"h01_recalc.txt", "aucune"),
"C15": ("PASS", "4 525 ; au moins 2,4 % de 190 546 ; 2,9 % avec 3 destinataires", "4 524,91 ; 190 546,47 ; 2,3747 % ; 973,33 ; 2,886 %", H+"h01_recalc.txt ; h10_reste.txt", "D21 : écrire 973,3 SOL à côté de 2,9 %"),
"C16": ("PASS", "0,032 SOL, 35 s", "0,032 et 35 s dans group_edges_check.json", H+"h08_assertions.txt", "aucune"),
"C17": ("PASS", "16:11:24 à 16:14:34, 190 s ; 15 wallets en 2 rafales", "15 versements le 26/01/2025 dans g30_in.csv, 14 lignes au tableau de COORDINATION, Cv3p9Wu1 à 17:21:56 manque", H+"h10_reste.txt", "D32 : compléter le tableau"),
"C18": ("PASS", "48 expéditeurs, 94,5 %, plancher, 100 % avec 6 adresses", "48 ; 94,46 % ; 956,52 SOL", H+"h02_tables.txt ; h08_assertions.txt", "D19 : retirer l'argument des frais"),
"C19": ("PASS", "niveaux scindés", "A, B sur le créateur et 12 wallets, C pour les 33 et un même bénéficiaire, écrits dans CASE_REPORT et ATTRIBUTION", "docs/CASE_REPORT.md:14 ; reports/ATTRIBUTION.md:21-25", "aucune"),
"C20": ("PASS", "sans lien par transfert direct", "0 arête de jetons, 0 arête de lien avec les 33 ni entre eux", H+"h08_assertions.txt", "D30 : ATTRIBUTION écrit « rien ne le soutient », à accorder avec G7"),
"C21": ("PASS", "5 491 ; 990 744 $ ; 1 087 $ ; 2 540 ; 1 748", "5 490,86 ; 990 743,77 ; 1 086,77 ; 2 540,10 ; 1 747,80", H+"h01_recalc.txt", "aucune"),
"C22": ("PASS", "aucun lien, aucune adresse du noyau", "dans le corpus lu, le noyau ne publie que le mint et le pool ; 0 arête wallet_revendique ; corpus partiel écrit", H+"h08_assertions.txt", "aucune"),
"C23": ("PASS", "796 883 ; 913 880 ; 2 699 114 ; 1 130 194 ; 118 ; 71 706", "mêmes valeurs ; 0 doublon ; 83,03 et 90,18 % relus dans le journal de A", H+"h01_recalc.txt ; h08_assertions.txt", "aucune"),
"C24": ("PASS", "0 sur 681 308 ; 1 sur 681 300 ; 83, 215 309, 0 ; 40, 214 910, 22, 1,23 SOL", "valeurs identiques dans vault_chain.json et venue_chain.csv", H+"h06_divers.txt", "aucune"),
"C25": ("INCONCLUSIVE", "1 087 contre 1 086 ; 844 k$ ; 48,5 SOL et 14,69 M", "partie recalculée juste : 1 086,77 ; 844 k$ à 13:38:12 ; 48,5 ; 14,6988 M, tronqué. Lecture des captures et du post non refaite", H+"h01_recalc.txt ; h06_divers.txt", "aucune"),
"C26": ("PASS", "97 ruptures comblées, tranche recouvrant 5 h 36", "journal derive.out présent ; 0 doublon sur data_v2 ; 4 966 lignes doublées sur l'ancien dans audit_facts", H+"h08_assertions.txt", "aucune"),
"C27": ("PASS", "coût moyen, frais exclus, limites, 20 tronqués", "20 wallets dmaga_all tronqués recomptés", H+"h06_divers.txt", "aucune"),
"C28": ("PASS", "33 min, Coinbase 3, 0,5 SOL, 7,1 M pour 0,2 SOL", "7,106 M pour 0,2012 SOL ; 0 vente par swap avant 2025", H+"h05_misc.txt", "aucune"),
"C29": ("PASS", "créateur seul au slot ; 17, 310,8 M, 11,9 SOL", "1 ; 17 ; 310,824 M ; 11,916 SOL", H+"h05_misc.txt", "aucune"),
"C30": ("PASS", "13 virements, 7 sans achat, 2 à 65 min", "tableau de COORDINATION recompté : 13 de 01:46:23 à 02:03:38, 7 non, 11 dans le groupe ; 65 min 44 et 65 min 17 ; brut lu par D", "reports/COORDINATION.md:96-108,120-121", "aucune"),
"C31": ("FAIL", "CASE_REPORT corrigé : @FrancoAppr 16:00:59. EARLY_BUYERS : « plus ancienne image identique » pour @ChrisWinig", "pHash 0 chez @FrancoAppr à 16:00:59, 90 s avant @ChrisWinig", "reports/EARLY_BUYERS.md:5 ; "+H+"h06_divers.txt", "D03 : corriger EARLY_BUYERS et TOP_TRADERS"),
"C32": ("FAIL", "CASE_REPORT corrigé : image retrouvée. EARLY_BUYERS : « média perdu » à 16:00:08", "image retrouvée d'après X_FOLLOWUP partie 2, non relue ici ; contradiction interne vérifiée", "reports/EARLY_BUYERS.md:6 ; docs/CASE_REPORT.md:36", "D03"),
"C33": ("FAIL", "@koreanjewcrypto dès le 15/07, @kanpai dès le 16/07", "@koreanjewcrypto 15/07 16:56:29 juste ; @kanpai 15/07 22:56:01 d'après la métadonnée et l'id d'origine", H+"h03_small.txt ; h10_reste.txt", "D09"),
"C34": ("PASS", "cohortes de premier achat ; 107 des 184, 51 en 6 h ; deux tableaux", "184 ; 107 ; 51", H+"h08_assertions.txt", "aucune"),
"C35": ("PASS", "74 SOL ; 631 364 à 09:01:46 ; 18 247 sur 53 960 ; 9 816", "74,17 ; 76,26 M sortis ; 631 363,6 à 09:01:46 ; 18 247 ; 53 960 ; 9 816", H+"h01_recalc.txt ; h08_assertions.txt", "D12 : « tête » oublie le rang 3"),
"C36": ("PASS", "11 à 12 sur 33 ; 11 G41vRrsH", "11 lignes « oui » au tableau ; group_split.json 11 et 10 sur 32 ; le passage à 33 vient de D", H+"h08_assertions.txt", "aucune"),
"C37": ("PASS", "Bybit 2 8 523 ; Binance 1 8 051 ; Coinbase 3 3 284 ; Coinbase 1 2 589 ; Coinbase 2 2 038 ; 12 tronqués sur 65 ; 93 522 ; 24 485", "mêmes valeurs depuis exit_summary.json", H+"h01_recalc.txt", "D26 : dire que 25 511,5 des 25 765,7 viennent d'un wallet"),
"C38": ("PASS", "composante large sans propriétaire unique", "345 wallets au premier rang de wallet_clusters ; phrase présente", H+"h08_assertions.txt", "aucune"),
"C39": ("INCONCLUSIVE", "scénario le plus simple sans H2, écrit comme jugement ; lien non établi", "jugement non calculable. Le test gelé n'y sert plus d'appui", "docs/CASE_REPORT.md:67", "D05 : intégrer le comparatif à H3"),
"C40": ("FAIL", "le groupe ne trade pas entre le visuel et la bascule", "vrai depuis 16:00:59 et 16:02:29 : 0 ligne. Faux depuis 12:50:45, plus ancienne image de la composition au même rapport : 3 ventes de 7mdCAs8C, 12,34 SOL, de 13:26:46 à 14:01:34, 5 transferts", H+"h01_recalc.txt", "D03 : nommer la borne"),
"C41": ("PASS", "37,3 % contre 40,8 à 43,7 % ; 22,5 contre 35,0 signalé asymétrique", "37,28 ; 40,78 ; 43,70 ; 22,49 ; 34,95 ; 110 détenteurs, 643,6 M", H+"h10_reste.txt", "aucune"),
"C42": ("FAIL", "gestes du groupe avant le visuel, 07:57-08:33 et 14:22-14:25", "heures justes. 14:22-14:25 est 1 h 31 après 12:50:45, donc pas « avant le visuel » au sens de l'essentiel 10. 26,0 M et non 25,5 M", H+"h05_misc.txt ; reports/COORDINATION.md:84", "D03, D11"),
"C43": ("PASS", "13 920 ; 84 jours", "13 920 par somme des compteurs ; 84", H+"h02_tables.txt ; h08_assertions.txt", "aucune"),
"C44": ("PASS", "M1 à M7", "mesures, médianes et p recalculés depuis metrics.csv, identiques", H+"h02_tables.txt", "aucune"),
"C45": ("PASS", "402 ; 508 au vault ; 6,1 ; 0,036 ; 27", "401,52 ; 507,93 ; 6,06 ; 1/28 ; 27", H+"h01_recalc.txt ; h02_tables.txt", "D22 : « bien réveillé » à retirer"),
"C46": ("INCONCLUSIVE", "0,08, médiane 0, p 0,073, k 40, écrit non recalculable", "funder_share.json relu ; réponses réseau non gardées", H+"h02_tables.txt", "aucune"),
"C47": ("PASS", "33 comparaisons, 0,00152, M3 et M4 ne peuvent pas ouvrir", "registre.py compter : 33 et 0,00152", "registre.py compter etude_final", "D17 : ajouter le compte hors registre"),
"C48": ("PASS", "pics tardifs, mesures après DMAGA, A-08", "phrases présentes ; A-08 repris de A, non refait", "docs/CASE_REPORT.md:92,98", "D17 : étiqueter ces p"),
"C49": ("PASS", "plomberie seulement, 2,4 ; 3,3 ; 7,5 ; pas de copie vierge", "17 empreintes sur 17 recalculées, gel du 02/11 23:47:06", H+"h02_tables.txt", "aucune"),
"C50": ("PASS", "42,4 ; 22,1 ; 20,6 ; 14,8 ; 189, 184, 114, 4 ; borne basse", "42,44 ; 22,14 ; 20,55 ; 14,80 ; 189, 184, 114, 4 ; 1 316 494 SOL", H+"h01_recalc.txt", "aucune"),
"C51": ("PASS", "services retirés des liens", "aucune arête de link_edges vers un nœud non wallet", H+"h08_assertions.txt", "aucune"),
"N01": ("PASS", "13 sur 2 201 ; 2 188 ; 507 s", "cb_window 2 517 lignes, 2 201 destinataires, 13 dans les 48 expéditeurs, 01:32:23 à 01:40:50 ; CV 0,245 ; P 5e-05 repris de D", H+"h08_assertions.txt ; h02_tables.txt", "D08 : étiqueter P et le témoin exploratoires ; D30 : relier à 14"),
"N02": ("PASS", "compte de dépôt, niveau B", "sorties reprises de D, g30_in cohérent. L'argument des 155 000 lamports est réfuté par FLOW_BOUNDARIES section 8", "work_G/FLOW_BOUNDARIES.md:223,240", "D19"),
"N03": ("PASS", "31 sur 48 contre 8 sur 1 365", "31 recalculé ; 1 365 dans d43_perim.txt", H+"h08_assertions.txt", "D08"),
"N04": ("PASS", "écart exact 100 000 lamports, B pour 2025", "ligne de d21_match.txt relue, réseau non relancé", H+"h08_assertions.txt", "aucune"),
"N05": ("PASS", "créateur hors des 33, 0 échange", "0 arête dans token_edges", H+"h08_assertions.txt", "aucune"),
"N06": ("PASS", "217,04 ; 61,36 ; 92,08 ; 266,70 ; 28,4 %", "217,037 ; 61,357 ; 92,079 ; 266,697 ; 28,44 %", H+"h01_recalc.txt", "aucune"),
"N07": ("PASS", "2,89 % ; 37,3 contre 40,8 à 43,7", "2,886 ; 37,28 ; 40,78 ; 43,70", H+"h10_reste.txt", "aucune"),
"N08": ("PASS", "2,4 ; 2,4 ; 3,3 ; 100 ; 3,3 ; 7,5", "2,36 ; 2,36 ; 3,3 ; 100,0 ; 3,3 ; 7,52 dans d11_scenarios.csv, simulation non relancée", H+"h06_divers.txt", "aucune"),
"N09": ("PASS", "texte gelé accompagné", "mot pour mot avec AUDIT_FINAL section 4.3 ; centiles 83,4 ; 82,0 ; 76,3 ; 45,5 ; 73,9 ; 84,8 ; 82,5", H+"h02_tables.txt", "aucune"),
"N10": ("PASS", "13,5 % ; 30,7 % ; rangs 1 à 3", "106 254,0 sur 787 109,5 par code propre ; 44,66 sur 145,44 ; 32 832,7, 16 739,8, 12 869,3", H+"h08_assertions.txt", "aucune"),
"N11": ("PASS", "5 903 ; 5 469,8 et non 5 594,0 ; top 100 à 3 lignes", "5 903 sur l'ancien fichier ; 5 469,82 ; top 100 repris de audit_facts", H+"h08_assertions.txt ; h01_recalc.txt", "aucune"),
"N12": ("PASS", "27 196, 1 168, 2 845 M, sauf 84,7 M déjà compensés", "27 196 ; 1 168 ; 1 508,5 + 1 336,9 ; 84,737 dont 84,537 pour AtZjv3Du ; 15 à cheval, 1,01 M, non écrits", H+"h01_recalc.txt", "D27"),
"N13": ("PASS", "42,4 ; 22,1 ; 20,6 ; 14,8", "voir C50", H+"h01_recalc.txt ; h04_choix.txt", "aucune"),
"N14": ("PASS", "83,03 et 90,18 %", "8 199 964 sur 9 875 478 ; 5 974 078 sur 6 624 533 dans a01_sigs.log", H+"h08_assertions.txt", "aucune"),
"N15": ("PASS", "26/06/2024 et 23/08/2024", "lignes de d20_series.txt relues", H+"h08_assertions.txt", "aucune"),
"N16": ("PASS", "93 522 contre 24 485", "93 521,6 ; 24 485,4", H+"h01_recalc.txt", "aucune"),
"N17": ("PASS", "89,78 M ; 76 ; 76,3 nets ; 110,2 sur 114,96", "89,783 ; 76 ; 76,299 ; 110,2 ; 114,955 ; 2 762,2 SOL. « dont » est mal placé : 110,2 n'est pas une part de 76,3", H+"h01_recalc.txt", "D27 : reformuler"),
}
NEW = [
("X01", "Le thread d'@Aristos_Revenge écrit que @kikisknees a lancé @DarkMagaCoin et les pfp deux jours avant Butler (essentiel 1, Q1)", "INCONCLUSIVE", "citation, C ; compte du 11/06/2024", "présence seule, thread lu par Thread Reader ; X_FOLLOWUP donne D, contredit", "docs/CASE_REPORT.md:10,34 ; work_E/X_FOLLOWUP.md:145", "D14"),
("X02", "@XHEILIGX publie l'adresse de 9PrmF8 le 30/03/2024, 106 jours avant le mint, indice C (essentiel 7)", "INCONCLUSIVE", "30/03/2024, 106 jours, C", "date de l'id 30/03/2024 02:01:36 et 106,0 jours recalculés ; contenu du post non relu", H+"h10_reste.txt", "aucune"),
("X03", "@kikisknees, 21/07 12:50:45, plus ancienne image connue de la composition, pHash 14 (essentiel 10, Q2)", "INCONCLUSIVE", "12:50:45, pHash 14, A", "date de l'id recalculée ; image et pHash non relus", H+"h10_reste.txt ; docs/TIMELINE.md:24", "aucune"),
("X04", "@FrancoAppr 16:00:59 et @ChrisWinig 16:02:29, images identiques à l'avatar, 90 s d'écart", "PASS", "16:00:59, pHash 0, 90 s", "visual_new.csv : 1024 x 1024, pHash 0, dHash 0 ; 90 s", H+"h06_divers.txt ; h01_recalc.txt", "aucune"),
("X05", "@GreatBambin0 15:58:21, plus ancien envoi connu de la variante à Musk", "INCONCLUSIVE", "15:58:21, A", "date et 900 x 900, pHash 16 lus ; variante par l'œil non relue", H+"h06_divers.txt", "aucune"),
("X06", "@kikisknees à Musk le 18/07 22:22:13 : « We are building an army for you for that purpose. $DMAGA »", "INCONCLUSIVE", "18/07 22:22:13", "date de l'id égale ; texte présent dans la frise, brut non relu", "docs/TIMELINE.md:21", "aucune"),
("X07", "L'image de 16:00:08 est le Trump « dark maga », même sha256", "INCONCLUSIVE", "A", "présence seule", "docs/CASE_REPORT.md:36", "aucune"),
("X08", "Réponses de @kikisknees à Musk à 18:46:37 et 18:55:15, médias perdus (Q3, frise)", "FAIL", "médias perdus", "18:46:37 : image GTCEEQ2WoAAm65s présente dans work_E, pHash 0 avec la référence V3, A dans X_FOLLOWUP lignes 45 et 233. 18:55:15 : rien trouvé", H+"h08_assertions.txt", "D10"),
("X09", "@kanpai, frise, 16/07/2024 00:14:58", "FAIL", "16/07 00:14:58, 556 k$", "id de repost ; original 15/07 22:56:01 ; capitalisation 667 k$ à cette heure", H+"h02_tables.txt ; h06_divers.txt", "D09"),
("X10", "Frise : une date de post vient de son identifiant ; dans tous les cas lus, elle égale la métadonnée", "FAIL", "tous les cas lus", "372 lignes sur 5 155 diffèrent", H+"h02_tables.txt", "D09"),
("X11", "Corpus partiel : 30 recherches, 1 249 textes, 1 306 et 379 posts restants (Q3)", "PASS", "30 ; 1 249 ; 1 306 ; 379", "30 lignes ; 1 419 moins 170 ; table relue. Omis : 20, 54, 8 et 11 restants", H+"h06_divers.txt ; work_E/X_FOLLOWUP.md:76-82", "D24"),
("X12", "@twicrates écrit le 23/07 « i was sent some » (Q9)", "INCONCLUSIVE", "23/07, C", "date de l'id 23/07 22:17:15 ; texte non relu", H+"h10_reste.txt", "aucune"),
("X13", "@kikisknees revendique « pfp by me and @ChrisWinig », « made the first one » du 22/07 (Q2)", "INCONCLUSIVE", "A pour le post, C pour le contenu", "présence seule", "docs/CASE_REPORT.md:36", "aucune"),
("X14", "Cela établit une campagne publique visant Musk (essentiel 10)", "FAIL", "établit", "X_FOLLOWUP : traces publiques, aucune n'établit un plan de l'équipe ; H1 reste B", "work_E/X_FOLLOWUP.md:84", "D06"),
("X15", "Texte de @kikisknees récupéré pour 208 posts, Wayback refuse la suite (MISSING_EVIDENCE)", "FAIL", "208 et 17", "1 249 textes de plus au 03/11, écrit en Q3", "reports/MISSING_EVIDENCE.md:9 ; docs/CASE_REPORT.md:38", "D13"),
("X16", "Fenêtres avant_pmarca et pmarca_a_winig de EARLY_BUYERS", "FAIL", "borne 20/07 21:47:23", "la frise corrige en 20:46:54 ; events.json et windows.csv gardent l'id de repost", H+"h05_misc.txt", "D31"),
("G01", "Caw4Rrwk reçoit 590 933,95 USDC et 35,63 SOL de 55 expéditeurs, dont 27 des 48 de 9W9b (essentiel 8)", "PASS", "590 933,95 ; 35,63 ; 55 ; 27", "valeurs identiques dans g30_in.csv, brut hors de mon angle", H+"h02_tables.txt", "aucune"),
("G02", "14 et non 13 des 2 201 destinataires reversent à l'un des deux dépôts, tous dans les 507 s", "PASS", "14", "10 vers Caw4, 13 vers 9W9b, 14 en union ; Fp6kgqHU est le 14e ; sorties de g66", H+"h02_tables.txt ; work_G/g66.txt", "D30"),
("G03", "Le périmètre du créateur vend surtout par DCA : 47 ordres, 113,37 M, 1 292,4 SOL éq.", "PASS", "47 ; 113,37 ; 1 292,4", "valeurs identiques dans g52_orders.csv", H+"h03_small.txt", "aucune"),
("G04", "Il s'arrête à 86,6 % sur les deux dépôts", "PASS", "86,6 %", "3 138,6 sur 3 626,0 depuis flow_boundaries.csv", H+"h10_reste.txt", "D21"),
("G05", "Une seule jonction par dépôt hors des 2 de la série : 4 wallets, 31,9 SOL, le 23/07/2024", "PASS", "4 ; 31,9", "7,9 + 8 + 8 + 8", H+"h02_tables.txt", "aucune"),
("G06", "Les 33 : 76 ordres deBridge, 1 018 687 USD (essentiel 9)", "FAIL", "76 ; 1 018 687", "76 lignes pour toutes les sources, somme 1 023 933,51 ; 33 : 68 ordres, 979 324,28 USD. 1 018 687,18 n'existe que dans la prose de work_G", H+"h02_tables.txt ; h06_divers.txt", "D01"),
("G07", "Ponts 44,5 % des SOL éq. tracés des 33, dépôts Coinbase 1,4 %", "FAIL", "44,5 ; 1,4", "valeurs de P2, qui n'est pas les 33. Sur les 33 exacts : 5 468,8 sur 12 133,8, 45,1 % ; 165,7, 1,4 %", H+"h03_small.txt", "D01"),
("G08", "C73Yv9iH envoie 496 372 USD vers un même receveur dès 22:53:42 le 21/07/2024", "PASS", "496 372", "27 ordres, 496 371,60 USD, jusqu'au 09/06/2025", H+"h02_tables.txt", "D28"),
("G09", "Ei5yGz8d, Gcyg2jeL, HGBiExZR : même receveur, 263 573 USD en 9 min 36 s", "PASS", "263 573 ; 9 min 36 s", "4 ordres, 263 573,16 USD, 00:54:36 à 01:04:12 ; nature du receveur non vérifiée", H+"h02_tables.txt", "aucune"),
("G10", "Deux wallets de la série donnent 1,5 M et 1 M à deux wallets qui versent aux dépôts de GXZvX, C", "PASS", "1,5 M ; 1 M", "2 lignes de token_edges ; suite reprise de g48 et g49", H+"h10_reste.txt", "aucune"),
("G11", "9PrmF8 partage H9Xezqfd avec 9 wallets, 8 sur 10 touchent DMAGA", "PASS", "9 ; 8 sur 10", "10 expéditeurs, 8 dans accounts.parquet", H+"h10_reste.txt", "aucune"),
("G12", "3GMsedVP : 1 913 blocs, 3,12 % des achats, marge 194,85 SOL, aucun lien", "PASS", "1 913 ; 3,12 % ; 194,85", "1 913 dans g53.txt ; 24 537,38 sur 787 109,5 = 3,12 %. TOP_TRADERS écrit « non identifié »", H+"h10_reste.txt ; h08_assertions.txt", "D18"),
("G13", "Témoin : au plus 4 communs sur 7 140 paires", "PASS", "4 ; 7 140", "g31 : maximum 4, 0 à 5 ou plus. Limites SOL, 3 pages, USDC en face, non écrites", H+"h10_reste.txt", "D08"),
("G14", "Les 33 sortent d'abord par des ponts, pas par Coinbase (titre)", "FAIL", "pas par Coinbase", "table arrêtée au premier saut : 29,0 % wallets sondés et 21,0 % non suivis, destination inconnue", H+"h03_small.txt ; work_G/FLOW_BOUNDARIES.md:190", "D02"),
("G15", "Une sortie commune en salves de moins de 3 minutes soutient le niveau B des 29 (COORDINATION)", "FAIL", "sortie commune", "salves du dépôt : 2 des 33 le 23/07, 2 le 26/01. L'essentiel 8 écrit « chacun leur sortie »", "reports/COORDINATION.md:79,160-177 ; docs/CASE_REPORT.md:17", "D04"),
]
cols = ["id", "assertion", "verdict", "verdict_A", "verdict_B", "verdict_C", "valeur_rapport", "valeur_verifiee", "preuve", "correction_requise", "verdict_v1"]
out = []
for r in V1:
    v = U[r["id"]]
    out.append({"id": r["id"], "assertion": r["assertion"], "verdict": v[0], "verdict_A": r["verdict_A"], "verdict_B": r["verdict_B"], "verdict_C": r["verdict_C"], "valeur_rapport": v[1], "valeur_verifiee": v[2], "preuve": v[3], "correction_requise": v[4], "verdict_v1": r["verdict"]})
for i, a, ve, vr, vv, p, c in NEW:
    out.append({"id": i, "assertion": a, "verdict": ve, "verdict_A": "non couvert", "verdict_B": "non couvert", "verdict_C": "non couvert", "valeur_rapport": vr, "valeur_verifiee": vv, "preuve": p, "correction_requise": c, "verdict_v1": "absent"})
assert all(r["id"] in U for r in V1) and len(V1) == 68
with open(A / "CLAIM_VERIFICATION_V2.csv", "w", newline="") as f:
    w = csv.DictWriter(f, cols); w.writeheader(); w.writerows(out)
print("lignes", len(out), Counter(r["verdict"] for r in out))
for pre in "CNXG":
    print(pre, Counter(r["verdict"] for r in out if r["id"].startswith(pre)))
print("changés", [(r["id"], r["verdict_v1"], r["verdict"]) for r in out if r["verdict_v1"] != r["verdict"] and r["verdict_v1"] != "absent"])
txt = (A / "CLAIM_VERIFICATION_V2.csv").read_text(); assert "—" not in txt and "–" not in txt
