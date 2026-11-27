#!/bin/zsh
# Auditeur A : reprise après les arrêts du garde.
cd REDACTED_HOME/Projects/Dark-MAGA-Investigation
W=audits/2026-11-03/work_A
python3 audits/2026-11-03/tools/heavy.py --rss-mo 1000 -- scripts/py.sh $W/a15_named.py > $W/out/a15_named.txt 2>&1
python3 audits/2026-11-03/tools/heavy.py --rss-mo 1000 -- scripts/py.sh $W/a13b_accounts.py > $W/out/a13b_accounts.txt 2>&1
python3 audits/2026-11-03/tools/heavy.py --rss-mo 1000 -- scripts/py.sh $W/a20_time.py > $W/out/a20_time.txt 2>&1
python3 audits/2026-11-03/tools/heavy.py --rss-mo 1000 -- scripts/py.sh $W/a18_misc.py > $W/out/a18_misc.txt 2>&1
python3 audits/2026-11-03/tools/heavy.py --rss-mo 1000 -- scripts/py.sh $W/a19_gaps.py > $W/out/a19_gaps.txt 2>&1
python3 audits/2026-11-03/tools/heavy.py --rss-mo 1000 -- scripts/py.sh $W/a21_ruptures.py > $W/out/a21_ruptures.txt 2>&1
