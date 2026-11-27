"""KEKIUS Ethereum : achats, ventes et résultat en ETH par wallet, du lancement au 04/01/2025 00:00 UTC.

Par transaction : delta net de KEKIUS par adresse (hors pools, contrat du jeton qui encaisse la taxe, collecteur de frais
Uniswap, routeurs). Delta net de WETH des pools = ETH payé (achat) ou reçu (vente). Une tx avec un seul receveur net (ou un
seul vendeur net) reçoit tout le montant WETH ; sinon la tx est marquée ambiguë et son WETH n'est pas attribué."""
import csv, gzip
from collections import defaultdict
from k_lib import DATA, ETH_KEKIUS

POOLS = {"0xfff8d5fff6ee3226fa2f5d7d5d8c3ff785be9c74", "0xa2542303c9a01c011da9106128d9b0838e6c3e57"}
NOT_OWNERS = POOLS | {ETH_KEKIUS, "0x0000000000000000000000000000000000000000",
                      "0x000000fee13a103a10d593b9ae06b3e05f2e7e1c",  # FeeCollector (Uniswap)
                      "0x3fc91a3afd70395cd496c647d5a6cc9d4b2b7fad",  # Universal Router
                      "0x1111111254eeb25477b68fb85ed929f73a960582",  # 1inch v5
                      "0x70bf6634ee8cb27d04478f184b9b8bb13e5f4710",  # 0x MainnetSettler
                      "0x22f9dcf4647084d6c31b2765f6910cd85c178c18",  # 0x FlashWallet
                      "0x74de5d4fcbf63e00296fd95d33236b9794016631"}  # MetaMask Spender


def load():
    tok = defaultdict(lambda: defaultdict(int))
    meta = {}
    for r in csv.DictReader(gzip.open(DATA / "eth_kekius_transfers.csv.gz", "rt")):
        v = int(r["raw"])
        tok[r["tx"]][r["from"]] -= v
        tok[r["tx"]][r["to"]] += v
        meta.setdefault(r["tx"], (int(r["block"]), int(r["time"]), int(r["tx_index"])))
    weth = defaultdict(int)  # >0 : WETH entré dans les pools (achat)
    for r in csv.DictReader(gzip.open(DATA / "eth_kekius_pool_weth.csv.gz", "rt")):
        v = int(r["raw"])
        if r["to"] in POOLS:
            weth[r["tx"]] += v
        if r["from"] in POOLS:
            weth[r["tx"]] -= v
    return tok, meta, weth


def ledger():
    tok, meta, weth = load()
    rows, amb = [], 0
    for tx, d in tok.items():
        own = {a: v for a, v in d.items() if v and a not in NOT_OWNERS}
        pos = [a for a, v in own.items() if v > 0]
        neg = [a for a, v in own.items() if v < 0]
        w = weth.get(tx, 0)
        b, t, i = meta[tx]
        for a, v in own.items():
            eth = 0
            if w > 0 and v > 0 and len(pos) == 1:
                eth = -w
            elif w < 0 and v < 0 and len(neg) == 1:
                eth = -w
            elif w and ((w > 0 and v > 0) or (w < 0 and v < 0)):
                amb += 1
            rows.append({"tx": tx, "block": b, "time": t, "tx_index": i, "owner": a, "kekius_raw": v, "eth_wei": eth,
                         "kind": ("buy" if w > 0 else "transfer_in") if v > 0 else ("sell" if w < 0 else "transfer_out")})
    rows.sort(key=lambda r: (r["block"], r["tx_index"]))
    return rows, amb


if __name__ == "__main__":
    rows, amb = ledger()
    agg = defaultdict(lambda: {"bought": 0, "sold": 0, "eth_in": 0, "eth_out": 0, "net": 0, "first_buy": None, "first_buy_tx": "", "n_buys": 0, "n_sells": 0})
    for r in rows:
        g = agg[r["owner"]]
        g["net"] += r["kekius_raw"]
        if r["kind"] == "buy":
            g["bought"] += r["kekius_raw"]; g["eth_in"] += -r["eth_wei"]; g["n_buys"] += 1
            if g["first_buy"] is None:
                g["first_buy"], g["first_buy_tx"] = r["time"], r["tx"]
        elif r["kind"] == "sell":
            g["sold"] += -r["kekius_raw"]; g["eth_out"] += r["eth_wei"]; g["n_sells"] += 1
    with gzip.open(DATA / "eth_kekius_ledger.csv.gz", "wt", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
    with open(DATA / "eth_kekius_wallets.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["owner", "first_buy_utc", "first_buy_tx", "n_buys", "n_sells", "bought_M", "sold_M", "eth_spent", "eth_received", "realized_eth", "residual_M"])
        for a, g in sorted(agg.items(), key=lambda x: -(x[1]["eth_out"] - x[1]["eth_in"])):
            from k_lib import utc
            w.writerow([a, utc(g["first_buy"]) if g["first_buy"] else "", g["first_buy_tx"], g["n_buys"], g["n_sells"],
                        round(g["bought"] / 1e15, 6), round(g["sold"] / 1e15, 6), round(g["eth_in"] / 1e18, 6),
                        round(g["eth_out"] / 1e18, 6), round((g["eth_out"] - g["eth_in"]) / 1e18, 6), round(g["net"] / 1e15, 6)])
    print("lignes", len(rows), "wallets", len(agg), "lignes WETH ambiguës", amb)
