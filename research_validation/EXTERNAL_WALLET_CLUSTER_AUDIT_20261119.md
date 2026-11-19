# External Solana wallet-clustering code review (19 November 2026)

**Status: completed source-code review and independent arithmetic recount; no additional on-chain transaction replay and no validated trading edge.**

## Sources inspected

- [hiburhan/wallet-analyzer: bundle_engine.py](https://github.com/hiburhan/wallet-analyzer/blob/main/bundle_engine.py), Git blob ac9497b9aaac9ca8452da4ce1300211880fa4678 (read 19 November 2026).
- [hiburhan/wallet-analyzer: cluster_detector.py](https://github.com/hiburhan/wallet-analyzer/blob/main/cluster_detector.py), Git blob cfee3b80d78a1050fd4e8dbcc4661560df3d5cbd.
- [hiburhan/wallet-analyzer: graph_builder.py](https://github.com/hiburhan/wallet-analyzer/blob/main/graph_builder.py), Git blob 007901bf5b69195601164de4c621e08385cd9473.
- Internal archival source: [data/snipe_log.json](../data/snipe_log.json), blob b323514a543ecb4df221e6684c2a284c63b077be; independent reading of its JSON rows.
- Existing internal replication: [snipe-log timing and label audit](../audits/snipe-log-label-timing-20261119/README.md) and [research controls](README.md).

## Verified implementation observations

The external clustering implementation combines funder ancestry, temporal proximity, behavioral cosine similarity, Jito-tip heuristics and slot packing. In cluster_detector.py, the boolean named same_operator is set when either behavioral similarity is at least 0.92 **or** the shared-funder score is at least 0.6. This is a **heuristic label in that code**, not transaction-level proof that a human or entity controls every wallet. Shared service infrastructure, custodians, bots and market-maker activity are alternative explanations. Similarly, a Jito-related tip or same-slot inclusion is not, by itself, proof that separate transactions were submitted in the same verifiable bundle. A genuine bundle-membership claim requires an independently verifiable bundle ID/provider record or equivalent direct evidence.

The reviewed external source is useful as an implementation benchmark for **candidate generation**, not as a ground-truth operator identity classifier. Its scored clusters should not be imported as verified identities. No external code, images, databases, or results have been copied into this repository.

## Independent local archive cross-check

The archived JSON contains 211 rows for 211 unique mints: 100 marked full_snipe and 111 not. The lifetime reached_100k label matches max_ath >= 100000 on all 211 rows. Among the 100 full_snipe rows, 69 are labeled lifetime-positive, but 32 entries in the overall archive were **already** at or above $100,000 market cap at detection and 31 rows have no positive detection timestamp. Filtering to a positive detected_at and detect_mc < $100,000 leaves 148 records: 31/58 full_snipe lifetime-positive versus 5/90 other records. These are an independent recount of previously reported figures, **not a new prospective result**. The archive does not contain a first-threshold-crossing timestamp and the groups have poor market-cap overlap.

Reproduce from the existing repository:

    python3 audits/snipe-log-label-timing-20261119/recheck.py --self-test
    python3 audits/snipe-log-label-timing-20261119/recheck.py --check

## Falsification gates before adapting the external detector

1. Separate an observed transfer edge from a common-funder inference, from a service-mediated path, from a beneficial-owner claim; emit distinct evidence tiers.
2. For Jito claims, preserve transaction signatures, slots, tip program and accounts, and independently verifiable bundle metadata. Flag same-slot-only evidence as temporal, not as bundle membership.
3. Freeze the wallet graph, token selection, thresholds and feature-availability time **before** examining later prices. A lifetime ATH is never an alert-time predictor.
4. Reject or separately classify known custodians, routers, pools, bridges and exchange hot wallets; use degree- and time-matched negative controls.
5. Evaluate recurrence on previously unseen operators/launch days, with clustering of dependent observations, corrected multiple testing and executable fees, latency and slippage.
6. Compare against a price/liquidity-only baseline, record missing history and report false alerts per unit time. If ground-truth identities are absent, do not report identity precision.

**Conclusion:** the independent code review identifies useful candidate-generation mechanics but no transferable validated operator attribution or trading alpha. Existing NO_TRADABLE_EDGE findings are not superseded. No frozen input, README or prior conclusion was altered.