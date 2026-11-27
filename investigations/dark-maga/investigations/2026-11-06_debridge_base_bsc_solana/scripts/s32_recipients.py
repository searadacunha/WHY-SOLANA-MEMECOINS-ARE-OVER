"""Destinataires réels d'un wallet Solana (SOL hors comptes temporaires, jetons vers des wallets), filtrés aux comptes
détenus par le System Program (wallets), puis profil des 100 premières tx de chacun : premier financeur, vierge ou non,
premiers jetons achetés, créations de jetons (pump.fun create / initializeMint), sorties de SOL.
Sortie : data/sol_<w8>_recipients.csv. Usage : py312 -I s32_recipients.py <wallet> [ts_min] [ts_max]"""
import sys, os, csv, json, collections
sys.path.insert(0, os.path.dirname(__file__))
import nt_lib as N, sol_lib as S
import s31_sol_ledger as L
SYS = "11111111111111111111111111111111"
NOISE = {"25mYnjJ2MXHZH6NvTTdA63JvjgRVcuiaj6MRiEQNs1Dq"}  # frais du bot de trading (117 micro-versements), pas un financement

def owners(addrs):
    out = {}
    for i in range(0, len(addrs), 100):
        chunk = addrs[i:i + 100]
        r = S.call("getMultipleAccounts", [chunk, {"encoding": "base64", "dataSlice": {"offset": 0, "length": 0}}])
        for a, v in zip(chunk, r["value"]): out[a] = v["owner"] if v else None
    return out

def first_page(a):
    opts = {"transactionDetails": "full", "sortOrder": "asc", "limit": 100, "encoding": "jsonParsed", "maxSupportedTransactionVersion": 1,
            "filters": {"tokenAccounts": "balanceChanged"}}
    return S.call("getTransactionsForAddress", [a, opts]).get("data") or []

def profile(a, w):
    txs = first_page(a); funder = None; fresh = None; bought = []; created = []; sol_out = collections.Counter(); first_ts = None
    for t in sorted(txs, key=lambda t: (t["slot"], t.get("transactionIndex") or 0)):
        r, xs = L.parse(t, a)
        first_ts = first_ts or r["ts"]
        if funder is None:
            ins = [x for x in xs if x["asset"] == "SOL" and x["to"] == a and int(x["raw"]) > 0]
            if ins:
                funder = ins[0]["frm"]; fresh = (r["ts"] == first_ts)
        tok = json.loads(r["tok"])
        for m, v in tok.items():
            if v > 0 and m not in ("So11111111111111111111111111111111111111112", "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v") and len(bought) < 6 and r["signer"] == a:
                bought.append(f"{m}@{r['ts']}")
        for ix in L.all_ix(t):
            p = ix.get("parsed"); pid = ix.get("programId", "")
            if pid == "6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P" and r["signer"] == a and "create" in json.dumps(ix.get("data", ""))[:0]:
                pass
            if isinstance(p, dict) and p.get("type") in ("initializeMint", "initializeMint2") and r["signer"] == a:
                created.append(f"{p['info'].get('mint')}@{r['ts']}")
        for x in xs:
            if x["asset"] == "SOL" and x["frm"] == a and not x.get("tag"): sol_out[x["to"]] += int(x["raw"])
    return dict(first_ts=first_ts, n_first_page=len(txs), first_funder=funder, funder_is_w=(funder == w), fresh_at_funding=fresh,
                first_buys=" ".join(bought), created_mints=" ".join(created),
                top_sol_out=" ".join(f"{k}:{v / 1e9:.3f}" for k, v in sol_out.most_common(3)))

if __name__ == "__main__":
    w = sys.argv[1]; t0 = sys.argv[2] if len(sys.argv) > 2 else "0"; t1 = sys.argv[3] if len(sys.argv) > 3 else "9"
    X = [x for x in csv.DictReader(open(N.ROOT / "data" / f"sol_{w[:8]}_transfers.csv")) if t0 <= x["ts"] <= t1]
    agg = collections.defaultdict(lambda: dict(sol=0, n=0, tokens=collections.Counter(), first="", last="", sigs=[]))
    for x in X:
        if x["frm"] != w or x["to"] in (w, "?", "", None) or x["to"] in NOISE: continue
        if x["asset"] == "SOL" and x["tag"]: continue
        if x["asset"] == "SOL_create": continue
        g = agg[x["to"]]
        if x["asset"] == "SOL": g["sol"] += int(x["raw"])
        else: g["tokens"][x["mint"]] += int(x["raw"])
        g["n"] += 1; g["first"] = g["first"] or x["ts"]; g["last"] = x["ts"]; g["sigs"].append(x["sig"])
    own = owners(list(agg))
    rows = []
    for a, g in sorted(agg.items(), key=lambda kv: -kv[1]["sol"]):
        if own.get(a) not in (SYS, None): continue  # None = compte fermé ou wallet vidé (0 lamport) : à profiler, pas à écarter
        rows.append(dict(recipient=a, account_now=own.get(a) and "system" or "absent", sol_from_w=g["sol"] / 1e9, n=g["n"], first=g["first"], last=g["last"],
                         tokens=" ".join(f"{m}:{v}" for m, v in g["tokens"].items()), first_sig=g["sigs"][0], **profile(a, w)))
    out = N.write_csv(N.ROOT / "data" / f"sol_{w[:8]}_recipients.csv", rows)
    print(out, len(rows), "wallets destinataires (System), sur", len(agg), "destinataires")
