# Lead 5: `BY4StcU9` is a service by the plan's test

Follow-up of 13 November 2026, after the report. Lead 5 of [TOP10.md](TOP10.md) asks whether `BY4StcU9Y2BpgH8quZzorg31EGE4L1rjomN8FNsCBEcx` is a service or a link. It is the deployer's first funder (20 April 2026, 13:00:49 UTC, [REPORT.md](REPORT.md)), and the August note ends 12 of 15 funding chains of the 13:58:54 group on it. Item 13 of [AMENDMENTS.md](AMENDMENTS.md) left its classification to the author.

**Short answer: when it funded the deployer, `BY4StcU9` passed the plan's own service test, with 574 distinct wallet counterparties in its 1,000 transactions up to that second. Under the plan it is a stop point, so that funding ties the deployer to no one. This says nothing about who runs it.**

## The test

[PLAN.md](PLAN.md), "What does not count as a link": an address shows service behaviour with at least 500 distinct counterparties in a sample of 1,000 transactions. The samples and a first counting rule were committed in `code/ana_70_by4_service.py` (e41244d) before any transaction was read. After the samples were collected and before any count was computed, a review found ways that rule could inflate the count, so a strict rule and a three-way verdict were added (2135b2a). The first rule's count is kept below.

- **Sample A** decides lead 5: the 1,000 successful transactions of `BY4StcU9` up to the end of the second of the funding. The cut is the first block after 13:00:49 UTC on 20 April (slot 414479402, 13:00:50). 8 failed transactions in that range were passed over.
- **Sample B** is context: its 1,000 most recent successful transactions, read on 13 November 2026.
- **Strict counterparty**: a wallet (a key on the ed25519 curve, not a token account, a nonce account or a program-derived address) on the other side of a token transfer that `BY4StcU9` signed with a non-zero amount, or of a system transfer of at least 0.01 SOL read from an instruction. Dust under 0.01 SOL counts only for a wallet seen in at least three transactions, as the plan allows.
- **Verdict**: service when the strict count reaches 500, not a service when the broadest count stays under 500, inconclusive in between.

## Results

| | A: up to the funding of the deployer | B: most recent |
|---|---|---|
| Window, UTC | 2026-04-19 23:11:31 to 2026-04-20 13:00:49 | 2026-09-19 17:08:48 to 2026-11-01 06:57:28 |
| Transactions per day | 1,736.4 | 23.5 |
| Strict counterparties | **574** (500 it pays, 73 that pay it) | **979** (977 it pays, 2 that pay it) |
| Strict, with the 8 failed transactions inside the 1,000 | 571 or more | no failed transaction |
| First rule / broadest count | 576 / 596 | 980 / 996 |
| **Plan's test** | **service** | **service** |
| Strict counterparties seen in one transaction only | 489 of 574 | 979 of 979 |
| Signed by `BY4StcU9`, which also pays the fee | 763 | 977 |
| Opened by a durable nonce | 959, authority `38QU8LKVK1Ew5uzsqttamNTTFxvnfzgi2ACQvj3ekuom` in 958 | 978, authority `EtKfYWHXTRUJVovWWgGvpWR8XK9dVfC6RUe7bxWi3Y9W` in 977 |
| SOL sent / received | 15,675.0 / 12,059.0 | 1.1 / 1.4 |
| Token transfers sent, five most sent mints | 334 | 977, in three mints |

- The funding of the deployer is in sample A: `4bv34kJFT2BnsvW7sbCRNPS59Y6Ggjj6REQdpQLZ1DYQh6Zw9AtXoWPoQVBZxQRemDoTt3QyuFSrXfxdAK5Nu7Z7`, 4.431561 SOL at 13:00:49, the only SOL edge to the deployer in the sample.
- Exploratory (X), outside the plan, with its reading fixed before the counts: in sample A, 169 of the 276 wallets paid 0.01 SOL or more held no lamports before, and the largest of 73 SOL senders gave 34.1% of the SOL received. The reading needs both a majority of empty recipients and one sender above half to favour a single operator's distribution wallet. Only the first holds, so this fits a shared service at least as well.
- Mints, amounts and the nonce authorities are in `evidence/lead5_by4.json`. Counterparties are not named there; they are in the raw transactions.

## What it changes

- For the window of the funding, item 13 of AMENDMENTS.md has an answer: `BY4StcU9` is a service by the plan's test, so tracing stops there, and the plan says a shared funder at a service is not R5. Its 4.43 SOL to the deployer is not a link.
- The 12 funding chains of the August note that end on it were not re-read, and their dates are outside both samples. Both samples pass, five months apart, with durable nonces under a different authority in each, but the months between were not sampled.
- [REPORT.md](REPORT.md) and [WALLETS.csv](WALLETS.csv) give it "248 counterparties in 1,000 transactions on 20 April, under the plan's service test". The probe they cite (`evidence/followups.json`, `coverage_probes`) holds 346 transactions between 10:03:48 and 15:14:01 UTC, not 1,000. On the 1,000 transactions of sample A the test passes. Flagged here, not corrected there.

## Limits

- The test reads behaviour, not ownership. It cannot see who runs `BY4StcU9`, and a stop point is not proof that the deployer and the 13:58:54 group have different owners. The August notes' "HTX" label is not checked here.
- One operator funding many fresh wallets also reaches many counterparties. The plan counts the address as a service anyway; the exploratory figures above are the only check against that, and they decide nothing.
- Durable nonces let a transaction be signed ahead and sent later, a common design for custody and exchange withdrawals. Scripts use them too.
- One sample per period. Sample B depends on the day it was read: if `BY4StcU9` becomes active again, a new run selects other transactions.
- Reads went through the public RPC `api.mainnet-beta.solana.com`, apart from a few through a Helius key of the research pool before its quota ran out. The credit count of `RUN_MANIFEST.json` is unchanged.

## Check it

Offline, from the repository root:

```bash
python investigations/ansem_network/code/ana_70_by4_service.py   # rebuilds evidence/lead5_by4.json
python -m pytest investigations/ansem_network/tests/test_lead5_by4.py -q
```

Raw data: `evidence/raw/lead5_by4_sigs.json.gz` (the anchor and both samples) and `evidence/raw/lead5_by4_txs.json.gz` (2,000 transactions in the "json" encoding), with their sha256 in `evidence/lead5_by4.json`. Rebuilding them from the chain takes about 2,000 calls: `python investigations/ansem_network/code/col_12_by4_windows.py` (no key; `LEAD5_CHECKPOINT` resumes an interrupted run).
