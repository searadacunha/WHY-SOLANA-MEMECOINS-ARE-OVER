# Timing and label audit of the archived Solana snipe log

**Date:** 19 November 2026. **Status:** independent arithmetic check of an existing internal archive, not a chain replay or a new alpha claim.

**Source:** [data/snipe_log.json](../../data/snipe_log.json), Git blob `b323514a543ecb4df221e6684c2a284c63b077be`. This audit uses only this repository's existing 211-row snapshot; it imports no external research, code, wallet identities or results. The source file and previous frozen studies are unchanged.

## Findings

| Archival measurement | Count |
| --- | ---: |
| Records / unique mint addresses | 211 / 211 |
| `full_snipe` true / false | 100 / 111 |
| Lifetime `reached_100k` labels, all rows | 74 |
| `full_snipe` and lifetime label true | 69 / 100 |
| Non-`full_snipe` and lifetime label true | 5 / 111 |
| Rows with missing/zero `detected_at` | 31 |
| Market capitalization already ≥$100k at detection | 32 |
| Those 32 rows flagged `full_snipe` and `reached_100k` | 32 |
| Timestamped rows with `detect_mc < $100k` | 148 |
| Within those 148: full-snipe lifetime-positive | 31 / 58 |
| Within those 148: non-full lifetime-positive | 5 / 90 |

The apparent **69% versus 4.5%** lifetime hit-rate contrast is not a valid prospective comparison. Thirty-two of the full-snipe positives were **already at or above the $100k threshold at detection**; another 31 archive rows have no usable positive detection timestamp. Among the 148 timestamped, below-threshold rows, the unadjusted 31/58 versus 5/90 contrast remains **descriptive, not predictive**.

**Outcome construction:** on every one of the 211 archived rows, `reached_100k` is exactly `max_ath >= 100000`. `max_ath` is an outcome-derived maximum, not an alert-time feature. The archive has **no timestamp of the first $100k crossing**. Therefore even a below-threshold `detect_mc` does not prove the recorded lifetime high happened *after* the alert; some may have crossed earlier and returned below threshold. Do not use `max_ath`, `reached_100k`, or `graduated` as predictors for an alert-time model.

## Non-overlap in detection-price strata

Only the 148 rows with a positive `detected_at` and `detect_mc < $100k` appear below. The rightmost columns are *lifetime labels*, not later trade outcomes.

| Detection market cap | Full snipe (lifetime positive) | Not full snipe (lifetime positive) |
| --- | ---: | ---: |
| <$20k | 0 / 1 | 5 / 84 |
| $20k–<$40k | 5 / 12 | 0 / 6 |
| $40k–<$60k | 12 / 30 | 0 / 0 |
| $60k–<$80k | 4 / 5 | 0 / 0 |
| $80k–<$100k | 10 / 10 | 0 / 0 |

The two classes have **almost no common support in entry valuation**: there is no non-full-snipe comparator above $40k in this eligible subset. A regression, propensity score or simple pooled rate would not repair that missing overlap. The class definition, token selection, detector coverage, prior price history and latent quality could all be confounded with the outcome.

## Evidence tier and decision

- **CONFIRMED WITHIN ARCHIVE:** the counts, missing timestamps, lifetime-label equivalence and lack of high-price comparators; these are recomputed by the attached script.
- **UNRESOLVED:** true historical timing of $100k threshold crossings; population base rates outside the selected archive; whether a full-snipe signal adds information over entry market cap and other pre-alert variables.
- **NOT ESTABLISHED:** causality, independently verified token success rates, forward precision, executable profitability or human operator attribution.

A real forward test needs (1) alert receipt timestamps, (2) first threshold-crossing timestamps, (3) all qualifying launches including misses, (4) comparable detection-price support and event-time controls, and (5) executable bid/ask and fees. Freeze these before observing outcomes. Existing post-detection negative economic verdicts remain in force.

## Reproduction

From repository root, Python 3.10+ standard library only:

```bash
python3 audits/snipe-log-label-timing-20261119/recheck.py --self-test
python3 audits/snipe-log-label-timing-20261119/recheck.py --check
```

This is a replay of archived **metadata**, not fresh Solana RPC verification. The original README, dataset, historical reports and publication guard are untouched.
