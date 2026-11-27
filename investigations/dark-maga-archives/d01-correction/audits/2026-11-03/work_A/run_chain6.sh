#!/bin/zsh
# Auditeur A : mesures et sensibilité, une fois a03 terminé.
cd REDACTED_HOME/Projects/Dark-MAGA-Investigation
W=audits/2026-11-03/work_A
python3 audits/2026-11-03/tools/heavy.py --rss-mo 1000 -- scripts/py.sh $W/a25_s1.py > $W/out/a25_s1.txt 2>&1
python3 audits/2026-11-03/tools/heavy.py --rss-mo 1000 -- scripts/py.sh $W/a04_metrics.py > $W/out/a04_metrics.log 2>&1
python3 audits/2026-11-03/tools/heavy.py --rss-mo 1000 -- scripts/py.sh $W/a05_sensitivity.py > $W/out/a05_sensitivity.log 2>&1
python3 audits/2026-11-03/tools/heavy.py --rss-mo 1000 -- scripts/py.sh $W/a42_roundtrip_peers.py > $W/out/a42_roundtrip_peers.log 2>&1
