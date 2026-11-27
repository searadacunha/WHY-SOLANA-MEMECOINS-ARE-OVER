# Main README publication baseline review — 18 November 2026

**Scope:** Restore the existing main-branch publication gate without changing, reverting, replacing or weakening the current README or any frozen research data.

## Trigger and authorization

The repository owner requested final public-facing preparation of the Dark MAGA investigation on 18 November 2026, with existing title, visuals and evidence preserved. The owner has also previously approved the current public-facing README narrative and its later visual/reader changes. This review documents accepting the **already published** main README as a new fixed baseline, rather than re-authoring it.

## Verified pre-migration state

- Main head inspected: `b583f4c60ae4956b34614b80467a90c00591f10b` (15 November 2026).
- README blob at that head: `da5f60fb37f4cee6df7f0d759bd2dec54ded1bcc` — retains `# Dark MAGA: Did Musk Know?` and the existing `assets/dark-maga-trump-banner.webp` visual.
- Previous `state/publication_baselines.json` for main pins baseline commit `846a0937e6a5d803251de3cec949c5673ca6cbfb` and README blob `6396eedc386ffa4831758ce8d9278dc211629d16`.
- GitHub Actions [run 43691335141](https://github.com/searadacunha/DARK-MAGA/actions/runs/43691335141) fails with `PUBLICATION CHECK FAILED: Committed file changed or deleted: README.md`; downstream guard and test steps are skipped.
- The separately maintained `audit-2026-11-03` target must be left untouched.

## Migration contract

1. Preserve the complete **existing** root README octet-for-octet; never select an old README via bulk merge.
2. Make this dated review a committed parent of the new accepted baseline; then update **only** `targets.main.baseline_commit` to that review commit and **only** `targets.main.readme_blob` to the observed current README blob.
3. Preserve `targets.main.protocol_locks`, the entire `targets.audit-2026-11-03` rule, every source archive, study file, and `scripts/check_publication.py` unchanged.
4. This is an authorized **baseline migration**. The initial policy commit itself cannot be certified by the old policy; this is not a green run and must never be represented as one. The subsequent independent candidate/PR must pass the unchanged guard against the accepted new destination policy.
5. Recheck source-readme blob, parent history, frozen locks, reviewable diffs and the new PR's actual CI. Do not force push, bypass checks, or claim that a GitHub Actions check replaces full raw-data reproduction.

## What is and is not approved

**Approved:** the already-existing root README as a fixed baseline, plus independent additive portfolio-facing documents that state limitations and negative results.  
**Not approved or implied:** unfreezing `etude_final/` or `etude_groupe/`, reconciling `audit-2026-11-03` via an undifferentiated merge, inventing findings, merging unfinished forensic-code changes, weakening publication checks or asserting insider trading.

Issue: [#37 — publication gate restoration](https://github.com/searadacunha/DARK-MAGA/issues/37).
