# Dark MAGA ($DMAGA) investigation

An on-chain and public-source investigation by Benjamin Da Cunha into the launch, trading activity, funding and exits of the Solana token **$DMAGA**, and the public chronology surrounding Elon Musk's adoption of a related image in July 2024.

**Token mint:** `7D7BRcBYepfi77vxySapmeqRNN1wsBBxnFPJGbH5pump`.

## Status and branches

**The investigation is not validated.** This branch preserves the original report and frozen study. Substantial later work is on [audit-2026-11-03](https://github.com/searadacunha/Dark-MAGA-Investigation/tree/audit-2026-11-03), which was eight commits ahead of the original `main` snapshot when reviewed on 4 November 2026.

Read the later [H review](https://github.com/searadacunha/Dark-MAGA-Investigation/blob/audit-2026-11-03/audits/2026-11-03/work_H/REAUDIT_CONCLUSIONS.md) and [I review](https://github.com/searadacunha/Dark-MAGA-Investigation/blob/audit-2026-11-03/audits/2026-11-03/work_I/REFUTATION.md) before reusing figures from this branch. H recorded 73 PASS, 15 FAIL and 11 INCONCLUSIVE assertions out of 99. I identifies additional accounting and interpretation corrections. A README update does not merge or validate that audit work.

## What to read

| File or directory | Purpose |
|---|---|
| [docs/CASE_REPORT.md](docs/CASE_REPORT.md) | Original synthesis. Several statements are superseded by the later reviews linked above. |
| [docs/TIMELINE.md](docs/TIMELINE.md), [reports/](reports/) | Chronology, early buyers, accounting, coordination and attribution. |
| [etude_final/](etude_final/) | Frozen primary protocol, code, results and amendments. |
| [etude/CONTAMINATION_E2E.md](etude/CONTAMINATION_E2E.md) | Explains why the earlier study registry is not the final study. |
| [dmaga/](dmaga/), [scripts/](scripts/) | Collection, normalization, accounting and reporting code. |
| [evidence/](evidence/) | Archived sources, labels and manifests. |
| [viz/index.html](viz/index.html) | Local visualization, reflecting the report version that generated it. |

Detailed research material remains in French. This overview is in English.

## Interpretation

The archived creation transaction dates the token to **14 July 2024, 02:05:25 UTC**. That does not date the beginning of a social account or private preparation.

The descriptive 33-wallet transfer component is separate from the creator's funding/deposit cohort. The later audits explicitly place the creator **outside** that component. Financial links do not, by themselves, identify a single owner.

The frozen primary study used 211 comparators and returned its predefined non-detection verdict. Later power checks show that the result supplies little evidence for or against advance knowledge. The [later group study](https://github.com/searadacunha/Dark-MAGA-Investigation/blob/audit-2026-11-03/etude_groupe/results.md) collected 48 of its required 59 comparators and remains inconclusive.

The later reviews also require separation of exact wallet populations, tokens deposited into DCA orders versus tokens actually sold, and tips or retained-token valuations versus realized profit. A shared exchange or service alone is never proof that two wallets have the same owner. No real-world identity, unlawful act or privileged information is established.

## Reproduction and handover

The full raw archive and large Parquet files are outside Git. Locations and hashes are documented in [state/STATE.md](state/STATE.md) and [evidence/RAW_MANIFEST.tsv](evidence/RAW_MANIFEST.tsv). A checkout alone cannot reproduce the entire investigation. The historical `scripts/py.sh` launcher expects the original macOS interpreter and external dependency directory.

Run substantial computations under `scripts/guard.py`. Preserve the frozen protocol and archived evidence; methodological changes belong in amendments and separate result sets. Read [AGENTS.md](AGENTS.md), [state/STATE.md](state/STATE.md), [JOURNAL_AGENTS.md](JOURNAL_AGENTS.md) and the latest audit before continuing a session.
