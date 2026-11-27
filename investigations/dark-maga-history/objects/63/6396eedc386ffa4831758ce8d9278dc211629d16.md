# Dark MAGA: Did Musk Know?

*One profile picture. Seven days of trading before it changed. A money trail spanning thousands of transactions, dozens of wallets and multiple blockchains.*

On **July 21, 2024**, Elon Musk appeared on X with a red-and-blue laser-eye “Dark MAGA” profile picture. The Solana token **$DMAGA** had been launched on **July 14**.

By the time the new avatar was documented, early wallets had bought millions of tokens, transferred supply between addresses and established funding relationships. When the image spread, the market reacted.

**What happened before the profile change? Who held the tokens? Where did the money go?**

This repository follows the transactions — from the first Solana buys to later exchange deposits and cross-chain executions. Each major figure links to the underlying receipts, ledgers or reconstruction.

**[Trading profits](reports/TOP_TRADERS.md) · [Wallet connections](reports/COORDINATION.md) · [Cross-chain tracing](investigations/2026-11-06_debridge_base_bsc_solana/FINDINGS.md) · [Early X accounts](docs/historical/pass4/PUBLIC_X_ACTIVITY.md) · [Evidence archive](docs/REPRODUCTION.md)**

---

## 1. Two buys. Forty-eight sales. Nearly $1 million in realized trading profit.

One of the earliest documented large winners was:

`H3QsBrrivimFJmSpTXuvig2n1Bh7JuYxrriRSEszT6cc`

Its first recorded $DMAGA purchase was on **July 14 at 16:43:58 UTC** — a full week before Musk's profile change.

| Reconstructed wallet activity | Result |
|---|---:|
| Historical purchase cost | **$1,086.77** |
| Purchases / sales | **2 / 48** |
| Realized trading PnL | **5,490.86 SOL** |
| Realized trading PnL, historical USD conversion | **$990,743.77** |
| Last recorded sale | **July 23, 2024** |

The result comes from recorded trades and historical prices, not a screenshot of a peak portfolio value. This is **wallet-level realized trading PnL**, not a verified bank withdrawal.

[Full trade ledger and rankings](reports/TOP_TRADERS.md) · [Independent numerical review](docs/README_REVIEW_2026-11-05.md)

## 2. 189.656 SOL returned. 41.2 million tokens bought. 20 million transferred.

Another trail begins **33 minutes before $DMAGA was minted**.

On **July 14 at 01:32:11 UTC**, wallet `7GVCZAYG5NfiJsuqUdvc9hB2ts2W3tSrGdya4CyR1M5j` received **189.656069 SOL** following the closure of **its own Jupiter Perpetuals position**.

That wallet subsequently bought **41,197,138 $DMAGA for 7.903074 SOL**, and directly transferred **20 million tokens** to:

`9Sxmf25WG5WVQ5p86ycWeo5hMEwxiWPkFtLdRdTrHSQS`

The transaction replay also tracks three funding paths from 7GVC into other early buyers:

| Funded wallet | Direct funding from 7GVC | Subsequent documented DMAGA buys |
|---|---:|---:|
| `A1UDMqcU…` | **5 SOL** | **12.08M tokens** |
| `6QFDe4yu…` | **60 SOL** (two transfers) | **15.39M tokens** |
| `H4mQu98T…` | **16 SOL** | **3.77M tokens** |

The connections extend to **pre-existing, two-way transfers** involving 7GVC, 9Sxm and other related addresses. The receipts establish the money movements and their chronology.

[Transaction-by-transaction replay](investigations/2026-11-06_historical_replay/FINDINGS.md) · [Reproducible receipt tests](investigations/2026-11-06_historical_replay/README.md)

## 3. Thirty-three wallets. Forty direct transfers. 217 million DMAGA.

A separate transfer-defined network contains **33 wallets connected by 40 direct $DMAGA transfers**, each of at least one million tokens.

**Fifteen wallets in this component bought during the token's first hour.**

Before the documented Musk avatar change, those addresses collectively held an estimated **upper bound of 217.037 million $DMAGA** — approximately **23% of supply outside liquidity pools** at that reference point.

In the first 24 hours following the event, their recorded swaps generated **4,524.914 SOL in sale proceeds**, about **2.38% of market-wide recorded SOL sale proceeds** during that period.

| Measured feature | Recorded result |
|---|---:|
| Wallets in the connected component | **33** |
| Direct token-transfer links | **40** |
| Early buyers, first hour | **15** |
| Pre-event holdings, upper bound | **217.037M DMAGA** |
| 24-hour swap sale proceeds | **4,524.914 SOL** |
| Reconstructed realized trading PnL for the component | **5,472 SOL** |

This is a **network defined by on-chain transfers**; the graph measures relationships between addresses rather than a headcount of people.

[Network evidence](reports/COORDINATION.md) · [Rebuilt component figures](docs/REBUILD_2026-11-07.md) · [Wallet-level case report](docs/CASE_REPORT.md)

## 4. Fourteen early funding arrivals. Twenty-seven shared deposit senders.

The creator's wallet is part of another traceable funding story.

On **July 14, between 01:32:23 and 01:40:50 UTC**, **14 wallets**, including the future token creator, received their first recorded funding through Coinbase hot wallets. The $DMAGA mint was created at **02:05:25 UTC**.

A subsequent examination of exchange-bound flows identified two addresses receiving funds from overlapping senders:

- `9W9b3zgHH9mCEHDhsdbnbEPHStm9vvXS4aia4DWHBxpL`
- `Caw4RrwkmxqtbLSFzgSs6id3XiFxWQxs2t1mrn5a3mME`

Under the documented matching rules, **27 qualifying senders** appear at **both destinations**. These account for roughly **71% of the incoming value at each address**.

The evidence is a sequence of dated fundings, transfers and deposit convergence. Coinbase is the observed funding infrastructure; attribution of exchange customers is a separate question.

[Funding and deposit review](docs/README_REVIEW_2026-11-05.md) · [Creator case file](docs/CASE_REPORT.md)

## 5. Three Solana wallets. Four bridge orders. One Ethereum destination.

The investigation does not stop at Solana.

On **July 22, 2024**, **three Solana wallets** originated **four deBridge orders** to one Ethereum recipient, within **nine minutes and 36 seconds**.

Those four source orders committed a combined **263,573.15 USDC**:

`0xb947bf7f409e998b28f8e218802fc9575c3c8c57`

**All four destination executions were matched.**

Across the wider investigated populations, the bridge-order review reconstructed **76 deBridge orders** carrying **1,018,687.18 USDC in source-side commitments** (including proportional bridge fees). **41 orders**, representing **942,534.32 USDC in source-side commitments**, were matched to Ethereum execution.

Follow-on audit work traces identified transactions across **Ethereum, Base, BSC and back toward Solana**, including subsequent swaps and exchange-facing destinations.

These are **bridge amounts and observable transaction paths**. They are not a claim that every USDC originated from $DMAGA trading or that every destination belonged to one person.

[Original cross-chain reconciliation](docs/README_REVIEW_2026-11-05.md) · [Ethereum deep trace](investigations/2026-11-05_evm-recipient-deeptrace/FINDINGS.md) · [Audited multichain reconstruction](investigations/2026-11-06_debridge_base_bsc_solana/FINDINGS.md)

## 6. The public trail was already visible on July 14.

The X archive records DMAGA-related posts beginning on the morning the token launched.

| Earliest post found in the searched archive (UTC) | Public account | Observed activity |
|---|---|---|
| **July 14, 02:33:53** | [@adamjia7](https://x.com/adamjia7/status/1812314544204882062) | Posted the official mint |
| **July 14, 02:41:55** | [@Murray_Gothbard](https://x.com/Murray_Gothbard/status/1812316567150985272) | Early ticker mention |
| **July 14, 02:48:08** | [@CryptoOnlyCoims](https://x.com/CryptoOnlyCoims/status/1812318131890594282) | Shared the ticker and mint |
| **July 14, 03:00:28** | [@DarkMagaCoin](https://x.com/DarkMagaCoin/status/1812321235688157500) | Project-account publication |
| **July 14, 13:39:32** | [@CristusVictor](https://x.com/CristusVictor/status/1812482060818186492) | Circulated the official mint |
| **July 14, 14:18:14** | [@kanpai](https://x.com/kanpai/status/1812491802844471629) | Public promotion |
| **July 17, 21:49:02** | [@ChrisWinig](https://x.com/ChrisWinig/status/1813692412025274712) | Public visual relay |

The historical pass-4 archive includes **23 source-linked public accounts**, their earliest posts found in the searched windows and the specific activity documented. “Earliest found” refers to the preserved search material, not a guaranteed first-ever post.

These are **public X publications**, separate from the wallet evidence. No financial identity is inferred from a handle.

[All 23 public accounts and source links](docs/historical/pass4/PUBLIC_X_ACTIVITY.md) · [Social-source research](docs/SOCIAL_FINDINGS.md) · [Historical passes 1–3](docs/historical/pass3/README.md)

## 7. The 21 minutes and 56 seconds that frame the market's reaction.

The profile chronology has two documentary anchors on **July 21, 2024**:

- **19:03:27 UTC:** an archived profile view still displays Musk's earlier avatar.
- **19:25:23 UTC:** [@realjohnnewburg](https://x.com/realjohnnewburg/status/1815105812076904904) posts a screenshot showing the new laser-eye avatar. [@AutismCapital](https://x.com/AutismCapital/status/1815106321810919673) follows at **19:27:24 UTC**.

The documented observation interval is **21 minutes and 56 seconds**. These timestamps concern the surviving records, rather than the exact moment a profile-setting change was made.

In the reconstructed trading data:

| Market window | Recorded DMAGA purchases |
|---|---:|
| Uncertain avatar-change interval | **20.85 SOL** |
| First hour following the documentary upper bound | **5,347.29 SOL** |

The source archive includes earlier public versions of the artwork, posts aimed at prominent accounts, repost provenance and a transaction-level replay around the event.

[Timestamped timeline](docs/TIMELINE.md) · [Historical replay](investigations/2026-11-06_historical_replay/FINDINGS.md) · [Event-dependent report](reports/EARLY_BUYERS.md)

---

## Follow the evidence

| Start here | What you can examine |
|---|---|
| [Trading profits](reports/TOP_TRADERS.md) | Purchases, sales, realized PnL and accounting definitions |
| [Financial network](reports/COORDINATION.md) | Direct transfers, wallet components and funding relationships |
| [Historical replay](investigations/2026-11-06_historical_replay/FINDINGS.md) | Signed transactions, early-wallet paths and independent receipt tests |
| [Cross-chain audit](investigations/2026-11-06_debridge_base_bsc_solana/FINDINGS.md) | Matched orders and transaction paths on Ethereum, Base, BSC and Solana |
| [Public X participants](docs/historical/pass4/PUBLIC_X_ACTIVITY.md) | Dated posts and named public accounts from the early DMAGA conversation |
| [Rebuilt datasets](docs/REBUILD_2026-11-07.md) | Deduplicated trade reconstruction, PnL and changes to event windows |
| [Statistical controls](etude_final/results.md) | The separate frozen comparison study against 211 tokens |
| [Reproduce the investigation](docs/REPRODUCTION.md) | Datasets, source boundaries, scripts and test instructions |

**Research scope:** $DMAGA on Solana, mint `7D7BRcBYepfi77vxySapmeqRNN1wsBBxnFPJGbH5pump`. All times are UTC. Wallets, exchange services and public X accounts are distinct evidence categories. Trading PnL, token holdings, bridge commitments and exchange-facing transfers use different accounting definitions. This repository records their observable histories and the limits of what each record establishes.
