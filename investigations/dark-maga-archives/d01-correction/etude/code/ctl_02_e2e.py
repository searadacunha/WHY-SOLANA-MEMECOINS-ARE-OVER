#!/usr/bin/env python3
"""Contrôle de bout en bout : transactions brutes synthétiques jusqu'au verdict, sans réseau.

Couvre collect, verify, iter_raw, parse_swaps, chaîne de vault, select, swaps, load, ana_10, ana_50, ana_90.
Tout se passe dans un dossier temporaire, copie du code comprise : rien n'écrit dans l'étude ni au registre.
Scénarios : nul (la cible vient de la même loi), fort (accumulation juste avant le pic), rupture (une
transaction retirée du brut doit faire exclure le token). Sort en erreur si un résultat n'est pas celui attendu.
"""
import csv
import importlib
import json
import os
import random
import runpy
import shutil
import sys
import tempfile
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
H = 3600
DMAGA_POOL = "CRSwXnfF21yHDXdYBVWwCwQ5Ni2A4QuK3qGYis5k7x7k"
MINT_D = "7D7BRcBYepfi77vxySapmeqRNN1wsBBxnFPJGbH5pump"
WSOL = "So11111111111111111111111111111111111111112"
AUTH = "5Q544fKrFoe6tsEbD7S8EmxGTJYAKtTVhAW5Q5pge4j1"
K = 140


def make_tx(t, slot, idx, owner, vt, vs, mint, x, y, dx, dy, ok=True):
    """Une transaction jsonParsed minimale : le trader, son compte de jetons, les deux vaults."""
    keys = [{"pubkey": owner, "signer": True}, {"pubkey": owner + "A", "signer": False},
            {"pubkey": vt, "signer": False}, {"pubkey": vs, "signer": False}]
    bal = lambda i, m, o, a, dec: {"accountIndex": i, "mint": m, "owner": o, "uiTokenAmount": {"amount": str(a), "decimals": dec}}
    pre = [bal(1, mint, owner, 10**15, 6), bal(2, mint, AUTH, x, 6), bal(3, WSOL, AUTH, y, 9)]
    post = [bal(1, mint, owner, 10**15 - dx, 6), bal(2, mint, AUTH, x + dx, 6), bal(3, WSOL, AUTH, y + dy, 9)]
    return {"slot": slot, "transactionIndex": idx, "blockTime": t,
            "transaction": {"signatures": [f"{vt[:6]}{slot}{idx}"], "message": {"accountKeys": keys, "instructions": []}},
            "meta": {"err": None if ok else {"x": 1}, "fee": 5000, "preBalances": [0] * 4, "postBalances": [0] * 4,
                     "preTokenBalances": pre, "postTokenBalances": post}}


def build_token(rng, pool, mint, created, S, effect, extend_to=None):
    vt, vs = pool[:20] + "VT", pool[:20] + "VS"
    n = rng.randint(120, 320)
    events = []
    for _ in range(n):
        t = created + int((rng.random() ** 2.0) * (S - created))
        events.append((t, f"w{rng.randint(0, 80)}", rng.random() < 0.55, rng.lognormvariate(-1.0, 1.0)))
    if effect == "fort":
        slot_t = S - 1800
        for i in range(15):
            t = slot_t if i < 8 else S - rng.randint(60, 3 * H - 60)
            events.append((t, f"new{i}", True, rng.lognormvariate(0.5, 0.4) * 25))
    # transactions après S : compute doit les ignorer, seule la fenêtre S1 de DMAGA les utilise
    for i in range(30):
        events.append((S + rng.randint(1, H - 1), f"post{i}", True, 50.0))
    if extend_to:
        events.append((extend_to, "postZ", True, 1.0))
    events.sort(key=lambda e: e[0])
    x, y = 200_000_000 * 10**6, 500 * 10**9
    txs, hist = [], {}
    for idx, (t, o, is_buy, size) in enumerate(events):
        slot = (t - created) * 5 // 2 + 1000
        lam = int(size * 1e9)
        if is_buy:
            dq = int(x * lam / (y + lam))
            tx = make_tx(t, slot, idx, o, vt, vs, mint, x, y, -dq, lam)
            x, y = x - dq, y + lam
        else:
            dq = int(x * lam / max(y - lam, 1)) if y > 2 * lam else 0
            if not dq:
                continue
            tx = make_tx(t, slot, idx, o, vt, vs, mint, x, y, dq, -lam)
            x, y = x + dq, y - lam
        txs.append(tx)
        hist[t // H] = hist.get(t // H, 0) + 1
    hist[S // H] = hist.get(S // H, 0) + 900  # le pic au sens de la règle, en signatures
    mig = {"mint": mint, "pool": pool, "vault_token": vt, "vault_sol": vs, "created": created, "slot": 1,
           "signature": "m" + pool}
    act = {"mint": mint, "pool": pool, "created": created, "pages": 1, "truncated": False, "n_late_first_page": 900,
           "hist": sorted(hist.items())}
    return txs, mig, act


class FakeHelius:
    stats = {}

    def __init__(self, data):
        self.data = data

    def txs_page(self, address, *, details="full", limit=1000, sort="asc", token=None, filters=None):
        rows = self.data[address]
        bt = (filters or {}).get("blockTime", {})
        rows = [r for r in rows if r["blockTime"] >= bt.get("gte", 0) and r["blockTime"] < bt.get("lt", 2**40)]
        if sort == "desc":
            rows = rows[::-1]
        off = int(token or 0)
        page = rows[off:off + limit]
        nxt = str(off + limit) if off + limit < len(rows) else None
        return {"data": page, "paginationToken": nxt}


def scenario(name, effect, drop_tx_from=None):
    tmp = Path(tempfile.mkdtemp(prefix=f"e2e_{name}_", dir=os.environ.get("TMPDIR")))
    code = tmp / "etude" / "code"
    shutil.copytree(HERE, code, ignore=shutil.ignore_patterns("__pycache__", "ctl_*"))
    ext = tmp / "ext"
    (ext / "raw" / "solusd").mkdir(parents=True)
    (ext / "data" / "controls").mkdir(parents=True)
    (ext / "logs").mkdir(parents=True)
    with zipfile.ZipFile(ext / "raw" / "solusd" / "SOLUSDT-1m-2024-07.zip", "w") as z:
        lines = [f"{m * 60000},0,0,0,170.0,0\n" for m in range(1719000000 // 60, 1724000000 // 60, 1)]
        z.writestr("x.csv", "".join(lines))
    code_env = {"DMAGA_EXT": str(ext), "ETUDE_REPRO": "1", "ETUDE_REPRO_DIR": str(tmp)}
    prog = f"""
import json, os, random, runpy, sys
sys.path.insert(0, {str(code)!r})
sys.path.insert(0, {str(HERE)!r})
import ctl_02_e2e as C
import col_50_ctrl as K
import ana_10_table, ana_50_tests
rng = random.Random(7)
data, migs, acts = {{}}, [], []
for i in range({K}):
    pool = f"pool{{i:04d}}" + "x" * 30
    created = 1720000000 + i * 7200
    S = (created + 7 * 86400) // 3600 * 3600
    t, m, a = C.build_token(rng, pool, f"mint{{i:04d}}", created, S, "nul")
    data[pool], _ = t, migs.append(m); acts.append(a)
created, S = 1720923331, 1721588400
t, m, a = C.build_token(rng, C.DMAGA_POOL, C.MINT_D, created, S, {effect!r}, extend_to=K.AVATAR)
data[C.DMAGA_POOL] = t; migs.append(m); acts.append(a)
if {drop_tx_from!r} is not None:
    victim = "pool0000" + "x" * 30
    del data[victim][{drop_tx_from!r}]
out = K.OUT
out.mkdir(parents=True, exist_ok=True)
(out / "migrations.jsonl").write_text("".join(json.dumps(x) + "\\n" for x in migs))
(out / "activity.jsonl").write_text("".join(json.dumps(x) + "\\n" for x in acts))
h = C.FakeHelius(data)
K.select(print, h)
K.swaps(print, h)
ana_10_table.main()
ana_50_tests.main()
runpy.run_path({str(code / 'ana_90_verdict.py')!r}, run_name="__main__")
"""
    import subprocess
    env = dict(os.environ, **code_env)
    env["PYTHONPATH"] = os.environ.get("PYTHONPATH", "")
    r = subprocess.run([sys.executable, "-c", prog], env=env, capture_output=True, text=True, timeout=900)
    if r.returncode:
        raise SystemExit(f"scénario {name} en échec :\n{r.stdout[-1500:]}\n{r.stderr[-2500:]}")
    verdict = json.load(open(tmp / "etude" / "tables" / "verdict.json"))["verdict"]
    counts = json.load(open(tmp / "etude" / "derived" / "selection_counts.json"))
    shutil.rmtree(tmp, ignore_errors=True)
    return verdict, counts


def main():
    lines = ["", "# Contrôle de bout en bout (brut synthétique jusqu'au verdict)", "",
             f"{K} comparateurs + la cible, sans réseau, dans un dossier temporaire.", "",
             "| scénario | verdict | exclus pour rupture |", "|---|---|---|"]
    fail = []
    for name, effect, drop, want in (("nul", "nul", None, "NON DISTINGUABLE"), ("fort", "fort", None, "INHABITUEL"),
                                     ("rupture", "nul", 40, "NON DISTINGUABLE")):
        v, c = scenario(name, effect, drop)
        lines.append(f"| {name} | {v[:60]} | {c.get('exclu_rupture_de_chaine', 0)} |")
        if want not in v:
            fail.append(f"{name}: attendu {want}, obtenu {v}")
        if name == "rupture" and not c.get("exclu_rupture_de_chaine"):
            fail.append("rupture non détectée : la transaction retirée n'a pas exclu le token")
    print("\n".join(lines))
    with open(HERE.parent / "controles" / "synth.md", "a") as f:
        f.write("\n".join(lines) + "\n")
    if fail:
        sys.exit("\n".join(fail))


if __name__ == "__main__":
    main()
