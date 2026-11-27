#!/usr/bin/env python3
"""Auditeur D. Parseur écrit sans lire a02_full.py de A pour la logique de sortie : relit pre/post token balances du brut full_*.
Sorties (flux, faible mémoire) dans audits_work/D : d01_tx, d01_own, d01_acct. Aucune donnée d'étude gelée touchée."""
import gzip, json, os, sys, time
from pathlib import Path
import pyarrow as pa, pyarrow.parquet as pq
RAW = Path("/Volumes/VERBATIM HD/Dark-MAGA-Investigation/raw")
OUT = Path("/Volumes/VERBATIM HD/Dark-MAGA-Investigation/audits_work/D")
MINT = "7D7BRcBYepfi77vxySapmeqRNN1wsBBxnFPJGbH5pump"
WSOL = "So11111111111111111111111111111111111111112"
STABLE = {"EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v", "Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB"}
VT, VS = "5HuEsLbebeuottMsFW3hHcXTrKVsu3WUNSQnSr6aX4eL", "3p7DbnWekWjtMQkey6fp1emdwXbAAxecnYuD5eU9ZZPH"
S_TX = pa.schema([("src", pa.string()), ("slice", pa.string()), ("sig", pa.string()), ("slot", pa.int64()), ("idx", pa.int32()), ("bt", pa.int64()),
                  ("failed", pa.bool_()), ("payer", pa.string()), ("signers", pa.string()), ("fee", pa.int64()),
                  ("vt_d", pa.int64()), ("vs_d", pa.int64()), ("n_acct", pa.int32()), ("net", pa.int64())])
S_OWN = pa.schema([("sig", pa.string()), ("slot", pa.int64()), ("idx", pa.int32()), ("bt", pa.int64()), ("owner", pa.string()), ("d", pa.int64()),
                   ("wsol", pa.int64()), ("stable", pa.int64()), ("native", pa.int64()), ("signer", pa.bool_()), ("src", pa.string())])
S_AC = pa.schema([("sig", pa.string()), ("slot", pa.int64()), ("idx", pa.int32()), ("bt", pa.int64()), ("account", pa.string()), ("owner", pa.string()),
                  ("pre", pa.int64()), ("post", pa.int64())])
class W:
    def __init__(s, name, schema):
        s.w = pq.ParquetWriter(OUT / name, schema, compression="zstd"); s.b = []; s.sc = schema
    def add(s, row):
        s.b.append(row)
        if len(s.b) >= 20000: s.flush()
    def flush(s):
        if s.b:
            s.w.write_table(pa.Table.from_pylist(s.b, schema=s.sc)); s.b = []
    def close(s):
        s.flush(); s.w.close()
wt, wo, wa = W("d01_tx.parquet", S_TX), W("d01_own.parquet", S_OWN), W("d01_acct.parquet", S_AC)
def side(lst):
    r = {}
    for b in lst or []:
        r[(b["accountIndex"], b["mint"])] = (int(b["uiTokenAmount"]["amount"]), b.get("owner"))
    return r
def one(t, src, slc):
    m = t["transaction"]["message"]; me = t["meta"]
    sig = t["transaction"]["signatures"][0]; slot = t["slot"]; idx = t.get("transactionIndex"); bt = t.get("blockTime")
    keys = [k["pubkey"] for k in m["accountKeys"]]
    signers = {k["pubkey"] for k in m["accountKeys"] if k.get("signer")}
    pre, post = side(me.get("preTokenBalances")), side(me.get("postTokenBalances"))
    vt_d = vs_d = 0; net = 0; n = 0
    own = {}
    for k in pre.keys() | post.keys():
        a, b = pre.get(k), post.get(k)
        x, y = (a[0] if a else 0), (b[0] if b else 0)
        o = (b[1] if b else None) or (a[1] if a else None)
        acct = keys[k[0]]
        if acct == VT: vt_d += y - x
        if acct == VS: vs_d += y - x
        if x == y: continue
        if k[1] == MINT:
            net += y - x; n += 1
            wa.add(dict(sig=sig, slot=slot, idx=idx, bt=bt, account=acct, owner=o, pre=x, post=y))
        e = own.setdefault(o, [0, 0, 0])
        if k[1] == MINT: e[0] += y - x
        elif k[1] == WSOL: e[1] += y - x
        elif k[1] in STABLE: e[2] += y - x
    pos = {}
    for i, a in enumerate(keys): pos.setdefault(a, i)
    pb, qb = me.get("preBalances") or [], me.get("postBalances") or []
    for o, e in own.items():
        if not e[0]: continue
        i = pos.get(o)
        nat = qb[i] - pb[i] if i is not None and i < len(pb) and i < len(qb) else None
        wo.add(dict(sig=sig, slot=slot, idx=idx, bt=bt, owner=o, d=e[0], wsol=e[1], stable=e[2], native=nat, signer=o in signers, src=src))
    if n or vt_d or vs_d:
        wt.add(dict(src=src, slice=slc, sig=sig, slot=slot, idx=idx, bt=bt, failed=me.get("err") is not None, payer=keys[0],
                    signers=",".join(sorted(signers)), fee=me.get("fee"), vt_d=vt_d, vs_d=vs_d, n_acct=n, net=net))
    return bool(n)
def dirs():
    yield "curve", "full_curve", RAW / "full_curve"
    for s in ("pool", "mint", "venue"):
        for p in sorted((RAW / f"full_{s}").iterdir()):
            if not p.name.startswith("._") and p.is_dir(): yield s, p.name, p
t0 = time.time(); tot = 0; withd = 0; ndir = 0
for src, slc, d in dirs():
    ndir += 1
    for f in sorted(x for x in d.iterdir() if x.name.endswith(".jsonl.gz") and not x.name.startswith("._")):
        with gzip.open(f, "rt") as fh:
            for line in fh:
                if not line.strip(): continue
                tot += 1
                if one(json.loads(line), src, slc): withd += 1
    if ndir % 100 == 0:
        print(ndir, tot, withd, int(time.time() - t0), flush=True)
wt.close(); wo.close(); wa.close()
print("FIN dossiers", ndir, "tx", tot, "avec delta DMAGA", withd, "sec", int(time.time() - t0), flush=True)
