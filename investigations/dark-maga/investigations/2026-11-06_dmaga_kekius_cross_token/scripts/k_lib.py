"""Chemins et constantes de l'enquête DMAGA × KEKIUS. Aucune clé ici : Helius passe par dmaga.config (pool de recherche).

Les données brutes restent hors dépôt : KEKIUS_EXT (défaut ../../../../raw relatif au clone) reçoit les pages Helius
(via dmaga.collect, qui lit DMAGA_EXT) et le cache EVM (EV_RAW)."""
import datetime as dt
import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
INV = HERE.parent
REPO = INV.parents[1]
EXT = Path(os.environ.get("KEKIUS_EXT", REPO.parent / "raw")).resolve()
os.environ.setdefault("DMAGA_EXT", str(EXT / "sol"))
os.environ.setdefault("EV_RAW", str(EXT / "evm"))
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "investigations" / "2026-11-05_evm-recipient-deeptrace" / "scripts"))
DATA = INV / "data"
EVID = INV / "evidence"
# Données DMAGA déjà dérivées (disque externe de l'enquête d'origine, non publié en entier)
DMAGA_BIG = Path(os.environ.get("DMAGA_BIG", "/Volumes/VERBATIM HD/Dark-MAGA-Investigation/data_v2"))

# Tokens étudiés (vérifiés on-chain le 06/11, voir FINDINGS.md §1)
KM = "HuAncxDEsakCDgZS2Yfo9xJbHmtHXMnxxkT9jqdXnHhm"          # Solana, Pump.fun, créé 2024-12-10 07:29:00
KM_CURVE = "92d2PputxVRXp5hLY17EcAr9m1CG2cFG1PoSU2JZdxaH"
XC = "XC78JjRHnSqaysrHiTrhR8eRngFbvX3rrHyRjWEpump"           # Solana, Pump.fun, créé 2024-12-29 16:33:45
XC_CURVE = "8bHymiGnSP4sKxz7uyzi86AfXGibWqNAG8U3tWQPh2X9"
ETH_KEKIUS = "0x26e550ac11b26f78a04489d5f20f24e3559f7dd9"      # Ethereum, créé 2024-12-14 02:29:35, bloc 21397776
DMAGA = "7D7BRcBYepfi77vxySapmeqRNN1wsBBxnFPJGbH5pump"
WSOL = "So11111111111111111111111111111111111111112"
T_END = 1735948800  # 2025-01-04 00:00:00 UTC : fin de la fenêtre de collecte


def utc(t):
    return dt.datetime.fromtimestamp(int(t), dt.UTC).strftime("%Y-%m-%d %H:%M:%S") if t is not None else ""
