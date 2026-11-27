#!/bin/zsh
# Auditeur A : calculs lourds à la suite, chacun sous le verrou commun.
cd REDACTED_HOME/Projects/Dark-MAGA-Investigation
W=audits/2026-11-03/work_A
python3 audits/2026-11-03/tools/heavy.py --rss-mo 1000 -- scripts/py.sh $W/a15_named.py > $W/out/a15_named.txt 2>&1
python3 audits/2026-11-03/tools/heavy.py --rss-mo 1000 -- scripts/py.sh $W/a20_time.py > $W/out/a20_time.txt 2>&1
python3 audits/2026-11-03/tools/heavy.py --rss-mo 1000 -- scripts/py.sh $W/a16_labels.py > $W/out/a16_labels.txt 2>&1
python3 audits/2026-11-03/tools/heavy.py --rss-mo 1000 -- scripts/py.sh $W/a14_pnl.py > $W/out/a14_pnl.log 2>&1
