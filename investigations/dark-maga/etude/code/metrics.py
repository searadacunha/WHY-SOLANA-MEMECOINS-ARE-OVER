"""Mesures M1 à M7 du plan, sur un token. Fonctions pures, aucune entrée réseau ni disque.

Une mesure indéfinie (aucun achat, moins de 2 acheteurs, aucun précoce) vaut NaN, jamais 0.

Entrée : colonnes numpy triées par (slot, tx_index) : t, slot, owner (entiers), qty (signé), sol (lamports
signés côté trader : négatif à l'achat), vault_pre (réserve SOL juste avant le swap).
"""
import numpy as np

H = 3600
FLOOR_LAMPORTS = 100_000_000  # 0,1 SOL
SLOTS_24H = 216_000  # 24 h à 0,4 s par slot


def spike_hour(hist: dict[int, int], created: int, mult: float = 20.0, min_tx: int = 500) -> int | None:
    """Première heure h >= création + 96 h et < création + 60 j où n(h) >= mult × médiane(72 h d'avant)."""
    if not hist:
        return None
    first = (created + 96 * H) // H + (1 if (created + 96 * H) % H else 0)
    last = (created + 60 * 86400) // H
    for h in range(first, last):
        n = hist.get(h, 0)
        if n < min_tx:
            continue
        med = float(np.median([hist.get(x, 0) for x in range(h - 72, h)]))
        if n >= mult * max(med, 5.0):
            return h * H
    return None


def _windows_median(t, buy, start, end, width):
    edges = np.arange(end - width, start - 1, -width)  # fenêtres alignées sur la fin, sans chevauchement
    vals = [buy[(t >= e) & (t < e + width)].sum() for e in edges if e >= start]
    return float(np.median(vals)) if vals else 0.0


def compute(t, slot, owner, qty, sol, vault_pre, S: int, created: int) -> dict:
    before = t < S
    t, slot, owner, qty, sol, vault_pre = t[before], slot[before], owner[before], qty[before], sol[before], vault_pre[before]
    is_buy = (qty > 0) & (sol < 0)
    buy = np.where(is_buy, -sol, 0).astype(np.float64)

    w3 = t >= S - 3 * H
    m1 = buy[w3].sum() / max(_windows_median(t, buy, S - 75 * H, S - 3 * H, 3 * H), FLOOR_LAMPORTS)
    w24 = t >= S - 24 * H
    total24 = buy[w24].sum()
    m2 = total24 / max(_windows_median(t, buy, S - 96 * H, S - 24 * H, 24 * H), FLOOR_LAMPORTS)

    # premier swap de chaque wallet, tous types
    first_t: dict[int, int] = {}
    for o, x in zip(owner.tolist(), t.tolist()):
        first_t.setdefault(o, x)
    idx = np.nonzero(w24 & is_buy)[0]
    by_owner: dict[int, float] = {}
    first_slot: dict[int, int] = {}
    new_sol = 0.0
    for i in idx.tolist():
        o = int(owner[i])
        by_owner[o] = by_owner.get(o, 0.0) + float(buy[i])
        first_slot.setdefault(o, int(slot[i]))
        if first_t[o] >= S - 24 * H:
            new_sol += float(buy[i])
    m3 = new_sol / total24 if total24 > 0 else float("nan")
    m4 = sum(sorted(by_owner.values(), reverse=True)[:5]) / total24 if total24 > 0 else float("nan")

    n_buyers = len(first_slot)
    counts: dict[int, int] = {}
    for s in first_slot.values():
        counts[s] = counts.get(s, 0) + 1
    observed = sum(c * (c - 1) / 2 for c in counts.values())
    expected = n_buyers * (n_buyers - 1) / 2 / SLOTS_24H
    m5 = observed / expected if n_buyers >= 2 else float("nan")

    # détention à S des wallets entrés dans les 24 h suivant la création
    early = set(owner[(t < created + 24 * H) & is_buy].tolist())
    net: dict[int, int] = {}
    bought: dict[int, int] = {}
    for o, q in zip(owner.tolist(), qty.tolist()):
        if o in early:
            net[o] = net.get(o, 0) + q
            if q > 0:
                bought[o] = bought.get(o, 0) + q
    tot = sum(bought.values())
    m6 = sum(max(0, min(net[o], bought[o])) for o in bought) / tot if tot else float("nan")

    m7 = float("nan")
    if len(idx):
        i = int(buy[idx].argmax())  # le plus gros achat rapporté à SA réserve, pas le plus grand ratio
        m7 = float(buy[idx][i] / max(float(vault_pre[idx][i]), 1.0))
    return {"M1": float(m1), "M2": float(m2), "M3": float(m3), "M4": float(m4), "M5": float(m5), "M6": float(m6),
            "M7": m7, "n_swaps_before": int(len(t)), "n_swaps_96h": int((t >= S - 96 * H).sum()), "n_buyers_24h": n_buyers}


METRICS = ("M1", "M2", "M3", "M4", "M5", "M6", "M7")


def rank_p(target: float, controls: list[float]) -> float:
    """p unilatéral de rang, DMAGA plus élevé que ses pairs. Les indéfinis sont hors du calcul, jamais à 0."""
    if target != target:
        raise ValueError("mesure indéfinie sur la cible")
    vals = [c for c in controls if c == c]
    return (1 + sum(1 for c in vals if c >= target)) / (len(vals) + 1)


def holm(ps: dict[str, float], alpha: float = 0.05) -> dict[str, bool]:
    order = sorted(ps, key=ps.get)
    out = {}
    still = True
    for i, k in enumerate(order):
        still = still and ps[k] <= alpha / (len(order) - i)
        out[k] = still
    return out


def verdict(ps: dict[str, float], k: int) -> str:
    if k < 139:
        return f"INCONCLUSIF (puissance) : {k} comparateurs, il en faut 139 pour qu'un test puisse passer Holm"
    h = holm(ps)
    hits = [m for m in METRICS if h.get(m)]
    if not hits:
        return "DMAGA NON DISTINGUABLE DE SES PAIRS"
    return (f"DMAGA INHABITUEL SUR {', '.join(hits)}. Ceci décrit un écart à la distribution des pics tardifs ; "
            "ce n'est pas une preuve de connaissance préalable ni d'une action illégale.")
