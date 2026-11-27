"""Parseur indépendant de l'audit I. Lit les transactions brutes (C/net, G/net), en flux. Rien n'est repris de work_G."""
import gzip, json, os
R = "/Volumes/VERBATIM HD/Dark-MAGA-Investigation"
NETS = [R + "/audits_work/C/net", R + "/audits_work/G/net"]
USDC = "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"
USDT = "Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB"
WSOL = "So11111111111111111111111111111111111111112"
DMAGA = "7D7BRcBYepfi77vxySapmeqRNN1wsBBxnFPJGbH5pump"

def net_paths(w):
    out = []
    for d in NETS:
        for suf in (".jsonl.gz", ".desc.jsonl.gz"):
            p = f"{d}/{w}{suf}"
            if os.path.exists(p):
                out.append(p)
    return out

def iter_tx(w):
    """Toutes les tx brutes d'un wallet, dédoublonnées par signature. Le set de signatures reste petit (un wallet)."""
    seen = set()
    for p in net_paths(w):
        with gzip.open(p, "rt") as h:
            for l in h:
                t = json.loads(l)
                s = t["transaction"]["signatures"][0]
                if s in seen:
                    continue
                seen.add(s)
                yield t

def keys(t):
    return [a["pubkey"] if isinstance(a, dict) else a for a in t["transaction"]["message"]["accountKeys"]]

def signers(t):
    return [a["pubkey"] for a in t["transaction"]["message"]["accountKeys"] if isinstance(a, dict) and a.get("signer")]

def sol_delta(t):
    k = keys(t)
    pre, post = t["meta"]["preBalances"], t["meta"]["postBalances"]
    return {k[i]: post[i] - pre[i] for i in range(len(k)) if post[i] != pre[i]}

def tok_delta(t):
    """{(owner, mint): delta en unités entières}, {mint: decimales}. Un compte fermé ou ouvert compte pour son solde."""
    m = t["meta"]
    d, dec = {}, {}
    for side, sign in (("preTokenBalances", -1), ("postTokenBalances", 1)):
        for b in m.get(side) or []:
            o = b.get("owner")
            mint = b["mint"]
            a = int(b["uiTokenAmount"]["amount"])
            dec[mint] = b["uiTokenAmount"]["decimals"]
            d[(o, mint)] = d.get((o, mint), 0) + sign * a
    return {k: v for k, v in d.items() if v}, dec

def programs(t):
    ps = set()
    msg = t["transaction"]["message"]
    for i in msg["instructions"]:
        ps.add(i.get("programId"))
    for g in t["meta"].get("innerInstructions") or []:
        for i in g["instructions"]:
            ps.add(i.get("programId"))
    return ps

BASIC = {"11111111111111111111111111111111", "TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA",
         "TokenzQdBNbLqP5VEhdkAS6EPFLC1PHnBqCXEpPxuEb",
         "ATokenGPvbdGVxr1b2hvZbsiqW5xWH25efTNsLJA8knL", "ComputeBudget111111111111111111111111111111",
         "MemoSq4gqABAXKb96qnH8TysNcWxMyWCqXgDLGmfcHr", "Memo1UhkJRfHyvLMcVucJwxXeuD728EqVDDwQDxFMNo"}

def ok(t):
    return t["meta"]["err"] is None

def snow(i):
    """Heure d'un id X, ms UTC."""
    return (int(i) >> 22) + 1288834974657
