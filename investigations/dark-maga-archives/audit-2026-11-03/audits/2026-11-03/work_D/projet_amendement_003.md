# Projet d'amendement 003, 03/11/2026

**PROJET, non installé. Rédigé par l'auditeur D. La décision revient à Benjamin. Ce fichier ne doit pas être copié dans `etude_final/amendements/` sans son accord écrit.**

resultats_vus: oui

## Résultats déjà observés au moment de ce texte
- `etude_final/tables/verdict.json` : DMAGA NON DISTINGUABLE DE SES PAIRS.
- `etude_final/tables/tests.json` : M1 à M7, rangs, p, R1, R2, R3, S1.
- Audits A, B, C, D, dont la puissance sur vraies données : 2,4 % sans effet, 3,3 % à deux fois la réserve, 7,5 % pour le « fort » du contrôle (`audits/2026-11-03/work_D/d11_power.txt`).

Tout ce qui suit est donc écrit après résultats. Rien ne peut servir à changer le verdict.

## Ce qui ne change pas
Population principale, labels, cohortes, fenêtres, seuils, mesures M1 à M7, rang, Holm, texte du verdict, `metrics.csv`, `tests.json`, `verdict.json`, registre. Aucun recalcul n'est demandé par ce projet.

## Ce qui change
1. **Texte de l'amendement 001.** Remplacer, par ajout daté et sans réécrire 001, « l'ordre d'activité des pools, sans lien avec les mesures » par « l'ordre de création des pools, lien avec les mesures non testé au moment de la décision ». Raison : Spearman position et création 0,9995 sur les 310 tokens hors principal (`work_D/d30_amend.txt`).
2. **Statut de R1 et R2.** Les rapporter comme « variantes partielles, sans valeur de robustesse sur la bande ». R1 : k 212 sur 231 possibles. R2 : k 240 sur 498 possibles, 29 tokens sur 287 hors principal, tous créés du 15 au 23/06/2024. Raison : R2 ne teste pas la bande large.
3. **Comptage omis.** Publier `tronque_sans_S20` = 5, tous passés en `reporte_budget`. Le plan demande ce compteur, `selection_counts.json` ne l'a pas. Effet sur le verdict : nul.
4. **Fichier hors verrou.** Noter l'empreinte de `selection.jsonl` (écrit à 03:24:24 UTC le 03/11, avant `metrics.csv`) dans une annexe datée. Elle ne prouve pas l'état d'avant cette heure. Limite à écrire telle quelle.
5. **Phrase du plan.** Noter que « R3 le borne » ne décrit pas ce que fait R3 : S−1 h reste collé à un S déclenché par du spam. Ne pas réécrire le plan, ajouter la limite.
6. **Lecture du verdict.** Ajouter dans `results.md`, à côté du texte gelé inchangé, une section datée « interprétation d'audit » reprenant `CLAIM_VERIFICATION.csv`, ligne N09, et la table de puissance (N08).

## Ce que ce projet ne décide pas
- Valider ou rejeter l'amendement 001 : recommandation dans `AUDIT_FINAL.md`.
- Un seuil de puissance sur vraies données pour remplacer `k < 139` : il vaudrait pour une prochaine étude seulement, jamais pour celle-ci.
- Une collecte tirée au hasard, par tranche de capitalisation, parmi les 258 tokens reportés de R2 : ce serait un autre amendement, avec son budget.

## Pourquoi cet amendement serait utile
Ces points n'ouvrent aucune marge sur le résultat. Ils corrigent une description inexacte du protocole et une lecture trop forte de variantes annoncées comme robustesse.
