"""Lead 5 of TOP10.md: the two samples of 1,000 BY4StcU9 transactions that ana_70_by4_service.py reads. Public RPC, no key.

Sample A ends at its first funding of the deployer (REPORT.md: 20 April 2026, 13:00:49 UTC). Its anchor is the first
signature of the first block after that second, found by a search on block times, and the sample is the 1,000
successful transactions of BY4StcU9 before that anchor. Sample B is its 1,000 most recent successful transactions.
Transactions are read in the "json" encoding that forensics_v2/decode.py expects. Every transaction read is appended
to a checkpoint (LEAD5_CHECKPOINT, default in the system temp folder), so an interrupted run resumes. An RPC error or
an empty answer stops the run: nothing is written as empty.
Writes evidence/raw/lead5_by4_sigs.json.gz and evidence/raw/lead5_by4_txs.json.gz.
"""
from __future__ import annotations

import json
import os
import tempfile
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

from lib import save_gz

RPC = os.environ.get("SOLANA_RPC", "https://api.mainnet-beta.solana.com")
BY4 = "BY4StcU9Y2BpgH8quZzorg31EGE4L1rjomN8FNsCBEcx"
FUNDING_TS = 1776690049  # 2026-04-20 13:00:49 UTC
N = 1000
SKIPPED = (-32004, -32007, -32009)  # no block at this slot, or not in long-term storage
CHECKPOINT = Path(os.environ.get("LEAD5_CHECKPOINT", str(Path(tempfile.gettempdir()) / "lead5_by4.jsonl")))
PACE = float(os.environ.get("LEAD5_PACE", "0.95"))  # seconds between calls: the public RPC served about 11 getTransaction per 10 s


class Skipped(Exception):
    pass


def call(method: str, params: list[Any]) -> Any:
    body = json.dumps({"jsonrpc": "2.0", "id": 1, "method": method, "params": params}).encode()
    for attempt in range(8):
        time.sleep(PACE)
        req = urllib.request.Request(RPC, data=body, headers={"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"})
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                out = json.loads(r.read())
        except urllib.error.HTTPError as e:
            if e.code not in (429, 500, 502, 503, 504):
                raise
            wait = e.headers.get("Retry-After") if e.code == 429 else None  # the public RPC asks for 10 s
            time.sleep(float(wait) if wait and wait.isdigit() else min(60, 2 ** attempt))
            continue
        except (urllib.error.URLError, TimeoutError, ConnectionError):
            time.sleep(min(60, 2 ** attempt))
            continue
        if "error" in out:
            if out["error"].get("code") in SKIPPED:
                raise Skipped(method)
            raise RuntimeError("%s: %s" % (method, out["error"]))
        return out["result"]
    raise RuntimeError(method + ": no answer after 8 tries")


def first_block(slot: int) -> tuple[int, int]:
    """(slot, block time) of the first produced block at or after this slot."""
    for s in range(slot, slot + 500):
        try:
            t = call("getBlockTime", [s])
        except Skipped:
            continue
        if t is not None:
            return s, int(t)
    raise RuntimeError("no block in 500 slots after %d" % slot)


def anchor() -> dict[str, Any]:
    hi = int(call("getSlot", [{"commitment": "finalized"}]))
    lo = hi - 80_000_000
    if first_block(lo)[1] > FUNDING_TS:
        raise RuntimeError("the search starts after the funding")
    while hi - lo > 1:  # smallest slot whose first block is after the funding second
        mid = (lo + hi) // 2
        if first_block(mid)[1] > FUNDING_TS:
            hi = mid
        else:
            lo = mid
    slot, t = first_block(hi)
    while True:
        block = call("getBlock", [slot, {"encoding": "json", "transactionDetails": "signatures", "rewards": False, "maxSupportedTransactionVersion": 0}])
        if block and block.get("signatures"):
            return {"slot": slot, "block_time": t, "signature": block["signatures"][0]}
        slot, t = first_block(slot + 1)


def successes(before: str | None) -> dict[str, Any]:
    """The first N successful signatures of BY4StcU9 before `before` (newest first), and how many failed ones were passed."""
    picked: list[str] = []
    failed = 0
    while len(picked) < N:
        page = call("getSignaturesForAddress", [BY4, {"limit": 1000, **({"before": before} if before else {})}])
        if not page:
            raise RuntimeError("history ends before %d successful transactions" % N)
        for row in page:
            if row.get("err") is None:
                picked.append(row["signature"])
            else:
                failed += 1
            if len(picked) == N:
                break
        before = page[-1]["signature"]
    return {"signatures": picked, "failed_skipped": failed}


def main() -> None:
    plan_path = CHECKPOINT.with_suffix(".sigs.json")
    if plan_path.exists():
        plan = json.loads(plan_path.read_text())
    else:
        a = anchor()
        plan = {"anchor": a, "A": successes(a["signature"]), "B": successes(None)}
        plan_path.write_text(json.dumps(plan))
    have: dict[str, Any] = {}
    if CHECKPOINT.exists():
        lines = CHECKPOINT.read_text().splitlines()
        for i, line in enumerate(lines):
            try:
                row = json.loads(line)
            except ValueError:
                if i < len(lines) - 1:
                    raise
                break  # last line cut by an interrupted run: that transaction is read again
            have[row["sig"]] = row["tx"]
    wanted = list(dict.fromkeys(plan["A"]["signatures"] + plan["B"]["signatures"]))
    todo = [s for s in wanted if s not in have]

    def read(s: str) -> tuple[str, Any]:
        for _ in range(5):  # the public RPC sometimes answers null for a transaction it serves a moment later
            tx = call("getTransaction", [s, {"encoding": "json", "maxSupportedTransactionVersion": 0, "commitment": "confirmed"}])
            if tx:
                return s, tx
            time.sleep(5)
        raise RuntimeError("empty answer for " + s)

    with open(CHECKPOINT, "a") as f:
        for s, tx in map(read, todo):
            have[s] = tx
            f.write(json.dumps({"sig": s, "tx": tx}) + "\n")
            f.flush()
            if len(have) % 100 == 0:
                print("read", len(have), "of", len(wanted), flush=True)
    save_gz("raw/lead5_by4_sigs.json.gz", plan)
    save_gz("raw/lead5_by4_txs.json.gz", have)
    print("anchor", plan["anchor"], "| A failed", plan["A"]["failed_skipped"], "| B failed", plan["B"]["failed_skipped"])


if __name__ == "__main__":
    main()
