"""Textes de l'audit du 03/11 repris mot pour mot dans les rapports : aucun chiffre ni aucune adresse n'est retapé.

Ces textes sont déjà en français : ils passent après fr(), qui lirait « 2,886 » comme un millier. Dans un gabarit, écrire @@N01@@ puis appeler rendu().
"""
import csv
import re
from pathlib import Path

from .frfmt import fr

AUD = Path("audits/2026-11-03")
CLAIMS = {r["id"]: r for r in csv.DictReader((AUD / "CLAIM_VERIFICATION.csv").open())}
INTERPRETATION = re.search(r"« (Verdict du plan : .*?) »", (AUD / "AUDIT_FINAL.md").read_text(), re.S).group(1)
_AUDITS = {"A": AUD / "AUDIT_A_DATA.md", "B": AUD / "AUDIT_B_STATISTICS.md", "C": AUD / "AUDIT_C_ATTRIBUTION.md"}


def niveau_et_texte(cid: str) -> tuple[str, str]:
    """Une ligne N de CLAIM_VERIFICATION.csv : « [niveau] assertion »."""
    m = re.match(r"\[(.*?)\] (.*)", CLAIMS[cid]["assertion"], re.S)
    return m.group(1), m.group(2)


def assertion(cid: str) -> str:
    return niveau_et_texte(cid)[1]


def verifie(cid: str) -> str:
    return CLAIMS[cid]["valeur_verifiee"]


def ligne_constat(ident: str, debut: str) -> str:
    """Première ligne d'un constat d'audit (A-08, C-10...) qui commence par `debut`, sans le préfixe."""
    txt = _AUDITS[ident[0]].read_text()
    bloc = txt[txt.index(f"### {ident},"):]
    bloc = bloc[:bloc.find("\n### ", 5)]
    for li in bloc.splitlines():
        li = li.strip().lstrip("- ")
        if li.startswith(debut):
            return li[len(debut):].strip()
    raise KeyError((ident, debut))


def rendu(txt: str, **verbatim: str) -> str:
    out = fr(txt)
    for k, v in verbatim.items():
        out = out.replace(f"@@{k}@@", v)
    if "@@" in out:
        raise ValueError("texte d'audit non injecté : " + out[out.index("@@"):out.index("@@") + 30])
    return out
