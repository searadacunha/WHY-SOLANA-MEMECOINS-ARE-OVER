"""SOLANA_RETURN_FLOWS.csv : ce que fait Ei5yGz8d de chaque exécution DLN payée par b298 (Ethereum ou Base), sans attribuer
d'office toute dépense aux fonds reçus : pour la première dépense qui suit, borne basse = max(0, dépense - solde avant réception).
Ajoute ses propres ordres DLN sortants, ses virements directs de SOL vers des wallets, et les retours des wallets de vente."""
import csv, json, sys, os, collections
sys.path.insert(0, os.path.dirname(__file__))
import nt_lib as N
R = N.ROOT; W = N.EI5
def rd(p): return list(csv.DictReader(open(p)))
T = rd(R / "data/sol_Ei5yGz8d_txs.csv"); X = collections.defaultdict(list)
for x in rd(R / "data/sol_Ei5yGz8d_transfers.csv"): X[x["sig"]].append(x)
links = {r["dst_tx"]: r for r in rd(R / "CROSSCHAIN_LINKS.csv") if r["dst_chain"] == "solana"}
api_src = {}
for r in rd(N.DEB_RECEIVERS):
    if r["maker"] == W: api_src[r["create_tx"]] = r
for r in rd(N.DEB_ORDERS):
    if r["maker"] == W: api_src.setdefault(r["source_signature"], dict(receiver=r["receiver"], take_chain=r["take_chain"], take_symbol="", take_amount=r["take_amount_raw"], give_symbol="", give_amount=r["give_amount_raw"], order_id=r["order_id_local"]))
SWAP = {"jupiter", "raydium_v4", "raydium_clmm", "meteora_dlmm", "pumpfun", "pumpswap", "orca", "routeUGW", "6m2CDdhR", "SoLFiHG9", "CPMMoo8L", "jup_dca", "jup_limit", "PhoeNiXZ", "obriQD1z"}
def cat(r):
    p = set(r["progs"].split("|"))
    if "dln_src" in p: return "dln_order_out"
    if "dln_dst" in p: return "dln_fill_in"
    if "jup_dca" in p: return "jupiter_dca"
    if p & SWAP: return "swap"
    return "transfer"
def main_token(r):
    tok = json.loads(r["tok"]); tok = {m: v for m, v in tok.items() if m not in ("So11111111111111111111111111111111111111112",)}
    return max(tok, key=lambda m: abs(tok[m])) if tok else ""
OWN = {"FZ7uyvP7KMCMFnUc5kGDRMrXnmUFTCS5shgYzz16yeyi"}  # compte WSOL d'Ei5yGz8d (propriétaire Ei5yGz8d dans les soldes de jetons)
WALLETS = {r["recipient"] for r in rd(R / "data/sol_Ei5yGz8d_recipients.csv") if r["first_funder"] and r["recipient"] not in OWN}
rows = []; bal = 0; prev = []
idx = {r["sig"]: i for i, r in enumerate(T)}
cum = []
for r in T:
    bal += int(r["sol"]); cum.append(bal)
for i, r in enumerate(T):
    if r["sig"] in links:
        L = links[r["sig"]]; before = cum[i] - int(r["sol"])
        thr = max(10 ** 7, int(r["sol"]) // 20)  # dépense significative : au moins 0,01 SOL et 5 % du montant reçu
        nxt = [(j, T[j]) for j in range(i + 1, min(i + 40, len(T))) if T[j]["signer"] == W and -int(T[j]["sol"]) >= thr][:3]
        uses = []
        for k, (j, u) in enumerate(nxt):
            spent = -int(u["sol"])
            uses.append(f"{u['ts']} {cat(u)} -{spent / 1e9:.4f} SOL {main_token(u)} {u['sig']}")
        first = nxt[0][1] if nxt else None
        lo = max(0, -int(first["sol"]) - max(0, before)) if first else 0
        rows.append(dict(kind="fill_from_b298", utc=r["ts"], sig=r["sig"], src_chain=L["src_chain"], src_tx=L["src_tx"], orderId=L["orderId"],
                         sol_in=int(r["sol"]) / 1e9, usdc_in=json.loads(r["tok"]).get("EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v", 0) / 1e6,
                         sol_balance_before=before / 1e9, first_use_category=cat(first) if first else "", first_use_sig=first["sig"] if first else "",
                         first_use_utc=first["ts"] if first else "", first_use_token=main_token(first) if first else "",
                         first_use_sol=-int(first["sol"]) / 1e9 if first else "", first_use_from_fill_min=lo / 1e9, next_uses=" | ".join(uses)))
    if cat(r) == "dln_order_out" and r["signer"] == W:
        a = api_src.get(r["sig"], {})
        rows.append(dict(kind="ei5_dln_order_out", utc=r["ts"], sig=r["sig"], sol_in=int(r["sol"]) / 1e9, usdc_in=json.loads(r["tok"]).get("EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v", 0) / 1e6,
                         orderId=a.get("order_id", ""), dst_chain=a.get("take_chain", ""), receiver=a.get("receiver", ""),
                         note=("TX ÉCHOUÉE, refaite ensuite ; " if r["err"] == "True" else "") + (f"{a.get('give_symbol', '')} {a.get('give_amount', '')} -> {a.get('take_symbol', '')} {a.get('take_amount', '')} (index deBridge)" if a else "ordre absent de l'index local")))
    for x in X.get(r["sig"], []):
        # seuil 0,01 SOL : celui de 0,1 omettait 2aeEoq5n (premier SOL, 0,0258) et deux envois de 0,05 à E72DuqDL
        if x["asset"] == "SOL" and not x.get("tag") and int(x["raw"]) >= 10 ** 7 and x["frm"] == W and x["to"] in WALLETS and cat(r) == "transfer":  # pas les commissions dans les échanges
            rows.append(dict(kind="ei5_sol_to_wallet", utc=r["ts"], sig=r["sig"], sol_in=-int(x["raw"]) / 1e9, receiver=x["to"]))
        if x["asset"] == "SOL" and x["to"] == W and x["frm"] in ("8kNKNiHKjbCPjaWGjoEEWeQ6X4jkZn2sDV7tz7azfL4t", "BdX9J5pQZ9SoH7PqwDCiiQ2rzaMiT4D9WZ8C1DiwXgyX"):
            rows.append(dict(kind="sale_wallet_return", utc=r["ts"], sig=r["sig"], sol_in=int(x["raw"]) / 1e9, receiver=W, note=f"retour de {x['frm']} après vente de DMAGA"))
fields = ["kind", "utc", "sig", "src_chain", "src_tx", "orderId", "sol_in", "usdc_in", "sol_balance_before", "first_use_category", "first_use_utc", "first_use_sig",
          "first_use_token", "first_use_sol", "first_use_from_fill_min", "dst_chain", "receiver", "note", "next_uses"]
N.write_csv(R / "SOLANA_RETURN_FLOWS.csv", rows, fields)
c = collections.Counter(r["kind"] for r in rows); print(c)
f = [r for r in rows if r["kind"] == "fill_from_b298"]
print("fills", len(f), "SOL", round(sum(r["sol_in"] for r in f), 6), "USDC", round(sum(r["usdc_in"] for r in f), 6))
print(collections.Counter(r["first_use_category"] for r in f))
