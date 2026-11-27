#!/usr/bin/env python3
"""Réseau borné, pool de recherche (classe Helius du projet), aucune clé lue ni écrite ici. Chaque appel est compté dans work_G/credits.csv, 10 crédits la page (tarif retenu par C et D).
 full <fichier d'adresses> [pages_max_par_adresse]  : historique jsonParsed, limit=100, ordre croissant, écrit dans audits_work/G/net/<addr>.jsonl.gz
 sigs <fichier d'adresses>                          : une page de signatures (limit=1000), écrit audits_work/G/net/<addr>.sigs.json
 ext <addr> [pages]                                 : prolonge un historique tronqué de C à partir de son curseur, sans toucher au dossier de C."""
import gzip, json, os, sys, time
from pathlib import Path
from dmaga.helius import Helius
WORK = Path("audits/2026-11-03/work_G"); CRED = WORK / "credits.csv"
NETG = Path("/Volumes/VERBATIM HD/Dark-MAGA-Investigation/audits_work/G/net"); NETC = Path("/Volumes/VERBATIM HD/Dark-MAGA-Investigation/audits_work/C/net")
NETG.mkdir(parents=True, exist_ok=True)
COST, BUDGET = 10, 5000
def used():
    if not CRED.exists(): return 0
    return sum(int(l.split(",")[3]) for l in CRED.read_text().splitlines()[1:] if l.strip())
def note(m, a):
    new = not CRED.exists()
    with open(CRED, "a") as f:
        if new: f.write("utc,method,addr,credits\n")
        f.write(f"{time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())},{m},{a},{COST}\n")
def page(h, a, details, limit, tok, sort="asc"):
    if used() + COST > BUDGET: raise SystemExit("budget atteint")
    r = h.txs_page(a, details=details, limit=limit, sort=sort, token=tok, filters={"tokenAccounts": "balanceChanged", "status": "succeeded"})
    note("gtfa_" + details, a)
    return r
def full(h, a, maxp, st=None):
    p = NETG / f"{a}.jsonl.gz"; cur = NETG / f"{a}.cursor.json"
    if cur.exists(): st = json.loads(cur.read_text())
    st = st or {"token": None, "n": 0, "complete": False, "pages": 0}
    k = 0
    while not st["complete"] and k < maxp:
        r = page(h, a, "full", 100, st["token"]); rows = r["data"]
        if rows:
            with gzip.open(p, "at", compresslevel=6) as f:
                for x in rows: f.write(json.dumps(x, separators=(",", ":")) + "\n")
        st["n"] += len(rows); st["token"] = r.get("paginationToken"); st["complete"] = not st["token"]; st["pages"] += 1; k += 1
        cur.write_text(json.dumps(st))
    print(json.dumps({"a": a, "n": st["n"], "complete": st["complete"], "pages": st["pages"]}), flush=True)
def sigs(h, a):
    r = page(h, a, "signatures", 1000, None); rows = r["data"]
    (NETG / f"{a}.sigs.json").write_text(json.dumps({"n": len(rows), "more": bool(r.get("paginationToken")), "first": rows[0] if rows else None, "last": rows[-1] if rows else None}))
    print(json.dumps({"a": a, "n": len(rows), "more": bool(r.get("paginationToken")), "first_bt": rows[0].get("blockTime") if rows else None, "last_bt": rows[-1].get("blockTime") if rows else None}), flush=True)
if __name__ == "__main__":
    cmd = sys.argv[1]; h = Helius(rps=2)
    if cmd == "full":
        for a in [l.strip() for l in open(sys.argv[2]) if l.strip() and not l.startswith("#")]:
            full(h, a, int(sys.argv[3]) if len(sys.argv) > 3 else 1)
    elif cmd == "sigs":
        for a in [l.strip() for l in open(sys.argv[2]) if l.strip() and not l.startswith("#")]: sigs(h, a)
    elif cmd == "ext":
        a = sys.argv[2]; c = json.load(open(NETC / f"{a}.cursor.json"))
        full(h, a, int(sys.argv[3]) if len(sys.argv) > 3 else 5, {"token": c["token"], "n": 0, "complete": False, "pages": 0})
    print("crédits", used(), "stats", {k: v for k, v in h.stats.items()}, flush=True)
    if cmd == "desc":  # dernière page d'une adresse, ordre décroissant ; fichier séparé pour ne pas mêler les curseurs
        for a in [l.strip() for l in open(sys.argv[2]) if l.strip() and not l.startswith("#")]:
            r = page(h, a, "full", 100, None, sort="desc"); rows = r["data"]
            with gzip.open(NETG / f"{a}.desc.jsonl.gz", "wt", compresslevel=6) as f:
                for x in rows: f.write(json.dumps(x, separators=(",", ":")) + "\n")
            print(json.dumps({"a": a, "n": len(rows), "more": bool(r.get("paginationToken"))}), flush=True)
        print("crédits", used(), flush=True)
    if cmd == "window":  # fenêtre de dates : window <addr> <gte> <lte> [pages] ; fichier séparé <addr>.win.jsonl.gz
        a, gte, lte = sys.argv[2], int(sys.argv[3]), int(sys.argv[4]); maxp = int(sys.argv[5]) if len(sys.argv) > 5 else 2; tok = None; n = 0
        for _ in range(maxp):
            if used() + COST > BUDGET: raise SystemExit("budget atteint")
            r = h.txs_page(a, details="full", limit=100, sort="asc", token=tok, filters={"tokenAccounts": "balanceChanged", "status": "succeeded", "blockTime": {"gte": gte, "lte": lte}})
            note("gtfa_full_win", a); rows = r["data"]; n += len(rows); tok = r.get("paginationToken")
            with gzip.open(NETG / f"{a}.win.jsonl.gz", "at", compresslevel=6) as f:
                for x in rows: f.write(json.dumps(x, separators=(",", ":")) + "\n")
            if not tok: break
        print(json.dumps({"a": a, "n": n, "more": bool(tok)}), "crédits", used(), flush=True)
