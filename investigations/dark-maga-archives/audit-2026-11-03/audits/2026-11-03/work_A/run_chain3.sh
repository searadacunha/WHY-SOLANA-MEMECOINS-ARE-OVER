#!/bin/zsh
cd REDACTED_HOME/Projects/Dark-MAGA-Investigation
W=audits/2026-11-03/work_A
python3 audits/2026-11-03/tools/heavy.py --rss-mo 1000 -- scripts/py.sh $W/a23_group.py > $W/out/a23_group.txt 2>&1
python3 audits/2026-11-03/tools/heavy.py --rss-mo 1000 -- scripts/py.sh $W/a24_roundtrip.py > $W/out/a24_roundtrip.txt 2>&1
python3 audits/2026-11-03/tools/heavy.py --rss-mo 1000 -- scripts/py.sh $W/a26_hidden.py > $W/out/a26_hidden.txt 2>&1
