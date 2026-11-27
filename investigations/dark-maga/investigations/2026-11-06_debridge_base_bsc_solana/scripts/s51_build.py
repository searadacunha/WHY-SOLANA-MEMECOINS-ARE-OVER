"""Construit les livrables CSV à partir des données collectées (aucun appel réseau) :
BASE_FLOWS.csv, BSC_FLOWS.csv, SOLANA_RETURN_FLOWS.csv, CROSSCHAIN_LINKS.csv. Bornes : s50_bounds (sans FIFO)."""
import csv, json, sys, os, collections
sys.path.insert(0, os.path.dirname(__file__))
import nt_lib as N
from s50_bounds import bounds
R = N.ROOT
B298, ZX = N.B298, "0x2ac17414e34c9a1f70f6eadb6230fa503301e878"
USDC_BASE = "0x833589fcd6edb6e08f4c7c32d4f71b54bda02913"
CB_DEP = "0x34172888e808debea84bb224bbfa8dcd6d78de7d"
TAKERS = {"0x663dc15d3c1ac63ff12e45ab68fea3f0a883c251", "0x555ce236c0220695b68341bc48c68d52210cc35b"}
LABEL = {CB_DEP: "dépôt Coinbase inféré (Base) : balayé vers Coinbase 14/31/41/42/55", ZX: "satellite 0x2ac17414 (gaz de b298)",
         B298: "b298", N.MEXC_DEP: "dépôt MEXC inféré (Ethereum)", "0xb1e5042f759dc67a2eed103cd4425a73b44e678e": "dépôt BloFin inféré (Ethereum)",
         N.EI5: "Ei5yGz8d (Solana)", "0x4b6a508cd730434b4f9a0e32be3646f71b58a8d3": "satellite Base 0x4b6a508c (mars-avril 2024)"}
DEX = {"0x3fc91a3afd70395cd496c647d5a6cc9d4b2b7fad": "Uniswap UniversalRouter", "0x0389879e0156033202c44bf784ac18fc02edee4f": "Sushi RouteProcessor4",
       "0xf2614a233c7c3e7f08b1f887ba133a13f1eb2c55": "Sushi RouteProcessor5", "0xdef1c0ded9bec7f1a1670819833240f027b25eff": "0x ZeroEx",
       "0x0000000000001ff3684f28c67538d4d072c22734": "0x AllowanceHolder"}

def rd(p): return list(csv.DictReader(open(p)))
DLN_BASE = {r["tx"]: r for r in rd(R / "evidence/s12_dln_base.csv")}
S51 = {r["tx_hash"].lower(): r for r in rd(N.OLD_INV / "evidence/s51_b298_usdc_bounds.csv")}
for _r in rd(R / "evidence/s15_s51_corrected.csv"):  # bornes basses sous H (relais = b947), recalculées par s15 : s51 trace le relais depuis le 06/11
    S51[_r["tx_hash"].lower()]["from_b947_min"] = _r["from_b947_min_under_H"]
ETH_ORD = {r["orderId"].lower(): r for r in rd(N.OLD_INV / "evidence/dln_orders_evm.csv") if r["direction"] in ("created", "out", "OUT", "maker") or True}

def taint_share_of_fill(fill_tx):
    """Part (min, max) venue de b947 de l'USDC donné par l'ordre Ethereum que paie ce fill Base, sous H (relais = b947)."""
    d = DLN_BASE.get(fill_tx)
    if not d or d["event"] != "FulfilledOrder" or d["giveChain"] != "ethereum": return None
    eo = ETH_ORD.get(d["orderId"].lower())
    if not eo: return None
    b = S51.get(eo["tx"].lower())
    if not b: return None
    amt = float(b["amount"]); return float(b["from_b947_min"]) / amt, float(b["from_b947_max"]) / amt, eo["tx"]

def per_tx(ledger, a):
    by = collections.OrderedDict()
    for r in ledger:
        t = by.setdefault(r["tx"], dict(ts=r["ts"], block=int(r["block"]), eth=0, usdc=0, fee=0, cps=set(), toks=collections.Counter(), meth=set(), eth_in=0, eth_out=0))
        if r["kind"] == "tx" and r["status"] != "ok": r = dict(r, raw="0")
        s = 1 if r["dir"] == "in" else (-1 if r["dir"] == "out" else 0)
        if r["kind"] in ("tx", "internal") and r["asset"] == "ETH":
            v = int(r["raw"] or 0); t["eth"] += s * v
            if s > 0: t["eth_in"] += v
            elif s < 0: t["eth_out"] += v
            if r["kind"] == "tx" and r["frm"] == a: t["fee"] += int(r["fee"] or 0)
        elif r["kind"] == "token" and r["token"] == USDC_BASE and r["raw"] != "":
            t["usdc"] += s * int(r["raw"])
        elif r["kind"] == "token" and r["raw"] != "" and s:
            t["toks"][r["asset"]] += s
        cp = r["to"] if r["dir"] == "out" else r["frm"]
        if cp != a: t["cps"].add(cp)
        t["meth"].add(r["method"])
    return by

def classify(tx, t, a):
    d = DLN_BASE.get(tx)
    if d and d["event"] == "FulfilledOrder" and d["receiverDst"].lower() == a: return "dln_fill_in", d
    if d and d["event"] == "CreatedOrder" and d["makerSrc"].lower() == a: return "dln_order_out", d
    cps = t["cps"]
    if cps & set(DEX) or t["toks"]:
        return ("swap_buy" if t["eth"] + t["fee"] < 0 or t["usdc"] < 0 else "swap_sell"), None
    if len(cps) == 1:
        c = next(iter(cps)); return ("transfer_out" if t["eth"] < 0 or t["usdc"] < 0 else "transfer_in"), {"counterparty": c}
    return "other", None

def base_flows(a, t0, t1, taint_fn):
    ledger = rd(R / f"data/base_{a[:6]}_ledger.csv")
    txs = per_tx(ledger, a); rows = []; evE = []; evU = []
    for tx, t in txs.items():
        cat, d = classify(tx, t, a)
        sh = taint_fn(tx, cat, d)
        net_eth = t["eth"] - t["fee"]
        # entrées / sorties d'ETH par tx (frais inclus dans la sortie)
        if t["eth_in"]:
            mn, mx = (int(t["eth_in"] * sh[0]), int(t["eth_in"] * sh[1])) if sh else (0, 0)
            evE.append(dict(kind="in", x=t["eth_in"], taint_min=mn, taint_max=mx, proceeds=(cat == "swap_sell" or (cat == "swap_buy" and t["eth_in"] > 0)), tx=tx))
        if t["eth_out"] + t["fee"]:
            evE.append(dict(kind="out", x=t["eth_out"] + t["fee"], tx=tx))
        if t["usdc"] > 0:
            mn, mx = (int(t["usdc"] * sh[0]), int(t["usdc"] * sh[1])) if sh else (0, 0)
            evU.append(dict(kind="in", x=t["usdc"], taint_min=mn, taint_max=mx, proceeds=cat.startswith("swap"), tx=tx))
        elif t["usdc"] < 0:
            evU.append(dict(kind="out", x=-t["usdc"], tx=tx))
        t["cat"], t["d"], t["share"] = cat, d, sh
    bE = {e["tx"]: e for e in bounds(evE)}; bU = {e["tx"]: e for e in bounds(evU)}
    for tx, t in txs.items():
        if not (t0 <= t["ts"] <= t1): continue
        if abs(t["eth"] - t["fee"]) < 10 ** 15 and abs(t["usdc"]) < 10 ** 6: continue
        d = t["d"] or {}; cp = d.get("counterparty") or (",".join(sorted(t["cps"]))[:200])
        rec = d.get("receiverDst", "") if t["cat"].startswith("dln") else ""
        rows.append(dict(chain="base", wallet=a, utc=t["ts"].replace("T", " "), block=t["block"], tx=tx, category=t["cat"],
                         eth_net=round((t["eth"] - t["fee"]) / 1e18, 9), usdc_net=round(t["usdc"] / 1e6, 6),
                         tokens=" ".join(f"{k}:{v:+d}" for k, v in t["toks"].items()),
                         counterparty=cp if not t["cat"].startswith("dln") else (d.get("makerSrc") if t["cat"] == "dln_fill_in" else rec),
                         counterparty_label=LABEL.get((d.get("counterparty") or rec or "").lower() if (d.get("counterparty") or rec) else "", LABEL.get(rec, "")) or ", ".join(sorted({DEX[c] for c in t["cps"] if c in DEX})),
                         dln_orderId=d.get("orderId", ""), dln_other_chain=(d.get("giveChain") if t["cat"] == "dln_fill_in" else d.get("takeChain", "")),
                         dln_take_amount_raw=d.get("takeAmount", ""), dln_take_token=d.get("takeTokenAddress", ""),
                         tainted_inflow_share_min=round(t["share"][0], 6) if t["share"] else "", source_order_eth_tx=t["share"][2] if t["share"] and len(t["share"]) > 2 else "",
                         eth_out_marked_min=round(bE[tx]["lo"] / 1e18, 9) if tx in bE else "", eth_out_marked_max=round(bE[tx]["hi"] / 1e18, 9) if tx in bE else "",
                         usdc_out_marked_min=round(bU[tx]["lo"] / 1e6, 6) if tx in bU else "", usdc_out_marked_max=round(bU[tx]["hi"] / 1e6, 6) if tx in bU else ""))
    return rows

def taint_b947(tx, cat, d):
    if cat != "dln_fill_in": return None
    s = taint_share_of_fill(tx)
    return s if s and s[0] > 0 else None

def taint_ei5(tx, cat, d):
    return (1.0, 1.0, "") if cat == "dln_fill_in" and d and d["makerSrc"] == N.EI5 else None

if __name__ == "__main__":
    rows = base_flows(B298, "2024-10-01", "2025-01-31", taint_b947)
    for r in rows: r["marker"] = "USDC venu de b947, sous H (relais = b947)"
    rz = base_flows(ZX, "2024-10-01", "2025-03-31", taint_ei5)
    for r in rz: r["marker"] = "ETH des ordres d'Ei5yGz8d"
    cb = [r for r in rd(R / "data/base_0x3417_ledger.csv")]
    rc = [dict(chain="base", wallet=CB_DEP, utc=r["ts"].replace("T", " "), block=r["block"], tx=r["tx"], category="transfer_" + r["dir"], eth_net=(1 if r["dir"] == "in" else -1) * float(r["amount"]),
               counterparty=r["frm"] if r["dir"] == "in" else r["to"], counterparty_label=(r["to_name"] or r["from_name"] or ""), marker="adresse de dépôt Coinbase inférée") for r in cb]
    fields = ["chain", "wallet", "utc", "block", "tx", "category", "eth_net", "usdc_net", "tokens", "counterparty", "counterparty_label", "dln_orderId", "dln_other_chain",
              "dln_take_amount_raw", "dln_take_token", "tainted_inflow_share_min", "source_order_eth_tx", "eth_out_marked_min", "eth_out_marked_max",
              "usdc_out_marked_min", "usdc_out_marked_max", "marker"]
    N.write_csv(R / "BASE_FLOWS.csv", rows + rz + rc, fields)
    print("BASE_FLOWS", len(rows), len(rz), len(rc))
