#!/usr/bin/env python3
"""Audit dependence in the legacy Phase-1 pooled-wallet null (read-only).

This is a diagnostic, NOT a replacement false-positive estimate: independent
40-wallet groups cannot be drawn one per token from only nine control launches.
The script never changes frozen data or published estimates.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from itertools import combinations
import json
from math import comb
from pathlib import Path
import random

REPO = Path(__file__).resolve().parents[1]
KNOWN = frozenset({
    "G2YxRa6wt1qePMwfJzdXZG62ej4qaTC7YURzuh2Lwd3t",
    "5tzFkiKscXHK5ZXCGbXZxdw7gTjjD1mBwuoFbhUvuAi9",
    "BmFdpraQhkiDQE6SnfG5omcA1VwzqfXrwtNYBwWTymy6",
    "2snHHreXbpJ7UwZxPe37gnUNf7Wx7wv6UKDSR2JckKuS",
    "u6PJ8DtQuPFnfmwHbGFULQ4u4EgjDiyYKjVEsynXq2w",
    "is6MTRHEgyFLNTfYcuV4QBWLjrZBfmhVNYR6ccgr8KV",
})


def load_pool(folder: Path) -> list[dict]:
    pool = []
    seen = set()
    for path in sorted(folder.glob("e2_funding_*.json")):
        raw = json.loads(path.read_text(encoding="utf-8"))
        token = raw["label"]
        for wallet in raw.get("wallets", []):
            address = wallet["wallet"]
            if address in seen:
                raise ValueError(f"Duplicate wallet in cohort: {address}")
            seen.add(address)
            sources = {
                flow["source"]
                for flow in wallet.get("inflows", [])
                if flow.get("nature") != "produit_de_vente"
                and flow.get("amount_sol", 0) > 0
                and flow.get("source")
                and flow["source"] not in KNOWN
            }
            pool.append({"token": token, "wallet": address, "funders": sources})
    if not pool:
        raise ValueError("No control wallet found; check input directory")
    return pool


def funder_flags(group: list[dict]) -> tuple[bool, bool]:
    """Shared-source edges with same-launch and across-launch endpoints.

    A single group can contain both kinds of edges. Neither is necessarily a
    false positive: the pooled-wallet control fails to remove both dependencies.
    """
    by_source = defaultdict(list)
    for wallet in group:
        for source in wallet["funders"]:
            by_source[source].append(wallet["token"])
    within = across = False
    for tokens in by_source.values():
        if len(tokens) < 2:
            continue
        different = len(set(tokens))
        within |= different < len(tokens)
        across |= different > 1
    return within, across


def audit(pool: list[dict], *, draws: int = 5000, seed: int = 12345,
          group_sizes: tuple[int, ...] = (10, 20, 40)) -> dict:
    if draws <= 0:
        raise ValueError("draws must be positive")
    sizes = Counter(row["token"] for row in pool)
    n = len(pool)
    if any(k <= 1 or k > n for k in group_sizes):
        raise ValueError("group sizes must be between 2 and pool size")
    same_launch_pairs = sum(comb(k, 2) for k in sizes.values())
    all_pairs = comb(n, 2)
    by_source = defaultdict(list)
    for row in pool:
        for source in row["funders"]:
            by_source[source].append(row)
    within_edges = set()
    across_edges = set()
    for rows in by_source.values():
        for a, b in combinations(rows, 2):
            key = tuple(sorted((a["wallet"], b["wallet"])))
            if a["token"] == b["token"]:
                within_edges.add(key)
            else:
                across_edges.add(key)
    rng = random.Random(seed)
    samples = {}
    for k in group_sizes:
        counts = Counter()
        for _ in range(draws):
            within, across = funder_flags(rng.sample(pool, k))
            counts["any"] += within or across
            counts["within"] += within
            counts["across"] += across
            counts["only_within"] += within and not across
            counts["only_across"] += across and not within
            counts["both"] += within and across
        samples[str(k)] = {
            key: round(counts[key] / draws, 6)
            for key in ("any", "within", "across", "only_within", "only_across", "both")
        }
    return {
        "status": "CONTAMINATED_NULL_NOT_AN_INDEPENDENT_FALSE_POSITIVE_RATE",
        "scope": "Criterion C: shared non-allowlisted funder; A/B not re-estimated",
        "wallet_count": n,
        "launch_count": len(sizes),
        "launch_wallet_counts": dict(sorted(sizes.items())),
        "same_launch_pair_probability_in_pool": same_launch_pairs / all_pairs,
        "expected_same_launch_pairs_in_40_wallet_sample": (
            comb(40, 2) * same_launch_pairs / all_pairs if n >= 40 else None
        ),
        "shared_funder_pairs_within_launch": len(within_edges),
        "shared_funder_pairs_across_launches": len(across_edges),
        "max_launch_independent_wallets": len(sizes),
        "can_construct_40_independent_launch_wallets": len(sizes) >= 40,
        "draws": draws,
        "seed": seed,
        "sampled_rates_not_true_fpr": samples,
        "next_step": (
            "Collect >=40 independent launches; sample one wallet per launch, "
            "match era/activity, and test against a frozen launch-level baseline."
        ),
    }


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--input-dir", type=Path, default=REPO / "data" / "trace_temoins")
    ap.add_argument("--draws", type=int, default=5000)
    ap.add_argument("--seed", type=int, default=12345)
    args = ap.parse_args()
    print(json.dumps(audit(load_pool(args.input_dir), draws=args.draws,
                           seed=args.seed), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
