"""Tous les ordres DLN reçus (FulfilledOrder, receiverDst = A) et créés (CreatedOrder, maker = A) par chaque adresse, sur Ethereum.
Candidats entrants : toute tx où A reçoit un jeton d'un tiers, ou de l'ETH interne venu de DlnDestination ou du forwarder.
Pour 2d86 (15 000 transferts) : seulement les tx dont la méthode ou l'expéditeur a déjà servi à un fill confirmé (biais noté dans UNRESOLVED).
Sortie : ../evidence/dln_orders_evm.csv"""
import csv, os, sys, datetime as dt
sys.path.insert(0, ".")
import ev_lib as E, dln
FWD = "0x663dc15d3c1ac63ff12e45ab68fea3f0a883c251"
A = {"b947": "0xb947bf7f409e998b28f8e218802fc9575c3c8c57", "b298": "0xb29826d809aa04d2ead6f2310d8965a45b87fa67",
     "86f9": "0x86f99097c563e84dd5190f3e85f6a2988f1c47a5", "2d86": "0x2d86499a410a9ac2139833ba8d6942b8a8700a7b"}
keys = sys.argv[1:] or list(A)
rows, seen_methods, seen_takers = [], set(), set()
if keys == ["2d86"] and os.path.exists("../evidence/dln_orders_evm.csv"):  # lancé seul : reprend méthodes et takers déjà confirmés
    prev = list(csv.DictReader(open("../evidence/dln_orders_evm.csv")))
    seen_takers = {r["taker"].lower() for r in prev if r["taker"]}; seen_methods = {"0xc358547e"}
def ts(h):
    t = E.rpc("eth_getBlockByNumber", [E.rpc("eth_getTransactionByHash", [h])["blockNumber"], False])
    return dt.datetime.fromtimestamp(int(t["timestamp"], 16), dt.timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
for k in keys:
    a = A[k]
    T, c1 = E.bs_all(a, "token-transfers"); X, c2 = E.bs_all(a, "transactions"); I, isrc = E.internals(a); c3 = True
    assert c1 and c2 and c3, f"historique incomplet pour {k}"
    tin = [x for x in T if x["to"]["hash"].lower() == a and x["from"]["hash"].lower() != a]
    cand = {x["transaction_hash"]: x.get("method") for x in tin}
    cand.update({x["transaction_hash"]: "internal" for x in I if (x.get("to") or {}).get("hash", "").lower() == a
                 and x["from"]["hash"].lower() in (dln.DLN_DST, FWD) and x.get("success", True)})
    if k == "2d86":
        cand = {h: m for h, m in cand.items() if m in seen_methods or m == "internal"} | \
               {x["transaction_hash"]: x.get("method") for x in tin if x["from"]["hash"].lower() in seen_takers}
    nin = 0
    for h in cand:
        r = E.rpc("eth_getTransactionReceipt", [h])
        for o in dln.fills_in_receipt(r):
            if o["receiverDst"].lower() != a: continue
            nin += 1; seen_takers.add(o["sender"].lower())
            if cand[h] not in (None, "internal"): seen_methods.add(cand[h])
            rows.append(dict(wallet=k, direction="IN", utc=ts(h), tx=h, orderId=o["orderId"], maker=o["makerSrc"], give_chain=o["giveChain"],
                             give_token=o["giveTokenAddress"], give_amount_raw=o["giveAmount"], take_chain=o["takeChain"], take_token=o["takeTokenAddress"],
                             take_amount_raw=o["takeAmount"], receiver=o["receiverDst"], taker=o["sender"], external_call=bool(o["externalCall"])))
    out = {x["hash"] for x in X if x["from"]["hash"].lower() == a and (x.get("to") or {}).get("hash", "").lower() in (dln.DLN_SRC_EVM, FWD) and x.get("status") == "ok"}
    nout = 0
    for h in sorted(out):
        for o in dln.created_in_receipt(E.rpc("eth_getTransactionReceipt", [h])):
            nout += 1
            rows.append(dict(wallet=k, direction="OUT", utc=ts(h), tx=h, orderId=o["orderId"], maker=o["makerSrc"], give_chain=o["giveChain"],
                             give_token=o["giveTokenAddress"], give_amount_raw=o["giveAmount"], take_chain=o["takeChain"], take_token=o["takeTokenAddress"],
                             take_amount_raw=o["takeAmount"], receiver=o["receiverDst"], taker="", external_call=bool(o["externalCall"])))
    print(k, "candidats entrants", len(cand), "fills", nin, "| tx vers DlnSource/forwarder", len(out), "ordres créés", nout, flush=True)
rows.sort(key=lambda r: (r["wallet"], r["utc"]))
mode = "a" if keys == ["2d86"] else "w"
with open("../evidence/dln_orders_evm.csv", mode, newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0])); (w.writeheader() if mode == "w" else None); w.writerows(rows)
print("méthodes de fill vues", sorted(m for m in seen_methods if m)); print("takers vus", len(seen_takers))
