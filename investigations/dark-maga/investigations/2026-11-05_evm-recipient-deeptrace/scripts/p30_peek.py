"""Aperçu d'une adresse EVM : premiers et derniers transferts de jetons et tx, avec tags Blockscout. Usage : p30_peek.py <adresse> [n]"""
import sys
sys.path.insert(0, ".")
import ev_lib as E
a = sys.argv[1].lower(); n = int(sys.argv[2]) if len(sys.argv) > 2 else 15
def tg(o):
    t = [x.get("name", "") for x in ((o.get("metadata") or {}).get("tags") or [])]
    return (o.get("name") or "") + ("|" + ",".join(t) if t else "") + ("|ENS:" + o["ens_domain_name"] if o.get("ens_domain_name") else "") + ("|C" if o.get("is_contract") else "")
T, comp = E.bs_all(a, "token-transfers", max_pages=int(sys.argv[3]) if len(sys.argv) > 3 else 40)
X, compx = E.bs_all(a, "transactions", max_pages=int(sys.argv[3]) if len(sys.argv) > 3 else 40)
print(a, "token-transfers", len(T), "complet" if comp else "PARTIEL", "| tx", len(X), "complet" if compx else "PARTIEL")
T.sort(key=lambda x: (x["block_number"], x["log_index"]))
def show(x):
    tok = x["token"]; v = int(x["total"].get("value") or 0) / 10 ** int(tok.get("decimals") or 0)
    d = "OUT" if x["from"]["hash"].lower() == a else "IN "
    cp = x["to"] if d == "OUT" else x["from"]
    print(" ", x["timestamp"][:19], d, x["transaction_hash"], cp["hash"], tg(cp), tok["symbol"], tok["address_hash"][:10], round(v, 6))
for x in T[:n]: show(x)
if len(T) > 2 * n: print("  ...")
for x in T[max(n, len(T) - n):]: show(x)
X.sort(key=lambda x: x["block_number"])
print(" tx propres (premières):")
for x in X[:min(n, 8)]:
    print("  ", x["timestamp"][:19], x["hash"], x["from"]["hash"], tg(x["from"]), "->", (x.get("to") or {}).get("hash"), tg(x.get("to") or {}), int(x["value"]) / 1e18, x.get("method"))
