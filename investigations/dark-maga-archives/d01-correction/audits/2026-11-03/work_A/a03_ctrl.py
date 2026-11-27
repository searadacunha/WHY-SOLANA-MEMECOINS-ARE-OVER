#!/usr/bin/env python3
"""Auditeur A. Reparse tout raw/ctrl_tx avec un code écrit depuis le texte du plan (pas d'import de col_50_ctrl, chainutil, metrics).
Sorties dans audits_work/A : a03_lines.parquet (lignes de swap, règle du plan), a03_tx.parquet (une ligne par transaction touchant un vault),
a03_pools.jsonl (curseur, chaîne des deux vaults, histogramme des réussies, compteurs)."""
import csv, gzip, json, sys, time
from pathlib import Path
import pyarrow as pa, pyarrow.parquet as pq

BIG = Path("/Volumes/VERBATIM HD/Dark-MAGA-Investigation/data/controls")
RAW = Path("/Volumes/VERBATIM HD/Dark-MAGA-Investigation/raw/ctrl_tx")
OUT = Path("/Volumes/VERBATIM HD/Dark-MAGA-Investigation/audits_work/A")
ROOT = Path("REDACTED_HOME/Projects/Dark-MAGA-Investigation")
DP = "CRSwXnfF21yHDXdYBVWwCwQ5Ni2A4QuK3qGYis5k7x7k"
L = pa.schema([("pool", pa.string()), ("t", pa.int64()), ("slot", pa.int64()), ("tx_index", pa.int64()), ("owner", pa.string()),
               ("qty", pa.int64()), ("sol", pa.int64()), ("vault_pre", pa.int64())])
T = pa.schema([("pool", pa.string()), ("t", pa.int64()), ("slot", pa.int64()), ("tx_index", pa.int64()), ("dt", pa.int64()), ("ds", pa.int64()),
               ("vs_pre", pa.int64()), ("n_lines", pa.int32()), ("sum_qty", pa.int64()), ("excl_two_sided", pa.int32()), ("kind", pa.string())])
FEE = 0.05


def parse(tx, mint, vt, vs, pool, lines, txs, c, chain):
    meta = tx["meta"]
    c["tx"] += 1
    if meta.get("err") is not None:
        c["err"] += 1
        return
    msg = tx["transaction"]["message"]
    keys = [k["pubkey"] for k in msg["accountKeys"]]
    signers = {k["pubkey"] for k in msg["accountKeys"] if k.get("signer")}
    if tx.get("transactionIndex") is None:
        c["sans_tx_index"] += 1
    if len(keys) != len(meta.get("preBalances") or []):
        c["keys_ne_balances"] += 1
    bal = {}
    for b in meta.get("preTokenBalances") or []:
        bal[(b["accountIndex"], b["mint"])] = [int(b["uiTokenAmount"]["amount"]), 0, b.get("owner")]
    for b in meta.get("postTokenBalances") or []:
        k = (b["accountIndex"], b["mint"])
        x = bal.setdefault(k, [0, 0, b.get("owner")])
        x[1] = int(b["uiTokenAmount"]["amount"])
        if b.get("owner"):
            x[2] = b["owner"]
    dT = dS = None
    preS = None
    owners = {}
    for (i, m), (a, b, o) in bal.items():
        acct = keys[i]
        if acct == vt:
            if a != b:
                dT = b - a
                chain["t"].append((tx["slot"], tx.get("transactionIndex") or 0, a, b))
            continue
        if acct == vs:
            if a != b:
                dS = b - a
                preS = a
                chain["s"].append((tx["slot"], tx.get("transactionIndex") or 0, a, b))
            continue
        if a != b and o:
            d = owners.setdefault(o, {})
            d[m] = d.get(m, 0) + b - a
    t, slot, idx = tx["blockTime"], tx["slot"], tx.get("transactionIndex") or 0
    if dT is None or dS is None:
        c["sans_deux_vaults"] += 1
        if dT is not None or dS is not None:
            c["un_seul_vault"] += 1
        return
    if (dT > 0) == (dS > 0):
        c["lp"] += 1
        txs.append({"pool": pool, "t": t, "slot": slot, "tx_index": idx, "dt": dT, "ds": dS, "vs_pre": preS, "n_lines": 0, "sum_qty": 0, "excl_two_sided": 0, "kind": "lp"})
        return
    cand = {}
    excl = 0
    for o, m in owners.items():
        v = m.get(mint, 0)
        if not v:
            continue
        if o not in signers and any(k != mint and x and (x > 0) != (v > 0) for k, x in m.items()):
            excl += 1
            continue
        if (v > 0) == (dT < 0):
            cand[o] = v
    full = sum(cand.values())
    keep = {o: v for o, v in cand.items() if abs(v) >= FEE * abs(full)}
    tot = sum(keep.values())
    if not keep:
        c["sans_ligne"] += 1
        c["sans_ligne_sol"] += abs(dS)
    c["sol_vault_achat"] += dS if dS > 0 else 0
    for o, v in keep.items():
        lines.append({"pool": pool, "t": t, "slot": slot, "tx_index": idx, "owner": o, "qty": v, "sol": round(-dS * v / tot), "vault_pre": preS})
    txs.append({"pool": pool, "t": t, "slot": slot, "tx_index": idx, "dt": dT, "ds": dS, "vs_pre": preS, "n_lines": len(keep), "sum_qty": tot, "excl_two_sided": excl, "kind": "swap"})


def main():
    sel = {}
    for x in (BIG / "selection.jsonl").read_text().splitlines():
        r = json.loads(x)
        if r["status"] == "retenu_superset":
            sel[r["pool"]] = r
    prim = [r["pool"] for r in csv.DictReader(open(ROOT / "etude_final/derived/metrics.csv")) if r["variant"] == "primary"]
    order = [DP] + [p for p in prim if p != DP] + [p for p in sel if p not in prim]
    wl = pq.ParquetWriter(OUT / "a03_lines.parquet", L, compression="zstd")
    wt = pq.ParquetWriter(OUT / "a03_tx.parquet", T, compression="zstd")
    rep = open(OUT / "a03_pools.jsonl", "w")
    t0 = time.time()
    for ip, pool in enumerate(order):
        r = sel[pool]
        d = RAW / pool
        cur = json.loads((d / "cursor.json").read_text())
        c = {k: 0 for k in ("tx", "err", "sans_tx_index", "keys_ne_balances", "sans_deux_vaults", "un_seul_vault", "lp", "sans_ligne", "sans_ligne_sol", "sol_vault_achat")}
        chain = {"t": [], "s": []}
        hist = {}
        lines, txs = [], []
        tmin, tmax, nonmono, last = None, None, 0, (-1, -1)
        rupt = {"t": 0, "s": 0}
        lastpost = {"t": None, "s": None}
        first = {"t": None, "s": None}

        def drain():
            for k in ("t", "s"):
                for s_, i_, a_, b_ in chain[k]:
                    if first[k] is None:
                        first[k] = a_
                    if lastpost[k] is not None and lastpost[k] != a_:
                        rupt[k] += 1
                    lastpost[k] = b_
                chain[k].clear()
        for p in sorted(d.glob("p*.jsonl.gz")):
            with gzip.open(p, "rt") as f:
                for line in f:
                    tx = json.loads(line)
                    k = (tx["slot"], tx.get("transactionIndex") or 0)
                    if k < last:
                        nonmono += 1
                    last = k
                    bt = tx["blockTime"]
                    tmin = bt if tmin is None else min(tmin, bt)
                    tmax = bt if tmax is None else max(tmax, bt)
                    hist[bt // 3600] = hist.get(bt // 3600, 0) + 1
                    parse(tx, r["mint"], r["vault_token"], r["vault_sol"], pool, lines, txs, c, chain)
            drain()
            if len(lines) >= 50000:
                wl.write_table(pa.Table.from_pylist(lines, schema=L))
                lines = []
            if len(txs) >= 50000:
                wt.write_table(pa.Table.from_pylist(txs, schema=T))
                txs = []
        if lines:
            wl.write_table(pa.Table.from_pylist(lines, schema=L))
        if txs:
            wt.write_table(pa.Table.from_pylist(txs, schema=T))
        rep.write(json.dumps({"pool": pool, "cursor_n": cur["n"], "complete": cur["complete"], "filters": cur.get("filters"), "created": r["created"],
                              "tmin": tmin, "tmax": tmax, "nonmono": nonmono, "ruptures_token": rupt["t"], "ruptures_sol": rupt["s"], "first_pre_token": first["t"],
                              "first_pre_sol": first["s"], "hist_ok": sorted(hist.items()), **c}) + "\n")
        rep.flush()
        if ip % 10 == 0:
            print(ip, len(order), pool, round(time.time() - t0), flush=True)
    wl.close(); wt.close()
    print("FIN", round(time.time() - t0), flush=True)


if __name__ == "__main__":
    main()
