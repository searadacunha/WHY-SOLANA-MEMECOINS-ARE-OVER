"""Tables publiées : WALLET_OVERLAP.csv, FUNDING_GRAPH.csv, CROSSCHAIN_FLOWS.csv.

Les lignes viennent des reçus figés, des CSV de data/ et des classements écrits ci-dessous (chaque classement cite sa
preuve). k18 ajoute ensuite les lignes du test ATA de l'univers DMAGA (data/ata_overlap.csv), si le fichier existe."""
import csv, json
from k_lib import INV, DATA, EVID, utc
from k11_parse import sol_deltas, signers

OV = ["token", "chain", "kekius_side_address", "dmaga_side_address", "level", "relation", "tx_or_signature", "utc",
      "asset_amount", "method", "status", "interpretation", "source"]
ov = []
EVM_CITED = {  # adresse : (nature vérifiée, source de l'étiquette)
    "0x555ce236c0220695b68341bc48c68d52210cc35b": "solveur DLN (taker deBridge), service",
    "0xfbeedcfe378866dab6abbafd8b2986f5c1768737": "bot MEV (étiquette Blockscout « MEV Bot: 0xfbe…737 », 911 346 tx)",
    "0x00000000009e50a7ddb7a7b0e2ee6604fd120e49": "contrat de bot MEV (préfixe 0x00000000, contrepartie interne de 2d86)",
    "0x9642b23ed1e01df1092b92641051881a322f5d4e": "portefeuille chaud MEXC 21 (étiquette OLI)",
    "0xf2614a233c7c3e7f08b1f887ba133a13f1eb2c55": "Sushi RouteProcessor5, routeur",
    "0x8526e4f21d060ef0ef2e69d2a00392e82eefa63d": "contrepartie d'un transfert NFT vers 2d86 (2023), non personnelle à DMAGA",
    "0xf081470f5c6fbccf48cc4e5b82dd926409dcdd67": "contrepartie de jetons de 2d86 (2024)",
    "0xcf5540fffcdc3d510b18bfca6d2b9987b0772559": "contrepartie de 2d86 (2026)",
    "0x2052051a0474fb0b98283b3f38c13b0b0b6a3677": "contrepartie de 2d86 (2026)",
}
for a, why in EVM_CITED.items():
    ov.append(["KEKIUS-ETH", "ethereum", a, a, "A", "même adresse, citée par les enquêtes deBridge", "", "", "", "intersection d'adresses",
               "REJETÉ", why, "data/eth_kekius_wallets.csv ; investigations/2026-11-05_evm-recipient-deeptrace"])
SOL_FIRST100 = {
    "CaShxDq2Vbdp2XryjDdUZthbTzwYsvKuH6Knn9pPi4xU": ("XC", "bot d'arbitrage : achat DMAGA de 0,0002 SOL 13 s après la migration, « financé » par l'autorité Raydium"),
    "DQeJQ91Uzcuyk4iAtpQ9FwD8Ddwr62NeWd8hoE1kgLLs": ("XC", "bot d'arbitrage, même geste ; finance ATomG2gR en janvier 2024"),
    "ATomG2gRJcB2jNvwcjo2zBMoyLsHZzLgwqy651zzYoCq": ("XC", "bot d'arbitrage, même geste"),
    "CH7MJuK5Kh2e7cribybdQLPzSxLqL4AgWwKZgaNoHA7J": ("XC", "hub ou bot : 8 639 virements vers 88 wallets, 104 achats DMAGA, 3 461 tx KM"),
    "D2vZhPW1mtZDcB1yxiErebPcsYBvsCKrieYGWkcSVxp6": ("XC", "payeur de CH7MJuK5 (5 530 SOL), hub"),
    "GTvBQnRvAPweU2qmYg8MDLND2PAAyYFKe35aKQGMRDaL": ("KM", "trader DMAGA tardif (1er achat 05/11/2024)"),
    "xK5mDD8DfHL1ERQ9T91yCWtQzGqFZMe2ZGnbnBi6eDj": ("KM", "trader DMAGA tardif (05/11/2024)"),
    "8J9panvq2ULV7ueK5gBTJXm9dxvW1uHyh2189xLUY1V7": ("KM", "trader DMAGA tardif (06/11/2024)"),
    "DSVc1Rd69sLcXBoZAsvkzK4jGFyJKP77K3J2CaFVNAFP": ("KM", "trader DMAGA après le changement de photo (23/07/2024)"),
    "7wYSQEU1iNt2oETyYEWfPU9HUf6eL13SiMKQ2XPs9ke4": ("KM", "trader DMAGA après le changement de photo (22/07/2024)"),
    "FxSuDZSxfouRxKH8LqGUHaecvQTrUNUvh9hk3HRAXiGa": ("KM", "trader DMAGA tardif (13/02/2025)"),
    "2Cjtrc39CufRWH8uEPzANfsEDvsESbej6NiixXMLbeaL": ("KM", "trader DMAGA tardif (08/10/2024)"),
    "8EeQnwzkbveShuZXX4fymcHBhsE2YieDkeRmyc5RcCqX": ("KM", "trader DMAGA tardif (25/10/2024)"),
}
for a, (tk, why) in SOL_FIRST100.items():
    st = "REJETÉ" if ("bot" in why or "hub" in why) else "CONFIRMÉ"
    ov.append([tk, "solana", a, a, "A", "même adresse : 100 premiers acheteurs Kekius et wallets DMAGA", "", "", "",
               "intersection d'adresses", st, why + ("" if st == "REJETÉ" else " ; non discriminant"),
               f"data/sol_first100_buyers_{tk}.csv ; wallets.parquet de l'enquête d'origine"])
ov.append(["XC", "solana", "DQmMnakiKr1YNE2gcpggLCzBrauBwFbQkAaao2FTbjgp", "FJkb8WnWocfuQYj4v4vg5VpZoST3LebjQk8WpuD7VbgC", "A",
           "financement direct du wallet DMAGA par l'acheteur XC78 ; même programme de sniping 9NLjj4Gj…",
           "4dChb1EMrLFYNpDx9iWAtKzXde1VeGoxGF6LQ8kTDpE6FX8WMrFr7y2VYTJyqbtoJM1sY4yKxoDMs24Nu1EgiAyV", "2024-07-11 13:10:39",
           "SOL 1.474847595 (+ 1 SOL le 10/07, 3kXEwKY5…)", "transfert système signé par DQmMnaki", "CONFIRMÉ",
           "même opérateur de bot de sniping de migration (CORROBORÉ) ; non discriminant pour la question Musk",
           "evidence/receipts ; FINDINGS §6"])
for r in (csv.DictReader(open(DATA / "ata_overlap.csv")) if (DATA / "ata_overlap.csv").exists() else []):
    ov.append([r[k] for k in OV])
with open(INV / "WALLET_OVERLAP.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(OV); w.writerows(ov)

FG = ["src", "dst", "chain", "asset", "amount", "utc", "tx_or_signature", "nature", "status", "traceability", "source"]
fg = []
rec = lambda s: json.loads((EVID / "receipts" / f"{s}.json").read_text())
sell = "5GvjoEMEiPfjqnck7iegRCGuKUrtfe1amJYvvR6D7WxrcPWA19peM163vuEQuorCZDFpYHmknUJ5TDSnPxHfYBxn"
t = rec(sell)
for a, v in sol_deltas(t).items():
    if v == 6_655_700_950:
        fg.append(["Go5rFkwKpTYGVck7emf4Uop81HBozmHHZfEhe2zJDY5u", a, "solana", "SOL", "6.65570095", utc(t["blockTime"]), sell,
                   "produit de la vente de Go5 versé dans sa propre tx (signataire unique), puis rachat co-signé au même slot",
                   "CONFIRMÉ", "directe", "evidence/receipts ; FINDINGS §4"])
for s, amt in [("3kXEwKY5A9Givucjcd59n77qRWwoj4J8sgBPTtxMm8Ey5SLVGuAACFhuU2nueM6gBB2iwT6wFYXAPV9nceQLsxvn", "1.0"),
               ("4dChb1EMrLFYNpDx9iWAtKzXde1VeGoxGF6LQ8kTDpE6FX8WMrFr7y2VYTJyqbtoJM1sY4yKxoDMs24Nu1EgiAyV", "1.474847595")]:
    t = rec(s)
    fg.append(["DQmMnakiKr1YNE2gcpggLCzBrauBwFbQkAaao2FTbjgp", "FJkb8WnWocfuQYj4v4vg5VpZoST3LebjQk8WpuD7VbgC", "solana", "SOL", amt,
               utc(t["blockTime"]), s, "transfert système, avant l'achat DMAGA de FJkb8WnW (14/07/2024 02:15:33)", "CONFIRMÉ", "directe",
               "evidence/receipts ; FINDINGS §6"])
OPS = "3oqARBNDr56L2oWQ9aR2QzS7FeTMEubd8J2v29wP5N58"
idx = json.loads((EVID / "receipts" / "INDEX.json").read_text())
for sig, why in idx.items():
    if "3oqARBND" not in why:
        continue
    t = rec(sig)
    sd = sol_deltas(t)
    payers = [a for a, v in sd.items() if v < 0 and a in signers(t)]
    for dst, v in sd.items():
        if v <= 0 or dst in payers or v < 10**8:
            continue
        nat = "frais prélevés à un taux presque constant (6,957 % et 6,961 % du montant reçu par 3oqARBND) : service probable" if dst.startswith("C6UEzXJc") else why
        fg.append(["+".join(payers), dst, "solana", "SOL", repr(v / 1e9), utc(t["blockTime"]), sig, nat, "CONFIRMÉ",
                   "rompue en amont : FBwXQAEb non étiqueté, plus de 2 000 tx en 12 jours" if dst == OPS and "FBwXQAEb" in why else "directe",
                   "evidence/receipts ; FINDINGS §4"])
EVM = [  # (src, dst, tx, nature, traçabilité) : montant et heure relus dans data/eth_history ou evidence/blockscout_*.json
    ("0x016606acc6b0cfe537acc221e3bf1bb44b4049ee", "0xaa4f58e9aafd36b4b6446f6dc417c02908641a7c", "0x771dc8d4f1907a3eef0e674f975bb6815de648c30f7889f086f97395c8fdad7a", "seul financement du créateur du KEKIUS Ethereum", "rompue : portefeuille chaud ChangeHero"),
    ("0x98db3a41bf8bf4ded2c92a84ec0705689ddeef8b", "0x33a57f4e88c9ceb0788eb41a407e51533d70cc4d", "0x82644cf71a54d3b0984ccd08444589198afcd3ef5fc7fa24698966e546ec043e", "premier apport", "rompue : Ramp Network (rampe fiat)"),
    ("0x4976a4a02f38326660d17bf34b431dc6e2eb2327", "0x33a57f4e88c9ceb0788eb41a407e51533d70cc4d", "0x981fcbcd0ab285100da08f5618a3456dc409f9a1e978f0164779f5598149ced2", "apport", "rompue : portefeuille chaud Binance"),
    ("0xdfd5293d8e347dfe59e90efd55b2956a1343963d", "0x33a57f4e88c9ceb0788eb41a407e51533d70cc4d", "0xa7131b0f3a4519aa8d1a8ac0bb1c3836d380ca875f2c92f033982488672e8b69", "apport", "rompue : portefeuille chaud Binance"),
    ("0x28c6c06298d514db089934071355e5743bf21d60", "0x33a57f4e88c9ceb0788eb41a407e51533d70cc4d", "0x5688e1ff53a6c8631d8f88a06e2aa0508dc8bbfbd2fc9c8cf06c92af35f900bd", "apport", "rompue : portefeuille chaud Binance"),
    ("0x4976a4a02f38326660d17bf34b431dc6e2eb2327", "0x33a57f4e88c9ceb0788eb41a407e51533d70cc4d", "0xfd022f83d19e47ceb3edbb49c64e1dab73fd8304bb976bb610bd6bc1c7ef6c97", "apport", "rompue : portefeuille chaud Binance"),
    ("0x21a31ee1afc51d94c2efccaa2092ad1028285549", "0x33a57f4e88c9ceb0788eb41a407e51533d70cc4d", "0x977064d942db88f25107e34f614b16fc57c13422892916fda92d5a5f3d593854", "apport", "rompue : portefeuille chaud Binance"),
    ("0x4976a4a02f38326660d17bf34b431dc6e2eb2327", "0x33a57f4e88c9ceb0788eb41a407e51533d70cc4d", "0xccd87d536b0311fea7d8e55737d163ff3b02f847269c8b18222220ef925c7fe6", "apport", "rompue : portefeuille chaud Binance"),
    ("0x9696f59e4d72e237be84ffd425dcad154bf96976", "0x33a57f4e88c9ceb0788eb41a407e51533d70cc4d", "0x94943c6ed33c3b8b4c75a5c77fc337ecd9aeee8fcce477e71b20c8a19abe1e6e", "apport", "rompue : portefeuille chaud Binance"),
    ("0x33a57f4e88c9ceb0788eb41a407e51533d70cc4d", "0xecaa5a79369f147015a6c6f28ab4479f68994a8d", "0xac5d86b6ee10a92a0fc5fb3656004ab6a02350dcc2cbecb4723fc056514c44c7", "sortie après les ventes KEKIUS", "vers une adresse de dépôt Binance inférée"),
    ("0x33a57f4e88c9ceb0788eb41a407e51533d70cc4d", "0xecaa5a79369f147015a6c6f28ab4479f68994a8d", "0xf092475df073c30c93c005bf40ffb9ac58239bf15aad7da07aac86746bfda930", "sortie après les ventes KEKIUS", "vers une adresse de dépôt Binance inférée"),
    ("0xecaa5a79369f147015a6c6f28ab4479f68994a8d", "0x28c6c06298d514db089934071355e5743bf21d60", "0x2e63bc8547695b4a19ef267e7bd937c0eaaf9a2ee5b2137e4b96dfbeafd01ea3", "transfert vers Binance (comportement d'adresse de dépôt)", "rompue : exchange"),
    ("0xecaa5a79369f147015a6c6f28ab4479f68994a8d", "0x28c6c06298d514db089934071355e5743bf21d60", "0xd902cd0c999339c25e4ea1e7a90fc3c4e392ceaaf5f65ac7e975613de351155b", "transfert vers Binance (comportement d'adresse de dépôt)", "rompue : exchange"),
]
hist = {}
for f in (DATA / "eth_history").glob("*.csv"):
    for r in csv.DictReader(open(f)):
        if r["kind"] == "tx":
            hist[r["tx"]] = (r["amount"], r["time_utc"])
for x in json.loads((EVID / "blockscout_0xecaa5a79_outgoing.json").read_text())["items"]:
    hist.setdefault(x["hash"].lower(), (repr(int(x["value"]) / 1e18), x["timestamp"][:19].replace("T", " ")))
for s, d, tx, nat, tr in EVM:
    amt, t = hist[tx]
    fg.append([s, d, "ethereum", "ETH", amt, t, tx, nat, "CONFIRMÉ", tr, "data/eth_history ; evidence/blockscout_0xecaa5a79_outgoing.json ; étiquettes metadata.services.blockscout.com"])
with open(INV / "FUNDING_GRAPH.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(FG); w.writerows(fg)

CC = ["src_chain", "src_address", "dst_chain", "dst_address", "bridge", "order_id_or_tx", "utc", "amount", "status", "note"]
with open(INV / "CROSSCHAIN_FLOWS.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(CC)
    w.writerow(["ethereum", "b947, b298, 86f9, 2d86, relais 0x4978cd7e", "ethereum", "KEKIUS 0x26e5…7dd9", "deBridge DLN (exécutions DMAGA)",
                "", "2024-12-14 → 2025-01-04", "0", "CONFIRMÉ (absence)",
                "aucun transfert KEKIUS vers ou depuis les destinataires EVM des exécutions deBridge DMAGA ; voir FINDINGS §3"])
print(len(ov), "chevauchements,", len(fg), "arêtes de financement")
