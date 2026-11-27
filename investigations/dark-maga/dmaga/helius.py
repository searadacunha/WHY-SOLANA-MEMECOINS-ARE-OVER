"""Client Helius : lève les erreurs (jamais de None silencieux), compte tout, tourne les clés."""
import json
import threading
import time
import urllib.error
import urllib.request
from collections import Counter

from .config import helius_keys, scrub


class RpcError(RuntimeError):
    pass


class Helius:
    def __init__(self, rps: float = 6.0, timeout: int = 120, max_tries: int = 10):
        self.keys = helius_keys()
        self.i = 0
        self.min_gap = 1.0 / rps
        self.last = 0.0
        self.timeout = timeout
        self.max_tries = max_tries
        self.stats = Counter()
        self.lock = threading.Lock()
        self.dead: set[str] = set()

    def _next_key(self) -> str:
        with self.lock:
            for _ in range(len(self.keys)):
                k = self.keys[self.i % len(self.keys)]
                self.i += 1
                if k not in self.dead:
                    return k
        raise RpcError("toutes les clés Helius sont épuisées ou refusées")

    def _throttle(self) -> None:
        with self.lock:
            wait = self.last + self.min_gap - time.monotonic()
            self.last = max(self.last + self.min_gap, time.monotonic())
        if wait > 0:
            time.sleep(wait)

    def call(self, method: str, params: list):
        body = json.dumps({"jsonrpc": "2.0", "id": 1, "method": method, "params": params}).encode()
        delay = 1.0
        last_err = ""
        for attempt in range(self.max_tries):
            self._throttle()
            key = self._next_key()
            url = f"https://mainnet.helius-rpc.com/?api-key={key}"
            req = urllib.request.Request(url, data=body, headers={"content-type": "application/json"})
            self.stats["requests"] += 1
            try:
                with urllib.request.urlopen(req, timeout=self.timeout) as r:
                    payload = json.load(r)
            except urllib.error.HTTPError as e:
                msg = scrub(e.read()[:300].decode(errors="replace"))
                self.stats[f"http_{e.code}"] += 1
                last_err = f"HTTP {e.code}: {msg}"
                if e.code in (401, 403) or "max usage" in msg.lower():
                    self.dead.add(key)  # quota ou droit perdu : on passe à la clé suivante sans attendre
                    continue
                if e.code == 400:
                    raise RpcError(f"{method}: {last_err}")
                time.sleep(delay)
                delay = min(delay * 2, 60)
                continue
            except Exception as e:  # réseau, timeout, JSON tronqué : on retente, on ne masque pas
                self.stats["net_errors"] += 1
                last_err = scrub(repr(e))
                time.sleep(delay)
                delay = min(delay * 2, 60)
                continue
            if "error" in payload:
                err = scrub(json.dumps(payload["error"])[:300])
                self.stats["rpc_errors"] += 1
                last_err = err
                code = payload["error"].get("code")
                if code == -32429 or "rate" in err.lower():
                    time.sleep(delay)
                    delay = min(delay * 2, 60)
                    continue
                raise RpcError(f"{method}: {err}")
            self.stats["ok"] += 1
            return payload["result"]
        raise RpcError(f"{method}: échec après {self.max_tries} essais, dernier: {last_err}")

    def txs_page(self, address: str, *, details="full", limit=1000, sort="asc", token=None, filters=None):
        opts = {"transactionDetails": details, "sortOrder": sort, "limit": limit}
        if details == "full":
            opts["encoding"] = "jsonParsed"
            opts["maxSupportedTransactionVersion"] = 1  # des transactions version 1 existent depuis 2026
        if token:
            opts["paginationToken"] = token
        if filters:
            opts["filters"] = filters
        return self.call("getTransactionsForAddress", [address, opts])
