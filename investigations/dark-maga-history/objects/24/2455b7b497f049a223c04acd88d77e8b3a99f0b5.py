#!/usr/bin/env python3
"""Découverte des venues : propriétaires qui échangent DMAGA contre autre chose sans jamais signer.

Une adresse est candidate si, dans une même transaction, son solde DMAGA et son solde d'un autre mint
varient en sens opposés, sans qu'elle soit signataire. Une adresse qui signe une seule fois en est exclue
(un trader, pas un pool). Sortie : reports/data_checks/venues.json, relue par dmaga/venues.py.
"""
import gzip
import json
from collections import Counter, defaultdict
from multiprocessing import Pool
from pathlib import Path

from dmaga.config import MINT, RAW
from dmaga.normalize import _keys, token_deltas


def scan(path):
    two_sided = Counter()
    quotes = defaultdict(Counter)
    programs = defaultdict(Counter)
    signers = set()
    with gzip.open(path, "rt") as f:
        for line in f:
            t = json.loads(line)
            if t["meta"].get("err") is not None:
                continue
            msg = t["transaction"]["message"]
            signers.update(k["pubkey"] for k in msg["accountKeys"] if k.get("signer"))
            ds = token_deltas(t, _keys(t))
            by = defaultdict(dict)
            for d in ds:
                by[d["owner"]][d["mint"]] = by[d["owner"]].get(d["mint"], 0) + d["delta"]
            prog = None
            for o, m in by.items():
                dm = m.get(MINT)
                if not dm:
                    continue
                for other, v in m.items():
                    if other != MINT and v and (v > 0) != (dm > 0):
                        two_sided[o] += 1
                        quotes[o][other] += 1
                        if prog is None:
                            prog = {i.get("programId") for i in msg["instructions"]}
                            for inner in t["meta"].get("innerInstructions") or []:
                                prog |= {i.get("programId") for i in inner["instructions"]}
                        programs[o].update(prog)
    return two_sided, {k: dict(v) for k, v in quotes.items()}, {k: dict(v) for k, v in programs.items()}, signers


def main():
    files = [str(p) for lab in ("full_pool", "full_mint") for d in sorted((RAW / lab).glob("t*"))
             for p in sorted(d.glob("p*.jsonl.gz"))] + [str(p) for p in sorted((RAW / "full_curve").glob("p*.jsonl.gz"))]
    two, quotes, progs, signers = Counter(), defaultdict(Counter), defaultdict(Counter), set()
    with Pool(3, maxtasksperchild=20) as pool:
        for a, b, c, s in pool.imap_unordered(scan, files):
            two.update(a)
            signers |= s
            for k, v in b.items():
                quotes[k].update(v)
            for k, v in c.items():
                progs[k].update(v)
    venues = {}
    for o, n in two.most_common():
        if o in signers:
            continue
        p = Counter(progs[o])
        for skip in ("ComputeBudget111111111111111111111111111111", "11111111111111111111111111111111",
                     "TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA", "ATokenGPvbdGVxr1b2hvZbsiqW5xWH25efTNsLJA8knL",
                     "JUP6LkbZbjS1jKKwapdHNy74zcZ3tLUZoi5QNyVTaV4", None):
            p.pop(skip, None)
        venues[o] = {"n_two_sided": n, "quotes": dict(quotes[o].most_common(4)), "programs": dict(p.most_common(4))}
    Path("reports/data_checks").mkdir(parents=True, exist_ok=True)
    Path("reports/data_checks/venues.json").write_text(json.dumps(venues, indent=1))
    print("venues", len(venues), "signataires", len(signers), "fichiers", len(files))
    for o, v in list(venues.items())[:30]:
        print(o, v["n_two_sided"], {k[:6]: n for k, n in v["quotes"].items()}, {k[:8]: n for k, n in v["programs"].items()})


if __name__ == "__main__":
    main()
