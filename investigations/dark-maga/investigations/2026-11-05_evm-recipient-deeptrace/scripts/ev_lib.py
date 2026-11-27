"""Accès sans clé à l'historique Ethereum : Routescan (API compatible Etherscan, chaîne 1) et RPC public.
Chaque réponse brute est gardée dans RAW (clé = sha256 de l'URL), relue ensuite sans réseau.
Aucune clé n'est utilisée. Une réponse 'status 0' autre que 'No transactions found' n'est jamais mise en cache."""
import hashlib, json, os, time, urllib.request, urllib.parse
from pathlib import Path

RAW = Path(os.environ.get("EV_RAW", Path(__file__).resolve().parent.parent / "raw"))  # raw/ est ignoré par git
RS = "https://api.routescan.io/v2/network/mainnet/evm/1/etherscan/api"
RPC = os.environ.get("EV_RPC", "https://ethereum-rpc.publicnode.com")
UA = {"user-agent": "dmaga-research/1.0", "accept": "application/json"}
LEDGER = RAW / "ledger.jsonl"

def _cache(key):
    return RAW / key[:2] / (key + ".json")

def _http(url, data=None, timeout=60):
    req = urllib.request.Request(url, data=data, headers={**UA, **({"content-type": "application/json"} if data else {})})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()

def _store(key, url, body):
    p = _cache(key); p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes(body)
    with open(LEDGER, "a") as f:
        f.write(json.dumps({"t": int(time.time()), "key": key, "url": url, "sha256": hashlib.sha256(body).hexdigest(), "n": len(body)}) + "\n")

def rs(**params):
    """Routescan, réponse 'result' (liste ou valeur). Lève une erreur si la réponse n'est ni OK ni vide."""
    url = RS + "?" + urllib.parse.urlencode(params)
    key = hashlib.sha256(url.encode()).hexdigest()
    p = _cache(key)
    if p.exists():
        return json.loads(p.read_bytes())["result"]
    err = None
    for i in range(8):
        try:
            time.sleep(0.45)
            body = _http(url)
            d = json.loads(body)
            ok = d.get("status") == "1" or (d.get("status") == "0" and "no transactions found" in str(d.get("message", "")).lower()) \
                or (d.get("status") == "0" and d.get("result") == [])
            if ok:
                _store(key, url, body)
                return d["result"]
            err = f"{d.get('message')} {str(d.get('result'))[:150]}"
        except Exception as e:  # réseau, 429, 5xx : on réessaie
            err = repr(e)
        time.sleep(3 + 4 * i)
    raise RuntimeError(f"routescan {params.get('action')} {params.get('address')}: {err}")

def rpc(method, params):
    body_req = json.dumps({"jsonrpc": "2.0", "id": 1, "method": method, "params": params}).encode()
    key = hashlib.sha256((RPC + body_req.decode()).encode()).hexdigest()
    p = _cache(key)
    if p.exists():
        return json.loads(p.read_bytes())["result"]
    err = None
    for i in range(6):
        try:
            body = _http(RPC, body_req)
            d = json.loads(body)
            if "result" in d and d["result"] is not None:
                _store(key, RPC + " " + method + " " + json.dumps(params), body)
                return d["result"]
            err = str(d.get("error"))
        except Exception as e:
            err = repr(e)
        time.sleep(2 + 3 * i)
    raise RuntimeError(f"rpc {method} {params}: {err}")

def pull(address, action, start=0, end=99999999, offset=10000):
    """Historique complet par fenêtres de blocs. Le dernier bloc d'une page pleine est relu en entier à la page suivante,
    donc aucun doublon ni trou à la frontière (sauf un bloc à plus de `offset` lignes pour une seule adresse)."""
    out, b = [], start
    while True:
        res = rs(module="account", action=action, address=address, startblock=b, endblock=end, page=1, offset=offset, sort="asc")
        res = res or []
        if len(res) < offset:
            out += res
            return out
        last = int(res[-1]["blockNumber"])
        keep = [r for r in res if int(r["blockNumber"]) < last]
        assert keep, f"bloc {last} a plus de {offset} lignes pour {address}"
        out += keep
        b = last

BS = "https://eth.blockscout.com/api/v2"

def bs(path, params=None):
    """Blockscout v2 sans clé. Cache par URL. Réessaie sur 429 et 5xx ; lève une erreur sinon."""
    url = BS + path + ("?" + urllib.parse.urlencode(params) if params else "")
    key = hashlib.sha256(url.encode()).hexdigest()
    p = _cache(key)
    if p.exists():
        return json.loads(p.read_bytes())
    err = None
    for i in range(10):
        try:
            time.sleep(1.1)
            body = _http(url)
            d = json.loads(body)
            _store(key, url, body)
            return d
        except urllib.error.HTTPError as e:
            err = repr(e)
            if e.code == 404:
                raise
        except Exception as e:
            err = repr(e)
        time.sleep(5 + 6 * i)
    raise RuntimeError(f"blockscout {url}: {err}")

def bs_all(address, kind, extra=None, max_pages=100000):
    """Toutes les pages de /addresses/<a>/<kind> (token-transfers, transactions, internal-transactions)."""
    items, params, n = [], dict(extra or {}), 0
    while True:
        d = bs(f"/addresses/{address}/{kind}", params or None)
        items += d.get("items") or []
        n += 1
        nxt = d.get("next_page_params")
        if not nxt or n >= max_pages:
            return items, (nxt is None)
        params = {**(extra or {}), **{k: v for k, v in nxt.items() if v is not None}}

def internals(address):
    """Transactions internes : Blockscout si complet, sinon Routescan (txlistinternal) mis au format Blockscout utile ici.
    Retourne (items, source)."""
    try:
        if os.environ.get("EV_SKIP_BS_INTERNAL"):  # Blockscout expire sur les très grosses adresses (2d86)
            raise RuntimeError("skip")
        items, complete = bs_all(address, "internal-transactions", max_pages=int(os.environ.get("EV_BS_INTERNAL_MAX", "100000")))
        if complete:
            return items, "blockscout-v2"
    except Exception:
        pass
    import datetime as _dt
    out = []
    for x in pull(address, "txlistinternal"):
        out.append({"transaction_hash": x["hash"], "from": {"hash": x["from"]}, "to": {"hash": x["to"]}, "value": x["value"],
                    "timestamp": _dt.datetime.fromtimestamp(int(x["timeStamp"]), _dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000000Z"),
                    "block_number": int(x["blockNumber"]), "success": x.get("isError") == "0", "index": -1})
    return out, "routescan"

def meta_tags(address):
    """Tags du service metadata de Blockscout (sans clé), mis en cache. Liste de noms."""
    url = f"https://metadata.services.blockscout.com/api/v1/metadata?chainId=1&addresses={address}"
    key = hashlib.sha256(url.encode()).hexdigest(); p = _cache(key)
    if not p.exists():
        time.sleep(0.5); _store(key, url, _http(url))
    d = json.loads(p.read_bytes()).get("addresses") or {}
    return [t.get("name") for v in d.values() for t in (v.get("tags") or [])]
