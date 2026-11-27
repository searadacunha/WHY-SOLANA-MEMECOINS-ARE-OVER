#!/bin/zsh
# Recalcule tout le dérivé depuis le brut. S'arrête à la première erreur.
set -e
cd "$(dirname "$0")/.."
[ "${1:-}" = "--skip-norm" ] || { scripts/py.sh scripts/dis_05_venues.py | head -3; scripts/py.sh scripts/nrm_10_trades.py --force | tail -1; }
scripts/py.sh scripts/chk_20_vault_chain.py
scripts/py.sh scripts/chk_21_venue_chain.py
scripts/py.sh scripts/ana_19_export.py
scripts/py.sh scripts/ana_20_pnl.py
scripts/py.sh scripts/ana_21_token_edges.py
scripts/py.sh scripts/ana_22_nodes.py | head -2
scripts/py.sh scripts/ana_50_cohorts.py
echo DERIVE_OK
