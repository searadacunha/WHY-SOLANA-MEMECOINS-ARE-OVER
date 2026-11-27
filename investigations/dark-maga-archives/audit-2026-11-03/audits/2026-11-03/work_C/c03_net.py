#!/usr/bin/env python3
"""Reseau borne (pool de recherche, classe Helius du projet). Compte chaque appel dans credits.csv.
 sigs <addr> [max_pages]        : compte les signatures (y compris comptes de jetons au solde change), ecrit la 1re et la derniere
 full <addr> [max_pages]        : historique complet en jsonParsed, limit=100, un seul fichier gz par wallet (append)
Tarif retenu pour le compte : 10 credits par appel GTFA (mesure notee dans la memoire 02/11, non revalidee ici).
"""
import gzip
import json
import sys
import time
from pathlib import Path

from dmaga.helius import Helius

WORK = Path(__file__).resolve().parent
NET = Path("/Volumes/VERBATIM HD/Dark-MAGA-Investigation/audits_work/C/net")
CRED = WORK / "credits.csv"
COST = 10
BUDGET = 20000


def used():
    if not CRED.exists():
        return 0
    return sum(int(l.split(",")[3]) for l in CRED.read_text().splitlines()[1:] if l.strip())


def note(method, addr):
    new = not CRED.exists()
    with open(CRED, "a") as f:
        if new:
            f.write("utc,method,addr,credits\n")
        f.write(f"{time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())},{method},{addr},{COST}\n")


def page(h, addr, details, limit, tok):
    if used() + COST > BUDGET:
        raise SystemExit("budget de credits atteint")
    r = h.txs_page(addr, details=details, limit=limit, sort="asc", token=tok,
                   filters={"tokenAccounts": "balanceChanged", "status": "succeeded"})
    note(f"gtfa_{details}", addr)
    return r


def sigs(h, addr, max_pages):
    n, tok, first, last, pages = 0, None, None, None, 0
    while True:
        r = page(h, addr, "signatures", 1000, tok)
        rows = r["data"]
        pages += 1
        if rows:
            first = first or rows[0]
            last = rows[-1]
        n += len(rows)
        tok = r.get("paginationToken")
        if not tok or pages >= max_pages:
            break
    print(json.dumps({"addr": addr, "n": n, "complete": not tok, "pages": pages,
                      "first_bt": first and first.get("blockTime"), "last_bt": last and last.get("blockTime")}), flush=True)


def full(h, addr, max_pages):
    NET.mkdir(parents=True, exist_ok=True)
    path = NET / f"{addr}.jsonl.gz"
    cur = NET / f"{addr}.cursor.json"
    st = json.loads(cur.read_text()) if cur.exists() else {"token": None, "n": 0, "complete": False, "pages": 0}
    pages = 0
    while not st["complete"] and pages < max_pages:
        r = page(h, addr, "full", 100, st["token"])
        rows = r["data"]
        if rows:
            with gzip.open(path, "at", compresslevel=6) as f:
                for x in rows:
                    f.write(json.dumps(x, separators=(",", ":")) + "\n")
        st["n"] += len(rows)
        st["token"] = r.get("paginationToken")
        st["complete"] = not st["token"]
        st["pages"] += 1
        pages += 1
        cur.write_text(json.dumps(st))
    print(json.dumps({"addr": addr, **{k: st[k] for k in ("n", "complete", "pages")}}), flush=True)


if __name__ == "__main__":
    cmd, addr = sys.argv[1], sys.argv[2]
    mp = int(sys.argv[3]) if len(sys.argv) > 3 else 50
    h = Helius()
    {"sigs": sigs, "full": full}[cmd](h, addr, mp)
    print("credits utilises", used(), "stats", dict(h.stats), flush=True)
