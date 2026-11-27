"""RPC public Solana (api.mainnet-beta.solana.com), sans clé : signatures et transactions historiques.

Débit bas (limite publique ~40 requêtes / 10 s par méthode et par IP). Les transactions sont mises en cache (sha256 de la
signature) sous KEKIUS_EXT/pub ; une erreur persistante lève une exception, jamais un résultat vide silencieux."""
import gzip, json, threading, time, urllib.error, urllib.request
from k_lib import EXT

URL = "https://api.mainnet-beta.solana.com"
CACHE = EXT / "pub"
_lock = threading.Lock()
_last = [0.0]
GAP = 0.3


def call(method, params, tries=12):
    body = json.dumps({"jsonrpc": "2.0", "id": 1, "method": method, "params": params}).encode()
    delay, err = 2.0, ""
    for _ in range(tries):
        with _lock:
            w = _last[0] + GAP - time.monotonic()
            if w > 0:
                time.sleep(w)
            _last[0] = time.monotonic()
        try:
            req = urllib.request.Request(URL, data=body, headers={"content-type": "application/json", "user-agent": "dmaga-research/1.0"})
            with urllib.request.urlopen(req, timeout=60) as r:
                d = json.load(r)
        except urllib.error.HTTPError as e:
            err = f"HTTP {e.code}"
            time.sleep(delay); delay = min(delay * 2, 60); continue
        except Exception as e:
            err = repr(e)
            time.sleep(delay); delay = min(delay * 2, 60); continue
        if "error" in d:
            err = json.dumps(d["error"])[:200]
            if d["error"].get("code") in (429, -32429, -32005) or "rate" in err.lower():
                time.sleep(delay); delay = min(delay * 2, 60); continue
            raise RuntimeError(f"{method}: {err}")
        return d["result"]
    raise RuntimeError(f"{method}: échec après {tries} essais : {err}")


def sigs(address, max_pages=5):
    """Toutes les signatures (plus récentes d'abord), jusqu'à max_pages × 1000. Rend (liste, tronqué?)."""
    out, before = [], None
    for _ in range(max_pages):
        p = {"limit": 1000, **({"before": before} if before else {})}
        res = call("getSignaturesForAddress", [address, p])
        out += res
        if len(res) < 1000:
            return out, False
        before = res[-1]["signature"]
    return out, True


def tx(sig):
    p = CACHE / sig[:2] / (sig + ".json.gz")
    if p.exists():
        return json.loads(gzip.decompress(p.read_bytes()))
    r = call("getTransaction", [sig, {"maxSupportedTransactionVersion": 1, "encoding": "jsonParsed"}])
    if r is None:
        raise RuntimeError(f"getTransaction {sig}: null")
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes(gzip.compress(json.dumps(r).encode(), 6))
    return r
