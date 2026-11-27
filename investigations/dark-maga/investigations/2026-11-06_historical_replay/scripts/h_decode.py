"""Décodeur du rejeu : le module du dépôt `dmaga.spl` (issue #27), réexporté pour les scripts et tests de ce dossier."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from dmaga.spl import (WSOL, SYSTEM, TOKEN, TOKEN22, b58e, bstr, instructions, keys, movements, programs,  # noqa: E402,F401
                       pump_create_event, signers, sol_delta, token_accounts, token_delta)
