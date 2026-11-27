"""Jambe WETH des pools KEKIUS (Uniswap V2 0xfff8d5…, V3 0xa25423…) sur la même fenêtre : coût et produit en ETH par tx."""
import csv, gzip, io
from k_lib import DATA, T_END
import ev_lib

WETH = "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2"
POOLS = {"v2": "0xfff8d5fff6ee3226fa2f5d7d5d8c3ff785be9c74", "v3": "0xa2542303c9a01c011da9106128d9b0838e6c3e57"}
START = 21397776
END = int(ev_lib.rs(module="block", action="getblocknobytime", timestamp=T_END, closest="before"))
buf = io.StringIO()
w = csv.writer(buf)
w.writerow(["pool", "block", "time", "tx", "from", "to", "raw"])
for name, pool in POOLS.items():
    b, n, OFF = START, 0, 10000
    while True:
        res = ev_lib.rs(module="account", action="tokentx", address=pool, contractaddress=WETH, startblock=b, endblock=END,
                        page=1, offset=OFF, sort="asc") or []
        full = len(res) == OFF
        last = int(res[-1]["blockNumber"]) if res else b
        keep = [r for r in res if not full or int(r["blockNumber"]) < last]
        assert keep or not full
        for r in keep:
            assert r["contractAddress"].lower() == WETH
            w.writerow([name, r["blockNumber"], r["timeStamp"], r["hash"], r["from"], r["to"], r["value"]])
        n += len(keep)
        if not full:
            break
        b = last
    print(name, n, flush=True)
(DATA / "eth_kekius_pool_weth.csv.gz").write_bytes(gzip.compress(buf.getvalue().encode(), 9))
