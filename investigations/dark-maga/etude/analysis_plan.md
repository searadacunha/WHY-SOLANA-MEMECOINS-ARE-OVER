# Plan d'analyse : le comportement d'avant-pic de DMAGA est-il anormal ?

Écrit avant le calcul de toute métrique de test, sur DMAGA comme sur les comparateurs. Déjà vus par
l'auteur avant le gel, à ne pas cacher : la courbe horaire de DMAGA, ses plus gros gagnants, l'existence de
transferts directs entre certains de ses wallets, son heure de pic (21/07 19:00 UTC, n = 1 719 signatures) et sa
capitalisation une heure avant (environ 1,3 M$, 382 SOL de réserve), lues pour centrer la bande ci-dessous. L'auditeur des
échecs silencieux a lu des parts de SOL par adresse sur le premier bloc de DMAGA. Aucune métrique ci-dessous n'a été
calculée, sur aucun token. Le choix des métriques n'a donc pas regardé les comparateurs, mais il a pu être influencé par ce qui
a été vu sur DMAGA : c'est une limite, écrite ici et rappelée dans les résultats.

Question : avant son pic du 21/07/2024, DMAGA se distingue-t-il des autres memecoins Pump.fun de la même
période ayant eu un pic tardif comparable, sur des mesures associées à une accumulation informée ou coordonnée ?

Le plan cherche à détruire cette hypothèse, pas à la confirmer. Un résultat « anormal » ne prouve ni une
connaissance préalable ni un délit : il dit seulement que DMAGA sort de la distribution de ses pairs.

## Données

- Source : Helius `getTransactionsForAddress`, réponses brutes sur `VERBATIM HD/Dark-MAGA-Investigation/raw`.
- Population de départ : toutes les migrations Pump.fun vers Raydium v4 du compte
  `39azUYFWPz3VHgKCf3VChUwbpURdCHRxjWVowf5jUJjg`, du 15/06/2024 inclus au 01/09/2024 exclu (13 920 lues).
- Activité : histogramme horaire des signatures de chaque pool sur [création + 24 h, création + 60 j), plafond
  150 000 signatures (`scripts/col_40_controls.py`). Moins de 500 signatures après 96 h : pas de pic tardif possible.
- Transactions : pour chaque token retenu, transactions réussies du pool Raydium v4 de sa création à S+1 h.
- Un swap : les deux réserves du pool varient en sens opposés. Le bénéficiaire est le propriétaire final des jetons.
  Écartés et comptés sur tous les tokens : parts sous 5 % du swap (collecteurs de frais, 0,85 % en médiane sur DMAGA) ;
  propriétaires non signataires dont le jeton et un autre mint varient en sens opposés (réserves d'autres venues, escrows,
  dont `5V97uEb4` et `AD65fgYt` sur DMAGA, nature non établie). Transactions réussies seulement.
- Chaîne de soldes par pool : le solde WSOL après une transaction doit être le solde avant la suivante. Un pool rompu est
  exclu et compté. Couverture SOL/USD : une minute absente fait échouer la sélection, jamais une exclusion muette.
- Pour la comparabilité, **seul le pool Raydium v4 compte, pour DMAGA comme pour les comparateurs**. Les
  autres venues (CLMM, DLMM, Orca) sont ignorés dans ces tests : ils existent sur DMAGA et sont traités dans
  la reconstruction du PnL, pas ici.
- Comptabilité rapportée : tokens demandés, reçus, vides, en erreur ; pools tronqués au plafond de pages.
- Pièges contrôlés : ordre (slot, transactionIndex), décimales lues dans chaque balance, version de
  transaction, propriétaire et non signataire, soldes de vault en chaîne, swaps multi-bénéficiaires.

## Unité et n effectif

Unité : le token. n = 1 pour DMAGA, k pour les comparateurs. Les comparateurs d'un même créateur ou d'une même
journée ne sont pas indépendants : on rapporte le nombre de jours distincts de pic comme n effectif prudent.
Les p sont des rangs : p = (1 + #{comparateurs ≥ DMAGA}) / (k + 1). Le plus petit p possible est 1/(k+1).

## Population des comparateurs, fixée maintenant

Un token entre s'il remplit toutes ces conditions, dans cet ordre, DMAGA compris :
1. Un pic trouvé dans la partie listée ; un pool tronqué sans pic trouvé est exclu et compté.
2. **Pic tardif** : il existe une heure h ≥ création + 96 h et < création + 60 j telle que le nombre de signatures de h est
   ≥ 20 fois la médiane horaire des 72 heures précédentes (médiane plancher 5) et ≥ 500. S = début de la
   première heure qui remplit ces conditions.
3. **Appariement à la capitalisation** : capitalisation pleine (prix du pool × offre 10^9, en USD à la minute)
   entre 100 000 $ et 10 000 000 $ une heure avant S, soit environ un facteur 10 de part et d'autre de DMAGA.
   Dernier swap lu parmi les 200 dernières transactions réussies d'avant S−1 h ; sinon `sans_swap_avant_S`, compté.
4. Au moins 20 lignes de swap Raydium sur [S−96 h, S).
Choix de l'heure pour les pics : la cadence est fixée à 1 h, les mesures n'en essaient pas d'autres. Le pic compte toutes
les signatures, échouées comprises : du spam peut donc le déclencher, le même biais touche tous les tokens, R3 le borne.
Un pool tronqué qui n'a que S10 sort de la variante principale et il est compté (`tronque_sans_S20`).
Survivants : les tokens morts sans pic sont exclus par construction, c'est le groupe de comparaison voulu
(des tokens qui ont explosé tard). La conclusion ne vaut donc que parmi les pics tardifs.

## Mesures, calculées à l'identique sur chaque token

Fenêtres définies par S. Tout achat est un swap Raydium attribué au propriétaire final, en SOL côté vault.
Point dans le temps : aucune mesure n'utilise une donnée postérieure à S. Une mesure indéfinie vaut NaN, jamais 0 : elle sort
du rang de cette mesure, son nombre est publié, et une cible indéfinie fait échouer le calcul.
- **M1 run-up 3 h** : SOL acheté sur [S−3 h, S) / médiane du SOL acheté par fenêtre glissante de 3 h sans
  chevauchement sur [S−75 h, S−3 h) (plancher 0,1 SOL).
- **M2 run-up 24 h** : SOL acheté sur [S−24 h, S) / médiane par fenêtre de 24 h sur [S−96 h, S−24 h) (plancher 0,1 SOL).
- **M3 nouveaux wallets** : part du SOL acheté sur [S−24 h, S) par des wallets sans aucun swap Raydium antérieur sur ce token.
  Indéfinie sans achat sur la fenêtre, comme M4 et M7.
- **M4 concentration** : part des 5 premiers wallets dans le SOL acheté sur [S−24 h, S).
- **M5 synchronisation** : (paires de wallets distincts dont le premier achat de la fenêtre [S−24 h, S) tombe
  dans le même slot) / (paires attendues pour n acheteurs répartis au hasard sur 216 000 slots). Indéfinie sous 2 acheteurs.
- **M6 détention des précoces** : parmi les wallets ayant acheté durant les 24 h suivant la création du pool, part
  des jetons qu'ils ont achetés avant S encore détenue à S (net des ventes, transferts ignorés car le pool ne les voit pas).
  Indéfinie sans acheteur précoce.
- **M7 gros achat sur liquidité faible** : plus gros achat unique sur [S−24 h, S), rapporté à la réserve SOL du vault juste avant lui.

## Tests

- Principaux : 7, un par mesure, unilatéraux (DMAGA plus élevé que ses pairs). p de rang. Correction de Holm,
  alpha 0,05. Comptage officiel par le registre, sur les comparaisons de données réelles.
- Secondaires, sur DMAGA seul (S1), à titre descriptif :
  S1 : SOL acheté et wallets nouveaux sur [E−3 h, E) pour E = publication @ChrisWinig (21/07 16:02:29 UTC), comparés
  à toutes les fenêtres de 3 h sans chevauchement entre création + 96 h et E−3 h. Même calcul pour E = envoi de l'avatar
  de Musk, 21/07 19:23:20 UTC. « Nouveaux wallets » : acheteurs distincts dont le premier swap tombe dans la fenêtre. Les données
  de DMAGA vont jusqu'à E. 4 comparaisons, Holm séparé, jamais utilisées dans le verdict.
- Déclaré : 7 principaux + 4 secondaires + 3 variantes de 7 mesures = 32 comparaisons sur données réelles. Le registre fait foi.

## Puissance

Holm sur 7 tests exige, pour le meilleur test, p ≤ 0,05/7 = 0,00714, donc k ≥ 139 comparateurs. En dessous, aucun
test ne peut être significatif : le verdict devient INCONCLUSIF. Le rapport de contrôles donne la puissance.

## Contrôles positifs avant le gel

Deux niveaux, rapport `controles/synth.md`. Mesures et verdict sur tables synthétiques : effet nul, moyen, fort, plus une baleine
unique (M4) et des précoces qui gardent (M6), 40 graines. Puis de bout en bout : transactions brutes synthétiques passées par
collect, verify, parse_swaps, chaîne de soldes, select, swaps, table, tests et verdict, sans réseau (nul, fort, et une transaction
retirée qui doit faire exclure le pool). Le nul doit rester muet.

## Variantes de robustesse, fixées maintenant, jamais utilisées pour choisir

R1 : seuil de pic 10× au lieu de 20×. R2 : bande de capitalisation 10 000 $ à 50 000 000 $. R3 : S décalé d'une heure en arrière
(S−1 h) pour écarter un démarrage dans l'heure d'avant. Rapportées à côté des principaux, sans correction.

## Verdict, calculé par code (`code/ana_90_verdict.py`), texte fixé maintenant

- `INCONCLUSIF (puissance)` si k < 139.
- `DMAGA NON DISTINGUABLE DE SES PAIRS` si aucune mesure ne passe Holm.
- `DMAGA INHABITUEL SUR <liste>` si au moins une passe, avec cette phrase obligatoire : « Ceci décrit un écart à la
  distribution des pics tardifs ; ce n'est pas une preuve de connaissance préalable ni d'une action illégale. »

## Ce que le verdict ne couvre pas

La chronologie, l'attribution de wallets, les liens financiers directs et le récit des comptes X sont traités hors de ce
test, avec l'échelle A à D du rapport. Un test sur un seul token ne dit rien de l'intention.

## Interdits

Pas de seuil, fenêtre ou population choisis après avoir vu une mesure. Pas de retrait d'observation après en avoir vu la
valeur. Pas de test secondaire promu en principal.

## Amendements

Aucun au gel. Tout changement ultérieur : `amendements/NNN-<date>.md` avec `resultats_vus: oui|non`.
