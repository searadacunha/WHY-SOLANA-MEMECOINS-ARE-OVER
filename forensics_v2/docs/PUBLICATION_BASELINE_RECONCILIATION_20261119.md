# Main-branch publication baseline reconciliation — 19 November 2026

**Purpose:** repair a stale guard anchor without changing or weakening any published README, frozen protocol, historical evidence, or negative finding.

## Audited difference

- Original protected main anchor: `0d8c251cc724673c3df402f4b2dcb57635de6570`
- Previously published and CI-green current main: `29099b8d2ce7de4d3708c024baaa52e0c68d18e5`
- Original root README blob: `c0e09713c5a7cf9b34a28e806bb0bdd7cc513d53`
- Accepted root README blob: `bb1b854f0fc15768b66d2c5d9685be5cf90b8316`
- GitHub comparison: https://github.com/searadacunha/WHY-SOLANA-MEMECOINS-ARE-OVER/compare/0d8c251cc724673c3df402f4b2dcb57635de6570...29099b8d2ce7de4d3708c024baaa52e0c68d18e5
- Comparison returns nine commits and **one protected README file changed**: root `README.md`, with **two added lines** inserting `assets/readme-hero-photo.jpg`. No deletions or other README changes are reported by this comparison.
- The accepted `main` root README contents are *unchanged by this PR*. This is not permission to rewrite any report, statistical outcome, or personal trading claim.

## Correction and security invariants

The old `forensics_v2/publication_policy.json` baseline pointed to an ancestor that predated an image already accepted on `main`. Thus **every unrelated additive research PR was blocked** as if it had changed the README. Set only the `main` baseline to the audited published `main` commit above; **the `forensics-v2` and `ansem-network` anchors remain unchanged**.

The existing guard still requires:
1. Candidate has the pinned baseline as an ancestor.
2. Every README existing in the new accepted baseline retains exactly the same Git blob, path, kind and mode.
3. Missing policy or missing baseline fails closed.
4. A PR from before the accepted state is rejected, even if merging might hide the stale head.
5. Added investigation READMEs are allowed; pre-existing READMEs may not be edited, deleted, renamed or chmodded.

This correction **does not retroactively validate** analyses in outstanding Solana PRs. Review each PR and require its own CI; the root README change in historical PR #3 remains disallowed and requires separate explicit resolution. The correction must first pass the existing publication-guard test suite and main CI on its own PR, then may be merged without unrelated code changes.

No existing README, raw dataset, frozen result or original historical commit is modified here.
