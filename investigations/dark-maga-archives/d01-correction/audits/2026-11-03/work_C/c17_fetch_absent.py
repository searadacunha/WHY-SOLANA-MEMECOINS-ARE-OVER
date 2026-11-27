#!/usr/bin/env python3
"""Telecharge en jsonParsed les transactions >= 1 M vues dans flows/dmaga_all mais absentes du brut mint/pool/venue."""
import csv, gzip, json, time
from pathlib import Path
from dmaga.helius import Helius
W=Path(__file__).resolve().parent
NET=Path("/Volumes/VERBATIM HD/Dark-MAGA-Investigation/audits_work/C/net")
h=Helius()
sigs=[r['sig'] for r in csv.DictReader(open(W/'flows_absent_raw_1M.csv'))]
sigs=list(dict.fromkeys(sigs))
out=gzip.open(NET/'absent_1M.jsonl.gz','wt',compresslevel=6)
n=0
for s in sigs:
    t=h.call("getTransaction",[s,{"encoding":"jsonParsed","maxSupportedTransactionVersion":1}])
    assert t is not None, s
    out.write(json.dumps(t,separators=(',',':'))+"\n"); n+=1
out.close()
with open(W/'credits.csv','a') as f:
    f.write(f"{time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime())},getTransaction_x{n},absent,{n}\n")
print('ok',n,dict(h.stats))
