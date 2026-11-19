#!/usr/bin/env python3
"""Read-only point-in-time audit of the project's archived 211-row snipe log.

No third-party data or dependencies. Does not claim chain-RPC verification.
"""
import argparse
import json
import math
from pathlib import Path

SOURCE = Path(__file__).resolve().parents[2] / "data" / "snipe_log.json"
REQUIRED = {
    "mint", "detected_at", "detect_mc", "max_ath", "full_snipe",
    "reached_100k", "graduated", "is_snipe",
}
EXPECTED = {
    "rows": 211,
    "unique_mints": 211,
    "full_snipe": 100,
    "non_full_snipe": 111,
    "positive_lifetime_label": 74,
    "full_and_positive": 69,
    "nonfull_and_positive": 5,
    "timestamp_zero": 31,
    "already_at_100k_at_detection": 32,
    "already_at_100k_full_and_positive": 32,
    "below_100k_and_timestamped": 148,
    "below_100k_and_timestamped_full": 58,
    "below_100k_and_timestamped_full_positive": 31,
    "below_100k_and_timestamped_nonfull": 90,
    "below_100k_and_timestamped_nonfull_positive": 5,
    "lifetime_label_mismatch": 0,
}


def load_rows(path):
    rows = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(rows, list) or not rows:
        raise ValueError("Expected a nonempty JSON list")
    seen = set()
    for i, row in enumerate(rows):
        if not isinstance(row, dict) or not REQUIRED.issubset(row):
            raise ValueError(f"Row {i}: missing required fields")
        mint = row["mint"]
        if not isinstance(mint, str) or not mint or mint in seen:
            raise ValueError(f"Row {i}: blank/duplicate mint")
        seen.add(mint)
        if any(type(row[k]) is not bool for k in ("full_snipe", "reached_100k", "graduated", "is_snipe")):
            raise ValueError(f"Row {i}: malformed Boolean field")
        for k in ("detect_mc", "max_ath", "detected_at"):
            v = row[k]
            if isinstance(v, bool) or not isinstance(v, (int, float)) or not math.isfinite(v) or v < 0:
                raise ValueError(f"Row {i}: invalid {k}")
    return rows


def summarize(rows):
    num = lambda pred: sum(bool(pred(r)) for r in rows)
    eligible = lambda r: r["detected_at"] > 0 and r["detect_mc"] < 100000
    summary = {
        "rows": len(rows),
        "unique_mints": len({r["mint"] for r in rows}),
        "full_snipe": num(lambda r: r["full_snipe"]),
        "non_full_snipe": num(lambda r: not r["full_snipe"]),
        "positive_lifetime_label": num(lambda r: r["reached_100k"]),
        "full_and_positive": num(lambda r: r["full_snipe"] and r["reached_100k"]),
        "nonfull_and_positive": num(lambda r: not r["full_snipe"] and r["reached_100k"]),
        "timestamp_zero": num(lambda r: r["detected_at"] == 0),
        "already_at_100k_at_detection": num(lambda r: r["detect_mc"] >= 100000),
        "already_at_100k_full_and_positive": num(
            lambda r: r["detect_mc"] >= 100000 and r["full_snipe"] and r["reached_100k"]
        ),
        "below_100k_and_timestamped": num(eligible),
        "below_100k_and_timestamped_full": num(lambda r: eligible(r) and r["full_snipe"]),
        "below_100k_and_timestamped_full_positive": num(
            lambda r: eligible(r) and r["full_snipe"] and r["reached_100k"]
        ),
        "below_100k_and_timestamped_nonfull": num(lambda r: eligible(r) and not r["full_snipe"]),
        "below_100k_and_timestamped_nonfull_positive": num(
            lambda r: eligible(r) and not r["full_snipe"] and r["reached_100k"]
        ),
        "lifetime_label_mismatch": num(
            lambda r: r["reached_100k"] != (r["max_ath"] >= 100000)
        ),
    }
    intervals = [(0, 20000), (20000, 40000), (40000, 60000),
                 (60000, 80000), (80000, 100000)]
    summary["point_in_time_price_strata"] = [
        {
            "detect_mc_from_inclusive": lo,
            "detect_mc_to_exclusive": hi,
            "n": num(lambda r: eligible(r) and lo <= r["detect_mc"] < hi),
            "full": num(lambda r: eligible(r) and lo <= r["detect_mc"] < hi and r["full_snipe"]),
            "nonfull": num(lambda r: eligible(r) and lo <= r["detect_mc"] < hi and not r["full_snipe"]),
            "full_lifetime_positive": num(
                lambda r: eligible(r) and lo <= r["detect_mc"] < hi and r["full_snipe"]
                and r["reached_100k"]
            ),
            "nonfull_lifetime_positive": num(
                lambda r: eligible(r) and lo <= r["detect_mc"] < hi and not r["full_snipe"]
                and r["reached_100k"]
            ),
        }
        for lo, hi in intervals
    ]
    return summary


def self_test():
    rows = [
        {"mint": "a", "detected_at": 1, "detect_mc": 15000, "max_ath": 130000,
         "full_snipe": False, "reached_100k": True, "graduated": False, "is_snipe": False},
        {"mint": "b", "detected_at": 2, "detect_mc": 110000, "max_ath": 110000,
         "full_snipe": True, "reached_100k": True, "graduated": True, "is_snipe": True},
    ]
    out = summarize(rows)
    assert out["already_at_100k_at_detection"] == 1
    assert out["below_100k_and_timestamped"] == 1
    assert out["lifetime_label_mismatch"] == 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="require the pinned archive counts")
    ap.add_argument("--self-test", action="store_true", help="run synthetic logic tests")
    args = ap.parse_args()
    if args.self_test:
        self_test()
        print("Synthetic tests passed")
        return
    result = summarize(load_rows(SOURCE))
    print(json.dumps(result, sort_keys=True, indent=2))
    if args.check:
        for key, value in EXPECTED.items():
            if result[key] != value:
                raise SystemExit(f"Snapshot mismatch: {key}: {result[key]} != {value}")


if __name__ == "__main__":
    main()
