# Launch-network and public-attribution addendum — 18 November 2026

**Scope:** Solana $DMAGA (`7D7BRcBYepfi77vxySapmeqRNN1wsBBxnFPJGbH5pump`), the 14 July 2024 launch and the July 21 Musk-avatar narrative. Times are UTC.

This is a **source-preserving integration of a user-supplied forensic report**, not a fresh collection of 2024 Solana or X data. The `.txt` uploaded in the preceding conversation and the `.md` uploaded subsequently were compared and have **identical text**; one canonical copy is retained as [SOURCE_REPORT.md](SOURCE_REPORT.md). The submitted report states it used X API v2, Wayback, Solana RPC and IPFS. Its referenced `raw/x*.json`, `raw/rpc*.json`, media snapshots, `assertions.json`, `assertions.csv` and query log **were not among the supplied files and are not represented here as committed evidence**. A cited signature, X snowflake or link is a lookup key, not independent replication of the underlying record.

## What this adds

| Finding from supplied report | Report-level assessment | Reconciliation with the existing repository |
|---|---|---|
| Mint metadata and @DarkMagaCoin profile use the same described image and wording; profile-image snowflake predates mint | **B for technical association**, not civil attribution | New technical association with the creator-signed metadata. The stated zero perceptual-hash distances do **not by themselves prove pixel-by-pixel identity**; original image bytes or a decoded-pixel comparison are needed |
| G41v attempted pump.fun buys at **02:05:54** and **02:06:10 UTC**, 29s/45s after the 02:05:25 mint; both failed, reportedly with error 6002 | **A in source for transaction results**, pending independent receipt retrieval in this import | Adds two failed transactions to existing coverage of the 13 × 0.5 SOL early fundings, 5 SOL to GFpqfj and later Jupiter trade; *attempts are not successful purchases or proof of advance knowledge* |
| @DarkMagaCoin's deleted `1812312706826854843` post was dated **02:26:35 UTC** and reportedly showed the mint | **A in source for archived post**; its X-ID timestamp was independently decoded offline | Corrects the prior **03:00:28** as *earliest surviving post in the old pass-4 corpus*, not first-ever project post |
| @ChoupetteJoe's July 23 post thread lists **19** early buyer addresses: **10** in the existing 33-wallet component (including seven G41v-funded), **nine** elsewhere | **B as a contemporary third-party list**; classification not independently re-computed here | Nine *candidates*, not nine independently validated additional group members; their exact addresses require the thread/raw list to reconstruct |
| The phrase and ticker predate the Solana mint (May 26 ETH-related mention; June 1 post) | **A for identified post records; B for historical contextual claim** in supplied report | Indicates pre-existing public vocabulary. No proof of the same deployer or team |
| Statements about @kikisknees as “lead”, and a developer described by @Murray_Gothbard | **A only for existence of reported statements, C for their truth** | Public assertions are not documentary evidence of a role or ownership |
| No direct creator↔G41v transaction across the reported **972** creator and **416** G41v signatures | **A as negative search within submitted corpus, not a universal absence** | The reported direct-transfer null does not rule out intermediaries, services or missing history |

The report also documents public requests directed at Elon Musk ahead of the profile change. It **does not establish** a private message, advance knowledge of the avatar choice or a wallet belonging to a public X account. The existing study's negative result (**211 comparator tokens; best primary rank p ≈ 0.15566**) is **unchanged**. Do not infer an insider-trading offence or a trading edge from chronology or contact.

## Temporal correction to pass 4

The [pass-4 list](../../docs/historical/pass4/PUBLIC_X_ACTIVITY.md) is intentionally left intact as a historical record of *that pass's retrieved corpus*. Its `03:00:28` row for @DarkMagaCoin is superseded for the **first observed project post** by the new report's `02:26:35` Wayback finding. @adamjia7 at `02:33:53` remains the earliest bot-style mention **in the pass-4 sample**, not the earliest public DMAGA post in all sources.

X snowflake decoding (`(id >> 22) + 1288834974657`) corroborates *creation timestamps encoded in IDs*, not deleted post text, tweet availability, retweet semantics, account control, image provenance or post authenticity. A small [offline regression test](../../tests/test_launch_network_snowflakes.py) checks the listed ID/timestamp pairs.

## Required evidence gates before upgrading claims

1. Retrieve and hash the actual IPFS image and dated X media; perform decoded-pixel comparison, and search for a publicly available common source before 14 July **01:49 UTC**.
2. Fetch both failed Solana transaction receipts; confirm signer, error code, program and context, and measure sniper-delay base rates across other contemporaneous pump.fun launches.
3. Retrieve the archived deleted post, verify capture provenance and preserve the complete Wayback URL and response artifact rather than only a snowflake.
4. Retrieve the full @ChoupetteJoe thread, materialize all 19 addresses, rebuild the 10/9 intersection against the original 33-wallet address universe, then examine funds/outflows at the transaction level without hub-induced false joins.
5. Re-run the creator↔G41v comparison on preserved, timestamped complete histories, then test two-hop paths while filtering Coinbase, Jupiter, routers, bridges and deposit infrastructure.
6. Preserve any further statements by @kikisknees, @ChrisWinig, @Murray_Gothbard or @kanpai as **claims about their own contents only** until supported by independent records.

**Do not** edit `etude_final/` or generated legacy reports to reconcile these historical-source updates. The previous `03:00:28` pass-4 observation remains accurate *for its own search pass*, and this addendum supplies the broader discovery. Full raw-data reproduction cannot be claimed from these files.

## Reviewer navigation

- [Full supplied source report](SOURCE_REPORT.md) — original language, timeline, relationship graph, X/transaction reference keys, alternatives and open questions.
- [Machine-readable source claims](CLAIM_REGISTER.csv) — limited extraction; source grades vs. verification performed during this integration.
- [Public evidence index](../../docs/EVIDENCE_INDEX_2026-11-18.md) — cross-links new source claims to the original case.
- [Final case brief](../../docs/FINAL_CASE_BRIEF_2026-11-18.md) — concise presentation; frozen statistical and accounting conclusions unchanged.
- [Original on-chain coordination](../../reports/COORDINATION.md) and [historical pass 4](../../docs/historical/pass4/PUBLIC_X_ACTIVITY.md) — unchanged source records.

**Authorship/provenance:** incorporated at the repository owner's request on 18 November 2026 from two identical supplied report files. The original report's claim grades are not silently promoted to independently reproduced facts by this publication.
