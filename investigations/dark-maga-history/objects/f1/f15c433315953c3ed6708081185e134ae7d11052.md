# Evidence index and claim-control matrix
**Dark MAGA / DMAGA | Updated 18 November 2026 | Public research index**

This is a source map for reviewers and future investigators—not a new transaction collection. **A recorded transaction confirms a transfer, not common ownership, motive, identity, unlawful conduct or advance knowledge.**

## 1. Evidence standards

| Label | Meaning | Publication rule |
|---|---|---|
| **A — transaction / artifact verified** | Exact receipt, on-chain transfer, recorded primary X post or explicitly timestamped archive inspected by an original investigation, with signature/post ID | State only the observable action and its scope; preserved evidence may still have provider limitations |
| **B — corroborated** | Multiple consistent primary-source observations or a properly reconstructed accounting result | Identify the method, input window, dependencies and exclusions |
| **C — hypothesis / exploratory** | Indirect graph relationship, suggestive timing, or post-hoc association | Give rival explanations, base-rate gap and falsification test; never elevate to identification |
| **D — unverified / rejected** | Missing raw transaction path, shared service masquerading as identity, contradicted timestamp/amount, or unresolved claim | Retain transparently as a negative result |

This matrix organizes the existing repository's classifications. It is not a replacement for the A–D labels inside dated investigations.

## 2. Core claim register

| ID | Finding | Direct evidence / method | Current interpretation | Remaining gate |
|---|---|---|---|---|
| MINT-01 | Created 14 July 2024 02:05:25 UTC | [Timeline with full mint signature and slot](TIMELINE.md); [case report](CASE_REPORT.md) | **A:** mint and migration chronology | None for the timestamp; creator's identity remains unknown |
| SOCIAL-01 | Prior DMAGA publicity and avatar image visible publicly | [Social findings](SOCIAL_FINDINGS.md); [X-post reconciliations](../investigations/2026-11-06_historical_replay/data/x_observations_reconciled.csv) | **A/B:** public tokens and imagery predate profile change | Recover missing 16:00:08 media if a lawful primary archive exists |
| AVATAR-01 | Old avatar visible 19:03:27; first known new-avatar screenshot posted 19:25:23 | [Timeline](TIMELINE.md); [historical replay](../investigations/2026-11-06_historical_replay/FINDINGS.md) | **A for archive/post timestamps; B for screenshot content:** actual switch occurred within documentary bounds, not necessarily at screenshot posting | Earlier authenticated avatar observation, direct platform event log |
| FLOW-01 | H3Qs 2 buys / 48 sales; ~5,490.86 SOL reconstructed trading PnL | [Top-trader table](../reports/TOP_TRADERS.md); [alternate replay by mint](../investigations/2026-11-06_historical_replay/data/h3qs_by_mint.csv) | **B:** trade-accounting result, not full net cash-out | Source-by-source re-execution with historical SOL/USD and all excluded fees |
| FLOW-02 | 33 wallets joined by 40 direct DMAGA transfers | [Group edge check](../reports/data_checks/group_edges_check.json); [case report](CASE_REPORT.md) | **A for direct transfers; B for connected component:** identity not established | Review costs on inter-wallet transfers and all unobserved transfers |
| FLOW-03 | 217.037M tokens before Musk as an upper bound; 4,524.914 SOL sold in first 24h | [Rebuilt component checks](../reports/data_checks/sigrule_20261107.json); [rebuild memo](REBUILD_2026-11-07.md) | **B:** defined population and distinct accounting windows | Full external-data re-normalization; avoid stale `COORDINATION.md` figures |
| FLOW-04 | 7GVC's 189.656068999 SOL originated from closure of own Jupiter position | [Signed receipt replay](../investigations/2026-11-06_historical_replay/FINDINGS.md); [receipt fixtures](../investigations/2026-11-06_historical_replay/tests/test_replay.py) | **A:** *not* evidence of outside mystery funding | No new attribution from this event |
| FLOW-05 | 7GVC's 20M-token transfer and satellite SOL funding | [Historical replay and receipts](../investigations/2026-11-06_historical_replay/FINDINGS.md) | **A for transfers; C for owner-level coordination:** common signers or human identity not proven | Broader counterparty checks without exchange-hub links |
| BRIDGE-01 | 76 source orders / 1,018,687.178289 USDC commitments (includes 407.474833 USDC proportional fees) | [Order-by-order CSV](../investigations/2026-11-05_debridge_winners/TABLE_DEBRIDGE_ORDERS.csv); [validator](../investigations/2026-11-05_debridge_winners/validate.py) | **B for decoded order commitments:** not equivalent to DMAGA trading proceeds | Full destination receipt validation and ultimate exposure accounting |
| BRIDGE-02 | 4 orders, 3 Solana makers, 1 Ethereum recipient, 263,573.151396 USDC source commitments | [Same order CSV](../investigations/2026-11-05_debridge_winners/TABLE_DEBRIDGE_ORDERS.csv) | **B:** convergent transfer destination, not a natural person | Separate source-of-funds reconciliation; destination onward flows |
| BRIDGE-03 | Two BSC fulfilments on 20 March 2025, 9,908.862223 USDC source | [Receipt-backed follow-up](../investigations/2026-11-13_debridge_bsc_delivery/FINDINGS.md); [BSC order CSV](../investigations/2026-11-13_debridge_bsc_delivery/data/ordres_dln.csv) | **A/B:** specific receipt/order correlation; credited BNB balance delta not independently recomputed | Trace intra-wallet balances, source accounting discrepancy vs earlier 9,912.827353 USDC |
| STATS-01 | 211 controls, 7 primary measures, min p = 0.15566; Holm negative | [Frozen analysis plan](../etude_final/analysis_plan.md), [metrics CSV](../etude_final/derived/metrics.csv), [tests JSON](../etude_final/tables/tests.json) | **B:** table-level reproduction supports exact published negative statistical result | Independent raw data rebuild, alternative population/out-of-sample power analysis |
| KEKIUS-01 | No confirmed DMAGA core-group overlap with tested Kekius buyer sets | [Cross-token findings](../investigations/2026-11-06_dmaga_kekius_cross_token/FINDINGS.md) | **B:** absence in the *specified* address/token/time universe, not a global negative | Non-ATA accounts, other token copies, independent unmatched controls |
| RESEARCH-01 | No validated pre-catalyst trading advantage after execution costs | [Study verdict](../etude_final/results.md); [validation standard](SIGNAL_VALIDATION_STATUS_2026-11-18.md) | **D as a positive claim:** signal not established | Pre-registered independent study and prospective log |

## 3. Audit corrections that must travel with the claims

**Historical windows:** [10 November audit](AUDIT_2026-11-10.md) finds two trades totaling **0.277882029 SOL** counted at the old high-bound edge in both segments. The corrected sub-window is **17.561 SOL** (not 17.838882029), while the entire uncertain window remains **20.851551083 SOL**. Use half-open `[start,end)` intervals.

**SPL ledger / PnL:** [7 November rebuild](REBUILD_2026-11-07.md) and [10 November audit](AUDIT_2026-11-10.md) document double counting of transfer legs and cost-basis effects. The code now nets eligible transfers per signature and owner, allocates quotes in integer units, and fails if historical required prices are invalid/missing. Historic exported Parquet is not committed.

**deBridge accounting:** The 76-order register spans **May 2024–June 2025** and includes **18 orders created before the 14 July 2024 DMAGA mint**, totaling **4,632.170480 USDC** of source commitments. These orders are relevant to prior wallet history but **cannot** be proceeds of future DMAGA trades. Of the 76 entries, **31** are `archive_match_with_tx_hash`, **10** are `archive_match_without_tx_hash`, and **35** remain `unverified` *in that particular CSV*. Newer multichain investigations have additional evidence under **different order universes**; don't sum their counts to 76 or treat every archival match as equivalent to a full receipt check. Full per-row [register](../investigations/2026-11-05_debridge_winners/TABLE_DEBRIDGE_ORDERS.csv).

**RETIREDIO timing:** [Issue #36](https://github.com/searadacunha/DARK-MAGA/issues/36) documents the historical replay script's inclusion of a token debit up to **60 seconds after** the DMAGA buy while describing a pre-buy rotation. One specific wallet had a reported debit **50 seconds after** its DMAGA buy; the 11 vs 4 exploratory rotation counts need re-execution and should not be promoted to a validated early predictor.

**Study contamination and pre-registration:** `etude/` contains a contaminated experimental registry and is not an independent validation dataset. The frozen `etude_final/` study has a protocol lock, corrections in dated amendments, and a negative result. The seven measures were defined after some DMAGA exploratory facts were already known; this is not blind hypothesis generation.

**Shared services:** A Coinbase hot wallet, exchange deposit, route executor, liquidity pool, Jito tip recipient, DLN solver and dust distributor can connect thousands of independent traders. A graph path through any such service **does not prove** shared human identity.

## 4. Negative and refuted interpretations worth preserving

- **Rejected:** `189.656 SOL` as unexplained third-party funding; Jupiter Perpetuals closed 7GVC's own position.
- **Rejected:** profile-switch time as exactly the first screenshot post time; only a documentary interval survives.
- **Rejected:** automatic linkage of the token creator with the precise 33-wallet direct-transfer component.
- **Rejected:** shared centralized-exchange infrastructure implies one operator.
- **Not established:** Musk or the named X users owned any cited wallets.
- **Not established:** a documented direct financial operator group recurring between DMAGA's core winners and Kekius.
- **Not established:** statistical outlier on frozen seven-measure study; best rank p 0.15566.
- **Not established:** advance information, manipulation intent or any tradable net-positive predictive edge.

## 5. Audit-readiness checklist

- Read [publication policy](../AGENTS.md) and [reproduction guide](REPRODUCTION.md) before editing.
- Verify external storage is actually mounted before claiming a complete raw-data replay.
- Preserve `etude_final/PROTOCOL.lock`, every frozen file and the original archived `etude/` registry.
- Run cached receipt/fixture validators and publication guard; record actual command, environment and pass/fail.
- Never edit generated legacy tables to cosmetically reconcile two incompatible windows.
- Attribute new hypotheses, reference data and third-party research with provenance and license. A secondary article is not a second independent observation.
- Log unanswered questions as open work, not as affirmative evidence.

**Public-facing framing:** *A forensic reconstruction of money flows around an event, with strict attribution limits and a falsifiable negative result.* 
