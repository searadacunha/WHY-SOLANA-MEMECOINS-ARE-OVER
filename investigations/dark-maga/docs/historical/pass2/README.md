# Dark-MAGA — Historical X research, pass 2 (6 November 2026)

This directory preserves the **five user-supplied Grok research deliverables** from the second retrospective pass as source documents, not verified findings from on-chain investigation.

## Files and provenance
- `DMAGA_X_NEW_FINDINGS.md`: 15 further historical observations (N01–N15), including corrections and source-level leads.
- `DMAGA_GROK_TO_CLAUDE_HANDOFF.md`: prioritized, falsifiable forensic checks. **Instructions are proposals; no chain replay occurred in this import.**
- `DMAGA_WALLET_TWEET_LEADS.csv`: 24 source-linked leads, five named Jeffro wallets and four *socially documented candidate* comparator mints. The field `evidence_status` is `SOCIAL_CLAIM_NOT_CHAIN_VERIFIED`.
- `DMAGA_X_SEARCH_COVERAGE.md`: 89 retrospective X calls, search coverage, limits and references to unavailable local raw responses/media.
- `../../../data/historical_x_pass2/DMAGA_X_ARCHIVE.part-001.jsonl` through `part-005.jsonl`: the single uploaded `DMAGA_X_ARCHIVE.jsonl` was split in original record order into **five consecutive parts** for repository review. Each JSONL record's content was preserved logically; the original file's byte-level identity is **not** asserted.

The 1,001 JSON records have unique IDs, timestamps and author IDs; 374 unique author IDs and 35 records marked present in the older corpus. That is an internal consistency check, not proof that the X API, media or claimed transfers are authentic. All posts were collected retrospectively; counts are not independent witnesses. Check `DMAGA_X_SEARCH_COVERAGE.md` for incomplete source responses and query limits.

## Directly actionable *documentary* updates
- N01: @JeffroBTC's contemporaneous reply `1815291795787690478` gives complete addresses of three formerly truncated satellites: `A1UDMqcUC8RkZ8YENAktdueSQ6jxUUBickBK2y61vQ8J`, `6QFDe4yu9mVhv3cbbaMtkTnakz4bGJLAjLjhwrMn5jqD`, `H4mQu98TuxYTn3VSJone6jCTiDfXpuKcZbNZGHKUJU5y`. **No transfer signatures were verified here**; the parent alleges 5/60/16 SOL.
- N06: `1815088124193579253` is a stand-alone rotation statement; `1815088727250858444` replies to `1815084272098697611` by @DegenerateNews. The two @dissident42069 posts are not replies to each other. This corrects A7's context without demonstrating any wallet action.
- N07: @realjohnnewburg posted a screenshot showing the changed Musk profile at **19:25:23 UTC on 2024-07-21**, earlier than the source from pass 1 at 19:27:24. With the existing Wayback lower bound, the *documentary* interval is **[19:03:27, 19:25:23] UTC**. The exact avatar-click time is not known, and the screenshot's media bytes are **not included** here.
- N04/N05/N11/N14: social sources explicitly print candidate Solana contract addresses for **KLLARY, RETIREDI0, BARRON, ZOOMER**. None has been tied by an audited swap to the target wallets in this import. **JOE, BILLY and WIF have no established mint for this comparison.**
- N08/N09: Noah's screenshot is transcribed as 204,505,170 tokens across 14 displayed rows (20.450517% if the denominator were exactly 1B), while individually truncated percentages sum to 20.39%. Its snapshot slot and exact supply remain unknown. The 6QFD line is **not color-grouped** with Noah's four claimed entities; social overlap is not common wallet ownership.
- N12: possible Jupiter atomic arbitrage at slot 279711913 is a potential *negative control* for insider labeling, not a confirmed transaction classification.
- N15: A1UD tracker publications mix mark-to-market, realized proceeds and asserted non-sales. Recalculate from ledger, not snapshots.

## Offline verification
Run these without RPC access:
```bash
python scripts/audit_pass2_x_archive.py
python -m pytest -q tests/test_pass2_historical_x.py
```
The audit checks JSONL integrity, timestamp consistency, source cross-references, exact reported addresses and known original/repost/reply edges. It **cannot** verify X image provenance, media SHA256, tx signatures, PnL or asset ownership.

## Evidence boundaries / next action
The source report references `/workspace/dmaga_pass2_work/raw/` and downloaded images in the researcher's workspace. **Those raw HTTP response files and media binaries are not part of these five uploaded deliverables**; only post variants, URLs and reported hashes in JSONL/coverage are available.

Use `PROMPT_CLAUDE_PASS2.md` to execute a separate on-chain replay with transaction receipts. Preserve the existing `README.md`, frozen studies and unrelated deBridge/Kekius investigations. Historical source findings do not establish insider trading, knowledge by Musk, coordinated financial ownership, or a DMAGA/Kekius common operator.
