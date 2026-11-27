#!/usr/bin/env python3
"""Flux d'un wallet : financement avant le premier achat, jetons DMAGA, sorties après la première vente.

Un fichier gz par couple (wallet, requête), écrit une fois terminé : une reprise saute ce qui existe.
Chaque requête note si elle a été tronquée par son plafond de pages : jamais de « aucun lien » muet.
usage: col_30_flows.py <fichier d'adresses avec colonnes owner,t_first_buy,t_first_sell | --from-wallets N>
"""
import gzip
import json
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from dmaga.collect import logger
from dmaga.config import BIG, MINT, RAW
from dmaga.helius import Helius

NATIVE = "So11111111111111111111111111111111111111111"
USDC = "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"
USDT = "Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB"
OUT = RAW / "flows"


def transfers(h: Helius, addr: str, cfg: dict, cap: int) -> tuple[list, bool]:
    rows, tok = [], None
    for _ in range(cap):
        c = dict(cfg, limit=100)
        if tok:
            c["paginationToken"] = tok
        res = h.call("getTransfersByAddress", [addr, c])
        rows.extend(res["data"])
        tok = res.get("paginationToken")
        if not tok:
            return rows, False
    return rows, True  # plafond atteint : tronqué


def queries(t_buy: int | None, t_sell: int | None) -> dict:
    ref = t_buy or t_sell
    q = {
        "first_in": ({"direction": "in", "mint": NATIVE, "sortOrder": "asc"}, 1),
        "dmaga_all": ({"mint": MINT, "sortOrder": "asc"}, 60),
    }
    if ref:
        q["in_before"] = ({"direction": "in", "mint": NATIVE, "sortOrder": "desc",
                           "filters": {"blockTime": {"lt": ref}, "amount": {"gte": 10_000_000}}}, 4)
    if t_sell:
        base = {"direction": "out", "sortOrder": "asc"}
        q["sol_out_after"] = ({**base, "mint": NATIVE,
                               "filters": {"blockTime": {"gte": t_sell}, "amount": {"gte": 100_000_000}}}, 25)
        q["usdc_out_after"] = ({**base, "mint": USDC,
                                "filters": {"blockTime": {"gte": t_sell}, "amount": {"gte": 100_000_000}}}, 6)
        q["usdt_out_after"] = ({**base, "mint": USDT,
                                "filters": {"blockTime": {"gte": t_sell}, "amount": {"gte": 100_000_000}}}, 6)
    return q


def run_one(h: Helius, owner: str, t_buy, t_sell, log) -> int:
    d = OUT / owner
    d.mkdir(parents=True, exist_ok=True)
    n = 0
    for name, (cfg, cap) in queries(t_buy, t_sell).items():
        path = d / f"{name}.json.gz"
        if path.exists():
            continue
        rows, trunc = transfers(h, owner, cfg, cap)
        blob = json.dumps({"owner": owner, "query": name, "cfg": cfg, "truncated": trunc, "rows": rows})
        tmp = path.with_suffix(".tmp")
        tmp.write_bytes(gzip.compress(blob.encode(), 6))
        tmp.replace(path)
        n += len(rows)
    path = d / "age.json.gz"
    if not path.exists():
        res = h.txs_page(owner, details="signatures", sort="asc", limit=1)
        first = res["data"][0] if res["data"] else None
        cnt = h.txs_page(owner, details="signatures", sort="desc", limit=1000)
        tmp = path.with_suffix(".tmp")
        tmp.write_bytes(gzip.compress(json.dumps({"first": first, "recent_page": len(cnt["data"]),
                                                  "more": bool(cnt.get("paginationToken"))}).encode()))
        tmp.replace(path)
    return n


def main():
    import pyarrow.parquet as pq
    h = Helius(rps=float(sys.argv[3]) if len(sys.argv) > 3 else 4, timeout=120)
    log = logger("col_30_flows")
    rows = []
    src = sys.argv[1]
    for line in Path(src).read_text().splitlines():
        if not line.strip() or line.startswith("#"):
            continue
        p = line.split(",")
        rows.append((p[0], int(p[1]) if len(p) > 1 and p[1] else None, int(p[2]) if len(p) > 2 and p[2] else None))
    failures = []

    def job(r):
        try:
            return r[0], run_one(h, r[0], r[1], r[2], log)
        except Exception as e:  # le wallet reste à refaire, l'échec est journalisé et compté
            failures.append(r[0])
            log(f"ECHEC {r[0]}: {e!r}")
            return r[0], -1

    workers = int(sys.argv[2]) if len(sys.argv) > 2 else 4
    with ThreadPoolExecutor(workers) as ex:
        for i, (o, n) in enumerate(ex.map(job, rows), 1):
            if i % 10 == 0 or i == len(rows):
                log(f"{i}/{len(rows)} dernier={o} n={n} echecs={len(failures)} {dict(h.stats)}")
    log(f"FIN wallets={len(rows)} echecs={failures}")


if __name__ == "__main__":
    main()
