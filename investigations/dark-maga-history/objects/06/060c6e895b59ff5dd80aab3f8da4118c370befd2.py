"""Décode, sur une chaîne EVM, les ordres DLN reçus (FulfilledOrder de DlnDestination) et émis (CreatedOrder de DlnSource)
dans les tx d'un grand livre. Reçus lus sur RPC public (cache). Réutilise le décodeur dln.py du dossier précédent.
Usage : python3 -I s12_dln_evm.py base data/base_0xb298_ledger.csv [autres grands livres]"""
import csv, json, sys, os
sys.path.insert(0, os.path.dirname(__file__))
import nt_lib as N
import dln as D
import s11_base_balances as S
from s20_bisect import batch

RPCS = {"base": lambda tx: S.rpc("eth_getTransactionReceipt", [tx]),
        "bsc": lambda tx: batch("bsc", [("eth_getTransactionReceipt", [tx])])[0],
        "ethereum": lambda tx: N.E.rpc("eth_getTransactionReceipt", [tx])}
CHAIN_ID = {"base": 8453, "bsc": 56, "ethereum": 1}
REAL_TOKENS = {"base": {"0x833589fcd6edb6e08f4c7c32d4f71b54bda02913", "0x4200000000000000000000000000000000000006"}}  # USDC, WETH
# dln.py (dossier précédent) lit les deux versions de FulfilledOrder depuis le 06/11 : v1 (0xd281ee92) et v2 (0xc164aca3, 2026), dont la
# tête a un mot de plus avant sender. Même Order dans les deux (orderId recalculé à l'identique par s13_orderid_check.py).
def fills(rcpt):
    return D.fills_in_receipt(rcpt)

def created(rcpt, chain_id):
    out = []
    for l in rcpt["logs"]:
        if l["address"].lower() != N.DLN_SRC or len(l["data"]) < 2 + 64 * 20: continue
        try: o = D.decode_fulfilled(l["data"])
        except Exception: continue
        if o["giveChainId"] != chain_id: continue
        o.pop("sender"); o.pop("unlockAuthority")
        out.append(dict(o, tx=rcpt["transactionHash"], logIndex=int(l["logIndex"], 16), event="CreatedOrder"))
    return out

def run(chain, ledgers):
    txs = {}
    for lg in ledgers:
        L = list(csv.DictReader(open(lg)))
        own = {r["frm"] for r in L if r["kind"] == "tx" and r["dir"] == "out"} or {""}
        signed = {r["tx"] for r in L if r["kind"] == "tx" and r["frm"] in own}
        for r in L:
            dln_in = (r["kind"] == "internal" and r["frm"] == N.DLN_DST) or (r["kind"] == "token" and r["frm"] in ("0x663dc15d3c1ac63ff12e45ab68fea3f0a883c251", "0x555ce236c0220695b68341bc48c68d52210cc35b"))
            # une exécution peut venir de n'importe quel solver : toute entrée d'actif réel dans une tx que le wallet n'a pas signée
            # est décodée (audit EVM du 06/11 : l'ordre 0x1596c70d, exécuté par 0xef1ec136, manquait)
            dln_in = dln_in or (r["dir"] == "in" and r["tx"] not in signed and r["raw"] not in ("", "0")
                                and (r["kind"] == "internal" or (r["kind"] == "token" and r["token"] in REAL_TOKENS.get(chain, ()))))
            dln_out = r["kind"] == "tx" and r["to"] in (N.DLN_SRC, "0x663dc15d3c1ac63ff12e45ab68fea3f0a883c251") and r["status"] == "ok"
            if dln_in or dln_out: txs[r["tx"]] = (r["ts"], r["block"])
    rows = []
    for tx, (ts, blk) in sorted(txs.items(), key=lambda kv: kv[1]):
        rc = RPCS[chain](tx)
        for o in [dict(x, event="FulfilledOrder") for x in fills(rc)] + created(rc, CHAIN_ID[chain]):
            o = {k: (v.hex() if isinstance(v, bytes) else v) for k, v in o.items()}
            rows.append(dict(chain=chain, ts=ts, block=blk, **o))
    return rows

if __name__ == "__main__":
    chain = sys.argv[1]; rows = run(chain, sys.argv[2:])
    keep = ["chain", "ts", "block", "event", "tx", "logIndex", "orderId", "makerSrc", "giveChain", "giveTokenAddress", "giveAmount", "takeChain",
            "takeTokenAddress", "takeAmount", "receiverDst", "orderAuthorityAddressDst", "makerOrderNonce", "sender", "externalCall"]
    out = N.write_csv(N.ROOT / "evidence" / f"s12_dln_{chain}.csv", rows, keep)
    import collections
    print(out, len(rows), collections.Counter((r["event"], r["giveChain"], r["takeChain"]) for r in rows))
