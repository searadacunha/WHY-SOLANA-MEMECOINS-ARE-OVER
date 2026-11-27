"""H3Qs (cité par @toupaiwang le 30/07/2024 : meilleurs trades DMAGA, JOE, ZOOMER) : bilan par mint sur trois mois, pertes comprises.

Fenêtre 25/04/2024 - 31/07/2024 (trois mois avant le post). Chaque transaction réussie est relue : variation des soldes de
jetons du wallet par mint, variation de SOL natif et de WSOL. Une transaction qui ne fait varier qu'un seul jeton (hors WSOL,
USDC) lui impute son SOL ; sinon elle est classée « multi » et exclue du bilan par mint (comptée à part).
Sortie : data/h3qs_by_mint.csv, data/h3qs_rotations.csv (vente d'un jeton suivie d'un achat d'un autre dans les 5 minutes)."""
import csv
import json
from collections import defaultdict
from h_lib import DATA, DMAGA, EXT, utc
import k16_pubrpc as pub
from h_decode import sol_delta
from h50_contracts import metaplex

H3 = "H3QsBrrivimFJmSpTXuvig2n1Bh7JuYxrriRSEszT6cc"
A, Z = 1714003200, 1722470400
QUOTE = {"So11111111111111111111111111111111111111112", "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"}


def deltas(t, owner):
    d = defaultdict(int)
    for side, sgn in (("preTokenBalances", -1), ("postTokenBalances", 1)):
        for b in t["meta"].get(side) or []:
            if b.get("owner") == owner:
                d[b["mint"]] += sgn * int(b["uiTokenAmount"]["amount"])
    return {m: v for m, v in d.items() if v}


if __name__ == "__main__":
    sigs = [x for x in json.loads((EXT / f"sigs_{H3}.json").read_text())["sigs"] if not x.get("err") and A <= x["blockTime"] < Z]
    per = defaultdict(lambda: {"n_buys": 0, "n_sells": 0, "bought": 0, "sold": 0, "sol_spent": 0, "sol_received": 0, "first": None, "last": None})
    events, multi = [], 0
    for x in sorted(sigs, key=lambda x: x["slot"]):
        t = pub.tx(x["signature"])
        d = deltas(t, H3)
        sol = sol_delta(t, H3) + d.get("So11111111111111111111111111111111111111112", 0)
        toks = {m: v for m, v in d.items() if m not in QUOTE}
        if len(toks) != 1:
            multi += bool(toks)
            continue
        (m, v), = toks.items()
        p = per[m]
        p["first"] = p["first"] or t["blockTime"]
        p["last"] = t["blockTime"]
        if v > 0:
            p["n_buys"] += 1; p["bought"] += v; p["sol_spent"] += -min(sol, 0)
        else:
            p["n_sells"] += 1; p["sold"] += -v; p["sol_received"] += max(sol, 0)
        events.append((t["blockTime"], x["signature"], m, v, sol))
    rows = []
    for m, p in per.items():
        rows.append({"mint": m, **p, "first": utc(p["first"]), "last": utc(p["last"]), "net_sol": (p["sol_received"] - p["sol_spent"]) / 1e9,
                     "closed": p["sold"] >= 0.99 * p["bought"] if p["bought"] else False})
    rows.sort(key=lambda r: -abs(r["net_sol"]))
    for r in rows[:25]:
        meta = metaplex(r["mint"])
        r["symbol"], r["name"] = meta.get("symbol", ""), meta.get("name", "")
    with (DATA / "h3qs_by_mint.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["mint", "symbol", "name", "n_buys", "n_sells", "bought", "sold", "sol_spent", "sol_received", "net_sol", "closed", "first", "last"])
        w.writeheader()
        w.writerows(rows)
    rot = [(a, b) for a, b in zip(events, events[1:]) if a[3] < 0 and b[3] > 0 and a[2] != b[2] and b[0] - a[0] <= 300]
    with (DATA / "h3qs_rotations.csv").open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["sell_utc", "sell_signature", "sold_mint", "sold_raw", "sol_from_sell", "buy_utc", "buy_signature", "bought_mint", "bought_raw", "sol_for_buy", "gap_s"])
        for a, b in rot:
            w.writerow([utc(a[0]), a[1], a[2], -a[3], a[4], utc(b[0]), b[1], b[2], b[3], b[4], b[0] - a[0]])
    tot = sum(r["net_sol"] for r in rows)
    print("tx", len(sigs), "multi exclues", multi, "mints", len(rows), "net SOL toutes positions", round(tot, 3),
          "gagnantes", sum(1 for r in rows if r["net_sol"] > 0), "perdantes", sum(1 for r in rows if r["net_sol"] < 0))
    for r in rows[:12]:
        print(r.get("symbol", ""), r["mint"][:8], r["n_buys"], r["n_sells"], round(r["net_sol"], 3), r["closed"], r["first"][:10])
    print("rotations", [(utc(a[0]), a[2][:6], b[2][:6], b[0] - a[0]) for a, b in rot if DMAGA in (a[2], b[2])])
