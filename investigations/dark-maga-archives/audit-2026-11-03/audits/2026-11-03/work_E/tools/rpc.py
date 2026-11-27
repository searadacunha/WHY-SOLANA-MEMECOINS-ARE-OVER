"""Lecture publique d'une transaction Solana (RPC public, sans clé). usage: python3 -I rpc.py <signature> <sous-dossier>"""
import hashlib, json, sys, urllib.request
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import e

URL = "https://api.mainnet-beta.solana.com"
sig, sub = sys.argv[1:3]
body = json.dumps({"jsonrpc": "2.0", "id": 1, "method": "getTransaction", "params": [sig, {"encoding": "jsonParsed", "maxSupportedTransactionVersion": 0}]}).encode()
req = urllib.request.Request(URL, data=body, headers={"content-type": "application/json", **e.UA})
raw = urllib.request.urlopen(req, timeout=45).read()
d = e.EV / sub
d.mkdir(parents=True, exist_ok=True)
p = d / f"tx_{sig[:16]}.json"
p.write_bytes(raw)
with e.MAN.open("a") as f:
    f.write(json.dumps({"url": URL + " getTransaction " + sig, "file": str(p.relative_to(e.W)), "http": 200, "collected_utc": e.now(), "sha256": hashlib.sha256(raw).hexdigest(), "bytes": len(raw), "note": "RPC public"}) + "\n")
j = json.loads(raw).get("result")
if not j:
    print("vide", raw[:300])
    sys.exit(0)
from datetime import datetime, timezone
print(sig[:16], datetime.fromtimestamp(j["blockTime"], timezone.utc).isoformat())
msg = j["transaction"]["message"]
print("signataires", [a["pubkey"] for a in msg["accountKeys"] if a.get("signer")])
for ins in msg["instructions"]:
    print(ins.get("program"), (ins.get("parsed") or {}).get("type") if isinstance(ins.get("parsed"), dict) else None, json.dumps((ins.get("parsed") or {}).get("info") if isinstance(ins.get("parsed"), dict) else None)[:400])
