"""Bornes de provenance par actif, à travers les échanges, pour un wallet EVM (b298 sur Base). Aucun appel réseau.

Question : quelle part minimale (et maximale) de chaque sortie de b298 descend de l'USDC de b947, quand l'argent marqué
passe par des mèmes (HIGHER, BOOMER, SYNDOG, RUNNER, CJ...) avant de repartir ?

Modèle, en entiers bruts, par actif a (ETH natif, USDC, chaque jeton) : solde B_a (grand livre complet), T_lo,a et T_hi,a.
- Sortie x de a :
  borne basse de la part marquée de x = max(0, x - (B_a - T_lo,a)) : tout le non-marqué possible part d'abord dans x ;
  borne haute = min(x, T_hi,a) ;
  puis T_lo,a -= min(x, T_lo,a) (marqué d'abord) et T_hi,a = min(T_hi,a, B_a - x) (non marqué d'abord).
- Échange atomique d'une seule entrée a (x) contre une seule sortie b (y) : b reçoit y * lo / x en borne basse,
  y * hi / x en borne haute (un seul prix dans la tx : la part de valeur marquée de l'entrée passe à la sortie).
  Plusieurs entrées ou plusieurs sorties : borne basse 0 pour chaque sortie, borne haute y (sans prix, rien de plus sûr).
- Exécution deBridge reçue d'un ordre Ethereum de b298 : part de b947 de cet ordre (bornes s51 du dossier précédent).
- Autre entrée : borne basse 0 ; borne haute y à partir de la première exécution marquée, 0 avant (hypothèse H : l'argent
  de b947 n'arrive pas sur Base avant cette exécution).

Validité de la borne basse, pour toute règle d'allocation qui conserve la valeur dans un échange : par récurrence, sur chaque
actif, le marqué réel T_P >= T_lo. Sortie x : la règle P sort a_P <= min(x, T_P) de marqué, donc T_P - a_P >= max(0, T_P - x)
>= max(0, T_lo - x). Le marqué sorti a_P >= x - (B - T_P) >= x - (B - T_lo). Échange : la sortie reçoit au moins y * a_P / x
>= y * lo / x. La borne basse n'est pas atteinte par une même allocation à chaque étape : elle est prudente, pas exacte.
Si un solde reconstitué devient négatif (jeton à frais ou rebasage), l'actif est marqué « rompu » et remis à 0 (prudent)."""
import csv, sys, os, collections, json
from decimal import Decimal
sys.path.insert(0, os.path.dirname(__file__))
import nt_lib as N

R = N.ROOT
ETH = "ETH"
USDC_BASE = "0x833589fcd6edb6e08f4c7c32d4f71b54bda02913"

def rd(p): return list(csv.DictReader(open(p)))

def raw6(s): return int((Decimal(s) * 10 ** 6).to_integral_value())

def fill_taint(relay_traced=False):
    """tx d'exécution Base -> (min_num, max_num, den, tx Ethereum) : part de b947 de l'ordre Ethereum payé par b298.
    relay_traced : bornes basses de s15 (relais tracé, pire cas propre à chaque ordre) au lieu de celles de s51 (relais = b947)."""
    s51 = {r["tx_hash"].lower(): r for r in rd(N.PREV / "evidence/s51_b298_usdc_bounds.csv")}
    if relay_traced:
        for r in rd(R / "evidence/s15_s51_corrected.csv"): s51[r["tx_hash"].lower()]["from_b947_min"] = r["from_b947_min_relay_traced"]
    eth = {r["orderId"].lower(): r for r in rd(N.PREV / "evidence/dln_orders_evm.csv")}
    out = {}
    for d in rd(R / "evidence/s12_dln_base.csv"):
        if d["event"] != "FulfilledOrder" or d["giveChain"] != "ethereum" or d["receiverDst"].lower() != N.B298: continue
        eo = eth.get(d["orderId"].lower()); b = s51.get(eo["tx"].lower()) if eo else None
        if b: out[d["tx"]] = (raw6(b["from_b947_min"]), raw6(b["from_b947_max"]), raw6(b["amount"]), eo["tx"])
    return out

def per_tx(ledger, a):
    """Variation nette par tx et par actif (entiers), frais à part. Ordre : bloc, puis ordre du grand livre."""
    txs = collections.OrderedDict()
    for r in ledger:
        t = txs.setdefault(r["tx"], dict(tx=r["tx"], ts=r["ts"], block=int(r["block"]), net=collections.Counter(), fee=0, cps=set(), sym={}))
        d = 1 if r["dir"] == "in" else (-1 if r["dir"] == "out" else 0)
        if r["kind"] == "tx":
            if r["frm"] == a: t["fee"] += int(r["fee"] or 0)
            if r["status"] == "ok": t["net"][ETH] += d * int(r["raw"] or 0)
        elif r["kind"] == "internal":
            if r["status"] == "ok": t["net"][ETH] += d * int(r["raw"] or 0)
        elif r["kind"] == "token" and r["raw"] != "":
            t["net"][r["token"]] += d * int(r["raw"]); t["sym"][r["token"]] = r["asset"]
        cp = r["to"] if r["dir"] == "out" else r["frm"]
        if cp and cp != a: t["cps"].add(cp)
    return sorted(txs.values(), key=lambda t: t["block"])

class Book:
    def __init__(self): self.s = collections.defaultdict(lambda: [0, 0, 0]); self.broken = {}
    def out(self, a, x, tx):
        B, lo_t, hi_t = self.s[a]
        if x > B:  # grand livre incohérent pour cet actif : on remet tout à 0 (prudent pour la borne basse)
            self.broken.setdefault(a, tx); self.s[a] = [0, 0, 0]; return 0, x
        lo = max(0, x - (B - lo_t)); hi = min(x, hi_t)
        self.s[a] = [B - x, max(0, lo_t - x), min(hi_t, B - x)]
        return lo, hi
    def inn(self, a, y, clo, chi):
        assert 0 <= clo <= chi <= y, (a, y, clo, chi)
        B, lo_t, hi_t = self.s[a]; self.s[a] = [B + y, lo_t + clo, hi_t + chi]

def run(txs, taint, t_first):
    bk = Book(); rows = []
    for t in txs:
        net = {k: v for k, v in t["net"].items() if v}
        outs = {k: -v for k, v in net.items() if v < 0}; ins = {k: v for k, v in net.items() if v > 0}
        res = {}
        if t["fee"]: bk.out(ETH, t["fee"], t["tx"])          # frais : sortie d'ETH ordinaire
        for k, x in outs.items(): res[k] = (x,) + bk.out(k, x, t["tx"])
        hyp = t["ts"] >= t_first
        for k, y in ins.items():
            if t["tx"] in taint and not outs:  # exécution deBridge : l'actif reçu (ETH ou USDC) porte la part de l'ordre source
                mn, mx, den, _ = taint[t["tx"]]; clo, chi = y * mn // den, min(y, -(-y * mx // den))
            elif len(outs) == 1 and len(ins) == 1:
                x, lo, hi = next(iter(res.values())); clo, chi = y * lo // x, min(y, -(-y * hi // x))
            elif outs:
                clo, chi = 0, y
            else:
                clo, chi = 0, (y if hyp else 0)
            bk.inn(k, y, clo, chi); res.setdefault(k, (0, 0, 0)); res[k] = res[k] + (y, clo, chi)
        rows.append(dict(t, res=res))
    return rows, bk

def _selftest():
    # 100 propres, puis 1000 dont 990 marqués ; échange de 500 ETH contre 50 X ; vente de 50 X contre 600 ETH ; sortie de 650.
    T = lambda tx, ts, net, fee=0: dict(tx=tx, ts=ts, block=int(tx[1:]), net=collections.Counter(net), fee=fee, cps=set(), sym={})
    txs = [T("t1", "a", {ETH: 100}), T("t2", "b", {ETH: 1000}), T("t3", "c", {ETH: -500, "X": 50}), T("t4", "d", {"X": -50, ETH: 600}), T("t5", "e", {ETH: -650})]
    rows, bk = run(txs, {"t2": (990, 1000, 1000, "")}, "b")
    r = {x["tx"]: x["res"] for x in rows}
    assert r["t3"][ETH] == (500, 390, 500), r["t3"]                    # au plus 110 propres disponibles
    assert r["t3"]["X"] == (0, 0, 0, 50, 39, 50), r["t3"]              # 50 X, au moins 39 marqués
    assert r["t4"]["X"][:3] == (50, 39, 50) and r["t4"][ETH][3:] == (600, 468, 600), r["t4"]
    # avant t5 : B = 1200, T_lo = max(0, 990 - 500) + 468 = 958 ; non marqué max 242 -> borne basse 408
    assert r["t5"][ETH] == (650, 408, 650), r["t5"]
    # sans propagation par l'échange (règle s50 : produits de vente non marqués), la borne basse serait max(0, 650 - 710) = 0
_selftest()

if __name__ == "__main__":
    a = N.B298
    ledger = rd(R / "data/base_0xb298_ledger.csv")
    txs = per_tx(ledger, a); taint = fill_taint()
    t_first = min(t["ts"] for t in txs if t["tx"] in taint)
    rows, bk = run(txs, taint, t_first)
    rows_w, _ = run(txs, fill_taint(relay_traced=True), t_first)
    lo_w = {t["tx"]: {k: v[1] for k, v in t["res"].items()} for t in rows_w}
    dln = {r["tx"]: r for r in rd(R / "evidence/s12_dln_base.csv")}
    old = {r["tx"]: r for r in rd(R / "BASE_FLOWS.csv") if r["wallet"] == a}
    sym = {}
    for t in txs: sym.update(t["sym"])
    out = []; pos = collections.defaultdict(lambda: collections.Counter())
    for t in rows:
        if t["ts"] < "2024-10-01": continue
        d = dln.get(t["tx"]) or {}; res = t["res"]
        cat = ("dln_order_out" if d.get("event") == "CreatedOrder" else "dln_fill_in" if d.get("event") == "FulfilledOrder" else
               "swap" if len([k for k, v in res.items() if v[0]]) == 1 and len([k for k, v in res.items() if len(v) > 3 and v[3]]) == 1 else
               "transfer_out" if any(v[0] for v in res.values()) else "transfer_in")
        for k, v in res.items():
            x, lo, hi = v[:3]; y, clo, chi = (v[3:] + (0, 0, 0))[:3]
            if cat == "swap" and k != ETH and k != USDC_BASE:
                p = pos[k]; p["n_buy" if y else "n_sell"] += 1; p["tok_in"] += y; p["tok_out"] += x; p["lo_in"] += clo; p["lo_out"] += lo
            if cat == "swap" and k == ETH:
                tok = next((kk for kk in res if kk != ETH), None)
                if tok: pos[tok]["eth_spent" if x else "eth_got"] += x or y; pos[tok]["eth_lo_spent" if x else "eth_lo_got"] += lo if x else clo
            if x and (cat in ("dln_order_out", "transfer_out") or k in (ETH, USDC_BASE)):
                o = old.get(t["tx"], {})
                out.append(dict(utc=t["ts"].replace("T", " "), block=t["block"], tx=t["tx"], category=cat, asset=sym.get(k, k), token=k if k != ETH else "",
                                out_raw=x, marked_min_raw=lo, marked_max_raw=hi, marked_min_share=round(lo / x, 6),
                                dln_orderId=d.get("orderId", ""), dln_take_chain=d.get("takeChain", ""), receiver=d.get("receiverDst", "") or ",".join(sorted(t["cps"]))[:120],
                                marked_min_raw_relay_traced=lo_w[t["tx"]].get(k, 0), s50_min=o.get("eth_out_marked_min" if k == ETH else "usdc_out_marked_min", "")))
    N.write_csv(R / "evidence/s60_b298_base_out_bounds.csv", out)
    prow = []
    for k, p in sorted(pos.items(), key=lambda kv: -kv[1]["eth_spent"]):
        prow.append(dict(token=k, symbol=sym.get(k, ""), n_buy=p["n_buy"], n_sell=p["n_sell"], eth_spent=p["eth_spent"] / 1e18, eth_got=p["eth_got"] / 1e18,
                         eth_spent_marked_min=p["eth_lo_spent"] / 1e18, eth_got_marked_min=p["eth_lo_got"] / 1e18,
                         tokens_in_raw=p["tok_in"], tokens_out_raw=p["tok_out"], tokens_in_marked_min_raw=p["lo_in"], broken=bk.broken.get(k, "")))
    N.write_csv(R / "evidence/s60_b298_base_positions.csv", prow)
    for k, tx in bk.broken.items(): print("actif rompu", sym.get(k, k), k, "à", tx)
    print(len(out), "sorties ;", len(prow), "jetons échangés depuis le 01/10/2024 ; actifs rompus :", len(bk.broken))
    for o in out:
        if o["category"] == "dln_order_out" or o["tx"] == "0x52da33cb31aa36ecce1a05774dd7bc69bed8d0a9b555db97e8659771a4a00245":
            print(o["utc"], o["category"], o["asset"], o["out_raw"] / (1e18 if o["asset"] == ETH else 1e6), "min", round(o["marked_min_raw"] / (1e18 if o["asset"] == ETH else 1e6), 6), "relais tracé", round(o["marked_min_raw_relay_traced"] / (1e18 if o["asset"] == ETH else 1e6), 6),
                  "s50", o["s50_min"], "->", o["dln_take_chain"], o["receiver"][:12])
