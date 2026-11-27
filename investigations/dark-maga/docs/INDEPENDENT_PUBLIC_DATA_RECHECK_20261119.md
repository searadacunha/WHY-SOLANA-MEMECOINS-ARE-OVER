# Independent public-data statistical and chronology recheck — 19 November 2026

**Scope:** an independent arithmetic check of existing repository evidence, **not** a Solana RPC replay, new person attribution, frozen-protocol amendment or trading-edge discovery.

## Sources and integrity boundary

- [etude_final/tables/tests.json](../etude_final/tables/tests.json), primary seven-metric rank-test output, Git blob 9260fd01661c5652f9ec2da83f758ea4aee8eaf4.
- [historical RETIREDIO rotation export](../investigations/2026-11-06_historical_replay/data/rotation_retiredio.csv), pre-existing legacy file.
- [current RETIREDIO replay code](../investigations/2026-11-06_historical_replay/scripts/h52_rotation.py) and [point-in-time helper](../investigations/2026-11-06_historical_replay/scripts/h_time_rules.py).
- [point-in-time regression](../investigations/2026-11-06_historical_replay/tests/test_h52_rotation_point_in_time.py), merged in [commit f4c1af6](https://github.com/searadacunha/DARK-MAGA/commit/f4c1af67434e693180ee06ffa9b53d50b46ac4f8).
- [issue #36](https://github.com/searadacunha/DARK-MAGA/issues/36) remains the raw-receipt reconciliation task.

## Independently recomputed arithmetic

Primary frozen comparison: 211 control tokens across 84 distinct peak days. Sorting the seven stored primary unadjusted p-values yields M6 0.1556603774, M1 0.1698113208, M7 0.1792452830, M2 0.1839622642, M3 0.2405660377, M5 0.2641509434, and M4 0.5471698113. Under the usual step-down Holm procedure across the **seven prespecified tests**, every adjusted p-value is 1.0: the smallest p times seven already exceeds one. No primary metric is statistically significant. This checks the arithmetic of the stored primary values; it **does not** independently validate comparator sampling, data completeness, test assumptions or source transactions.

The published RETIREDIO CSV has 90 records, of which 15 have the **legacy** rotation=True flag. Among those 15, exactly one has a stored non-positive sell_to_buy_s: wallet DpvWg6MaWAN9BTKKPheVTPPSxH7bdZ8ebU4q61Zo7THz, with the last apparent sale at 18:17:13 UTC, **50 seconds after** its 18:16:23 first DMAGA buy on 21 July 2024. That legacy flag is not valid evidence of a pre-buy sale. The 90 CSV rows are **not the denominator** of the separately reported 11/35 vs 4/149 exploratory contrast; do not splice the numbers or claim corrected counts from this recount.

The code now excludes post-buy timestamps using the strict half-open interval [first_buy - 3600 seconds, first_buy); the code's current check is distinct from the still-unrecomputed archived CSV. A negative token-balance delta is not automatically a DEX sale. Rebuilding the published counts requires raw receipts, route decoding, actual counterasset proceeds and equal cutoffs for selected and control wallets.

## Reproduction on a full checkout

Run this independent offline excerpt from the repository root:

~~~python
import csv
import json
from pathlib import Path

r = Path("etude_final/tables/tests.json")
primary = json.loads(r.read_text())["variants"]["primary"]
pvals = sorted((float(v["p"]), k) for k, v in primary["mesures"].items())
holm = []
running = 0.0
for i, (p, label) in enumerate(pvals):
    running = max(running, min(1.0, p * (len(pvals) - i)))
    holm.append((label, running))
assert len(pvals) == 7 and all(adj == 1.0 for _, adj in holm)

c = Path("investigations/2026-11-06_historical_replay/data/rotation_retiredio.csv")
rows = list(csv.DictReader(c.open()))
old = [x for x in rows if x["rotation"] == "True"]
future = [x for x in old if x["sell_to_buy_s"] and float(x["sell_to_buy_s"]) <= 0]
assert len(rows) == 90 and len(old) == 15 and len(future) == 1
print("Holm:", holm)
print("Legacy non-prebuy rows:", [(x["owner"], x["sell_to_buy_s"]) for x in future])
~~~

This is an archival self-consistency check with assertions against the current pinned data, **not** a regeneration of the original historical study.

## Remaining gates

1. Replay complete token/DEX receipts in the old RETIREDIO selection, classify bona fide sells versus ordinary debits, and re-export both groups; keep the old CSV as legacy evidence.
2. Freeze reconstructed transfer and price timestamps before testing a cross-token predictive claim; test matched launch/news controls including the documented public Biden and profile-image chronology.
3. Preserve the frozen 211-token statistical result and the independently supported funding/deBridge findings, without inferring one owner or privileged information.

**Verdict: arithmetic consistent with the previously published negative statistical finding; one proven temporal false positive in the legacy exported screen; corrected replay counts unresolved.**