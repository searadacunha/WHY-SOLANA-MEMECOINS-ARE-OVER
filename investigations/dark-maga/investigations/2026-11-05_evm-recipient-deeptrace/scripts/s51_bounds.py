"""Bornes prudentes de la part « venue de b947 » dans chaque sortie USDC de b298, sans FIFO ni hypothèse sur le relais.
Marqué : l'USDC que b947 envoie à partir du 01/10/2024 (son vidage du 01/10), directement ou par le relais 0x4978cd7e. b947 n'a jamais
détenu de DMAGA : son stock d'USDC vient de cinq exécutions deBridge de makers DMAGA (384 277,99), de b298 (50 003,33) et d'un sosie (10).
Tout le reste est non marqué. Deux réservoirs par wallet, T (marqué) et C (non marqué) ; l'USDC est fongible. Pour chaque sortie x :
- T_max = T restant si toutes les sorties passées avaient puisé d'abord dans C ; C_max = C restant si elles avaient puisé d'abord dans T ;
- borne basse = max(0, x - C_max) ; borne haute = min(x, T_max).

Le relais n'est pas un conduit pur : b298 lui renvoie 100 000 USDC le 06/10/2024 (0x6407f6bc) et la règle donne 0 comme borne basse
de la part marquée de ce renvoi. Le relais est donc tracé avec la même règle : entrées de b947 marquées, entrée de b298 marquée entre 0
et son montant ; chaque envoi du relais entre dans b298 entre sa borne basse et sa borne haute. Prendre 0 pour le renvoi est toujours
valable ; ici c'est aussi sa borne basse exacte (assertion). Correction du 06/11/2026 : la version initiale comptait le relais comme
100 % b947 (ordre o1 du 12/11 : 100 046,83 au lieu de 46,81 ; ordre o2 : 99 981,82 au lieu de 0). Les 31 bornes basses et hautes ont été
recoupées contre un programme linéaire exact à deux réservoirs (toute allocation qui conserve la valeur).

Borne commune d'un ensemble S de sorties de b298 (joint_min) : pour tout point k avant S, l'USDC non marqué que S peut emporter est au plus
le solde de b298 après k, plus ses entrées non marquées hors relais jusqu'à la dernière sortie de S, plus ce que le relais peut lui rendre
de non marqué, soit au plus les entrées du relais hors b947. Donc marqué(S) >= somme(S) - ce total, pour toute allocation ; on garde le
meilleur k. Variante makers : seul l'USDC des exécutions deBridge reçues par b947 est marqué ; b947 rejoint alors le relais comme source
possible de non marqué (b298 et le sosie lui ont versé 50 013,33 USDC avant son vidage).
Sortie : ../evidence/s51_b298_usdc_bounds.csv"""
import csv
B947, RELAY, B298 = "0xb947bf7f409e998b28f8e218802fc9575c3c8c57", "0x4978cd7e5a3565cafcc88a105940b0ea01adc04d", "0xb29826d809aa04d2ead6f2310d8965a45b87fa67"
USDC = "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48"
RET = "0x6407f6bccc370f06128fd95981f5c13475fc3be04922d6213d84d05c97944d8c"  # renvoi b298 -> relais, 06/10/2024 19:28:35
O1 = "0x4b7c7a2fcda576c58c961dee9d35840fba0151a9156cc0c48a0282c2fb024e16"  # 12/11/2024, deBridge vers b298 sur Base
O2 = "0xca82377984453a77f40592a694c5ad4c8076acce66b64a25e7c43f119f3cf8a4"  # 12/11/2024, deBridge vers b298 sur BSC
T0 = "2024-10-01"
key = lambda r: (r["timestamp_utc"], int(r["log_index"]))
ref = lambda r: (r["tx_hash"].lower(), r["log_index"])
U = lambda v: round(v / 1e6, 6)

def load(ev="../evidence", root=".."):
    # entrées de vrai USDC venues d'un sosie (poussière d'empoisonnement) : vraie valeur, gardées pour le solde
    R = [r for r in csv.DictReader(open(f"{ev}/b298_full_history.csv")) if r["asset"] == "USDC"
         and (not r["flags"] or (r["flags"] == "lookalike" and r["direction"] == "IN"))]
    RL = [r for r in csv.DictReader(open(f"{ev}/relay_4978_history.csv")) if r["kind"] == "erc20"
          and r["token_contract"].lower() == USDC and int(r["amount_raw"]) > 0]
    W = [r for r in csv.DictReader(open(f"{root}/b947_full_history.csv")) if r["kind"] == "erc20"
         and r["token_contract"].lower() == USDC and int(r["amount_raw"]) > 0 and "unsigned_out" not in r["flags"]]
    for L in (R, RL, W): L.sort(key=key)
    return R, RL, W

def scen(R, t_lo, t_hi):
    """{(tx, log_index) d'une sortie: (borne basse, borne haute, T si propre d'abord, T si marqué d'abord)}, unités brutes.
    t_lo(r), t_hi(r) : part marquée minimale et maximale d'une entrée."""
    lo_s, hi_s, res = [0, 0], [0, 0], {}  # [T, C] : lo_s puise d'abord dans T (garde C), hi_s d'abord dans C (garde T)
    for r in R:
        x = int(r["amount_raw"])
        if r["direction"] == "IN":
            a, b = t_lo(r), t_hi(r); lo_s[0] += a; lo_s[1] += x - a; hi_s[0] += b; hi_s[1] += x - b
            continue
        lo, hi = max(0, x - max(0, lo_s[1])), min(x, max(0, hi_s[0]))
        for s, first in ((lo_s, 0), (hi_s, 1)):
            take = min(x, max(0, s[first])); s[first] -= take; s[1 - first] -= x - take
        res[ref(r)] = (lo, hi, hi_s[0], lo_s[0])
    return res

def bounds(R, RL):
    """Bornes de b298 avec le relais tracé, et bornes des envois du relais."""
    mark947 = lambda r: int(r["amount_raw"]) if r["counterparty"] == B947 and r["timestamp_utc"] >= T0 else 0
    rel = scen(RL, mark947, lambda r: int(r["amount_raw"]) if r["counterparty"] in (B947, B298) else 0)
    via = lambda i: (lambda r: rel[ref(r)][i] if r["counterparty"] == RELAY else mark947(r))
    b = scen(R, via(0), via(1))
    assert b[next(k for k in b if k[0] == RET)][0] == 0, "le renvoi au relais a une borne basse > 0 : itérer jusqu'au point fixe"
    return b, rel

def joint_min(R, S, U_extra, extra_from=()):
    """Borne commune sans hypothèse de marqué(S), S = ensemble de tx de sorties de b298. U_extra : non-marqué maximal que les wallets
    de extra_from (plus le relais) peuvent apporter à b298. Rend (borne en unités brutes, horodatage du meilleur point k)."""
    feeders = {RELAY, *extra_from}
    idx = [i for i, r in enumerate(R) if r["direction"] == "OUT" and r["tx_hash"].lower() in S]
    assert len(idx) == len(S), "sortie absente de l'historique"
    tot = sum(int(R[i]["amount_raw"]) for i in idx); best, at, bal = 0, None, 0
    for k in range(-1, idx[0]):  # k = -1 : avant le premier événement
        if k >= 0: bal += int(R[k]["amount_raw"]) * (1 if R[k]["direction"] == "IN" else -1)
        win = [r for r in R[k + 1: idx[-1] + 1] if r["direction"] == "IN"]
        free = sum(int(r["amount_raw"]) for r in win if r["counterparty"] not in feeders and not (r["counterparty"] == B947 and r["timestamp_utc"] >= T0))
        fed = sum(int(r["amount_raw"]) for r in win if r["counterparty"] in feeders)
        v = tot - bal - free - min(U_extra, fed)
        if v > best: best, at = v, (R[k]["timestamp_utc"] if k >= 0 else "début")
    return best, at

def unmarked_in(L, src_ok, before=None):
    """Somme des entrées non marquées d'un wallet (src_ok(r) vrai si l'entrée est marquée), arrivées après son dernier solde nul
    antérieur à T0 et au plus tard à `before` : ce qui a été dépensé avant ce solde nul ne peut plus sortir."""
    bal, start = 0, 0
    for i, r in enumerate(L):
        if r["timestamp_utc"] >= T0: break
        bal += int(r["amount_raw"]) * (1 if r["direction"] == "IN" else -1)
        if bal == 0: start = i + 1
    return sum(int(r["amount_raw"]) for r in L[start:] if r["direction"] == "IN" and not src_ok(r) and (before is None or r["timestamp_utc"] <= before))

def joint_bounds(R, RL, W, b947_fills):
    """Borne commune de o1 + o2 : (marqué = venu de b947, marqué = exécutions deBridge reçues par b947), avec leurs non-marqués maximaux."""
    u_rel = unmarked_in(RL, lambda r: r["counterparty"] == B947)  # entrées du relais hors b947, renvoi de b298 compris en entier
    u_947 = unmarked_in(W, lambda r: r["tx_hash"].lower() in b947_fills, before=max(r["timestamp_utc"] for r in W if r["direction"] == "OUT"))
    j, at = joint_min(R, {O1, O2}, u_rel)
    jm, atm = joint_min(R, {O1, O2}, u_rel + u_947, extra_from=(B947,))
    return dict(joint=j, at=at, u_relay=u_rel, joint_makers=jm, at_makers=atm, u_b947=u_947)

if __name__ == "__main__":
    R, RL, W = load()
    b, rel = bounds(R, RL)
    D = {r["tx"].lower(): r for r in csv.DictReader(open("../evidence/dln_orders_evm.csv"))}
    out = []
    for r in R:
        if r["direction"] != "OUT": continue
        lo, hi, t_hi, t_lo = b[ref(r)]
        if r["timestamp_utc"] >= T0 and (hi > 0 or lo > 0):
            d = D.get(r["tx_hash"].lower())
            out.append(dict(utc=r["timestamp_utc"], tx_hash=r["tx_hash"], amount=U(int(r["amount_raw"])), counterparty=r["counterparty"], category=r["category"],
                            label=(r["inferred_label"] or r["label"])[:60], dln_dest=(f"{d['take_chain']}:{d['receiver']}" if d else ""),
                            from_b947_min=U(lo), from_b947_max=U(hi), T_left_if_clean_first=U(t_hi), T_left_if_taint_first=U(t_lo)))
    with open("../evidence/s51_b298_usdc_bounds.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(out[0])); w.writeheader(); w.writerows(out)
    agg = {}
    for o in out:
        k = o["dln_dest"] or (o["label"] or o["category"]) + " " + o["counterparty"][:10]
        a = agg.setdefault(k, [0, 0, 0]); a[0] += o["from_b947_min"]; a[1] += o["from_b947_max"]; a[2] += 1
    for k, v in sorted(agg.items(), key=lambda kv: -kv[1][1]):
        print(f"{k[:75]:75s} n={v[2]:3d} min={v[0]:12,.2f} max={v[1]:12,.2f}")
    print("T restant à la dernière ligne (propre d'abord, marqué d'abord) :", out[-1]["T_left_if_clean_first"], out[-1]["T_left_if_taint_first"])
    assert all(o["from_b947_min"] <= o["from_b947_max"] for o in out), "borne basse > borne haute"
    # borne commune des deux ordres du 12/11/2024
    J = joint_bounds(R, RL, W, {r["tx"].lower() for r in D.values() if r["wallet"] == "b947" and r["direction"] == "IN"})
    print(f"o1 seul >= {U(b[next(k for k in b if k[0] == O1)][0]):,.6f} ; o2 seul >= {U(b[next(k for k in b if k[0] == O2)][0]):,.6f}")
    print(f"o1 + o2 >= {U(J['joint']):,.6f} USDC venus de b947 (point k = {J['at']}) ; non-marqué maximal du relais {U(J['u_relay']):,.6f}")
    print(f"o1 + o2 >= {U(J['joint_makers']):,.6f} USDC des exécutions deBridge reçues par b947 (point k = {J['at_makers']}) ; "
          f"non-marqué de b947 {U(J['u_b947']):,.6f}")
