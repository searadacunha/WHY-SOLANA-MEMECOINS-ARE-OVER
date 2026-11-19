# Solana — reproducible controls and external-method comparisons

**Scope:** additive research checks only. The root README, original 2024 trades, frozen 2026 studies, existing economic verdicts and protected publication files are unchanged.

## Three integrated checks

1. [Pooled-wallet null dependence](NULL_COHORT_AUDIT.md) tests why the historical 88.86% pooled-wallet trigger rate should **not** be represented as an independently sampled launch-level false-positive rate. The script quantifies within-launch and across-launch shared-funder pairs and distinguishes 136 launch observations from 132 unique wallet addresses; it does not invent a repaired FPR.
2. [Historical snipe-log timing audit](../audits/snipe-log-label-timing-20261119/README.md) independently recounts 211 archived rows, finds 32 tokens already above the $100k label threshold at detection, 31 missing positive alert timestamps, and substantial lack of comparable price support. No independent RPC replay or forward-return claim.
3. [External benchmark map](EXTERNAL_BENCHMARKS_20261118.md) reviews independently published Solana research and proposes falsifiable dataset-linkage/holdout experiments. These studies are **cited as external**; their results were not independently reproduced and their code or datasets were not imported.

## Reproduction

```bash
python3 research_validation/null_cohort_contamination.py --draws 500
python3 -m pytest -q research_validation/test_null_cohort_contamination.py
python3 audits/snipe-log-label-timing-20261119/recheck.py --self-test
python3 audits/snipe-log-label-timing-20261119/recheck.py --check
```

## Evidence boundary

Historical outcomes and wallet clusters are not necessarily causal predictions. For a prospective detector, define cohorts, freeze features and thresholds before outcome examination, hold out complete operators/time windows, use first observable alert, and simulate executable entry/exit with latency and real fees. Existing **NO_TRADABLE_EDGE** results remain authoritative in their stated populations; these checks identify possible confounders and research directions, not positive alpha.

This integration reuses the original exact file blobs from former draft PRs #14, #15 and #16 on top of the publication baseline corrected by PR #17, without merging their stale branches, changing the protected README or altering their published data.
