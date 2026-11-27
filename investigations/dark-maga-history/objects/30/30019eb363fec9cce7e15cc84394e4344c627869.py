"""Offline regression checks for the 2026-11-06 pass-2 public X snapshot."""
import json
import tempfile
import unittest
from pathlib import Path

from scripts.audit_pass2_x_archive import (
    read_archive, read_leads, check_snapshot, FIVE_JEFFRO_ADDRESSES, source_time_ms
)


class HistoricalPass2Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.posts = read_archive()
        cls.leads = read_leads()

    def test_source_structure_and_deduplication(self):
        self.assertEqual(len(self.posts), 1001)
        self.assertEqual(len({p["author_id"] for p in self.posts.values()}), 374)
        self.assertEqual(len(self.leads), 24)

    def test_documented_claims_are_internally_consistent(self):
        result = check_snapshot(self.posts, self.leads)
        self.assertTrue(result["not_a_blockchain_audit"])
        self.assertEqual(result["comparator_mints_documented"], 4)
        self.assertEqual(result["resolved_jeffro_addresses"], 5)

    def test_corrupted_or_duplicate_jsonl_is_rejected(self):
        sample = self.posts["1815291795787690478"]
        with tempfile.TemporaryDirectory() as directory:
            p = Path(directory) / "DMAGA_X_ARCHIVE.part-001.jsonl"
            with p.open("w") as stream:
                stream.write(json.dumps(sample) + "\n" + json.dumps(sample) + "\n")
            with self.assertRaisesRegex(ValueError, "Duplicated post id"):
                read_archive(Path(directory))

    def test_missing_post_from_leads_fails_closed(self):
        mutated = dict(self.leads)
        mutated["T01"] = {**mutated["T01"], "source_post_id": "1"}
        with self.assertRaisesRegex(ValueError, "Comparator candidate T01"):
            check_snapshot(self.posts, mutated)

    def test_doc_upper_bound_is_not_an_avatar_click_time(self):
        post = self.posts["1815105812076904904"]
        self.assertEqual(post["created_at_utc"], "2024-07-21T19:25:23.000Z")
        self.assertEqual(post["author_handle"], "realjohnnewburg")
        self.assertIn("GTCNAerXYAA-ajC.png", post["media"][0]["url"])
        self.assertEqual(source_time_ms(post["id"]) // 1000,
                         1721590003)


if __name__ == "__main__":
    unittest.main()
