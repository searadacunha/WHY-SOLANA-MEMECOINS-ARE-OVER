"""Recalcule l'orderId de chaque événement DLN (CreatedOrder de DlnSource, FulfilledOrder de DlnDestination) trouvé dans les
reçus bruts en cache (fixtures, cache local, caches en lecture seule), et le compare à l'orderId émis par le contrat.
Puis contrôle CROSSCHAIN_LINKS.csv : chaque lien doit avoir au moins un événement EVM dont l'orderId recalculé est identique,
avec le même maker et le même receveur que la table. Aucun appel réseau. Sortie : evidence/s13_orderid_check.csv"""
import csv, json, sys, os, collections
sys.path.insert(0, os.path.dirname(__file__))
import nt_lib as N
import dln_orderid as O

SRC = {"0xef4fb24ad0916217251f553c0596f8edc630eb66"}
DST = {"0xe7351fd770a37282b91d153ee690b63579d6dd7f"}
B58 = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"

def b58(b):
    n = int.from_bytes(b, "big"); s = ""
    while n: n, r = divmod(n, 58); s = B58[r] + s
    return "1" * (len(b) - len(b.lstrip(b"\0"))) + s

def addr(chain, b): return b58(b) if chain == 7565164 else "0x" + b.hex()

def receipts():
    """Tous les reçus présents dans les caches, dédoublonnés par hash de tx."""
    roots = [N.FIXTURES, N.NEW_RAW] + [d for r in N.RAW_RO for d in (r / "cache", r)]
    seen = {}
    for root in roots:
        if not root.is_dir(): continue
        for p in root.glob("[0-9a-f][0-9a-f]/*.json"):
            try: d = json.loads(p.read_bytes())
            except Exception: continue
            res = d.get("result") if isinstance(d, dict) else None
            items = [x.get("result") for x in d] if isinstance(d, list) else [res]
            for r in items:
                if isinstance(r, dict) and "logs" in r and "transactionHash" in r:
                    seen.setdefault(r["transactionHash"].lower(), r)
    return seen

def check(rc):
    out = []
    for l in rc["logs"]:
        a = l["address"].lower()
        if a not in SRC | DST or len(l["data"]) < 2 + 64 * 20: continue
        try: o, emitted = O.raw_order(l["data"])
        except Exception: continue
        if o["giveChainId"] > 10 ** 12 or o["takeChainId"] > 10 ** 12: continue  # pas un Order (autre événement du contrat)
        ok = O.order_id(o) == emitted
        ok_h = (not ok) and len(o["externalCall"]) == 32 and "0x" + O.keccak256(O.encode_order(o, True)).hex() == emitted
        out.append(dict(tx=rc["transactionHash"].lower(), logIndex=int(l["logIndex"], 16), contract="DlnSource" if a in SRC else "DlnDestination",
                        topic0=l["topics"][0][:10], orderId=emitted, recomputed_ok=ok or ok_h, external_call_hash_variant=ok_h,
                        makerSrc=addr(o["giveChainId"], o["makerSrc"]), giveChainId=o["giveChainId"], giveAmount=o["giveAmount"],
                        takeChainId=o["takeChainId"], takeAmount=o["takeAmount"], receiverDst=addr(o["takeChainId"], o["receiverDst"]),
                        tx_status=rc.get("status"), block=int(rc["blockNumber"], 16)))
    return out

if __name__ == "__main__":
    R = receipts(); rows = []
    for rc in R.values(): rows += check(rc)
    N.write_csv(N.ROOT / "evidence/s13_orderid_check.csv", sorted(rows, key=lambda r: (r["block"], r["tx"], r["logIndex"])))
    bad = [r for r in rows if not r["recomputed_ok"]]
    print(len(R), "reçus,", len(rows), "événements DLN,", len(bad), "orderId non retrouvés ;", collections.Counter((r["contract"], r["topic0"], r["recomputed_ok"]) for r in rows))
    by = collections.defaultdict(list)
    for r in rows:
        if r["recomputed_ok"]: by[int(r["orderId"], 16)].append(r)
    links = list(csv.DictReader(open(N.ROOT / "CROSSCHAIN_LINKS.csv"))); miss = []
    for k in links:
        ev = by.get(int(k["orderId"], 16), [])
        good = [e for e in ev if e["makerSrc"].lower() == k["maker"].lower() and e["receiverDst"].lower() == k["receiver"].lower()
                and str(e["takeAmount"]) == k["take_amount_raw"]]
        if not good: miss.append((k["orderId"], k["src_chain"], k["dst_chain"], len(ev)))
    print(len(links), "liens ;", len(links) - len(miss), "avec un événement EVM dont l'orderId recalculé, le maker, le receveur et le takeAmount concordent")
    for m in miss: print("  non confirmé", m)
