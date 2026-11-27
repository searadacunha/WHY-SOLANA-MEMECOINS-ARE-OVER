# From historical DMAGA forensics to falsifiable early warning
**Research gate document | 18 November 2026**

**Current decision: NO VALIDATED EARLY-WARNING TRADING PATTERN. No live-trading module should be represented as validated.** This is a pre-analysis specification and prioritization, **not** the result of a new backtest.

## 1. What can and cannot be inferred today

The frozen [211-peer study](../etude_final/results.md) tested pre-peak activity on seven metrics and returned no Holm-significant outlier. This constrains the *specific* hypothesis of DMAGA being unusual among similarly spiking tokens under those features. It does not test whether a narrow traceable funding network could predict a later information event in a wider universe.

The [Kekius comparison](../investigations/2026-11-06_dmaga_kekius_cross_token/FINDINGS.md) found a clear launch-coordination mechanism for XC78, but no demonstrable recurrence of the central DMAGA financial actors in the specified Kekius mints. The RETIREDIO-to-DMAGA rotation remains exploratory and contains a known timing error ([issue #36](https://github.com/searadacunha/DARK-MAGA/issues/36)).

## 2. Candidate signals — a falsification-first priority queue

| Rank | Candidate signature | Real-time observables | Dominant false-positive explanation | Gate before any claim |
|---|---|---|---|---|
| 1 | **Recurring directly funded buyer subgraphs** | Wallet funding transfers, shared *non-service* origin, token acquisition, timestamps, independently observed recurrence across prior events | Bot/sniping infrastructure that routinely participates in many launches | Same rule, after service filtering, on pre-registered future token universe and negative-control launches |
| 2 | **Concentrated synchronized accumulation** | Entry counts, amount-weighted concentration, signed token transfers, liquidity at each slot | Ordinary sniper bundles, relayers, liquidity migration | Improvement over matched price/volume/liquidity model with time-split validation |
| 3 | **Cross-token capital rotation** | A verifiable sale of earlier token **before** funding and buying the next; time-order and value conservation | Public narrative rotation, broad political news, arbitrage | Correct `t_sell < t_buy` logic, matched contemporary controls, no future data |
| 4 | **Public social activity vs. on-chain lead/lag** | Timestamped original posts/images, first independently observable buys, proof of capture availability | Reposts misdated as originals, public promotions preceding token activity | Independent timestamp provenance and interval-censored event times |
| 5 | **Bridge-to-new-wallet reentry** | Contract event/order ID, source and destination receipts, onward funding to a newly observed wallet | Bridge solvers, CEX hot wallets and multiuser infrastructure | End-to-end financial continuity without crossing unobservable account boundaries |
| 6 | **Dormant wallet activation around catalysts** | First activity after fixed dormant period, purchases and funding history known at alert time | Routine account reuse and automated market makers | Significant positive predictive value above dormant-wallet control cohort |

These are hypotheses, not findings of advance knowledge. Choose one *before* seeing the validation outcomes.

## 3. Mandatory prospective protocol

**Prediction target.** Define a publicly measurable outcome without presuming insider activity. For example, conditional on a launch being observable at time `t`, predict a specified return/liquidity outcome over the next 1h, 6h or 24h. Predefine whether the target includes any *public* social catalyst or only market moves. Use independently timestamped market data; define delisted/rugged, zero-liquidity and censored outcomes before tests.

**Universe and controls.** Include *all* eligible token launches during predeclared calendar intervals, not only historical spectacular gainers. Compare matched controls for market capitalization, age, liquidity depth, public mentions and hourly trend. Count each service-funded account appropriately. Also run shuffled time and shuffled funder labels, neutral non-event tokens and false social-event windows.

**Point-in-time integrity.** Every raw observation needs `event_time`, `first_available_to_detector`, `source`, `transaction_signature` or `post_id`, and a capture hash. An alert at time `t` may use only observations available by `t`; a token later known as a winner must not be retrospectively included in an earlier candidate universe.

**Validation splits.** Set disjoint exploration, chronological validation and locked holdout periods. **Split by both wallet network and event family where feasible** to reduce dependence leakage. Preserve all failed attempts and results. Require permutation tests, multiple-testing correction over attempted patterns/horizons/thresholds, uncertainty intervals, precision-recall calibration and coverage statistics.

**Economic model.** Simulate execution against observed pool depth at the first actually tradable quote after latency; deduct price impact, slippage, platform/network/priority fees and failed fills. Model adverse selection, MEV exposure, exits under poor liquidity and costs of false positives. Compare against simple price/volume/momentum and public-social baseline policies, under several fixed position sizes. No transaction keys or real trading.

**Promotion standard.** A candidate can be called *reproducible predictive* only with net-positive holdout performance, measured base rates, uncertainty bounds, transaction-level auditability and a prospectively logged trial. Do not turn a generic anomaly score into a probability of insider trading.

## 4. Work remaining before the repository can claim prospective results

- Recover and verify the off-Git historical Parquet/raw ledgers cited in [state/STATE.md](../state/STATE.md) and [raw manifest](../evidence/RAW_MANIFEST.tsv) before full financial replays. A path is not evidence that bytes are currently present.
- Resolve **4,795 classification discrepancies** noted in the [7 November research status](RESEARCH_STATUS_2026-11-07.md) by re-normalizing the historical archive in an isolated output path. Retain old derivations.
- Repair and re-run RETIREDIO historical rotation interpretation ([issue #36](https://github.com/searadacunha/DARK-MAGA/issues/36)), keeping it outside frozen results.
- Finish the independent matching controls for other meme/political-token events, including negatives without major attention catalysts. Do not accept exchange-service overlaps as operator identities.
- Ensure the publication gate on `main` is green before describing the research as CI-validated ([issue #37](https://github.com/searadacunha/DARK-MAGA/issues/37)).
- Only then consider a **paper-only** monitor that stores its raw observations before outcomes and produces calibration reports.

## 5. Explicit conclusion

**No prospective alert system or after-cost profitable predictor has been validated from DMAGA to date.** A strong forensic reconstruction and a negative statistical finding are valid research outputs. Their defensible value is independent of whether a sensational explanation ultimately survives testing.
