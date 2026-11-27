"""Lecture rapide de la structure d'activity.jsonl (phase aveugle)."""
import json, collections
from pathlib import Path
EXT = Path("/Volumes/VERBATIM HD/Dark-MAGA-Investigation")
keys = collections.Counter(); n=0; hist_nonempty=0; trunc=0; pages=collections.Counter()
first=None; dmaga=None; types=collections.Counter()
for line in open(EXT/"data/controls/activity.jsonl"):
    r=json.loads(line); n+=1
    keys.update(r.keys())
    if r.get("hist"): 
        hist_nonempty+=1
        if first is None: first=r
    if r.get("truncated"): trunc+=1
    pages[min(r.get("pages",0),3)]+=1
    if r["mint"]=="7D7BRcBYepfi77vxySapmeqRNN1wsBBxnFPJGbH5pump": dmaga=r
print(n, keys, "hist_nonempty",hist_nonempty,"trunc",trunc,pages)
print(json.dumps(first)[:800])
d=dict(dmaga); h=d.pop("hist",None); print(d); print(type(h), len(h)); print(h[:6]); print(h[-3:])
