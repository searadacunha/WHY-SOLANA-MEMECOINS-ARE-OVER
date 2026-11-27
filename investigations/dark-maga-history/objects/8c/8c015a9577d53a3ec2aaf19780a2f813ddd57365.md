# Reproduction and branch guide

## Choose the research version

`main` is the landing page and preserves its own research snapshot. `audit-2026-11-03` contains subsequent audits, accounting corrections and offline pipeline tests. The two branches are not interchangeable.

The root README links its research claims to the audit snapshot `6e839acc022a38427fdb1f4f3b221488db454a78`. Read the H numerical review and the later I transaction review with the older generated reports. The README evidence ledger is `docs/README_REVIEW_2026-11-05.md`.

The narrative update does not merge the two research trees. It does not imply that `d01-correction` has been integrated.

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

## Forensic pipeline integrity (proposed 6 November fixes)

The pipeline must rebuild `token_edges.parquet` **before** running `ana_20_pnl.py`, because cost basis consumes transfers that are missing from the standard trade normalization. Stale transfer files must not be reused in a fresh PnL calculation.

The proposed `dmaga/db.py` deduplicates overlapping source slices using transaction, event type, owner, venue and token delta, while retaining the preferred raw-history source. `ana_19_export.py` reads the fresh shards, validates a staging Parquet and only then replaces the previously validated export. The normalizer retains the last materialized export if shard rebuilding fails. Failed batch commands now stop the driver.

The `Forensic pipeline regression checks` workflow runs offline parser, PnL and deduplication tests on `main` pull requests. These tests do **not** independently validate the historical July 2024 PnL, full token-transfer coverage, source-provider labels or the conclusions in the root README.

Before treating regenerated numerical claims as independently reproduced, rerun the complete derivation with the archived raw data on an isolated external volume, check the physical `trades.parquet` for duplicate keys, run the report self-check, and reconcile affected wallet-level and cohort results against the audit branch. Do not rewrite any frozen protocol or source archive.

## Full reproduction requires external data

Raw responses and large Parquet files are outside Git. Their recorded paths and manifests are in `state/STATE.md`, `evidence/RAW_MANIFEST.tsv` and, on the audit branch, `evidence/DATA_V2_MANIFEST.tsv`.

On the audit branch, `DMAGA_EXT` selects the external archive. `DMAGA_BIG` must select a separate derived-output directory, such as `data_v3`, without overlapping archived data or frozen studies. Check the actual mounted disk and the paths in `scripts/py.sh`; that historical launcher expects the original macOS interpreter and external dependencies.

Run substantial computations through `scripts/guard.py`. The historical `main` version of `scripts/chk_90_selfcheck.py` checks base58 references in top-level `docs/*.md` and `reports/*.md`; the audit version also checks duplicate trades. These checks need their actual inputs. Finding an identifier in an archive does not verify the amount, date, direction or interpretation of the surrounding claim. Neither version validates the deBridge investigation directory. Offline tests are not a substitute for a raw-data replay.

The `main` [case report](CASE_REPORT.md) explicitly retains its historical synthesis. Its opening scope note and the later H/I reviews govern interpretation of the creator and exact-33 wallet populations.

## deBridge evidence checks

The corrected deBridge package has a separate offline validator using only the Python standard library:

```bash
python3 investigations/2026-11-05_debridge_winners/validate.py
python3 -m unittest discover -s investigations/2026-11-05_debridge_winners -p 'test_*.py' -v
```

These checks reconcile the table with pinned archival evidence, preserve the decoded maker's cohort, and distinguish source amounts, requested destination amounts and reported destination execution. They do not perform new RPC queries or independently confirm that every destination executed. The dedicated deBridge workflow runs them separately from the publication guard.

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
