"""Où va l'argent après les ordres DMAGA vers b947. Trois niveaux :
1) b947 : sorties dans 5 min, 1 h, 24 h, 7 j après chaque arrivée ; puis le vidage complet (comptabilité de stock : solde ramené à 0,012 USDC, pas de FIFO).
2) relais 0x4978cd7e : entrées et sorties (tout vers b298).
3) b298 : sorties dans 5 min, 1 h, 24 h après chaque arrivée venue de b947 ou du relais ; signalées « quasi identiques » si |sortie-entrée| < 1 %.
   b298 mélange d'autres fonds : ces lignes décrivent une proximité temporelle et de montant, pas une attribution FIFO.
Sortie : ../b947_post_dmaga_flows.csv"""
import csv, datetime as dt
B947, B298, RELAY = "0xb947bf7f409e998b28f8e218802fc9575c3c8c57", "0xb29826d809aa04d2ead6f2310d8965a45b87fa67", "0x4978cd7e5a3565cafcc88a105940b0ea01adc04d"
P = lambda s: dt.datetime.strptime(s, "%Y-%m-%d %H:%M:%S")
load = lambda p: [r for r in csv.DictReader(open(p)) if not r["flags"] and r["kind"] != "call"]
H, R, B = load("../b947_full_history.csv"), load("../evidence/relay_4978_history.csv"), load("../evidence/b298_full_history.csv")
D = {(r["tx"].lower()): r for r in csv.DictReader(open("../evidence/dln_orders_evm.csv"))}
WIN = [("5min", 300), ("1h", 3600), ("24h", 86400), ("7d", 604800)]
rows = []
def add(level, ev, rel=None, delay=None, window="", note=""):
    d = D.get(ev["tx_hash"].lower())
    dl = f"DLN {d['give_chain']}->{d['take_chain']} receveur {d['receiver']}" if d and d["direction"] == "OUT" else (f"DLN maker {d['maker']}" if d else "")
    rows.append(dict(level=level, event_utc=ev["timestamp_utc"], tx_hash=ev["tx_hash"], wallet=ev["wallet"], direction=ev["direction"], asset=ev["asset"],
                     amount=ev["amount"], counterparty=ev["counterparty"], category=ev["category"], label=(ev["label"] or ev["inferred_label"])[:80], dln=dl,
                     related_arrival_tx=rel or "", delay_s=delay if delay is not None else "", window=window, note=note))
arr = [r for r in H if r["direction"] == "IN" and r["asset"] == "USDC" and r["timestamp_utc"] >= "2024-07-01"]
outs = [r for r in H if r["direction"] == "OUT" and r["asset"] == "USDC" and r["timestamp_utc"] >= "2024-07-01"]
for a in arr:
    d = D.get(a["tx_hash"].lower()); src = f"ordre DLN de {d['maker']}" if d else ("b298" if a["counterparty"] == B298 else "")
    t0 = P(a["timestamp_utc"])
    counts = {w: sum(1 for o in outs if 0 <= (P(o["timestamp_utc"]) - t0).total_seconds() <= s) for w, s in WIN}
    first = min(outs, key=lambda o: o["timestamp_utc"])
    add("1_b947_arrivee", a, note=f"source {src} ; sorties b947 : 5min={counts['5min']} 1h={counts['1h']} 24h={counts['24h']} 7d={counts['7d']} ; "
        f"première sortie {first['timestamp_utc']} ({(P(first['timestamp_utc']) - t0).days} j après)")
for o in outs:
    add("1_b947_vidage", o, note="vidage du stock : 434 281,32 USDC reçus (+10 USDC d'un empoisonneur), solde final 0,012 USDC")
for r in R:
    if r["asset"] in ("USDC", "ETH") and float(r["amount"]) > 0:
        add("2_relais", r, note="relais gazé une seule fois par b298 (0,02 ETH le 06/10/2024)" if r["asset"] == "ETH" else "")
src_arr = [r for r in B if r["direction"] == "IN" and r["asset"] == "USDC" and r["counterparty"] in (B947, RELAY) and r["timestamp_utc"] >= "2024-07-01"]
bouts = [r for r in B if r["direction"] == "OUT" and float(r["amount"]) > 0]
for a in src_arr:
    add("3_b298_arrivee", a, note="arrivée venue de b947" if a["counterparty"] == B947 else "arrivée venue du relais")
    t0 = P(a["timestamp_utc"]); amt = float(a["amount"])
    for o in bouts:
        dlt = (P(o["timestamp_utc"]) - t0).total_seconds()
        if 0 <= dlt <= 86400:
            w = next(w for w, s in WIN if dlt <= s)
            qi = o["asset"] == "USDC" and abs(float(o["amount"]) - amt) / amt < 0.01
            add("3_b298_sortie", o, rel=a["tx_hash"], delay=int(dlt), window=w, note=("QUASI IDENTIQUE au montant arrivé ; " if qi else "") + "fonds mélangés chez b298 : proximité, pas FIFO")
rows.sort(key=lambda r: (r["event_utc"], r["level"]))
with open("../b947_post_dmaga_flows.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
for r in rows:
    if r["level"] != "3_b298_sortie" or "QUASI" in r["note"] or r["dln"]:
        print(r["level"], r["event_utc"], r["direction"], r["asset"], round(float(r["amount"]), 2), r["counterparty"][:10], r["dln"][:60], r["delay_s"], r["note"][:90])
