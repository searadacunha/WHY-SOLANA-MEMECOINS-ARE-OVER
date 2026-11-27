#!/usr/bin/env python3
"""Auditeur A. Reste du budget réseau (24 getTransaction, total 300) : que sont les transferts vus par les seuls flux ? Aucune clé écrite."""
import json, sys
sys.path.insert(0, "REDACTED_HOME/Projects/Dark-MAGA-Investigation")
from dmaga.helius import Helius
OUT = "REDACTED_HOME/Projects/Dark-MAGA-Investigation/audits/2026-11-03/work_A/out"
G = json.load(open("REDACTED_HOME/Projects/Dark-MAGA-Investigation/data/prevent_groups.json"))[0]["edges_top"]
E5 = json.load(open(OUT + "/a26_group_absent.json"))  # arêtes du groupe de 33 absentes du brut a02
S = [[e["sig"], e["src"], e["dst"], e["M"] * 1e6] for e in E5][:5]
S += json.load(open(OUT + "/a26_sample.json"))[:24 - len(S)]
MINT = "7D7BRcBYepfi77vxySapmeqRNN1wsBBxnFPJGbH5pump"
h = Helius(rps=3)
res = []
for sig, src, dst, q in S:
    t = h.call("getTransaction", [sig, {"encoding": "jsonParsed", "maxSupportedTransactionVersion": 1, "commitment": "finalized"}])
    if t is None:
        res.append({"sig": sig, "absente": True})
        continue
    msg = t["transaction"]["message"]
    keys = [k["pubkey"] for k in msg["accountKeys"]]
    progs = sorted({i.get("programId") for i in msg["instructions"]} | {i.get("programId") for g in (t["meta"].get("innerInstructions") or []) for i in g["instructions"]})
    types = sorted({(i.get("parsed") or {}).get("type") for i in msg["instructions"] if isinstance(i.get("parsed"), dict)})
    bal = {}
    for b in t["meta"].get("preTokenBalances") or []:
        if b["mint"] == MINT:
            bal[b.get("owner")] = bal.get(b.get("owner"), 0) - int(b["uiTokenAmount"]["amount"])
    for b in t["meta"].get("postTokenBalances") or []:
        if b["mint"] == MINT:
            bal[b.get("owner")] = bal.get(b.get("owner"), 0) + int(b["uiTokenAmount"]["amount"])
    res.append({"sig": sig, "src": src, "dst": dst, "M": q / 1e6, "delta_src": bal.get(src), "delta_dst": bal.get(dst), "blockTime": t.get("blockTime"), "err": t["meta"].get("err"), "mint_dans_cles": MINT in keys, "version": t.get("version"), "progs": progs, "types_top": types, "signers": [k["pubkey"] for k in msg["accountKeys"] if k.get("signer")]})
json.dump(res, open(OUT + "/a31_network_hidden.json", "w"), indent=0)
print("appels", len(res), dict(h.stats))
import collections
print("mint dans les clés", collections.Counter(r.get("mint_dans_cles") for r in res))
print("programmes", collections.Counter(p for r in res for p in r.get("progs", []) if p).most_common(25))
print("types", collections.Counter(x for r in res for x in r.get("types_top", []) if x).most_common(8))
