#!/usr/bin/env python3
"""Sélection des comparateurs et collecte de leurs swaps Raydium, selon le plan.

select : applique le pic (10× et 20×) à activity.jsonl, lit le prix une heure avant chaque S, écrit
         selection.jsonl avec le motif de chaque exclusion. Superset : 10× et bande large (variantes R1, R2).
swaps  : pour chaque token retenu, transactions réussies du pool de la création à S+1 h, puis une table de
         swaps et un compteur de rejets. DMAGA passe par le même code, depuis le même type de requête.
Refuse de partir sur une population partielle. `h` est injectable pour les contrôles de bout en bout.
"""
import csv
import io
import json
import os
import sys
import threading
import zipfile
from collections import Counter
from concurrent.futures import ThreadPoolExecutor

import pyarrow as pa
import pyarrow.parquet as pq

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from chainutil import _keys, _signers, token_deltas  # noqa: E402
from metrics import spike_hour  # noqa: E402

from dmaga.collect import collect, iter_raw, logger, verify  # noqa: E402
from dmaga.config import BIG, RAW, WSOL  # noqa: E402

OUT = BIG / "controls"
DMAGA_POOL = "CRSwXnfF21yHDXdYBVWwCwQ5Ni2A4QuK3qGYis5k7x7k"
AVATAR = 1721589800  # S1 mesure [E−3 h, E) pour E = envoi de l'avatar : les données de DMAGA doivent aller jusque-là
H = 3600
FEE_SHARE = 0.05
BAND = (100_000, 10_000_000)  # bande principale, centrée sur DMAGA, voir le plan
WIDE = (10_000, 50_000_000)  # variante R2 et superset de collecte
SCHEMA = pa.schema([("t", pa.int64()), ("slot", pa.int64()), ("tx_index", pa.int64()), ("signature", pa.string()),
                    ("owner", pa.string()), ("qty", pa.int64()), ("sol", pa.int64()), ("vault_pre", pa.int64())])


def sol_usd() -> dict[int, float]:
    out = {}
    for z in sorted((RAW / "solusd").glob("SOLUSDT-1m-*.zip")):
        if z.name.startswith("._"):
            continue
        with zipfile.ZipFile(z) as f, f.open(f.namelist()[0]) as fh:
            for row in csv.reader(io.TextIOWrapper(fh)):
                if row and row[0].isdigit():
                    ms = int(row[0])
                    out[(ms // 1000 if ms > 10**14 else ms) // 60000] = float(row[4])
    if not out:
        raise RuntimeError("aucun prix SOL/USD")
    return out


def parse_swaps(tx: dict, mint: str, vault_token: str, vault_sol: str, stats: Counter) -> list[dict]:
    """Swaps Raydium v4 d'une transaction. Le vault fait foi. Tout rejet est compté dans `stats`."""
    stats["tx"] += 1
    if tx["meta"].get("err") is not None:
        stats["tx_echouee"] += 1
        return []
    keys = _keys(tx)
    ds = token_deltas(tx, keys)
    dt = next((d for d in ds if d["account"] == vault_token), None)
    dq = next((d for d in ds if d["account"] == vault_sol), None)
    if dt is None or dq is None:
        stats["sans_vault"] += 1
        return []
    if (dt["delta"] > 0) == (dq["delta"] > 0):
        stats["lp"] += 1  # dépôt ou retrait : les deux réserves dans le même sens
        return []
    signers = set(_signers(tx))
    per: dict[str, dict] = {}
    for d in ds:
        if d["account"] in (vault_token, vault_sol) or not d["owner"]:
            continue
        per.setdefault(d["owner"], {}).setdefault(d["mint"], 0)
        per[d["owner"]][d["mint"]] += d["delta"]
    others: dict[str, int] = {}
    for o, m in per.items():
        v = m.get(mint, 0)
        if not v:
            continue
        # propriétaire non signataire à deux côtés : réserve d'un autre venue ou escrow, écarté de tous les tokens
        if o not in signers and any(k != mint and x and (x > 0) != (v > 0) for k, x in m.items()):
            stats["non_signataire_deux_cotes"] += 1
            continue
        others[o] = v
    side = {o: v for o, v in others.items() if (v > 0) == (dt["delta"] < 0)}
    stats["sens_opposes_ignores"] += len(others) - len(side)
    full = sum(side.values())
    same = {o: v for o, v in side.items() if abs(v) >= FEE_SHARE * abs(full)}
    stats["parts_de_frais"] += len(side) - len(same)
    total = sum(same.values())
    if not same:
        stats["sans_beneficiaire"] += 1
        return []
    if abs(abs(full) - abs(dt["delta"])) > 0.01 * abs(dt["delta"]):
        stats["qty_differente_du_vault"] += 1
    stats["swaps"] += 1
    return [{"t": tx["blockTime"], "slot": tx["slot"], "tx_index": tx.get("transactionIndex") or 0,
             "signature": tx["transaction"]["signatures"][0], "owner": o, "qty": v,
             "sol": int(round(-dq["delta"] * v / total)), "vault_pre": dq["pre"]} for o, v in same.items()]


def read_jsonl_strict(path) -> tuple[list[dict], int]:
    rows, bad = [], 0
    for line in path.read_text().splitlines():
        if not line.strip():
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError:
            bad += 1
    return rows, bad


def fdv_at(h, r, S, px) -> float | str:
    """Capitalisation une heure avant S, ou un motif d'absence. Une minute hors couverture lève."""
    res = h.txs_page(r["pool"], details="full", sort="desc", limit=200,
                     filters={"blockTime": {"lt": S - H}, "status": "succeeded"})
    for tx in res["data"]:
        ds = {d["account"]: d for d in token_deltas(tx, _keys(tx))}
        dt, dq = ds.get(r["vault_token"]), ds.get(r["vault_sol"])
        if dt and dq and dt["post"] > 0:
            price = (dq["post"] / 1e9) / (dt["post"] / 10 ** dt["decimals"])
            usd = px.get(tx["blockTime"] // 60)
            if usd is None:
                raise RuntimeError(f"pas de prix SOL/USD à {tx['blockTime']} : couverture à compléter")
            return price * 1e9 * usd
    return "sans_swap"


def select(log, h=None):
    from dmaga.helius import Helius
    h = h or Helius(rps=5)
    px = sol_usd()
    mig = {}
    for x in (OUT / "migrations.jsonl").read_text().splitlines():
        m = json.loads(x)
        mig[m["pool"]] = m
    acts, bad = read_jsonl_strict(OUT / "activity.jsonl")
    seen = {a["pool"] for a in acts}
    missing = set(mig) - seen
    if missing or bad:
        sys.exit(f"activité incomplète : {len(missing)} pools absents, {bad} lignes invalides. Sélection refusée.")
    if len(acts) != len(seen):
        sys.exit("activity.jsonl contient des doublons")
    out_path = OUT / "selection.jsonl"
    done = {r["pool"] for r in read_jsonl_strict(out_path)[0]} if out_path.exists() else set()
    f = out_path.open("a")
    lock = threading.Lock()
    errors = []

    def one(a):
        hist = {int(k): int(v) for k, v in a["hist"]}
        m = mig[a["pool"]]
        s20, s10 = spike_hour(hist, a["created"], 20.0), spike_hour(hist, a["created"], 10.0)
        r = {"pool": a["pool"], "mint": a["mint"], "created": a["created"], "S20": s20, "S10": s10,
             "truncated": a["truncated"], "vault_token": m["vault_token"], "vault_sol": m["vault_sol"],
             "tronque_sans_S20": bool(a["truncated"] and s10 and not s20)}
        if not s20 and not s10:
            r["status"] = "tronque_sans_pic" if a["truncated"] else "pas_de_pic"
            return r
        for name, S in (("fdv_s20", s20), ("fdv_s10", s10)):
            if S:
                v = fdv_at(h, r, S, px)
                if isinstance(v, str):
                    r[f"{name}_absent"] = v
                else:
                    r[name] = v
        vals = [r[k] for k in ("fdv_s20", "fdv_s10") if k in r]
        if not vals:
            r["status"] = "sans_swap_avant_S"
        elif any(WIDE[0] <= v <= WIDE[1] for v in vals):
            r["status"] = "retenu_superset"
        else:
            r["status"] = "hors_bande"
        return r

    def safe(a):
        try:
            return one(a)
        except Exception as e:  # pas de ligne écrite : le pool reste à refaire, la sortie est en erreur
            errors.append(a["pool"])
            log(f"ECHEC select {a['pool']}: {e!r}")
            return None

    with ThreadPoolExecutor(5) as ex:
        for r in ex.map(safe, [a for a in acts if a["pool"] not in done]):
            if r:
                with lock:
                    f.write(json.dumps(r) + "\n")
                    f.flush()
    f.close()
    counts = Counter(r["status"] for r in read_jsonl_strict(out_path)[0])
    log(f"selection {dict(counts)} erreurs={len(errors)}")
    if errors:
        sys.exit(1)


def swaps(log, h=None):
    from dmaga.helius import Helius
    h = h or Helius(rps=6, timeout=240)
    all_rows, bad = read_jsonl_strict(OUT / "selection.jsonl")
    if bad:
        sys.exit(f"selection.jsonl : {bad} lignes invalides")
    rows = [r for r in all_rows if r["status"] == "retenu_superset"]
    if not any(r["pool"] == DMAGA_POOL for r in rows):
        sys.exit("DMAGA absent de la sélection : la règle de pic ou la bande l'exclut, à signaler")
    d = OUT / "swaps"
    d.mkdir(parents=True, exist_ok=True)
    stats_f = (OUT / "swaps_stats.jsonl").open("a")
    lock = threading.Lock()
    errors = []

    def one(r):
        path = d / f"{r['pool']}.parquet"
        if path.exists():
            return 0
        end = max(x for x in (r["S20"], r["S10"]) if x) + H
        if r["pool"] == DMAGA_POOL:
            end = max(end, AVATAR + 1)  # hors de compute, qui coupe à S : sert seulement à S1
        label = f"ctrl_tx/{r['pool']}"
        collect(h, label, r["pool"], details="full", sort="asc", log=lambda m: None,
                filters={"blockTime": {"gte": r["created"], "lt": end}, "status": "succeeded"})
        v = verify(label)
        if not (v["ok"] and v["complete"]):
            raise RuntimeError(f"{label} incomplet ou illisible: {v}")
        stats: Counter = Counter()
        out = []
        chain = []
        for tx in iter_raw(label):
            out.extend(parse_swaps(tx, r["mint"], r["vault_token"], r["vault_sol"], stats))
            for x in token_deltas(tx, _keys(tx)):
                if x["account"] == r["vault_sol"]:
                    chain.append((tx["slot"], tx.get("transactionIndex") or 0, x["pre"], x["post"]))
        chain.sort()
        # solde après une transaction = solde avant la suivante, sinon une transaction manque
        ruptures = sum(1 for a, b in zip(chain, chain[1:]) if a[3] != b[2])
        out.sort(key=lambda x: (x["slot"], x["tx_index"]))
        tmp = path.with_name(path.name + ".tmp")
        pq.write_table(pa.Table.from_pylist(out, schema=SCHEMA), tmp, compression="zstd")
        tmp.replace(path)
        with lock:
            stats_f.write(json.dumps({"pool": r["pool"], "ruptures": ruptures, **stats}) + "\n")
            stats_f.flush()
        return len(out)

    def safe(r):
        try:
            return one(r)
        except Exception as e:
            errors.append(r["pool"])
            log(f"ECHEC swaps {r['pool']}: {e!r}")
            return 0

    with ThreadPoolExecutor(4) as ex:
        for i, _ in enumerate(ex.map(safe, rows), 1):
            if i % 20 == 0 or i == len(rows):
                log(f"swaps {i}/{len(rows)} erreurs={len(errors)} {dict(getattr(h, 'stats', {}))}")
    log(f"FIN swaps tokens={len(rows)} erreurs={errors}")
    if errors:
        sys.exit(1)


if __name__ == "__main__":
    lg = logger("col_50_ctrl")
    {"select": select, "swaps": swaps}[sys.argv[1]](lg)
