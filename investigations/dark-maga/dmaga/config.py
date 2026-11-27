"""Constantes de l'enquête et chemins. Aucune clé n'est écrite ici ni journalisée."""
import hashlib
import json
import os
import re
from pathlib import Path

MINT = "7D7BRcBYepfi77vxySapmeqRNN1wsBBxnFPJGbH5pump"
BONDING_CURVE = "87g44hEXP7R8ZxoAJtz941tsVftpEXC1LqAFTf2ZHtkH"
RAYDIUM_POOL = "CRSwXnfF21yHDXdYBVWwCwQ5Ni2A4QuK3qGYis5k7x7k"
RAYDIUM_AUTHORITY = "5Q544fKrFoe6tsEbD7S8EmxGTJYAKtTVhAW5Q5pge4j1"
WSOL = "So11111111111111111111111111111111111111112"

ROOT = Path(__file__).resolve().parent.parent
# Disque USB en direct : l'image PHI-Data met 174 s à renommer un fichier, FAT32 0,002 s (mesuré le 02/11).
# FAT32 : 4 Gio max par fichier, pas de liens symboliques, donc pas de base DuckDB persistante ici.
EXT = Path(os.environ.get("DMAGA_EXT", "/Volumes/VERBATIM HD/Dark-MAGA-Investigation"))
RAW = EXT / "raw"
DATA = ROOT / "data"  # petits livrables, gros fichiers reliés vers BIG
BIG = EXT / "data"
LOGS = EXT / "logs"
TMP = EXT / "tmp"
EVIDENCE = ROOT / "evidence"  # preuves légères (posts X, captures, manifeste)
STATE = ROOT / "state"

_KEY = re.compile(r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}")


def helius_keys() -> list[str]:
    """Pool de recherche : sources et empreintes de ~/.config/forensics_v2/helius_sources.json.

    Les clés de ~/Downloads/.env et du bot servent à des services en production : on n'y touche pas.
    Aucune valeur de clé n'est recopiée ni journalisée.
    """
    cfg = json.loads((Path.home() / ".config" / "forensics_v2" / "helius_sources.json").read_text())
    allowed = set(cfg["pool_fingerprints"])
    keys: list[str] = []
    for src in cfg["sources"]:
        p = Path(src["path"]).expanduser()
        if not p.exists():
            continue
        for k in _KEY.findall(p.read_text(errors="replace")):
            if hashlib.sha256(k.encode()).hexdigest()[:8] in allowed and k not in keys:
                keys.append(k)
    if not keys:
        raise RuntimeError("aucune clé du pool de recherche trouvée")
    return keys


def scrub(text: str) -> str:
    """Retire toute clé d'un message avant journalisation."""
    return _KEY.sub("<KEY>", text)
