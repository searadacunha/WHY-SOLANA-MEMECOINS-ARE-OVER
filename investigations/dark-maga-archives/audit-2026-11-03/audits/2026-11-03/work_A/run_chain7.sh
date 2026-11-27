#!/bin/zsh
cd REDACTED_HOME/Projects/Dark-MAGA-Investigation
W=audits/2026-11-03/work_A
python3 audits/2026-11-03/tools/heavy.py --rss-mo 1000 -- scripts/py.sh $W/a04_metrics.py > $W/out/a04_metrics.log 2>&1
