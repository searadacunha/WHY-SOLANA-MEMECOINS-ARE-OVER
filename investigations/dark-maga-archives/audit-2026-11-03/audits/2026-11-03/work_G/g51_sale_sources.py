#!/usr/bin/env python3
"""D'où vient l'argent versé aux dépôts ? Pour les wallets de P1 : encaissements par nature, depuis net_txs. Ventes directes de DMAGA (delta DMAGA négatif et valeur reçue), encaissements d'ordres DCA (programme DCA265Vj, DMAGA inchangé, valeur reçue, non signé par le wallet), autres échanges, retraits Coinbase. Sortie g51.txt."""
import csv, gzip, sys, time, json, collections
OUT = "audits/2026-11-03/work_G/"; G = "/Volumes/VERBATIM HD/Dark-MAGA-Investigation/audits_work/G/"
sys.stdout = open(OUT + "g51.txt", "w")
price = {r["date"]: float(r["close"]) for r in csv.DictReader(open(OUT + "sol_daily.csv"))}
def px(bt):
    d = time.strftime("%Y-%m-%d", time.gmtime(bt))
    return price.get(d) or (price[min(price)] if d < min(price) else price[max(price)])
series = {r["wallet"] for r in csv.DictReader(open("audits/2026-11-03/work_C/cb_series.csv"))}
send9 = {r["sender"] for r in csv.DictReader(open("audits/2026-11-03/work_D/d20_senders.csv"))}
g33 = set(json.load(open("data/prevent_groups.json"))[0]["members"])
SAL = {"G41vRrsHShLEvwMj58ruhqJycGfAtWXxtLD56uFExL8E", "C73Yv9iHmTaf8SU2XFnGLt7QXUDqbeWNtUYza9WJhkae", "AtZjv3DuV9cLn3Jxm72TMSdTN4aM6CrBaGyxUC4c2wDk", "EGtyQEgMKGKXjppDqj9sYy97e9m7nvu1US4SfFXNakMy"}
P1 = (series | send9 | {"8YLEuUtZ4eFMJbf46oNb1CeG6dYFWGyxnQSh9hrgzBzR"}) - SAL
P2 = (g33 | SAL) - P1
MINT = 1720922725
C = {"P1": collections.Counter(), "P2": collections.Counter()}
for l in csv.DictReader(gzip.open(G + "net_txs.csv.gz", "rt")):
    a = l["owner"]; p = "P1" if a in P1 else ("P2" if a in P2 else None)
    if not p or l["err"] != "0" or l["pure"] == "1": continue
    bt = int(l["bt"]); v = (int(l["native_delta"]) + int(l["wsol_delta"])) / 1e9 + (int(l["usdc_delta"]) + int(l["usdt_delta"])) / 1e6 / px(bt)
    d = int(l["dmaga_delta"]); dca = "DCA265Vj8a9CEuX1eb1LWRnDT7uK6q1xMipnNyatn23M" in l["programs"]; other = int(l["n_other_mints"]) > 0
    if bt < MINT: tag = "avant_mint"
    elif d < 0 and v > 0: tag = "vente_DMAGA_directe"
    elif d == 0 and dca and v > 0 and l["signed"] == "0": tag = "encaissement_DCA_non_signé"
    elif d < 0 and v <= 0: tag = "DMAGA_sorti_sans_valeur_reçue"
    elif d > 0 and v < 0: tag = "achat_DMAGA"
    elif d > 0 and v >= 0: tag = "DMAGA_reçu_sans_paiement_lu"
    elif other and v > 0: tag = "vente_autre_jeton"
    elif other and v < 0: tag = "achat_autre_jeton"
    else: tag = "autre_programme"
    C[p][tag] += v; C[p]["n_" + tag] += 1
    if d < 0: C[p]["jetons_sortis_" + tag] += -d / 1e6
for p, c in C.items():
    print(p, {k: round(v, 1) for k, v in sorted(c.items()) if not k.startswith(("n_", "jetons"))})
    print("  nombres", {k[2:]: v for k, v in sorted(c.items()) if k.startswith("n_")})
    print("  jetons M sortis", {k[14:]: round(v / 1e6, 2) for k, v in sorted(c.items()) if k.startswith("jetons")})
