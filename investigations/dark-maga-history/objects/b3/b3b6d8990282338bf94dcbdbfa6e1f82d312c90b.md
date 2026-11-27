# Dark MAGA ($DMAGA) | On-chain forensic investigation

Private research repository examining the Solana token `7D7BRcBYepfi77vxySapmeqRNN1wsBBxnFPJGbH5pump`, its early funding and trading, token flows, and the public chronology surrounding its promotion in July 2024. **No wallet, account or person is identified here as having committed a crime.**

## Research status

**Not yet independently validated for publication (4 November 2026).** The main-branch case report and several derived tables predate a more recent independent audit. That audit documents duplicate trade rows, attribution and funding-label caveats, and claims requiring correction. Its findings and proposed remedies are in the separate [3 November audit branch](https://github.com/searadacunha/Dark-MAGA-Investigation/blob/audit-2026-11-03/audits/2026-11-03/AUDIT_FINAL.md) and [correction register](https://github.com/searadacunha/Dark-MAGA-Investigation/blob/audit-2026-11-03/audits/2026-11-03/CORRECTIONS.md). **Those audit reports have not been incorporated into the generated case report on `main`.**

The audit independently reproduced the core frozen calculations but reported 5,903 duplicate rows in the derived trade table and other issues affecting selected PnL and descriptive results. A proposed code fix must be followed by a complete re-derivation and verification against the raw data before the affected figures are republished. The original raw evidence and frozen study are preserved.

## What the evidence can and cannot show

- The token's mint transaction is dated **14 July 2024 at 02:05:25 UTC**, according to the archived on-chain records. The public-post timeline distinguishes verifiable timestamps from statements made by third parties.
- Funding and token-transfer graphs document interactions between addresses. A common exchange or service, close timing, or similar trading activity **does not establish common ownership or privileged information**.
- The frozen comparison with other tokens found **no measure significant after Holm correction**. The subsequent audit found that this test had very low power for realistic effects in the observed population. A nonsignificant result is therefore **not evidence of equivalence, innocence or absence of foreknowledge**.
- Estimates based on incomplete cost basis, transfers between wallets, routed swaps or incomplete history are not independently verified profits. Conclusions about organizers, account operators and their intentions remain limited by the available public evidence.

## Where to start

| Resource | Purpose |
|---|---|
| [Case report](docs/CASE_REPORT.md) | Main historical narrative; read together with the outstanding audit corrections |
| [Timeline](docs/TIMELINE.md) | Event timestamps, source quality and on-chain price context |
| [Attribution](reports/ATTRIBUTION.md) | Transaction evidence versus identity hypotheses |
| [Coordination](reports/COORDINATION.md) | Funding and wallet groups, including limitations |
| [Top traders](reports/TOP_TRADERS.md) | Realized-PnL estimates with cost-basis caveats |
| [Interactive visualization](viz/index.html) | Locally viewable evidence and relationship map |
| [Agent state](state/STATE.md) | Operational dependencies, checkpoints and restart instructions |

## Code and reproducibility

`dmaga/` holds collection, RPC, parsing, venue attribution and PnL modules. `scripts/` contains collection, normalization, reconciliation, derived analyses and report generation. `tests/` contains offline parser and accounting tests. `etude_final/` is the frozen statistical study and **must not be rewritten to obtain a preferred result**. The earlier `etude/` is retained as a documented contaminated predecessor, not as the study of record.

With a Python environment containing the project's dependencies, the lightweight tests can be run as:

```bash
python3 -m pytest tests/test_normalize.py tests/test_pnl.py tests/test_db_dedup.py
```

A full replay requires the original raw files and the external volume configured by `DMAGA_EXT`. Follow [state/STATE.md](state/STATE.md) and its disk and memory guards before attempting the resource-intensive `scripts/run_derive.sh`. After re-derivation, the downstream report generators and evidence checks also need to be rerun. **A GitHub clone on its own cannot reproduce the complete study.**

## Data and evidence custody

Small evidence indexes, selected outputs, archived public posts and source manifests are tracked here. Large raw transactions and Parquet datasets remain outside Git, historically under `/Volumes/VERBATIM HD/Dark-MAGA-Investigation/`. The [raw-data manifest](evidence/RAW_MANIFEST.tsv) records their inventory and hashes but is not a substitute for the raw files.

The separate audit reports a single physical copy of part of the raw corpus as of 3 November 2026. GitHub is not a verified second copy of those raw files. Never claim full backup coverage until byte-level restoration and independent-copy checks succeed.

**Evidence standard:** a transaction is not a person; a service label is not a verified customer; a public claim is not an on-chain proof; and absence of statistical significance is not proof of absence.
