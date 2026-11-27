#!/usr/bin/env python3
"""Auditeur A. Liste brute des signatures vers parquet, en flux. Aucun import de dmaga.normalize ni dmaga.pnl."""
import gzip, json, sys, time
from pathlib import Path
import pyarrow as pa, pyarrow.parquet as pq

RAW = Path("/Volumes/VERBATIM HD/Dark-MAGA-Investigation/raw")
OUT = Path("/Volumes/VERBATIM HD/Dark-MAGA-Investigation/audits_work/A")
SCHEMA = pa.schema([("signature", pa.string()), ("slot", pa.int64()), ("tx_index", pa.int64()), ("block_time", pa.int64()),
                    ("failed", pa.bool_()), ("err", pa.string()), ("page", pa.int32())])
for label in sys.argv[1:] or ["sigs_curve", "sigs_pool", "sigs_mint"]:
    t0 = time.time()
    d = RAW / label
    w = pq.ParquetWriter(OUT / f"{label}.parquet", SCHEMA, compression="zstd")
    buf, n, nfail, non_mono, last = [], 0, 0, 0, (0, -1)
    pages = sorted(p for p in d.glob("p*.jsonl.gz"))
    for p in pages:
        pg = int(p.name[1:7])
        with gzip.open(p, "rt") as f:
            for line in f:
                r = json.loads(line)
                k = (r["slot"], r.get("transactionIndex") if r.get("transactionIndex") is not None else -1)
                if k < last:
                    non_mono += 1
                last = k
                e = r.get("err")
                buf.append({"signature": r["signature"], "slot": r["slot"], "tx_index": r.get("transactionIndex"),
                            "block_time": r.get("blockTime"), "failed": e is not None,
                            "err": json.dumps(e, separators=(",", ":"))[:60] if e is not None else None, "page": pg})
                n += 1
                nfail += e is not None
        if len(buf) >= 100_000:
            w.write_table(pa.Table.from_pylist(buf, schema=SCHEMA))
            buf = []
    if buf:
        w.write_table(pa.Table.from_pylist(buf, schema=SCHEMA))
    w.close()
    cur = json.loads((d / "cursor.json").read_text())
    print(json.dumps({"label": label, "pages_files": len(pages), "n_lues": n, "n_curseur": cur["n"], "complete": cur["complete"],
                      "echouees": nfail, "non_monotone": non_mono, "duree_s": round(time.time() - t0)}), flush=True)
