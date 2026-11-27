"""Lit sur SQD Portal (sans clé) les tx, journaux et traces d'une adresse dans des blocs donnés (fenêtres serrées autour des
changements d'état trouvés par s20_bisect). Pagination de flux : on reprend à dernier_bloc+1 jusqu'à toBlock (doc SQD).
Réponses brutes en cache. Usage : python3 -I s22_sqd_blocks.py <dataset> <adresse> <csv_changements>"""
import sys, os, json, csv, hashlib, time, urllib.request, urllib.error
sys.path.insert(0, os.path.dirname(__file__))
import nt_lib as N

def stream(dataset, q):
    url = f"https://portal.sqd.dev/datasets/{dataset}/stream"; out = []; fb = q["fromBlock"]
    while fb <= q["toBlock"]:
        body = json.dumps(dict(q, fromBlock=fb)); key = hashlib.sha256(("sqd " + dataset + body).encode()).hexdigest(); p = N.E._cache(key)
        if p.exists(): raw = p.read_bytes()
        else:
            for i in range(12):
                try:
                    req = urllib.request.Request(url, data=body.encode(), headers={"content-type": "application/json", "accept-encoding": "identity"})
                    with urllib.request.urlopen(req, timeout=120) as r:
                        code = r.status; raw = r.read()
                    if code == 204: raw = b""
                    break
                except urllib.error.HTTPError as e:
                    if e.code in (429, 529, 503, 502): time.sleep(int(e.headers.get("Retry-After") or 3) + 2 * i); continue
                    raise
                except Exception:
                    time.sleep(3 + 2 * i)
            else:
                raise RuntimeError("SQD indisponible")
            N.E._store(key, "sqd " + dataset + " " + body[:150], raw); time.sleep(0.6)
        lines = [json.loads(l) for l in raw.decode().splitlines() if l.strip()]
        if not lines: break
        out += lines; fb = lines[-1]["header"]["number"] + 1
    return out

def query(a, fb, tb):
    pad = "0x" + a[2:].rjust(64, "0")
    return {"type": "evm", "fromBlock": fb, "toBlock": tb,
            "fields": {"block": {"number": True, "timestamp": True}, "transaction": {"hash": True, "from": True, "to": True, "value": True, "nonce": True, "status": True, "sighash": True, "transactionIndex": True},
                       "log": {"address": True, "topics": True, "data": True, "transactionHash": True, "logIndex": True, "transactionIndex": True},
                       "trace": {"type": True, "callFrom": True, "callTo": True, "callValue": True, "transactionIndex": True}},
            "transactions": [{"from": [a], "logs": True, "traces": True}, {"to": [a]}],
            "logs": [{"topic1": [pad], "transaction": True}, {"topic2": [pad], "transaction": True}],
            "traces": [{"callTo": [a], "transaction": True}]}

if __name__ == "__main__":
    ds, a, f = sys.argv[1], sys.argv[2].lower(), sys.argv[3]
    blocks = sorted({int(r["block"]) for r in csv.DictReader(open(f))})
    wins = []
    for b in blocks:
        if wins and b - wins[-1][1] <= 200: wins[-1][1] = b
        else: wins.append([b, b])
    allb = []
    for fb, tb in wins: allb += stream(ds, query(a, fb, tb))
    txs = {}
    for blk in allb:
        for t in blk.get("transactions", []): txs[t["hash"]] = dict(t, block=blk["header"]["number"], ts=blk["header"]["timestamp"])
    p = N.RAW / f"sqd_{ds}_{a[:6]}.json"; p.write_text(json.dumps(allb))
    print(len(wins), "fenêtres,", len(allb), "blocs,", len(txs), "tx ;", sum(1 for t in txs.values() if t["from"].lower() == a), "signées par l'adresse")
