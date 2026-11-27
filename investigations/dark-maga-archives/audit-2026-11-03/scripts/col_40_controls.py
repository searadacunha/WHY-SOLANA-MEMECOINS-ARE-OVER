#!/usr/bin/env python3
"""Corpus de comparateurs, par règle et non à la main.

Étape A (`migrations`) : toutes les migrations Pump.fun du compte de migration, du 15/06 au 31/08/2024,
    en transactions complètes : mint, pool, vaults et heure de création du pool.
Étape B (`activity`) : un appel par pool sur [création + 96 h, création + 60 j). Moins de 500 signatures :
    pas de pic tardif possible, fini. Sinon, signatures sur [création + 24 h, création + 60 j) jusqu'à MAX_PAGES.
Sorties : BIG/controls/migrations.jsonl, BIG/controls/activity/<pool>.json.gz (histogramme horaire).
Reprise : ce qui existe est sauté. Aucun résultat d'analyse n'est calculé ici.
"""
import gzip
import json
import sys
import threading
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from dmaga.collect import collect, iter_raw, logger
from dmaga.config import BIG, RAW, WSOL
from dmaga.helius import Helius
from dmaga.normalize import _keys

MIGRATION = "39azUYFWPz3VHgKCf3VChUwbpURdCHRxjWVowf5jUJjg"
RAYDIUM_V4 = "675kPX9MHTjS2zt1qfr1NYHuzeLXfQM9H24wFSUt1Mp8"
AUTH = "5Q544fKrFoe6tsEbD7S8EmxGTJYAKtTVhAW5Q5pge4j1"
T_FROM, T_TO = 1718409600, 1725148800  # 15/06/2024 00:00 UTC, 01/09/2024 00:00 UTC
MAX_PAGES = 150  # 150 000 signatures : au-delà le pool est marqué tronqué, jamais comptabilisé en silence
OUT = BIG / "controls"


def parse_migration(t: dict) -> dict | None:
    logs = t["meta"].get("logMessages") or []
    if not any("initialize2" in l for l in logs):
        return None
    keys = _keys(t)
    msg = t["transaction"]["message"]
    pool = None
    for ins in msg["instructions"]:
        if ins.get("programId") == RAYDIUM_V4:
            pool = ins["accounts"][4]  # compte AMM de initialize2, vérifié sur DMAGA dans le test
            break
    if not pool:
        return None
    mint, vault_tok, vault_sol = None, None, None
    held = [b for b in t["meta"].get("postTokenBalances") or [] if b.get("owner") == AUTH]
    if len(held) != 2:
        raise ValueError(f"migration {t['transaction']['signatures'][0]}: {len(held)} soldes de l'autorité, 2 attendus")
    for b in held:
        if b.get("owner") == AUTH:
            if b["mint"] == WSOL:
                vault_sol = keys[b["accountIndex"]]
            else:
                mint, vault_tok = b["mint"], keys[b["accountIndex"]]
    if not (mint and vault_sol):
        return None
    return {"mint": mint, "pool": pool, "vault_token": vault_tok, "vault_sol": vault_sol,
            "created": t["blockTime"], "slot": t["slot"], "signature": t["transaction"]["signatures"][0]}


def migrations(log):
    h = Helius(rps=4, timeout=240)
    st = collect(h, "ctrl_migrations", MIGRATION, details="full", sort="asc", log=log,
                 filters={"blockTime": {"gte": T_FROM, "lt": T_TO}, "status": "succeeded"})
    log(f"migrations brut n={st['n']} complete={st['complete']}")
    OUT.mkdir(parents=True, exist_ok=True)
    n = bad = 0
    with (OUT / "migrations.jsonl").open("w") as f:
        for t in iter_raw("ctrl_migrations"):
            m = parse_migration(t)
            if m:
                f.write(json.dumps(m) + "\n")
                n += 1
            else:
                bad += 1
    log(f"migrations parsées n={n}, transactions du compte sans pool={bad}")


def activity(log, workers=14):
    h = Helius(rps=18, timeout=120)
    rows = [json.loads(x) for x in (OUT / "migrations.jsonl").read_text().splitlines()]
    # un seul fichier en ajout : le disque USB ne supporte pas 14 000 petits fichiers
    path = OUT / "activity.jsonl"
    done = set()
    if path.exists():
        for line in path.read_text().splitlines():
            try:
                done.add(json.loads(line)["pool"])
            except json.JSONDecodeError:  # dernière ligne tronquée par une coupure : le pool sera refait
                pass
    rows = [m for m in rows if m["pool"] not in done]
    log(f"activité : déjà faits {len(done)}, restent {len(rows)}")
    if path.exists() and path.stat().st_size and not path.read_bytes().endswith(b"\n"):
        with path.open("a") as f:  # coupure en plein ajout : la ligne suivante ne doit pas s'y coller
            f.write("\n")
    out = path.open("a")
    lock = threading.Lock()
    failures = []

    def job(m):
        # pré-filtre : un pic tardif exige au moins 500 signatures après création + 96 h
        late = {"blockTime": {"gte": m["created"] + 96 * 3600, "lt": m["created"] + 60 * 86400}}
        res = h.txs_page(m["pool"], details="signatures", sort="asc", limit=1000, filters=late)
        n_late = len(res["data"])
        hist = Counter()
        pages = 0
        truncated = False
        if n_late >= 500:
            flt = {"blockTime": {"gte": m["created"] + 24 * 3600, "lt": m["created"] + 60 * 86400}}
            tok = None
            while True:
                res = h.txs_page(m["pool"], details="signatures", sort="asc", limit=1000, token=tok, filters=flt)
                for x in res["data"]:
                    hist[x["blockTime"] // 3600] += 1
                pages += 1
                tok = res.get("paginationToken")
                if not tok or not res["data"]:
                    break
                if pages >= MAX_PAGES:
                    truncated = True
                    break
        blob = {"mint": m["mint"], "pool": m["pool"], "created": m["created"], "pages": pages, "truncated": truncated,
                "n_late_first_page": n_late, "hist": sorted(hist.items())}
        with lock:
            out.write(json.dumps(blob) + "\n")
            out.flush()
        return pages

    def safe(m):
        try:
            return job(m)
        except Exception as e:  # le pool reste à refaire : pas de fichier écrit, l'échec est compté
            failures.append(m["pool"])
            log(f"ECHEC {m['pool']}: {e!r}")
            return 0

    with ThreadPoolExecutor(workers) as ex:
        for i, _ in enumerate(ex.map(safe, rows), 1):
            if i % 200 == 0 or i == len(rows):
                log(f"activité {i}/{len(rows)} echecs={len(failures)} {dict(h.stats)}")
    log(f"FIN activité pools={len(rows)} echecs={len(failures)}")
    if failures:
        sys.exit(1)  # population partielle : la sélection refusera de partir


if __name__ == "__main__":
    lg = logger("col_40_controls")
    if sys.argv[1] == "migrations":
        migrations(lg)
    else:
        activity(lg)
