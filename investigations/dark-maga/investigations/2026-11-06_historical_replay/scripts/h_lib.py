"""Chemins et constantes du rejeu historique (sources X du 06/11/2026). Aucune clé ici.

Réutilise le client RPC public (k16) et les décodeurs de soldes (k11) de l'enquête Kekius : même règle de calcul, même cache.
Les données brutes restent hors dépôt, sur le disque de l'enquête (HIST_EXT)."""
import datetime as dt
import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
INV = HERE.parent
REPO = INV.parents[1]
EXT = Path(os.environ.get("HIST_EXT", "/Volumes/VERBATIM HD/Dark-MAGA-Investigation/raw/historical_replay")).resolve()
os.environ.setdefault("DMAGA_EXT", "/Volumes/VERBATIM HD/Dark-MAGA-Investigation")
os.environ.setdefault("KEKIUS_EXT", str(EXT))  # k16_pubrpc met son cache dans KEKIUS_EXT/pub
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "investigations" / "2026-11-06_dmaga_kekius_cross_token" / "scripts"))
DATA = INV / "data"
EVID = INV / "evidence"
DMAGA_BIG = Path(os.environ.get("DMAGA_BIG", "/Volumes/VERBATIM HD/Dark-MAGA-Investigation/data"))

DMAGA = "7D7BRcBYepfi77vxySapmeqRNN1wsBBxnFPJGbH5pump"
WSOL = "So11111111111111111111111111111111111111112"
CURVE = "87g44hEXP7R8ZxoAJtz941tsVftpEXC1LqAFTf2ZHtkH"
T_CREATE = 1720922725   # 14/07/2024 02:05:25, création du mint (signature fePxr7ER…)
T_MIGRATE = 1720923331  # 14/07/2024 02:15:31, migration Raydium

W7GVC = "7GVCZAYG5NfiJsuqUdvc9hB2ts2W3tSrGdya4CyR1M5j"
W9SXM = "9Sxmf25WG5WVQ5p86ycWeo5hMEwxiWPkFtLdRdTrHSQS"
# Les quatre listes publiées par @Noah_nftn le 22/07/2024 13:04:17 UTC (post 1815372294426124565), recopiées du mémo historique A4
NOAH = {
    1: ["EaoxyxgjUZvksR57aNy2jHWno3DCBNQU4dd4BWhgk66w", "BteHCeVLvbSDYy9X5ZUZLyfLLzE7MrQ4jcrWSF7F65D2"],
    2: ["5QhJJcFZu2ashyKyWSTGHcsyo6ZBCbpVuJqeutvQHScd", "NxtXcmEW3gQvrCdBEm5GYT3zaqMre3QiPUhnwViNsD7",
        "7FGoCB63x3FAJNF25MMZG8pheR4rRtJbApQuynJRxLdE", "7mdCAs8CWYJxkWz2gfj3sRhDBmUi6Q9qvRGuKiv2Bazu",
        "GFpqfjEQFhXRbWEJCwUqKuNjSNTCgqAsANMbVyTGmi1p"],
    3: ["APfA9dgxbnLGw4gexrJNDMU7XdS1juHP4fbATDi84sK", "9SHtoDswbWxmqyFm2CYj6fcJgnQMgefG1ZtwerEg2BZZ"],
    4: [W7GVC, "AeiMit5PMUvdJSsa8jm2RpHJCdfJLFyW6dzkm65w1ybh", W9SXM],
}


def utc(t):
    return dt.datetime.fromtimestamp(int(t), dt.UTC).strftime("%Y-%m-%d %H:%M:%S") if t is not None else ""


_PX = {}


def sol_usd(t):
    """Clôture SOLUSDT Binance de la minute de t (fichiers mensuels de l'enquête d'origine, raw/solusd)."""
    import csv, io, zipfile
    m = dt.datetime.fromtimestamp(int(t), dt.UTC).strftime("%Y-%m")
    if m not in _PX:
        z = Path(os.environ["DMAGA_EXT"]) / "raw" / "solusd" / f"SOLUSDT-1m-{m}.zip"
        d = {}
        with zipfile.ZipFile(z) as f, f.open(f.namelist()[0]) as fh:
            for row in csv.reader(io.TextIOWrapper(fh)):
                if row and row[0].isdigit():
                    ms = int(row[0])
                    d[(ms // 1000 if ms > 10**14 else ms) // 60000] = float(row[4])
        _PX[m] = d
    return _PX[m][int(t) // 60]
