# DARK MAGA: DID MUSK KNOW?
## Forensic case brief | Independent on-chain investigation | 18 November 2026

**Subject:** Solana token `7D7BRcBYepfi77vxySapmeqRNN1wsBBxnFPJGbH5pump` ($DMAGA) and the July 2024 change to Elon Musk's X profile picture.  
**Research:** Benjamin Da Cunha / searadacunha.  
**Status:** Historical forensic reconstruction with receipt-backed findings, separately frozen statistical testing, explicit negative results, and unresolved attribution. **No allegation of misconduct is established.**

> **Bottom line.** Public Solana transactions document early trading gains, direct token transfers, funding relationships and cross-chain exits. The best available avatar-change window is 21 July 2024 **19:03:27–19:25:23 UTC**; DMAGA and related imagery had already been promoted publicly. The frozen comparison against **211** other tokens detects **no significant anomaly** on seven predefined metrics after Holm correction. Neither privileged knowledge of Musk's decision nor a profitable prospective trading signal has been demonstrated.

### Start here (a 15-minute evidence review)

1. **Chronology:** [timestamped timeline](TIMELINE.md) and [historical X / transaction replay](../investigations/2026-11-06_historical_replay/FINDINGS.md) distinguish public information, observed profile states and trades.
2. **Wallet accounting:** [top traders](../reports/TOP_TRADERS.md) and the [7 November reconstruction](REBUILD_2026-11-07.md) explain PnL, cost basis, transfers and differences from earlier reports.
3. **Financial connections:** [coordination case file](../reports/COORDINATION.md) identifies the direct-transfer graph, but is **legacy/non-regenerated**. Use [rebuild machine checks](../reports/data_checks/sigrule_20261107.json) for corrected component totals.
4. **Cross-chain evidence:** [order register](../investigations/2026-11-05_debridge_winners/TABLE_DEBRIDGE_ORDERS.csv), [Base/BSC/Solana audit](../investigations/2026-11-06_debridge_base_bsc_solana/FINDINGS.md), and [BSC receipt follow-up](../investigations/2026-11-13_debridge_bsc_delivery/FINDINGS.md).
5. **Attempt to falsify the narrative:** [frozen statistical plan](../etude_final/analysis_plan.md), [derived metric table](../etude_final/derived/metrics.csv), [test output](../etude_final/tables/tests.json), [verdict](../etude_final/results.md) and [post-freeze amendments](../etude_final/amendements/).
6. **Cross-event recurrence:** [DMAGA × Kekius findings](../investigations/2026-11-06_dmaga_kekius_cross_token/FINDINGS.md) and [unresolved paths](../investigations/2026-11-06_dmaga_kekius_cross_token/UNRESOLVED.md).
7. **How to reproduce:** [reproduction guide](REPRODUCTION.md), [10 November technical audit](AUDIT_2026-11-10.md), and [claim-by-claim evidence index](EVIDENCE_INDEX_2026-11-18.md).

### Key findings and their precise scope

| Claim | Quantification | What has been established | What has **not** been established |
|---|---|---|---|
| Mint and first trading | Mint created **14 Jul 2024 02:05:25 UTC** | On-chain mint signature/slot and Raydium migration documented in [timeline](TIMELINE.md) | An identity behind the creator or a connection to Musk |
| Early winner H3Qs | **2 buys / 48 sells**; about **5,490.86 SOL** of reconstructed realized trading PnL; historical USD conversion **$990,743.77** | Wallet-specific swaps and a cost-basis model; [ranking](../reports/TOP_TRADERS.md), [additional replay](../investigations/2026-11-06_historical_replay/data/h3qs_by_mint.csv) | Bank cash-out, net profit after all fees/taxes, or insider knowledge; the full raw archive is not in Git |
| Direct-transfer network | **33 wallets; 40 DMAGA transfers; 15 first-hour buyers** | A transaction-defined component with **217.037M DMAGA** pre-event holdings as an **upper bound** and **4,524.914 SOL** in 24-hour sale proceeds | One beneficial owner of all wallets; proceeds equal to profit |
| Component trade accounting | **5,472 SOL** reconstructed realized trading PnL | Corrected aggregate in the [rebuild check](../reports/data_checks/sigrule_20261107.json) | A bank withdrawal; direct equivalence to the separate 24-hour sale-proceeds figure |
| Jupiter / 7GVC | **189.656068999 SOL** received 33m14s before mint; **41.197M DMAGA** purchased; **20M** transferred | Jupiter proceeds were from 7GVC's **own closed perpetuals position**; direct transfers/funding of downstream wallets recorded in [receipt-backed replay](../investigations/2026-11-06_historical_replay/FINDINGS.md) | A mysterious external funder, a common human owner, or privileged information |
| July 22 bridge convergence | **4 deBridge orders / 3 Solana wallets / 1 Ethereum recipient** in **9m36s**, **263,573.15 USDC** of source-side commitments | Order-level convergence to `0xb947bf7f409e998b28f8e218802fc9575c3c8c57` in [order register](../investigations/2026-11-05_debridge_winners/TABLE_DEBRIDGE_ORDERS.csv) | That all funds came from DMAGA trades, or that all wallets belong to one person |
| Wider deBridge register | **76 orders**, **1,018,687.18 USDC** source commitments including proportional USDC fees | Order register reconciles principal + proportional fees; **41** historical Ethereum archive matches | All 76 destination deliveries independently confirmed, or that the source totals are realized profit |
| Statistical controls | **211 comparator tokens; 84 distinct peak days; 7 primary metrics** | Recomputed rank p-values from published metric table; best primary **p = 0.15566**, no Holm significance | Proof of equivalence or proof that every possible pre-event signal is absent |
| Cross-event recurrence | **7,152 DMAGA addresses × 2 Solana Kekius mints** | Archive tests found **no** activity in KM/XC78 for the 33-wallet DMAGA component or the selected core winners in the tested period | A universal absence of related actors; exchanges/unknown token accounts can hide paths |

The H3Qs USD amount uses historical conversion rather than a single exit-day exchange rate. All profits in this brief are **model-based wallet trading results**, and bridge transfers are **movements of funds**, not additional profits. Do **not** add numbers from overlapping populations.

### The information timeline (UTC)

| Timestamp | Verifiable observation | Interpretation |
|---|---|---|
| **14 Jul 02:05:25** | Solana mint creation | Token precedes the 21 July profile change, but follows a major public political event |
| **14 Jul 02:33:53** | Earliest located X post sharing official mint in the pass-4 source corpus | Promotion is publicly observable; this is *earliest retrieved*, not first-ever |
| **16 Jul 05:40:46** | Archived promotion of red laser-eye profile images | Public narrative predates the exact avatar change |
| **21 Jul 16:00:08** | Archived post with a now-missing image | Cannot prove whether this was the eventual avatar image |
| **21 Jul 16:02:29** | @ChrisWinig publishes an image matched to the later Musk avatar | Exact visual publicly documented **before** the avatar-change interval |
| **21 Jul 17:46** | Joe Biden's withdrawal becomes public | Major confounder for political-token activity that afternoon |
| **21 Jul 19:03:27** | Archived view with prior Musk avatar | Lower documentary bound |
| **21 Jul 19:23:20** | Timestamp decoded from apparent avatar upload image identifier | **Indicative**, not independently proven time of profile adoption |
| **21 Jul 19:25:23** | First archived post found showing changed avatar | Upper documentary bound, **not** the time Musk clicked Save |
| **After upper bound (1 h)** | **5,347.29 SOL** in DMAGA buys in the reconstructed window | Marked *post-observation* activity; not evidence of early informed buying |

The [replayed interval](../investigations/2026-11-06_historical_replay/data/windows_sensitivity.csv) records **20.85 SOL** in buys during the 21m56s unresolved window. Earlier historical reports using a 19:30:13 upper bound are superseded on that narrow timing point. No financial identifier has been proven to correspond to Musk, @DarkMagaCoin, or the public promoters.

### Statistical falsification comes before interpretation

The [frozen plan](../etude_final/analysis_plan.md) selects a particular reference population: other Pump.fun-to-Raydium tokens with late, intense activity peaks, matching a broad market-capitalization range. It does **not** represent all launched tokens or a random sample of unremarkable events.

- The seven primary one-sided rank tests use point-in-time quantities before each token's own peak. The strongest DMAGA result is M6 (early holders retaining supply): **33rd rank among 212** when sorted descending; **p = 33/212 ≈ 0.15566**.
- The first Holm threshold at family-wise alpha = 0.05 is **0.05/7 ≈ 0.00714**. None of the seven tests passes.
- All seven published rank p-values and control medians have been independently recomputed **from the committed metric CSV**, as have their R1/R2/R3 variants. This is *table-level arithmetic reproduction*, **not** an independent recollection of 15.85 million source transactions.
- A negative test is not a test of innocence. The study does not establish equivalence, lacks direct prospective economic tests, and may have limited power for narrower phenomena.
- [Post-freeze amendments](../etude_final/amendements/) clarify robustness populations and Holm wording. The historic `etude/` registry contains mislabelled synthetic data and is **not** independent confirmation.

### Findings that **do not** support a privileged-information hypothesis

1. The precise image used by Musk was publicly posted before the known profile-change window, with earlier general political-token promotion.
2. The 189.656 SOL 7GVC receipt is a Jupiter position close by the same wallet, not newly discovered outside funding.
3. The connected 33-wallet token-transfer component does not include the token creator merely by virtue of shared infrastructure or later deposits.
4. The [DMAGA × Kekius](../investigations/2026-11-06_dmaga_kekius_cross_token/FINDINGS.md) comparison finds public-post-following trades and separate coordinated launch behavior, **not** a proven common early-winning financial network across the two events.
5. The frozen statistical result is negative; no prospective trading edge has been validated.
6. Shared Coinbase hot wallets, public DEX programs, relayers, DLN solvers, exchange deposits and dust transactions **must not** be used to infer a common individual.

### Scope and reproducibility status

The project's Python and offline receipt tests exercise SPL transfer parsing, balance netting, integer quote allocation, historical window boundary logic, deBridge order checks, BSC receipts and DMAGA–Kekius fixtures. These are evidence consistency checks, not a replacement for collecting historical raw chain data again.

**Important limits:** The archived `trades.parquet`, `wallets.parquet` and all provider raw responses are on an external volume named in [state](../state/STATE.md); their presence was **not verified** in this GitHub-only review. Full PnL recalculation from those raw bytes, transaction-by-transaction USD conversion and a complete receipt-level re-trace of every bridge output remain outstanding. `reports/COORDINATION.md` and `reports/ATTRIBUTION.md` retain legacy accounting views; source-controlled rebuild checks take precedence where they differ. Never interpret a green fixture test as proof of a complete data universe.

**Outstanding quality gates:** [raw-data normalization and coverage status](RESEARCH_STATUS_2026-11-07.md), [prospective signal-validation criteria](SIGNAL_VALIDATION_STATUS_2026-11-18.md), and the [evidence index](EVIDENCE_INDEX_2026-11-18.md) explicitly separate completed findings from further tests.

### Publication principle

This is an **independent, inspectable research portfolio**, not a claim of insider trading by any individual. Its value is in signed-transaction reconstruction, defensible graph inference, adversarial refutation, cross-chain accounting, testable tooling and transparent negative results. Further investigation should produce new receipts or an externally validated, point-in-time signal—not a stronger accusation based on the existing records.

**Version:** 2026-11-18; additive editorial synthesis. The root README, original receipts, frozen studies, historical reports and separate `audit-2026-11-03` branch remain unchanged by this brief.
