# Reproduction and branch guide

## Choose the research version

`main` contains the landing page, the active pipeline, its offline tests and dated research snapshots. `audit-2026-11-03` contains a separate set of audits, accounting corrections and offline pipeline tests. The two branches are not interchangeable.

The root README links its research claims to the audit snapshot `6e839acc022a38427fdb1f4f3b221488db454a78`. Read the H numerical review and the later I transaction review with the older generated reports. The README evidence ledger is `docs/README_REVIEW_2026-11-05.md`.

The narrative update does not merge the two research trees. It does not imply that `d01-correction` has been integrated.

## Offline tests on main

Use Python 3.12 and a separate checkout of `main`. The pinned dependencies match the CI environment verified on 10 November 2026:

```bash
python3.12 -m venv .venv
.venv/bin/python -m pip install -r requirements-test.txt
.venv/bin/python -m pytest -q tests --ignore=tests/test_publication_guard.py
.venv/bin/python -m unittest discover -s tests -p test_publication_guard.py -v
```

The first command suite discovers all core tests, including window boundaries, integer quote conservation, transfer cost basis and missing-price failures. Publication tests use disposable local Git repositories. Neither suite needs API credentials or the original external drive.

The investigation suites use the standard library and their published fixtures:

```bash
.venv/bin/python investigations/2026-11-05_debridge_winners/validate.py
.venv/bin/python -m unittest discover -s investigations/2026-11-05_debridge_winners -p 'test_*.py' -v
.venv/bin/python -I -m unittest discover -s investigations/2026-11-05_evm-recipient-deeptrace/tests -v
(cd investigations/2026-11-05_evm-recipient-deeptrace/scripts && ../../../.venv/bin/python -I s99_selfcheck.py)
.venv/bin/python -I -m unittest discover -s investigations/2026-11-06_debridge_base_bsc_solana/tests -v
.venv/bin/python -I investigations/2026-11-06_debridge_base_bsc_solana/scripts/s13_orderid_check.py
.venv/bin/python -I investigations/2026-11-06_debridge_base_bsc_solana/scripts/s99_selfcheck.py
.venv/bin/python -I -m unittest discover -s investigations/2026-11-06_historical_replay/tests -v
.venv/bin/python -I -m unittest discover -s investigations/2026-11-06_dmaga_kekius_cross_token/tests -v
```

These checks validate stored evidence and reject malformed or contradictory inputs. Their scope is described in the [10 November audit](AUDIT_2026-11-10.md); passing them does not reconstruct the complete historical PnL.

## Offline tests on the audit branch

Use a separate checkout of `audit-2026-11-03`, Python 3.12 and an isolated environment. Do not switch a working directory while another agent is changing it.

```bash
python3.12 -m venv .venv
.venv/bin/python -m pip install -r requirements-test.txt
.venv/bin/python scripts/guard.py -- .venv/bin/python -m pytest tests -q
```

These dependencies cover the offline test suite, not every historical audit script. Software-test success does not validate the completeness of transaction collection or every research conclusion.

After fetching the current remote target, the publication guard checks branch ancestry, the accepted README and locked protocol files:

```bash
python3 scripts/check_publication.py --target audit-2026-11-03
```

Use `--target main` only for a candidate based on `main`. The guard reads local Git refs; it does not fetch them. Passing it is not server-side branch protection.

The policy is read from the destination commit and must remain identical in the candidate commit, index and working tree. A candidate cannot approve its own README by changing `state/publication_baselines.json`, or silently remove a study lock. In CI, pull requests use the event's base SHA; pushes use the destination SHA **before** the push. An absent destination or policy fails the check. An explicitly authorized future baseline migration needs a separately reviewed publication procedure; changing the candidate policy alone cannot validate it.

## Forensic pipeline integrity (merged 6 November 2026, PR #19)

The pipeline must rebuild `token_edges.parquet` **before** running `ana_20_pnl.py`, because cost basis consumes transfers that are missing from the standard trade normalization. Stale transfer files must not be reused in a fresh PnL calculation.

The merged `dmaga/db.py` deduplicates overlapping source slices using transaction, event type, owner, venue and token delta, while retaining the preferred raw-history source. `ana_19_export.py` reads the fresh shards, validates a staging Parquet and only then replaces the previously validated export. The normalizer retains the last materialized export if shard rebuilding fails. Failed batch commands now stop the driver.

The `Forensic pipeline regression checks` workflow runs offline parser, PnL and deduplication tests on `main` pull requests. These tests do **not** independently validate the historical July 2024 PnL, full token-transfer coverage, source-provider labels or the conclusions in the root README.

Since the 10 November audit, GTBA-only transfer legs are netted by transaction and owner before costing. Quote amounts are allocated in integer units with an exact conserved sum. Every SOL/USD minute price used for a swap or stablecoin conversion must be finite and positive; a missing or invalid required price stops the export and preserves the previous `wallets.parquet`. Documentary windows use `[start, end)` consistently, so a trade at the first capture belongs to the following window.

Before treating regenerated numerical claims as independently reproduced, rerun the complete derivation with the archived raw data on an isolated external volume, check the physical `trades.parquet` for duplicate keys, run the report self-check, and reconcile affected wallet-level and cohort results against the audit branch. Do not rewrite any frozen protocol or source archive.

## Full reproduction requires external data

Raw responses and large Parquet files are outside Git. Their recorded paths and manifests are in `state/STATE.md`, `evidence/RAW_MANIFEST.tsv` and, on the audit branch, `evidence/DATA_V2_MANIFEST.tsv`.

On the audit branch, `DMAGA_EXT` selects the external archive. `DMAGA_BIG` must select a separate derived-output directory, such as `data_v3`, without overlapping archived data or frozen studies. Check the actual mounted disk and the paths in `scripts/py.sh`; that historical launcher expects the original macOS interpreter and external dependencies.

Run substantial computations through `scripts/guard.py`. The current `main` `scripts/chk_90_selfcheck.py` checks base58 references in top-level `docs/*.md` and `reports/*.md`, and detects duplicate keys in the physical exported `trades.parquet`. These checks do not validate historical cost basis without the complete raw corpus. These checks need their actual inputs. Finding an identifier in an archive does not verify the amount, date, direction or interpretation of the surrounding claim. Neither version validates the deBridge investigation directory. Offline tests are not a substitute for a raw-data replay.

The `main` [case report](CASE_REPORT.md) explicitly retains its historical synthesis. Its opening scope note and the later H/I reviews govern interpretation of the creator and exact-33 wallet populations.

## deBridge evidence checks

The corrected deBridge package has a separate offline validator using only the Python standard library:

```bash
python3 investigations/2026-11-05_debridge_winners/validate.py
python3 -m unittest discover -s investigations/2026-11-05_debridge_winners -p 'test_*.py' -v
```

These checks reconcile the table with pinned archival evidence, preserve the decoded maker's cohort, and distinguish source amounts, requested destination amounts and reported destination execution. They do not perform new RPC queries or independently confirm that every destination executed. The dedicated deBridge workflow runs them separately from the publication guard.

## Follow-up investigations merged on 6 November 2026

- [PR #17](https://github.com/searadacunha/Dark-MAGA/pull/17) repairs the relay-aware provenance bounds and decodes DLN FulfilledOrder v2. Its standalone self-check and Base/BSC/Solana checks ran successfully in CI after merge.
- [PR #20](https://github.com/searadacunha/Dark-MAGA/pull/20) requires the full ABI event topic0 for both FulfilledOrder variants and CreatedOrder before interpreting an order. Synthetic regression tests check nonmatching topics.
- [PR #18](https://github.com/searadacunha/Dark-MAGA/pull/18) adds the separate DMAGA–Kekius investigation, with 15 offline assertions. Its `k37` operator-counterparty list is a balance-delta *screen*, not proof of direct transfers: the direct edges still require instruction-level validation.
- The original draft [PR #1](https://github.com/searadacunha/Dark-MAGA/pull/1) is closed, superseded by PR #19; do not import its previous README into `main`.

Run the relevant workflow suites on each new branch, then rerun the publication guard. Those tests validate stored fixtures, bookkeeping invariants and decoder behavior, not the entire raw-data archive or the possibility of privileged information.

## Evidence and handover

On the audit branch:

| Path | Purpose |
|---|---|
| `docs/CASE_REPORT.md`, `docs/TIMELINE.md` | Generated synthesis and chronology. Read with subsequent audit corrections. |
| `reports/` | Trading, early buyers, coordination, attribution and data checks. |
| `audits/2026-11-03/work_H/` | Numerical review and claim checks. |
| `audits/2026-11-03/work_I/` | Transaction-level review, decoded bridge orders and execution checks. |
| `etude_final/`, `etude_groupe/` | Frozen protocols, results and amendments. |
| `dmaga/`, `scripts/` | Collection, normalization, accounting, reporting and resource controls. |
| `evidence/` | Archived sources and manifests. |
| `viz/index.html` | Visualization tied to its generating report version. |

Before continuing research, read `AGENTS.md`, `state/STATE.md`, `JOURNAL_AGENTS.md` and the latest dated review. Preserve frozen files and the original evidence. Methodological revisions belong in amendments and separate result sets.
