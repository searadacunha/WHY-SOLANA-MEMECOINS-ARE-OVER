# Pourquoi ce dossier n'est pas l'étude : registre contaminé par un test, le 02/11/2026

Ce dossier est conservé tel quel, comme trace. L'étude utilisée est `../etude_final/`.

`code/ctl_02_e2e.py` plaçait le code réel avant la copie temporaire dans `sys.path`. Le test de bout en bout a donc écrit dans ce
dossier. Conséquences, toutes avant le gel et avant toute lecture de donnée réelle :
- `registre/tests.jsonl`, lignes 9 à 22 : étiquetées `reelles`, en réalité **synthétiques**.
- `derived/metrics.csv`, `derived/selection_counts.json`, `tables/tests.json` : synthétiques. Les pools s'y nomment `pool0000xxx…`
  et les valeurs de DMAGA y viennent de `build_token`, pas de la chaîne.

Aucun résultat de ce dossier n'a de valeur. Le registre n'a pas été réécrit : il ne se réécrit pas. Le test a été corrigé dans
`../etude_final/code/ctl_02_e2e.py` et contrôle désormais qu'il n'écrit rien hors de son dossier temporaire.
