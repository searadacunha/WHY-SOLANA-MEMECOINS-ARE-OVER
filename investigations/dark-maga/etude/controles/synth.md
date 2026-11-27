# Contrôles positifs, tokens synthétiques

k = 150 comparateurs par tirage, 40 graines par effet.

| effet | verdict inhabituel | tirages | taux | mesures qui passent Holm au moins une fois |
|---|---|---|---|---|
| nul | 2 | 40 | 0.05 | M1:1, M6:1 |
| moyen | 40 | 40 | 1.00 | M1:38, M2:26, M3:39, M4:5, M5:37, M6:1, M7:13 |
| fort | 40 | 40 | 1.00 | M1:40, M2:40, M3:40, M5:40, M6:1, M7:40 |
| baleine | 40 | 40 | 1.00 | M1:29, M2:40, M3:40, M4:40, M6:1, M7:40 |
| precoces | 40 | 40 | 1.00 | M1:1, M6:40 |

Règle du nul : taux ≤ 0,10 attendu avec Holm à 0,05 sur 7 mesures, observé 0.05.

Puissance : k = 139 est le minimum pour qu'un test puisse passer ; le verdict l'exige.
k = 50 rend bien l'inconclusif : INCONCLUSIF (puissance) : 50 comparateur.
