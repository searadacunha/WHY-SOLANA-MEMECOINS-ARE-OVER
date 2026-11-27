#!/usr/bin/env python3
"""Collecte de l'étude de groupe. Lève les erreurs, compte tout, reprend par token. Lancer sous scripts/guard.py.
Écrit raw/grp/<pool>.jsonl.gz (réponses brutes) et etude_groupe/derived/par_token.jsonl (une ligne par token fini)."""
import csv
import gzip
import json
import os
import random
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import numpy as np  # noqa: E402
import pyarrow.parquet as pq  # noqa: E402
from graphe import ata, deltas, post_balance, transfers  # noqa: E402

from dmaga.config import BIG, RAW  # noqa: E402
from dmaga.helius import Helius, RpcError  # noqa: E402
from dmaga.labels import load as load_labels  # noqa: E402

ROOT = HERE.parent.parent
DMAGA = "CRSwXnfF21yHDXdYBVWwCwQ5Ni2A4QuK3qGYis5k7x7k"
JUIL = (1719792000, 1722470400)  # 01/07/2024 et 01/08/2024, 00:00 UTC
BUDGET, COHORTE, EXT_MAX, PAGES_MINT, PAGES_ATA = 60_000, 30, 60, 20, 5
OUT = ROOT / "etude_groupe" / "derived" / "par_token.jsonl"
RAWG = RAW / "grp"


def population() -> list[dict]:
    primary = {r["pool"] for r in csv.DictReader(open(ROOT / "etude_final" / "derived" / "metrics.csv")) if r["variant"] == "primary"}
    rows = []
    with open(BIG / "controls" / "selection.jsonl") as f:
        for line in f:
            r = json.loads(line)
            if r["pool"] in primary and JUIL[0] <= r["created"] < JUIL[1]:
                rows.append({k: r[k] for k in ("pool", "mint", "created", "S20")})
    target = [r for r in rows if r["pool"] == DMAGA]
    assert len(target) == 1, "DMAGA absent de la population"
    others = sorted((r for r in rows if r["pool"] != DMAGA), key=lambda r: r["pool"])
    random.Random(20261103).shuffle(others)
    return target + others


def pages(h, addr, flt, n_max, sink, role):
    """Rend (transactions, tronqué). Chaque réponse brute part sur le disque."""
    tok, out = None, []
    for i in range(n_max):
        res = h.txs_page(addr, limit=100, sort="asc", token=tok, filters=flt)
        rows = res.get("data") or []
        sink.write(json.dumps({"role": role, "addr": addr, "page": i, "data": rows}) + "\n")
        out += rows
        tok = res.get("paginationToken")
        if not tok:
            return out, False
    return out, True


def collect_token(h, tok, labels):
    pool, mint, created, S = tok["pool"], tok["mint"], tok["created"], tok["S20"]
    RAWG.mkdir(parents=True, exist_ok=True)
    part = RAWG / f"{pool}.part"
    r = dict(tok, courbe_tronquee=False, ata_tronque=0, ata_vides=0, extension_plafonnee=False, ambigu=0)
    with gzip.open(part, "wt") as sink:
        # cohorte : pages du mint avant la migration + 24 h de swaps Raydium
        net: dict[str, int] = {}
        txs, r["courbe_tronquee"] = pages(h, mint, {"blockTime": {"lt": created}, "status": "succeeded"}, PAGES_MINT, sink, "mint")
        for tx in txs:
            for o, v in deltas(tx, mint).items():
                net[o] = net.get(o, 0) + v
        del txs
        t = pq.read_table(BIG / "controls" / "swaps" / f"{pool}.parquet", columns=["t", "owner", "qty"])
        keep = np.array(t["t"]) < created + 86400
        owners = t["owner"].to_pylist()
        qty = np.array(t["qty"])
        for i in np.nonzero(keep)[0].tolist():
            net[owners[i]] = net.get(owners[i], 0) + int(qty[i])
        del t, owners, qty
        cohort = [o for o, v in sorted(net.items(), key=lambda kv: (-kv[1], kv[0])) if v > 0 and o not in labels][:COHORTE]
        del net
        r["cohorte"] = cohort
        # comptes de jetons, puis extension par les transferts retenus
        flt = {"blockTime": {"lt": S}, "status": "succeeded"}
        queue, seen, new, edges, bal, done_sig = list(cohort), set(cohort), 0, [], {}, set()
        cov = 0
        while queue:
            w = queue.pop(0)
            acc = ata(w, mint)
            txs, trunc = pages(h, acc, flt, PAGES_ATA, sink, "ata")
            if not txs:
                r["ata_vides"] += 1
                continue
            cov += w in cohort
            last = txs[-1]
            if trunc:
                r["ata_tronque"] += 1
                res = h.txs_page(acc, limit=1, sort="desc", filters=flt)
                sink.write(json.dumps({"role": "ata_dernier", "addr": acc, "page": 0, "data": res.get("data") or []}) + "\n")
                last = (res.get("data") or [last])[0]
            bal[w] = post_balance(last, mint, w)
            for tx in txs:
                sig = tx["transaction"]["signatures"][0]
                if sig in done_sig:
                    continue
                done_sig.add(sig)
                es, amb = transfers(tx, mint)
                r["ambigu"] += amb
                for src, dst, raw in es:
                    edges.append([src, dst, raw, tx["blockTime"], sig])
                    for x in (src, dst):
                        if x not in seen and x not in labels:
                            if new < EXT_MAX:
                                seen.add(x)
                                queue.append(x)
                                new += 1
                            else:
                                r["extension_plafonnee"] = True
            del txs
    os.replace(part, RAWG / f"{pool}.jsonl.gz")
    r.update(couverture=cov, nouveaux=new, aretes=edges, soldes=bal)
    return r


def main():
    labels = set(load_labels())
    done = {json.loads(x)["pool"] for x in OUT.read_text().splitlines()} if OUT.exists() else set()
    h = Helius(rps=5)
    t0 = time.time()
    pop = population()
    print(f"population {len(pop)}, déjà faits {len(done)}", flush=True)
    for i, tok in enumerate(pop):
        if tok["pool"] in done:
            continue
        credits = h.stats["requests"] * 10
        if credits >= BUDGET:
            print(f"ARRET budget : {credits} crédits, {dict(h.stats)}", flush=True)
            break
        try:
            r = collect_token(h, tok, labels)
        except RpcError as e:
            print(f"ARRET {tok['pool']} : {e}, {dict(h.stats)}", flush=True)
            break
        r["credits_cumul"] = h.stats["requests"] * 10
        with OUT.open("a") as f:
            f.write(json.dumps(r) + "\n")
        print(f"{i + 1}/{len(pop)} cov {r['couverture']} aretes {len(r['aretes'])} tronq {r['ata_tronque']} crédits {r['credits_cumul']} {time.time() - t0:.0f} s", flush=True)
    print("FIN", dict(h.stats), flush=True)


if __name__ == "__main__":
    main()
