"""Pass-3 documentary consistency tests: no web or chain access."""
import json
import tempfile
import unittest
from pathlib import Path
from scripts.audit_pass3_x_archive import load_delta, check


class Pass3HistoricalCorpusTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.posts = load_delta()

    def test_source_counts_and_provenance(self):
        result = check(self.posts)
        self.assertEqual(result["posts"], 316)
        self.assertEqual(result["authors"], 148)
        self.assertEqual(result["media_originals_reported"], 19)
        self.assertTrue(result["not_chain_verification"])

    def test_repeat_id_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            for i in range(1, 5):
                path = Path(temp) / f"DMAGA_PASS3_DELTA.part-{i:03d}.jsonl"
                entry = next(iter(self.posts.values()))
                path.write_text(json.dumps(entry) + "\n")
            with self.assertRaisesRegex(ValueError, "Duplicate post"):
                load_delta(Path(temp))

    def test_missing_author_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            for i in range(1, 5):
                path = Path(temp) / f"DMAGA_PASS3_DELTA.part-{i:03d}.jsonl"
                entry = dict(next(iter(self.posts.values())))
                entry["id"] = str(int(entry["id"]) + i * (1 << 22))
                entry["post_id"] = entry["id"]
                entry["author_id"] = None
                path.write_text(json.dumps(entry) + "\n")
            with self.assertRaisesRegex(ValueError, "missing author"):
                load_delta(Path(temp))


if __name__ == "__main__":
    unittest.main()
