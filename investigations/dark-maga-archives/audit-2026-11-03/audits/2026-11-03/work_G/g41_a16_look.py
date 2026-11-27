#!/usr/bin/env python3
"""A-16 : ce que montrent les pages du programme 3GMsedVP et de 4ToQp55m : signataires, mints, contreparties, frais, journaux. Sortie g41_a16_look.txt"""
import gzip, json, collections, sys, time
sys.path.insert(0, "audits/2026-11-03/work_G")
from g_lib import parse, NETG, MINT
from dmaga.labels import label
iso = lambda t: time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(t))
P = "3GMsedVPsXjWR7HYUvwm1YUpvBC2bTgSkXixm4gMXnPk"; O = "4ToQp55myvfpeprgKuqGbDqyji9Ezm7CZg7QbcTpL33S"
sys.stdout = open("audits/2026-11-03/work_G/g41_a16_look.txt", "w")
for fn in (P + ".jsonl.gz", P + ".desc.jsonl.gz", O + ".jsonl.gz", O + ".desc.jsonl.gz"):
    sig = collections.Counter(); mints = collections.Counter(); progs = collections.Counter(); first = last = None; n = 0; nat = collections.Counter(); ex = None; onat = 0; own = collections.Counter(); logs = collections.Counter()
    for l in gzip.open(NETG + fn, "rt"):
        t = json.loads(l); x = parse(t); n += 1
        first = min(first or x["bt"], x["bt"]); last = max(last or x["bt"], x["bt"])
        for s in x["signers"]: sig[s] += 1
        for (o, m), v in x["tok"].items(): mints[MINT.get(m, m[:10])] += 1; own[o] += 1
        for p in x["progs"]: progs[p] += 1
        for k, v in x["nat"].items():
            if abs(v) > 1e7: nat[k] += v
        for m in t["meta"].get("logMessages") or []:
            if "Program log:" in m: logs[m[13:60]] += 1
        ex = ex or x["sig"]
    print("==", fn[:10], fn[44:], "n", n, iso(first), "->", iso(last), "ex", ex)
    print(" signataires", len(sig), sig.most_common(8))
    print(" mints", mints.most_common(10))
    print(" programmes", [(k[:12], v) for k, v in progs.most_common(8)])
    print(" propriétaires de jetons qui bougent", [(k, v) for k, v in own.most_common(8)])
    print(" natif net au moins 0,01 SOL", [(k, round(v / 1e9, 2), label(k)) for k, v in sorted(nat.items(), key=lambda kv: -abs(kv[1]))[:8]])
    print(" journaux", logs.most_common(8))
