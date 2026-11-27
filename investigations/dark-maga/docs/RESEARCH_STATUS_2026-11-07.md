# Dark-MAGA — consolidated research status, 7 November 2026

## Publication state

Two formerly stacked investigations have been merged into `main`:

- [PR #25 — transaction-level historical replay](https://github.com/searadacunha/Dark-MAGA/pull/25). On-chain receipts for the 7GVC/Jupiter position close, $DMAGA buys, 7GVC→9Sxm token transfer, three satellite fundings, Noah wallet relationships, selected KLLARY activity and historical X attribution.
- [PR #28 — SPL transfer coverage and deduplicated reconstruction](https://github.com/searadacunha/Dark-MAGA/pull/28). A shared mint-preserving SPL decoder, 913,880 deduplicated trading rows, recalculated wallet/PnL figures, regenerated `CASE_REPORT`, `EARLY_BUYERS`, `TOP_TRADERS` and the event-dependent visualizations. CI also tests a transient WSOL account's rent refund.

Both PRs have published receipts and reproducible offline tests. The final PR CI checks passed on the target branches. This does **not** mean that all historical on-chain records have been independently collected from scratch: some external datasets and service attribution remain limited.

## Strongest findings: what the actual transactions establish

1. **7GVC's Jupiter Perpetuals position closed before the token launch.** `7GVCZAYG5NfiJsuqUdvc9hB2ts2W3tSrGdya4CyR1M5j` received 189.656068999 SOL on 14 July 2024 at 01:32:11 UTC, 33 min 14 s before the DMAGA mint. The relevant instruction returned funds from **7GVC's own position**, not from an independently identified person funding it.
2. **A directly signed 20M $DMAGA transfer.** 7GVC bought 41,197,138.380017 DMAGA in two launch-period transactions for 7.903073760 SOL, then directly transferred 20,000,000 DMAGA to `9Sxmf25WG5WVQ5p86ycWeo5hMEwxiWPkFtLdRdTrHSQS` at 02:23:09 UTC. The token transfer is in the receipt; the elapsed time from the second buy is 11m26s.
3. **Additional direct funding paths.** 7GVC sent 5 SOL to A1UD, 30+30 SOL to 6QFD and 16 SOL to H4mQ. Their subsequent DMAGA purchases were traced, and the amounts and signatures are recorded in the replay.
4. **Preexisting wallet relationships.** 7GVC, 9Sxm, AeiMit and several satellites exchanged funds directly, including transactions preceding July 2024. This materially strengthens a **financial-link / possible coordination** hypothesis. A single owner, a legal beneficiary, an exchange customer or knowledge of Musk's decision are **not identified** by those transfers.
5. **Noah's historical network.** Four proposed groups were tested using 141 direct intra-group edges, with balances checked against historical ATA transactions. Common-service counterparties and mere social connections are not converted into ownership evidence.
6. **Grok pass 3 is now reconciled.** The historical 9Sxm screenshot's ~1.8M DMAGA → ~17.875 SOL corresponds to a raw swap at 2024-07-15 16:59:20 UTC: the swap's gross WSOL leg is 17.874608396 SOL; the screenshot displayed 09:59 (consistent with UTC−7). The earlier 6QFD holder screenshot is compatible with the token balance in the relevant period. The BARRON–DMAGA "same team" claims have **no demonstrated shared mint funder, wallet transfer or token overlap** in the tested histories.

The avatar change is bounded by a documented old-profile view at 19:03:27 UTC and a published new-profile screenshot at 19:25:23 UTC on 21 July. The newer timing reduces the *uncertain* 21m56s trading window to **20.85 SOL of buys**, compared with 148.73 SOL under the former upper bound. A screenshot publication date is not the exact time the profile was changed.

## Rebuilt numbers, with populations kept distinct

| Reconstructed metric | Previous | Published 7 Nov |
|---|---:|---:|
| `trades.parquet` rows | 919,783 | **913,880** |
| Duplicate keys found before rebuild | 5,903 | **0 in re-export** |
| Total wallet realized trading PnL | 100,128.3 SOL | **98,189.9 SOL** |
| Wallets with realized PnL difference greater than 0.01 SOL | — | **765** |
| Largest 33-wallet transfer component | 33 wallets / 40 edges | **Unchanged** |
| Component pre-event holdings upper bound | ~217M DMAGA | **217.037M DMAGA** |
| Component realized trading PnL | 5,594 SOL | **5,472 SOL** |
| Component USD trading PnL | $990,207 | **$969,158** |
| 24h market-wide SOL sale proceeds | 190,551 SOL | **190,355 SOL** |
| Component's 24h swap sale proceeds | ~4,525 SOL | **4,524.914 SOL (~2.38% of market)** |

The reconstructed individual leader remains H3Qs (`H3QsBrrivimFJmSpTXuvig2n1Bh7JuYxrriRSEszT6cc`), about **5,490.86 SOL / $990,744** in realized *trading* PnL, based on the documented accounting model. This is not an after-all-costs bank cash-out.

These figures come from [the 7 November rebuild](REBUILD_2026-11-07.md) and [its machine-readable before/after record](../reports/data_checks/rebuild_20261107.json), not from screenshots.

## What is **not** finished

- **Full raw renormalization not executed.** Re-running `nrm_10_trades.py --force` over roughly 19 GB of historical records is pending. A separate `data_v2` export differs in the *classification* of 4,795 rows even though its referenced balance deltas match. This is a coverage/semantics risk, not yet a falsification of the observed 7GVC transfer receipts.
- **Incomplete universe of token transfers.** The mint-based transaction stream misses ordinary SPL `Transfer` instructions that do not list the mint. The new positions and PnL workflows supplement `gtba` transfer edges, but **transfers between two untracked wallets remain invisible**, and 20 of 1,219 tracked histories were truncated, mostly service accounts.
- **Some reports remain legacy.** `reports/COORDINATION.md`, `reports/ATTRIBUTION.md` and `data/collector.json` depend on Helius historical reads. The markdown reports are prominently labeled as not regenerated. The equivalent recalculated group figures are available in `reports/data_checks/rebuild_20261107.json`.
- **The crucial attribution question remains open.** The project does not have evidence that Musk communicated his future profile change to a trader, that he controlled any identified wallet, or that the project's named promoters controlled the investigated wallets. A social claim of a common BARRON/DMAGA team is not a financial link.

## Next work by evidentiary value

1. **Only if archival data/budget is available:** run the 19 GB full normalization with a before/after acceptance test for the 4,795 disputed classifications; reconcile remaining invisible/truncated transfer paths without treating service hubs as identities.
2. **Resolve specific financial counterparts** of the early direct wallet network and the `9W9b3zg…` collector: demonstrate or falsify identifiable on-chain paths from wallets to launch funding, treasury and exits, with signed transaction evidence. Existing 7GVC connections alone do not identify a person.
3. **Test the strongest alternative explanations** (prior public promotion, independent traders, exchange infrastructure, arbitrage, normal activity on other tokens) with matched controls before adding an insider/coordination label. A broad fourth Grok/X search is not a substitute for this.

**Verdict:** the investigation has substantially strengthened direct financial links among early wallets and made the public analyses internally more coherent. It has **not** established privileged information about Musk's avatar change, a shared private-key controller, or intentional criminal manipulation.
