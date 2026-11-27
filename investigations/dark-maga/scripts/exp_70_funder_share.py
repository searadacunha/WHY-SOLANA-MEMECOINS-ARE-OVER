#!/usr/bin/env python3
"""EXPLORATOIRE, hors plan gelé : financeur commun chez les premiers gros acheteurs, DMAGA contre 40 comparateurs.

Pour chaque token : les 50 wallets ayant acheté le plus de jetons dans les 24 h suivant la création du pool. Pour chacun, ses
virements SOL ≥ 0,05 reçus dans les 72 h avant son premier achat. Mesure : part des 50 qui partagent un financeur direct avec au
moins un autre des 50. Un financeur étiqueté échange, ou sans étiquette mais avec au moins 1 000 signatures récentes, est un
service et ne compte pas. Comparateurs tirés au hasard (graine fixe) dans la bande principale, sans regarder la mesure.
Écrit tables/funder_share.json dans etude_final/. Le registre force ce test en exploratoire : code non gelé.
"""
import json
import random
import sys
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "etude_final" / "code"))
import pyarrow.parquet as pq  # noqa: E402
from registre import enregistrer  # noqa: E402

from dmaga.config import BIG  # noqa: E402
from dmaga.helius import Helius  # noqa: E402
from dmaga.labels import label  # noqa: E402

OUT = BIG / "controls"
NATIVE = "So11111111111111111111111111111111111111111"
TOP = 50
DMAGA = "CRSwXnfF21yHDXdYBVWwCwQ5Ni2A4QuK3qGYis5k7x7k"
h = Helius(rps=5)
busy_cache: dict[str, bool] = {}


def is_service(a: str) -> bool:
    if label(a):
        return True
    if a in busy_cache:
        return busy_cache[a]
    r = h.txs_page(a, details="signatures", sort="desc", limit=1000)
    busy_cache[a] = len(r["data"]) >= 1000 and bool(r.get("paginationToken"))
    return busy_cache[a]


def measure(sel):
    t = pq.read_table(OUT / "swaps" / f"{sel['pool']}.parquet", columns=["t", "owner", "qty", "sol"]).to_pydict()
    first, bought = {}, defaultdict(int)
    for tt, o, q, s in zip(t["t"], t["owner"], t["qty"], t["sol"]):
        if q > 0 and s < 0:
            first.setdefault(o, tt)
            if tt < sel["created"] + 86400:
                bought[o] += q
    top = sorted(bought, key=bought.get, reverse=True)[:TOP]

    def funders(w):
        res = h.call("getTransfersByAddress", [w, {"direction": "in", "mint": NATIVE, "sortOrder": "desc", "limit": 100,
                                                  "filters": {"blockTime": {"lt": first[w], "gte": first[w] - 72 * 3600},
                                                              "amount": {"gte": 50_000_000}}}])
        return w, {x["fromUserAccount"] for x in res["data"] if x.get("fromUserAccount")}

    with ThreadPoolExecutor(4) as ex:
        got = dict(ex.map(funders, top))
    by = defaultdict(set)
    for w, fs in got.items():
        for f in fs:
            by[f].add(w)
    shared = {f: ws for f, ws in by.items() if len(ws) >= 2}
    real = {f: ws for f, ws in shared.items() if not is_service(f)}
    linked = set().union(*real.values()) if real else set()
    return {"pool": sel["pool"], "n": len(top), "part": len(linked) / max(len(top), 1), "n_financeurs_communs": len(real),
            "services_ecartes": len(shared) - len(real), "exemples": {f: sorted(ws)[:8] for f, ws in list(real.items())[:6]}}


rows = [json.loads(x) for x in (OUT / "selection.jsonl").read_text().splitlines()]
prim = [r for r in rows if r.get("S20") and r.get("fdv_s20") is not None and 100_000 <= r["fdv_s20"] <= 10_000_000
        and (OUT / "swaps" / f"{r['pool']}.parquet").exists()]
target = next(r for r in prim if r["pool"] == DMAGA)
others = sorted((r for r in prim if r["pool"] != DMAGA), key=lambda r: r["pool"])
random.Random(20241102).shuffle(others)
res_t = measure(target)
res_c = []
for r in others[:40]:
    try:
        res_c.append(measure(r))
    except Exception as e:  # compté : un comparateur en échec sort du rang sans être noté à zéro
        print("échec", r["pool"], repr(e))
vals = [c["part"] for c in res_c]
p = (1 + sum(v >= res_t["part"] for v in vals)) / (len(vals) + 1)
out = {"statut": "EXPLORATOIRE, hors plan", "dmaga": res_t, "p_rang": p, "k": len(vals), "comparateurs": res_c,
       "mediane_comparateurs": sorted(vals)[len(vals) // 2] if vals else None}
path = ROOT / "etude_final" / "tables" / "funder_share.json"
path.parent.mkdir(exist_ok=True)
path.write_text(json.dumps(out, indent=1))
enregistrer(str(ROOT / "etude_final"), test="exp_financeur_commun", declare=False, n=len(vals), agent="analyse-exploratoire",
            stat=res_t["part"], p=p, sortie="tables/funder_share.json", note="hors plan, financeur commun des 50 premiers gros acheteurs")
print("DMAGA", res_t["part"], res_t["n_financeurs_communs"], "médiane", out["mediane_comparateurs"], "p", p, "k", len(vals))
