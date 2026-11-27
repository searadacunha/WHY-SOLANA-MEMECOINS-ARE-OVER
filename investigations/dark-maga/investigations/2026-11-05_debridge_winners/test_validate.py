"""Regressions for the concrete scope, hash and receipt errors in the draft."""

import copy
import csv
import json
import shutil
import tempfile
import unittest
from pathlib import Path

import validate as bridge


class BridgeEvidenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows = bridge.build_rows(bridge.ROOT / "evidence")

    def setUp(self):
        self.actual = copy.deepcopy(self.rows)

    def test_current_table_reconciles_to_pinned_evidence(self):
        result = bridge.validate()
        self.assertEqual(result["orders"], 76)
        self.assertEqual(result["source_total_usdc"], "1018687.178289")
        self.assertEqual(result["perimeters"]["groupe_33"], {"orders": 68, "source_total_usdc": "974077.946152"})
        self.assertEqual(result["destination_status"], {"archive_match_with_tx_hash": 31, "archive_match_without_tx_hash": 10, "unverified": 35})
        self.assertEqual(result["source_usdc_of_archived_matches"], "942534.318384")

    def test_extra_csv_cell_is_rejected(self):
        self.actual[0][None] = ["unexpected-extra-cell"]
        with self.assertRaisesRegex(bridge.ValidationError, "missing or extra fields"):
            bridge.validate_rows(self.actual, self.rows)

    def test_contract_address_cannot_masquerade_as_transaction_hash(self):
        row = next(r for r in self.actual if r["destination_match_status"] == "archive_match_without_tx_hash")
        row["destination_tx"] = "0xe7351fd770a37282b91d153ee690b63579d6dd7f"
        with self.assertRaisesRegex(bridge.ValidationError, "32-byte transaction hash"):
            bridge.validate_rows(self.actual, self.rows)

    def test_valid_length_but_unsubstantiated_hash_is_rejected(self):
        row = next(r for r in self.actual if r["destination_tx"])
        row["destination_tx"] = "0x" + "1" * 64
        with self.assertRaisesRegex(bridge.ValidationError, "destination_tx"):
            bridge.validate_rows(self.actual, self.rows)

    def test_bsc_requested_bnb_is_not_a_received_amount(self):
        rows = [r for r in self.rows if r["destination_chain_id"] == "56"]
        self.assertEqual(len(rows), 2)
        self.assertTrue(all(r["destination_match_status"] == "unverified" for r in rows))
        self.assertTrue(all(r["destination_amount_observed"] == r["destination_amount_observed_raw"] == "" for r in rows))
        row = next(r for r in self.actual if r["destination_chain_id"] == "56")
        row["destination_amount_observed"] = row["destination_amount_requested"]
        with self.assertRaisesRegex(bridge.ValidationError, "cannot claim a received amount"):
            bridge.validate_rows(self.actual, self.rows)

    def test_ten_archived_matches_do_not_gain_missing_fields(self):
        rows = [r for r in self.rows if r["destination_match_status"] == "archive_match_without_tx_hash"]
        self.assertEqual(len(rows), 10)
        self.assertTrue(all(not r["destination_tx"] and not r["destination_amount_observed_raw"] for r in rows))

    def test_same_hex_recipient_on_base_is_not_an_ethereum_match(self):
        recipient = "0xb29826d809aa04d2ead6f2310d8965a45b87fa67"
        eth = [r for r in self.rows if r["recipient"] == recipient and r["destination_chain_id"] == "1"]
        base = [r for r in self.rows if r["recipient"] == recipient and r["destination_chain_id"] == "8453"]
        self.assertEqual((len(eth), len(base)), (8, 8))
        self.assertEqual(sum(int(r["source_total_raw"]) for r in eth), 151360766904)
        self.assertEqual(sum(int(r["source_total_raw"]) for r in base), 21217495586)
        self.assertTrue(all(r["destination_match_status"] == "unverified" for r in base))

    def test_exact33_scope_uses_maker_instead_of_cache_filename(self):
        with (bridge.ROOT / "evidence/i14_orders.csv").open(newline="") as handle:
            sources = list(csv.DictReader(handle))
        members = bridge.exact_members(bridge.ROOT / "evidence")
        foreign_cache = [r for r in sources if r["maker"] in members and r["wallet_file"] not in members]
        self.assertEqual(len(foreign_cache), 4)
        actual = {r["source_signature"]: r for r in self.rows}
        for source in foreign_cache:
            self.assertEqual(actual[source["sig"]]["source_wallet"], source["maker"])
            self.assertEqual(actual[source["sig"]]["perimeter"], "groupe_33")

    def test_extended_cohort_egty_is_not_one_of_exact33(self):
        members = bridge.exact_members(bridge.ROOT / "evidence")
        self.assertNotIn("EGtyQEgMKGKXjppDqj9sYy97e9m7nvu1US4SfFXNakMy", members)
        self.assertNotIn("8YLEuUtZ4eFMJbf46oNb1CeG6dYFWGyxnQSh9hrgzBzR", members)
        row = next(r for r in self.actual if r["perimeter"] == "hors_33_P1")
        row["perimeter"] = "groupe_33"
        with self.assertRaisesRegex(bridge.ValidationError, "perimeter"):
            bridge.validate_rows(self.actual, self.rows)

    def test_source_debit_and_destination_receipt_remain_distinct(self):
        rows = [r for r in self.rows if r["recipient"] == "0xb947bf7f409e998b28f8e218802fc9575c3c8c57"]
        self.assertEqual(sum(int(r["source_total_raw"]) for r in rows), 263573151396)
        self.assertEqual(sum(int(r["destination_amount_observed_raw"]) for r in rows), 263320105094)

    def test_one_micro_usdc_error_fails_reconciliation(self):
        self.actual[0]["source_total_raw"] = str(int(self.actual[0]["source_total_raw"]) + 1)
        with self.assertRaisesRegex(bridge.ValidationError, "source_total_raw"):
            bridge.validate_rows(self.actual, self.rows)

    def test_duplicate_source_signature_fails(self):
        self.actual[1] = self.actual[0].copy()
        with self.assertRaisesRegex(bridge.ValidationError, "Duplicate source signature"):
            bridge.validate_rows(self.actual, self.rows)

    def test_before_mint_is_separate_from_execution_status(self):
        before = [r for r in self.rows if r["before_mint"] == "true"]
        self.assertEqual(len(before), 18)
        self.assertEqual(sum(int(r["source_total_raw"]) for r in before), 4632170480)
        self.assertNotIn("avant_mint", {r["destination_match_status"] for r in self.rows})

    def test_evidence_tamper_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            dest = Path(directory) / "evidence"
            shutil.copytree(bridge.ROOT / "evidence", dest)
            with (dest / "i14_orders.csv").open("ab") as handle:
                handle.write(b"\n")
            with self.assertRaisesRegex(bridge.ValidationError, "byte count changed"):
                bridge.verify_sources(dest)

    def test_manifest_cannot_silently_reanchor_evidence(self):
        with tempfile.TemporaryDirectory() as directory:
            dest = Path(directory) / "evidence"
            shutil.copytree(bridge.ROOT / "evidence", dest)
            path = dest / "source_manifest.json"
            manifest = json.loads(path.read_text())
            manifest["files"][0]["git_blob_sha"] = "0" * 40
            path.write_text(json.dumps(manifest))
            with self.assertRaisesRegex(bridge.ValidationError, "blob anchor changed"):
                bridge.verify_sources(dest)


if __name__ == "__main__":
    unittest.main()
