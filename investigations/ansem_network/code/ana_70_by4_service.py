"""Lead 5 of TOP10.md: the plan's service test on BY4StcU9, rebuilt from the saved raw transactions. No network.

PLAN.md ("What does not count as a link"): an address shows service behaviour when its own history has at least 500
distinct counterparties in a sample of 1,000 transactions. Fixed in this file before either sample was read:
- sample A: the 1,000 successful transactions of BY4StcU9 up to its first funding of the deployer (20 April 2026,
  13:00:49 UTC, REPORT.md). Sample B: its 1,000 most recent successful transactions. Both read by col_12_by4_windows.py.
- counterparty: an owner other than BY4StcU9 on the other side of a token transfer it sends or receives, or of a SOL
  edge of forensics_v2/decode.py of at least 0.01 SOL, the plan's dust limit. Being a fee payer or a co-signer does not
  make an address a counterparty, and invoked programs are never counted. The count that adds smaller SOL edges is
  written beside it and decides nothing.
- verdict: service by the plan's test at 500 or more, otherwise not a service by this test.
Writes evidence/lead5_by4.json.
"""
from __future__ import annotations

import gzip
import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any

from lib import OUT, save_json, utc

from forensics_v2 import decode as D

BY4 = "BY4StcU9Y2BpgH8quZzorg31EGE4L1rjomN8FNsCBEcx"
DEPLOYER = "yHCxHBEaJW5tbndqC8JciSThr7U1cqLpdcsvHcx6PRe"
DUST = 10_000_000  # lamports, 0.01 SOL (PLAN.md)
SERVICE = 500
SYSTEM = "11111111111111111111111111111111"
ADVANCE_NONCE = (4).to_bytes(4, "little")  # system instruction 4
SIGS = OUT / "raw" / "lead5_by4_sigs.json.gz"
TXS = OUT / "raw" / "lead5_by4_txs.json.gz"


def load(p: Path) -> Any:
    return json.loads(gzip.decompress(p.read_bytes()))


def nonce_authority(tx: dict[str, Any], keys: list[str]) -> str | None:
    """Authority of an AdvanceNonceAccount that opens the transaction: it was signed ahead with a durable nonce."""
    ix = tx["transaction"]["message"]["instructions"][0]
    if keys[ix["programIdIndex"]] == SYSTEM and D.b58decode(ix.get("data") or "")[:4] == ADVANCE_NONCE:
        return keys[ix["accounts"][2]]
    return None


def sample(sigs: list[str], txs: dict[str, Any]) -> dict[str, Any]:
    full: Counter[str] = Counter()     # counterparties of the decision, by number of transactions
    small: set[str] = set()            # seen only through SOL edges under the dust limit
    authorities: Counter[str] = Counter()
    cosigners: Counter[str] = Counter()
    mints: dict[str, dict[str, Any]] = {}
    times, signed, payer, sent_sol, got_sol, funding, to_deployer, no_owner = [], 0, 0, 0, 0, None, 0, 0
    for s in sigs:
        tx = txs[s]
        d = D.decode(tx)
        if not d.ok or d.signature != s:
            raise ValueError("unusable transaction in the sample: " + s)
        times.append(d.block_time)
        signed += BY4 in d.signers
        payer += d.fee_payer == BY4
        cosigners.update(x for x in d.signers if x != BY4)
        auth = nonce_authority(tx, d.keys)
        if auth:
            authorities[auth] += 1
        here, dust = set(), set()
        for t in d.transfers:
            if t.kind != "spl" or BY4 not in (t.src_owner, t.dst_owner):
                continue
            other = t.dst_owner if t.src_owner == BY4 else t.src_owner
            if other and other != BY4:
                here.add(other)
            no_owner += not other
            if t.src_owner == BY4 and t.mint:
                dec = (d.token_accounts.get(t.src) or D.TokenAccount(t.mint, None)).decimals or 0
                m = mints.setdefault(t.mint, {"transfers": 0, "min": None, "max": None})
                ui = t.amount / 10 ** dec
                m["transfers"] += 1
                m["min"] = ui if m["min"] is None else min(m["min"], ui)
                m["max"] = ui if m["max"] is None else max(m["max"], ui)
        for e in d.edges:
            if BY4 not in (e.src, e.dst):
                continue
            other = e.dst if e.src == BY4 else e.src
            if e.src == BY4:
                sent_sol += e.lamports
            else:
                got_sol += e.lamports
            if e.src == BY4 and e.dst == DEPLOYER:
                to_deployer += 1
                funding = funding or {"signature": s, "utc": utc(d.block_time), "sol": e.lamports / 1e9}
            (here if e.lamports >= DUST else dust).add(other)
        here -= set(d.programs)
        dust -= here | set(d.programs)
        full.update(here)
        small |= dust
    small -= set(full)
    span = (max(times) - min(times)) / 3600
    out = {
        "transactions": len(sigs),
        "first_utc": utc(min(times)),
        "last_utc": utc(max(times)),
        "span_hours": round(span, 2),
        "per_day": round(len(sigs) / span * 24, 1) if span else None,
        "signed_by_BY4": signed,
        "fee_paid_by_BY4": payer,
        "opened_by_a_durable_nonce": sum(authorities.values()),
        "nonce_authorities": authorities.most_common(3),
        "other_signers": cosigners.most_common(3),
        "counterparties": len(full),
        "counterparties_with_dust_edges": len(full) + len(small),
        "verdict": "service by the plan's test" if len(full) >= SERVICE else "not a service by the plan's test",
        "most_repeated_counterparties": full.most_common(5),
        "sol_sent": round(sent_sol / 1e9, 3),
        "sol_received": round(got_sol / 1e9, 3),
        "mints_sent": sorted(({"mint": k, **v} for k, v in mints.items()), key=lambda r: -r["transfers"])[:5],
        "token_transfers_with_no_known_owner": no_owner,
        "sol_edges_to_the_deployer": to_deployer,
    }
    if funding:
        out["latest_funding_of_the_deployer"] = funding
    return out


def build() -> dict[str, Any]:
    sigs, txs = load(SIGS), load(TXS)
    return {
        "test": "PLAN.md: at least 500 distinct counterparties in a sample of 1,000 transactions. Definitions in code/ana_70_by4_service.py",
        "address": BY4,
        "raw_sha256": {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in (SIGS, TXS)},
        "anchor_of_sample_A": sigs["anchor"],
        "A_up_to_the_funding_of_the_deployer": {"failed_skipped": sigs["A"]["failed_skipped"], **sample(sigs["A"]["signatures"], txs)},
        "B_most_recent": {"failed_skipped": sigs["B"]["failed_skipped"], **sample(sigs["B"]["signatures"], txs)},
    }


if __name__ == "__main__":
    res = build()
    save_json("lead5_by4.json", res)
    for k in ("A_up_to_the_funding_of_the_deployer", "B_most_recent"):
        r = res[k]
        print(k, r["first_utc"], "to", r["last_utc"], "|", r["counterparties"], "counterparties ->", r["verdict"])
