"""Étiquettes d'adresses, toujours avec leur source. Une étiquette désigne un service, pas une personne."""
import re
from pathlib import Path

from .config import ROOT

_LABELS: dict[str, tuple[str, str]] = {}

# Programmes et autorités vérifiés dans les transactions de cette enquête.
INFRA = {
    "5Q544fKrFoe6tsEbD7S8EmxGTJYAKtTVhAW5Q5pge4j1": "Raydium AMM v4 authority",
    "39azUYFWPz3VHgKCf3VChUwbpURdCHRxjWVowf5jUJjg": "Pump.fun migration",
    "PNLCQcVCD26aC7ZWgRyr5ptfaR7bBrWdTFgRWwu2tvF": "Raydium fee collector",
    "87g44hEXP7R8ZxoAJtz941tsVftpEXC1LqAFTf2ZHtkH": "DMAGA bonding curve",
    "TSLvdd1pWpHVjahSpsvCXUbgwsL3JAcvokwaKt1eokM": "Pump.fun mint authority",
}


def load() -> dict[str, tuple[str, str]]:
    if _LABELS:
        return _LABELS
    p = ROOT / "evidence" / "labels" / "dune_cex_solana_addresses.sql"
    # lignes de la forme ('solana', 'adresse', 'Binance', 'Binance 1', ...), avec ou sans cast
    for m in re.finditer(r"([1-9A-HJ-NP-Za-km-z]{32,44})'[^,]*,\s*'([^']+)'\s*,\s*'([^']*)'", p.read_text()):
        _LABELS[m.group(1)] = (m.group(3) or m.group(2), "dune spellbook cex_solana_addresses")
    for a, n in INFRA.items():
        _LABELS[a] = (n, "lu dans les transactions")
    return _LABELS


def label(addr: str) -> str | None:
    v = load().get(addr)
    return v[0] if v else None
