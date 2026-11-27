"""Détail des changements d'état de b298 sur BSC : pour chaque bloc trouvé par s20_bisect, tx du bloc envoyées par ou vers
l'adresse (eth_getBlockByNumber complet) et journaux Transfer qui la touchent (eth_getLogs sur ce seul bloc), par le nœud
archive public thirdweb (cache). Sortie : data/bsc_<a6>_block_details.json"""
import sys, os, csv, json
sys.path.insert(0, os.path.dirname(__file__))
import nt_lib as N
import hashlib, time, urllib.request
RPCS = ["https://56.rpc.thirdweb.com", "https://bsc-mainnet.gateway.tatum.io"]

def one(method, params):
    """Un appel, en cache ; alterne deux nœuds archive publics et attend sur 429 (pas de lot : tatum les refuse sans abonnement)."""
    body = json.dumps({"jsonrpc": "2.0", "id": 1, "method": method, "params": params})
    key = hashlib.sha256(("bsc one " + body).encode()).hexdigest(); p = N.E._cache(key)
    if p.exists(): return json.loads(p.read_bytes())["result"]
    err = None
    for i in range(14):
        try:
            req = urllib.request.Request(RPCS[i % 2], data=body.encode(), headers={"content-type": "application/json", "user-agent": "dmaga-research/1.0"})
            raw = urllib.request.urlopen(req, timeout=90).read(); d = json.loads(raw)
            if d.get("result") is not None:
                N.E._store(key, "bsc " + method + " " + json.dumps(params)[:120], raw); time.sleep(0.4); return d["result"]
            err = str(d.get("error"))[:200]
        except Exception as e:
            err = repr(e)
        time.sleep(2 + 3 * (i // 2))
    raise RuntimeError(f"{method}: {err}")
T = "0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef"

if __name__ == "__main__":
    a = sys.argv[1].lower(); pad = "0x" + a[2:].rjust(64, "0")
    ch = list(csv.DictReader(open(N.ROOT / f"data/bsc_{a[:6]}_state_changes.csv")))
    # priorité : 2024-2025, puis entrées sans tx signée (financements), puis le reste ; le résultat est écrit au fil de l'eau
    pri = lambda r: (0 if int(r["block"]) >= 37000000 else (1 if int(r["d_nonce"]) == 0 else 2), int(r["block"]))
    blocks = [int(r["block"]) for r in sorted(ch, key=pri)]
    out = {}
    for b in blocks:
        blk = one("eth_getBlockByNumber", [hex(b), True])
        l1 = one("eth_getLogs", [{"fromBlock": hex(b), "toBlock": hex(b), "topics": [T, pad]}])
        l2 = one("eth_getLogs", [{"fromBlock": hex(b), "toBlock": hex(b), "topics": [T, None, pad]}])
        txs = [t for t in blk["transactions"] if (t.get("from") or "").lower() == a or (t.get("to") or "").lower() == a]
        out[b] = dict(ts=int(blk["timestamp"], 16), txs=txs, logs=l1 + l2)
        (N.ROOT / f"data/bsc_{a[:6]}_block_details.json").write_text(json.dumps(out))
    (N.ROOT / f"data/bsc_{a[:6]}_block_details.json").write_text(json.dumps(out))
    n_own = sum(1 for v in out.values() for t in v["txs"] if t["from"].lower() == a)
    unexplained = [b for b, v in out.items() if not v["txs"] and not v["logs"]]
    print(len(out), "blocs ;", n_own, "tx signées ;", sum(len(v["logs"]) for v in out.values()), "journaux Transfer ; blocs sans tx ni journal :", unexplained)
