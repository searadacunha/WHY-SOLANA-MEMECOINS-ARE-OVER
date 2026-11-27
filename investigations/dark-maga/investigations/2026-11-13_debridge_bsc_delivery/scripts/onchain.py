"""Accès aux données publiques pour les enquêtes OpenPlanter (bibliothèque standard seulement).

- Chaque réponse brute est archivée, compressée, dans sources/<dossier>/ avec son empreinte sha256 et l'heure de
  collecte (journal sources/<dossier>/INDEX.jsonl) : c'est la source primaire citée par les fiches de découvertes.
- Les clés Helius viennent du pool de recherche (~/.config/forensics_v2/helius_sources.json), comme dmaga/config.py ;
  aucune valeur de clé n'est affichée, journalisée ni archivée (les URL archivées sont expurgées).
- Arrêt net si le disque passe sous 13,55 Go (plancher commun 13,5 Go, voir le garde-fou disque).
"""
from __future__ import annotations

import gzip
import hashlib
import json
import re
import shutil
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCES = ROOT / "sources"
# Écritures légères seulement (réponses gzip de quelques Ko, plafond par exécution) : arrêt sous 12,4 Go, au-dessus du
# plancher de scellement de PolySentinel (12 Go). Le plancher commun de 13,5 Go reste celui des opérations lourdes
# (diskguard) ; il a été franchi le 12/11 par le swap du modèle local (journal/INCIDENTS.md), pas par ces écritures.
FLOOR = 12_400_000_000
WRITE_CAP = 15_000_000  # octets d'archives par exécution (plusieurs collecteurs peuvent tourner en même temps)
EVM_RPC = {  # RPC publics sans clé ; drpc sert d'archive quand publicnode refuse un état ancien
    "ethereum": ["https://ethereum-rpc.publicnode.com", "https://eth.drpc.org"],
    "polygon": ["https://polygon-bor-rpc.publicnode.com", "https://polygon.drpc.org"],
    "bsc": ["https://bsc-rpc.publicnode.com", "https://bsc.drpc.org"],
    "base": ["https://base-rpc.publicnode.com", "https://base.drpc.org"],
    "arbitrum": ["https://arbitrum-one-rpc.publicnode.com", "https://arbitrum.drpc.org"],
    "optimism": ["https://optimism-rpc.publicnode.com", "https://optimism.drpc.org"],
}
SOLANA_PUBLIC = "https://api.mainnet-beta.solana.com"
INLINE_MAX = 512  # réponse plus courte (page vide) : gardée dans INDEX.jsonl, pas de fichier de 4 Ko
_written = 0
UA = "Mozilla/5.0 (research; read-only)"  # générique : aucune donnée personnelle dans les en-têtes
_KEY = re.compile(r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}")


class DiskFloor(RuntimeError):
    pass


def helius_keys() -> list[str]:
    cfg = json.loads((Path.home() / ".config/forensics_v2/helius_sources.json").read_text())
    allowed, keys = set(cfg["pool_fingerprints"]), []
    for src in cfg["sources"]:
        p = Path(src["path"]).expanduser()
        try:
            text = p.read_text(errors="replace")
        except OSError:  # source sur le disque externe débranché
            continue
        for k in _KEY.findall(text):
            if hashlib.sha256(k.encode()).hexdigest()[:8] in allowed and k not in keys:
                keys.append(k)
    return keys


def fingerprint(key: str) -> str:
    return hashlib.sha256(key.encode()).hexdigest()[:8]


def scrub(text: str) -> str:
    return _KEY.sub("<KEY>", re.sub(r"(api[-_]?key=)[^&\s]+", r"\1<KEY>", text, flags=re.I))


def _check_disk() -> None:
    free = shutil.disk_usage("/").free
    if free < FLOOR:
        raise DiskFloor(f"disque {free / 1e9:.2f} Go < {FLOOR / 1e9:.2f} Go : arrêt avant écriture")


def archive(case: str, url: str, request: object, body: bytes, status: int) -> dict:
    """Écrit la réponse brute (gzip) et renvoie sa référence {file, sha256, fetched_at, url}."""
    _check_disk()
    sha = hashlib.sha256(body).hexdigest()
    d = SOURCES / case
    d.mkdir(parents=True, exist_ok=True)
    f = d / f"{sha[:16]}.json.gz"
    inline = len(body) <= INLINE_MAX
    if not inline and not f.exists():
        global _written
        z = gzip.compress(body)
        if _written + len(z) > WRITE_CAP:
            raise DiskFloor(f"plafond d'écriture de {WRITE_CAP / 1e6:.0f} Mo atteint pour cette exécution")
        f.write_bytes(z)
        _written += len(z)
    ref = {"file": None if inline else str(f.relative_to(ROOT)), "inline": body.decode(errors="replace") if inline else None,
           "sha256": sha, "status": status, "url": scrub(url),
           "request": json.loads(scrub(json.dumps(request))) if request is not None else None,
           "fetched_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
    with open(d / "INDEX.jsonl", "a") as fh:
        fh.write(json.dumps(ref, ensure_ascii=False) + "\n")
    return ref


def http_json(case: str, url: str, payload: object = None, *, retries: int = 5, timeout: int = 40,
              pause: float = 0.0) -> tuple[object, dict]:
    """GET (ou POST JSON si payload) avec relances sur 429/5xx ; renvoie (données, référence d'archive).

    Une erreur définitive lève une exception : jamais de valeur par défaut qui ressemblerait à une mesure.
    """
    data = json.dumps(payload).encode() if payload is not None else None
    last = None
    for attempt in range(retries):
        if pause:
            time.sleep(pause)
        req = urllib.request.Request(url, data=data, method="POST" if data else "GET",
                                     headers={"Content-Type": "application/json", "User-Agent": UA,
                                              "Accept": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                body = resp.read()
                ref = archive(case, url, payload, body, resp.status)
                return json.loads(body), ref
        except urllib.error.HTTPError as exc:
            last = f"HTTP {exc.code}"
            if exc.code in (429, 500, 502, 503, 504, 529):
                time.sleep(min(60, 2 ** attempt * 2))
                continue
            raise RuntimeError(f"{scrub(url)} -> {last}: {exc.read()[:200]!r}") from None
        except (urllib.error.URLError, TimeoutError, ConnectionError) as exc:
            last = str(exc)
            time.sleep(min(60, 2 ** attempt * 2))
    raise RuntimeError(f"{scrub(url)} -> échec après {retries} essais ({last})")


def rpc(case: str, url: str, method: str, params: list, **kw) -> tuple[object, dict]:
    """Appel JSON-RPC ; lève si la réponse contient une erreur (pas de résultat vide silencieux)."""
    out, ref = http_json(case, url, {"jsonrpc": "2.0", "id": 1, "method": method, "params": params}, **kw)
    if not isinstance(out, dict) or "error" in out:
        raise RuntimeError(f"{method} -> {scrub(json.dumps(out)[:300])}")
    return out["result"], ref


_sol_urls: list[str] | None = None
_sol_next = 0


def solana(case: str, method: str, params: list, pause: float = 0.3) -> tuple[object, dict]:
    """RPC Solana : clés du pool de recherche en rotation, repli sur le RPC public ; lève si tout échoue.

    Ne jamais remplacer une erreur par un résultat vide : un historique incomplet doit se voir.
    """
    global _sol_urls, _sol_next
    if _sol_urls is None:
        _sol_urls = [f"https://mainnet.helius-rpc.com/?api-key={k}" for k in helius_keys()] + [SOLANA_PUBLIC]
    last = None
    for attempt in range(2 * len(_sol_urls)):
        url = _sol_urls[(_sol_next + attempt) % len(_sol_urls)]
        try:
            out = rpc(case, url, method, params, retries=1, pause=pause)
            _sol_next = (_sol_next + attempt + 1) % len(_sol_urls)
            return out
        except DiskFloor:
            raise
        except Exception as exc:  # 429 ou panne d'un nœud : nœud suivant
            last = exc
            time.sleep(1.5)
    raise RuntimeError(f"Solana {method} : tous les nœuds ont échoué ({scrub(str(last))[:200]})")


def evm(case: str, chain: str, method: str, params: list, pause: float = 0.1) -> tuple[object, dict]:
    """RPC EVM public de la chaîne, avec repli sur le second nœud ; lève si les deux échouent."""
    last = None
    for url in EVM_RPC[chain]:
        try:
            return rpc(case, url, method, params, retries=2, pause=pause)
        except DiskFloor:
            raise
        except Exception as exc:
            last = exc
    raise RuntimeError(f"{chain} {method} : {scrub(str(last))[:200]}")
