"""CROSSCHAIN_LINKS.csv : les ordres DLN entre Base et Ethereum, d'Ethereum et de Base vers Ei5yGz8d, et l'aller-retour BSC de b298
(88 liens), reliés des deux côtés par son orderId. Les autres ordres de ces wallets sont dans dln_orders_evm.csv du dossier précédent.
(journal CreatedOrder/FulfilledOrder sur EVM, « Order Id » dans les logs Solana). Aucun rapprochement par montant ou par heure.
Les reçus Ethereum des fills manquants sont relus (RPC public, cache)."""
import csv, sys, os, json
sys.path.insert(0, os.path.dirname(__file__))
import nt_lib as N
import s21_dln_by_tx as X
R = N.ROOT
def rd(p): return list(csv.DictReader(open(p)))

base = rd(R / "evidence/s12_dln_base.csv")
s33 = {int(r["orderId"], 16): r for r in rd(R / "evidence/s33_sol_dln_Ei5yGz8d.csv") if r["orderId"]}
corpus = {int(r["orderId"], 16): r for r in rd(N.OLD_INV / "evidence/dln_orders_evm.csv")}
api = {}
for r in rd(N.DEB_RECEIVERS):
    api.setdefault(int(r["order_id"], 16), r)
for r in rd(N.DEB_ORDERS):
    api.setdefault(int(r["order_id_local"], 16), dict(create_tx=r["source_signature"], fulfil_tx=r["fulfil_tx"], create_utc=r["source_utc"], fulfil_utc=r["fulfil_ts"]))
rows = []

def add(oid, src_chain, src_tx, src_utc, dst_chain, dst_tx, dst_utc, o, ver, level):
    rows.append(dict(orderId="0x%064x" % oid, src_chain=src_chain, src_tx=src_tx, src_utc=src_utc, dst_chain=dst_chain, dst_tx=dst_tx, dst_utc=dst_utc,
                     maker=o.get("makerSrc") or o.get("maker", ""), receiver=o.get("receiverDst") or o.get("receiver", ""),
                     give_token=o.get("giveTokenAddress") or o.get("give_token", ""), give_amount_raw=o.get("giveAmount") or o.get("give_amount_raw", ""),
                     take_token=o.get("takeTokenAddress") or o.get("take_token", ""), take_amount_raw=o.get("takeAmount") or o.get("take_amount_raw", ""),
                     verification=ver, level=level))

seen = set()
for o in base:
    oid = int(o["orderId"], 16)
    if (oid, o["event"]) in seen: continue
    seen.add((oid, o["event"]))
    if o["event"] == "CreatedOrder":
        if o["takeChain"] == "solana":
            s = s33.get(oid)
            ok = s and s["amount_ok"] == "True"
            add(oid, "base", o["tx"], o["ts"], "solana", s["sig"] if s else "", s["ts"] if s else "", o,
                "CreatedOrder Base + Order Id dans les logs Solana, montant exact" if ok else "Solana non retrouvé", "VERIFIED" if ok else "UNRESOLVED")
        else:
            a = api.get(oid, {}); ftx = a.get("fulfil_tx", ""); ok = False; dts = a.get("fulfil_utc", "")
            if ftx:
                evs, rc = X.decode("ethereum", ftx)
                ok = any(int(e["orderId"], 16) == oid and e["event"] == "FulfilledOrder" and str(e["takeAmount"]) == o["takeAmount"] for e in evs)
            add(oid, "base", o["tx"], o["ts"], o["takeChain"], ftx, dts, o,
                "CreatedOrder Base + FulfilledOrder Ethereum, même orderId et même montant" if ok else "fill non relu", "VERIFIED" if ok else "UNRESOLVED")
    else:
        if o["giveChain"] == "ethereum":
            c = corpus.get(oid)
            add(oid, "ethereum", c["tx"] if c else "", c["utc"] if c else "", "base", o["tx"], o["ts"], o,
                "CreatedOrder Ethereum (dossier précédent) + FulfilledOrder Base, même orderId" if c else "création non relue", "VERIFIED" if c else "PARTIAL")
        else:
            a = api.get(oid, {})
            add(oid, "solana", a.get("create_tx", ""), a.get("create_utc", ""), "base", o["tx"], o["ts"], o,
                "FulfilledOrder Base (maker = champ signé de l'ordre) + signature Solana de l'index deBridge du projet deBridge", "VERIFIED" if a.get("create_tx") else "PARTIAL")
# Ethereum -> Solana (Ei5yGz8d) : orderId du corpus Ethereum retrouvé dans les logs Solana
for oid, s in s33.items():
    c = corpus.get(oid)
    if c and s["program"] == "dln_dst":
        add(oid, "ethereum", c["tx"], c["utc"], "solana", s["sig"], s["ts"], c, "CreatedOrder Ethereum (dossier précédent) + Order Id dans les logs Solana", "VERIFIED")
# Aller-retour BSC du 12/11/2024 : les quatre tx relues ici
for tx_src, chain_src, tx_dst, chain_dst in [("0xca82377984453a77f40592a694c5ad4c8076acce66b64a25e7c43f119f3cf8a4", "ethereum", "0x549e4bc55eb2310b903f087d439b16af35c9d4c17624873012443c4eb6730afe", "bsc"),
                                             ("0x76ffdad7e00a284fc1041b7c045319741bac650d4fdf7d1767524ddad2204f6c", "bsc", "0xf9b44d3ac32c0ad76280d57f31277844e6b5384ec399b7509b287668e128b3cf", "ethereum")]:
    cs, rcs = X.decode(chain_src, tx_src); fs, rcd = X.decode(chain_dst, tx_dst)
    c = [e for e in cs if e["event"] == "CreatedOrder"][0]; f = [e for e in fs if e["event"] == "FulfilledOrder"][0]
    assert c["orderId"] == f["orderId"] and str(c["takeAmount"]) == str(f["takeAmount"])
    add(int(c["orderId"], 16), chain_src, tx_src, "", chain_dst, tx_dst, "", c, "CreatedOrder et FulfilledOrder relus ici, même orderId et même montant", "VERIFIED")
N.write_csv(R / "CROSSCHAIN_LINKS.csv", rows)
import collections
print(len(rows), collections.Counter((r["src_chain"], r["dst_chain"], r["level"]) for r in rows))
