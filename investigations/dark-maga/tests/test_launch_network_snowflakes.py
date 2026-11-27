"""Sanity-check publicly encoded X ID times cited by a supplied report.

This does NOT verify post text, availability, source archive, or account identity.
"""
import datetime as dt
import unittest

X_EPOCH_MS = 1288834974657
CASES = {
    1812303793645666304: "2024-07-14T01:51:10",
    1812312706826854843: "2024-07-14T02:26:35",
    1812317575411351639: "2024-07-14T02:45:55",
    1815763101196636373: "2024-07-23T14:57:13",
    1794759622026486139: "2024-05-26T15:56:53",
    1829519827268153602: "2024-08-30T14:01:32",
}

class SnowflakeTimestampTests(unittest.TestCase):
    def test_x_post_id_utc_seconds(self):
        for post_id, expected in CASES.items():
            with self.subTest(post_id=post_id):
                ms = (post_id >> 22) + X_EPOCH_MS
                got = dt.datetime.fromtimestamp(
                    ms / 1000, tz=dt.timezone.utc
                ).isoformat(timespec="seconds").replace("+00:00", "")
                self.assertEqual(expected, got)

if __name__ == "__main__":
    unittest.main()
