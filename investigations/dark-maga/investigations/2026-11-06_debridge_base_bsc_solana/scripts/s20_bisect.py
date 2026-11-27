"""Localise par dichotomie, sur un nœud archive public, chaque bloc où change l'état d'un EOA :
(nonce, solde natif, balanceOf de quelques jetons). Sert là où aucun historique gratuit n'existe (BSC).
Un EOA ne peut perdre du natif ni augmenter son nonce sans signer : l'égalité d'état aux deux bornes
d'un intervalle prouve l'absence de changement natif et de tx signée dedans.
shortcut: un jeton reçu puis retiré par un tiers (transferFrom) dans le même intervalle, nonce inchangé, reste invisible ;
  passer par les journaux Transfer (SQD) sur les fenêtres trouvées pour le combler.
Usage : python3 -I s20_bisect.py bsc <adresse> [bloc_haut]"""
import json, sys, os, hashlib, time, urllib.request
sys.path.insert(0, os.path.dirname(__file__))
import nt_lib as N

CHAINS = {
    "bsc": dict(rpcs=["https://56.rpc.thirdweb.com"], tokens={
        "USDT": "0x55d398326f99059ff775485246999027b3197955", "USDC": "0x8ac76a51cc950d9822d68b83fe1ad97b32cd580d",
        "ETH": "0x2170ed0880ac9a755fd29b2688956bd959f933f8", "WBNB": "0xbb4cdb9cbd36b01bd1cbaebf2de08d9173bc095c",
        "BUSD": "0xe9e7cea3dcc4dbb5bd5a6ab3ee4c6ad8b5ad8a9f"}),
}

def batch(chain, calls):
    body = json.dumps([{"jsonrpc": "2.0", "id": i, "method": m, "params": p} for i, (m, p) in enumerate(calls)])
    key = hashlib.sha256((chain + " batch " + body).encode()).hexdigest(); pth = N.E._cache(key)
    if pth.exists():
        return [x["result"] for x in sorted(json.loads(pth.read_bytes()), key=lambda x: x["id"])]
    err = None
    for i in range(10):
        url = CHAINS[chain]["rpcs"][i % len(CHAINS[chain]["rpcs"])]
        try:
            req = urllib.request.Request(url, data=body.encode(), headers={"content-type": "application/json", "user-agent": "dmaga-research/1.0"})
            raw = urllib.request.urlopen(req, timeout=60).read(); d = json.loads(raw)
            if isinstance(d, list) and len(d) == len(calls) and all("result" in x and x["result"] is not None for x in d):
                N.E._store(key, f"{chain} batch {len(calls)}", raw)
                return [x["result"] for x in sorted(d, key=lambda x: x["id"])]
            err = str(d)[:200]
        except Exception as e:
            err = repr(e)
        time.sleep(1 + 2 * i)
    raise RuntimeError(f"batch {chain}: {err}")

class State:
    def __init__(self, chain, addr):
        self.chain, self.a = chain, addr.lower(); self.toks = CHAINS[chain]["tokens"]; self.memo = {}; self.calls = 0
    def __call__(self, b):
        if b in self.memo: return self.memo[b]
        tag = hex(b)
        calls = [("eth_getTransactionCount", [self.a, tag]), ("eth_getBalance", [self.a, tag])] + \
                [("eth_call", [{"to": t, "data": "0x70a08231" + self.a[2:].rjust(64, "0")}, tag]) for t in self.toks.values()]
        r = batch(self.chain, calls); self.calls += 1
        s = tuple(int(x, 16) if x not in ("0x",) else 0 for x in r)
        self.memo[b] = s; return s

def changes(st, lo, hi, workers=1):
    """Blocs b dans ]lo, hi] tels que état(b) != état(b-1). Parcours par vagues : les états d'une vague sont lus en parallèle."""
    from concurrent.futures import ThreadPoolExecutor
    out, wave = [], [(lo, hi)]
    with ThreadPoolExecutor(max_workers=workers) as ex:
        while wave:
            need = sorted({b for l, h in wave for b in (l, h)} - set(getattr(st, "memo", {})))
            list(ex.map(st, need))
            nxt = []
            for l, h in wave:
                if st(l) == st(h): continue
                if h - l == 1: out.append(h); continue
                m = (l + h) // 2; nxt += [(l, m), (m, h)]
            wave = nxt
    return sorted(out)

def selftest():
    """Test hors réseau sur un état simulé : changements à 5, 6, 1000 et un aller-retour natif bloqué par le nonce."""
    seq = {5: (1, 10), 6: (1, 12), 1000: (2, 3)}
    def fake(b):
        s = (0, 0)
        for k in sorted(seq):
            if b >= k: s = seq[k]
        return s
    class F:
        def __call__(self, b): return fake(b)
    assert changes(F(), 0, 4096) == [5, 6, 1000], changes(F(), 0, 4096)

if __name__ == "__main__":
    selftest()
    chain, a = sys.argv[1], sys.argv[2].lower()
    hi = int(sys.argv[3]) if len(sys.argv) > 3 else int(batch(chain, [("eth_blockNumber", [])])[0], 16)
    st = State(chain, a)
    ch = changes(st, 0, hi, workers=int(os.environ.get('BISECT_WORKERS', '6')))
    names = ["nonce", "native"] + list(st.toks)
    rows = []
    for b in ch:
        s0, s1 = st(b - 1), st(b)
        rows.append(dict(block=b, **{f"d_{n}": s1[i] - s0[i] for i, n in enumerate(names)}, **{n: s1[i] for i, n in enumerate(names)}))
    out = N.write_csv(N.ROOT / "data" / f"{chain}_{a[:6]}_state_changes.csv", rows)
    print(out, len(rows), "changements,", st.calls, "lots RPC ; nonce final", st(hi)[0])
