"""Contreparties communes entre b947 (+ relais 0x4978cd7e), b298, 2d86, 86f9, sur les historiques nettoyés (sans empoisonnement).
Rôle : hub de service (CEX hot wallet, routeur, pont, contrat de jeton, pool) exclu des conclusions ; dépôt CEX inféré = per-utilisateur, signal
mais pas preuve ; wallet = contrepartie non-service. Sortie : ../evm_shared_counterparties.csv"""
import csv, os, sys
sys.path.insert(0, ".")
F = {"b947": "../b947_full_history.csv", "relay_4978": "../evidence/relay_4978_history.csv", "b298": "../evidence/b298_full_history.csv",
     "86f9": "../evidence/86f9_full_history.csv", "2d86": "../evidence/2d86_full_history.csv"}
SELF = {"0xb947bf7f409e998b28f8e218802fc9575c3c8c57": "b947", "0x4978cd7e5a3565cafcc88a105940b0ea01adc04d": "relay_4978",
        "0xb29826d809aa04d2ead6f2310d8965a45b87fa67": "b298", "0x86f99097c563e84dd5190f3e85f6a2988f1c47a5": "86f9", "0x2d86499a410a9ac2139833ba8d6942b8a8700a7b": "2d86"}
STABLE = {"USDC", "USDT", "DAI"}
agg = {}
for k, p in F.items():
    if not os.path.exists(p): print("absent", p); continue
    for r in csv.DictReader(open(p)):
        if r["flags"] or (r["kind"] == "call" and r["category"] not in ("bridge",)): continue
        cp = r["counterparty"]
        if not cp: continue
        a = agg.setdefault(cp, dict(wallets=set(), n=0, usd=0.0, eth=0.0, first="9999", last="", cats=set(), label=r["label"], inferred=r["inferred_label"], dirs=set(), real=False))
        # une contrepartie qui n'a fait qu'envoyer des jetons inconnus est un distributeur non sollicité (airdrop), pas un lien
        a["real"] |= r["direction"] == "OUT" or r["asset"] in STABLE or r["asset"] in ("ETH", "WETH", "WOO", "HOT")
        a["wallets"].add(k); a["n"] += 1; a["first"] = min(a["first"], r["timestamp_utc"]); a["last"] = max(a["last"], r["timestamp_utc"])
        a["cats"].add(r["category"]); a["dirs"].add(f"{k}:{r['direction']}"); a["label"] = a["label"] or r["label"]
        if r["asset"] in STABLE: a["usd"] += float(r["amount"] or 0)
        if r["kind"].startswith("native"): a["eth"] += float(r["amount"] or 0)  # ETH natif seul : un jeton peut s'appeler « ETH »
rows = []
for cp, a in agg.items():
    ws = a["wallets"] - ({SELF[cp]} if cp in SELF else set())
    if len(ws | ({SELF[cp]} if cp in SELF else set())) < 2: continue
    cats = a["cats"]
    if cp in SELF: role = "wallet étudié"
    elif not a["real"] or "disperse" in (a["label"] or "").lower(): role = "hub de service : airdrop non sollicité"
    elif "cex_deposit_inferred" in cats: role = "dépôt CEX inféré (par utilisateur)"
    elif cats & {"cex"}: role = "hub de service : CEX"
    elif cats & {"bridge", "bridge_taker"}: role = "hub de service : pont / taker DLN"
    elif cats & {"dex", "contract", "mint"}: role = "hub de service : DEX / contrat"
    else:
        # vérification : un contrat ou une adresse taguée (service metadata Blockscout) n'est pas un wallet personnel
        import ev_lib as E
        info = E.bs(f"/addresses/{cp}"); tg = E.meta_tags(cp)
        if info.get("is_contract") or tg:
            role = "hub de service : " + ("contrat " + (info.get("name") or "") if info.get("is_contract") else "") + (" tags " + ",".join(tg[:3]) if tg else "")
            a["label"] = a["label"] or ",".join(tg[:3])
        else: role = "wallet non-service"
    hub = role.startswith("hub")
    conf = "exclu (service partagé)" if hub else ("signal fort" if role == "wallet étudié" else ("signal moyen (dépôt par utilisateur, à recouper)" if role.startswith("dépôt") else "signal à vérifier"))
    rows.append(dict(counterparty=cp, wallets_connected="|".join(sorted(a["wallets"])), directions="|".join(sorted(a["dirs"])), tx_count=a["n"],
                     total_stable_usd=round(a["usd"], 2), total_eth=round(a["eth"], 6), first_seen=a["first"], last_seen=a["last"], role=role,
                     label_source=("blockscout:" + a["label"][:80]) if a["label"] else ("inféré:" + a["inferred"][:80] if a["inferred"] else "aucune"),
                     excluded_as_service_hub=hub, confidence=conf))
rows.sort(key=lambda r: (r["excluded_as_service_hub"], -len(r["wallets_connected"].split("|")), -r["total_stable_usd"]))
with open("../evm_shared_counterparties.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
for r in rows:
    if not r["excluded_as_service_hub"]: print(r["counterparty"], r["wallets_connected"], r["tx_count"], r["total_stable_usd"], r["total_eth"], r["first_seen"][:10], r["last_seen"][:10], r["role"])
print("hubs exclus", sum(r["excluded_as_service_hub"] for r in rows), "| non-service", sum(not r["excluded_as_service_hub"] for r in rows))
