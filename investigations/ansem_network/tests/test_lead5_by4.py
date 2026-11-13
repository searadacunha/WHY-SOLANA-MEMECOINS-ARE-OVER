"""Lead 5 (LEAD5_BY4StcU9.md): the service test on BY4StcU9 is rebuilt from the saved raw transactions. Offline."""
from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "code"))

import ana_70_by4_service as lead5  # noqa: E402

B58 = re.compile(r"[1-9A-HJ-NP-Za-km-z]{32,88}")


def test_numbers_are_rebuilt_from_raw():
    assert json.loads(json.dumps(lead5.build())) == json.loads((ROOT / "evidence" / "lead5_by4.json").read_text())


def test_each_sample_holds_1000_distinct_successful_transactions():
    sigs, txs = lead5.load(lead5.SIGS), lead5.load(lead5.TXS)
    for k in ("A", "B"):
        s = sigs[k]["signatures"]
        assert len(s) == len(set(s)) == 1000
        assert all(txs[x]["meta"]["err"] is None and txs[x]["transaction"]["signatures"][0] == x for x in s)
    assert not set(sigs["A"]["signatures"]) & set(sigs["B"]["signatures"])


def test_curve_check_passes_every_signer_and_about_half_of_random_keys():
    """Signers must be curve points; a random 32-byte string is one about half the time."""
    signers = set()
    for tx in lead5.load(lead5.TXS).values():
        m = tx["transaction"]["message"]
        signers.update(m["accountKeys"][:m["header"]["numRequiredSignatures"]])
    assert signers and all(lead5.on_curve(k) for k in signers)
    rnd = [lead5.D.b58encode(hashlib.sha256(b"%d" % i).digest()) for i in range(400)]
    assert 0.4 < sum(map(lead5.on_curve, rnd)) / len(rnd) < 0.6


def test_every_address_in_the_note_comes_from_the_data():
    """An address completed by hand would appear nowhere in the measured output or the raw transactions."""
    note = (ROOT / "LEAD5_BY4StcU9.md").read_text()
    data = (ROOT / "evidence" / "lead5_by4.json").read_text() + json.dumps(lead5.load(lead5.TXS))
    for a in set(B58.findall(note)):
        assert a in data, a
    assert "—" not in note
    res = json.loads((ROOT / "evidence" / "lead5_by4.json").read_text())
    for k in ("A_up_to_the_funding_of_the_deployer", "B_most_recent"):
        assert "**%d**" % res[k]["counterparties_strict"] in note and res[k]["verdict"] == "service by the plan's test"
