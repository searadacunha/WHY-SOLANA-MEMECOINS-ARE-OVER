"""A failing producer in a shell pipeline must stop the derivation."""
import os
from pathlib import Path
import subprocess

import pytest


@pytest.fixture
def runner(tmp_path):
    scripts = tmp_path / "scripts"
    scripts.mkdir()
    source = Path(__file__).resolve().parents[1] / "scripts" / "run_derive.sh"
    (scripts / "run_derive.sh").write_text(source.read_text())
    stub = scripts / "py.sh"
    stub.write_text("""#!/usr/bin/env bash
printf '%s\\n' "$1" >> "$AUDIT_CALLS"
if [ "$1" = "${FAIL_STAGE:-}" ]; then exit 42; fi
printf 'one\\ntwo\\nthree\\nfour\\nfive\\n'
""")
    stub.chmod(0o755)
    return tmp_path


@pytest.mark.parametrize("stage", ["dis_05_venues.py", "nrm_10_trades.py", "ana_22_nodes.py"])
def test_pipeline_failure_is_not_reported_as_success(runner, stage):
    log = runner / "calls.txt"
    env = {**os.environ, "DMAGA_BIG": str(runner / "out"),
           "AUDIT_CALLS": str(log), "FAIL_STAGE": "scripts/" + stage}
    result = subprocess.run(["bash", str(runner / "scripts" / "run_derive.sh")],
                            env=env, capture_output=True, text=True, timeout=10)
    assert result.returncode == 42
    assert "DERIVE_OK" not in result.stdout
    assert log.read_text().splitlines()[-1] == "scripts/" + stage


def test_successful_pipeline_runs_all_stages(runner):
    log = runner / "calls.txt"
    env = {**os.environ, "DMAGA_BIG": str(runner / "out"),
           "AUDIT_CALLS": str(log), "FAIL_STAGE": ""}
    result = subprocess.run(["bash", str(runner / "scripts" / "run_derive.sh")],
                            env=env, capture_output=True, text=True, timeout=10)
    assert result.returncode == 0, result.stderr
    assert result.stdout.rstrip().endswith("DERIVE_OK")
    assert log.read_text().splitlines()[-1] == "scripts/ana_30_flows.py"
