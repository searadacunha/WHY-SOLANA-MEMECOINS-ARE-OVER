#!/bin/zsh
# Télécharge pool puis mint sur [since, until). Résumable : relancer la même commande reprend.
set -eu
cd "$(dirname "$0")/.."
/opt/homebrew/bin/python3.12 scripts/col_02_full.py --source pool --since "$1" --until "$2" --workers 5 --rps 5
/opt/homebrew/bin/python3.12 scripts/col_02_full.py --source mint --since "$1" --until "$2" --workers 5 --rps 5
