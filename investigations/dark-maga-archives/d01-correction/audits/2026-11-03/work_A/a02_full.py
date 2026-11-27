#!/usr/bin/env python3
"""Auditeur A. Parseur propre du brut DMAGA (full_curve, full_pool, full_mint, full_venue) vers parquet, en flux.

Indépendant de dmaga/normalize.py : ne l'importe pas, relit preTokenBalances, postTokenBalances, pre/postBalances
et les instructions de transfert jsonParsed. Sorties dans audits_work/A : a02_tx, a02_acct, a02_own.
"""
import gzip, json, sys, time
from pathlib import Path
import pyarrow as pa, pyarrow.parquet as pq

RAW = Path("/Volumes/VERBATIM HD/Dark-MAGA-Investigation/raw")
OUT = Path("/Volumes/VERBATIM HD/Dark-MAGA-Investigation/audits_work/A")
MINT = "7D7BRcBYepfi77vxySapmeqRNN1wsBBxnFPJGbH5pump"
WSOL = "So11111111111111111111111111111111111111112"
USDC = "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"
USDT = "Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB"
VT = "5HuEsLbebeuottMsFW3hHcXTrKVsu3WUNSQnSr6aX4eL"
VS = "3p7DbnWekWjtMQkey6fp1emdwXbAAxecnYuD5eU9ZZPH"
AUTH = "5Q544fKrFoe6tsEbD7S8EmxGTJYAKtTVhAW5Q5pge4j1"
NOISE = {"ComputeBudget111111111111111111111111111111", "11111111111111111111111111111111",
         "TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA", "ATokenGPvbdGVxr1b2hvZbsiqW5xWH25efTNsLJA8knL",
         "TokenzQdBNbLqP5VEhdkAS6EPFLC1PHnBqCXEpPxuEb"}

TX = pa.schema([("src", pa.string()), ("slice", pa.string()), ("signature", pa.string()), ("slot", pa.int64()),
                ("tx_index", pa.int64()), ("block_time", pa.int64()), ("failed", pa.bool_()), ("version", pa.string()),
                ("n_keys", pa.int32()), ("n_prebal", pa.int32()), ("vt_pre", pa.int64()), ("vt_post", pa.int64()),
                ("vs_pre", pa.int64()), ("vs_post", pa.int64()), ("ix_vt", pa.int64()), ("ix_vs", pa.int64()),
                ("dmaga_sum", pa.int64()), ("n_dmaga", pa.int32()), ("fee", pa.int64()), ("payer", pa.string()),
                ("signers", pa.string()), ("progs", pa.string()), ("auth_other_wsol", pa.int64()), ("decimals_bad", pa.bool_())])
ACCT = pa.schema([("src", pa.string()), ("signature", pa.string()), ("slot", pa.int64()), ("tx_index", pa.int64()),
                  ("block_time", pa.int64()), ("account", pa.string()), ("owner", pa.string()), ("pre", pa.int64()), ("post", pa.int64())])
OWN = pa.schema([("src", pa.string()), ("signature", pa.string()), ("slot", pa.int64()), ("tx_index", pa.int64()),
                 ("block_time", pa.int64()), ("owner", pa.string()), ("dmaga", pa.int64()), ("wsol", pa.int64()),
                 ("stable", pa.int64()), ("native", pa.int64()), ("is_signer", pa.bool_()), ("is_payer", pa.bool_()),
                 ("other_opp", pa.string())])


def ints(entries):
    out = {}
    for b in entries or []:
        out[(b["accountIndex"], b["mint"])] = (int(b["uiTokenAmount"]["amount"]), b.get("owner"), b["uiTokenAmount"]["decimals"])
    return out


def parse(tx, src, slc, wtx, wac, wow):
    msg = tx["transaction"]["message"]
    meta = tx["meta"]
    sig = tx["transaction"]["signatures"][0]
    keys = [k["pubkey"] for k in msg["accountKeys"]]
    signers = [k["pubkey"] for k in msg["accountKeys"] if k.get("signer")]
    pre, post = ints(meta.get("preTokenBalances")), ints(meta.get("postTokenBalances"))
    slot, idx, bt = tx["slot"], tx.get("transactionIndex"), tx.get("blockTime")
    vt, vs = None, None
    dsum, nd, bad_dec, other_auth = 0, 0, False, 0
    by = {}
    for k in set(pre) | set(post):
        i, mint = k
        a = pre.get(k)
        b = post.get(k)
        va = a[0] if a else 0
        vb = b[0] if b else 0
        owner = (b[1] if b else None) or (a[1] if a else None)
        acct = keys[i]
        if acct == VT:
            vt = (va, vb)
        if acct == VS:
            vs = (va, vb)
        if va == vb:
            continue
        if mint == MINT:
            if (b or a)[2] != 6:
                bad_dec = True
            dsum += vb - va
            nd += 1
            wac.append({"src": src, "signature": sig, "slot": slot, "tx_index": idx, "block_time": bt, "account": acct,
                        "owner": owner, "pre": va, "post": vb})
        elif acct == VS:
            wac.append({"src": src, "signature": sig, "slot": slot, "tx_index": idx, "block_time": bt, "account": acct,
                        "owner": owner, "pre": va, "post": vb})
        elif mint == WSOL and owner == AUTH:
            other_auth += vb - va
        d = by.setdefault(owner, {})
        d[mint] = d.get(mint, 0) + vb - va
    ix_vt = ix_vs = 0
    progs = set()

    def scan(ins):
        nonlocal ix_vt, ix_vs
        p = ins.get("programId")
        if p and p not in NOISE:
            progs.add(p)
        pr = ins.get("parsed")
        if isinstance(pr, dict) and pr.get("type") in ("transfer", "transferChecked"):
            info = pr.get("info") or {}
            amt = info.get("amount")
            if amt is None:
                amt = (info.get("tokenAmount") or {}).get("amount")
            if amt is None:
                return
            amt = int(amt)
            s, d = info.get("source"), info.get("destination")
            if s == VT:
                ix_vt -= amt
            if d == VT:
                ix_vt += amt
            if s == VS:
                ix_vs -= amt
            if d == VS:
                ix_vs += amt
    for ins in msg["instructions"]:
        scan(ins)
    for g in meta.get("innerInstructions") or []:
        for ins in g["instructions"]:
            scan(ins)
    wtx.append({"src": src, "slice": slc, "signature": sig, "slot": slot, "tx_index": idx, "block_time": bt,
                "failed": meta.get("err") is not None, "version": str(tx.get("version")), "n_keys": len(keys),
                "n_prebal": len(meta.get("preBalances") or []), "vt_pre": vt[0] if vt else None, "vt_post": vt[1] if vt else None,
                "vs_pre": vs[0] if vs else None, "vs_post": vs[1] if vs else None, "ix_vt": ix_vt, "ix_vs": ix_vs,
                "dmaga_sum": dsum, "n_dmaga": nd, "fee": meta.get("fee"), "payer": keys[0], "signers": ",".join(signers),
                "progs": ",".join(sorted(progs)), "auth_other_wsol": other_auth, "decimals_bad": bad_dec})
    pb, qb = meta.get("preBalances") or [], meta.get("postBalances") or []
    idx_of = {}
    for i, a in enumerate(keys):
        idx_of.setdefault(a, i)
    for o, m in by.items():
        v = m.get(MINT, 0)
        if not v:
            continue
        i = idx_of.get(o)
        nat = qb[i] - pb[i] if i is not None and i < len(pb) and i < len(qb) else None
        opp = [k for k, x in m.items() if k != MINT and x and (x > 0) != (v > 0)]
        wow.append({"src": src, "signature": sig, "slot": slot, "tx_index": idx, "block_time": bt, "owner": o, "dmaga": v,
                    "wsol": m.get(WSOL, 0), "stable": m.get(USDC, 0) + m.get(USDT, 0), "native": nat,
                    "is_signer": o in signers, "is_payer": o == keys[0], "other_opp": ",".join(sorted(opp))[:200]})


def main():
    wt = pq.ParquetWriter(OUT / "a02_tx.parquet", TX, compression="zstd")
    wa = pq.ParquetWriter(OUT / "a02_acct.parquet", ACCT, compression="zstd")
    wo = pq.ParquetWriter(OUT / "a02_own.parquet", OWN, compression="zstd")
    labels = [("curve", "full_curve")]
    for src in ("pool", "mint", "venue"):
        labels += [(src, f"full_{src}/{p.name}") for p in sorted((RAW / f"full_{src}").iterdir()) if not p.name.startswith("._")]
    t0 = time.time()
    n = 0
    report = open(OUT / "a02_cursors.jsonl", "w")
    bt, ba, bo = [], [], []

    def flush():
        nonlocal bt, ba, bo
        if bt:
            wt.write_table(pa.Table.from_pylist(bt, schema=TX))
        if ba:
            wa.write_table(pa.Table.from_pylist(ba, schema=ACCT))
        if bo:
            wo.write_table(pa.Table.from_pylist(bo, schema=OWN))
        bt, ba, bo = [], [], []

    for i, (src, label) in enumerate(labels):
        d = RAW / label
        cur = json.loads((d / "cursor.json").read_text())
        nl = 0
        for p in sorted(d.glob("p*.jsonl.gz")):
            with gzip.open(p, "rt") as f:
                for line in f:
                    parse(json.loads(line), src, label, bt, ba, bo)
                    nl += 1
                    if len(bt) >= 20000:
                        flush()
        report.write(json.dumps({"label": label, "src": src, "n_lues": nl, "n_curseur": cur["n"], "complete": cur["complete"],
                                 "filters": cur.get("filters"), "address": cur["address"], "page": cur["page"]}) + "\n")
        report.flush()
        n += nl
        if i % 50 == 0:
            print(i, len(labels), n, round(time.time() - t0), flush=True)
    flush()
    wt.close(); wa.close(); wo.close()
    print("FIN", n, round(time.time() - t0), flush=True)


if __name__ == "__main__":
    main()
