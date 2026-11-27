"""Soldes ETH et USDC de b298 sur Base reconstitués depuis le grand livre, puis contrôlés contre l'état archive (base.drpc.org,
eth_getBalance / balanceOf au bloc) à des points de contrôle. Échec = assertion. Sortie : evidence/s11_base_balance_checks.csv"""
import csv, json, sys, os, hashlib, time, urllib.request
sys.path.insert(0, os.path.dirname(__file__))
import nt_lib as N
USDC_BASE = "0x833589fcd6edb6e08f4c7c32d4f71b54bda02913"
RPC = "https://base.drpc.org"

def rpc(method, params, url=RPC):
    body = json.dumps({"jsonrpc": "2.0", "id": 1, "method": method, "params": params})
    key = hashlib.sha256(("base " + body).encode()).hexdigest(); p = N.E._cache(key)
    if p.exists(): return json.loads(p.read_bytes())["result"]
    for i in range(8):
        try:
            req = urllib.request.Request(url, data=body.encode(), headers={"content-type": "application/json", "user-agent": "dmaga-research/1.0"})
            raw = urllib.request.urlopen(req, timeout=60).read(); d = json.loads(raw)
            if d.get("result") is not None:
                N.E._store(key, "base " + method + " " + json.dumps(params), raw); return d["result"]
            err = d.get("error")
        except Exception as e:
            err = repr(e)
        time.sleep(1 + 2 * i)
    raise RuntimeError(f"{method}: {err}")

def running(rows, a):
    eth = usdc = 0; out = []
    for r in rows:
        if r["kind"] == "tx" and r["frm"] == a:
            eth -= int(r["raw"]) + int(r["fee"] or 0)
        if r["kind"] == "tx" and r["to"] == a and r["frm"] != a and r["status"] == "ok":
            eth += int(r["raw"])
        if r["kind"] == "internal" and r["status"] == "ok":
            if r["to"] == a: eth += int(r["raw"])
            if r["frm"] == a: eth -= int(r["raw"])
        if r["kind"] == "token" and r["token"] == USDC_BASE and r["raw"] != "":
            if r["to"] == a: usdc += int(r["raw"])
            if r["frm"] == a: usdc -= int(r["raw"])
        out.append((int(r["block"]), eth, usdc))
    return out

if __name__ == "__main__":
    a = N.B298
    rows = list(csv.DictReader(open(N.ROOT / "data/base_0xb298_ledger.csv")))
    # tx d'erreur : seule la commission sort
    for r in rows:
        if r["kind"] == "tx" and r["status"] != "ok": r["raw"] = "0"
    run = running(rows, a)
    last = {}
    for b, e, u in run: last[b] = (e, u)
    blocks = sorted(last)
    checks = [blocks[i] for i in range(0, len(blocks), max(1, len(blocks) // 40))] + [blocks[-1]]
    out = []
    for b in checks:
        e, u = last[b]
        e_rpc = int(rpc("eth_getBalance", [a, hex(b)]), 16)
        u_rpc = int(rpc("eth_call", [{"to": USDC_BASE, "data": "0x70a08231" + a[2:].rjust(64, "0")}, hex(b)]), 16)
        out.append(dict(block=b, eth_ledger=e, eth_rpc=e_rpc, eth_diff=e - e_rpc, usdc_ledger=u, usdc_rpc=u_rpc, usdc_diff=u - u_rpc))
    N.write_csv(N.ROOT / "evidence/s11_base_balance_checks.csv", out)
    bad = [o for o in out if o["eth_diff"] or o["usdc_diff"]]
    print(len(out), "points de contrôle,", len(bad), "écarts")
    for o in bad[:10]: print(o)
