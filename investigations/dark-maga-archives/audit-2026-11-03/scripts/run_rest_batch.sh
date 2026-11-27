#!/bin/zsh
# Tout l'historique après le 24/07/2024, pool puis mint, par calendrier. Résumable.
cd "$(dirname "$0")/.."
/opt/homebrew/bin/python3.12 scripts/col_02_full.py --calendar --source pool --since 1721779200 --workers 6 --rps 7
/opt/homebrew/bin/python3.12 scripts/col_02_full.py --calendar --source mint --since 1721779200 --workers 6 --rps 7
