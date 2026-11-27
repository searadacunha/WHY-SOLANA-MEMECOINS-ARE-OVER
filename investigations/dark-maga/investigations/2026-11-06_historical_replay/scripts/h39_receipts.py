"""Fige les transactions citées dans FINDINGS.md (evidence/receipts/<signature>.json) pour les tests hors ligne.

Sources des signatures : data/receipts_jeffro.json (h31), arêtes DMAGA directes et premières arêtes SOL de chaque couple
dans data/noah_edges.csv (h32), paiements de data/counterparty_HBsgbpsM….csv (h33), et la liste EXTRA ci-dessous.
Toutes sont relues par le RPC public (cache k16) : un reçu introuvable arrête le script."""
import csv
import json
import re
from h_lib import DATA, EVID
import k16_pubrpc as pub

EXTRA = {
    "2LXvSeMHzJAV": "AtZj : virement Transfer simple de 6t2dz4jm, absent de trades.parquet",
    "58SeigZv41h2": "AtZj : virement Transfer simple de 6t2dz4jm (13,19 M), absent de trades.parquet",
    "dLnMuAksDjjA": "AtZj : 41 M vers NxtXcmEW (TransferChecked, présent dans trades.parquet)",
    "5kGaZNhDcm7PaPFAeYhD": "KLLARY : création Pump.fun, CreateEvent décodé",
    "3P6igyNv1eWd8Yva": "KLLARY : premier achat de 7GVC",
    "3K2CSyaHDL9yS4nX": "KLLARY : premier achat de 9Sxm",
    "yACQEPggkJM2opaw": "KLLARY : 23 M de 7GVC vers 7rSZBE2S",
    "4nPPf19oG7oX1PhUGmkJ": "H3Qs : vente de JOE (h53)",
    "5zc5i9VWYwzU1hgWUUti": "H3Qs : achat de DMAGA 23 s après (h53)",
    "29NFuxQwFq": "GXZvX : avant-dernière vente (23/07 11:47:09)",
    "2WJ1MmWWsr": "GXZvX : vente 23/07 11:47:37",
    "521vdgUCSk": "GXZvX : dernière vente 23/07 11:48:23",
    "4UiQXVF3UAkRVbmw": "6QFD : première transaction, payée par 9Sxm",
    "4pcw28aApDZVvvJR": "AeiMit : première transaction, payée par 7GVC",
    "ur6ajcoGpH": "H4mQ renvoie 76,68 SOL à 9Sxm",
    "RM8AZbLuWLkc": "6QFD renvoie 4,62 SOL à 7GVC",
    "2PHU4HTSGRJ6xKncBiVm": "Passe 3 L02 : 9Sxm vend 1,8 M DMAGA, 17,874608396 SOL brut",
    "veJgufrqRRfWvo6fXNeG": "Passe 3 L03 : création de BARRON",
    "2a9YNG2S1sud1aCe1KsB": "Passe 3 L03 : premier financement du créateur de BARRON",
    "3wFx6C1HXs1PuKcMQVsj": "Passe 3 L03 : seule transaction commune aux deux créateurs (swap d'un tiers)",
}


def known_signatures():
    """Toutes les signatures complètes connues localement (listes h10, tables CSV) pour résoudre les préfixes d'EXTRA."""
    from h_lib import EXT
    out = set()
    for p in EXT.glob("sigs_*.json"):
        out |= {x["signature"] for x in json.loads(p.read_text())["sigs"]}
    for p in DATA.glob("*.json"):  # signatures citées dans les sorties JSON (h35, h50)
        out |= set(re.findall(r"\b[1-9A-HJ-NP-Za-km-z]{86,88}\b", p.read_text()))
    for p in DATA.glob("*.csv"):
        for r in csv.DictReader(p.open()):
            for k, v in r.items():
                if k and "signature" in k and v:
                    out |= set(v.split(";"))
    return out


def resolve_prefixes(extra):
    import duckdb
    from h_lib import DMAGA_BIG
    full = known_signatures()
    out = {}
    B = str(DMAGA_BIG).replace("/data", "/data_v2")
    for pre, why in extra.items():
        hit = sorted(s for s in full if s.startswith(pre))
        if not hit:
            hit = sorted({r[0] for r in duckdb.sql(f"select signature from '{B}/trades.parquet' where signature like '{pre}%' union "
                                                   f"select signature from '{B}/token_edges.parquet' where signature like '{pre}%'").fetchall()})
        assert len(hit) == 1, (pre, hit)  # un préfixe ambigu ou absent arrête : pas de signature devinée
        out[hit[0]] = why
    return out


if __name__ == "__main__":
    sigs = json.loads((DATA / "receipts_jeffro.json").read_text())
    for r in csv.DictReader((DATA / "noah_edges.csv").open()):
        if r["asset"] == "DMAGA" and r["source_table"] in ("tx_balances", "token_direct"):
            sigs.setdefault(r["signature"], f"Noah : virement DMAGA {r['src'][:6]} → {r['dst'][:6]}")
    first = {}
    for r in csv.DictReader((DATA / "noah_edges.csv").open()):
        if r["asset"] == "SOL":
            first.setdefault((r["src"], r["dst"]), r["signature"])
    for (s, d), sig in first.items():
        sigs.setdefault(sig, f"Noah : premier virement SOL {s[:6]} → {d[:6]}")
    for r in csv.DictReader((DATA / "counterparty_HBsgbpsM1j1YsNYqtCXcFU4mCRofwcor2qFwifNqddmH.csv").open()):
        if r["dir"] == "in" and int(r["amount_raw"]) >= 3 * 10**8:
            sigs.setdefault(r["signature"], f"HBsgbpsM : paiement de {r['counterparty'][:6]}")
    sigs.update(resolve_prefixes(EXTRA))
    d = EVID / "receipts"
    d.mkdir(parents=True, exist_ok=True)
    for s in sigs:
        t = pub.tx(s)
        (d / f"{s}.json").write_text(json.dumps(t, separators=(",", ":")))
    (d / "INDEX.json").write_text(json.dumps(dict(sorted(sigs.items())), ensure_ascii=False, indent=1))
    print(len(sigs), "reçus")
