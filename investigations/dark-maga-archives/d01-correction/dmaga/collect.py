"""Collecte brute paginée, résumable et idempotente.

Chaque page va dans un fichier gz immuable ; le curseur n'avance qu'une fois le fichier écrit et
renommé. Une reprise repart du dernier curseur écrit, une page déjà écrite n'est jamais refaite.
"""
import gzip
import json
import os
import sys
import time
from pathlib import Path

from .config import RAW, LOGS
from .helius import Helius


def _atomic_write(path: Path, data: bytes) -> None:
    tmp = path.with_suffix(path.suffix + ".tmp")
    # pas de fsync : le disque externe partagé le bloque plusieurs minutes (mesuré le 02/11).
    # shortcut: une coupure de courant peut perdre une page, verify() le détecte et la page se recharge.
    with open(tmp, "wb") as f:
        f.write(data)
    os.replace(tmp, path)


def collect(h: Helius, label: str, address: str, *, details="full", sort="asc", filters=None,
            limit=1000, max_pages=None, log=print) -> dict:
    """Parcourt une adresse jusqu'à épuisement. Rend le compte de pages et de transactions."""
    d = RAW / label
    d.mkdir(parents=True, exist_ok=True)
    cur_path = d / "cursor.json"
    st = {"address": address, "details": details, "sort": sort, "filters": filters, "limit": limit,
          "page": 0, "n": 0, "token": None, "complete": False}
    if cur_path.exists():
        old = json.loads(cur_path.read_text())
        for k in ("address", "details", "sort", "filters"):
            if old.get(k) != st[k]:
                raise RuntimeError(f"{label}: curseur incompatible sur {k}: {old.get(k)} != {st[k]}")
        st = old
    if st["complete"]:
        return st
    t0 = time.time()
    pages_now = 0
    while True:
        res = h.txs_page(address, details=details, limit=limit, sort=sort, token=st["token"], filters=filters)
        rows = res.get("data")
        if rows is None:
            raise RuntimeError(f"{label}: réponse sans champ data à la page {st['page']}")
        tok = res.get("paginationToken")
        if rows:
            blob = "\n".join(json.dumps(r, separators=(",", ":")) for r in rows).encode()
            _atomic_write(d / f"p{st['page']:06d}.jsonl.gz", gzip.compress(blob, 6))
        st["n"] += len(rows)
        st["page"] += 1
        st["token"] = tok
        st["complete"] = not tok
        st["ts"] = int(time.time())
        _atomic_write(cur_path, json.dumps(st).encode())
        pages_now += 1
        if pages_now % 10 == 0 or st["complete"]:
            bt = rows[-1].get("blockTime") if rows else None
            log(f"{label}: page {st['page']} n={st['n']} blockTime={bt} {pages_now / (time.time() - t0):.2f} p/s {dict(h.stats)}")
        if st["complete"] or (max_pages and pages_now >= max_pages):
            return st


def verify(label: str) -> dict:
    """Contrôle d'intégrité : chaque page se décompresse et le total égale le curseur."""
    d = RAW / label
    st = json.loads((d / "cursor.json").read_text())
    n = 0
    bad = []
    for p in sorted(d.glob("p*.jsonl.gz")):
        try:
            with gzip.open(p, "rt") as f:
                n += sum(1 for _ in f)
        except Exception as e:
            bad.append((p.name, repr(e)))
    return {"label": label, "cursor_n": st["n"], "file_n": n, "bad": bad, "ok": n == st["n"] and not bad,
            "complete": st["complete"]}


def iter_raw(label: str):
    """Relit les transactions brutes d'un libellé, dans l'ordre de collecte."""
    d = RAW / label
    for p in sorted(d.glob("p*.jsonl.gz")):
        with gzip.open(p, "rt") as f:
            for line in f:
                yield json.loads(line)


def logger(name: str):
    LOGS.mkdir(parents=True, exist_ok=True)
    path = LOGS / f"{name}.log"

    def _log(msg: str) -> None:
        line = f"{time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())} {msg}"
        print(line, flush=True)
        with open(path, "a") as f:
            f.write(line + "\n")
    return _log


if __name__ == "__main__":
    # usage: python -m dmaga.collect <label> <address> [details] [sort]
    label, address = sys.argv[1], sys.argv[2]
    details = sys.argv[3] if len(sys.argv) > 3 else "full"
    sort = sys.argv[4] if len(sys.argv) > 4 else "asc"
    h = Helius()
    print(collect(h, label, address, details=details, sort=sort, log=logger(label)))
