"""Profil comportemental de chaque wallet EVM sur l'historique nettoyé. Fenêtres DMAGA : avant < 2024-07-14 ; pendant 2024-07-14 -> 2024-08-31 ;
après > 2024-08-31. Délai réception -> sortie : pour chaque entrée de stablecoin ou d'ETH >= 100 USD-équivalent (1 ETH compté 3 000 USD,
ordre de grandeur seulement), délai jusqu'à la sortie suivante du même actif. 'Vidage' : sortie qui ramène le solde de l'actif sous 1 %.
Sortie : ../evidence/s90_profiles.json"""
import csv, json, os, statistics as st, datetime as dt
F = {"b947": "../b947_full_history.csv", "b298": "../evidence/b298_full_history.csv", "86f9": "../evidence/86f9_full_history.csv",
     "2d86": "../evidence/2d86_full_history.csv", "relay_4978": "../evidence/relay_4978_history.csv"}
X = {"b947": "../evidence/s60_crosschain.json"}
P = lambda s: dt.datetime.strptime(s, "%Y-%m-%d %H:%M:%S")
out = {}
for k, p in F.items():
    if not os.path.exists(p): continue
    R = [r for r in csv.DictReader(open(p)) if not r["flags"]]
    own = {r["tx_hash"] for r in R if r["gas_payer"] == r["from"] and r["direction"] == "OUT"}
    V = [r for r in R if r["kind"] != "call"]
    per = lambda a, b: [r for r in R if a <= r["timestamp_utc"] < b]
    def vol(rows, d):
        return dict(stable_usd=round(sum(float(r["amount"]) for r in rows if r["direction"] == d and r["asset"] in ("USDC", "USDT", "DAI")), 2),
                    eth=round(sum(float(r["amount"]) for r in rows if r["direction"] == d and r["kind"].startswith("native")), 4))
    cps = {r["counterparty"] for r in V}
    cex = sorted({(r["label"].split("|")[-1].split(",")[0]) for r in V if r["category"] == "cex"})
    cexd = sorted({r["counterparty"] for r in V if r["category"] == "cex_deposit_inferred"})
    br = sorted({r["counterparty"] for r in V if r["category"] in ("bridge",)})
    # délais et vidages
    bal, delays, sweeps, nout = {}, [], 0, 0
    pend = {}
    for r in sorted(V, key=lambda r: (r["timestamp_utc"], r["direction"] == "OUT")):
        a = "ETH" if r["kind"].startswith("native") else r["asset"]
        if a not in ("USDC", "USDT", "DAI", "ETH") or (a == "ETH" and not r["kind"].startswith("native")): continue
        x = float(r["amount"]); usd = x * (3000 if a == "ETH" else 1)
        if r["direction"] == "IN":
            bal[a] = bal.get(a, 0) + x
            if usd >= 100: pend.setdefault(a, []).append(P(r["timestamp_utc"]))
        else:
            before = bal.get(a, 0); bal[a] = before - x; nout += 1
            if before > 0 and bal[a] <= 0.01 * before: sweeps += 1
            for t in pend.pop(a, []): delays.append((P(r["timestamp_utc"]) - t).total_seconds())
    first, last = min(r["timestamp_utc"] for r in R), max(r["timestamp_utc"] for r in R)
    out[k] = dict(first_seen=first, last_seen=last, age_days=(P(last) - P(first)).days, rows=len(R), own_signed_tx=len(own),
                  counterparties=len(cps), tokens_distinct=len({r["token_contract"] for r in V if r["token_contract"]}),
                  volume_in=vol(V, "IN"), volume_out=vol(V, "OUT"),
                  activity_rows=dict(before_dmaga=len(per("0", "2024-07-14")), during_dmaga=len(per("2024-07-14", "2024-09-01")), after_dmaga=len(per("2024-09-01", "9"))),
                  outflows_stable_eth=nout, sweeps_to_under_1pct=sweeps,
                  median_receipt_to_outflow_h=round(st.median(delays) / 3600, 2) if delays else None, n_delays=len(delays),
                  cex_hot_wallets_tagged=cex, cex_deposits_inferred=cexd, bridges=br,
                  dln_fills_in=sum(1 for r in V if r["category"] == "bridge_taker" or (r["counterparty"] == "0xe7351fd770a37282b91d153ee690b63579d6dd7f" and r["direction"] == "IN")))
cc = json.load(open("../evidence/s60_crosschain.json"))
for k in out:
    out[k]["nonce_other_chains"] = {c.split(".")[1]: v.get("nonce") for c, v in cc.items() if c.startswith(k + ".")}
json.dump(out, open("../evidence/s90_profiles.json", "w"), indent=1)
for k, v in out.items():
    print(k, {x: v[x] for x in ("first_seen", "age_days", "own_signed_tx", "counterparties", "tokens_distinct", "volume_in", "volume_out", "activity_rows", "sweeps_to_under_1pct", "outflows_stable_eth", "median_receipt_to_outflow_h", "n_delays")})
    print("   CEX", v["cex_hot_wallets_tagged"][:8], "dépôts", len(v["cex_deposits_inferred"]), "ponts", len(v["bridges"]), "nonces", v["nonce_other_chains"])
