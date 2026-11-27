# Grok historical pass 3 — imported source package (6 November 2026)

The user-supplied `DMAGA_PASS3.txt` contained **seven concatenated documentary deliverables**. This directory preserves the six small deliverables; the seventh, `DMAGA_PASS3_DELTA.jsonl`, is stored in four contiguous, ordered chunks under `../../../data/historical_x_pass3/`.

| Deliverable | Content |
|---|---|
| [DMAGA_PASS3_FINDINGS.md](DMAGA_PASS3_FINDINGS.md) | Seven documentary findings, P3-01–P3-07 |
| [DMAGA_PASS3_CLAUDE_HANDOFF.md](DMAGA_PASS3_CLAUDE_HANDOFF.md) | Eight falsifiable on-chain or documentary investigations |
| [DMAGA_PASS3_WALLET_LEADS.csv](DMAGA_PASS3_WALLET_LEADS.csv) | Nine candidate wallet/asset rows, no new on-chain signatures |
| [DMAGA_PASS3_MEDIA.csv](DMAGA_PASS3_MEDIA.csv) | 19 source media entries plus five derived video frames, with reported original file hashes |
| [DMAGA_PASS3_SOURCE_GRAPH.csv](DMAGA_PASS3_SOURCE_GRAPH.csv) | Documented X post relationships; derived edges explicitly marked as documentary |
| [DMAGA_PASS3_SEARCH_COVERAGE.md](DMAGA_PASS3_SEARCH_COVERAGE.md) | Search methodology, 88 X calls, provenance and limitations |
| [X delta JSONL](../../../data/historical_x_pass3/) | 316 unique previously unarchived post IDs, in four ordered parts (79 records each) |

**Import checks performed:** every one of the 316 posts parses as JSON, has a unique ID, an author ID and an UTC timestamp agreeing within ~1 second with its ID's Snowflake timestamp. The archive contains **148 distinct author IDs**. These consistency checks do **not** independently authenticate X API responses or financial claims.

**What is not included:** the original Grok ZIP, raw X query-response files from `/workspace/dmaga_pass3_work/`, the 19 media binaries, the MP4, and the five extracted frames. The uploaded file was text-only; media URLs, file names and hashes in the CSV are *reported* by the source, not independently rehashed during this import. The concatenated text was split into separate files, so the original Grok manifest hashes cannot be presumed to apply to the reconstructed files.

## New evidence to prioritize against the on-chain replay

1. **P3-02 / 9Sxm.** A screenshot attached to @JeffroBTC's already archived post appears to show **1.8M DMAGA → 17.875 SOL on 15 July at 09:59 interface time**. This is a **transaction search fingerprint**, not an identified transaction. The screen's timezone is unknown, and four neighboring sales belong to an unreadable wallet. Check against the 9Sxm ledger in [PR #25](https://github.com/searadacunha/Dark-MAGA/pull/25).
2. **P3-01 / 6QFD.** @VikingXBT's post dated **22 July 2024, 12:56:22 UTC**, shows the truncated account `6QFDe4…5jqD`, **15.3M DMAGA / 1.53%** in a contemporaneous panel, **7m55s before Noah's post**. The screenshot's time and slot cannot be asserted. Validate compatibility with the canonical 6QFD ATA history, already covered in PR #25.
3. **P3-03 / BARRON.** Multiple 21–22 July social accounts explicitly mentioned a shared BARRON/DMAGA team; @ChrisWinig promoted BARRON in May. These are contemporaneous *social* signals only. Compare the verified creation/funder histories of the **specific** BARRON mint and DMAGA, and test whether any apparent intersection survives service-node filtering.
4. **P3-04 / 9Prm.** A social post alleges DMAGA trading results, but the attached sampled video illustrates **WOLF/SOL**. The clip is not proof of a DMAGA trade and should not be used for attribution. Financial performance of 9Prm remains a separate on-chain question.
5. **P3-05/06/07.** Contract homonym (EVM DMAGA); PERCY as control for a recurring Kekius creator; pre-DMAGA PEIPEI/QUBY performance claims for 2d86. These are comparator/negative-control tasks rather than new DMAGA funding links.

**Critical distinction:** [PR #25](https://github.com/searadacunha/Dark-MAGA/pull/25) adds an on-chain reconstruction of older X leads (7GVC transfers, Noah holdings, KLLARY, event windows); the current pass 3 adds documentary context and targeted tests for that reconstruction. Do not add the numerical claims in these X screenshots to financial totals until their individual transactions are independently identified.

See [research status and acceptance gates](../../RESEARCH_STATUS_2026-11-06.md). No new public-facing claim of Musk participation, wallet ownership or insider trading follows from these documents.
