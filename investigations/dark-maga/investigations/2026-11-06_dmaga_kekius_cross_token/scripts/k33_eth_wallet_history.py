"""Historique complet d'adresses Ethereum (txlist, internes, ERC-20) via Routescan sans clé, cache brut, CSV par adresse."""
import csv, sys
from k_lib import DATA, utc
import ev_lib


def history(a):
    a = a.lower()
    rows = []
    for x in ev_lib.pull(a, "txlist"):
        rows.append(("tx", x["timeStamp"], x["hash"], x["from"], x["to"], "ETH", int(x["value"]) / 1e18, x.get("functionName", "")[:40], x["isError"]))
    for x in ev_lib.pull(a, "txlistinternal"):
        rows.append(("internal", x["timeStamp"], x["hash"], x["from"], x["to"], "ETH", int(x["value"]) / 1e18, "", x.get("isError", "0")))
    for x in ev_lib.pull(a, "tokentx"):
        rows.append(("erc20", x["timeStamp"], x["hash"], x["from"], x["to"], x["tokenSymbol"], int(x["value"]) / 10 ** int(x["tokenDecimal"] or 0), x["contractAddress"], ""))
    rows.sort(key=lambda r: int(r[1]))
    out = DATA / "eth_history" / f"{a}.csv"
    out.parent.mkdir(exist_ok=True)
    with open(out, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["kind", "time_utc", "tx", "from", "to", "asset", "amount", "info", "is_error"])
        for r in rows:
            w.writerow([r[0], utc(r[1]), *r[2:]])
    return rows


if __name__ == "__main__":
    for a in sys.argv[1:]:
        print(a, len(history(a)))
