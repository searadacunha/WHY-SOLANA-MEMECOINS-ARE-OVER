# README review and publication record, 5 November 2026

## Authorization and scope

Benjamin explicitly requested a stronger English Dark MAGA repository presentation in the narrative style of his Solana memecoin and Polymarket README files, centered on whether Musk's action created an insider-trading opportunity. This authorizes replacement of the root README, not alteration of evidence or frozen protocols.

The chosen question is: "Did anyone trade on advance knowledge of Elon Musk's profile-picture change?" It does not assert that Musk knowingly facilitated a scheme.

Source snapshot: `audit-2026-11-03` at `6e839acc022a38427fdb1f4f3b221488db454a78`. Main parent: `692ec9f5eaf402138ea036fa3fdd39613288c14f`. Style references were read, not modified: `searadacunha/Why-Solana-Memecoins-Are-Over/README.md` and `searadacunha/Polymarket-Home-of-the-Insiders/README.md`.

## Evidence ledger

All paths below refer to the source snapshot above.

| README claim | Source | Interpretation retained |
|---|---|---|
| Profile change on 21 July 2024 | `docs/SOCIAL_FINDINGS.md`, section 3 | Documented change window 19:03:27-19:30:13 UTC. The image-upload identifier is not described as an independently proven exact adoption time. |
| H3QsBr: $1,086.77 cost; 5,490.86 SOL and $990,743.77 realized trading PnL | `reports/TOP_TRADERS.md`; `work_H/REAUDIT_CONCLUSIONS.md`, section 4, Essentiel 6 | Reconstructed trade accounting, not peak valuation, a bank cash-out or an all-cost return. No private-information attribution. |
| H3QsBr: two buys, 48 sales, first buy 14 July 16:43:58, last sale 23 July | `reports/TOP_TRADERS.md`, first wallet row | The buyer is not assigned to the creator or the 33-wallet component. |
| 33 wallets, 40 direct token transfers, 15 first-hour buyers | `docs/CASE_REPORT.md`, Essentiel 4; H section 4 | Descriptive component. Creator outside it; common ownership not established. |
| Up to 217 million tokens before Musk, about 23% outside pools | H section 4, Essentiel 4 | Upper bound; denominator is 937.765 million tokens outside pools, not total supply. |
| About 4,525 SOL sold in the 24-hour window, 2.4% of market sales | H section 4, Essentiel 4 | 4,524.91 / 190,546.47 SOL; sale proceeds, not profit. |
| Fourteen first-funding transactions in 507 seconds, later deposit convergence | `work_I/REFUTATION.md`, section 2; `docs/CASE_REPORT.md`, creation transaction | The 14 transactions were re-read by I. The README does not reproduce the 2,201-population denominator as newly verified or call the selected window a prospective test. |
| 27 shared qualifying senders, about 71% of incoming amounts per deposit | I section 1 | Threshold-dependent overlap; no ultimate-beneficiary identity. One sending account reaches the USDC deposit through a program. |
| 76 orders, 1,018,687.18 nominal USDC including proportional fees | I section 4; `work_I/i14_orders.csv`, `i15_dln_sum.txt` | Source-side USDC; fixed SOL fees excluded. All investigated populations, not the exact 33-wallet group alone. |
| 41 Ethereum executions; 942,534.32 source-side USDC | I section 4 | Matched executions, not an assertion that the destination received that amount in USDC. Thirty-five arrivals remain unverified in that review. |
| Three Solana makers, four orders, one Ethereum recipient, 263,573.15 source-side USDC in 9 min 36 s | I section 4; `i15_dln_sum.txt`, 0xb947 detail | Period is 22 July 2024, 00:54:36-01:04:12 UTC. The common receiver is not assigned to a named person. |
| 211 comparison tokens; low sensitivity of the frozen test | `docs/CASE_REPORT.md`, Essentiel 3; H section 4 | Non-detection does not establish absence of advance knowledge. No insider-trading finding or Musk participation is asserted. |

`work_H` and `work_I` abbreviate `audits/2026-11-03/work_H` and `audits/2026-11-03/work_I`.

## Bridge-source correction

The previous audit README used `work_G/g43_orders.csv` directly: 1,023,933.51 USD across 76 rows and 979,324.28 USD for 68 rows assigned to the exact 33-wallet group.

I section 4 explicitly identifies two erroneous `usd_sortis` entries in that CSV. Its independent event decoder gives 1,018,687.18 nominal USDC across the 76 orders. The new README uses this corrected decoded total and labels the population, fee treatment and execution coverage.

The editorial revision did not modify the historical CSV, rerun its decoder or regenerate `docs/CASE_REPORT.md`. At that stage, the generated bridge paragraph and its generator still used the old table. The targeted follow-up below synchronizes them with the decoded source. The README links the decoded table and I's reconciliation directly.

## Targeted bridge synchronization, 5 November 2026

The audit branch's `scripts/rep_90_case.py` now reads `work_I/i14_orders.csv` through `dmaga/debridge.py`. The helper sums integer `give_amount + fee_pct` units before converting to nominal USDC. Proportional fees are included; fixed SOL fees are excluded. No USD exchange-rate estimate or destination receipt is substituted for that source-side amount.

| Population | Orders | Nominal source USDC, before display rounding |
|---|---:|---:|
| All collected populations | 76 | 1,018,687.178289 |
| Makers belonging to the exact 33-wallet component | 68 | 974,077.946152 |
| Other makers | 8 | 44,609.232137 |
| Exact-component orders before mint creation | 15 | 1,610.177867 |

Membership uses the decoded `maker`. Four orders were found in cache files named after other wallets; using `wallet_file` would wrongly omit 175,439.743465 USDC from the component. The historical `work_G/g43_orders.csv` and the decoded I table remain unchanged.

The `C73Yv9iH…` figures also retain their separate scopes: 29 orders and 527,600.400084 USDC across all destinations; 27 orders and 496,371.589492 USDC specifically toward `0x2d86499a…` on Ethereum, spread from 21 July 2024 through 9 June 2025.

Only point 9 of `docs/CASE_REPORT.md` was regenerated using the same pure helper now called by the full report generator. The 41 matched Ethereum executions and associated 942,534.32 source-side USDC remain explicitly attributed to I's archived review; no new raw decoding or destination-chain verification is claimed.

Verification: 21 targeted bridge regressions and the complete local offline suite, **96 tests passed**, using Python 3.12 and the pinned `requirements-test.txt` dependencies through `scripts/guard.py`. Both protocol-lock tests passed, covering the frozen study files. The new tests cover exact micro-USDC totals, maker/cache differences, native-fee exclusion, pre-mint timing, duplicate or invalid rows and agreement between the published paragraph and its recalculation. The external raw archive was unavailable, so the full report pipeline and `scripts/chk_90_selfcheck.py` were not run. The root README, its baseline and frozen protocols are unchanged.

## D01 is preserved, not blindly merged

The published commit `6143964e532cb60a7d3938a1f4d175ada895b00c` on `d01-correction` changes more than the point-9 paragraph. Among other changes it imports `texte_i` and loads `audits/2026-11-03/work_F/f20_passe2.json`.

A read of that JSON on `d01-correction` returned 404 during this review. The user's local status also showed it as untracked. This revision therefore does not merge the entire D01 commit or claim that the local uncommitted work is available on GitHub.

## Deliberate README-baseline revision

The repository guard intentionally pins the accepted README blob to a historical commit. Its policy must change when the user explicitly requests a new README.

For each target separately, create a content commit based on that target's current remote tree, then a child policy commit pinning that target to the new content commit and README blob. Preserve the other target's rule, both prior correction histories, and every `protocol_locks` entry. Do not weaken or edit the guard or its workflow.

Only the root README, this review record, `docs/REPRODUCTION.md` and the target's entry in `state/publication_baselines.json` belong to this editorial publication. No frozen file, raw record, computation code or other repository is modified. The main and audit research trees are not merged into each other.

## Verification boundary

The work is a source-grounded editorial review of committed material. No external raw archive or Mac working directory was available, and no full scientific validation or report regeneration is claimed. Software CI and ancestry checks, when run on the publication candidate, are separate from validation of the underlying investigation.
