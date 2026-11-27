#!/bin/zsh
# Dérivé corrigé dans data_v2, étape par étape : chaque script prend le verrou commun sous le chien de garde. S'arrête à la première erreur.
set -e
cd "$(dirname "$0")/../../.."
export DMAGA_BIG="/Volumes/VERBATIM HD/Dark-MAGA-Investigation/data_v2"
step() {
  echo "=== $(date -u +%H:%M:%S) $*"
  python3 audits/2026-11-03/tools/heavy.py --rss-mo 1000 -- scripts/py.sh "$@"
}
for s in "$@"; do
  step ${=s}
done
echo "=== $(date -u +%H:%M:%S) FIN_OK"
