"""Adversarial Solana log attribution checks, with no network or mutable evidence."""
import base64
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import sol_dln as S


class SolanaOrderEvents(unittest.TestCase):
    oid = "0x" + "12" * 32
    foreign = "11111111111111111111111111111111"

    def receipt(self, program=S.DESTINATION):
        payload = ("Program log: Order Id: " + self.oid if program == S.DESTINATION else
                   "Program data: " + base64.b64encode(S.CREATED_ID + bytes.fromhex(self.oid[2:])).decode())
        return {"meta": {"err": None, "logMessages": [f"Program {program} invoke [1]", payload,
                                                        f"Program {program} success"]}}

    def test_exact_source_and_destination_events(self):
        for program in (S.SOURCE, S.DESTINATION):
            with self.subTest(program=program):
                self.assertEqual(S.order_ids(self.receipt(program), program), {self.oid})

    def test_decimal_ids_preserve_all_256_bits(self):
        tx = self.receipt()
        tx["meta"]["logMessages"][1] = "Program log: Order Id: " + str(int(self.oid, 16))
        self.assertEqual(S.order_ids(tx, S.DESTINATION), {self.oid})

    def test_failed_or_missing_status_does_not_prove_execution(self):
        for meta in ({"err": {}}, {}):
            tx = self.receipt()
            tx["meta"].pop("err")
            tx["meta"].update(meta)
            self.assertEqual(S.order_ids(tx, S.DESTINATION), set())

    def test_same_id_printed_by_a_nested_foreign_program_is_not_dln(self):
        tx = self.receipt()
        logs = tx["meta"]["logMessages"]
        logs[1:2] = [f"Program {self.foreign} invoke [2]", logs[1], f"Program {self.foreign} success"]
        self.assertEqual(S.order_ids(tx, S.DESTINATION), set())

    def test_caught_inner_failure_discards_its_events(self):
        tx = self.receipt()
        logs = tx["meta"]["logMessages"]
        logs[0] = f"Program {S.DESTINATION} invoke [2]"
        logs[-1] = f"Program {S.DESTINATION} failed: custom program error: 0x1"
        tx["meta"]["logMessages"] = [f"Program {self.foreign} invoke [1]", *logs,
                                       f"Program {self.foreign} success"]
        self.assertEqual(S.order_ids(tx, S.DESTINATION), set())

    def test_later_failed_parent_also_discards_a_successful_child_event(self):
        tx = self.receipt()
        logs = tx["meta"]["logMessages"]
        logs[0] = f"Program {S.DESTINATION} invoke [3]"
        tx["meta"]["logMessages"] = [f"Program outer invoke [1]", f"Program parent invoke [2]",
                                       *logs, "Program parent failed: custom program error: 0x1", "Program outer success"]
        self.assertEqual(S.order_ids(tx, S.DESTINATION), set())

    def test_truncated_source_event_and_log_stack_fail(self):
        tx = self.receipt(S.SOURCE)
        tx["meta"]["logMessages"][1] = "Program data: " + base64.b64encode(S.CREATED_ID + b"1").decode()
        with self.assertRaisesRegex(ValueError, "Truncated"):
            S.order_ids(tx, S.SOURCE)
        tx = self.receipt()
        tx["meta"]["logMessages"].pop()
        with self.assertRaisesRegex(ValueError, "Incomplete"):
            S.order_ids(tx, S.DESTINATION)


if __name__ == "__main__":
    unittest.main()
