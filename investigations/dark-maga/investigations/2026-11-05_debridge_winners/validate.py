#!/usr/bin/env python3
"""Rebuild and check the bridge table against pinned, committed audit outputs.

This is an offline consistency check, not a raw-RPC decoder or a live-chain
execution check. No third-party packages, API keys or external archive required.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import sys
from collections import Counter
from decimal import Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SOURCE_COMMIT = "933ebe8afc0558a2406b189a272311df060aef7a"
SOURCE_REPO = "searadacunha/Dark-MAGA"
MINT_UTC = "2024-07-14T02:05:25Z"
USDC_SOLANA = "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"
ZERO = "0x" + "0" * 40
ADDRESS = re.compile(r"0x[0-9a-f]{40}\Z")
TX_HASH = re.compile(r"0x[0-9a-f]{64}\Z")
BASE58 = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
CHAIN_NAMES = {"1": "Ethereum", "8453": "Base", "56": "BSC", "137": "Polygon", "42161": "Arbitrum"}
ASSETS = {
    ("1", ZERO): ("ETH", 18),
    ("8453", ZERO): ("ETH", 18),
    ("56", ZERO): ("BNB", 18),
    ("137", ZERO): ("MATIC", 18),
    ("1", "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48"): ("USDC", 6),
    ("8453", "0x833589fcd6edb6e08f4c7c32d4f71b54bda02913"): ("USDC", 6),
    ("42161", "0xaf88d065e77c8cc2239327c5edb3a432268e5831"): ("USDC", 6),
}
OUTSIDE = {
    "DfYyxDNEXBzZWVPuJrNfko1rDrtR8SiqWLeGUMmNn8DT": "hors_33_P1",
    "8YSi5yNRN2KMbGU7Q3i5w9W6fTRxnk1qatQ5YmzS5da7": "hors_33_aval_H3QsBr",
    "7SEoKiBLaGhZxr5V8JYGdiV55ZhkgC727ftSYDST148i": "hors_33_neuf_post_Musk",
    "J2EuNwCSDfFGUhmpWdnoEgZKA17b4dgE9PQVY3jMFiQ3": "hors_33_neuf_post_Musk",
}
SOURCE_FILES = {
    "i14_orders.csv": "audits/2026-11-03/work_I/i14_orders.csv",
    "i21_evm_fill.txt": "audits/2026-11-03/work_I/i21_evm_fill.txt",
    "i22_evm_rest.txt": "audits/2026-11-03/work_I/i22_evm_rest.txt",
    "group_split.json": "data/group_split.json",
}
PINNED_BLOBS = {
    "i14_orders.csv": "2daecd013a7c53f1d1e738e11ef1ae71dd8d1c0a",
    "i21_evm_fill.txt": "68a137b7b21b80a39e318ea7329566d01931d115",
    "i22_evm_rest.txt": "3fdd722ce7f1faf920752d0335be0f8519dafdb5",
    "group_split.json": "b4f7df7cb01d4dc8f8ce3e5e333e558db1f6c79c",
}
FIELDS = [
    "order_index", "perimeter", "source_wallet", "source_signature",
    "source_time_utc", "source_instruction", "source_nonce", "source_token",
    "source_amount_raw", "source_proportional_fee_raw", "source_total_raw",
    "source_total_usdc", "source_fixed_fee_lamports", "before_mint",
    "destination_chain_id", "destination_chain", "recipient", "destination_token",
    "destination_asset", "destination_amount_requested_raw", "destination_amount_requested",
    "destination_match_status", "destination_tx", "destination_amount_observed_raw",
    "destination_amount_observed", "destination_payment_contract", "destination_delay_seconds",
    "source_evidence", "destination_evidence",
]


class ValidationError(ValueError):
    """A table, provenance or archived matching inconsistency."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValidationError(message)


def units(raw: str | int, decimals: int) -> str:
    """Exact decimal string without floating-point conversion."""
    return format(Decimal(int(raw)).scaleb(-decimals), f".{decimals}f")


def check_base58(value: str, length: int, label: str) -> None:
    require(bool(value) and all(c in BASE58 for c in value), f"Invalid {label}")
    number = 0
    for char in value:
        number = number * 58 + BASE58.index(char)
    size = len(value) - len(value.lstrip("1")) + (number.bit_length() + 7) // 8
    require(size == length, f"Invalid {label} length: {value}")


def verify_sources(evidence: Path) -> None:
    manifest = json.loads((evidence / "source_manifest.json").read_text())
    require(manifest.get("source_commit") == SOURCE_COMMIT, "Unexpected source commit")
    require(manifest.get("repository") == SOURCE_REPO, "Unexpected source repository")
    entries = manifest.get("files", [])
    require(len(entries) == len(SOURCE_FILES), "Missing or duplicate source provenance")
    require({x.get("file") for x in entries} == set(SOURCE_FILES), "Unexpected source files")
    for entry in entries:
        name = entry["file"]
        require(entry["git_blob_sha"] == PINNED_BLOBS[name], f"Source blob anchor changed: {name}")
        require(entry["source_path"] == SOURCE_FILES[name], f"Wrong source path: {name}")
        url = f"https://github.com/{SOURCE_REPO}/blob/{SOURCE_COMMIT}/{SOURCE_FILES[name]}"
        require(entry["source_url"] == url, f"Wrong source URL: {name}")
        data = (evidence / name).read_bytes()
        require(len(data) == entry["bytes"], f"Source byte count changed: {name}")
        require(hashlib.sha256(data).hexdigest() == entry["sha256"], f"Source SHA256 changed: {name}")
        blob = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
        require(blob == entry["git_blob_sha"], f"Source Git blob changed: {name}")


def exact_members(evidence: Path) -> set[str]:
    groups = json.loads((evidence / "group_split.json").read_text())["sous_ensembles"]
    members = [wallet for group in groups for wallet in group["members"]]
    require(len(members) == len(set(members)) == 33, "Exact-33 population changed")
    for wallet in members:
        check_base58(wallet, 32, "Solana address")
    return set(members)


def classify(maker: str, members: set[str]) -> str:
    """Classify the decoded maker, never the wallet whose cache held the tx."""
    if maker in members:
        return "groupe_33"
    require(maker in OUTSIDE, f"Unclassified maker: {maker}")
    return OUTSIDE[maker]


def archived_matches(evidence: Path) -> dict:
    """Read recipient-scoped matching logs; do not invent missing tx hashes.

    i21 prints actual received raw units and a transaction hash. i22 only
    prints a matching assertion, payer contract and delay; its missing values
    stay blank even though the historical script reports an exact match.
    """
    full = re.compile(
        r"\s+(\S+Z) [0-9.]+ take (\d+) reçu (\d+) de (0x[0-9a-f]{40}) "
        r"écart s (\d+) (0x[0-9a-f]{64})\s*"
    )
    partial = re.compile(
        r"\s+(\S+Z) [0-9.]+ take (\d+) reçu (0x[0-9a-f]{40}) (\d+)\s*"
    )
    result = {}
    for name in ("i21_evm_fill.txt", "i22_evm_rest.txt"):
        recipient = None
        for line_no, line in enumerate((evidence / name).read_text().splitlines(), 1):
            header = re.match(r"== (0x[0-9a-f]{40}) ordres ", line)
            if header:
                recipient = header.group(1)
                continue
            if not re.match(r"\s+\d{4}-\d\d-\d\dT\S+Z .* take ", line) or "reçu" not in line:
                continue
            hit = full.fullmatch(line) if name == "i21_evm_fill.txt" else partial.fullmatch(line)
            require(hit is not None and recipient is not None, f"Unparsed match: {name}:{line_no}")
            if name == "i21_evm_fill.txt":
                utc, take, received, payer, delay, tx_hash = hit.groups()
                require(take == received, f"Non-exact archived match: {name}:{line_no}")
                status = "archive_match_with_tx_hash"
            else:
                utc, take, payer, delay = hit.groups()
                received = tx_hash = ""
                status = "archive_match_without_tx_hash"
            require(0 <= int(delay) <= 7200, f"Implausible archived delay: {name}:{line_no}")
            key = ("1", recipient, utc, take)
            require(key not in result, f"Duplicate archived match: {name}:{line_no}")
            result[key] = {
                "destination_match_status": status,
                "destination_tx": tx_hash,
                "destination_amount_observed_raw": received,
                "destination_payment_contract": payer,
                "destination_delay_seconds": delay,
                "destination_evidence": f"evidence/{name}:{line_no}",
            }
    return result


def build_rows(evidence: Path) -> list[dict[str, str]]:
    verify_sources(evidence)
    members = exact_members(evidence)
    with (evidence / "i14_orders.csv").open(newline="") as handle:
        sources = list(csv.DictReader(handle))
    require(len(sources) == 76, "Source order count changed")
    matches = archived_matches(evidence)
    source_keys = set()
    seen = set()
    rows = []
    for index, order in enumerate(sources, 1):
        maker, sig = order["maker"], order["sig"]
        check_base58(maker, 32, "maker")
        check_base58(sig, 64, "signature")
        identity = (sig, order["nonce"])
        require(identity not in seen, "Duplicate source order")
        seen.add(identity)
        require(order["give_token"] == USDC_SOLANA and order["give_chain"] == "7565164", "Unexpected source asset/chain")
        chain, token = order["take_chain"], order["take_token"]
        require((chain, token) in ASSETS, "Unknown destination asset/chain")
        asset, decimals = ASSETS[(chain, token)]
        require(ADDRESS.fullmatch(order["receiver"]) is not None, "Invalid recipient")
        total = int(order["give_amount"]) + int(order["fee_pct"])
        require(total >= 0, "Negative source total")
        key = (chain, order["receiver"], order["utc"], order["take_raw"])
        require(key not in source_keys, "Ambiguous source-to-archive matching key")
        source_keys.add(key)
        row = {
            "order_index": str(index),
            "perimeter": classify(maker, members),
            "source_wallet": maker,
            "source_signature": sig,
            "source_time_utc": order["utc"],
            "source_instruction": order["ix"],
            "source_nonce": order["nonce"],
            "source_token": order["give_token"],
            "source_amount_raw": order["give_amount"],
            "source_proportional_fee_raw": order["fee_pct"],
            "source_total_raw": str(total),
            "source_total_usdc": units(total, 6),
            "source_fixed_fee_lamports": order["fee_fix_lamports"],
            "before_mint": str(order["utc"] < MINT_UTC).lower(),
            "destination_chain_id": chain,
            "destination_chain": CHAIN_NAMES[chain],
            "recipient": order["receiver"],
            "destination_token": token,
            "destination_asset": asset,
            "destination_amount_requested_raw": order["take_raw"],
            "destination_amount_requested": units(order["take_raw"], decimals),
            "destination_match_status": "unverified",
            "destination_tx": "",
            "destination_amount_observed_raw": "",
            "destination_amount_observed": "",
            "destination_payment_contract": "",
            "destination_delay_seconds": "",
            "source_evidence": f"evidence/i14_orders.csv:{index + 1}",
            "destination_evidence": "",
        }
        row.update(matches.get(key, {}))
        if row["destination_amount_observed_raw"]:
            row["destination_amount_observed"] = units(row["destination_amount_observed_raw"], decimals)
        rows.append(row)
    require(set(matches).issubset(source_keys), "Archived match has no source order")
    return rows


def validate_rows(actual: list[dict[str, str]], expected: list[dict[str, str]]) -> None:
    require(len(actual) == len(expected), "Order count mismatch")
    seen = set()
    for row in actual:
        require(set(row) == set(FIELDS), "CSV row has missing or extra fields")
        tx_hash = row.get("destination_tx", "")
        require(not tx_hash or TX_HASH.fullmatch(tx_hash) is not None, "destination_tx must be a 32-byte transaction hash, not an address")
        require(row.get("source_signature") not in seen, "Duplicate source signature")
        seen.add(row.get("source_signature"))
        if row.get("destination_match_status") == "unverified":
            require(not tx_hash and not row.get("destination_amount_observed_raw") and not row.get("destination_amount_observed"), "Unverified order cannot claim a received amount or tx")
    by_signature = {row["source_signature"]: row for row in expected}
    for row in actual:
        sig = row.get("source_signature")
        require(sig in by_signature, f"Unknown source signature: {sig}")
        for field in FIELDS:
            require(row.get(field) == by_signature[sig][field], f"Mismatch {sig[:10]} field {field}")


def summarize(rows: list[dict[str, str]]) -> dict:
    def total(selected):
        return units(sum(int(r["source_total_raw"]) for r in selected), 6)
    scope = {}
    for key in sorted({r["perimeter"] for r in rows}):
        chosen = [r for r in rows if r["perimeter"] == key]
        scope[key] = {"orders": len(chosen), "source_total_usdc": total(chosen)}
    matched = [r for r in rows if r["destination_match_status"] != "unverified"]
    return {
        "validation_scope": "offline consistency against committed audit outputs; no live-chain revalidation",
        "source_commit": SOURCE_COMMIT,
        "orders": len(rows),
        "source_total_usdc": total(rows),
        "perimeters": scope,
        "destination_status": dict(sorted(Counter(r["destination_match_status"] for r in rows).items())),
        "source_usdc_of_archived_matches": total(matched),
        "before_mint_orders": sum(r["before_mint"] == "true" for r in rows),
    }


def validate(root: Path = ROOT) -> dict:
    expected = build_rows(root / "evidence")
    with (root / "TABLE_DEBRIDGE_ORDERS.csv").open(newline="") as handle:
        reader = csv.DictReader(handle)
        require(reader.fieldnames == FIELDS, "CSV schema mismatch")
        actual = list(reader)
    validate_rows(actual, expected)
    return summarize(actual)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-csv", action="store_true", help="Explicitly regenerate the derived CSV from the immutable evidence snapshots")
    args = parser.parse_args()
    try:
        if args.write_csv:
            rows = build_rows(ROOT / "evidence")
            with (ROOT / "TABLE_DEBRIDGE_ORDERS.csv").open("w", newline="") as handle:
                writer = csv.DictWriter(handle, fieldnames=FIELDS, lineterminator="\n")
                writer.writeheader()
                writer.writerows(rows)
        print(json.dumps(validate(), indent=2, ensure_ascii=False))
        return 0
    except (ValidationError, OSError, ValueError, KeyError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
