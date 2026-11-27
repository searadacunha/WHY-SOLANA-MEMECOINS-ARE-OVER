# Contrôle de la plomberie, transactions et graphes synthétiques

**Ce contrôle teste le code, pas la puissance.** Effets synthétiques choisis faciles à voir. Il ne dit rien de ce que le test détecterait sur la distribution réelle des pairs : celle-ci n'est pas connue au gel, elle sera rapportée avec les résultats.

Assertions passées : dérivation ATA contre un triple relu dans le brut de DMAGA, 11 cas de transferts (pur, multi-receveurs, seuil, échec, ambigu, somme fausse, swap par le SOL, swap par un autre mint, loyer), 5 cas de mesures, verdict à k = 58 et 59, rang avec NaN.

| Effet | Tirages | Verdict inhabituel | k |
|---|---|---|---|
| nul | 200 | 4 | 115 |
| fort | 200 | 200 | 115 |
