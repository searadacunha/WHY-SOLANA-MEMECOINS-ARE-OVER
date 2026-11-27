#!/usr/bin/env python3
"""Dernière page de RBsneDCL et RBHdGVfD : dates, destinations, expéditeurs. Sortie g56.txt."""
import gzip, json, sys, time, collections
sys.path.insert(0, "audits/2026-11-03/work_G")
from g_lib import parse, NETG
from dmaga.labels import label
iso = lambda t: time.strftime("%Y-%m-%d %H:%M", time.gmtime(t))
sys.stdout = open("audits/2026-11-03/work_G/g56.txt", "w")
for A in ("RBsneDCLZHmbTd3iuNyF2bJkiAoap2yiLuPQSkcAmaz", "RBHdGVfDfMjfU6iUfCb1LczMJcQLx7hGnxbzRsoDNvx"):
    o = collections.Counter(); i = collections.Counter(); bts = []; sg = 0
    for l in gzip.open(NETG + A + ".desc.jsonl.gz", "rt"):
        x = parse(json.loads(l)); bts.append(x["bt"]); sg += A in x["signers"]
        for k, a, m, s, d, r, dc in x["moves"]:
            if a == "SOL" and s == A and d != A: o[d] += r
            if a == "SOL" and d == A and s != A and r >= 1000000: i[s] += r
    print(A, "page récente", iso(min(bts)), "->", iso(max(bts)), "tx", len(bts), "signées", sg, "| sorties", [(k, label(k), round(v / 1e9, 2)) for k, v in o.most_common(5)], "| entrées", [(k, label(k), round(v / 1e9, 2)) for k, v in i.most_common(5)])
