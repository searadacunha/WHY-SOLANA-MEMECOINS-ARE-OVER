"""Regression tests for the standalone historical-X provenance scanner."""
import json
import tempfile
import unittest
from pathlib import Path

from scripts.audit_x_post_provenance import (
    KNOWN_REPOSTS, audit_file, audit_record, snowflake_dt,
)


class ReturnedObjectTests(unittest.TestCase):
    def test_repost_ids_resolve_to_their_original(self):
        from dmaga.xposts import returned_ids
        self.assertEqual(returned_ids("1814779160377602331"), {"1814763940410499481"})
        self.assertEqual(returned_ids("1813220461867573395"), {"1813086353741230327"})
        self.assertEqual(returned_ids("1815054750775173447"), {"1815054750775173447"})


class HistoricalXProvenanceTests(unittest.TestCase):
    def test_snowflake_is_original_post_timestamp(self):
        self.assertEqual(snowflake_dt("1814763940410499481").strftime("%Y-%m-%dT%H:%M:%S"), "2024-07-20T20:46:54")

    def test_known_repost_is_flagged_but_not_promoted_to_original(self):
        record = {"id": "1814779160377602331", "created_utc_metadata": "2024-07-20T21:47:23Z"}
        finding = audit_record(record)
        self.assertEqual(finding["reported_repost"]["original_id"], "1814763940410499481")
        self.assertIn("historical_repost_requires_source_review", finding["flags"])
        self.assertNotIn("metadata_snowflake_disagree", finding["flags"])

    def test_explicit_reference_is_not_assumed_from_text(self):
        record = {"id": "1813220461867573395", "text": "RT @kanpai:",
                  "referenced_tweets": [{"type": "retweeted", "id": "1813086353741230327"}]}
        self.assertIn("explicit_retweet_reference", audit_record(record)["flags"])
        other = {"id": "1813086353741230327", "text": "RT @someone: ..."}
        self.assertNotIn("explicit_retweet_reference", audit_record(other)["flags"])

    def test_metadata_mismatch_is_an_audit_flag_not_a_repost_verdict(self):
        finding = audit_record({"id": "1814763940410499481",
                                "created_utc_metadata": "2024-07-20T21:46:54Z"})
        self.assertIn("metadata_snowflake_disagree", finding["flags"])
        self.assertNotIn("historical_repost_requires_source_review", finding["flags"])

    def test_jsonl_output_without_mutating_input(self):
        with tempfile.TemporaryDirectory() as temp:
            input_file = Path(temp) / "posts.jsonl"
            output_file = Path(temp) / "flags.jsonl"
            original = json.dumps({"id": "1814779160377602331"}) + "\n"
            input_file.write_text(original, encoding="utf-8")
            summary = audit_file(input_file, output_file)
            self.assertEqual(summary["counts"]["rows"], 1)
            self.assertEqual(len(output_file.read_text().splitlines()), 1)
            self.assertEqual(input_file.read_text(encoding="utf-8"), original)


if __name__ == "__main__":
    unittest.main()
