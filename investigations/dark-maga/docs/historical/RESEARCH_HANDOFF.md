> **UPDATE — 2026-11-06 PASS 2:** See [pass2/README.md](pass2/README.md), [pass2/DMAGA_GROK_TO_CLAUDE_HANDOFF.md](pass2/DMAGA_GROK_TO_CLAUDE_HANDOFF.md) and [pass2/PROMPT_CLAUDE_PASS2.md](pass2/PROMPT_CLAUDE_PASS2.md). The original A7 reply-time paradox is resolved in N06; a new documentary avatar upper bound of 19:25:23 UTC is proposed in N07; the A1UD/6QFD/H4mQ full addresses and four social comparator-mint candidates are now reported. These are still documentary observations, not on-chain proofs. The material below records the prior state and may contain superseded research tasks.

# 2026-11-06 | Historical X intelligence — integration and verification plan

This dossier is a **historical research addendum**, not a new verdict on insider trading. It preserves the source report in `DMAGA_HISTORICAL_INTELLIGENCE_2026-11-06.md` and the 12 lead IDs in `X_SOURCE_MANIFEST.json`. The original report's raw X responses, screenshots, local `/workspace/dmaga_evidence/` folder, and blockchain receipts **were not attached**. They must be obtained and checksummed before claiming source-level reproduction.

## What is known in this repository vs what is new

- Existing project datasets already include 7GVC, 9Sxm, AtZj, 5QhJJc, H3Qs and GXZvX. **Do not list them as newly discovered wallets.**
- New historical sources A3 (@JeffroBTC) and A4 (@Noah_nftn) independently *describe* overlapping wallet sets. Neither report's new financial claims was verified on-chain in this import.
- A1 points to original/repost provenance confusion, including `1814779160377602331` (a @DarkMagaCoin repost) vs original `1814763940410499481` (@pmarca). A second control is `1813220461867573395` (repost) vs `1813086353741230327` (@kanpai original). **Audit the original object, referenced_tweets, archive payload, and author's user ID before changing event dates.**
- A2's screenshot on @AutismCapital at `2024-07-21T19:27:24Z` would improve the upper documentary avatar bound from `19:30:13Z`. This is a post-published screenshot, **not** the timestamp of Musk's avatar click. Keep the lower Wayback bound `19:03:27Z` unless independent evidence changes it.
- A7 has a temporal inconsistency requiring source verification: the alleged response at `18:15:06Z` precedes its alleged parent at `18:17:29Z`. Do not infer the conversation's reply direction.

## Why changing Markdown alone is unsafe

The existing `scripts/rep_75_timeline.py` manually labels the repost `1814779160377602331` as an original from @pmarca. `scripts/ana_50_cohorts.py` also hardcodes `pmarca_image_rouge` and `musk_borne_haute`; it regenerates `data/events.json`, `data/windows.csv`, and `cohorts.parquet`. Other reports consume these generated files. **Change generator code first and regenerate only with the required raw ledgers available.** Otherwise a partial edit can produce mutually inconsistent event windows and trading claims.

The new `scripts/audit_x_post_provenance.py` is a read-only source-audit aid:
```bash
python scripts/audit_x_post_provenance.py --input data/x_posts.jsonl --output /tmp/dmaga-x-provenance-flags.jsonl
python -m unittest discover -s tests -p test_x_provenance.py -v
```
Its output comprises **flags for review**, not verified retweets, fraudulent posts, or proof of attribution. Reconcile findings with `referenced_tweets` and archived original payloads; do not use the count of timestamp mismatches as a fraud metric.

## Priority work, in order

1. **P0 — Fix post provenance**: deterministic original/repost/quote/reply graph, raw source provenance, timestamp validation. Check source authors and archive IDs before editing `TIMELINE`.
2. **P0 — Rebound Musk profile**: hash the @AutismCapital attachment, compare against existing Bailey and archived profile images; compute trading-window sensitivity under old/new upper bounds. No claim of precise click time.
3. **P1 — Replay Jeffro's claim**: 7GVC `7GVCZAYG5NfiJsuqUdvc9hB2ts2W3tSrGdya4CyR1M5j`, 9Sxm `9Sxmf25WG5WVQ5p86ycWeo5hMEwxiWPkFtLdRdTrHSQS`, alleged 190-SOL Jupiter inflow, 41.2M DMAGA buy, 20M distribution and 5/60/16 SOL satellite funders; identify all signatures, inner instructions and intermediate accounts. Do not equate a Jupiter program with an individual funding source.
4. **P1 — Test Noah's four groups**: reproduce exact edges and holdings at a *fixed slot*, remove DEX, CEX, routers, escrows, dusting and shared services. Challenge each inferred single-owner group and document separations.
5. **P1 — Cost-basis controls**: AtZj self-transfer and received-token costs; do not call 20 USD → 60k USD net profit without full ledger.
6. **P2 — Comparative hypotheses**: authenticated KLLARY contract, claimed RETIREDI0 rotation after Biden's public announcement, H3Qs's JOE/ZOOMER trades, GXZvX selling around avatar removal, BOSSIE public promise; do not infer direct control from tweet mentions.
7. **P2 — Independent records**: authenticate the October @DarkMagaCoin claim of speaking to Musk; newspaper repetition of the project's own text is not a second witness.

## Merge protocol

Keep `README.md`, frozen studies, unrelated deBridge/Kekius investigation trees and existing results untouched until evidence and regression tests support an update. Make changes on a separate branch with a PR. Store new forensic findings with transaction signatures, original URLs, UTC timestamps, explicit evidence status, instructions for reproduction, and negative controls. No watch/cron/continuous bot is needed: the target evidence is historical.
