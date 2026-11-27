#!/usr/bin/env python3
"""Auditeur A. Deux ventes où le signataire ne reçoit presque rien : qui reçoit le SOL ? 2 getTransaction (total réseau 295 sur 300). Aucune clé écrite."""
import json, sys
sys.path.insert(0, "REDACTED_HOME/Projects/Dark-MAGA-Investigation")
from dmaga.helius import Helius
h = Helius(rps=2)
WSOL = "So11111111111111111111111111111111111111112"
for sig in ("5au4mKnXzBtp64qHbD1bJvNaqPYko38F8Mp7J7D7cwcobW6KdP9sXtvjai1r6xEnMe4eHFGeNEbrKvXv8gAVgZbW", "3dHETe5BTJBx9MM6NVrvaML1zxhtez1ctNu9c5k93DpxAu5Q2i3XrmPHbtbrQPyWSc9iCjKX6uULkZeqb83DCPRG"):
    t = h.call("getTransaction", [sig, {"encoding": "jsonParsed", "maxSupportedTransactionVersion": 1, "commitment": "finalized"}])
    keys = [k["pubkey"] for k in t["transaction"]["message"]["accountKeys"]]
    signers = [k["pubkey"] for k in t["transaction"]["message"]["accountKeys"] if k.get("signer")]
    nat = sorted(((q - p) / 1e9, keys[i]) for i, (p, q) in enumerate(zip(t["meta"]["preBalances"], t["meta"]["postBalances"])) if q != p)
    d = {}
    for b in t["meta"].get("preTokenBalances") or []:
        k = (b["mint"], b.get("owner"))
        d[k] = d.get(k, 0) - int(b["uiTokenAmount"]["amount"])
    for b in t["meta"].get("postTokenBalances") or []:
        k = (b["mint"], b.get("owner"))
        d[k] = d.get(k, 0) + int(b["uiTokenAmount"]["amount"])
    print(sig[:12], "signataires", signers, "t", t["blockTime"])
    print("  natif", nat[:3], nat[-4:])
    print("  jetons", sorted(((v, k[0][:6], k[1]) for k, v in d.items() if v), key=lambda x: x[0])[:6], sorted(((v, k[0][:6], k[1]) for k, v in d.items() if v), key=lambda x: x[0])[-4:])
    print("  programmes", sorted({i.get("programId")[:8] for i in t["transaction"]["message"]["instructions"]}))
