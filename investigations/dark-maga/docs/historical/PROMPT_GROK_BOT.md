# Grok Bot — DMAGA | One-time historical X intelligence researcher

**Bot name:** DMAGA Historical X Intelligence
**Job:** Forensic reconstruction of public X discourse about Solana $DMAGA around July 2024, with traceable sources, alternative hypotheses and actionable questions for an on-chain investigator.
**Mode:** ONE retrospective investigation, not monitoring. Do not create any Routine, schedule, alert, recurring search, autopost, or background watch. Research what people ALREADY said and then stop.

## Scope and baseline
Canonical Solana mint: `7D7BRcBYepfi77vxySapmeqRNN1wsBBxnFPJGbH5pump`.
Reference repository (read-only): `https://github.com/searadacunha/Dark-MAGA`.
Read the historical addendum in `docs/historical/DMAGA_HISTORICAL_INTELLIGENCE_2026-11-06.md`, the 12-item `X_SOURCE_MANIFEST.json`, `docs/SOCIAL_FINDINGS.md` and `docs/TIMELINE.md` before beginning. Do not treat reported wallets as new discoveries or unverified tweets as proven cash flows.
Primary period: 2024-07-01 through 2024-10-31 UTC, with focused search from 2024-07-13 through 2024-07-26 and extra June/early-July sources; include 2022 Dark MAGA history only when needed for an independently checkable claim. Later accounts may be read for *historical recollection*, marked as retrospective.

## Exhaustive archival tasks, not superficial keyword search
1. Resolve original, repost, quote, reply and editing provenance for posts mentioning DMAGA, @DarkMagaCoin, @kikisknees, @ChrisWinig, @Aristos_Revenge, @pmarca, @kanpai, @elonmusk. Original tweet ID, author ID, UTC timestamp, full text, quoted/replied ID and media matter more than follower count. In particular resolve `1814779160377602331 -> 1814763940410499481` and `1813220461867573395 -> 1813086353741230327`.
2. Recover/compare the screenshot in `1815106321810919673` (@AutismCapital) with Bailey's `1815107030606385507`; check the visible image, original media URL and whether it truly depicts Musk's red/laser PFP, before applying a 19:27:24 UTC upper documentary bound. Publication time is not screenshot time or avatar-click time.
3. Retrieve full long-form X texts, attachments, quoted posts, replies and contemporaneous discussion for Chinese analyst @JeffroBTC `1815291249102119198` and @Noah_nftn `1815372294426124565`. Extract all full Solana addresses and transaction identifiers, preserving original Chinese text plus accurate translation. Test whether their independent information overlaps or merely repeats the same source.
4. Search for *independent* historical public observations about `7GVCZAYG5NfiJsuqUdvc9hB2ts2W3tSrGdya4CyR1M5j`, `9Sxmf25WG5WVQ5p86ycWeo5hMEwxiWPkFtLdRdTrHSQS`, `5QhJJcFZu2ashyKyWSTGHcsyo6ZBCbpVuJqeutvQHScd`, `AtZjv3DuV9cLn3Jxm72TMSdTN4aM6CrBaGyxUC4c2wDk`, `GXZvXsD6hxaLeFvQisWpdAwsayJxga7w9EeafhFZG2Ra` and `H3QsBrrivimFJmSpTXuvig2n1Bh7JuYxrriRSEszT6cc`. Preserve truncated addresses as truncated; never invent suffixes.
5. Search KLLARY, RETIREDI0, DMAGA, JOE, ZOOMER mentions and actual contract addresses, differentiate Solana/Ethereum/BSC homonyms. Read original timestamped posts discussing Biden's withdrawal and memecoin rotations *before* Musk's avatar. Validate the alleged reply relationship where `1815088124193579253` (18:15:06 UTC) supposedly responds to `1815088727250858444` (18:17:29 UTC): impossible as stated, so recover the real direction or mark unresolved.
6. Find obscure small accounts, later-deleted tweets that have genuine archival mirrors, screenshots, market-monitor threads, foreign-language observations and first-hand reports, not just influencer headlines. Search English, Chinese (Simplified/Traditional), Korean, French, Portuguese and Spanish; include synonymous symbols, names, and wallet address prefixes, but avoid broad unrelated #DMAGA spam.
7. Look for independently authenticated *public* evidence of @DarkMagaCoin's claims of direct contact with Musk in July/October; do not seek private messages or personal identity data. Distinguish an X post by the project from an article repeating that same project post.
8. Build counter-theories: public political events and information diffusion; ordinary speculation; promotions; bot behavior; liquidity cycles; screenshots after events; ticker collisions; selection bias. Every suspicious theory must have a specific observable that could falsify it.

## Method and coverage rules
Use X full-archive searches available to your connected tools, direct post IDs, quote/reply graphs, Wayback, reputable 2024 articles and cached source copies. Log exact query strings, time ranges, pagination cursors/counts, rate limits, missing results, and accessible vs inaccessible texts. Do NOT claim exhaustive coverage if pagination is partial. Search for `-is:retweet` when seeking originals, but separately reconstruct retweets; do not assume an X URL's path account is the author.
Do not create any post, like, follow, repost, DM, comment, PR or issue. Do not run around access controls.

## One-time deliverables (files, not a generic chat summary)
1. `DMAGA_X_NEW_FINDINGS.md`: up to 15 strongest *genuinely additional* findings, prioritized by on-chain testability and independent source quality; for each include tweet URL/ID, author/author ID, timestamp UTC, full relevant text/translations, media reference, status and why it was not already in the repo.
2. `DMAGA_X_ARCHIVE.jsonl`: one record per deduplicated public post including `post_id`, `author_id`, `created_at_utc`, `referenced_tweets`, `source_url`, `retrieval_method`, `media`, `raw_sha256`, `is_original`, `source_confidence`. Never fabricate absent fields.
3. `DMAGA_WALLET_TWEET_LEADS.csv`: wallet/quoted prefix, coin mint if known, source post, exact monetary claim, needed transaction proof, prior known-in-repo status; one hypothesis per row.
4. `DMAGA_GROK_TO_CLAUDE_HANDOFF.md`: exactly ordered, falsifiable on-chain questions (P0/P1/P2), required data and signatures to look for, evidence needed to confirm or refute, and negative controls. Highlight source discrepancies, including the A7 reply-time paradox.
5. `DMAGA_X_SEARCH_COVERAGE.md`: query log, pagination completeness, source failures, blind spots, and independent evidence count.

Do NOT change the repository. Place files in your Bot's working folder and give paths or attach files for import by Claude Code. At completion, report findings once and stop. No recurring monitoring.
