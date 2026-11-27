# Audit final D : confrontation des audits A, B, C

Auditeur D, 03/11/2026. Commit de référence `01ae5a4`. Token `7D7BRcBYepfi77vxySapmeqRNN1wsBBxnFPJGbH5pump`. Personne n'est accusé. Aucune identité civile n'est présumée. Un wallet cité n'est mis en cause en rien.

## 1. Verdict global et statut

**Statut : NON VALIDÉE. L'enquête ne peut pas être dite « validée ».** Sur 16 objections majeures, 12 sont confirmées, 4 confirmées en partie, 0 réfutée, 0 non tranchée, 0 bloquante au sens des auditeurs. Aucune n'est corrigée au commit audité.

**Verdict sur le fond : les faits tiennent, la lecture doit changer.**
- **Ce qui tient :** le brut, les chronologies, le groupe de 33, les soldes d'avant Musk, le calcul du test gelé. Mes mesures écrites depuis le texte du plan retombent sur `metrics.csv` à 3e-16.
- **Ce qui ne tient pas :** l'usage du test gelé comme appui contre une connaissance préalable, « autour du créateur », « surtout d'échanges », 5 assertions sur 51.
- **Ce qui s'ajoute :** une série de 13 wallets financés par Coinbase en 507 s, créateur compris, qui reversent tous au même compte de dépôt. C'est le fait le plus fort du dossier, et le rapport ne le contient pas.
- **Trois audits corrigés par ce relecteur :** A-03 (table datée à tort, 55,9 % du SOL est postérieur au mint), B-06 (845,72 M est un achat brut, le stock vaut 90,05 M), C-03 (la rafale de 9 dépend d'un filtre choisi après coup, sans lui 4 témoins sur 120 l'atteignent).

Assertions : **44 PASS, 5 FAIL (C19, C34, C35, C49, C50), 2 INCONCLUSIVE (C39, C46)**, plus 17 lignes nouvelles. Détail : `CLAIM_VERIFICATION.csv`. Corrections : `CORRECTIONS.md`. Scripts et sorties : `work_D/`.

**Méthode.** Parseur propre relu sur 2 699 114 transactions (`d01_parse.py`), PnL réécrit (retombe sur `wallets.parquet` à 4,7e-05 SOL sur 71 706 wallets), simulation de puissance écrite sans lire celle de B, témoin direct nouveau sur la série. Réseau : 440 crédits Helius sur 1 000, 44 pages, 3 réponses 429 (`d23_ctrl_series.txt`). Aucune clé lue ni écrite par mes scripts en dehors de `dmaga.helius`.

## 2. Objections majeures

| Id | Objet | Statut | Preuve de D | Effet sur une conclusion |
|---|---|---|---|---|
| A-01 | 5 903 lignes doublées | **CONFIRMÉE** | 5 903 exactes, 4 966 du 24/07 00:00:11 à 05:36:26, 937 en venues, 0 avant 19:30:13 le 21/07 ; PnL : 2 673,49 SOL d'écart, 861 wallets dont le réalisé change, 967 si tout champ compte (`d40`, `d49`). A écrit 954 | Aucune conclusion. Tables seulement : voir section 5 |
| A-02 | Autorité `GpMZbSM2` | **CONFIRMÉE**, gravité mineure sur les conclusions | Vault lu dans mon parseur : 1 708 lignes `swap_other` sur 1 434 tx, 2 840,7 SOL comptés par ligne (A : 1 550, 2 630,8) ; 1 136 lignes `swap`, 391,2 SOL d'écart (A : 1 279, 416,3) ; 24 h après Musk : 5,52 SOL de ventes et 29,71 d'achats manquants ; avant Musk : 13 lignes, 6,86 SOL (`d40`) | Aucune. `DswkYbBh` 93,6 devient 4,4 SOL (estimation) |
| A-03 | Origine des fonds | **CONFIRMÉE EN PARTIE** | « Surtout » reste non établi. Mais la table de A n'a pas de borne haute : 55,9 % de son SOL arrive après le mint, jusqu'au 28/08/2026 (`d45`). Vraie fenêtre, 14/07/2023 au mint : sans étiquette 42,5 %, pools 22,1 %, Jupiter 20,5 %, échanges 14,8 % | C50 FAIL. Le correctif « 22 % et 68 % » de A ne doit pas être repris |
| A-04 | Allers-retours | **CONFIRMÉE** | Ma règle (même quantité à 1 %, 10 s) : 106 254 SOL sur 785 713, 13,5 % (A : 14,1 %) ; 44,66 des 145,44 SOL de 19:23:20 à 19:30:13 ; rangs 1 à 3 à 100 %, 100 %, 98,7 %, 0 ligne signataire (`d41`) | Lecture de C05 et des classements. La succession reste : 100,78 SOL nets |
| A-05 | Mouvements hors brut | **CONFIRMÉE**, portée bornée | 27 196 ruptures, 1 168 comptes, 1 508,5 et 1 336,9 M (`d42`). Voir section 4.4 | Résiduels et réalisés tardifs. Rien avant Musk |
| B-01 | Puissance proche du nul | **CONFIRMÉE** | Ma simulation : nul 2,4 %, 1 R 2,4 %, 2 R 3,3 %, 5 R 100 % par M7 seule (`d11`). B : 2,4 ; 2,8 ; 3,3 ; 100 | Le verdict ne déplace presque pas la croyance |
| B-02 | Contrôles positifs trop faciles | **CONFIRMÉE** | Mêmes effets sur vraies données : moyen 3,3 %, fort 7,5 % (B : 7,1 %), contre 100 % sur synthétique | C49 |
| B-03 | `INCONCLUSIF (puissance)` | **CONFIRMÉE** | `metrics.py` ligne 116 : `k < 139`, possibilité de passer et non puissance | Le verdict affirmatif était inévitable à k = 211 |
| B-04 | M3 et M4 ne peuvent pas ouvrir | **CONFIRMÉE** | 5 pairs à 1,0 sur M3, 3 sur M4, p minimal 0,0283 et 0,0189 contre 0,00714 ; facteur × 1 000 : 2,4 % (`d11`) | Holm paie 7 tests, 5 peuvent ouvrir |
| B-05 | Libellé trop fort | **CONFIRMÉE** | Au-dessus de la médiane 6/7, du P75 5/7 ; 0 pair au-dessus sur les 7, 7 sur 6 ; centile moyen 0,755, p 0,0425 exploratoire, une comparaison parmi les 121 de B, sans valeur de preuve | Ajouter la phrase N09 |
| B-06 | Angles morts | **CONFIRMÉE EN PARTIE** | Angles réels, chiffres à corriger : 845,72 M est un achat brut, solde vu à S 158,88 M, 90,05 M après retrait de 68,83 M déjà partis vers `AtZjv3Du`. 114,96 M reçus en 24 h, dont 110,2 M par le groupe, 76,3 M nets. 14:00 fait bien 269 signatures. 2 762 SOL dans l'heure de S (B : 2 756) (`d44`, `d46`, `d47`) | C09 tient, avec 90 M et non 846 M |
| C-01 | Série Coinbase | **CONFIRMÉE EN PARTIE** | Faits plus forts que chez C, témoin de C inadapté, voir section 4.2 | Niveau B pour le même opérateur ou compte, sur 13 wallets |
| C-02 | « Autour du créateur » | **CONFIRMÉE** | Créateur hors des 33, 0 arête, 0 tx DMAGA commune ; 2 des 33 dans la série, 4 expéditeurs de 9W9b ; SOL d'avant le mint en 2 composantes de 7 et 2 wallets ; périmètres 61,36 ; 92,08 ; 266,70 M (`d43`, `d44`) | Retirer l'expression, deux périmètres |
| C-03 | Nature de 9W9b | **CONFIRMÉE EN PARTIE** | Compte de dépôt Coinbase : B. Même bénéficiaire : non établi, C. Voir section 4.2 | Remplacer « non tranché » |
| C-04 | `BuHUkjUy` | **CONFIRMÉE** | Écart exact 100 000 lamports, nul empirique et frais standard, voir section 4.2 | B pour le lien de 2025 |
| C-05 | 2,4 % et « moins vendeur » | **CONFIRMÉE** | 34 transferts, 32,102 M, 16 destinataires ; 973,3 SOL vendus après réception, plafond non atteint ; 2,886 % ; base commune 37,3 % contre 40,8 à 43,7 % (`d43`). C compare `token_edges` à `trades` : asymétrie, d'où ma fourchette | Écart de 3,5 à 6,4 points et non 12,5 |

Aucun constat n'est classé BLOQUANT par A, B ou C. Je n'en reclasse aucun.

## 3. Désaccords et interactions entre auditeurs

| Point | Positions | Résolution |
|---|---|---|
| C30 | A INCONCLUSIVE, C PASS | **PASS.** A manquait de flux pour 3 destinataires. Historique brut de `G41vRrsH` : 15 virements exacts de 0,5 SOL, 13 de 01:46:23 à 02:03:38, 7 sans achat, 2 wallets à 65 min 44 s et 65 min 17 s (`d44`) |
| C49 | A INCONCLUSIVE, B FAIL | **FAIL.** Gel vrai (17 empreintes sur 17, 23:47:06 avant 03:25:36). Chiffres des contrôles vrais, portée fausse. Copie neuve : aucune trace trouvée dans le dépôt ni par une recherche partielle des transcriptions, seul le journal l'affirme. La reproduction existe désormais par trois voies : A, B, D |
| C37 | C INCONCLUSIVE, A non couvert | **PASS sur les montants.** Parcours réécrit, valeurs identiques, sans effet des décimales fausses de A-12. Mais 175 427 SOL éq. s'arrêtent sur un service non nommé, contre 24 933 sur les 6 échanges cités (`d48`) |
| C19 | C FAIL | **FAIL, au sens de C sur un périmètre seulement.** Le niveau C reste juste pour les 33 |
| C36 | A PASS, C PASS avec correctif | PASS. G41vRrsH : 11 sur 33 confirmé. Dans le groupe : 11 à 12 selon le seuil (`d46`) |
| PASS de C sur `trades.parquet` | C15, C41, C14 après A-01 | **Ils tiennent.** Une seule ligne de vente doublée tombe dans les 24 h : 190 551,17 devient 190 532,13 SOL. 22,49 et 34,96 % inchangés. Fenêtre de C14 sans doublon |
| Table de A-03 contre fait de C-03 | A voit « sans étiquette », C montre des hot wallets non étiquetés | Compatible : la part d'échange est une borne basse. Aucun des 6 balayeurs et de `5g7yNH` n'apparaît toutefois en financement de niveau 0 avant le mint (`d44`) |
| B-06 contre C-13 | Transferts invisibles pour le test, visibles dans les flux | Compatible. Sur les 114,96 M reçus en 24 h, 110,2 M le sont par des membres du groupe, soit 96 % |
| A-05 contre C20 | Le brut manque des transferts SPL | C20 n'en souffre pas : 0 rupture sur les comptes des 3 gagnants |
| A-05 contre C-05 | Sorties cachées ? | 0 sortie cachée en 24 h pour les 110 autres détenteurs comme pour le groupe |

## 4. Réponses aux angles demandés

### 4.1 Doublons et autorité partagée : quels chiffres bougent
Seuls bougent les tables de PnL, les 18 367 de C35, le réalisé du groupe et le total des lignes. Aucun chiffre de l'essentiel ne change au-delà de l'arrondi. H3QsBr, GXZvX, 9PrmF8 et 5QhJJc sont identiques. Top 10 inchangé, 3 changements dans le top 100. Détail en section 5.

### 4.2 Série Coinbase, 9W9b, `BuHUkjUy`
**Les témoins de C sont-ils bons ? En partie.**
- `cb_series_ctrl.csv` compare des rafales de montants ronds, pas le retour au même dépôt. Le 0,55 % de C est la présence de DMAGA chez les expéditeurs témoins, pas un taux de retour. Le chiffre de C-01 répond donc à une autre question.
- Le filtre {0,5 ; 1 ; 1,05} a été choisi après avoir vu le créateur et 5QhJJc. C le dit.

**La fenêtre a-t-elle été choisie après coup ? Oui, mais le résultat n'en dépend pas.** Sans aucun filtre de montant ni de fenêtre : sur 2 517 retraits vers 2 201 destinataires en 2 h, 13 destinataires reversent ensuite à 9W9b, et les 13 sont dans 507 s (`d20`). Écarts réguliers, CV 0,245, P = 5e-05 sous arrivées au hasard, 20 000 tirages. Fp6kgqHU et A52fNskQ, les 2 restants du filtre, ne reviennent pas. 14 des 15 sont neufs.

**Combien de séries comparables ailleurs ? Rares, mais pas nulles.**
- Témoin direct, nouveau : 4 fenêtres de 507 s du même matin, tirées à graine fixe avant tout appel (`d23_plan.csv`), 44 wallets à montant rond, première page de 100 tx. Destination commune par virement pur d'au moins 0,05 SOL : au plus 1, 3, 1, 1 wallets, contre 10 pour la série à même troncature et 13 sur l'historique complet (`d24`). Limite : 4 fenêtres, un seul matin.
- Dans le même compte : 3 wallets à environ 0,75 SOL en 2 min 25 s le 26/06/2024, 2 wallets à 0,02 SOL le 23/08/2024. L'habitude précède le mint de 17 jours (N15).

**Le passage de C à B est-il mérité ? Oui, sur un périmètre et un mot précis.**
- B pour « même opérateur ou même compte de dépôt » sur le créateur et 12 wallets de la série.
- C maintenu pour les 33 : grappes antérieures, 2 seulement dans la série.
- C pour « même bénéficiaire » : C écrit « B pour même bénéficiaire pour les rafales », je ne le reprends pas.

**Compte de dépôt client établi ? Le type oui, B. Le titulaire non.** Pour : 100 % des sorties vers 3 hot wallets et 6 adresses qui balaient aussi 53 témoins sur 120, 59 balayages signés par 9W9b, frais de 155 000 lamports. Pour un même compte : 31 expéditeurs sur 48 touchent DMAGA, 16 sur 33 hors série et hors groupe, contre 8 sur 1 365 témoins, jamais plus de 2 par dépôt (`d43`). **Service partagé :** un compte unique tenu pour plusieurs personnes, par un trésorier ou un opérateur payé pour un lancement, reste possible. Les témoins à forte rafale non ronde montrent que des opérateurs multi-wallets existent : sans le filtre « rond et vidé », 4 témoins sur 120 atteignent 9 expéditeurs en 10 min, maximum 18 (`d22`). L'argument « 9 contre 3 » ne doit donc pas être repris seul. Seule une réquisition de Coinbase trancherait.

**Le montant apparié de `BuHUkjUy` tient-il ? Oui.** Dépôt 6,576437507 SOL le 10/07/2025 à 03:05:01, retrait 6,576337507 SOL le 12/07 à 16:43:59, écart exact 100 000 lamports (`d21`).
- Nul empirique, mêmes wallets, 3 237 dépôts témoins non ronds, tous temps : 0 à cet écart exact ; 0 sur 1 951 dépôts d'au moins 1 SOL aux multiples de 100 000. Borne à 95 % : moins de 0,15 % par dépôt, moins de 1,2 % sur 8 dépôts d'au moins 1 SOL. Placebo en temps inversé : 0.
- Mécanisme : 70 des 2 517 retraits valent un rond moins exactement 100 000 lamports. C'est un frais d'envoi standard. C ne l'avait pas vu.
- `5g7yNH` : balayé par 16 dépôts témoins sur 120, 76,72 SOL (`d21`). C n'avait qu'un exemple.
- Les 3 autres correspondances de C sont 0,0105 contre 0,01 SOL, sans valeur.

### 4.3 Puissance
Chiffres de B-01 à B-04 **confirmés** par ma simulation, à 0,4 point près. Table : `work_D/d11_scenarios.csv`, `d11_factors.csv`. Puissance exacte d'une mesure : 12,0 % à un quantile vrai de 99 %, 81,0 % à 99,9 %.

**Le texte gelé peut être conservé tel quel, et doit l'être.** Le plan a fixé ce texte pour ce résultat, il ne peut pas changer après coup. Il doit être accompagné, juste à côté, de : « Verdict du plan : "DMAGA NON DISTINGUABLE DE SES PAIRS". Cela signifie qu'aucune mesure ne dépasse tous les 211 pairs. DMAGA est du 74e au 85e centile sur 6 mesures sur 7. Sur les vraies données, ce test détecte 2,4 % sans effet, 3,3 % pour une accumulation de deux fois la réserve du pool, 7,5 % pour l'effet fort de ses contrôles. Il n'apporte donc d'élément ni pour ni contre une connaissance préalable. » Le test ne doit plus figurer sous « Aucune preuve d'achat informé » comme appui, ni dans la ligne H2 comme argument.

### 4.4 Transferts SPL manqués : ce qu'ils touchent vraiment
| Période | Ruptures | Montant | Effet |
|---|---|---|---|
| Avant 19:03:27 le 21/07 | 5 | 84,737 M, dont 84,537 M vers `AtZjv3Du` déjà compensés | Aucun : somme des soldes 1 000 M |
| À cheval sur 19:03:27 | 15 | 1,01 M | Négligeable |
| 24 h après Musk | 243 | 3,98 M, sorties cachées 1,83 M | C15, C41 : aucun |
| Ensuite | reste | 2 755 M | Résiduels, réalisés de wallets tardifs, graphe post-Musk des non tracés |

Touché : la colonne « Résiduel », `7gEQ6syD` 122,28 M pour un dernier solde de 0, `HGs9NdwD` 34,35 M pour 0,037 M ; somme 937,1 M pour 567,8 M hors pools ; `completeness`. **Non touché :** groupe de 33, 217 M, ventes de 24 h, 3 gagnants (0 rupture), test gelé. Ruptures d'au moins 1 M sur des wallets non tracés : 0 avant Musk, 0 sur 24 h, 102 ensuite pour 274,4 M.

## 5. Table des recalculs

| Chiffre | Valeur au commit 01ae5a4 | Nouvelle valeur | Écart | Script |
|---|---|---|---|---|
| Lignes de `trades.parquet` | 919 783 | 913 880 uniques | −5 903 | `d40_trades.py` |
| C15, marché 24 h (SOL) | 190 551,17 | 190 532,13 ; 190 537,65 avec A-02 (estimation) | −19,04 ; −13,52 | `d40` |
| C15, part du groupe | 2,3746 % | 2,3749 % | +0,0002 point | `d43_perim.py` |
| C15, avec 3 destinataires | absent | 2,886 % | +0,51 point | `d43` |
| C35, réalisés positifs entrés après Musk | 18 367 sur 53 893 | 18 309 ; 18 259 sur 53 968 avec A-02 (estimation) | −58 ; −108 | `d40` |
| C35, à plus de 0,1 SOL | absent | 9 885 | | `d40` |
| C35, heure du sommet | 09:00 | 09:01:46 | heure ronde | `d46_claims.py` |
| Réalisé du groupe de 33 (SOL) | 5 594,0 | 5 471,7 ; 5 469,8 avec A-02 | −122,3 ; −124,2 | `d40` |
| Réalisé cumulé, tous wallets | 100 128,3 | 98 189,9 ; 97 278,3 avec A-02 | −1 938,4 ; −2 850,0 | `d49_small.py` |
| Acheté, vendu, tous wallets | 790 223,1 ; 785 853,8 | 787 071,7 ; 782 244,1 | −3 151,4 ; −3 609,7 | `d49` |
| `ET8ZG5zA`, `Akp46Dic`, `C7i9beNH`, `5FzhCSWL` | 359,14 ; 364,49 ; 404,55 ; 144,58 | 203,63 ; 268,70 ; 378,01 ; 187,91 | | `d40` |
| Top 100, entrants | absents | `7uRDe43i` rang 16, `BBcYhznj` 32, `CQQqZgro` 94 | 3 | `d40_top_changes.csv` |
| Top 100, sortants | `D4zVhwuU` 98, `9Q2iQTt6` 99, `CtXRQVs2` 100 | sortis | 3 | `d40_top_changes.csv` |
| C05, 19:23:20 à 19:30:13 | 145,44 SOL | 100,78 SOL hors allers-retours | −44,66 | `d41_roundtrip.py` |
| C41, sortie vendue | 22,49 % contre 34,96 % | 37,3 % contre 40,8 à 43,7 % sur base commune | écart 12,5 devient 3,5 à 6,4 points | `d43` |
| C36 | 11 sur 32 ; 10 sur 32 | 11 à 12 sur 33 ; 11 sur 33 | +1 G41 | `d46` |
| C50, table de A-03 | sans étiquette 67,8 ; pools 14,8 ; Jupiter 10,1 ; échanges 7,3 % | 42,5 ; 22,1 ; 20,5 ; 14,8 % | fenêtre corrigée | `d45_funding.py` |
| C50, premier financeur avant le mint | « surtout » ; A : 301, 244, 198, 4 sur toutes dates | 189 échange, 189 sans étiquette, 109 Jupiter, 4 service | | `d45` |
| B-06, jetons hors M6 | 845,72 M (B) | 158,88 M vus à S, 90,05 M après 68,83 M déjà sortis | ÷ 9,4 | `d44_misc.py`, `d46` |
| B-06, transferts 24 h | 114,96 M (B) | 76,3 M nets, 110,2 M reçus par le groupe | | `d44` |
| A-04, part des allers-retours | 14,1 % (A) | 13,5 % (règle à 1 %) | −0,6 point | `d41` |
| C37, service non nommé | « beaucoup » | 175 427 SOL éq. | | `d48_exits.py` |
| Inchangés | C05, C06, C07, C11 à C14, C21, C24, C28, C29, C40, C43 à C45 | identiques | 0 | `d40`, `d43`, `d46`, `d47` |

## 6. Amendement 001

Recalcul depuis `selection.jsonl` et `metrics.csv` (`d30_amend.txt`). Aucune approbation de l'audit n'est supposée.

| Variante | k réel | k maximal | Part hors principal | Meilleur p réel | Meilleur p si tous les reportés sont sous DMAGA | Pire p sur M6 |
|---|---|---|---|---|---|---|
| Principal | 211 | 211 | sans objet | 0,1557 | sans objet | sans objet |
| R1 | 212 | 231 | 3 tokens | 0,1596 | 0,146 | 0,232 |
| R2 | 240 | 498 | 29 sur 287, 10,1 % | 0,1411 | 0,068 | 0,586 |

1. **Modifie-t-il le résultat principal ? Non.** Les 213 tokens de la bande principale sont tous collectés, 0 reporté. Rangs, S et verdict sont reproduits par une chaîne où l'amendement ne joue aucun rôle.
2. **Réduit-il seulement la robustesse ? Oui.** R1 perd 19 tokens, R2 en perd 258.
3. **Peut-il masquer une faiblesse importante ? Pas sur le verdict, oui sur la lecture de R2.** Seuil de Holm 0,00714 ; à c = 33 sur M6, il faudrait k ≥ 4 759, l'univers n'a pas ce nombre. Mais R2 n'est pas un test de la bande large : les 29 ajouts sont tous créés du 15 au 23/06, de 10 324 $ à 94 498 $, Spearman position et création 0,9995. Aucun token au-dessus de 10 M$ n'est collecté, 3 sont reportés. Médianes M1 17,3 contre 3,75. Selon les reportés, le p de M6 irait de 0,068 à 0,586. Écrire « robuste à R2 » serait faux.

**Texte inexact :** « ordre d'activité, sans lien avec les mesures ». L'ordre est celui de la création, et le lien n'a pas été testé.

**`resultats_vus: non` : crédible, non prouvé.** Fichier à 02:46:05, `selection.jsonl` à 03:24:24, `metrics.csv` à 03:25:19, première ligne réelle du registre à 03:25:36. Mais `001` n'entre au dépôt qu'à 03:46:09, avec les résultats, et hors du verrou.

**Recommandation : CONSERVER pour le verdict, en corrigeant le texte et en requalifiant R1 et R2 en « variantes partielles, sans valeur de robustesse sur la bande ».** Le rejeter n'apporterait rien au verdict et demanderait une collecte que le pool, presque épuisé, ne peut plus payer. Si une lecture de la bande large est voulue, tirer au hasard par tranche de capitalisation parmi les 258, par un nouvel amendement. **La décision reste à Benjamin.** Rien n'a été réécrit. Projet : `work_D/projet_amendement_003.md`, `resultats_vus: oui`, non installé.

## 7. Objections mineures : échantillon

Recalculées et confirmées : A-06 (507,93 et 236,55 SOL au vault), A-09 (183 acheteurs, A écrit 184 ; 107 et 51), A-10 (09:01:46, 9 885), A-12 (les 5 000 lignes de A retrouvées, mon filtre en voit 5 001 sur 3 wallets, sans effet sur C37), A-15 (14 tronqués sur 65 dans C37), B-07 (S1, max passé 386,9), B-08 (0,9995 ; 29 ajouts), B-09 (borne k ≥ 4 619), B-15, B-16 (arithmétique), C-08 (`CZsBW8yC` financé par G41vRrsH), C-11 (5 `tronque_sans_S20`, tous `reporte_budget`).

Relues sans recalcul, aucune ne change une conclusion : A-07 (journal `a01_sigs.log` relu), A-08, A-11, A-13, A-14, B-10 à B-14, C-06, C-07, C-09, C-10.

Écart nouveau, mineur : `TOP_TRADERS.md` écrit 53 889, `CASE_REPORT.md` 53 893, sur deux populations (71 682 et 71 706 wallets) sans le dire.

## 8. Ce qui reste non vérifié

- La reproduction « en copie neuve » : aucune trace dans le dépôt. Recherche partielle dans les transcriptions.
- A-02 renormalisé : mes valeurs avec A-02 sont des estimations, le vault réparti au prorata des jetons. Seule une relance de `nrm_10_trades.py` donne le chiffre final.
- Effet de A-04 sur le test (`a42`) et lignes remises de B-22 : repris, non refaits.
- Nature des programmes `ChXs7eqj`, `3GMsedVP` et d'A-16 : non identifiée. Volume artificiel non testé.
- Lecture des captures (C25, IMG_5658) et heure de Butler : reprises de A et C.
- C46 : réponses réseau non gardées.
- `wallet_clusters.parquet` (345 wallets) : repris de C.
- Témoin direct de la série : 4 fenêtres, un matin, 100 premières tx. Un retour plus tardif échappe aux témoins comme à la série tronquée.
- Identité de tout wallet et de tout titulaire de compte : hors de portée sans réquisition.

## 9. Conclusions

**Confirmées :**
- Création du mint, 02:05:25 UTC, par `8YLEuUtZ` ; 3 h 54 après Butler.
- La hausse suit l'envoi de l'avatar (A pour les flux, B pour la cause). 100,78 SOL nets ou 145,44 bruts.
- Groupe de 33 wallets, 40 transferts, 217,04 M, 23,14 %, plafond.
- Calcul du test gelé, et son texte comme sortie du plan.
- 5QhJJc paie le gaz du créateur 35 s avant son ordre ; salve de 15 wallets vers 9W9b le 26/01/2025.
- Aucun lien direct entre les 3 gagnants et ces périmètres. Aucun lien documenté entre un wallet et un compte X du noyau.

**Invalidées ou à retirer :**
- « Ensemble autour du créateur » (N05).
- « Surtout d'échanges et d'historiques antérieurs » (C50).
- « Contrôles positifs corrects » comme garantie de détection (C49).
- « Cohortes distinctes » (C34) ; 18 367 et 09:00 (C35).
- « Moins vendeur, 22,5 contre 35,0 » sans base commune.
- Le test gelé comme argument contre H2.
- « 48 expéditeurs seulement, pas un service de masse » comme raisonnement.

**Nouvelles, à reprendre :** N01 à N17, dont la série de 13 wallets (B pour le même opérateur ou compte), le compte de dépôt (B), le lien `BuHUkjUy` (B en 2025).

**Incertaines :**
- Un seul propriétaire pour les 33 (C), et contre lui des grappes antérieures.
- Un même bénéficiaire derrière 9W9b (C).
- Connaissance préalable : ni établie ni écartée, le test ne départage pas (H2).
- Lien entre l'équipe X et les wallets : non établi.
- Le DM à Musk : non prouvé.

## 10. Blocages restants et ce qui les lève

| Blocage | Ce qui le lève | Qui |
|---|---|---|
| A-01, A-02 | Corriger `db.py` et `normalize.py`, relancer le dérivé, assertion « aucune ligne doublée » dans `chk_90` | Agent, après accord |
| A-03, A-04, A-05 | Republier le tableau des fonds, étiqueter les allers-retours, publier les ruptures, résiduels sur soldes | Agent |
| B-01 à B-06 | Ajouter N08, N09, N17 au rapport, retirer le test de la ligne H2 ; pour la prochaine étude, seuil de puissance sur vraies données | Agent, décision de Benjamin pour la suite |
| C-01 à C-05 | Réécrire Essentiel 4 et 5, tableau H3, Q1, Q6, Q12, niveaux scindés | Agent, après accord |
| Amendement 001, projet 003 | Décision écrite | **Benjamin** |
| Assertions FAIL et INCONCLUSIVE | Corrections de `CORRECTIONS.md` ; C39 et C46 restent à écrire comme jugement et non comme preuve | Agent |
| Corrections déjà intégrées sans audit, et ces nouvelles corrections | Nouvel audit des conclusions sur le rapport corrigé | Benjamin décide |

Tant que ces lignes ne sont pas closes, le mot « validée » reste interdit. Après elles, le texte honnête sera : « faits vérifiés, test gelé reproduit et peu puissant, attribution au niveau B sur un périmètre restreint, aucune identité ».
