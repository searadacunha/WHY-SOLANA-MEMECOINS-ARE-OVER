# forensics_v2 integration audit — 19 November 2026

**Status:** reviewed code port from the author's historic Solana branch; not a fresh independently reproduced historical-chain investigation. The original branch PR #3 was based on an obsolete main and included a root README addition that the current publication policy forbids. This integration takes only new `forensics_v2/` files from the pinned original source SHA `b75424bc46e1001a9018509d54bd7cc8275428f4`, leaves the current four shared publication/protection files untouched, and does not change the root README.

## Scope
- **110** previously absent source-branch blobs, with two limited documentation/regression replacements for the current main integration. New engine modules decode Solana integer balance deltas, trace multi-hop paths with stop reasons, provide retry/budget-aware RPC reads, reconcile local DuckDB tables and classify cross-chain proofs.
- Base main revision: `94f1c584659251e77195eaf1657a1305dc887c68`. No other root code, frozen data, prior financial result or accepted README changed.
- `tests/test_integrity.py` now checks the **actual accepted README and baseline** rather than falsely forbidding future unrelated research commits by comparing the whole repository against an obsolete 4 November commit.
- `forensics_v2/README.md` was corrected solely to accurately state that this current-main port does **not** modify the root README.
- The branch's `PROJECT_STATE.md` is an **archived 3 November checkpoint**, not a 19 November claim of fresh testing or live operation. Its private `private_trades/` directory is ignored and not published.

## Evidence and validation
Source-branch reports contain prior cached wallet/transaction comparisons, with their evidence links and stops. Those results remain separately traceable. Passing unit tests demonstrates decoder/store/trace invariants, **not** that every historical RPC read is complete, a profitable trade exists or a common human owner is identified. Third-party tooling is discussed in an attributed methods audit; no third-party source code imported here.

Reproduce locally in a clean checkout:

```bash
python3 -m pip install -r forensics_v2/requirements.txt
python3 -m pytest -q forensics_v2/tests
python3 code/check_no_secrets.py --require-clean
```

On GitHub, the new `forensics-v2-regression` job executes this test suite with Python 3.12 and pinned DuckDB/pytest. The previously merged publication guard and main regression checks run separately.

## Research limits
The personal trading ledger, original full RPC caches and external disk archives are not published. A chain replay against an independent archive remains necessary for complete claims. The historic branch's known incomplete co-signer findings and negative post-detection economic results are not upgraded to validated positives by this integration. No real-world person is identified solely from a funding graph.

Original PR #3 may be closed as superseded **only after** this re-based integration passes CI and is merged.
