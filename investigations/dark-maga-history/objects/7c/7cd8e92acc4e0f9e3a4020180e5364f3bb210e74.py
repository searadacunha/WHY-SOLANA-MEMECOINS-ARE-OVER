"""Bornes CONDITIONNELLES sous hypothèse H (le relais 0x4978... transporte exclusivement les USDC de b947), sans FIFO.
ATTENTION : H est non démontrée. Les minima de ce script ne sont pas des bornes garanties sans H.
Voir la correction s15_relay_bounds.py dans investigations/2026-11-06_debridge_base_bsc_solana/ et la PR #16.
Deux réservoirs : T (USDC arrivé de b947 ou du relais 0x4978cd7e à partir du 01/10/2024) et C (tout le reste). L'USDC est fongible :
toute répartition est possible. Pour chaque sortie x, avant elle :
- T_max = T restant si toutes les sorties passées avaient puisé d'abord dans C ; C_max = C restant si elles avaient puisé d'abord dans T ;
- borne basse = max(0, x - C_max) (même au mieux, il n'y avait pas assez d'argent propre) ; borne haute = min(x, T_max).
Les sommes de bornes basses par destination sont des minima valables (prudents). Sortie : ../evidence/s51_b298_usdc_bounds.csv"""
import csv
import sys
print("AVERTISSEMENT : sortie s51 conditionnelle a H ; voir audit PR #16 pour bornes sans H.", file=sys.stderr)
B947, RELAY = "0xb947bf7f409e998b28f8e218802fc9575c3c8c57", "0x4978cd7e5a3565cafcc88a105940b0ea01adc04d"
# entrées de vrai USDC venues d'un sosie (poussière d'empoisonnement) : vraie valeur, gardées pour le solde
R = [r for r in csv.DictReader(open("../evidence/b298_full_history.csv")) if r["asset"] == "USDC"
     and (not r["flags"] or (r["flags"] == "lookalike" and r["direction"] == "IN"))]
R.sort(key=lambda r: (r["timestamp_utc"], int(r["log_index"])))
D = {r["tx"].lower(): r for r in csv.DictReader(open("../evidence/dln_orders_evm.csv"))}
st = {"keepT": [0, 0], "keepC": [0, 0]}  # [T, C] en unités brutes (1e-6 USDC) : keepT puise d'abord dans C, keepC d'abord dans T
out = []
U = lambda v: round(v / 1e6, 6)
for r in R:
    x = int(r["amount_raw"]); tainted_in = r["direction"] == "IN" and r["counterparty"] in (B947, RELAY) and r["timestamp_utc"] >= "2024-10-01"
    if r["direction"] == "OUT":
        r["_lo"] = max(0, x - max(0, st["keepC"][1])); r["_hi"] = min(x, max(0, st["keepT"][0]))
    for mode, s in st.items():
        if r["direction"] == "IN":
            s[0 if tainted_in else 1] += x
        else:
            first, second = (1, 0) if mode == "keepT" else (0, 1)
            take1 = min(x, max(0, s[first])); s[first] -= take1; s[second] -= (x - take1)
    if r["direction"] == "OUT" and r["timestamp_utc"] >= "2024-10-01" and (r["_hi"] > 0 or r["_lo"] > 0):
        d = D.get(r["tx_hash"].lower())
        out.append(dict(utc=r["timestamp_utc"], tx_hash=r["tx_hash"], amount=U(x), counterparty=r["counterparty"], category=r["category"],
                        label=(r["inferred_label"] or r["label"])[:60], dln_dest=(f"{d['take_chain']}:{d['receiver']}" if d else ""),
                        from_b947_min=U(r["_lo"]), from_b947_max=U(r["_hi"]), T_left_if_clean_first=U(st["keepT"][0]), T_left_if_taint_first=U(st["keepC"][0])))
with open("../evidence/s51_b298_usdc_bounds.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(out[0])); w.writeheader(); w.writerows(out)
agg = {}
for o in out:
    k = o["dln_dest"] or (o["label"] or o["category"]) + " " + o["counterparty"][:10]
    a = agg.setdefault(k, [0, 0, 0]); a[0] += o["from_b947_min"]; a[1] += o["from_b947_max"]; a[2] += 1
for k, v in sorted(agg.items(), key=lambda kv: -kv[1][1]):
    print(f"{k[:75]:75s} n={v[2]:3d} min={v[0]:12,.2f} max={v[1]:12,.2f}")
print("T restant à la dernière ligne (propre d'abord, DMAGA d'abord) :", out[-1]["T_left_if_clean_first"], out[-1]["T_left_if_taint_first"])
assert all(o["from_b947_min"] <= o["from_b947_max"] for o in out), "borne basse > borne haute"
