"""Root-level wrapper so the repo CI (`python -m pytest -q tests`) also runs the ASTRA offline tests.
Place at tests/test_astra_launch_team.py. Stdlib only, no network."""
import importlib.util, os, sys
_DIR = os.path.join(os.path.dirname(__file__), '..', 'investigations', '2026-11-18_astra_team_promoters_beneficiaries', 'tests')
_spec = importlib.util.spec_from_file_location('astra_offline', os.path.join(_DIR, 'test_astra_offline.py'))
_mod = importlib.util.module_from_spec(_spec); sys.modules['astra_offline'] = _mod; _spec.loader.exec_module(_mod)
for _name in dir(_mod):
    _obj = getattr(_mod, _name)
    if isinstance(_obj, type) and _name in ('Snowflakes', 'G41vFailedReceipts', 'PumpPhaseRebuild', 'CoinbaseBatch', 'Integrity'):
        globals()['Astra' + _name] = _obj
