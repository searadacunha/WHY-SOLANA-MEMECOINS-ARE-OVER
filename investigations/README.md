# Solana case investigations

This is the companion investigation section of [Why Solana Memecoins Are Over](../README.md).

## Dark MAGA — Event-driven on-chain investigation

The companion case study follows the July 2024 $DMAGA launch on Solana, early accumulation, wallet funding, realized trading PnL, public-event chronology and cross-chain exits through Ethereum, Base and BSC.

It combines transaction-level reconstruction, transfer-defined wallet networks, matched bridge receipts, archived public sources and statistical controls. Documented financial relationships do not by themselves establish common ownership, coordination with a public figure or access to non-public information.

[Read the full DARK-MAGA investigation](dark-maga/README.md) · [Trading ledger](dark-maga/reports/TOP_TRADERS.md) · [Wallet networks](dark-maga/reports/COORDINATION.md) · [Cross-chain evidence](dark-maga/investigations/2026-11-06_debridge_base_bsc_solana/FINDINGS.md) · [Reproduction guide](dark-maga/docs/REPRODUCTION.md)

The case study retains its original directory structure and licenses. Public transaction evidence is retained; potential credentials and local paths in historical material are redacted. See the [migration manifest](MIGRATION_MANIFEST.json) for file-level before/after hashes. Its published main-branch snapshot is integrated under `investigations/dark-maga/` (source commit `15d6abcfe5b0ee708a653bd675eca15bd58e0059`). Run its tools from that directory; some full reproductions still require the external raw-data archives described in its documentation.

Two distinct historical research snapshots are preserved separately: [audit branch](dark-maga-archives/audit-2026-11-03/README.md) (source commit `b6e8cbd20dedf67e0f6ff56410d76ba576ed93ee`) and [D01 correction branch](dark-maga-archives/d01-correction/README.md) (source commit `6143964e532cb60a7d3938a1f4d175ada895b00c`). They are archived research versions, not silently merged findings. Their original branch-history-dependent checks require the source Git history.


## Historical branches and commit graph

[Full historical archive](dark-maga-history/README.md), including source branch refs, commit ancestry and historical file versions. The active investigation remains the authoritative publication.

## Migration verification — 2026-11-27

The source main tree (`7dade3768901c6893453639ce9b5e9b426fc1732`) was compared recursively with the integrated investigation at Solana commit `d2ddb65f2bd8c607e33edba2cdd19e5671077bf0`.

- All 10,659 source file paths are present; 10,640 have identical Git blob IDs and modes. No source file paths are missing.
- The 19 differences comprise 17 documented publication-redaction files, one checksum-test adaptation and one edited README. The original README is retained in the historical archive as blob `1aa252b2178c1b9b154b82928e639e336f2ed4b2`.
- All 47 live source branch heads match the archived [ref inventory](dark-maga-history/refs.json). The [archive summary](dark-maga-history/summary.json) records 239 commits and 11,461 distinct historical blobs. This is a sanitized reconstruction archive, not a byte-identical Git mirror.
- The archived GitHub metadata contains 40 pull requests, three issues and six issue comments. No source releases or open pull requests were returned by the API at verification time.

No original sensitive values are republished. Before permanently deleting the original repository, preserve an encrypted or otherwise access-restricted original Git mirror or bundle if byte-exact history is required. Untracked local files, external raw-data archives, and GitHub review events or other metadata not covered by the archive cannot be certified as transferred. This verification compares Git tree identities and branch refs; it does not constitute a new execution of the research test suites.
