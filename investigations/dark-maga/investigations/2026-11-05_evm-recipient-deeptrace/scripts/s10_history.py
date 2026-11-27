"""Historique normalisé d'une adresse Ethereum : ETH natif (tx et internes), ERC-20, NFT. Sources : Blockscout v2 (principal),
Routescan (internes manquants), RPC public (payeur du gaz des tx non signées par l'adresse).
Drapeaux : 'unsigned_out' = sortie de jeton dans une tx que l'adresse n'a pas signée (empoisonnement) ;
'lookalike' = contrepartie qui copie les 4 premiers et 4 derniers caractères hex d'une vraie contrepartie ; 'fake_token' = jeton hors liste connue
avec symbole d'imitation. Usage : s10_history.py <clé> <adresse> <sortie.csv> [--no-gas]"""
import csv, sys, datetime as dt
sys.path.insert(0, ".")
import ev_lib as E, dln
k, a, outp = sys.argv[1], sys.argv[2].lower(), sys.argv[3]; fetch_gas = "--no-gas" not in sys.argv
REAL = {"0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48": "USDC", "0xdac17f958d2ee523a2206206994597c13d831ec7": "USDT",
        "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2": "WETH", "0x6b175474e89094c44da98b954eedeac495271d0f": "DAI"}
INFERRED = {"0x311ef6b5953ae605dbe469e6566280f0514d3d2e": "MEXC deposit (inféré : gaz du hot wallet MEXC puis vidage vers MEXC)",
            "0x100a38ed14c25a5f456557e9e08298bbb14d4b98": "Stake.com deposit (inféré : gaz du hot wallet Stake puis vidage vers Stake)",
            "0xe1daccdc81b6f18e18b6704e9214b6e03a0fef1c": "KuCoin deposit (inféré : vidages vers KuCoin 3 et hot wallets KuCoin)",
            "0x4978cd7e5a3565cafcc88a105940b0ea01adc04d": "relais b947->b298 (gaz unique de b298, tout renvoyé à b298)"}
FWD = "0x663dc15d3c1ac63ff12e45ab68fea3f0a883c251"
import os
TAKERS = {r["taker"].lower() for r in csv.DictReader(open("../evidence/dln_orders_evm.csv")) if r.get("taker")} if os.path.exists("../evidence/dln_orders_evm.csv") else set()
def tags(o):
    t = [x.get("name", "") for x in ((o.get("metadata") or {}).get("tags") or [])]
    s = ",".join(dict.fromkeys(x for x in t if x)) + ((" ENS:" + o["ens_domain_name"]) if o.get("ens_domain_name") else "")
    return (o.get("name") or "") + ("|" + s if s else "")
def category(addr, lab, is_c):
    L = lab.lower()
    if addr in (dln.DLN_DST, dln.DLN_SRC_EVM, FWD) or "debridge" in L or "bridge" in L: return "bridge"
    if addr in TAKERS: return "bridge_taker"
    if addr in INFERRED and "deposit" in INFERRED[addr].lower(): return "cex_deposit_inferred"
    if "exchange" in L or "hot wallet" in L or "deposit address" in L: return "cex"
    if any(w in L for w in ("liquidity pool", "router", "dex", "uniswap", "sushiswap", "mev", "uniswapx", "solver", "rizzolver")): return "dex"
    if addr == "0x0000000000000000000000000000000000000000": return "mint"
    if is_c: return "contract"
    return "wallet"
T, c1 = E.bs_all(a, "token-transfers"); X, c2 = E.bs_all(a, "transactions"); I, isrc = E.internals(a); c3 = True
assert c1 and c2 and c3
own = {x["hash"]: x for x in X}
signed = {h for h, x in own.items() if x["from"]["hash"].lower() == a}
rows = []
def gas_payer(h):
    if h in own: return own[h]["from"]["hash"].lower()
    return E.rpc("eth_getTransactionByHash", [h])["from"].lower() if fetch_gas else ""
for x in X:
    v = int(x["value"] or 0)
    if v == 0 and x["from"]["hash"].lower() != a: continue
    to = (x.get("to") or {}); out = x["from"]["hash"].lower() == a; cp = to if out else x["from"]
    rows.append(dict(tx_hash=x["hash"], timestamp_utc=x["timestamp"][:19].replace("T", " "), block=x["block_number"], log_index=-1, kind="native_tx" if v else "call",
        **{"from": x["from"]["hash"].lower(), "to": to.get("hash", "").lower()}, asset="ETH" if v else "", token_contract="", amount_raw=v, decimals=18,
        amount=v / 1e18, direction="OUT" if out else "IN", gas_payer=x["from"]["hash"].lower(), method=x.get("method") or "",
        contract_interaction=bool(to.get("is_contract")), status=x.get("status"), counterparty=cp.get("hash", "").lower(), label=tags(cp)))
seen_i = set()
for x in I:
    v = int(x["value"] or 0)
    if v == 0 or not x.get("success", True): continue
    f, t = x["from"]["hash"].lower(), (x.get("to") or {}).get("hash", "").lower()
    if a not in (f, t): continue
    seen_i.add((x["transaction_hash"], f, t, v)); out = f == a; cp = x["to"] if out else x["from"]
    rows.append(dict(tx_hash=x["transaction_hash"], timestamp_utc=x["timestamp"][:19].replace("T", " "), block=x["block_number"], log_index=x.get("index", -1),
        kind="native_internal", **{"from": f, "to": t}, asset="ETH", token_contract="", amount_raw=v, decimals=18, amount=v / 1e18,
        direction="OUT" if out else "IN", gas_payer=gas_payer(x["transaction_hash"]), method="", contract_interaction=True, status="ok",
        counterparty=cp["hash"].lower(), label=tags(cp)))
for x in E.pull(a, "txlistinternal"):  # internes que Blockscout n'a pas
    v = int(x["value"]); key = (x["hash"], x["from"].lower(), x["to"].lower(), v)
    if v == 0 or key in seen_i or x.get("isError") != "0": continue
    out = x["from"].lower() == a
    rows.append(dict(tx_hash=x["hash"], timestamp_utc=dt.datetime.fromtimestamp(int(x["timeStamp"]), dt.timezone.utc).strftime("%Y-%m-%d %H:%M:%S"),
        block=int(x["blockNumber"]), log_index=-1, kind="native_internal", **{"from": x["from"].lower(), "to": x["to"].lower()}, asset="ETH",
        token_contract="", amount_raw=v, decimals=18, amount=v / 1e18, direction="OUT" if out else "IN", gas_payer=gas_payer(x["hash"]), method="",
        contract_interaction=True, status="ok", counterparty=(x["to"] if out else x["from"]).lower(), label="", source_note="routescan"))
for x in T:
    tok = x["token"]; c = tok["address_hash"].lower(); dec = int(tok.get("decimals") or 0); v = int(x["total"].get("value") or x["total"].get("token_id") or 0) if x["total"] else 0
    f, t = x["from"]["hash"].lower(), x["to"]["hash"].lower(); out = f == a; cp = x["to"] if out else x["from"]
    rows.append(dict(tx_hash=x["transaction_hash"], timestamp_utc=x["timestamp"][:19].replace("T", " "), block=x["block_number"], log_index=x["log_index"],
        kind="erc20" if x.get("token_type") == "ERC-20" else x.get("token_type", "token").lower(), **{"from": f, "to": t},
        asset=REAL.get(c, tok.get("symbol") or ""), token_contract=c, amount_raw=v, decimals=dec, amount=v / 10 ** dec if dec else v,
        direction="OUT" if out else "IN", gas_payer=gas_payer(x["transaction_hash"]) if (not out or x["transaction_hash"] in own) else gas_payer(x["transaction_hash"]),
        method=x.get("method") or "", contract_interaction=True, status="ok", counterparty=cp["hash"].lower(), label=tags(cp)))
# drapeaux
genuine = {r["counterparty"] for r in rows if (r["direction"] == "OUT" and r["tx_hash"] in signed and r["amount_raw"]) or (r["direction"] == "IN" and r["amount_raw"] and r["kind"] != "erc20")}
genuine |= {r["counterparty"] for r in rows if r["direction"] == "IN" and r["token_contract"] in REAL and r["amount"] >= 100}
for r in rows:
    fl = []
    cp = r["counterparty"]
    look = cp not in genuine and any(cp != g and cp[:6] == g[:6] and cp[-4:] == g[-4:] for g in genuine)
    fake = r["kind"] == "erc20" and r["token_contract"] not in REAL and any(s in (r["asset"] or "") for s in ("USD", "ꓴ", "Ѕ", "С", "Т"))
    if r["direction"] == "OUT" and r["tx_hash"] not in signed and r["kind"] != "native_internal":
        # sortie tirée par un tiers : empoisonnement si jeton faux ou inconnu, montant nul ou sosie ; sinon swap par intention (UniswapX, Permit2, solveur)
        if fake or not int(r["amount_raw"] or 0) or look or r["token_contract"] not in REAL: fl.append("unsigned_out")
        else: r["method"] = (r["method"] + " " if r["method"] else "") + "executed_by_third_party"
    if look: fl.append("lookalike")
    if fake: fl.append("fake_token")
    r["flags"] = "|".join(fl); r["inferred_label"] = INFERRED.get(cp, "")
    r["category"] = category(cp, (r["label"] or "") + " " + r["inferred_label"], r["contract_interaction"] and r["kind"] == "native_tx")
    r["source"] = r.pop("source_note", None) or "blockscout-v2" + ("+rpc(gas)" if r["gas_payer"] and r["tx_hash"] not in own else "")
    r["wallet"] = k
rows.sort(key=lambda r: (r["block"], r["log_index"]))
cols = ["wallet", "tx_hash", "timestamp_utc", "block", "log_index", "kind", "from", "to", "asset", "token_contract", "amount_raw", "decimals", "amount",
        "direction", "counterparty", "gas_payer", "method", "contract_interaction", "status", "category", "label", "inferred_label", "flags", "source"]
with open(outp, "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore"); w.writeheader(); w.writerows(rows)
clean = [r for r in rows if not r["flags"]]
print(k, "lignes", len(rows), "dont drapées", len(rows) - len(clean), "| tx", len(X), "signées", len(signed), "| jetons", len(T), "| internes", len(I))
