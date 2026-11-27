# RETIREDIO → DMAGA rotation timing correction (18 November 2026)

**Scope:** Fix future execution of `scripts/h52_rotation.py retiredio`; preserve committed evidence and historical exports. This is an **exploratory** subanalysis, not part of frozen `etude_final/` and not proof of knowledge of Musk's later avatar choice.

## The reproducible defect

The historical screen selected RETIREDIO ATA transactions in `[t_first_DMAGA_buy - 3600 seconds, t_first_DMAGA_buy + 60 seconds]`, then set `rotation=True` whenever the RETIREDIO balance fell.

A record in the published `data/rotation_retiredio.csv` was classified as a rotation despite its only reported negative balance movement being **50 seconds after** DMAGA buy:

- `DpvWg6MaWAN9BTKKPheVTPPSxH7bdZ8ebU4q61Zo7THz`
- First DMAGA buy: 2024-07-21 18:16:23 UTC
- RETIREDIO debit: 2024-07-21 18:17:13 UTC
- Original `sell_to_buy_s=-50` and `rotation=True`

A post-buy debit can never serve as a **pre-buy** feature. The bug is both temporal and terminological: a negative token balance does not automatically establish a market sale.

## Narrow repair

- A pure `in_prebuy_window(t_event, t_buy)` predicate accepts **only** `t_buy - 3600 <= t_event < t_buy`.
- The RETIREDIO scan now excludes the post-buy +60-second look-ahead; the historical KLLARY screen is unchanged.
- An offline regression test checks pre-buy, same-second, post-buy, out-of-window and the archived 50-second counterexample.

This repair enforces **causal ordering** for subsequent replays. It does **not** prove that all remaining qualifying debits were bona fide DEX sells, nor does it adjust the original historical CSV.

## What the old exploratory counts mean

`FINDINGS.md` reports 11/35 event-window buyers with RETIREDIO debits versus 4/149 in the preceding comparison window. At least one of the 11 was a documented post-buy movement, so **11/35 is not a defensible strictly pre-buy event count**. One possible simple correction would be 10/35, but that number **is not published as a validated replacement** until the receipts are re-read under the exact new rule and true sales are separated from transfers. The control counts must also be rechecked.

The sample is small, selection was exploratory, other information was already public on 21 July, and statistical significance does not imply causal knowledge. Do not use this screen as a prediction score or trade signal.

## Reproduction and limitations

With the external full DMAGA archive and an archival-capable Solana RPC configured, run `scripts/h52_rotation.py retiredio` in a **separate output copy**, diff against legacy `rotation_retiredio.csv`, and validate each debit by transaction instruction and SOL/WSOL swap proceeds. Never overwrite original historical tables silently.

Offline regression:

```bash
python3 -I -m unittest discover -s investigations/2026-11-06_historical_replay/tests -p 'test_h52_rotation_point_in_time.py' -v
```

**Dependencies:** standard library only for the timing regression. Complete historical re-execution requires DuckDB, cached transaction files and RPC access.

Issue tracking: [#36](https://github.com/searadacunha/DARK-MAGA/issues/36). Frozen statistical studies, the README and original receipt archive are unchanged.
