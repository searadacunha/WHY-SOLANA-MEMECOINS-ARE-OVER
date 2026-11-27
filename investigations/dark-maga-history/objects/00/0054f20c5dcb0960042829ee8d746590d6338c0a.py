"""Rapproche chaque tx Solana du programme DLN (destination ou source) d'un wallet à un ordre EVM par l'orderId lu dans les
logs Solana (« Order Id: », hex en 2024, décimal ensuite : comparaison en entiers). Aucun rapprochement par montant.
Sortie : evidence/s33_sol_dln_<w8>.csv"""
import sys, os, re, csv, gzip, json
sys.path.insert(0, os.path.dirname(__file__))
import nt_lib as N
import s31_sol_ledger as L
OID = re.compile(r"Order Id:\s*(0x[0-9a-fA-F]+|[0-9]+)")

def evm_orders():
    out = {}
    for r in csv.DictReader(open(N.OLD_INV / "evidence" / "dln_orders_evm.csv")):
        out[int(r["orderId"], 16)] = dict(src="ethereum_corpus", **r)
    for f in (N.ROOT / "evidence").glob("s12_dln_*.csv"):
        for r in csv.DictReader(open(f)):
            out.setdefault(int(r["orderId"], 16), dict(src=f.name, **r))
    return out

if __name__ == "__main__":
    w = sys.argv[1]; E = evm_orders(); rows = []
    for t in L.load(w):
        logs = t["meta"].get("logMessages") or []
        progs = {L.PROG.get(ix.get("programId") or "", "") for ix in L.all_ix(t)}
        if not ({"dln_dst", "dln_src"} & progs): continue
        r, _ = L.parse(t, w)
        ids = {int(m.group(1), 0) for l in logs for m in [OID.search(l)] if m}
        for oid in ids or {None}:
            e = E.get(oid) if oid is not None else None
            rows.append(dict(sig=r["sig"], ts=r["ts"], program="dln_dst" if "dln_dst" in progs else "dln_src", sol_delta=r["sol"], tok=r["tok"],
                             orderId=("0x%064x" % oid) if oid is not None else "", matched=bool(e), evm_tx=(e or {}).get("tx", ""), evm_chain=(e or {}).get("giveChain", ""),
                             maker=(e or {}).get("makerSrc", ""), receiver=(e or {}).get("receiverDst", ""), takeAmount=(e or {}).get("takeAmount", ""),
                             amount_ok=(e is not None and r["program" if False else "sol"] == int((e or {}).get("takeAmount") or -1)) if e and (e.get("takeTokenAddress") in ("11111111111111111111111111111111",)) else ""))
    out = N.write_csv(N.ROOT / "evidence" / f"s33_sol_dln_{w[:8]}.csv", rows)
    import collections
    print(out, len(rows), collections.Counter((r["program"], r["matched"], r["evm_chain"]) for r in rows))
