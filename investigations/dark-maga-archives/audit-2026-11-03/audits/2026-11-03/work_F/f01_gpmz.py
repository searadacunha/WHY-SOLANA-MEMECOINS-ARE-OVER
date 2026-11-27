"""Lecture seule du brut : quels comptes et quels mints de GpMZbSM2 bougent avec sa réserve DMAGA, avec ou sans le pool Raydium v4."""
import gzip, json
from collections import Counter
import duckdb
from dmaga.config import MINT, RAW
from dmaga.normalize import _keys, token_deltas
D = "/Volumes/VERBATIM HD/Dark-MAGA-Investigation/audits_work/D"
GP = "GpMZbSM2GgvTKHJirzeGfMFoaZ8UR2X7F4v8vHTvxFbL"; VD = "5HuEsLbebeuottMsFW3hHcXTrKVsu3WUNSQnSr6aX4eL"; VS = "3p7DbnWekWjtMQkey6fp1emdwXbAAxecnYuD5eU9ZZPH"
con = duckdb.connect(":memory:", config={"memory_limit": "500MB", "threads": 2, "temp_directory": D + "/duck"})
sigs = {r[0] for r in con.execute(f"SELECT DISTINCT sig FROM read_parquet('{D}/d01_acct.parquet') WHERE owner='{GP}'").fetchall()}
sl = con.execute(f"SELECT src,slice,count(DISTINCT sig) FROM read_parquet('{D}/d01_tx.parquet') WHERE sig IN (SELECT DISTINCT sig FROM read_parquet('{D}/d01_acct.parquet') WHERE owner='{GP}') GROUP BY 1,2 ORDER BY 3 DESC").fetchall()
print("signatures", len(sigs), "tranches", len(sl), sl[:6])
print("sans vault v4", con.execute(f"SELECT count(DISTINCT sig) FROM read_parquet('{D}/d01_tx.parquet') WHERE sig IN (SELECT DISTINCT sig FROM read_parquet('{D}/d01_acct.parquet') WHERE owner='{GP}') AND vs_d=0 AND vt_d=0").fetchone())
acc, shape, ex, opp, seen = Counter(), Counter(), {}, Counter(), set()
for src, sc, _ in sl:
    d = RAW / f"full_{src}" / sc if src != "curve" else RAW / "full_curve"
    for p in sorted(d.glob("p*.jsonl.gz")):
        if p.name.startswith("._"): continue
        for line in gzip.open(p, "rt"):
            t = json.loads(line); s = t["transaction"]["signatures"][0]
            if s not in sigs or s in seen or t["meta"].get("err") is not None: continue
            seen.add(s)
            ds = token_deltas(t, _keys(t))
            g = [x for x in ds if x["owner"] == GP]
            for x in g: acc[(x["account"], x["mint"])] += 1
            dm = sum(x["delta"] for x in g if x["mint"] == MINT)
            v4 = any(x["account"] in (VD, VS) for x in ds)
            others = sorted({x["mint"][:6] for x in g if x["mint"] != MINT})
            for x in g:
                if x["mint"] != MINT and dm and (x["delta"] > 0) != (dm > 0): opp[x["mint"]] += 1
            k = ("v4" if v4 else "sans_v4", tuple(others)[:3])
            shape[k] += 1
            ex.setdefault(k, s)
print("lues", len(seen))
print("comptes (compte, mint) n", acc.most_common(12))
print("mints en sens opposé au delta DMAGA de GpMZ", opp.most_common(10))
for k, n in shape.most_common(25): print(n, k, ex[k])
