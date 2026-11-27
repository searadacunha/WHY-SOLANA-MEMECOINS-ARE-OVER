"""Grand livre Solana d'un wallet depuis raw/sol_hist : par tx, variation nette de SOL et de chaque mint (propriétaire = wallet),
programmes touchés, transferts directs de SOL et de jetons (instructions parsées, internes comprises) avec la contrepartie.
Sorties : data/sol_<w8>_txs.csv (une ligne par tx), data/sol_<w8>_transfers.csv (une ligne par transfert direct)."""
import sys, os, json, gzip, datetime as dt
sys.path.insert(0, os.path.dirname(__file__))
import nt_lib as N
PROG = {"src5qyZHqTqecJV4aY6Cb6zDZLMDzrDKKezs22MPHr4": "dln_src", "dst5MGcFPoBeREFAA5E3tU5ij8m5uVYwkzkSAbsLbNo": "dln_dst",
        "JUP6LkbZbjS1jKKwapdHNy74zcZ3tLUZoi5QNyVTaV4": "jupiter", "6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P": "pumpfun",
        "pAMMBay6oceH9fJKBRHGP5D4bD4sWpmSwMn52FMfXEA": "pumpswap", "675kPX9MHTjS2zt1qfr1NYHuzeLXfQM9H24wFSUt1Mp8": "raydium_v4",
        "CAMMCzo5YL8w4VFF8KVHrK22GGUsp5VTaW7grrKgrWqK": "raydium_clmm", "LBUZKhRxPF3XUpBCjp4YzTKgLccjZhTSDM9YuVaPwxo": "meteora_dlmm",
        "whirLbMiicVdio4qvUfM5KAg6Ct8VwpYzGff3uctyCc": "orca", "DCA265Vj8a9CEuX1eb1LWRnDT7uK6q1xMipnNyatn23M": "jup_dca",
        "j1o2qRpjcyUwEvwtcfhEQefh773ZgjxcVRry7LDqg5X": "jup_limit", "MoonCVVNZFSYkqNXP6bxHLPL6QQJiMagDL3qcqUQTrG": "moonshot",
        "BSfD6SHZigAfDWSjzD5Q41jw8LmKwtmjskPH9XW1mrRW": "photon", "TSWAPaqyCSx2KABk68Shruf4rp7CxcNi8hAsbdwmHbN": "tensor"}

def keys_of(t):
    ks = [k["pubkey"] if isinstance(k, dict) else k for k in t["transaction"]["message"]["accountKeys"]]
    la = t["meta"].get("loadedAddresses") or {}
    return ks + la.get("writable", []) + la.get("readonly", [])

def all_ix(t):
    for ix in t["transaction"]["message"]["instructions"]: yield ix
    for inner in t["meta"].get("innerInstructions") or []:
        for ix in inner["instructions"]: yield ix

def parse(t, w):
    ks = keys_of(t); m = t["meta"]; sig = t["transaction"]["signatures"][0]
    ts = dt.datetime.fromtimestamp(t["blockTime"], dt.timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
    sol = (m["postBalances"][ks.index(w)] - m["preBalances"][ks.index(w)]) if w in ks else 0
    owner_of = {}; mint_of = {}
    for side in ("preTokenBalances", "postTokenBalances"):
        for b in m.get(side) or []:
            owner_of[ks[b["accountIndex"]]] = b.get("owner"); mint_of[ks[b["accountIndex"]]] = b["mint"]
    tok = {}
    for side, sg in (("preTokenBalances", -1), ("postTokenBalances", 1)):
        for b in m.get(side) or []:
            if b.get("owner") == w: tok[b["mint"]] = tok.get(b["mint"], 0) + sg * int(b["uiTokenAmount"]["amount"])
    tok = {k: v for k, v in tok.items() if v}
    progs = set(); xfers = []
    closed_to_w = set()  # comptes de jetons fermés au profit du wallet dans la même tx (WSOL temporaire)
    for ix in all_ix(t):
        p = ix.get("parsed")
        if isinstance(p, dict) and p.get("type") == "closeAccount" and (p.get("info") or {}).get("destination") == w:
            closed_to_w.add(p["info"].get("account"))
    def own(acct):
        return "own_token_acct" if owner_of.get(acct) == w else ("temp_closed" if acct in closed_to_w else "")
    for ix in all_ix(t):
        pid = ix.get("programId") or ks[ix["programIdIndex"]]; progs.add(PROG.get(pid, pid[:8]))
        p = ix.get("parsed")
        if not isinstance(p, dict): continue
        info = p.get("info") or {}; typ = p.get("type")
        if pid == "11111111111111111111111111111111" and typ in ("transfer", "transferWithSeed") and w in (info.get("source"), info.get("destination")):
            xfers.append(dict(sig=sig, ts=ts, asset="SOL", mint="", frm=info.get("source"), to=info.get("destination"), raw=int(info.get("lamports", 0)), decimals=9,
                              tag=own(info.get("destination")) or own(info.get("source"))))
        if typ == "createAccount" and info.get("source") == w:
            xfers.append(dict(sig=sig, ts=ts, asset="SOL_create", mint="", frm=w, to=info.get("newAccount"), raw=int(info.get("lamports", 0)), decimals=9, tag=own(info.get("newAccount")) or "created"))
        if pid in ("TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA", "TokenzQdBNbLqP5VEhdkAS6EPFLC1PHnBqCXEpPxuEb") and typ in ("transfer", "transferChecked"):
            src, dst = info.get("source"), info.get("destination"); auth = info.get("authority") or info.get("multisigAuthority")
            so, do = owner_of.get(src, auth), owner_of.get(dst, "?")
            if w in (so, do, auth):
                amt = info.get("amount") or (info.get("tokenAmount") or {}).get("amount")
                mint = info.get("mint") or mint_of.get(src) or mint_of.get(dst) or ""
                dec = (info.get("tokenAmount") or {}).get("decimals")
                xfers.append(dict(sig=sig, ts=ts, asset="TOKEN", mint=mint, frm=so, to=do, raw=int(amt or 0), decimals=dec if dec is not None else "", auth=auth, tag=""))
    signer = ks[0]
    return dict(sig=sig, ts=ts, slot=t["slot"], idx=t.get("transactionIndex"), err=bool(m.get("err")), signer=signer, fee=m["fee"],
                sol=sol, tok=json.dumps(tok), progs="|".join(sorted(progs))), xfers

def load(w):
    p = N.raw_dir("sol_hist") / f"{w}.jsonl.gz"
    return [json.loads(l) for l in gzip.open(p, "rt")]

if __name__ == "__main__":
    w = sys.argv[1]; txs = load(w); rows = []; xs = []
    for t in txs:
        r, x = parse(t, w); rows.append(r); xs += x
    rows.sort(key=lambda r: (r["slot"], r["idx"] or 0))
    N.write_csv(N.ROOT / "data" / f"sol_{w[:8]}_txs.csv", rows)
    N.write_csv(N.ROOT / "data" / f"sol_{w[:8]}_transfers.csv", xs, ["sig", "ts", "asset", "mint", "frm", "to", "raw", "decimals", "auth", "tag"])
    # contrôle : la somme des variations de SOL égale le solde final lu dans la dernière tx
    last = txs[-1] if txs else None
    tot = sum(r["sol"] for r in rows)
    ks = keys_of(max(txs, key=lambda t: (t["slot"], t.get("transactionIndex") or 0)))
    lt = max(txs, key=lambda t: (t["slot"], t.get("transactionIndex") or 0))
    first = min(txs, key=lambda t: (t["slot"], t.get("transactionIndex") or 0)); kf = keys_of(first)
    start = first["meta"]["preBalances"][kf.index(w)] if w in kf else 0
    end = lt["meta"]["postBalances"][ks.index(w)] if w in ks else None
    print(len(rows), "tx,", len(xs), "transferts ; solde initial", start / 1e9, "+ somme", tot / 1e9, "=", (start + tot) / 1e9, "contre solde final", (end or 0) / 1e9)
    assert end is None or start + tot == end, "grand livre SOL incomplet"
