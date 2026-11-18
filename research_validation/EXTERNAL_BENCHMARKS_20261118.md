# External Solana memecoin research catalogue — 18 November 2026

Scope: **attributed external literature and datasets**. This catalogue does not independently reproduce the authors' results. No literature claim here is evidence of a profitable public trading signal.

## Candidate data and methods

| Source | Availability | Principal use and limitation |
|---|---|---|
| [RED-PUMP-2026-v1](https://zenodo.org/records/20633603), May–June 2026 | Public downloadable archive, ~91.6 MB incl. scripts and checksums | 860,213 launches, 832,941 with terminal 24-h outcome, 1,651 graduations (0.198% of resolved). Strong token-level baseline, **no funding histories in described schema** |
| [loopholetape pumpfun-launches](https://huggingface.co/datasets/loopholetape/pumpfun-launches/blob/main/README.md), Aug–Nov 2026 | Public dataset; segregate legacy vs corrected decoder | 2,713,057 observed launches. Before 27 Sep 2026 ~48% of buy rows and 32% of curve SOL missing. Early-feature coverage selective (81.6%). Outcome "rugged" is a heuristic, not confirmed fraud |
| [Slinky21 Pumpfun Memecoin Corpus](https://huggingface.co/datasets/Slinky21/Pumpfun_Memecoin_Corpus), Jun–Jul 2026 | Public files; resolve license discrepancy first | Six linked token/trade/wallet/migration tables. Metadata states MIT; card prose states CC-BY-4.0; third-party holder inputs require provenance check |
| [ian05012 solana-memecoin-dataset](https://github.com/ian05012/solana-memecoin-dataset), June 2026 | Public GitHub files | About 44k snapshots and 9.5m trades; selected **freshly graduated / trending** tokens, not a population denominator. Forward peak labels unsuitable as executable exit quotes |
| [Gafarov, Early-Buyer Groups and Fast-Wallet Teams](https://arxiv.org/abs/2610.39458), Oct 29 2026 | Open research article, raw dataset replay not done | 200,443 launches, 15.85m trades, 51m transfers and 23,710 candidate groups. Observable group structure; no reliable profitable follower edge after execution controls in the reported experiment |
| [RED-COHORT-2026](https://zenodo.org/records/21765387), v1.1.1 | **Restricted files** though public metadata | Describes 1,012 recurring cohorts; no reproduction allowed to be claimed without data access |
| [Pine Analytics, Exit Liquidity Machines](https://pineanalytics.substack.com/p/exit-liquidity-machines), Apr 21 2025 | Public methodology, linked Flipside analyses | Strict direct deployer–sniper funding links, with documented 5–7-hop misses. Operator realized returns are not a follower's returns |
| [Catching the Rug](https://arxiv.org/abs/2608.20271), 2026 | Open abstract, underlying data/code not audited here | 6.4m token rug-pull research; distinguishing unsafe tokens from positive trading alpha is essential |

## Program and trade-cost era controls

- [Pump.fun fees, updated 16 Nov 2026](https://pump.fun/docs/fees): identify fee era, launch curve, protocol, migration, pair asset and all fees before modeling an entry. Never apply 2026 fees to 2024 prices.
- [Pump.fun curve mechanics](https://pump.fun/docs/bonding-curve): distinguish curve trades, migration and post-migration trades by token and date.
- [Jito documentation](https://docs.jito.wtf/bundles/): bundles are atomic sets of up to five transactions; tips and priority fees affect competitive inclusion. Same-slot buys by themselves do not prove a private Jito bundle.

## Four prioritized, falsifiable exercises

1. **Control repair**: The historical 88.86% pooled-wallet null samples 40 wallets from only nine launches; it may retain same-launch funder relations. Build at least 40 launch-independent controls matched on timestamp, history completeness and liquidity, and freeze the null before testing any threshold.
2. **2024 raw chain reconciliation**: Rebuild h2w6gm6jz mint FNqJtYs7rsP1H9GXWTtc5VnDoL2GhXEUKhYN46EEpump from original signatures, integer lamports, slots, prior token creation, and first buys; reconcile nine-wallet vs distinct 40-wallet collection, without declaring either complete.
3. **2026 denominator and regimes**: Import RED-PUMP and loopholetape only after checksum, licensing and missingness checks. Separate launch survival, graduation, subsequent 2x and **liquidatable** net exits. Different source base rates cannot be pooled across eras without matched eligibility.
4. **Prospective recurrent-funder OOS**: Establish wallet groups from earlier funding and exit cycles only. At the next launch, compare point-in-time recurrence against price-only, curve SOL, initial buy, creator history, volume and liquidity. Hold out entire operator groups and later dates; simulate delayed entries, failed transactions, fees and actual sellability for pre-registered small capital sizes.

## Reproducibility and publication status

The cited source metadata and methods were inspected, but none of these **external datasets** was downloaded or re-run in this investigation. No new economic edge is claimed. The protected existing README, frozen snapshots and negative-result artifacts must remain intact. Do not publish material whose redistribution terms are unresolved.
