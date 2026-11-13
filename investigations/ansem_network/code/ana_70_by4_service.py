"""Lead 5 of TOP10.md: the plan's service test on BY4StcU9, rebuilt from the saved raw transactions. No network.

PLAN.md ("What does not count as a link"): an address shows service behaviour when its own history has at least 500
distinct counterparties in a sample of 1,000 transactions. Fixed before either sample was read (commit e41244d):
- sample A: the 1,000 successful transactions of BY4StcU9 up to the end of the second of its first funding of the
  deployer (20 April 2026, 13:00:49 UTC, REPORT.md). It alone answers lead 5. Sample B, its 1,000 most recent
  successful transactions, is context. Both read by col_12_by4_windows.py.
- first rule: a counterparty is an owner other than BY4StcU9 on the other side of a token transfer it sends or
  receives, or of a SOL edge of forensics_v2/decode.py of at least 0.01 SOL, the plan's dust limit. Invoked programs
  are not counted. Kept and published as first committed.
Amended on 13 November 2026, after the samples were collected and before any count was computed, because a review of
the first rule found ways it could inflate the count and so end tracing at a false service:
- strict rule: only wallets count, that is keys on the ed25519 curve that are not a token account or a nonce account
  (so no program-derived account, pool or vault). Token transfers count only in transactions BY4StcU9 signed, with a
  non-zero amount, and wrapped SOL only from 0.01 SOL. SOL counts only through system transfers of at least 0.01 SOL
  read from an instruction, never through an edge inferred from balances or through an account creation. As the plan
  allows, a wallet seen through smaller system transfers in at least three transactions counts too.
- broad rule: the first rule with its smaller SOL edges, plus every token transfer whose owner is unknown.
- verdict: service by the plan's test when the strict count reaches 500; not a service by the plan's test when the
  broad count stays under 500; inconclusive under the plan's test in between.
Exploratory (X), outside the plan and never changing the verdict: how many SOL recipients (0.01 SOL or more) held no
lamports before the transfer, and how concentrated the SOL senders are. Reading fixed before the counts: more than
half of the recipients empty before, with one sender giving more than half of the SOL received, fits one operator's
distribution wallet better than a shared service; anything else fits a shared service at least as well.
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
REPEAT = 3  # PLAN.md: dust counts when the same pair repeats at least three times
SERVICE = 500
SYSTEM = "11111111111111111111111111111111"
ADVANCE_NONCE = (4).to_bytes(4, "little")  # system instruction 4
SIGS = OUT / "raw" / "lead5_by4_sigs.json.gz"
TXS = OUT / "raw" / "lead5_by4_txs.json.gz"
P = 2 ** 255 - 19
ED_D = -121665 * pow(121666, P - 2, P) % P


def load(p: Path) -> Any:
    return json.loads(gzip.decompress(p.read_bytes()))


def on_curve(addr: str) -> bool:
    """True for a key that can sign (a point of ed25519). Program-derived addresses are made to be off the curve."""
    b = D.b58decode(addr)
    if len(b) != 32:
        return False
    y = int.from_bytes(b, "little") & ((1 << 255) - 1)
    if y >= P:
        return False
    x2 = (y * y - 1) * pow(ED_D * y * y + 1, P - 2, P) % P
    x = pow(x2, (P + 3) // 8, P)
    if (x * x - x2) % P:
        x = x * pow(2, (P - 1) // 4, P) % P
    return (x * x - x2) % P == 0


def nonce_info(tx: dict[str, Any], keys: list[str]) -> tuple[str | None, str | None]:
    """(authority, nonce account) of an AdvanceNonceAccount that opens the transaction: it was signed ahead."""
    ix = tx["transaction"]["message"]["instructions"][0]
    if keys[ix["programIdIndex"]] == SYSTEM and D.b58decode(ix.get("data") or "")[:4] == ADVANCE_NONCE:
        return keys[ix["accounts"][2]], keys[ix["accounts"][0]]
    return None, None


def strict_count(per_tx: list[tuple[set[str], set[str]]]) -> int:
    big: set[str] = set()
    small: Counter[str] = Counter()
    for at_limit, under in per_tx:
        big |= at_limit
        small.update(under)
    return len(big | {a for a, n in small.items() if n >= REPEAT})


def sample(sigs: list[str], txs: dict[str, Any], failed: int) -> dict[str, Any]:
    full: Counter[str] = Counter()     # first rule, by number of transactions
    small: set[str] = set()            # first rule, seen only through SOL edges under the dust limit
    per_tx: list[tuple[set[str], set[str]]] = []  # strict rule: wallets at the limits, wallets only under them
    strict_tx: Counter[str] = Counter()
    sent_to, got_from = set(), set()
    authorities: Counter[str] = Counter()
    cosigners: Counter[str] = Counter()
    mints: dict[str, dict[str, Any]] = {}
    times, signed, payer, sent_sol, got_sol, funding, to_deployer, no_owner = [], 0, 0, 0, 0, None, 0, 0
    recipients, fresh, senders = set(), set(), Counter()  # exploratory (X): service or one operator's wallet?
    for s in sigs:
        tx = txs[s]
        d = D.decode(tx)
        if not d.ok or d.signature != s:
            raise ValueError("unusable transaction in the sample: " + s)
        times.append(d.block_time)
        mine = BY4 in d.signers
        signed += mine
        payer += d.fee_payer == BY4
        cosigners.update(x for x in d.signers if x != BY4)
        auth, nonce_account = nonce_info(tx, d.keys)
        if auth:
            authorities[auth] += 1
        kinds = {t.path: t.kind for t in d.transfers}
        not_wallet = set(d.programs) | set(d.token_accounts) | {BY4, nonce_account}

        def wallet(a: str | None) -> bool:
            return bool(a) and a not in not_wallet and on_curve(a)

        here, dust, at_limit, under = set(), set(), set(), set()
        for t in d.transfers:
            if t.kind != "spl" or BY4 not in (t.src_owner, t.dst_owner):
                continue
            out = t.src_owner == BY4
            other = t.dst_owner if out else t.src_owner
            if other and other != BY4:
                here.add(other)
            no_owner += not other
            if mine and t.amount > 0 and (t.mint != D.WSOL or t.amount >= DUST) and wallet(other):
                at_limit.add(other)
                (sent_to if out else got_from).add(other)
            if out and t.mint:
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
            if e.basis == "instruction" and kinds.get(e.path) == "sol_transfer" and wallet(other):
                if e.lamports >= DUST:
                    at_limit.add(other)
                    (sent_to if e.src == BY4 else got_from).add(other)
                else:
                    under.add(other)
            if e.lamports >= DUST and e.src == BY4:
                recipients.add(e.dst)
                if e.dst in d.keys and tx["meta"]["preBalances"][d.keys.index(e.dst)] == 0:
                    fresh.add(e.dst)
            elif e.lamports >= DUST:
                senders[e.src] += e.lamports
        here -= set(d.programs)
        dust -= here | set(d.programs)
        full.update(here)
        small |= dust
        per_tx.append((at_limit, under - at_limit))
        strict_tx.update(at_limit)
    small -= set(full)
    strict, broad = strict_count(per_tx), len(full) + len(small) + no_owner
    verdict = ("service by the plan's test" if strict >= SERVICE else
               "not a service by the plan's test" if broad < SERVICE else "inconclusive under the plan's test")
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
        "main_other_signer": cosigners.most_common(1),  # the others are not named: few transactions each
        "counterparties_strict": strict,
        "counterparties_strict_sent_to": len(sent_to),
        "counterparties_strict_received_from": len(got_from),
        # failed transactions add no counterparty: with them inside the 1,000, the strict count is at least this
        "counterparties_strict_if_failed_count_in_the_1000": strict_count(per_tx[:len(per_tx) - failed]),
        "counterparties_first_rule": len(full),
        "counterparties_first_rule_with_dust_edges": len(full) + len(small),
        "counterparties_broad": broad,
        "verdict": verdict,
        "verdict_first_rule": "service by the plan's test" if len(full) >= SERVICE else "not a service by the plan's test",
        # counts only: the counterparties themselves stay in the raw file, unnamed here
        "max_transactions_with_one_strict_counterparty": max(strict_tx.values()) if strict_tx else 0,
        "strict_counterparties_in_one_transaction_only": sum(v == 1 for v in strict_tx.values()),
        "sol_sent": round(sent_sol / 1e9, 3),
        "sol_received": round(got_sol / 1e9, 3),
        "mints_sent": sorted(({"mint": k, **v} for k, v in mints.items()), key=lambda r: -r["transfers"])[:5],
        "token_transfers_with_no_known_owner": no_owner,
        "sol_edges_to_the_deployer": to_deployer,
        "exploratory_X": {
            "sol_recipients": len(recipients),
            "sol_recipients_empty_before": len(fresh),
            "sol_senders": len(senders),
            "largest_sender_share_of_sol_received": round(max(senders.values()) / sum(senders.values()), 3) if senders else None,
        },
    }
    if funding:
        out["latest_funding_of_the_deployer"] = funding
    return out


def build() -> dict[str, Any]:
    sigs, txs = load(SIGS), load(TXS)
    res: dict[str, Any] = {
        "test": "PLAN.md: at least 500 distinct counterparties in a sample of 1,000 transactions. Rules in code/ana_70_by4_service.py",
        "address": BY4,
        "raw_sha256": {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in (SIGS, TXS)},
        "anchor_of_sample_A": sigs["anchor"],
    }
    for key, k in (("A_up_to_the_funding_of_the_deployer", "A"), ("B_most_recent", "B")):
        res[key] = {"failed_skipped": sigs[k]["failed_skipped"], **sample(sigs[k]["signatures"], txs, sigs[k]["failed_skipped"])}
    return res


if __name__ == "__main__":
    res = build()
    save_json("lead5_by4.json", res)
    for k in ("A_up_to_the_funding_of_the_deployer", "B_most_recent"):
        r = res[k]
        print(k, r["first_utc"], "to", r["last_utc"], "| strict", r["counterparties_strict"], "broad", r["counterparties_broad"], "->", r["verdict"])
