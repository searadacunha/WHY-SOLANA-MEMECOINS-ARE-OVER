"""Famille Coinbase présumée par balayages (K12, evidence/labels/hot_presume.tsv). Déduction de l'audit D : jamais une étiquette vérifiée, donc hors de labels.py."""
import csv

from .config import ROOT

with (ROOT / "evidence" / "labels" / "hot_presume.tsv").open() as _f:
    HOT_PRESUME = {r["adresse"] for r in csv.DictReader(_f, delimiter="\t")}
