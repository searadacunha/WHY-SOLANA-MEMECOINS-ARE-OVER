"""KEKIUS Ethereum : tous les transferts du contrat, du bloc de création au 04/01/2025 00:00 UTC.

Source : Routescan (API compatible Etherscan, sans clé), action tokentx filtrée par contrat, fenêtres de blocs ; cache brut
dans EV_RAW. Le RPC public publicnode refuse désormais les requêtes d'archive sans jeton (constaté le 06/11/2026).
Une page pleine reprend au dernier bloc lu, relu en entier : ni doublon ni trou à la frontière."""
import csv, gzip, io
from k_lib import DATA, ETH_KEKIUS, T_END
import ev_lib

START = 21397776
END = int(ev_lib.rs(module="block", action="getblocknobytime", timestamp=T_END, closest="before"))
out, b, OFF = [], START, 10000
while True:
    res = ev_lib.rs(module="account", action="tokentx", contractaddress=ETH_KEKIUS, startblock=b, endblock=END,
                    page=1, offset=OFF, sort="asc") or []
    if len(res) < OFF:
        out += res
        break
    last = int(res[-1]["blockNumber"])
    keep = [r for r in res if int(r["blockNumber"]) < last]
    assert keep, f"bloc {last} : plus de {OFF} transferts"
    out += keep
    b = last
    print(len(out), last, flush=True)
assert all(r["contractAddress"].lower() == ETH_KEKIUS for r in out)
buf = io.StringIO()
w = csv.writer(buf)
w.writerow(["block", "time", "tx", "tx_index", "from", "to", "raw", "method"])
for r in out:
    w.writerow([r["blockNumber"], r["timeStamp"], r["hash"], r["transactionIndex"], r["from"], r["to"], r["value"], r.get("methodId", "")])
(DATA / "eth_kekius_transfers.csv.gz").write_bytes(gzip.compress(buf.getvalue().encode(), 9))
print("transferts", len(out), "fin", END)
