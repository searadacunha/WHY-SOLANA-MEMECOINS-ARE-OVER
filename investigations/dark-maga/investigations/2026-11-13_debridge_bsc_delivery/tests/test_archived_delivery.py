"""Offline regression tests against the archived deBridge order and BSC receipts."""
import json
import sys
import unittest
from copy import deepcopy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from dm_debridge_ol07 import delivery_checks  # noqa: E402

CASES = (
    ("5c3a7f89a432aefd.json", "bb292c3356a7d477.json"),
    ("ab6fbeea17a85463.json", "3518c10ae703d328.json"),
)


class TestArchivedDelivery(unittest.TestCase):
    def test_both_archived_orders_pass(self):
        for detail_file, receipt_file in CASES:
            with self.subTest(detail=detail_file):
                d = json.loads((ROOT / "evidence" / detail_file).read_text())
                r = json.loads((ROOT / "evidence" / receipt_file).read_text())["result"]
                oid = d["orderId"]["stringValue"]
                self.assertTrue(delivery_checks(oid, d, r)["bsc_livraison_verifiee"])

    def test_unrelated_log_or_receiver_fails(self):
        d = json.loads((ROOT / "evidence" / CASES[0][0]).read_text())
        r = json.loads((ROOT / "evidence" / CASES[0][1]).read_text())["result"]
        oid = d["orderId"]["stringValue"]
        wrong_log = deepcopy(r)
        for log in wrong_log["logs"]:
            if log["address"].lower() == "0xe7351fd770a37282b91d153ee690b63579d6dd7f":
                log["address"] = "0x" + "1" * 40
        self.assertFalse(delivery_checks(oid, d, wrong_log)["bsc_livraison_verifiee"])
        wrong_receiver = deepcopy(d)
        wrong_receiver["receiverDst"]["stringValue"] = "0x" + "2" * 40
        self.assertFalse(delivery_checks(oid, wrong_receiver, r)["bsc_livraison_verifiee"])
        wrong_tx = deepcopy(r)
        wrong_tx["transactionHash"] = "0x" + "f" * 64
        self.assertFalse(delivery_checks(oid, d, wrong_tx)["bsc_livraison_verifiee"])


if __name__ == "__main__":
    unittest.main()
