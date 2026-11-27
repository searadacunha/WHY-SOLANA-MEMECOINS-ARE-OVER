"""Relation b298 <-> b947 : transferts directs (et via le relais 0x4978cd7e), contexte avant/après, parts, gaz, sessions à somme exacte.
Entrées : ../b947_full_history.csv, ../evidence/b298_full_history.csv, ../evidence/relay_4978_history.csv. Sorties : ../b298_b947_relationship.csv, ../evidence/s40_metrics.json"""
import csv, json, datetime as dt
B947, B298, RELAY = "0xb947bf7f409e998b28f8e218802fc9575c3c8c57", "0xb29826d809aa04d2ead6f2310d8965a45b87fa67", "0x4978cd7e5a3565cafcc88a105940b0ea01adc04d"
H = [r for r in csv.DictReader(open("../b947_full_history.csv")) if not r["flags"] and r["kind"] != "call"]
R = [r for r in csv.DictReader(open("../evidence/relay_4978_history.csv")) if not r["flags"] and r["kind"] != "call"]
P = lambda s: dt.datetime.strptime(s, "%Y-%m-%d %H:%M:%S")
def ctx(rows, i, before=True, win=3600):
    t = P(rows[i]["timestamp_utc"]); out = []
    rng = range(i - 1, -1, -1) if before else range(i + 1, len(rows))
    for j in rng:
        d = abs((P(rows[j]["timestamp_utc"]) - t).total_seconds())
        if d > win: break
        r = rows[j]; out.append(f"{r['direction']} {round(float(r['amount']), 6)} {r['asset']} {r['counterparty'][:10]} ({int(d)} s)")
    return " ; ".join(out[:4])
rel = []
for src, rows in (("direct", H), ("via_relay_0x4978cd7e", R)):
    for i, r in enumerate(rows):
        if r["counterparty"] != B298: continue
        sens = ("b298->b947" if r["direction"] == "IN" else "b947->b298") if src == "direct" else ("b298->relay" if r["direction"] == "IN" else "relay->b298")
        rel.append(dict(date_utc=r["timestamp_utc"], path=src, sens=sens, asset=r["asset"], amount=r["amount"], amount_raw=r["amount_raw"], tx_hash=r["tx_hash"],
                        gas_payer=r["gas_payer"], context_before_1h=ctx(rows, i, True), context_after_1h=ctx(rows, i, False)))
rel.sort(key=lambda r: r["date_utc"])
with open("../b298_b947_relationship.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rel[0])); w.writeheader(); w.writerows(rel)
# mesures
usd = lambda rows, d, cp=None: sum(float(r["amount"]) for r in rows if r["asset"] == "USDC" and r["direction"] == d and (cp is None or r["counterparty"] == cp))
eth_in = [r for r in H if r["asset"] == "ETH" and r["direction"] == "IN"]
inflow_by = {}
for r in H:
    if r["asset"] == "USDC" and r["direction"] == "IN":
        lab = "b298" if r["counterparty"] == B298 else ("deBridge (makers DMAGA)" if r["category"] == "bridge_taker" else (r["label"].split("|")[-1].split(",")[0] if r["label"] else r["counterparty"]))
        inflow_by[lab] = inflow_by.get(lab, 0) + float(r["amount"])
out_by = {}
for r in H:
    if r["asset"] == "USDC" and r["direction"] == "OUT":
        lab = "b298" if r["counterparty"] == B298 else ("relais 0x4978cd7e (tout vers b298)" if r["counterparty"] == RELAY else (r["inferred_label"] or r["counterparty"]))
        out_by[lab] = out_by.get(lab, 0) + float(r["amount"])
# gaz juste-à-temps : délai entre chaque ETH reçu de b298 et la tx suivante signée par b947
calls = [r for r in csv.DictReader(open("../b947_full_history.csv")) if r["gas_payer"] == B947 and r["direction"] == "OUT"]
jit = []
for r in eth_in:
    nxt = min((c for c in calls if c["timestamp_utc"] > r["timestamp_utc"]), key=lambda c: c["timestamp_utc"], default=None)
    jit.append(dict(topup=r["timestamp_utc"], eth=float(r["amount"]), tx=r["tx_hash"], from_b298=r["counterparty"] == B298,
                    next_b947_tx=nxt["timestamp_utc"] if nxt else None, delay_s=int((P(nxt["timestamp_utc"]) - P(r["timestamp_utc"])).total_seconds()) if nxt else None))
# sessions : chaque sortie USDC de b947 comparée à la somme exacte des entrées USDC depuis la sortie précédente
sess, acc, parts = [], 0, []
for r in sorted([r for r in H if r["asset"] == "USDC"], key=lambda r: (r["timestamp_utc"], r["direction"] == "OUT")):
    a = int(r["amount_raw"])
    if r["direction"] == "IN": acc += a; parts.append((r["counterparty"][:10], a))
    else:
        sess.append(dict(out_utc=r["timestamp_utc"], out_tx=r["tx_hash"], out_to=r["counterparty"], out_raw=a, inflows_since_last_out_raw=acc, exact=acc == a, parts=parts[:]))
        acc -= a; parts = [] if acc == 0 else [("solde", acc)]
m = dict(transfers_direct=sum(1 for r in rel if r["path"] == "direct"), transfers_via_relay=sum(1 for r in rel if r["path"] != "direct"),
         first=rel[0]["date_utc"], last=rel[-1]["date_utc"],
         b947_usdc_in_total=usd(H, "IN"), b947_usdc_in_from_b298=usd(H, "IN", B298), b947_usdc_in_by_source=inflow_by,
         b947_usdc_out_total=usd(H, "OUT"), b947_usdc_out_by_dest=out_by,
         b947_eth_in_total=sum(float(r["amount"]) for r in eth_in), b947_eth_in_from_b298=sum(float(r["amount"]) for r in eth_in if r["counterparty"] == B298),
         b947_eth_topups=jit, b947_eth_back_to_b298=[(r["timestamp_utc"], r["amount"], r["tx_hash"]) for r in H if r["asset"] == "ETH" and r["direction"] == "OUT" and r["counterparty"] == B298],
         usdc_sessions=sess)
json.dump(m, open("../evidence/s40_metrics.json", "w"), indent=1, default=str)
print(json.dumps({k: v for k, v in m.items() if k not in ("usdc_sessions",)}, indent=1, default=str)[:3500])
for s in sess: print(s["out_utc"], s["out_to"][:10], s["out_raw"] / 1e6, "entrées", s["inflows_since_last_out_raw"] / 1e6, "EXACT" if s["exact"] else "")
