#!/bin/zsh
# Enchaîne les recalculs après l'ajout d'historiques : un par un, verrou commun, journal sur le disque USB.
cd REDACTED_HOME/Projects/Dark-MAGA-Investigation
L="/Volumes/VERBATIM HD/Dark-MAGA-Investigation/audits_work/G/logs"
python3 scripts/guard.py --rss-mo 300 -- scripts/py.sh audits/2026-11-03/work_G/g02_moves.py > "$L/g02.log" 2>&1 || exit 1
python3 audits/2026-11-03/tools/heavy.py --rss-mo 1000 -- scripts/py.sh audits/2026-11-03/work_G/g04_ledger.py > "$L/g04.log" 2>&1 || exit 2
python3 audits/2026-11-03/tools/heavy.py --rss-mo 1000 -- scripts/py.sh audits/2026-11-03/work_G/g10_dest_scan.py > "$L/g10.log" 2>&1 || exit 3
python3 audits/2026-11-03/tools/heavy.py --rss-mo 600 -- scripts/py.sh audits/2026-11-03/work_G/g52_dca.py > "$L/g52.log" 2>&1 || exit 35
python3 scripts/guard.py --rss-mo 300 -- scripts/py.sh audits/2026-11-03/work_G/g51_sale_sources.py > "$L/g51.log" 2>&1 || exit 36
python3 scripts/guard.py --rss-mo 600 -- scripts/py.sh audits/2026-11-03/work_G/g30_deposits.py > "$L/g30.log" 2>&1 || exit 4
python3 scripts/guard.py --rss-mo 300 -- scripts/py.sh audits/2026-11-03/work_G/g43_misc.py > "$L/g43.log" 2>&1 || exit 41
python3 scripts/guard.py --rss-mo 300 -- scripts/py.sh audits/2026-11-03/work_G/g45_oneside.py > "$L/g45.log" 2>&1 || exit 42
python3 audits/2026-11-03/tools/heavy.py --rss-mo 800 -- scripts/py.sh audits/2026-11-03/work_G/g32_grappes.py > "$L/g32.log" 2>&1 || exit 5
python3 scripts/guard.py --rss-mo 500 -- scripts/py.sh audits/2026-11-03/work_G/g33_bridge.py > "$L/g33.log" 2>&1 || exit 6
python3 audits/2026-11-03/tools/heavy.py --rss-mo 1000 -- scripts/py.sh audits/2026-11-03/work_G/g40_boundaries.py > "$L/g40.log" 2>&1 || exit 7
python3 audits/2026-11-03/tools/heavy.py --rss-mo 1000 -- scripts/py.sh audits/2026-11-03/work_G/g42_a16.py > "$L/g42.log" 2>&1 || exit 8
python3 audits/2026-11-03/tools/heavy.py --rss-mo 1000 -- scripts/py.sh audits/2026-11-03/work_G/g46_junctions.py > "$L/g46.log" 2>&1 || exit 9
python3 audits/2026-11-03/tools/heavy.py --rss-mo 1000 -- scripts/py.sh audits/2026-11-03/work_G/g47_a16_pairs.py > "$L/g47.log" 2>&1 || exit 10
python3 scripts/guard.py --rss-mo 350 -- scripts/py.sh audits/2026-11-03/work_G/g49_hw.py > "$L/g49.log" 2>&1 || exit 11
python3 scripts/guard.py --rss-mo 500 -- scripts/py.sh audits/2026-11-03/work_G/g50_caw_links.py > "$L/g50.log" 2>&1 || exit 12
echo fini
