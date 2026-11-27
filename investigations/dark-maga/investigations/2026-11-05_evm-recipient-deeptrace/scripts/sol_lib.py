"""Solana via Helius, clés du pool de recherche seulement (dmaga.config.helius_keys, lu en lecture seule).
Réponses gardées dans RAW sous une clé qui ne contient jamais la clé d'API."""
import hashlib, json, sys, time, urllib.request, itertools
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))  # racine du dépôt
from dmaga.config import helius_keys, scrub  # lecture seule
import ev_lib as E

_KEYS = itertools.cycle(helius_keys())
DLN_SRC = "src5qyZHqTqecJV4aY6Cb6zDZLMDzrDKKezs22MPHr4"
DMAGA = "7D7BRcBYepfi77vxySapmeqRNN1wsBBxnFPJGbH5pump"
USDC = "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"
WSOL = "So11111111111111111111111111111111111111112"

def call(method, params, cache=True):
    body = json.dumps({"jsonrpc": "2.0", "id": 1, "method": method, "params": params})
    key = hashlib.sha256(("helius " + body).encode()).hexdigest()
    p = E._cache(key)
    if cache and p.exists():
        return json.loads(p.read_bytes())["result"]
    err = None
    for i in range(8):
        try:
            time.sleep(0.15)
            url = "https://mainnet.helius-rpc.com/?api-key=" + next(_KEYS)
            req = urllib.request.Request(url, data=body.encode(), headers={"content-type": "application/json"})
            with urllib.request.urlopen(req, timeout=90) as r:
                raw = r.read()
            d = json.loads(raw)
            if "error" in d:
                err = str(d["error"]); time.sleep(1 + 2 * i); continue
            if cache:
                E._store(key, "helius " + method + " " + json.dumps(params)[:200], raw)
            return d["result"]
        except Exception as e:
            err = scrub(repr(e)); time.sleep(2 + 3 * i)
    raise RuntimeError(f"helius {method}: {scrub(str(err))}")

def signatures(address):
    """Toutes les signatures (pagination 'before' jusqu'à une page vide). Les pages sont en cache par curseur."""
    out, before = [], None
    while True:
        cfg = {"limit": 1000, **({"before": before} if before else {})}
        page = call("getSignaturesForAddress", [address, cfg])
        if not page:
            return out
        out += page
        before = page[-1]["signature"]
        if len(page) < 1000:
            return out

def tx(sig):
    return call("getTransaction", [sig, {"encoding": "jsonParsed", "maxSupportedTransactionVersion": 0, "commitment": "confirmed"}])

def keys_of(t):
    return [k["pubkey"] if isinstance(k, dict) else k for k in t["transaction"]["message"]["accountKeys"]] + \
        (t["meta"].get("loadedAddresses", {}).get("writable", []) + t["meta"].get("loadedAddresses", {}).get("readonly", []) if t["meta"].get("loadedAddresses") else [])

def deltas(t, owner):
    """Variations nettes pour `owner` : SOL natif (lamports) et jetons par mint (unités brutes)."""
    ks = keys_of(t); m = t["meta"]; sol = 0
    if owner in ks:
        i = ks.index(owner); sol = m["postBalances"][i] - m["preBalances"][i]
    tok = {}
    for side, sgn in (("preTokenBalances", -1), ("postTokenBalances", 1)):
        for b in m.get(side) or []:
            if b.get("owner") == owner:
                tok[b["mint"]] = tok.get(b["mint"], 0) + sgn * int(b["uiTokenAmount"]["amount"])
    return sol, {k: v for k, v in tok.items() if v}

def programs(t):
    ks = keys_of(t); ps = set()
    for ix in t["transaction"]["message"]["instructions"]:
        ps.add(ix.get("programId") or ks[ix["programIdIndex"]])
    for inner in t["meta"].get("innerInstructions") or []:
        for ix in inner["instructions"]:
            ps.add(ix.get("programId") or ks[ix["programIdIndex"]])
    return ps
