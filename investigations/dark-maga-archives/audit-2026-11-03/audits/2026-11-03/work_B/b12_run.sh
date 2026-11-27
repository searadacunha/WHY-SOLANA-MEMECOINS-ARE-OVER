#!/bin/zsh
cd REDACTED_HOME/Projects/Dark-MAGA-Investigation
fails=0
while read -r p; do
  python3 scripts/guard.py --rss-mo 300 -- scripts/py.sh audits/2026-11-03/work_B/b12_features.py "$p" >> audits/2026-11-03/work_B/b12_features.log 2>&1 || { echo "ECHEC $p" >> audits/2026-11-03/work_B/b12_features.log; fails=$((fails+1)); }
done < audits/2026-11-03/work_B/b03_pools.txt
echo "FINI echecs=$fails"
