#!/usr/bin/env python3
"""Teste les clés du pool sans les afficher : getHealth puis un getTransactionsForAddress minimal. Sortie : empreinte courte et statut."""
import hashlib
import json
import urllib.error
import urllib.request

from dmaga.config import MINT, helius_keys, scrub


def call(key, method, params):
    body = json.dumps({"jsonrpc": "2.0", "id": 1, "method": method, "params": params}).encode()
    req = urllib.request.Request(f"https://mainnet.helius-rpc.com/?api-key={key}", data=body, headers={"content-type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            p = json.load(r)
        return "ok" if "result" in p else scrub(str(p.get("error"))[:120])
    except urllib.error.HTTPError as e:
        return f"HTTP {e.code} {scrub(e.read()[:120].decode(errors='replace'))}"
    except Exception as e:  # le texte d'exception peut contenir l'URL : on ne garde que le type
        return type(e).__name__


keys = helius_keys()
print("clés lues :", len(keys))
for k in keys:
    f8 = hashlib.sha256(k.encode()).hexdigest()[:8]
    print(f8, "getHealth:", call(k, "getHealth", []), "| gTFA:", call(k, "getTransactionsForAddress", [MINT, {"limit": 1, "transactionDetails": "signatures"}]), flush=True)
