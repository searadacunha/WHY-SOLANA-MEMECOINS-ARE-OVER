#!/bin/zsh
cd REDACTED_HOME/Projects/Dark-MAGA-Investigation
W=audits/2026-11-03/work_A
python3 audits/2026-11-03/tools/heavy.py --rss-mo 1000 -- scripts/py.sh $W/a32_small.py > $W/out/a32_small.txt 2>&1
python3 audits/2026-11-03/tools/heavy.py --rss-mo 1000 -- scripts/py.sh $W/a29_flows.py > $W/out/a29_flows.txt 2>&1
