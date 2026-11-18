# Audit complémentaire : dépendance dans le contrôle aléatoire de la phase 1

Date : 2026-11-18. Base : branche main, sans modification des artefacts figés.

## Question

Le taux historique de 88,86 % sur des groupes de 40 wallets tirés au hasard
(`data/adverse/a1_null_model.json`) est-il un **taux de faux positifs sur
des groupes sans coordination** ?

**Réponse : le protocole actuel ne permet pas de l'affirmer.** Le tirage
`random.sample(pool, 40)` est effectué sur les wallets de seulement neuf
lancements. Il ne contraint pas le nombre de wallets par lancement. Il peut donc
reconstituer des paires de wallets d'un même lancement — précisément des paires
dont les relations financières sont l'objet de l'étude. Un groupe de quarante
wallets provenant de quarante lancements indépendants n'est pas constructible
avec le corpus présent.

## Recalcul descriptif, depuis les neuf fichiers originaux

- 136 wallets de neuf lancements (40 et 40 pour les deux plus grands).
- 114 funders non présents dans la liste de six infrastructures exclues.
- 34 paires de wallets partageant un funder **et** le même lancement.
- 14 paires de wallets partageant un funder, sur **des lancements différents**.
- La probabilité que deux wallets tirés du pool appartiennent au même
  lancement est `sum(comb(n_launch, 2)) / comb(136, 2) = 0.1996732026`.
- Un tirage de 40 wallets contient donc en moyenne 155,745 paires
  appartenant au même lancement (ce nombre concerne toutes les paires,
  pas uniquement celles qui partagent un funder).

Ces nombres sont des **propriétés de dépendance du jeu de contrôle**, non
une preuve de propriété commune. Les funders communs entre lancements
peuvent eux-mêmes être des infrastructures ou des acteurs récurrents.

## Vérification autonome

Depuis la racine du dépôt :

```bash
python3 research_validation/null_cohort_contamination.py
python3 -m pytest -q research_validation/test_null_cohort_contamination.py
```

Le programme utilise uniquement la bibliothèque standard, lit les fichiers
existants et imprime un rapport JSON. Il sépare les déclenchements du
critère **C** (funder partagé) en quatre catégories exclusives :
*within only*, *across only*, *both*, *neither*.

Il ne prétend pas réestimer les critères A et B du détecteur originel ni
déterminer une nouvelle valeur du taux de faux positifs. Les répétitions du
tirage chiffrent une **contamination potentielle**, pas une erreur métier
confirmée. Les tests avec données synthétiques ne valident pas les données
on-chain et sont rapportés comme tels.

## Expérience manquante, prioritaire

1. Constituer des contrôles temporellement appariés provenant d'au moins
   40 lancements distincts et exhaustivement observés, en séparant les
   wallets de l'opérateur, les hot wallets et les pools partagés.
2. Tirer au plus un wallet par lancement pour tester le faux lien financier ;
   construire en parallèle un contrôle de **groupes entiers de lancements**
   pour mesurer le seuil opérationnel du détecteur.
3. Geler le choix des groupes, les règles de hub, le timestamp et les
   variantes avant toute mesure de performance.
4. Rapporter la précision au niveau du **lancement**, avec couverture,
   intervalles par grappes, base rate, délai, et comparaison au baseline.
5. Conserver séparément les échecs d'attribution de wallets et l'absence
   d'avantage de trading. Invalider un contrôle négatif n'implique pas
   un signal rentable.

## Publication

Cette addition ne modifie aucun README préexistant, script original,
table, jeu de données, résultat négatif ou baseline de publication.
La PR historique #3 reste ouverte et n'est pas fusionnée.
