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

# Reprises du dépôt WSMO (code/05_trace_origin.py), issues d'études antérieures : service, sans nom certifié ici.
WSMO = {
    "G2YxRa6wt1qePMwfJzdXZG62ej4qaTC7YURzuh2Lwd3t": "Service de swap G2Y (attribué ChangeNOW par les études WSMO)",
    "BmFdpraQhkiDQE6SnfG5omcA1VwzqfXrwtNYBwWTymy6": "Échange, hot wallet (études WSMO)",
    "2snHHreXbpJ7UwZxPe37gnUNf7Wx7wv6UKDSR2JckKuS": "Pont, solveur (études WSMO)",
    "u6PJ8DtQuPFnfmwHbGFULQ4u4EgjDiyYKjVEsynXq2w": "Service de swap (études WSMO)",
    "is6MTRHEgyFLNTfYcuV4QBWLjrZBfmhVNYR6ccgr8KV": "Échange, hot wallet (études WSMO)",
}

# Exécutants de Jupiter DCA, vérifiés dans les transactions (signataire, programme DCA265Vj, InitiateFlashFill) : jamais un lien.
KEEPERS = {"JD25qVdtd65FoiXNmR89JjmoJdYk9sjYQeSTZAALFiMy": "Jupiter DCA, exécutant",
           "JD1dHSqYkrXvqUVL8s6gzL1yB7kpYymsHfwsGxgwp55h": "Jupiter DCA, exécutant",
           "JD38n7ynKYcgPpF7k1BhXEeREu1KqptU93fVGy3S624k": "Jupiter DCA, exécutant",
           "DCAKuApAuZtVNYLk3KTAVW9GLWVvPbnb5CxxRRmVgcTr": "Jupiter DCA, exécutant",
           "DCAKxn5PFNN1mBREPWGdk1RXg5aVH9rPErLfBFEi2Emb": "Jupiter DCA, exécutant",
           "DCAK36VfExkPdAkYUQg6ewgxyinvcEyPLyHjRbmveKFw": "Jupiter DCA, exécutant",
           "AYymVrcAyPgcMcFkk5NqaEBLj7C4KH2NYvLognUGCEq5": "Escrow d'un ordre Jupiter DCA du créateur",
           "sYBdq543ZX4iAXpNzhT4kTvKBaEDUGkiUo9jBFYdaNd": "Escrow d'un ordre Jupiter DCA de 5QhJJc"}


def load() -> dict[str, tuple[str, str]]:
    if _LABELS:
        return _LABELS
    p = ROOT / "evidence" / "labels" / "dune_cex_solana_addresses.sql"
    # lignes de la forme ('solana', 'adresse', 'Binance', 'Binance 1', ...), avec ou sans cast
    for m in re.finditer(r"([1-9A-HJ-NP-Za-km-z]{32,44})'[^,]*,\s*'([^']+)'\s*,\s*'([^']*)'", p.read_text()):
        _LABELS[m.group(1)] = (m.group(3) or m.group(2), "dune spellbook cex_solana_addresses")
    # Comptes publiés par la documentation officielle de Jupiter (jup-ag/docs, transaction/submit.mdx, archivée).
    # Virements et transferts avec eux = jambes de routage ou pourboires d'exécution, jamais un lien entre personnes.
    for a in re.findall(r'"([1-9A-HJ-NP-Za-km-z]{32,44})"', (ROOT / "evidence" / "labels" / "jupiter_docs_submit.mdx").read_text()):
        _LABELS.setdefault(a, ("Jupiter, compte documenté", "jup-ag/docs transaction/submit.mdx"))
    for a in re.findall(r"'([1-9A-HJ-NP-Za-km-z]{32,44})'|\"([1-9A-HJ-NP-Za-km-z]{32,44})\"", (ROOT / "evidence" / "labels" / "defillama_fees_jupiter.ts").read_text()):
        _LABELS.setdefault(a[0] or a[1], ("Jupiter, compte listé par DefiLlama", "DefiLlama fees/jupiter.ts"))
    for a, n in WSMO.items():
        _LABELS.setdefault(a, (n, "études WSMO, code/05_trace_origin.py"))
    for a, n in KEEPERS.items():
        _LABELS.setdefault(a, (n, "lu dans les transactions"))
    for a, n in INFRA.items():
        _LABELS[a] = (n, "lu dans les transactions")
    return _LABELS


def label(addr: str) -> str | None:
    v = load().get(addr)
    return v[0] if v else None
