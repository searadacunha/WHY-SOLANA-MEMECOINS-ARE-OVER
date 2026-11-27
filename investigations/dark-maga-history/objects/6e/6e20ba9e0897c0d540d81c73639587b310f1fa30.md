# Dark MAGA ($DMAGA) investigation

An on-chain and public-source investigation by Benjamin Da Cunha into the launch, trading activity, funding and exits of **$DMAGA**, and the chronology of the images adopted by Elon Musk in July 2024.

**Solana token mint:** `7D7BRcBYepfi77vxySapmeqRNN1wsBBxnFPJGbH5pump`.

The repository contains transaction-processing code, archived evidence, reports, frozen statistical protocols and the objections raised during successive reviews. Financial links, common control, identity and prior knowledge are assessed separately.

## Current status

**The investigation is not validated.** The original `main` snapshot and subsequent work on `audit-2026-11-03` have different scopes. The audit branch was eight commits ahead of `main` at the start of the 4 November 2026 review; its latest existing commit was `1f2b4e0`.

The [H review](audits/2026-11-03/work_H/REAUDIT_CONCLUSIONS.md) recorded **73 PASS, 15 FAIL and 11 INCONCLUSIVE assertions out of 99**. The [I review](audits/2026-11-03/work_I/REFUTATION.md) identified further accounting and interpretation corrections. Those are historical review results; several objections remain open.

The [4 November review](docs/AUDIT_2026-11-04.md) corrects reproducible code defects and selected statements in the [case report](docs/CASE_REPORT.md) and its generator. It did not have the external raw archive, so it does **not** constitute a complete rerun of the financial or statistical investigation.

## Findings and their limits

| Question | Supported scope | Limit |
|---|---|---|
| Creation | The archived mint transaction is dated 14 July 2024, 02:05:25 UTC. | This dates the token, not private preparation or the creation of a social account. |
| Early financial links | The descriptive report identifies 33 wallets linked by 40 direct token transfers. | The creator is outside that component. A connected component does not establish a single owner. |
| Exchange links | The report examines funding sequences, subsequent deposits and controls. | A shared hot wallet or service alone does not establish common ownership. Deposit type, operator and beneficiary are separate claims. |
| Pre-event buying | The [frozen primary study](etude_final/results.md) returned its predefined non-detection verdict with 211 comparators. | Later power checks show little ability to distinguish relevant alternatives. The result provides little evidence for or against prior knowledge. |
| Group comparison | The [group study](etude_groupe/results.md) provides descriptive results for 48 comparators. | It required 59: the verdict remains inconclusive. The late table freeze and other deviations are documented. |
| Bridge outflows | The archived order CSV contains **68 orders and $979,324.28** for the exact 33-wallet group. | All populations together total 76 orders and $1,023,933.51. Order values do not prove every destination-chain execution or realized profit. |

The bridge totals were recomputed from the committed [order CSV](audits/2026-11-03/work_G/g43_orders.csv) and [membership list](data/prevent_groups.json). Fifteen of the group's orders, totaling $1,610.19, predate the mint. The earlier “P2” flow grouping differs from these 33 wallets.

The updated synthesis also distinguishes tokens **deposited into DCA orders from tokens sold**, and **tips and retained-token valuations from realized trading profit**. Those corrections are explicitly attributed to the H/I reviews; they were not independently replayed from the raw archive in this revision. No real-world owner, unlawful act or advance information is established.

## Repository map

| Path | Contents |
|---|---|
| [docs/CASE_REPORT.md](docs/CASE_REPORT.md) | Main synthesis, evidence levels, limits and open questions. |
| [docs/TIMELINE.md](docs/TIMELINE.md), [reports/](reports/) | Chronology, early buyers, accounting, coordination and attribution. Read alongside later audit corrections. |
| [audits/2026-11-03/](audits/2026-11-03/) | Reviews, claim ledgers, correction work, scripts and refutations. |
| [etude_final/](etude_final/), [etude_groupe/](etude_groupe/) | Frozen protocols, code, tables, registries and deviations. |
| [etude/CONTAMINATION_E2E.md](etude/CONTAMINATION_E2E.md) | Why the older `etude/` registry cannot serve as the final study. |
| [dmaga/](dmaga/), [scripts/](scripts/) | Collection, normalization, accounting, graphs, reports and resource guard. |
| [evidence/](evidence/) | Archived sources, labels and manifests. |
| [viz/index.html](viz/index.html) | Local visualization, reflecting the report version that generated it. |

Detailed research reports and evidence remain in French. This overview is in English.

## Offline code checks

Use Python 3.12 and an isolated environment:

```bash
python3.12 -m venv .venv
.venv/bin/python -m pip install -r requirements-test.txt
.venv/bin/python scripts/guard.py -- .venv/bin/python -m pytest tests -q
```

The pinned test dependencies cover this offline suite, not every historical audit script. Tests use synthetic transactions, small local tables and the archived protocol files; they make no network calls and need no credentials.

The 22 existing tests passed before the review. New regression cases exposed 25 failures in the previous code. After correction, **53 tests pass**, including verification of all **27 recorded file hashes** across the two frozen protocols. This does not establish completeness of the raw history or validate every research conclusion.

The required report-reference and duplicate-trade check, `scripts/chk_90_selfcheck.py`, has not run here because its actual input shards and supporting archive are unavailable; the offline tests and link checks do not replace it.

## Full data reproduction

The raw archive and large Parquet files are outside Git. Recorded locations and manifests are in [state/STATE.md](state/STATE.md), [evidence/RAW_MANIFEST.tsv](evidence/RAW_MANIFEST.tsv) and [evidence/DATA_V2_MANIFEST.tsv](evidence/DATA_V2_MANIFEST.tsv). A GitHub checkout alone cannot reproduce every result.

`DMAGA_EXT` selects the existing external archive. `DMAGA_BIG` must select a separate output directory, for example `data_v3`. The code rejects overlap with archived data, raw evidence and frozen studies, including aliases. The historical `scripts/py.sh` launcher expects the original macOS interpreter and external dependencies; verify its paths after a disk move.

Run substantial computations under `scripts/guard.py`. The files covered by both protocol locks remain unchanged. Methodological revisions require an amendment and a separate result set; a passing software test is not a reason to rewrite a frozen study.

For handover, read [AGENTS.md](AGENTS.md), [state/STATE.md](state/STATE.md), [JOURNAL_AGENTS.md](JOURNAL_AGENTS.md) and the latest dated review. Older tables and visualizations may still contain statements superseded by H/I.
