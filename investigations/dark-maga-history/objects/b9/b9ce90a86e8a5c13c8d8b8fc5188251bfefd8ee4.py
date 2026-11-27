"""Constantes de l'enquête et chemins. Aucune clé n'est écrite ici ni journalisée."""
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
    """Clés lues à l'exécution dans ~/Downloads/.env, dédoublonnées, jamais recopiées."""
    keys: list[str] = []
    env = Path.home() / "Downloads" / ".env"
    for line in env.read_text(errors="replace").splitlines():
        if "HELIUS" in line.upper() and "=" in line and not line.lstrip().startswith("#"):
            for k in _KEY.findall(line):
                if k not in keys:
                    keys.append(k)
    if not keys:
        raise RuntimeError("aucune clé Helius trouvée dans ~/Downloads/.env")
    return keys


def scrub(text: str) -> str:
    """Retire toute clé d'un message avant journalisation."""
    return _KEY.sub("<KEY>", text)
