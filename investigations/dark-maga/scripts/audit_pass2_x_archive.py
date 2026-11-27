#!/usr/bin/env python3
"""Read-only, offline consistency checks for the supplied DMAGA pass-2 X snapshot.

This checks source provenance, IDs, data shapes and cross-references. It DOES NOT
verify X API authenticity, media timestamps, Solana transfers, wallet ownership,
PnL or intent. Input rows are treated as untrusted historical observations.
"""
from __future__ import annotations

import argparse
import csv
from datetime import datetime, timezone
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ARCHIVE = ROOT / "data" / "historical_x_pass2"
DEFAULT_LEADS = ROOT / "docs" / "historical" / "pass2" / "DMAGA_WALLET_TWEET_LEADS.csv"
X_EPOCH_MS = 1288834974657
REQUIRED_POSTS = {
    "1815291795787690478": "JeffroBTC",  # full addresses
    "1815372294426124565": "Noah_nftn",
    "1815088124193579253": "dissident42069",
    "1815088727250858444": "dissident42069",
    "1815084272098697611": "DegenerateNews",
    "1815105812076904904": "realjohnnewburg",
}
REPOST_RELATIONS = {
    "1814779160377602331": "1814763940410499481",  # pmarca
    "1813220461867573395": "1813086353741230327",  # kanpai
    "1813004360592552354": "1812984492157771825",  # kanpai
    "1815004677160776126": "1814920352134537332",  # pmarca
}
COMPARATOR_MINTS = {
    "T01": ("1810386941180883011", "AUS4wtGQZcb6GPQxU4K8FRVqQMwUx2Q8G7K9JKuUpump"),
    "T02": ("1813651418471100660", "DyKwrqZMEDVHYAd4gn9V8vFioQQg1bVEgGxqbUr5Mkvo"),
    "T03": ("1798702410157973511", "HmAgiwjjP9CXqK5wQNsHKtjAt2CH3Kv8Q7xH5kGL2nqZ"),
    "T04": ("1814666414705274926", "9MBzpyMRkj2r5nTQZMMnxnCm5j1MAAFSYUtbSKjAF3WU"),
}
FIVE_JEFFRO_ADDRESSES = (
    "7GVCZAYG5NfiJsuqUdvc9hB2ts2W3tSrGdya4CyR1M5j",
    "9Sxmf25WG5WVQ5p86ycWeo5hMEwxiWPkFtLdRdTrHSQS",
    "A1UDMqcUC8RkZ8YENAktdueSQ6jxUUBickBK2y61vQ8J",
    "6QFDe4yu9mVhv3cbbaMtkTnakz4bGJLAjLjhwrMn5jqD",
    "H4mQu98TuxYTn3VSJone6jCTiDfXpuKcZbNZGHKUJU5y",
)


def source_time_ms(post_id: str) -> int:
    return (int(post_id) >> 22) + X_EPOCH_MS


def utc_ms(timestamp: str) -> int:
    d = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
    if d.tzinfo is None:
        raise ValueError("Naive timestamp")
    return round(d.timestamp() * 1000)


def read_archive(folder: Path = DEFAULT_ARCHIVE) -> dict[str, dict]:
    parts = sorted(folder.glob("DMAGA_X_ARCHIVE.part-*.jsonl"))
    if not parts:
        raise ValueError(f"No archive parts found in {folder}")
    posts: dict[str, dict] = {}
    for part in parts:
        with part.open(encoding="utf-8") as stream:
            for line_no, line in enumerate(stream, 1):
                if not line.strip():
                    continue
                try:
                    item = json.loads(line)
                except json.JSONDecodeError as error:
                    raise ValueError(f"{part.name}:{line_no}: invalid JSON") from error
                if not isinstance(item, dict):
                    raise ValueError(f"{part.name}:{line_no}: not an object")
                post_id = str(item.get("id") or "")
                if not post_id.isdecimal() or not item.get("author_id") or not item.get("author_handle"):
                    raise ValueError(f"{part.name}:{line_no}: missing id/author")
                if post_id in posts:
                    raise ValueError(f"Duplicated post id: {post_id}")
                if item.get("post_id") != post_id:
                    raise ValueError(f"{post_id}: post_id and id disagree")
                if item.get("created_at") != item.get("created_at_utc"):
                    raise ValueError(f"{post_id}: created_at and created_at_utc disagree")
                try:
                    skew = abs(utc_ms(item["created_at_utc"]) - source_time_ms(post_id))
                except (TypeError, KeyError, ValueError) as error:
                    raise ValueError(f"{post_id}: invalid post date") from error
                if skew > 1100:
                    raise ValueError(f"{post_id}: post date disagrees with ID ({skew} ms)")
                if not re.fullmatch("[0-9a-f]{64}", str(item.get("raw_sha256", ""))):
                    raise ValueError(f"{post_id}: missing/invalid *reported* source hash")
                posts[post_id] = item
    return posts


def read_leads(path: Path = DEFAULT_LEADS) -> dict[str, dict]:
    with path.open(newline="", encoding="utf-8") as stream:
        result = {}
        for row in csv.DictReader(stream):
            key = row.get("lead_id")
            if not key or key in result:
                raise ValueError(f"Missing/duplicate lead_id {key}")
            result[key] = row
        return result


def has_ref(post: dict, kind: str, target: str) -> bool:
    return any(str(r.get("id")) == target and r.get("type") == kind
               for r in post.get("references", []) if isinstance(r, dict))


def check_snapshot(posts: dict[str, dict], leads: dict[str, dict]) -> dict:
    """Check internal consistency; no claim of on-chain authentication."""
    for post_id, handle in REQUIRED_POSTS.items():
        if post_id not in posts or posts[post_id]["author_handle"].lower() != handle.lower():
            raise ValueError(f"Required historical post/author not found: {post_id}")
    for repost_id, original_id in REPOST_RELATIONS.items():
        if repost_id not in posts or original_id not in posts:
            raise ValueError(f"Missing repost pair: {repost_id} / {original_id}")
        if not has_ref(posts[repost_id], "reposted", original_id):
            raise ValueError(f"Invalid repost relationship {repost_id} -> {original_id}")
    a, b, parent = ("1815088124193579253",
                    "1815088727250858444", "1815084272098697611")
    if posts[a].get("references"):
        raise ValueError("A7 initial rotation post unexpectedly has references")
    if not has_ref(posts[b], "replied_to", parent):
        raise ValueError("A7 follow-up is not a reply to DegenerateNews")
    if any(str(ref.get("id")) in (a, b) for p in (posts[a], posts[b])
           for ref in p.get("references", []) if isinstance(ref, dict)):
        raise ValueError("Spurious reply edge between A7 posts")
    photo = posts["1815105812076904904"]
    if photo["created_at_utc"] != "2024-07-21T19:25:23.000Z":
        raise ValueError("Avatar documentary post time changed")
    if not any("GTCNAerXYAA-ajC.png" in str(media.get("url", ""))
               for media in photo.get("media", [])):
        raise ValueError("Avatar screenshot URL missing from supplied archive")
    jeffro = posts["1815291795787690478"]
    if not has_ref(jeffro, "replied_to", "1815291249102119198"):
        raise ValueError("Jeffro wallet list lacks its parent reply")
    for address in FIVE_JEFFRO_ADDRESSES:
        if address not in jeffro.get("text", ""):
            raise ValueError(f"Jeffro list missing address {address}")
    for key, (post_id, mint) in COMPARATOR_MINTS.items():
        lead = leads.get(key)
        if not lead or lead["address"] != mint or lead["source_post_id"] != post_id:
            raise ValueError(f"Comparator candidate {key} differs from its source")
        if mint not in posts[post_id].get("text", ""):
            raise ValueError(f"Comparator {key} mint absent from source post text")
    for key, row in leads.items():
        if row.get("source_post_id") not in posts:
            raise ValueError(f"Lead {key} references a post missing from the archive")
        if row.get("evidence_status") != "SOCIAL_CLAIM_NOT_CHAIN_VERIFIED":
            raise ValueError(f"Lead {key} unexpectedly claims independent chain verification")
    return {
        "posts": len(posts),
        "unique_authors": len({row["author_id"] for row in posts.values()}),
        "leads": len(leads),
        "repost_pairs_checked": len(REPOST_RELATIONS),
        "resolved_jeffro_addresses": len(FIVE_JEFFRO_ADDRESSES),
        "comparator_mints_documented": len(COMPARATOR_MINTS),
        "avatar_post_utc": photo["created_at_utc"],
        "source_provenance_only": True,
        "not_a_blockchain_audit": True,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--archive-dir", type=Path, default=DEFAULT_ARCHIVE)
    parser.add_argument("--leads-csv", type=Path, default=DEFAULT_LEADS)
    args = parser.parse_args()
    result = check_snapshot(read_archive(args.archive_dir), read_leads(args.leads_csv))
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
