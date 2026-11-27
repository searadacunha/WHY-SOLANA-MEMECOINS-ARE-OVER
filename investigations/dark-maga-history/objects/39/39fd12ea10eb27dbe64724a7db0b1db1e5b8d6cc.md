# Résultats : organisation du groupe précoce de DMAGA

Plan : `analysis_plan.md`, gelé le 03/11/2026 à 10:53:59 UTC, commit `5291098`. Sorties : `tables/tests.json`, `tables/verdict.json`, `derived/table.csv`.

## Verdict du code, texte fixé par le plan
**`INCONCLUSIF (collecte) : 48 comparateurs, il en faut 59`**

Le plafond de 60 000 crédits a arrêté la collecte à 61 110 crédits comptés, après DMAGA et 48 des 115 comparateurs, dans l'ordre tiré au hasard (graine 20261103). Le coût réel, environ 1 250 crédits par token, a été très supérieur à mon estimation d'environ 450, surtout à cause de l'extension et des pages de la courbe.

## Valeurs, à lire comme une description, pas comme un test
| Mesure | DMAGA | Médiane des 48 pairs | Maximum des pairs | Pairs au-dessus ou égaux | Centile | Pairs à zéro | p de rang, sans valeur de verdict |
|---|---|---|---|---|---|---|---|
| G1, wallets de la plus grande composante | 34 | 8 | 77 | 6 | 87,5 | 4,2 % | 0,143 |
| G2, part de l'offre tenue à S | 21,70 % | 3,77 % | 80,5 % | 4 | 91,7 | 25,0 % | 0,102 |
| G3, paires reliées | 50 | 23 | 114 | 8 | 83,3 | 4,2 % | 0,184 |

2 pairs sur 48 dépassent ou égalent DMAGA à la fois sur G1 et G2, 1 sur les trois mesures. Variantes, sans correction : V1 (5 M), G2 de DMAGA 13,5 %, 8 pairs au-dessus. V2 (sans retrait des services), G1 de DMAGA 34, 12 pairs au-dessus.

**Lecture.** Sur ces 48 tokens, un réseau de transferts directs entre gros acheteurs précoces est la règle, pas l'exception : seuls 4,2 % des pairs n'en ont aucun, et la moitié ont une composante d'au moins 8 wallets. Le réseau de DMAGA est dans le haut de la distribution, sans en être le maximum. **Ce n'est pas une conclusion d'équivalence :** le test est incomplet, et les 67 comparateurs restants peuvent déplacer ces chiffres. Cela interdit seulement d'écrire que l'existence d'un tel réseau est, à elle seule, atypique. Ce test ne dit rien de la série de retraits Coinbase ni du dépôt commun, qu'il ne mesure pas.

## Compteurs
- Couverture : 30 sur 30 pour DMAGA, médiane 30 chez les pairs, aucun pair sous 15, aucun NaN.
- Pairs à extension plafonnée (60 nouveaux wallets) : 10. À courbe tronquée (20 pages) : 10. DMAGA n'a ni l'un ni l'autre, avec 40 nouveaux wallets. Effet : la valeur de ces 10 pairs peut être sous-estimée, jamais celle de DMAGA.
- Réponses 429 : 3. Crédits comptés à 10 par requête, tarif repris d'une note du 02/11, non revalidé.
- Registre : 9 comparaisons réelles, seuil de Bonferroni 0,00556.

## Recoupement non prévu au plan
La méthode lit ici G1 = 34 et G2 = 21,70365 %, en partant de 30 wallets et sans connaître le groupe. L'audit C trouve, par une autre voie : 34 wallets avec la règle écrite (constat C-07) et 217,0365 M à 19:03:27 UTC. S vaut 19:00:00 UTC. Le recoupement valide la plomberie sur DMAGA, rien de plus.

## Deviations and data notes
1. **Gel de la table en retard.** La commande `gel.py ajouter` a échoué avant les tests par une erreur de shell : `derived/table.csv` et `derived/par_token.jsonl` n'ont été gelés qu'après le calcul de `tables/tests.json`, ce qui est écrit dans la raison de l'ajout au verrou. Heures : `par_token.jsonl` 11:15:38, `table.csv` 11:16:07, `tests.json` 11:16:09 UTC. Table non modifiée depuis.
2. **Plafond dépassé de 1 110 crédits**, car il n'est contrôlé qu'entre deux tokens, comme le permet le code gelé.
3. **Coût sous-estimé dans le plan.** Le plan prévoyait que 60 000 crédits suffiraient, sans le chiffrer par token, et cette estimation n'a pas été testée sur un pilote.

## Limites
Toutes celles du plan. Surtout : mesures choisies après avoir vu DMAGA, population conditionnée au pic tardif, ATA seuls, SOL non lu.

## Suite, à décider par Benjamin
Étendre le plafond serait un amendement, avec résultats déjà vus sur 48 comparateurs. Les comparateurs restants garderaient l'ordre tiré au hasard. Coût : environ 14 000 crédits pour atteindre k = 59, environ 84 000 pour k = 115. Même à k = 115, le meilleur test devrait valoir au plus 0,0167 : seul un DMAGA au-dessus de tous les pairs y arrive, car (1 + 1) / 116 = 0,0172. Or au moins 4 pairs lus sont déjà au-dessus sur G2, 6 sur G1, 8 sur G3. **Quelle que soit la suite de la collecte, le verdict ne pourrait être que « AUCUNE MESURE NE SORT DES PAIRS ».** Étendre le plafond n'apporterait qu'une description plus précise : je ne le recommande pas tant que le pool est aussi bas.
