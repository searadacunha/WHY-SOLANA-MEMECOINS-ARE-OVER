"""Offline regressions for the pre-buy RETIREDIO screening window.

Only the temporal predicate is asserted here. We do not silently rewrite the
historical 11/35 versus 4/149 screen, or claim every token debit is a swap.
"""
import csv
import sys
import unittest
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from h_time_rules import in_prebuy_window  # noqa: E402


def unix_utc(s):
    return int(datetime.strptime(s, "%Y-%m-%d %H:%M:%S").replace(tzinfo=timezone.utc).timestamp())


class PreBuyWindowTests(unittest.TestCase):
    def test_includes_valid_prebuy_debit(self):
        buy = unix_utc("2024-07-21 18:16:23")
        self.assertTrue(in_prebuy_window(buy - 50, buy))
        self.assertTrue(in_prebuy_window(buy - 3600, buy))

    def test_excludes_buy_time_and_future_debits(self):
        buy = unix_utc("2024-07-21 18:16:23")
        self.assertFalse(in_prebuy_window(buy, buy))
        self.assertFalse(in_prebuy_window(buy + 50, buy))
        self.assertFalse(in_prebuy_window(buy + 60, buy))

    def test_excludes_outside_lookback(self):
        buy = unix_utc("2024-07-21 18:16:23")
        self.assertFalse(in_prebuy_window(buy - 3601, buy))

    def test_invalid_window_fails_loudly(self):
        with self.assertRaises(ValueError):
            in_prebuy_window(1, 2, 0)

    def test_known_legacy_post_buy_false_positive(self):
        rows = list(csv.DictReader((ROOT / "data" / "rotation_retiredio.csv").open()))
        owner = "DpvWg6MaWAN9BTKKPheVTPPSxH7bdZ8ebU4q61Zo7THz"
        row = next(r for r in rows if r["owner"] == owner)
        self.assertEqual(row["rotation"], "True")  # stored legacy, not corrected
        self.assertEqual(int(row["sell_to_buy_s"]), -50)
        buy = unix_utc(row["first_dmaga_buy_utc"])
        sell = unix_utc(row["last_sell_utc"])
        self.assertEqual(sell - buy, 50)
        self.assertFalse(in_prebuy_window(sell, buy))


if __name__ == "__main__":
    unittest.main()
