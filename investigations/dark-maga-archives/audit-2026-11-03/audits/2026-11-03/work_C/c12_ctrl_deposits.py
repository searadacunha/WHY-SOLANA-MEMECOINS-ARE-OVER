#!/usr/bin/env python3
"""Temoin : population d'adresses qui balaient vers les hot wallets Coinbase publics (Dune), hors enquete.
Etape 1 (sample) : lit quelques pages des 3 hot wallets sur des fenetres fixes, garde les expediteurs X dont la transaction
  ne contient qu'un virement systeme vers le hot wallet, signee par X seul. Ecrit ctrl_candidates.csv.
Etape 2 (fetch) : tire N adresses au hasard (graine fixe), telecharge jusqu'a 3 pages (100 tx) de chaque, un seul fichier gz.
  Budget compte dans credits.csv.
"""
import csv
import gzip
import json
import random
import sys
import time
from pathlib import Path

from dmaga.helius import Helius

WORK = Path(__file__).resolve().parent
NET = Path("/Volumes/VERBATIM HD/Dark-MAGA-Investigation/audits_work/C/net")
CRED = WORK / "credits.csv"
HOT = ["H8sMJSCQxfKiFTCfDR3DUMLPwcRbM61LGFJ8N4dK3WjS", "2AQdpHJ2JpcEgPiATUXjQxA8QmafFegfQwSLWSprPicm", "GJRs4FwHtemZ5ZE9x3FNvJ8TMwitKTh21yxdRPqn7npE"]
# fenetres fixes, choisies avant de regarder : debut de chaque mois de juin a octobre 2024 (periode d'activite de 9W9b)
WINDOWS = [1717200000, 1719792000, 1722470400, 1725148800, 1727740800]


def note(method, addr):
    with open(CRED, "a") as f:
        f.write(f"{time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())},{method},{addr},10\n")


def used():
    return sum(int(l.split(",")[3]) for l in CRED.read_text().splitlines()[1:] if l.strip())


def sample():
    h = Helius()
    seen = {}
    w = csv.writer(open(WORK / "ctrl_candidates.csv", "w", newline=""))
    w.writerow("x hot sig bt lamports fee".split())
    for hot in HOT:
        for t0 in WINDOWS:
            tok = None
            for _ in range(2):  # 2 pages par fenetre et par hot wallet
                r = h.txs_page(hot, details="full", limit=100, sort="asc", token=tok,
                               filters={"blockTime": {"gte": t0, "lt": t0 + 86400}, "status": "succeeded"})
                note("gtfa_full", hot)
                for tx in r["data"]:
                    msg = tx["transaction"]["message"]
                    signers = [k["pubkey"] for k in msg["accountKeys"] if k["signer"]]
                    progs = {i["programId"] for i in msg["instructions"]}
                    if len(signers) != 1 or signers[0] == hot:
                        continue
                    if progs - {"11111111111111111111111111111111", "ComputeBudget111111111111111111111111111111"}:
                        continue
                    for i in msg["instructions"]:
                        p = i.get("parsed")
                        if i.get("program") == "system" and isinstance(p, dict) and p.get("type") == "transfer" and p["info"].get("destination") == hot and p["info"].get("source") == signers[0]:
                            x = signers[0]
                            w.writerow([x, hot, tx["transaction"]["signatures"][0], tx["blockTime"], p["info"]["lamports"], tx["meta"]["fee"]])
                            seen[x] = seen.get(x, 0) + 1
                tok = r.get("paginationToken")
                if not tok:
                    break
    print("candidats uniques", len(seen), "credits", used(), dict(h.stats), flush=True)


def fetch(n):
    h = Helius()
    rows = list(csv.DictReader(open(WORK / "ctrl_candidates.csv")))
    xs = sorted({r["x"] for r in rows})
    random.Random(20261103).shuffle(xs)
    xs = xs[:n]
    NET.mkdir(parents=True, exist_ok=True)
    raw = gzip.open(NET / "ctrl_deposits.jsonl.gz", "at", compresslevel=6)
    w = csv.writer(open(WORK / "ctrl_sampled.csv", "w", newline=""))
    w.writerow("x n_tx complete pages".split())
    for x in xs:
        tok, n_tx, pages = None, 0, 0
        while pages < 3:
            assert used() + 10 <= 20000, "budget"
            r = h.txs_page(x, details="full", limit=100, sort="asc", token=tok, filters={"status": "succeeded"})
            note("gtfa_full", x)
            pages += 1
            for tx in r["data"]:
                raw.write(json.dumps({"x": x, "tx": tx}, separators=(",", ":")) + "\n")
            n_tx += len(r["data"])
            tok = r.get("paginationToken")
            if not tok:
                break
        w.writerow([x, n_tx, not tok, pages])
    raw.close()
    print("echantillon", len(xs), "credits", used(), dict(h.stats), flush=True)


if __name__ == "__main__":
    if sys.argv[1] == "sample":
        sample()
    else:
        fetch(int(sys.argv[2]))
