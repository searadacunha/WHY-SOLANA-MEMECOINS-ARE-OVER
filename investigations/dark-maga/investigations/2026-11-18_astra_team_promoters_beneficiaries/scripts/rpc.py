"""Minimal public Solana RPC client with retry and on-disk cache (raw responses preserved)."""
import json, time, urllib.request, os, hashlib
RPC = os.environ.get('SOLANA_RPC', 'https://api.mainnet-beta.solana.com')
CACHE = os.path.join(os.path.dirname(__file__), '..', 'raw', 'rpc_cache')
os.makedirs(CACHE, exist_ok=True)
CALLS = {'n': 0}
def rpc(method, params, cache=True):
    key = hashlib.sha256(json.dumps([method, params], sort_keys=True).encode()).hexdigest()[:32]
    fp = os.path.join(CACHE, f'{method}_{key}.json')
    if cache and os.path.exists(fp):
        return json.load(open(fp))['result']
    body = json.dumps({"jsonrpc": "2.0", "id": 1, "method": method, "params": params}).encode()
    for k in range(8):
        try:
            CALLS['n'] += 1
            r = urllib.request.urlopen(urllib.request.Request(RPC, data=body, headers={'Content-Type': 'application/json'}), timeout=90)
            d = json.loads(r.read())
            if 'error' in d:
                if d['error'].get('code') in (-32009, -32007, -32004):  # skipped / not available
                    json.dump({'result': None, 'error': d['error'], 'method': method, 'params': params}, open(fp, 'w'))
                    return None
                time.sleep(2 + 2 * k); continue
            json.dump({'result': d['result'], 'method': method, 'params': params, 'fetched_utc': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}, open(fp, 'w'))
            return d['result']
        except Exception as e:
            time.sleep(3 + 3 * k)
    raise RuntimeError(f'RPC failed {method} {params}')
def sigs(addr, before=None, until=None, max_pages=50, limit=1000):
    out = []
    for _ in range(max_pages):
        p = {'limit': limit}
        if before: p['before'] = before
        if until: p['until'] = until
        r = rpc('getSignaturesForAddress', [addr, p])
        if not r: break
        out += r; before = r[-1]['signature']
        if len(r) < limit: return out, True
    return out, False
def tx(sig):
    return rpc('getTransaction', [sig, {"encoding": "jsonParsed", "maxSupportedTransactionVersion": 0}])
