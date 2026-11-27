# Dark MAGA: Did Musk Know?

*The profile picture changed. The token had been trading for seven days. The money trail led much further than one Solana chart.*

On **July 21, 2024**, Elon Musk adopted a red-and-blue laser-eye “Dark MAGA” image on X. The Solana token **$DMAGA** had launched on **July 14**. Some of its earliest buyers were holding substantial positions long before Musk's profile changed.

This investigation reconstructs their **trades, token transfers, early funding, exchange deposits and cross-chain orders**. It follows specific transactions rather than treating screenshots, influencer claims or shared service accounts as evidence of common ownership.

**[Trading data](reports/TOP_TRADERS.md) · [Wallet network](reports/COORDINATION.md) · [Cross-chain evidence](investigations/2026-11-05_evm-recipient-deeptrace/FINDINGS.md) · [Historical X archive](docs/historical/pass2/README.md)**

---

## 1. Two buys. Forty-eight sales. Nearly $1 million in reconstructed trading profit.

The wallet:

`H3QsBrrivimFJmSpTXuvig2n1Bh7JuYxrriRSEszT6cc`

made its first recorded $DMAGA purchase on **July 14, 2024, at 16:43:58 UTC**, seven days before the profile change.

| Reconstructed activity | Result |
|---|---:|
| Purchase cost, at historical USD prices | **$1,086.77** |
| Number of purchases / sales | **2 / 48** |
| Realized trading PnL | **5,490.86 SOL** |
| Realized trading PnL, USD conversion | **$990,743.77** |
| Last recorded sale | **July 23, 2024** |

These amounts are **reconstructed realized trading PnL**, based on the observed swaps and contemporaneous SOL/USD prices. They are not the portfolio's peak paper value, an exchange cash-out, or an after-fees-and-taxes bank profit.

This wallet is **not** assigned to the creator or to the 33-wallet component below. The financial result is established at the wallet level; its owner and what that owner knew are not.

[Reconstructed rankings and accounting definitions](reports/TOP_TRADERS.md) · [Claim-by-claim numerical review](docs/README_REVIEW_2026-11-05.md)

## 2. A second launch-day money trail: 7GVC → 9Sxm

A separate, **transaction-receipt-backed replay** traces another set of early $DMAGA accounts. Its calculations are currently undergoing financial review in [PR #25](https://github.com/searadacunha/Dark-MAGA/pull/25).

On **July 14, 2024**, `7GVCZAYG5NfiJsuqUdvc9hB2ts2W3tSrGdya4CyR1M5j` received **189.656069 SOL** as its own Jupiter Perpetuals position was closed, 33 minutes before the token's creation.

The same wallet then bought approximately **41.197 million $DMAGA for 7.903 SOL** and made a **direct transfer of 20 million $DMAGA** to `9Sxmf25WG5WVQ5p86ycWeo5hMEwxiWPkFtLdRdTrHSQS`.

That replay also identifies **three distinct SOL funding paths** from 7GVC:

| Recipient | Recorded SOL from 7GVC | Subsequent recorded $DMAGA purchases |
|---|---:|---:|
| `A1UDMqcUC8RkZ8YENAktdueSQ6jxUUBickBK2y61vQ8J` | **5 SOL** | 12.08 million |
| `6QFDe4yu9mVhv3cbbaMtkTnakz4bGJLAjLjhwrMn5jqD` | **60 SOL, in two transfers** | 15.39 million |
| `H4mQu98TuxYTn3VSJone6jCTiDfXpuKcZbNZGHKUJU5y` | **16 SOL** | 3.77 million |

Direct transfers, early trading and repeated interactions are stronger evidence of **financial relationships** than shared infrastructure or social posts. They do not identify a single human owner or show that anyone knew what Musk would do. These precise replay figures are documented with signatures, receipts and offline tests in the open PR, and are **not yet part of the finalized main-branch numerical analyses**.

[Receipt-based historical replay — PR #25](https://github.com/searadacunha/Dark-MAGA/pull/25) · [Third-pass primary-source leads](docs/historical/pass3/README.md)

## 3. Thirty-three wallets. Forty direct token transfers.

A second investigation identified **33 wallets linked by 40 direct transfers of at least one million $DMAGA each**. These are actual token movements, not coincidences created by a shared exchange, router or DEX.

**Fifteen** of these wallets bought during the token's **first hour**.

Before Musk's avatar change, their aggregate holdings had an estimated **upper bound of 217 million DMAGA**, about **23% of the supply outside liquidity pools** at that reference point.

In the following 24 hours, the component's recorded swaps produced approximately **4,525 SOL in sale proceeds**, or **2.4%** of the market-wide recorded SOL sale proceeds over that window.

The creator is **outside** this transfer-defined 33-wallet component. Its transactions establish a connected network; they do not establish one beneficial owner.

[Direct-transfer component, signatures and thresholds](reports/COORDINATION.md) · [Case evidence](docs/CASE_REPORT.md)

## 4. Follow the funding, then the exits.

The creator's funding and deposit investigation reveals another financial structure.

On **July 14, between 01:32:23 and 01:40:50 UTC**, **14 wallets**, including the future creator, received their first recorded funding through Coinbase hot wallets. The mint was created at **02:05:25 UTC**.

Their later movements converge on two identified deposit accounts:

- `9W9b3zgHH9mCEHDhsdbnbEPHStm9vvXS4aia4DWHBxpL`
- `Caw4RrwkmxqtbLSFzgSs6id3XiFxWQxs2t1mrn5a3mME`

The historical account review identified **27 qualifying senders shared by both deposits**, representing roughly **71% of incoming value at each** under the specified matching rules.

This is more informative than merely observing that wallets use Coinbase: it combines **time-concentrated first funding and subsequent convergence to the same destinations**. Exchange accounts remain attribution boundaries; their customers are not identified.

[Funding and deposit evidence](docs/README_REVIEW_2026-11-05.md) · [Wallet-level investigation](docs/CASE_REPORT.md)

## 5. The trail crosses chains.

The bridge-order review decoded **76 deBridge orders** across the investigated populations, with **1,018,687.18 USDC committed on the source side** (including proportional bridge fees). **41** were matched to Ethereum execution, representing **942,534.32 USDC of source-side commitments**. These counts cover a broader investigated population, **not just the 33 wallets**; they are neither an aggregate $DMAGA profit nor a verified total of received funds.

One especially direct path stands out:

> **Three Solana wallets → four deBridge orders → one Ethereum destination, within nine minutes and 36 seconds.**

On **July 22**, the four source orders committed **263,573.15 USDC** to the same Ethereum recipient:

`0xb947bf7f409e998b28f8e218802fc9575c3c8c57`

All four destination executions were matched. Subsequent investigations trace this destination's movements through Ethereum, Base, BSC and back toward Solana, using decoded orders and transaction-level checks. Shared destination and demonstrable transfers are not, by themselves, proof of one human operator.

[Bridge-order reconciliation](docs/README_REVIEW_2026-11-05.md) · [Ethereum recipient deep trace](investigations/2026-11-05_evm-recipient-deeptrace/FINDINGS.md) · [Audited Base / BSC / Solana trace](investigations/2026-11-06_debridge_base_bsc_solana/FINDINGS.md)

## 6. Reconstructing the moment the market reacted.

The timing is central, but the exact moment Musk clicked “save” is not observable in the evidence.

An archived view of his profile at **19:03:27 UTC on July 21** still shows the old avatar. The historical X archive includes a post by **@realjohnnewburg at 19:25:23 UTC** containing a screenshot of the changed profile, earlier than the previously catalogued screenshots. That post gives a **documentary upper bound**, subject to authenticating the image and its provenance—not an exact click timestamp.

The investigation also preserves early public appearances of the artwork, repost/original relationships, dated analyst observations and the subsequent removal of the avatar as a **separate event**.

[Original social chronology](docs/SOCIAL_FINDINGS.md) · [Historical sources and provenance](docs/historical/DMAGA_HISTORICAL_INTELLIGENCE_2026-11-06.md) · [Second-pass X findings](docs/historical/pass2/DMAGA_X_NEW_FINDINGS.md)

## Read the evidence

| Evidence collection | What it documents |
|---|---|
| [Trading reconstruction](reports/TOP_TRADERS.md) | Wallet-level purchases, sales, realized PnL and accounting scope |
| [Direct transfers and network tests](reports/COORDINATION.md) | Transfer-defined components, funding and statistical controls |
| [Creator and early-wallet case report](docs/CASE_REPORT.md) | Launch transactions and chronological wallet evidence |
| [EVM deep trace](investigations/2026-11-05_evm-recipient-deeptrace/FINDINGS.md) | Source-to-destination order matching and traced receipts |
| [Multichain forensic audit](investigations/2026-11-06_debridge_base_bsc_solana/FINDINGS.md) | Audited order IDs, Base/BSC flows and bounds |
| [DMAGA × Kekius investigation](investigations/2026-11-06_dmaga_kekius_cross_token/FINDINGS.md) | Separate cross-token comparison with transaction-level tests |
| [Historical X evidence, passes 1–3](docs/historical/pass3/README.md) | Archival source reconstruction, 316 additional X posts and wallet test leads |
| [Current investigation status](docs/RESEARCH_STATUS_2026-11-06.md) | What is demonstrated, what is under review, and the next decisive financial tests |\n| [Statistical control study](etude_final/results.md) | Comparison against 211 tokens, with its stated testing scope |
| [Reproduction guide](docs/REPRODUCTION.md) | Data availability, validation requirements and research versions |

**Scope:** Solana token `7D7BRcBYepfi77vxySapmeqRNN1wsBBxnFPJGbH5pump`. This is an evidence-led inquiry into early trading and financial flows, **not a claim that Elon Musk knowingly coordinated trades or that a named person controls the linked wallets**. Historical X testimony and unverified wallet leads are kept separately from confirmed chain transactions.
