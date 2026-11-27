"""Protect both archived protocols, including the code they freeze outside the study."""
import hashlib
import json
from pathlib import Path

import pytest


@pytest.mark.parametrize("study", ["etude_final", "etude_groupe"])
def test_frozen_files_match_their_recorded_hashes(study):
    directory = Path(__file__).resolve().parents[1] / study
    lock = json.loads((directory / "PROTOCOL.lock").read_text())
    assert lock["fichiers"]
    for name, expected in lock["fichiers"].items():
        path = directory / name
        assert path.is_file(), name
        assert hashlib.sha256(path.read_bytes()).hexdigest() == expected, name
