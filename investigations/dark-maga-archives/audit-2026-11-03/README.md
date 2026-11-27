# Dark MAGA: Did Musk Know?

On **July 21, 2024**, Elon Musk changed his X profile picture to a Dark MAGA image.

A Solana memecoin using the same imagery, **$DMAGA**, had launched a week earlier.

Buying accelerated around the profile change. But some wallets were already holding the token.

One early buyer had spent approximately **$1,087**. Its reconstructed realized trading PnL reached **$990,744**.

That raised the question behind this investigation:

> **Did anyone trade on advance knowledge of Elon Musk's profile-picture change?**

I reconstructed the trading, traced the funding, mapped financial connections and followed the money across blockchains.

Here is what the evidence shows.

[Profile-change chronology][social] · [Trading reconstruction][traders] · [Numerical review][review-h]

---

# 1. The Buyer Who Was Already There

The wallet was:

`H3QsBrrivimFJmSpTXuvig2n1Bh7JuYxrriRSEszT6cc`

Its first recorded purchase was on **July 14, 2024, at 16:43:58 UTC**, seven days before the profile change.

The reconstructed record contains **two purchases and 48 sales**.

| Recorded trading activity | Result |
|---|---:|
| Purchase cost | **$1,086.77** |
| Realized trading PnL | **5,490.86 SOL** |
| Trading PnL in USD | **$990,743.77** |
| Last recorded sale | July 23, 2024 |

The USD accounting uses prices at the time of the trades.

This is reconstructed trading PnL, not a peak portfolio valuation or a verified withdrawal to a bank account. It is not presented as an all-cost, after-tax return.

The investigation starts with the transactions: **who bought, when they bought, and what happened to the money.**

[Trade history and accounting definitions][traders] · [Cross-checked figures][review-h]

---

# 2. Thirty-Three Wallets. Forty Direct Transfers.

A separate part of the investigation reconstructed a component of **33 wallets connected by 40 direct $DMAGA transfers**, each involving at least one million tokens.

These links are token transfers between the addresses, not merely use of the same exchange or trading service.

**Fifteen of the 33 wallets bought during the token's first hour.**

Their reconstructed holdings before Musk's profile change reached an **upper bound of 217 million tokens**, approximately **23% of the tokens outside liquidity pools** at that point.

In the following 24-hour window, their recorded swap sales generated approximately **4,525 SOL in proceeds**.

That is sale proceeds, not profit, and it represents approximately **2.4% of recorded market-wide sale proceeds** in that window.

The token creator is **outside** this 33-wallet component. The early buyer above is not being assigned to it either.

**The finding is a measurable network of transfers and positions. It is not proof that all 33 wallets belong to one person.**

[Component, holdings and sales][case] · [Independent numerical checks][review-h]

---

# 3. The Creator's Trail: Funding In, Deposits Out

The creator's financial trail led to a different set of addresses.

On **July 14, 2024, between 01:32:23 and 01:40:50 UTC**, fourteen wallets received their first recorded funding through Coinbase hot wallets.

The token was created at **02:05:25 UTC**.

The fourteen, including the creator, later paid into at least one of two deposit addresses examined in the investigation:

- `9W9b3zgHH9mCEHDhsdbnbEPHStm9vvXS4aia4DWHBxpL`
- `Caw4RrwkmxqtbLSFzgSs6id3XiFxWQxs2t1mrn5a3mME`

The relevant pattern was not simply "these wallets used Coinbase."

It was **closely timed first funding, followed by later convergence on specific deposit addresses**.

Across the reviewed histories, the two deposits shared **27 qualifying sending wallets**. Those shared senders accounted for approximately **71% of the incoming amounts on each side**, under the review's stated thresholds.

The addresses are strongly corroborated as Coinbase deposit accounts. Their account holders and ultimate beneficiaries are not identified.

The funding-and-deposit pattern also appears outside the token's launch period.

[Funding sequence, deposit overlap and transaction checks][review-i]

---

# 4. The Trail Did Not End on Solana

The cross-chain investigation decoded **76 deBridge orders** across the investigated wallet populations.

Their source-side amount, including the proportional bridge fee, was **1,018,687.18 USDC**.

| Cross-chain evidence | Recorded result |
|---|---:|
| Decoded orders, all investigated populations | **76** |
| Source-side USDC, including proportional fees | **1,018,687.18** |
| Orders with execution matched on Ethereum | **41** |
| Source-side USDC associated with those 41 orders | **942,534.32** |

The remaining **35 destination executions are not verified in the published review**. Fixed SOL fees are excluded from the USDC totals.

These are orders across the collected histories, including activity outside the July 21 event. They are not all attributed to the exact 33-wallet component, and their full value is not claimed to be $DMAGA profit.

One route is particularly concrete:

**Three Solana wallets. Four orders. The same Ethereum recipient. Nine minutes and 36 seconds.**

On **July 22, 2024**, those orders committed **263,573.15 USDC** on the source side and named this recipient:

`0xb947bf7f409e998b28f8e218802fc9575c3c8c57`

All four destination executions were matched in the review.

This connects the source orders to a shared destination. It does not identify the person behind that destination.

[Decoded orders][orders] · [Cross-chain reconciliation and execution evidence][review-i]

---

# 5. Follow the Evidence

This repository combines **Solana transaction reconstruction, wallet-network analysis, exchange-deposit tracing, cross-chain order matching, public-source chronology and statistical testing**.

| Start here | What it contains |
|---|---|
| [Trading reconstruction][traders] | Purchases, sales, accounting definitions and wallet-level results. |
| [Case report][case] | The investigation's detailed findings and evidence levels. |
| [H numerical review][review-h] and [I transaction review][review-i] | Claim-level checks, corrections and the scope of each conclusion. |
| [Decoded bridge orders][orders] | Source transactions, makers, amounts and destination recipients. |
| [Frozen study][study] | Protocol, comparison data and statistical results. |
| [Reproduction and branch guide](docs/REPRODUCTION.md) | Code checks, external-data requirements and research handover. |

The evidence links above point to a fixed snapshot of the research branch. Where an older synthesis conflicts with a later transaction-level correction, the later correction governs the figures used here. The [README evidence ledger](docs/README_REVIEW_2026-11-05.md) records those choices.

**Research status:** the findings above are scoped to the cited records; full investigation validation remains pending. The complete raw archive is external to Git, so a checkout alone cannot reproduce every result.

Detailed research material is in French. This overview is in English.

**Solana mint:** `7D7BRcBYepfi77vxySapmeqRNN1wsBBxnFPJGbH5pump`

[social]: https://github.com/searadacunha/Dark-MAGA-Investigation/blob/6e839acc022a38427fdb1f4f3b221488db454a78/docs/SOCIAL_FINDINGS.md
[traders]: https://github.com/searadacunha/Dark-MAGA-Investigation/blob/6e839acc022a38427fdb1f4f3b221488db454a78/reports/TOP_TRADERS.md
[review-h]: https://github.com/searadacunha/Dark-MAGA-Investigation/blob/6e839acc022a38427fdb1f4f3b221488db454a78/audits/2026-11-03/work_H/REAUDIT_CONCLUSIONS.md
[review-i]: https://github.com/searadacunha/Dark-MAGA-Investigation/blob/6e839acc022a38427fdb1f4f3b221488db454a78/audits/2026-11-03/work_I/REFUTATION.md
[case]: https://github.com/searadacunha/Dark-MAGA-Investigation/blob/6e839acc022a38427fdb1f4f3b221488db454a78/docs/CASE_REPORT.md
[orders]: https://github.com/searadacunha/Dark-MAGA-Investigation/blob/6e839acc022a38427fdb1f4f3b221488db454a78/audits/2026-11-03/work_I/i14_orders.csv
[study]: https://github.com/searadacunha/Dark-MAGA-Investigation/blob/6e839acc022a38427fdb1f4f3b221488db454a78/etude_final/results.md
