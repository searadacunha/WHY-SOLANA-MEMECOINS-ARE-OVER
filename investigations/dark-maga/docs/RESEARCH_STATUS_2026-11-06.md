# Dark-MAGA research status — 6 November 2026

**Purpose:** a single decision-focused register of what has changed, what is already demonstrated by recorded transactions, and which *specific* tests must run next. Avoid restarting retrospective X searches unless a new transaction ID or documentary contradiction requires them.

## Research versions

- **Published `main`:** established H3Qs realized trading calculation, the separately defined 33-wallet direct token-transfer component, Coinbase funding/deposit observations and decoded deBridge order sets. See root README and the attached evidence links. These are different sampling populations and must never be summed or presented as one owner.
- **[PR #25](https://github.com/searadacunha/Dark-MAGA/pull/25) — on-chain historical replay, OPEN:** receipt-backed claims with 76 frozen receipts, scripts and offline tests; its CI checks pass. This branch has not yet been independently reviewed end-to-end or merged. Treat its exact new figures as **replay findings under review**, not as validated `main` statistics.
- **[Grok pass 3](historical/pass3/README.md):** seven documentary findings and 316 new X posts. **Zero new transfer signatures** authenticated by that collection. Three actionable deltas are 9Sxm's screenshot trading fingerprint, an earlier 6QFD holding snapshot, and dated BARRON/DMAGA social overlap.

## Most important change in PR #25

The replay identifies the alleged ~190 SOL Jupiter Perpetuals receipt as **7GVC's own closed position** (189.656068999 SOL at 01:32:11 UTC, 14 July 2024), not a new third-party funding identity.

It also reconstructs 7GVC's 41,197,138.380017 DMAGA bought for 7.903073760 SOL; a directly signed 20,000,000 DMAGA transfer to 9Sxm; 5 SOL to A1UD; 30+30 SOL to 6QFD; 16 SOL to H4mQ; and subsequent early purchases. These are receipt-level transfer findings, not an attribution to a person.

A broader multi-asset trail between 7GVC, 9Sxm, AeiMit and satellites, including transfers preceding July 2024, supports a **coordination hypothesis** with several direct counterparties. No shared private key, common legal beneficiary, knowledge of Musk's decision or deliberate market manipulation is established.

PR #25 further reports:
- 141 direct intra-group transfers across Noah's four proposed groupings under its matching rules (zero cross-group in the tested edge universe);
- 6.751% aggregated balances for Noah group 2 versus the rounded contemporaneous 6.73% quote;
- an earlier documentary upper bound for the changed Musk profile of **19:25:23 UTC**. The [19:03:27,19:25:23) uncertain window contains **20.85 SOL** in its recomputation versus **148.73 SOL** under the previous upper bound;
- KLLARY as a historically traded mint for 7GVC and 9Sxm *before* DMAGA.

All of the above depend on the explicit transaction/coverage limits in [the replay report](https://github.com/searadacunha/Dark-MAGA/blob/investigate/dmaga-historical-replay-20261106/investigations/2026-11-06_historical_replay/FINDINGS.md). Do not assign financial evidence to a person through a shared service, a tweet, an illustrated avatar, or a transfer alone.

## High-priority gates for PR #25 and public README numeric updates

**Gate 1 — Transfer completeness (blocking).** PR #25 documents **22,152 of 57,828 sampled SPL transfer edges missing from `trades.parquet`** because ordinary SPL `Transfer` instructions can omit the mint from the message account list. This is a real coverage defect; its impact on graph membership, historical balances, cost basis, realized PnL, and derived populations must be measured, fixed and regression-tested. A balance held only in `trades.parquet` is not automatically reliable. Where repair requires an external dataset, identify all affected reports and do not claim the repaired figures yet.

**Gate 2 — Generated report synchronization (blocking).** PR #25 regenerates `events.json`, `windows.csv`, `cohorts.parquet` and `TIMELINE.md` but explicitly leaves `CASE_REPORT`, `EARLY_BUYERS`, `TOP_TRADERS` and other readers of those files at previous 19:30:13 bound. Before treating new cohort comparisons as public final numbers, regenerate **only with the source ledgers present** or version the downstream reports as historical and mark the new derivations as such. Tests must assert event-window consistency and identify changed claims; never silently patch numeric Markdown.

**Gate 3 — Independent receipt and classification audit (blocking for merging unqualified financial conclusions).** Recheck the actual instruction paths, signer/owner assumptions, SOL/WSOL rent and fee accounting, Jupiter program flow, KLLARY mint, 7GVC→9Sxm and three satellites, Noah service filtering, and the exact source of transfer edges. Confirm the 76-receipt sample's coverage against all financial assertions, including those derived from uncommitted external datasets.

**Gate 4 — Three new falsifiable Grok tests.** First match the 9Sxm screenshot's **1.8M DMAGA→17.875 SOL** trade (15 July, interface timezone unknown) in the existing 13–25 July ledger; second align 6QFD's **15.3M/1.53%** holding snapshot to a bounded series of valid slot balances; third compare **BARRON vs DMAGA creator/deployer/funding flows**, checking CTO-date/mint ambiguity and excluding common services. Save transaction signatures, exact raw balances, confidence and falsification criteria for each.

**Gate 5 — Public claims and publication checks.** Preserve the root README title `# Dark MAGA: Did Musk Know?`, the frozen protocols and independent deBridge/Kekius investigations. Do not publish “Musk knew,” common wallet ownership, or same BARRON/DMAGA controller without discriminating evidence. Keep the documentary/social discoveries outside financial verdict tables. All affected offline and publication-guard tests must pass; no force pushes.

## When further X searching is justified

Only after a concrete missing input is identified: an original image hash, an unavailable quoted parent, a contract address uniquely tied to a transaction, or an actually missing primary post. A fourth broad X sweep will add little while the above gates remain open.

## Current verdict

**Direct multi-wallet financial relationships are now materially better evidenced than at the start of the project.** The investigated behavior is consistent with shared funding and coordinated trading, but evidence of an advance-knowledge scheme involving Musk remains **unproven**. The highest-leverage next work is **fixing transfer coverage, consolidating the replay and testing the BARRON link**, not expanding the social-post count.
