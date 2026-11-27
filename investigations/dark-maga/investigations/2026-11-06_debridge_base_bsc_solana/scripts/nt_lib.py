"""Bibliothèque commune du dossier. Aucun chemin propre à une machine : tout part de l'emplacement de ce fichier.

- Réutilise `ev_lib`, `sol_lib` et `dln` du dossier précédent, publié dans le même dépôt
  (`investigations/2026-11-05_evm-recipient-deeptrace/scripts/`), sans y écrire.
- Cache brut : `raw/` de ce dossier (ignoré par git), ou `$DMAGA_NT_RAW`. Tout nouvel appel réseau y est écrit.
- Caches existants en lecture seule : `$DMAGA_NT_RAW_RO`, liste de dossiers séparés par `os.pathsep`
  (par exemple le `raw/` d'une collecte antérieure). Chaque dossier peut contenir `cache/<2 hex>/<clé>.json`
  ou directement `<2 hex>/<clé>.json`, ainsi que `browser_dump/` et `sol_hist/`.
- Les fixtures publiées (`evidence/fixtures/cache/`) sont lues en premier : les tests hors ligne n'ont besoin de rien d'autre.
"""
import os, sys, csv, json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
REPO = ROOT.parents[1]
PREV = REPO / "investigations" / "2026-11-05_evm-recipient-deeptrace"
OLD_INV = PREV  # nom gardé pour les scripts de collecte
FIXTURES = ROOT / "evidence" / "fixtures" / "cache"
RAW = Path(os.environ.get("DMAGA_NT_RAW", ROOT / "raw"))
RAW_RO = [Path(p) for p in os.environ.get("DMAGA_NT_RAW_RO", "").split(os.pathsep) if p]
NEW_RAW = RAW / "cache"
# extraits publiés des réponses de l'API deBridge (projet deBridge, collectes s01 et s11), limités aux ordres utilisés ici
DEB_RECEIVERS = ROOT / "evidence" / "debridge_api_receivers_extract.csv"
DEB_ORDERS = ROOT / "evidence" / "debridge_api_orders_extract.csv"

sys.path.insert(0, str(PREV / "scripts"))
import ev_lib as E  # noqa: E402

E.RAW = NEW_RAW  # ev_lib lit ces globales à chaque appel : les nouveaux appels vont dans ce dossier, jamais dans PREV
E.LEDGER = NEW_RAW / "ledger.jsonl"
_write_path = E._cache


def _cache(key):
    """Fixture publiée, puis cache local, puis caches en lecture seule ; sinon chemin d'écriture local."""
    for base in [FIXTURES, NEW_RAW] + [d for r in RAW_RO for d in (r / "cache", r)]:
        p = base / key[:2] / (key + ".json")
        if p.exists():
            return p
    return _write_path(key)


E._cache = _cache


def raw_dir(name):
    """Premier dossier `name` (browser_dump, sol_hist) existant parmi le raw local et les raw en lecture seule."""
    for r in [RAW] + RAW_RO:
        if (r / name).is_dir():
            return r / name
    return RAW / name


DUMP = raw_dir("browser_dump")

B298 = "0xb29826d809aa04d2ead6f2310d8965a45b87fa67"
B947 = "0xb947bf7f409e998b28f8e218802fc9575c3c8c57"
RELAY = "0x4978cd7e5a3565cafcc88a105940b0ea01adc04d"
EI5 = "Ei5yGz8dPndr1aCeHZsfqJBcS3VBbz75VHEhxxJKLy3V"
MEXC_DEP = "0x311ef6b5953ae605dbe469e6566280f0514d3d2e"
DLN_DST = "0xe7351fd770a37282b91d153ee690b63579d6dd7f"
DLN_SRC = "0xef4fb24ad0916217251f553c0596f8edc630eb66"


def dump_pages(chain, addr, kind):
    """Pages Blockscout brutes déposées par l'onglet local ; exige le marqueur _DONE (pagination complète)."""
    pre = f"{chain}_{addr.lower() if addr.startswith('0x') else addr}_{kind}"
    files = sorted(DUMP.glob(pre + "_p*.json"))
    done = (DUMP / (pre + "_DONE.json")).exists()
    items = []
    for f in files:
        items += json.loads(f.read_bytes())["response"].get("items") or []
    return items, done, len(files)


def write_csv(path, rows, fields=None):
    path = Path(path); path.parent.mkdir(parents=True, exist_ok=True)
    fields = fields or (list(rows[0].keys()) if rows else [])
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore"); w.writeheader(); w.writerows(rows)
    return path
