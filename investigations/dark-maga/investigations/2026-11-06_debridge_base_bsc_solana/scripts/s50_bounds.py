"""Bornes prudentes, sans FIFO, de la part « marquée » de chaque sortie d'un wallet EVM, par actif (ETH natif ou USDC).
Deux scénarios bornants, en entiers bruts :
- scénario bas (marqué consommé d'abord, entrée marquée comptée à sa part minimale, produits de ventes = non marqués) -> C_max ;
- scénario haut (non marqué consommé d'abord, entrée marquée comptée en entier, produits de ventes = potentiellement marqués) -> T_max.
Pour une sortie x : borne basse = max(0, x - C_max), borne haute = min(x, T_max). Autotest en fin de fichier."""

def bounds(events):
    """events : liste ordonnée de dict(kind='in'|'out', x=int, taint_min=int (in), taint_max=int (in), proceeds=bool (in)).
    Rend la liste des sorties enrichies de lo, hi."""
    lowT = lowC = hiT = hiC = 0
    out = []
    for e in events:
        x = e["x"]
        if e["kind"] == "in":
            if e.get("proceeds"):
                lowC += x; hiT += x
            else:
                lowT += e.get("taint_min", 0); lowC += x - e.get("taint_min", 0)
                hiT += e.get("taint_max", 0); hiC += x - e.get("taint_max", 0)
            continue
        lo = max(0, x - max(0, lowC)); hi = min(x, max(0, hiT))
        out.append(dict(e, lo=lo, hi=hi))
        a = min(x, max(0, lowT)); lowT -= a; lowC -= x - a          # bas : marqué d'abord
        b = min(x, max(0, hiC)); hiC -= b; hiT -= x - b             # haut : propre d'abord
    return out

def _selftest():
    ev = [dict(kind="in", x=100, taint_min=0, taint_max=0), dict(kind="in", x=1000, taint_min=990, taint_max=1000),
          dict(kind="out", x=500), dict(kind="out", x=550), dict(kind="in", x=40, proceeds=True), dict(kind="out", x=80)]
    o = bounds(ev)
    assert (o[0]["lo"], o[0]["hi"]) == (390, 500), o[0]   # au mieux 110 propres disponibles
    assert (o[1]["lo"], o[1]["hi"]) == (440, 550), o[1]
    assert all(r["lo"] <= r["hi"] <= r["x"] for r in o)
    assert (o[2]["lo"], o[2]["hi"]) == (0, 80), o[2]       # produits de ventes : jamais marqués en bas, toujours possibles en haut
_selftest()
