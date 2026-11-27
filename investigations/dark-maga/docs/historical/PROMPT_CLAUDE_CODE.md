> **UPDATE — 2026-11-06 PASS 2:** The more recent, complete execution prompt is [pass2/PROMPT_CLAUDE_PASS2.md](pass2/PROMPT_CLAUDE_PASS2.md). It supersedes the unresolved wallet abbreviations, the older avatar upper bound, the erroneous A7 reply interpretation, and unspecified comparator contracts in the original prompt below. Read pass 2 before running any investigations.

# Claude Code — DMAGA | Historical intelligence integration and falsifiable on-chain reconstruction

**Run once. Work in an isolated branch/worktree. Do not run recurring collectors.**

You are the forensic maintainer of `https://github.com/searadacunha/Dark-MAGA`.
Mint in scope: `7D7BRcBYepfi77vxySapmeqRNN1wsBBxnFPJGbH5pump` (Solana).
This is a research investigation, not a token-promotion project. Claims of insider trading, common wallet ownership, direct funding by Musk, or the same DMAGA/Kekius operator REQUIRE evidence; they are NOT initial assumptions.

## Start safely
1. Read `README.md` and the existing methods and restrictions in `docs/CASE_REPORT.md`, `docs/SOCIAL_FINDINGS.md`, `docs/TIMELINE.md`, `reports/ATTRIBUTION.md`, `reports/COORDINATION.md`, `reports/MISSING_EVIDENCE.md`, `reports/EARLY_BUYERS.md`, and the `FINDINGS.md` from the existing three investigations (EVM deeptrace, Base/BSC/Solana deBridge, DMAGA/Kekius). Read `docs/historical/RESEARCH_HANDOFF.md`, `docs/historical/X_SOURCE_MANIFEST.json`, and the complete source memo `docs/historical/DMAGA_HISTORICAL_INTELLIGENCE_2026-11-06.md`.
2. Review branch `research/dmaga-historical-2026-11-06` and its PR first; integrate onto it or create a non-conflicting follow-up branch from current main. Do not duplicate or overwrite work by parallel agents.
3. Find the actual local working checkout (possibly under `/Volumes/TravailExterne/Enquetes-Crypto`). Never assume a path, and never run cleanup, reset, force push, recursive deletion, or large recomputation without inspecting changes and inputs. Use a separate worktree.
4. The repository README is frozen for this task: **DO NOT edit it**. Do not rewrite frozen studies, unrelated branches or other investigators' artifacts. Only publish verified changes in an isolated PR.
5. Never print keys/tokens. Prefer already configured RPC/Helius credentials via environment variables; respect rate limits, checkpoints, network budgets and the existing shared worker limit. Use public Solana JSON-RPC or a known archival provider if required; if historic data is unavailable, say so.

## Workstream P0 — source provenance & time
- Audit all 5,155 `data/x_posts.jsonl` records. Run `python scripts/audit_x_post_provenance.py --output /tmp/dmaga-x-flags.jsonl`; reconcile the flagged rows against original X objects, X author IDs, `referenced_tweets`, archived raw responses, Wayback CDX URLs, and media metadata. Do not infer author from the archive URL. 372 timestamp disagreements in a source memo are **flags**, not 372 proven reposts.
- Control examples: `1814779160377602331` (repost attributed to @pmarca) vs @pmarca original `1814763940410499481`; `1813220461867573395` vs @kanpai original `1813086353741230327`. Reconstruct original/repost/quote/reply edges with a verifiable row-level evidence map.
- Check the A7 chronology paradox: a tweet at 18:15:06 UTC supposedly replying to a 18:17:29 UTC tweet. Validate direction and context before narrative conclusions.
- Confirm @AutismCapital's `1815106321810919673` 2024-07-21 19:27:24 UTC screenshot and its original image; compare file hashes and visual content to Bailey's screenshot and archived Musk profile. It establishes at most a documentary *upper* bound, NOT the second when Musk clicked. Existing Wayback *lower* bound: 19:03:27 UTC; candidate upper: 19:27:24 instead of 19:30:13.
- Investigate the classification of transactions between 19:27:24 and 19:30:13. Update `scripts/rep_75_timeline.py` and `scripts/ana_50_cohorts.py` together only after source control. If historic raw inputs are present, rederive `data/events.json`, `data/windows.csv`, cohort data and all dependent derived reports in the normal pipeline; quantify differences, compare against baseline, test invariants. If inputs are absent, leave generated numbers untouched and prepare a precise patch/reproduction command.

## Workstream P1 — independent financial replays
**A3 (@JeffroBTC, 1815291249102119198, 22 July 2024):**
- Fully replay wallet `7GVCZAYG5NfiJsuqUdvc9hB2ts2W3tSrGdya4CyR1M5j` against `9Sxmf25WG5WVQ5p86ycWeo5hMEwxiWPkFtLdRdTrHSQS` around 14 July 2024 01:00–03:00 UTC.
- Verify or reject the claimed 190-SOL credit from Jupiter Perpetuals, 41.2M DMAGA purchase, 20M DMAGA transfer, sales near 02:26 UTC, and satellite funds 5, 60, 16 SOL. Resolve `A1UD…vQ8J`, `6QFD…5jqD`, `H4mQ…JU5y` ONLY by observed unique counterparties and instruction data, never from guessed Base58 completions.
- Capture signatures, slots, exact amounts, before/after token balances, nested SPL/ATA/System instructions, fee payers, destination accounts and transfer direction. A Jupiter service is NOT a personal funding identity.
**A4 (@Noah_nftn, 1815372294426124565):**
- Rebuild four asserted wallet sets as of an explicitly specified slot. Match the original full addresses in A4; distinguish single-owner evidence from mere token transfers. Remove pools, exchanges, shared service funding, dusting and escrow relationships, and run sensitivity/negative controls.
- Explicitly test the three less familiar addresses Eaoxy…, APfA…, AeiMit… against the entire repository and archival data; don't declare them globally new merely because they were absent from short tables.

## Workstream P2 — falsifiable controls
- Recalculate AtZj's claimed `$20 -> $60k` **with cost basis of tokens received**, all transfers and actual proceeds, not screenshots or terminal mark-to-market.
- Event study of GXZvX's reportedly $88,771 in sales around **avatar removal on July 23**, not avatar adoption on July 21; compare its full 103 sales and matched wallets.
- Authenticate contract mint(s) for KLLARY and RETIREDI0 from dated primary sources before linking DMAGA. Do not select ticker contracts opportunistically. Compare the same resolved wallets and political-memecoin controls; public Biden withdrawal information may explain rotations.
- Assess H3Qs's complete JOE/ZOOMER/DMAGA track record, including losses, fees and normal behavior. Verify BOSSIE self-claimed wallet `HRoWqUvWbnmA3p5qMy4fqqgHQe843ohchF8RvwNocHTu`, budget and purchases but don't equate self-declaration with control.
- Separate direct transfers, shared services, timing coincidences, promotional claims and unknowns. No inference of property ownership from interactions, similar amounts or shared DeBridge/Jupiter infrastructure.

## Deliverables & standard of proof
- Put new results in `docs/historical/` or a clearly versioned investigation subdirectory, not README. Provide an evidence index: source link, raw-content SHA256, UTC time, mint, transaction signature, decoded instruction, classification (CONFIRMED / SUPPORTED / NOT_CONFIRMED / REFUTED), alternative explanations, and executable reproduction steps.
- Create tests for the source/repost graph, timeline boundaries, cohort cuts, token-homonym exclusion, and at least one false-positive synthetic service hub. Do not silently replace previous cohort numbers.
- Keep a concise finance-first executive summary with exact newly verified flows and evidence links. State plainly when a material hypothesis is still unresolved.
- Run appropriate offline tests and publication guard; report which tests actually executed, which could not run, and why. Open a focused PR for changes; do not merge or alter main before checks and review.
- Final response: (1) confirmed NEW findings vs known results, (2) strongest existing evidence, (3) rejected or untestable hypotheses with explanation, (4) exact files changed/tests and PR link, (5) highest-value remaining question.
