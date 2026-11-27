"""Historique Solana complet d'un wallet via Helius getTransactionsForAddress (clés du pool de recherche, jamais affichées),
transactions complètes jsonParsed, version 1 acceptée, comptes de jetons inclus (tokenAccounts=balanceChanged).
Pages en cache (raw/cache) ; la pagination s'arrête sur une page sans paginationToken.
Sortie : raw/sol_hist/<wallet>.jsonl.gz (une tx par ligne). Usage : py312 -I s30_sol_hist.py <wallet> [ts_debut] [ts_fin]"""
import sys, os, json, gzip
sys.path.insert(0, os.path.dirname(__file__))
import nt_lib as N
import sol_lib as S

def history(addr, t0=None, t1=None):
    out, token, pages = [], None, 0
    filt = {"tokenAccounts": "balanceChanged"}
    bt = {}
    if t0: bt["gte"] = int(t0)
    if t1: bt["lt"] = int(t1)
    if bt: filt["blockTime"] = bt
    while True:
        opts = {"transactionDetails": "full", "sortOrder": "asc", "limit": 100, "encoding": "jsonParsed",
                "maxSupportedTransactionVersion": 1, "filters": filt}
        if token: opts["paginationToken"] = token
        res = S.call("getTransactionsForAddress", [addr, opts])
        data = res.get("data") or []
        out += data; pages += 1
        token = res.get("paginationToken")
        if not token:
            return out, pages
        if not data:
            raise RuntimeError("page vide avec jeton de pagination : arrêt pour ne pas boucler")

if __name__ == "__main__":
    a = sys.argv[1]; t0 = sys.argv[2] if len(sys.argv) > 2 else None; t1 = sys.argv[3] if len(sys.argv) > 3 else None
    txs, pages = history(a, t0, t1)
    d = N.RAW / "sol_hist"; d.mkdir(parents=True, exist_ok=True)
    p = d / f"{a}{'_' + t0 if t0 else ''}{'_' + t1 if t1 else ''}.jsonl.gz"
    with gzip.open(p, "wt") as f:
        for t in txs: f.write(json.dumps(t) + "\n")
    sigs = [t["transaction"]["signatures"][0] for t in txs]
    assert len(sigs) == len(set(sigs)), "doublons de signatures"
    print(p, len(txs), "tx,", pages, "pages,", txs[0]["blockTime"] if txs else None, txs[-1]["blockTime"] if txs else None)
