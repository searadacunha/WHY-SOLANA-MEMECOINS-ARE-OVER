"""Même adresse EVM (donc même clé) sur d'autres chaînes : nonce et solde actuels par RPC public sans clé. Lecture d'état courant, non mise en cache.
Sortie : ../evidence/s60_crosschain.json"""
import json, urllib.request
RPCS = {"base": "https://base-rpc.publicnode.com", "bsc": "https://bsc-rpc.publicnode.com", "arbitrum": "https://arbitrum-one-rpc.publicnode.com",
        "polygon": "https://polygon-bor-rpc.publicnode.com", "ethereum": "https://ethereum-rpc.publicnode.com"}
A = {"b947": "0xb947bf7f409e998b28f8e218802fc9575c3c8c57", "b298": "0xb29826d809aa04d2ead6f2310d8965a45b87fa67",
     "2d86": "0x2d86499a410a9ac2139833ba8d6942b8a8700a7b", "86f9": "0x86f99097c563e84dd5190f3e85f6a2988f1c47a5",
     "relay_4978": "0x4978cd7e5a3565cafcc88a105940b0ea01adc04d", "mexc_dep_311e": "0x311ef6b5953ae605dbe469e6566280f0514d3d2e"}
def call(url, m, p):
    req = urllib.request.Request(url, data=json.dumps({"jsonrpc": "2.0", "id": 1, "method": m, "params": p}).encode(), headers={"content-type": "application/json", "user-agent": "dmaga-research/1.0"})
    return json.loads(urllib.request.urlopen(req, timeout=30).read()).get("result")
out = {}
for k, a in A.items():
    for c, u in RPCS.items():
        try:
            n = int(call(u, "eth_getTransactionCount", [a, "latest"]), 16); b = int(call(u, "eth_getBalance", [a, "latest"]), 16) / 1e18
            code = call(u, "eth_getCode", [a, "latest"])
            out[f"{k}.{c}"] = dict(nonce=n, balance_native=b, code_len=(len(code) - 2) // 2 if code else None)
        except Exception as e:
            out[f"{k}.{c}"] = dict(error=repr(e)[:120])
        print(k, c, out[f"{k}.{c}"], flush=True)
json.dump(out, open("../evidence/s60_crosschain.json", "w"), indent=1)
