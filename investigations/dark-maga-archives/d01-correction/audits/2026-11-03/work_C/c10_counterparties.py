#!/usr/bin/env python3
"""Nature des contreparties SOL de chaque graine, depuis le brut telecharge.
Pour chaque contrepartie : etiquette publique, compte de jetons de la graine (ATA) ou non, programme proprietaire deduit.
Ecrit work_C/counterparties.csv.
"""
import csv
import gzip
import json
from collections import defaultdict
from pathlib import Path

from dmaga.labels import label

SEEDS = ["8YLEuUtZ4eFMJbf46oNb1CeG6dYFWGyxnQSh9hrgzBzR", "5QhJJcFZu2ashyKyWSTGHcsyo6ZBCbpVuJqeutvQHScd",
         "G41vRrsHShLEvwMj58ruhqJycGfAtWXxtLD56uFExL8E", "9W9b3zgHH9mCEHDhsdbnbEPHStm9vvXS4aia4DWHBxpL"]
NET = Path("/Volumes/VERBATIM HD/Dark-MAGA-Investigation/audits_work/C/net")
WORK = Path(__file__).resolve().parent


def walk(tx):
    for ins in tx["transaction"]["message"]["instructions"]:
        yield ins
    for grp in tx["meta"].get("innerInstructions") or []:
        for ins in grp["instructions"]:
            yield ins


w = csv.writer(open(WORK / "counterparties.csv", "w", newline=""))
w.writerow("seed counterparty dir n lamports label ata_of_seed ata_mint escrow_like first last".split())
for seed in SEEDS:
    ata_of = {}  # compte -> mint, pour les comptes crees/possedes par la graine
    stats = defaultdict(lambda: {"in": [0, 0, None, None], "out": [0, 0, None, None]})
    for line in gzip.open(NET / f"{seed}.jsonl.gz", "rt"):
        tx = json.loads(line)
        keys = [k["pubkey"] for k in tx["transaction"]["message"]["accountKeys"]]
        for side in ("preTokenBalances", "postTokenBalances"):
            for b in tx["meta"].get(side) or []:
                if b.get("owner") == seed:
                    ata_of[keys[b["accountIndex"]]] = b["mint"]
        for ins in walk(tx):
            p = ins.get("parsed")
            if not isinstance(p, dict):
                continue
            info = p.get("info") if isinstance(p.get("info"), dict) else {}
            if ins.get("program") == "spl-associated-token-account" and info.get("wallet") == seed:
                ata_of[info.get("account")] = info.get("mint")
            if ins.get("program") == "system" and p.get("type") in ("transfer", "createAccount"):
                src, dst = info.get("source"), info.get("destination") or info.get("newAccount")
                amt = int(info.get("lamports") or 0)
                for d, cp in (("in", src) if dst == seed else (None, None), ("out", dst) if src == seed else (None, None)):
                    if d:
                        s = stats[cp][d]
                        s[0] += 1
                        s[1] += amt
                        s[2] = s[2] or tx["blockTime"]
                        s[3] = tx["blockTime"]
    for cp, st in stats.items():
        for d in ("in", "out"):
            s = st[d]
            if s[0]:
                w.writerow([seed, cp, d, s[0], s[1], label(cp) or "", cp in ata_of, ata_of.get(cp, ""), "", s[2], s[3]])
