"""Racine du dérivé. `config.py` est gelé et fixe BIG = EXT/data : DMAGA_BIG (data_v2) la remplace sans y toucher.

Avec DMAGA_BIG, les petits dérivés (windows.csv, prevent_groups.json...) y vont aussi : data/ du dépôt et BIG restent tels quels.
Sans lui, tout retombe sur config.py, en lecture : un script qui écrit du dérivé appelle exige_v2().
"""
import os
import sys
from pathlib import Path

from .config import BIG as BIG_GELE, DATA as SOURCES, RAW, ROOT  # SOURCES : data/ du dépôt, posts X et archives de réponses réseau

_v2 = os.environ.get("DMAGA_BIG")
BIG = Path(_v2).expanduser().resolve() if _v2 else BIG_GELE
DATA = BIG if _v2 else SOURCES


def exige_v2() -> None:
    """Le dérivé de BIG_GELE est au manifeste evidence/RAW_MANIFEST.tsv : il ne doit ni changer ni disparaître."""
    if not _v2 or not _v2.strip():
        sys.exit("DMAGA_BIG absent : ce script écraserait le dérivé listé dans evidence/RAW_MANIFEST.tsv")
    target = BIG.expanduser().resolve()
    protected = (BIG_GELE, SOURCES, RAW, ROOT / "evidence", ROOT / "etude_final", ROOT / "etude_groupe")
    for root in protected:
        root = root.resolve()
        # Un alias, un sous-dossier ou un parent d'une preuve ne constitue pas un dérivé distinct.
        if target == root or target.is_relative_to(root) or root.is_relative_to(target):
            sys.exit(f"DMAGA_BIG recouvre un chemin protégé : {root}. Choisir un dossier séparé, par exemple data_v2.")
    BIG.mkdir(parents=True, exist_ok=True)
