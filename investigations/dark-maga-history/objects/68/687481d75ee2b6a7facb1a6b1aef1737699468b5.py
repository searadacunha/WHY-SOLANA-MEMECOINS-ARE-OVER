"""Autocontrôle hors ligne des constats clés : relit le cache brut (réseau interdit) et les CSV produits. Chaque assert = un constat de FINDINGS.md.
Lancer : /opt/homebrew/bin/python3.12 -I s99_selfcheck.py"""
import csv, json, sys, urllib.request
sys.path.insert(0, ".")
def _no_net(*a, **k): raise RuntimeError("réseau interdit pendant l'autocontrôle")
urllib.request.urlopen = _no_net
import os
os.environ.setdefault("EV_RAW", os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "evidence", "selfcheck_cache"))  # 9 reçus suffisent
import ev_lib as E, dln
B947, B298, RELAY = "0xb947bf7f409e998b28f8e218802fc9575c3c8c57", "0xb29826d809aa04d2ead6f2310d8965a45b87fa67", "0x4978cd7e5a3565cafcc88a105940b0ea01adc04d"
ok = []
def check(name, cond):
    assert cond, name; ok.append(name)
# 1. 120 957,888072 USDC : ordre DLN de GZXKYzwZ ; contrôle positif sur l'ordre test de Gcyg2jeL
f = dln.fills_in_receipt(E.rpc("eth_getTransactionReceipt", ["0x47e8da75f698f8c40419230c2274136c57666b92a91bef55c481e63a91758e14"]))[0]
check("F1 maker du 120957", f["makerSrc"] == "GZXKYzwZPgWH8TwyY9f8dkCQ9EKK6nrPZADGcEwfAg7Y" and f["takeAmount"] == 120957888072 and f["receiverDst"] == B947
      and f["giveChain"] == "solana" and f["giveAmount"] == 121013214273 and f["orderId"] == "0xc65ba1fa1b9d14301b5b0acaf159a5fd955a18899e4256a7604fd0af1f27a225")
c = dln.fills_in_receipt(E.rpc("eth_getTransactionReceipt", ["0xdb07ade91b6ed02470a9283a346f7062ba45dbb65ea5030763dd1150b78d8b3d"]))[0]
check("F1 contrôle positif Gcyg2jeL", c["makerSrc"] == "Gcyg2jeLfSY9gxxHf5za5QU74ijtxBb1dB2mdGSPZH3m" and c["takeAmount"] == 9992001)
# 2. côté Solana : l'ordre est créé par GZXKYzwZ (programme DLN source, -121 061,638928 USDC)
g = {r["signature"]: r for r in csv.DictReader(open("../evidence/s20_gzx_ledger.csv"))}
o = g["2SesFSiWhezf6a2RVvkRLua5obwjtBet5yaVFHooxnxubLsras6FKN4dkgHjVrSJrHa3Rwnc45uRnf7AiWRmiB8c"]
check("F1 création Solana", o["dln_src"] == "True" and int(o["usdc_delta_raw"]) == -121061638928 and o["fee_payer"] == "GZXKYzwZPgWH8TwyY9f8dkCQ9EKK6nrPZADGcEwfAg7Y")
# 3. GZXKYzwZ : 9 envois de DMAGA en 100 s, financé et vidé par Ei5yGz8d
E5 = "Ei5yGz8dPndr1aCeHZsfqJBcS3VBbz75VHEhxxJKLy3V"
ins = [r for r in g.values() if "2024-07-26 05:40:37" <= r["utc"] <= "2024-07-26 05:42:17" and int(r["dmaga_delta_raw"]) > 0]
check("F2 neuf envois en 100 s", len(ins) == 9 and sum(int(r["dmaga_delta_raw"]) for r in ins) == 29295679868145)
first = sorted(g.values(), key=lambda r: r["slot"])[:2]
check("F2 créé par Ei5yGz8d", all(r["fee_payer"] == E5 for r in first) and int(first[1]["sol_delta_lamports"]) == 500000000)
back = [r for r in g.values() if r["fee_payer"].startswith("GZXK") and E5 in r["counterparties"] and (int(r["dmaga_delta_raw"]) < 0 or int(r["sol_delta_lamports"]) < -100_000_000)]
check("F2 restes rendus à Ei5yGz8d", len(back) >= 2)
# 4. wallets de parking : gaz d'Ei5yGz8d le 22/07, SOL rendu à Ei5yGz8d le 29/07 entre 21:06:09 et 21:06:58
for w in ("EMucoi7y", "38p6SEUo", "8ScA8t7Q", "EMYihQ4k", "5nxBz7Y9"):
    L = list(csv.DictReader(open(f"../evidence/s21_{w}_ledger.csv")))
    gas = [r for r in L if r["fee_payer"] == E5 and int(r["sol_delta_lamports"]) >= 1_000_000_000]
    swp = [r for r in L if "2024-07-29 21:06:09" <= r["utc"] <= "2024-07-29 21:06:58" and int(r["sol_delta_lamports"]) < 0 and E5 in r["counterparties"]]
    check(f"F2 parking {w}", len(gas) == 1 and gas[0]["utc"].startswith("2024-07-22 17:") and len(swp) == 1)
# 5. b947 : gaz 100 % de b298 ; sessions de 2023 à somme exacte ; vidage complet du 01/10/2024
m = json.load(open("../evidence/s40_metrics.json"))
check("F3 gaz b947 = b298", m["b947_eth_in_total"] == m["b947_eth_in_from_b298"] and len(m["b947_eth_topups"]) == 5)
check("F3 cinq sessions exactes", sum(1 for s in m["usdc_sessions"] if s["exact"] and s["out_utc"] < "2023-03-01") == 5)
H = [r for r in csv.DictReader(open("../b947_full_history.csv")) if r["asset"] == "USDC" and (not r["flags"] or r["flags"] == "lookalike")]
bal = sum(int(r["amount_raw"]) * (1 if r["direction"] == "IN" else -1) for r in H)
check("F3 solde USDC b947 final 0,012", bal == 12000)
R = [r for r in csv.DictReader(open("../evidence/relay_4978_history.csv")) if r["asset"] == "USDC" and not r["flags"]]
check("F3 relais : tout vers b298", sum(int(r["amount_raw"]) for r in R if r["direction"] == "OUT" and r["counterparty"] == B298) == 434291334945
      and all(r["counterparty"] == B298 for r in R if r["direction"] == "OUT"))
RE = [r for r in csv.DictReader(open("../evidence/relay_4978_history.csv")) if r["asset"] == "ETH" and r["direction"] == "IN"]
check("F3 relais gazé par b298 seul", len(RE) == 1 and RE[0]["counterparty"] == B298)
# 6. aller-retour b298 -> Ei5yGz8d : 24 ordres vers Solana retrouvés au montant exact côté Solana
V = list(csv.DictReader(open("../evidence/s22_sol_fills_check.csv")))
check("F4 24/24 exécutions Solana", len(V) == 24 and all(r["status"] == "VERIFIED" for r in V) and sum(r["receiver"] == E5 for r in V) == 22)
# 7. dépôt MEXC inféré 0x311ef6b5 : les 6 fills deBridge reçus ont tous b298 pour maker
D = [r for r in csv.DictReader(open("../evidence/dln_orders_evm.csv"))]
check("F5 b298 vers lui-même sur Base (13) et BSC (1)", sum(1 for r in D if r["wallet"] == "b298" and r["direction"] == "OUT" and r["take_chain"] in ("base", "bsc") and r["receiver"] == B298) == 14)
MEXC = "0x311ef6b5953ae605dbe469e6566280f0514d3d2e"
for h in ("0x2ca633568bcc00c6d1bc8e32468b665d0293cf95ab07b1fa15d3e247a7e3479e", "0x0e1bfd346a85d504b655c2bee6bb4c66708dbb9d5bdf047e9d0f843336c688f4",
          "0x9b7af51ca255c6c344ad12623aa7ce6b3072d2979590790d6982bdd7bcc42095", "0x62d802cafd03512a17068fe15338975d87d05c43edc6b529f1f4c47848e452d5",
          "0x477507a39346d0dca314db619efe27f2ad2b9f1efbc2295681f828a8ad01bdb6", "0x309a755e0fccfe2e4a797f46ef4c911643df7a2eec8b9114e42753c394ea3007"):
    o = dln.fills_in_receipt(E.rpc("eth_getTransactionReceipt", [h]))[0]
    check(f"F5 fill {h[:10]} : maker b298 Base -> dépôt MEXC inféré", o["makerSrc"] == B298 and o["receiverDst"] == MEXC and o["giveChain"] == "base")
# 8. bornes : autocohérentes
Bd = list(csv.DictReader(open("../evidence/s51_b298_usdc_bounds.csv")))
check("F6 bornes basse <= haute", all(float(r["from_b947_min"]) <= float(r["from_b947_max"]) for r in Bd))
# 9. 2d86 : l'ETH des fills de C73Yv9iH repart en moins de 2 min vers coin-etf.eth ; aucune contrepartie non-service commune avec la branche b298
CE = "0xebc71f680a785314c413baaa9722a9f85bb3316e"
X = {r["tx_hash"]: r for r in csv.DictReader(open("../evidence/2d86_full_history.csv")) if r["counterparty"] == CE and r["direction"] == "OUT"}
for fill, sent, eth in (("0x918e6057259537876e62dd4c15cdaf5594bb404c1dfc01e6b2666448a60c4986", "0x9dd2f67e88e71ffc5aba78fa3accf4e23996130e1022681de0b6a44e8212b729", 10.0),):
    check("F7 fill C73Yv9iH -> 2d86 puis 10 ETH vers coin-etf.eth", dln.fills_in_receipt(E.rpc("eth_getTransactionReceipt", [fill]))[0]["makerSrc"] == "C73Yv9iHmTaf8SU2XFnGLt7QXUDqbeWNtUYza9WJhkae"
          and float(X[sent]["amount"]) == eth)
Sh = list(csv.DictReader(open("../evm_shared_counterparties.csv")))
Xw, Yw = {"2d86", "86f9"}, {"b947", "b298", "relay_4978"}
check("F7 branches séparées", not any(set(r["wallets_connected"].split("|")) & Xw and set(r["wallets_connected"].split("|")) & Yw and r["excluded_as_service_hub"] == "False" for r in Sh))
# 10. chiffres clés cités dans FINDINGS.md, recalculés depuis les CSV
b2e = [r for r in D if r["wallet"] == "b298" and r["direction"] == "OUT" and r["receiver"] == E5]
check("F8 b298 -> Ei5yGz8d : 22 ordres, 299 800,36 USDC et 34,1399 ETH cédés, 1 753,732 SOL reçus", len(b2e) == 22
      and round(sum(int(r["give_amount_raw"]) for r in b2e if r["give_token"].startswith("0xa0b8")) / 1e6, 2) == 299800.36
      and round(sum(int(r["give_amount_raw"]) for r in b2e if r["give_token"].startswith("0x0000")) / 1e18, 4) == 34.1399
      and round(sum(int(r["take_amount_raw"]) for r in b2e if r["take_token"].startswith("1111")) / 1e9, 3) == 1753.732)
e2b = [r for r in D if r["wallet"] == "b298" and r["direction"] == "IN" and r["maker"] == E5]
check("F8 Ei5yGz8d -> b298 sur Ethereum : 8 ordres, 151 300,22 USDC", len(e2b) == 8 and round(sum(int(r["give_amount_raw"]) for r in e2b) / 1e6, 2) == 151300.22)
lo = lambda pred: round(sum(float(r["from_b947_min"]) for r in Bd if pred(r)), 2)
check("F8 bornes basses Base 124 233,75 / BSC 99 981,82 / ventes ETH 247 663,99",
      lo(lambda r: r["dln_dest"].startswith("base:" + B298)) == 124233.75 and lo(lambda r: r["dln_dest"].startswith("bsc:" + B298)) == 99981.82
      and lo(lambda r: r["counterparty"] in ("0x43ee35d5542f5b826fa92832bd97caff153675a8", "0xbcc66fc7402daa98f5764057f95ac66b9391cd6b", "0x225a38bc71102999dd13478bfabd7c4d53f2dc17")) == 247663.99)
CEr = [r for r in csv.DictReader(open("../evidence/2d86_full_history.csv")) if r["counterparty"] == CE and r["kind"] == "native_tx" and not r["flags"]]
check("F8 2d86 <-> coin-etf.eth : 425 envois 1 338,64 ETH, 287 retours 1 298,53 ETH",
      sum(r["direction"] == "OUT" for r in CEr) == 425 and round(sum(float(r["amount"]) for r in CEr if r["direction"] == "OUT"), 2) == 1338.64
      and sum(r["direction"] == "IN" for r in CEr) == 287 and round(sum(float(r["amount"]) for r in CEr if r["direction"] == "IN"), 2) == 1298.53)
print(len(ok), "contrôles OK :", "; ".join(ok))
