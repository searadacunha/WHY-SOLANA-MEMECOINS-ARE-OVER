# Claude Code — Dark-MAGA historical X pass 2 | forensic execution

You are maintaining `searadacunha/Dark-MAGA`. The Grok historical pass-2 source package was imported in **research/dmaga-historical-x-pass2-2026-11-06** (or its merged PR). Start from the **latest main**, inspect concurrent branches/PRs and use an isolated Git worktree. Do not overwrite anyone's research.

## Evidence to read first

Read the existing methods and results in `docs/CASE_REPORT.md`, `docs/SOCIAL_FINDINGS.md`, `docs/TIMELINE.md`, `reports/ATTRIBUTION.md`, `reports/COORDINATION.md`, `reports/MISSING_EVIDENCE.md`, `reports/EARLY_BUYERS.md` and all current deBridge/DMAGA–Kekius FINDINGS. Then read **all** of `docs/historical/pass2/` and `docs/historical/DMAGA_HISTORICAL_INTELLIGENCE_2026-11-06.md`. The pass-2 archive has 1,001 posts across five parts under `data/historical_x_pass2/`.

Run offline audits first:
```bash
python scripts/audit_x_post_provenance.py --input data/x_posts.jsonl --output /tmp/dmaga-pass1-flags.jsonl
python scripts/audit_pass2_x_archive.py
python -m pytest -q tests/test_x_provenance.py tests/test_pass2_historical_x.py
```
These tests establish **internal documentary consistency only**, not blockchain facts. No on-chain replay or source-media byte verification was performed by Grok. The 15 N findings are additions to A1–A12, not 15 independent witnesses.

## Highest-priority P0 corrections

1. Correct provenance of original X posts vs reposts in the **source generators**, not by hand-editing Markdown. Legacy `scripts/rep_75_timeline.py` and `scripts/ana_50_cohorts.py` contain hardcoded event IDs/bounds. Use the preserved archive references, original author IDs and `referenced_tweets`. Audit all old 5,155 records, but treat its timestamp mismatches only as flags.
2. Fix A7 chronology: autonomous `1815088124193579253` at 18:15:06 UTC; `1815088727250858444` at 18:17:29 UTC replies to @DegenerateNews `1815084272098697611` (17:59:47 UTC), **not** to the preceding dissident tweet. Both posts follow publicly known Biden withdrawal news, so the social rotation is not an advance warning of that news.
3. Confirm original screenshot/source `1815105812076904904` (@realjohnnewburg). Post: 2024-07-21 19:25:23 UTC; image URL in JSONL. Earlier than the previous upper documentary bound of 19:27:24. Compare actual media hashes/perceptual image identity against Winig/AutismCapital/Bailey/Wayback. The *candidate* interval becomes [19:03:27,19:25:23] UTC. **Do not infer precise click or screenshot time.**
4. Only after confirming evidence and loading the full historic ledgers, update event generators and regenerate `data/events.json`, `data/windows.csv`, `cohorts.parquet`, TIMELINE, EARLY_BUYERS and dependent derived reports. Quantify which wallet cohorts differ between 19:25:23 and 19:30:13 (including 19:25:23–19:27:24). If ledger is unavailable, leave generated figures unchanged and document a pending deterministic rebuild.

## Highest-priority P1 financial replays

**J01–J05 / N01** — @JeffroBTC's original comment `1815291795787690478` supplies all five full addresses, **not** signatures:
- 7GVC `7GVCZAYG5NfiJsuqUdvc9hB2ts2W3tSrGdya4CyR1M5j`
- 9Sxm `9Sxmf25WG5WVQ5p86ycWeo5hMEwxiWPkFtLdRdTrHSQS`
- A1UD `A1UDMqcUC8RkZ8YENAktdueSQ6jxUUBickBK2y61vQ8J`
- 6QFD `6QFDe4yu9mVhv3cbbaMtkTnakz4bGJLAjLjhwrMn5jqD`
- H4mQ `H4mQu98TuxYTn3VSJone6jCTiDfXpuKcZbNZGHKUJU5y`

Mint DMAGA: `7D7BRcBYepfi77vxySapmeqRNN1wsBBxnFPJGbH5pump`. Independently replay 14–22 July 2024 via raw Solana RPC, SPL/ATA/System instructions, inner CPIs, balance deltas, signer, fee payer, program IDs, signature, slot and UTC timestamps:
- Alleged 190 SOL received via Jupiter Perpetuals, 41.2M DMAGA bought, 20M sent to 9Sxm, 5/60/16 SOL satellite funding.
- Determine actual sender and fee payer for each alleged edge; do not infer that a Jupiter vault PDA is the personal funder or that receiving SOL proves common ownership.
- Test whether 6QFD's purported 60 SOL financing is direct, routed or a service interaction; reconstruct its 15,392,092-token position as of the relevant Noah screenshot *only if a slot can be established*.

**N04/N05/N11/N14** — Candidate documented mint contracts to check, never assume the wallets actually traded them:
- KLLARY `AUS4wtGQZcb6GPQxU4K8FRVqQMwUx2Q8G7K9JKuUpump`
- RETIREDI0 `DyKwrqZMEDVHYAd4gn9V8vFioQQg1bVEgGxqbUr5Mkvo`
- BARRON `HmAgiwjjP9CXqK5wQNsHKtjAt2CH3Kv8Q7xH5kGL2nqZ`
- ZOOMER `9MBzpyMRkj2r5nTQZMMnxnCm5j1MAAFSYUtbSKjAF3WU`

For BARRON, investigate claimed developer overlap against DMAGA *only* with independently verified mint creation authority, funding, signers or direct treasury transfers. Social labels like "dev" are ambiguous. For KLLARY and RETIREDI0, compare exact swaps/funding and baseline political-memecoin traders. For ZOOMER, first check H3Qs actually traded this exact mint. **Do not guess mints for JOE, BILLY or WIF.**

**N08–N10** — Validate the Noah screenshot transcription (14 rows totaling 204,505,170 DMAGA); verify time/supply; do not treat sum of rounded percentages (20.39%) as direct exact supply percentage or infer four wallet owners. Compare @Pamp_It_ and @ogtraders_sol July 22 snapshots to existing AtZj→Nxt transaction receipts and beware duplicate evidence.

**N12** — Retrieve Solana slot 279711913 and the actual tx matching `RjL5pLQXzCjMHtT6nBSc9xiCsp2VJR1VWPjfudHrkSZ`. Confirm/reject an atomic WSOL→DMAGA→WSOL round trip, complete fees/tips and net token exposure. If confirmed, classify as an arbitrage *control* rather than privileged-information evidence.

**N15** — Reconstruct A1UD's entire ledger through 5 August 2024; independently calculate cost of received tokens, realized proceeds, remaining quantity and mark-to-market at the exact historic snapshots. The tracker claim `$652 → $492k` may describe unrealized worth, not cash; challenge the alleged "never sold" claim with chain evidence.

**N13** — Validate the address and claimed holdings in the Hasten/ClayBro controversy against a mint/slot, without inventing the unavailable parent tweet or attributing an X author to a wallet.

## Priorities and proof requirements
For every hypothesis include original source ID, author ID, URL, primary media hash if available, *raw Solana tx signature*, slot, exact token mint, units, direction, CPI, counterparty type, alternative interpretation and an explicit classification **CONFIRMED / REFUTED / UNRESOLVED**. Separate direct transfers from common CEX/DEX/bridge infrastructure, and distinguish receipt, realized profit, remaining balance and peak market cap.

Do not fabricate signatures or private attribution. If archival RPC cannot return data, mark UNRESOLVED. Do not confuse pre-/post-avatar adoption with pre-/post-avatar removal.

## Constraints and publication
- No README edits, no modifications to frozen study inputs, unrelated deBridge/Kekius findings or other agents' branches.
- Preserve source memos as historical records; document corrected interpretations in new verified technical reports instead of silently altering Grok's original text.
- Use existing credential configuration only via secure environment variables, and enforce the shared network-worker limit/checkpoints. No secrets in output.
- Add receipts, machine-readable ledgers, runnable tests, base-rate/negative controls and a concise technical result summary. Validate offline CI and publication guard.
- Open a focused PR with source code, derived outputs only where reproducible, verified new findings and links to transaction receipts. Do not merge an unverified analysis or publish premature insider allegations.

On completion provide: precise new confirmed transactions vs known ones; supported/refuted/unresolved claims; changed files and executed tests; PR link; the highest-value remaining question. This is a finite historical investigation, no recurring monitoring.
