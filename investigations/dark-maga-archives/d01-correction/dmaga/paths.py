"""Racine du dérivé. `config.py` est gelé et fixe BIG = EXT/data : DMAGA_BIG (data_v2) la remplace sans y toucher.

Avec DMAGA_BIG, les petits dérivés (windows.csv, prevent_groups.json...) y vont aussi : data/ du dépôt et BIG restent tels quels.
Sans lui, tout retombe sur config.py, en lecture : un script qui écrit du dérivé appelle exige_v2().
"""
import os
import sys
from pathlib import Path

from .config import BIG as BIG_GELE, DATA as SOURCES  # SOURCES : data/ du dépôt, posts X et archives de réponses réseau

_v2 = os.environ.get("DMAGA_BIG")
BIG = Path(_v2) if _v2 else BIG_GELE
DATA = BIG if _v2 else SOURCES


def exige_v2() -> None:
    """Le dérivé de BIG_GELE est au manifeste evidence/RAW_MANIFEST.tsv : il ne doit ni changer ni disparaître."""
    if not _v2:
        sys.exit("DMAGA_BIG absent : ce script écraserait le dérivé listé dans evidence/RAW_MANIFEST.tsv")
    BIG.mkdir(parents=True, exist_ok=True)
