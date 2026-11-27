"""Décode les événements DLN (CreatedOrder / FulfilledOrder) de reçus désignés par hash, sur une chaîne donnée.
Sert à relier un ordre entre deux chaînes par son orderId (jamais par montant). Usage : python3 -I s21_dln_by_tx.py <chaine> <tx> [tx...]"""
import sys, os, json
sys.path.insert(0, os.path.dirname(__file__))
import s12_dln_evm as Q, dln as D

def decode(chain, tx):
    rc = Q.RPCS[chain](tx)
    out = [dict(x, event="FulfilledOrder") for x in Q.fills(rc)] + Q.created(rc, Q.CHAIN_ID[chain])
    return [{k: (v.hex() if isinstance(v, bytes) else v) for k, v in o.items()} for o in out], rc

if __name__ == "__main__":
    chain = sys.argv[1]
    for tx in sys.argv[2:]:
        evs, rc = decode(chain, tx)
        print(chain, tx, "status", rc["status"], "block", int(rc["blockNumber"], 16), "from", rc["from"])
        for e in evs:
            print("  ", e["event"], "orderId", e["orderId"], "maker", e["makerSrc"], e["giveChain"], e["giveTokenAddress"], e["giveAmount"], "->", e["takeChain"], e["takeTokenAddress"], e["takeAmount"], "recv", e["receiverDst"])
