#!/usr/bin/env python3
"""Offline audit of imported Grok pass-3 documentary records.

It checks *internal source consistency*, NOT X authentication, media hashes,
transaction receipts, beneficial ownership, or insider trading.
"""
import argparse
import csv
from datetime import datetime
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DELTA = ROOT / "data" / "historical_x_pass3"
DOCS = ROOT / "docs" / "historical" / "pass3"
X_EPOCH_MS = 1288834974657


def load_delta(directory=DELTA):
    parts = sorted(Path(directory).glob("DMAGA_PASS3_DELTA.part-*.jsonl"))
    if len(parts) != 4:
        raise ValueError(f"Expected four ordered JSONL segments, found {len(parts)}")
    posts = {}
    for part in parts:
        with part.open(encoding="utf-8") as f:
            for line_no, line in enumerate(f, 1):
                if not line.strip():
                    continue
                try:
                    entry = json.loads(line)
                except json.JSONDecodeError as exc:
                    raise ValueError(f"{part.name}:{line_no}: bad JSON") from exc
                post_id = str(entry.get("id", ""))
                if not post_id.isdecimal() or entry.get("post_id") != post_id:
                    raise ValueError(f"{part.name}:{line_no}: invalid post ID")
                if post_id in posts:
                    raise ValueError(f"Duplicate post: {post_id}")
                if not entry.get("author_id") or not entry.get("author_handle"):
                    raise ValueError(f"{post_id}: missing author")
                source_url = entry.get("source_url", "")
                if not source_url.endswith("/status/" + post_id):
                    raise ValueError(f"{post_id}: source URL does not match id")
                try:
                    dt = datetime.fromisoformat(entry["created_at_utc"].replace("Z", "+00:00"))
                    assert dt.tzinfo is not None
                    delta_ms = abs(dt.timestamp() * 1000 - ((int(post_id) >> 22) + X_EPOCH_MS))
                except (KeyError, ValueError, AssertionError) as exc:
                    raise ValueError(f"{post_id}: invalid UTC time") from exc
                if delta_ms > 1100:
                    raise ValueError(f"{post_id}: metadata disagrees with Snowflake ({delta_ms:.1f} ms)")
                posts[post_id] = entry
    return posts


def table(filename, directory=DOCS):
    with (Path(directory) / filename).open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def check(posts, directory=DOCS):
    leads = table("DMAGA_PASS3_WALLET_LEADS.csv", directory)
    media = table("DMAGA_PASS3_MEDIA.csv", directory)
    graph = table("DMAGA_PASS3_SOURCE_GRAPH.csv", directory)
    if len(posts) != 316 or len({x["author_id"] for x in posts.values()}) != 148:
        raise ValueError("Unexpected source corpus size or author count")
    if len(leads) != 9 or len({x["lead_id"] for x in leads}) != 9:
        raise ValueError("Expected nine distinct leads")
    if len(media) != 24 or len(graph) != 182:
        raise ValueError("Unexpected media/graph row counts")
    if any(not x["financial_status"].startswith("NOT_CHAIN_VERIFIED") for x in leads):
        raise ValueError("A social lead is wrongly promoted to chain-confirmed")
    for row in leads:
        sid = row.get("source_post_id")
        # P3-02 reexamines a historical post already in baseline; others may refer
        # to other older sources. We validate the exact numeric ID, not presence in delta.
        if not sid or not sid.isdecimal():
            raise ValueError(f"Invalid lead source post: {row.get('lead_id')}")
        if row.get("transaction_signature_exact"):
            raise ValueError("New transfer signature unexpectedly asserted")
    for row in graph:
        if row.get("status") not in ("DOCUMENTARY_EDGE", "DERIVED_NOT_CHAIN_VERIFIED"):
            raise ValueError("Unclassified social edge")
        if not row.get("source_post_id", "").isdecimal():
            raise ValueError("Malformed X graph source")
    originals = sum(row.get("is_derived") == "False" for row in media)
    derivatives = sum(row.get("is_derived") == "True" for row in media)
    if (originals, derivatives) != (19, 5):
        raise ValueError("Unexpected reported original/derived media split")
    return {"posts":len(posts),"authors":len({x["author_id"] for x in posts.values()}),
            "leads":len(leads),"media_originals_reported":originals,
            "media_frames_reported":derivatives,"documentary_edges":len(graph),
            "not_chain_verification":True}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--delta",type=Path,default=DELTA)
    parser.add_argument("--docs",type=Path,default=DOCS)
    args=parser.parse_args()
    print(json.dumps(check(load_delta(args.delta),args.docs),indent=2))


if __name__ == "__main__":
    main()
