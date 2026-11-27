# Plan d'analyse : l'organisation du groupe précoce de DMAGA est-elle atypique ?

Écrit le 03/11/2026 avant toute lecture de transferts de jetons sur un comparateur. Le plan cherche à détruire l'hypothèse, pas à la confirmer. Un écart ne prouve ni un propriétaire unique, ni une connaissance préalable, ni un délit.

## Ce qui a déjà été vu avant ce plan, à ne pas cacher
Sur DMAGA : le groupe de 33 wallets, ses 40 transferts directs d'au moins 1 M, 217 M détenus avant Musk, la série de retraits Coinbase, le dépôt `9W9b…`, tous les audits du 03/11. **Les mesures ci-dessous sont donc choisies après avoir vu DMAGA.** Le seuil de 1 M vient de son rapport.
Sur les comparateurs : les mesures M1 à M7 du test gelé, et la part de financeurs communs sur 40 d'entre eux (`etude_final/tables/funder_share.json`). **Aucun transfert de jetons d'aucun comparateur n'a été lu.**

## Question
Parmi les memecoins Pump.fun créés en juillet 2024 ayant eu un pic tardif comparable, le réseau de transferts directs de jetons entre premiers acheteurs de DMAGA, avant son pic, sort-il de la distribution de ses pairs ?

## Population, fixée maintenant
Les 212 tokens de la variante principale d'`etude_final/derived/metrics.csv`, DMAGA compris, dont la création du pool (`created` de `data/controls/selection.jsonl`) tombe du 01/07/2024 inclus au 01/08/2024 exclu, en UTC : 116 tokens, DMAGA compris, soit 115 comparateurs au plus. S est le `S20` déjà calculé par le code gelé. Limite : le groupe témoin est conditionné au pic tardif, la conclusion ne vaut que parmi ces tokens.

## Collecte
Ordre : DMAGA d'abord, puis les comparateurs triés par adresse de pool et mélangés avec la graine 20261103, sans regarder aucune donnée. Plafond : 60 000 crédits, comptés à 10 par requête, clés du pool de recherche seulement. Le plafond ou l'épuisement des clés arrête la collecte, jamais une exclusion muette. Réponses brutes : `raw/grp/<pool>.jsonl.gz` sur le disque USB.

Pour chaque token :
1. **Courbe :** historique du mint avant `created`, 20 pages de 100 transactions au plus, réussies seulement. Le dépassement est compté (`courbe_tronquee`).
2. **Cohorte :** les 30 wallets au plus grand achat net de jetons, somme de la variation de jetons sur ces pages et des `qty` Raydium de `data/controls/swaps/<pool>.parquet` sur [created, created + 24 h). Net strictement positif. Les étiquettes connues (`dmaga/labels.py`) sont retirées.
3. **Comptes :** pour chaque wallet, son compte de jetons associé (ATA) est dérivé, son historique est lu avant S, réussies seulement, 5 pages au plus. Le dépassement est compté (`ata_tronque`) et une page descendante donne le dernier solde.
4. **Extension :** tout wallet relié par un transfert retenu est lu de la même façon, 60 nouveaux wallets au plus par token, dans l'ordre de découverte. Le dépassement est compté (`extension_plafonnee`).

## Un transfert retenu
Une transaction réussie avant S où, sur ce mint : un seul propriétaire perd des jetons, un ou plusieurs en gagnent, la somme reçue vaut la somme perdue à 1 % près, chaque receveur reçoit au moins 1 M de jetons, et ni l'expéditeur ni les receveurs ne voient un autre mint varier ni leur SOL varier d'au moins 0,05 SOL. Cette règle écarte les swaps, y compris par un AMM inconnu. Plusieurs expéditeurs : transaction comptée (`ambigu`), non retenue. Une vente de gré à gré en deux transactions reste comptée : c'est une limite.

**Service probable :** un wallet relié à au moins 15 wallets distincts est retiré du graphe avant les mesures, et compté.

## Mesures, à l'identique sur chaque token
- **G1** : nombre de wallets de la plus grande composante connexe.
- **G2** : solde à S de cette composante, en part de l'offre de 1 000 M (dernier post-solde lu de chaque wallet avant S).
- **G3** : nombre de paires distinctes de wallets reliées par un transfert retenu.

Sans aucun transfert, les trois valent 0, c'est une valeur mesurée. **Couverture :** si moins de 15 des 30 wallets de la cohorte ont un historique d'ATA non vide, les trois sont NaN, sortent du rang et sont comptés. Une cible indéfinie fait échouer le calcul.

## Tests et verdict
3 tests, un par mesure, unilatéraux, p de rang `(1 + #{pairs ≥ DMAGA}) / (k + 1)`, Holm à 0,05. Une mesure ne peut passer que si DMAGA dépasse tous les pairs, ou à défaut que si `1/(k+1) ≤ 0,0167`, soit k ≥ 59.

Verdict par code, texte fixé maintenant :
- `INCONCLUSIF (collecte)` si k < 59.
- `AUCUNE MESURE NE SORT DES PAIRS. Le test ne détecte qu'un DMAGA au-dessus de tous ses pairs, il n'exclut donc pas une organisation réelle.` si aucune mesure ne passe.
- `ORGANISATION INHABITUELLE SUR <liste>. Ceci décrit un écart à des tokens de juillet 2024 à pic tardif, sur des mesures choisies après avoir vu DMAGA. Ce n'est la preuve ni d'un propriétaire unique, ni d'une connaissance préalable, ni d'un acte illégal.` si au moins une passe.

Variantes rapportées sans correction, jamais utilisées pour le verdict : V1 seuil de 5 M sur les arêtes déjà lues ; V2 sans retrait des services probables. Comparaisons déclarées : 3 + 6 = 9. Le registre fait foi.

Rapportés quoi qu'il arrive : valeur de DMAGA, médiane, maximum des pairs, part de pairs à zéro, centile de DMAGA, tokens en NaN, compteurs de troncature, crédits réels.

## Limites connues
- n = 1 pour la cible. Mesures choisies après avoir vu DMAGA, comparateurs non vus : le p dit si DMAGA est extrême sur ces mesures, pas si elles ont été bien choisies.
- Un ATA ne couvre pas les comptes de jetons non associés. Le transfert par un wallet hors cohorte et hors extension n'est pas vu.
- Le groupe de DMAGA est plus large que ce que cette méthode lit : la valeur de DMAGA ici ne sera pas 33.
- Le SOL n'est pas lu : aucune mesure de financement commun ni de dépôt commun, trop coûteux pour le pool.
- La puissance dépend de la distribution réelle des pairs, inconnue à ce jour. Le contrôle positif ne dit rien d'elle : il teste la plomberie, voir `controles/synth.md`.

## Interdits
Pas de seuil, cohorte, fenêtre ou population changés après avoir vu une mesure de comparateur. Pas de retrait d'observation. Tout changement : `amendements/NNN-<date>.md` avec `resultats_vus`, décidé par Benjamin.
