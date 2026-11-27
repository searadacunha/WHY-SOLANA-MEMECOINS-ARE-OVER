#!/usr/bin/env python3
"""Offline audit of X post provenance. Never infers an author from a CDX URL.

Observations are flags for manual inspection, not accusations or verified reposts.
Does not contact X, modify input, or change trading-window boundaries.
"""
from __future__ import annotations

import argparse
from collections import Counter
from datetime import datetime, timezone
import json
from pathlib import Path

X_EPOCH_MS = 1288834974657
KNOWN_REPOSTS = {
    "1814779160377602331": {
        "original_id": "1814763940410499481", "reposter": "DarkMagaCoin",
        "original_author": "pmarca",
    },
    "1813220461867573395": {
        "original_id": "1813086353741230327", "reposter": "DarkMagaCoin",
        "original_author": "kanpai",
    },
}


def snowflake_dt(value: str) -> datetime:
    number = int(value)
    if number <= 0:
        raise ValueError("nonpositive X post ID")
    return datetime.fromtimestamp(((number >> 22) + X_EPOCH_MS) / 1000, timezone.utc)


def parse_dt(value):
    if value is None or value == "":
        return None
    if isinstance(value, (int, float)):
        seconds = value / 1000 if value > 10**11 else value
        return datetime.fromtimestamp(seconds, timezone.utc)
    if isinstance(value, str):
        try:
            return datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(timezone.utc)
        except ValueError:
            return None
    return None


def explicit_references(record):
    """Read explicit X references only; text beginning 'RT' is not proof."""
    references = []
    for part in [record, record.get("data"), record.get("tweet"), record.get("raw")]:
        if not isinstance(part, dict):
            continue
        for field in ("referenced_tweets", "referencedTweets"):
            values = part.get(field)
            if isinstance(values, list):
                for item in values:
                    if isinstance(item, dict):
                        rid = item.get("id") or item.get("tweet_id")
                        if rid:
                            references.append({"id": str(rid), "type": item.get("type", "unknown")})
    return references


def audit_record(record):
    post_id = str(record.get("id") or record.get("post_id") or "")
    result = {"id": post_id, "flags": [], "explicit_references": explicit_references(record)}
    if not post_id.isdigit():
        result["flags"].append("missing_or_invalid_post_id")
        return result
    snow = snowflake_dt(post_id)
    result["snowflake_utc"] = snow.isoformat()
    raw_metadata = record.get("created_utc_metadata")
    metadata = parse_dt(raw_metadata)
    if raw_metadata not in (None, "") and metadata is None:
        result["flags"].append("unparseable_metadata_timestamp")
    elif metadata is not None and abs((metadata - snow).total_seconds()) > 2:
        result["flags"].append("metadata_snowflake_disagree")
        result["metadata_utc"] = metadata.isoformat()
    if post_id in KNOWN_REPOSTS:
        result["flags"].append("historical_repost_requires_source_review")
        result["reported_repost"] = KNOWN_REPOSTS[post_id]
    if any(ref["type"] in ("retweeted", "retweet") for ref in result["explicit_references"]):
        result["flags"].append("explicit_retweet_reference")
    return result


def audit_file(path: Path, output: Path | None = None):
    counters = Counter()
    samples = []
    anomalies = []
    with path.open(encoding="utf-8") as stream:
        for line_number, line in enumerate(stream, 1):
            if not line.strip():
                continue
            counters["rows"] += 1
            try:
                record = json.loads(line)
                if not isinstance(record, dict):
                    raise ValueError("JSONL row is not an object")
                finding = audit_record(record)
            except (ValueError, TypeError, OverflowError) as exc:
                finding = {"id": "", "flags": ["malformed_row"], "reason": str(exc)}
            for flag in finding["flags"]:
                counters[flag] += 1
            if finding["flags"]:
                finding["line"] = line_number
                anomalies.append(finding)
                if len(samples) < 25:
                    samples.append(finding)
    if output:
        output.parent.mkdir(parents=True, exist_ok=True)
        with output.open("w", encoding="utf-8") as stream:
            for finding in anomalies:
                stream.write(json.dumps(finding, ensure_ascii=False) + "\n")
    return {
        "source": str(path), "counts": dict(counters),
        "sample": samples, "findings_file": str(output) if output else None,
        "note": "These flags require checking original X objects, referenced_tweets, and Wayback snapshots. Do not automatically change any trading cohort.",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=Path("data/x_posts.jsonl"))
    parser.add_argument("--output", type=Path, default=None,
                        help="Optional JSONL file for all flagged records (does not overwrite input)")
    args = parser.parse_args()
    if not args.input.is_file():
        parser.error(f"input not found: {args.input}")
    print(json.dumps(audit_file(args.input, args.output), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
