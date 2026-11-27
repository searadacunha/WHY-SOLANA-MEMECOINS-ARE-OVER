#!/bin/zsh
# Un processus par token : la mémoire repart de zéro. Reprise via les CSV.
cd REDACTED_HOME/Projects/Dark-MAGA-Investigation
python3 - <<'PY' > audits/2026-11-03/work_B/b03_pools.txt
import json
seen=[]
for l in open("audits/2026-11-03/work_B/b02_stats.jsonl"):
    p=json.loads(l)["pool"]
    if p not in seen: seen.append(p)
print("\n".join(seen))
PY
fails=0
while read -r p; do
  python3 scripts/guard.py --rss-mo 300 -- scripts/py.sh audits/2026-11-03/work_B/b03_metrics.py "$p" >> audits/2026-11-03/work_B/b03_metrics.log 2>&1 || { echo "ECHEC $p" >> audits/2026-11-03/work_B/b03_metrics.log; fails=$((fails+1)); }
done < audits/2026-11-03/work_B/b03_pools.txt
echo "FINI echecs=$fails"
