# README publication review — 6 November 2026

## Authorization and edit scope

The repository owner explicitly authorized replacing the current Dark-MAGA README's body while **preserving its exact existing title**, `# Dark MAGA: Did Musk Know?`. This change is editorial: it does not substitute new numerical results, recompute wallets, allege individual involvement or modify frozen studies.

Previous title and README are preserved in Git history. The new README is the content of branch `docs/readme-evidence-story-and-grok-pass3-2026-11-06` at commit `4095c901a4729381d83518375acdf053eecd767d`; the resulting README Git blob is `3df87a82ccce0c5e7746838c5320e987b8b9528b`.

## Claim-to-source trace

| Published README claim | Primary repository evidence | Required interpretation |
|---|---|---|
| Launch 14 July, profile change 21 July | `docs/CASE_REPORT.md`; `docs/SOCIAL_FINDINGS.md` | Avatar adoption time is interval-bound, not a proved second |
| H3Qs 2 buys, 48 sales, first buy, $1,086.77 cost, 5,490.86 SOL/$990,743.77 realized trading PnL | `reports/TOP_TRADERS.md`; `docs/README_REVIEW_2026-11-05.md` | Reconstruction of trading PnL only; not bank cash-out, net taxes or attribution |
| 33 wallets, 40 direct transfers ≥1M DMAGA, 15 in first hour, holding upper bound 217M and ~23% of non-pool supply | `reports/COORDINATION.md`; `docs/CASE_REPORT.md` | Component and upper bound; not one owner |
| 4,525 SOL sale proceeds and 2.4% of market proceeds in 24h | `reports/COORDINATION.md`; `docs/README_REVIEW_2026-11-05.md` | Sale proceeds, not realized profit |
| 14 early Coinbase first fundings over 507 s, subsequent convergence on two deposits | `docs/CASE_REPORT.md`; `docs/README_REVIEW_2026-11-05.md` | Exchange funding is a trace boundary; first-funding timing does not identify persons |
| 27 qualified common deposit senders, ~71% of incoming value under matched thresholds | `docs/README_REVIEW_2026-11-05.md` | Threshold-defined shared senders, not evidence of shared account holder |
| 76 deBridge source-side orders, 1,018,687.18 nominal USDC, 41 matched Ethereum executions | `docs/README_REVIEW_2026-11-05.md` (audit I reconciliation); `investigations/2026-11-05_evm-recipient-deeptrace/FINDINGS.md` | All investigated populations, not only 33; fixed SOL fees excluded; source-side funds, not profit |
| July 22: three makers/four orders, 263,573.15 source-side USDC into one EVM recipient | `docs/README_REVIEW_2026-11-05.md`; `investigations/2026-11-05_evm-recipient-deeptrace/FINDINGS.md` | Same recipient does not identify a natural person |
| EVM → Base/BSC → Solana trace | `investigations/2026-11-06_debridge_base_bsc_solana/FINDINGS.md` | Later flow evidence, different order universe; do not add to the 76-order total |
| Screenshot post dated 21 July 19:25:23 UTC, candidate documentary upper bound | `docs/historical/pass2/DMAGA_X_NEW_FINDINGS.md` N07, JSONL source `1815105812076904904`; `docs/historical/pass2/README.md` | Post time and reported screenshot: media bytes not independently authenticated in this editorial pass |
| Study of 211 peer tokens | `etude_final/results.md` | Separate statistical control, not advance-knowledge proof |
| Historical passes, 1,001 posts in pass 2 | `docs/historical/pass2/README.md`; `data/historical_x_pass2/` | Archive record count, not witnesses or validated transactions |

## Publication protection

The repository's `scripts/check_publication.py` requires a pinned README Git blob, a baseline content commit ancestral to the candidate, and unmodified frozen protocol files. Publication policy needs an explicit **main-target baseline update** corresponding to this authorized README; do not disable or alter the guard or its CI workflow. The `audit-2026-11-03` target and all protocol locks remain unchanged.

The accompanying `docs/historical/pass3/PROMPT_GROK_BOT.md` is a **prompt for a future single historical research run**, not evidence that this bot has executed or that more financial claims have been checked. The prompt permits a dedicated PR for new evidence only, not direct edits to `main`, historical reports or protected research inputs.
