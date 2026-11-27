# Résultats de l'étude gelée

Plan : `analysis_plan.md`. Verdict calculé par `code/ana_90_verdict.py` : **DMAGA NON DISTINGUABLE DE SES PAIRS**.

Comptages : `derived/selection_counts.json`. Sortie complète : `tables/tests.json`. k = 211, 84 jours de pic distincts, cible n = 1.

| Mesure | DMAGA | Médiane des pairs | p de rang |
|---|---|---|---|
| M1 | 39,867 | 3,755 | 0,170 |
| M2 | 9,371 | 1,464 | 0,184 |
| M3 | 0,680 | 0,450 | 0,241 |
| M4 | 0,308 | 0,347 | 0,547 |
| M5 | 433,798 | 176,327 | 0,264 |
| M6 | 0,205 | 0,075 | 0,156 |
| M7 | 0,138 | 0,074 | 0,179 |

Holm sur 7 mesures : aucune ne passe. Une mesure ne pouvait passer que si DMAGA dépassait tous les comparateurs. Secondaire S1, Holm séparé : aucune. Registre : 33 comparaisons réelles.

## Deviations and data notes
- Amendement 001 : R1 et R2 limités aux comparateurs collectés, décidé par l'agent, sans Benjamin, à valider (amendement 002).
- `selection.jsonl` réordonné pour traiter d'abord les tokens principaux, sans changement de contenu.
- Le gel de la table a été ajouté après son calcul par le code gelé, avant les tests.
- Exploratoire hors plan : `tables/funder_share.json`.
- Audit à l'aveugle (fuites, statistiques, protocole) non réalisé : la porte d'audit n'est pas ouverte.
