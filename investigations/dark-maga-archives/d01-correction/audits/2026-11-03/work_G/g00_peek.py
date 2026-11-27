#!/usr/bin/env python3
"""Regarde la forme des fichiers bruts : net/<wallet>.jsonl.gz et raw/flows/<wallet>/*.json.gz."""
import gzip, json, os
NET = "/Volumes/VERBATIM HD/Dark-MAGA-Investigation/audits_work/C/net/"
FL = "/Volumes/VERBATIM HD/Dark-MAGA-Investigation/raw/flows/"
W = "8YLEuUtZ4eFMJbf46oNb1CeG6dYFWGyxnQSh9hrgzBzR"
for f in sorted(os.listdir(FL + W)):
    if f.startswith("._"): continue
    d = json.load(gzip.open(FL + W + "/" + f, "rt"))
    print(f, type(d).__name__, (list(d.keys())[:12] if isinstance(d, dict) else len(d)))
    x = d
    if isinstance(d, dict):
        print("   ", json.dumps({k: (v if not isinstance(v, (list, dict)) else (type(v).__name__, len(v))) for k, v in d.items()})[:400])
        for k, v in d.items():
            if isinstance(v, list) and v:
                print("    first", k, json.dumps(v[0])[:600]); break
    elif d:
        print("    first", json.dumps(d[0])[:600])
n = 0
for l in gzip.open(NET + W + ".jsonl.gz", "rt"):
    t = json.loads(l); n += 1
    if n == 1:
        print("net keys", list(t.keys()), "meta", list(t["meta"].keys()))
        print(json.dumps(t)[:1500])
print("net tx", n)
