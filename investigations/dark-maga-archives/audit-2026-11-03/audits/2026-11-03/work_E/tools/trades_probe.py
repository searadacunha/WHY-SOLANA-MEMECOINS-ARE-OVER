"""Lecture seule : achats d'un montant donné dans une fenêtre, dans trades.parquet.
usage: python3.12 -I trades_probe.py <debut_iso> <fin_iso> <sol_min> <sol_max>
"""
import sys
sys.path.insert(0, "/Volumes/VERBATIM HD/Dark-MAGA-Investigation/pylib")
import pyarrow.dataset as ds
import pyarrow as pa
from datetime import datetime, timezone

a, b, lo, hi = sys.argv[1:5]
d = ds.dataset("/Volumes/VERBATIM HD/Dark-MAGA-Investigation/data/trades.parquet")
ty = d.schema.field("block_time").type
print(ty)
ta, tb = [datetime.fromisoformat(x).replace(tzinfo=timezone.utc) for x in (a, b)]
if pa.types.is_integer(ty):
    fa, fb = int(ta.timestamp()), int(tb.timestamp())
else:
    fa, fb = pa.scalar(ta, type=ty), pa.scalar(tb, type=ty)
t = d.to_table(columns=["signature", "block_time", "kind", "owner", "token_delta", "sol_lamports", "venue"], filter=(ds.field("block_time") >= fa) & (ds.field("block_time") <= fb))
rows = t.to_pylist()
print("lignes fenêtre", len(rows))
for r in sorted(rows, key=lambda r: str(r["block_time"])):
    sol = abs(r["sol_lamports"] or 0) / 1e9
    if float(lo) <= sol <= float(hi) and (r["token_delta"] or 0) > 0:
        print(r["block_time"], r["owner"], round(sol, 4), r["token_delta"], r["venue"], r["signature"])
