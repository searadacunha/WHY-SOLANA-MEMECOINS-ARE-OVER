"""Autocontrôle hors ligne (aucun appel réseau : les modules ne lisent que le cache et les fichiers locaux).
Chaque assertion rejoue un chiffre de FINDINGS.md depuis les données brutes ou dérivées de ce dossier. Usage : py312 -I s99_selfcheck.py"""
import csv, json, gzip, sys, os, socket
sys.path.insert(0, os.path.dirname(__file__))
import nt_lib as N
def _no_net(*a, **k): raise OSError("réseau coupé pendant l'autocontrôle")
socket.socket.connect = _no_net  # toute tentative d'appel réseau échoue
R = N.ROOT; ok = 0
def rd(p): return list(csv.DictReader(open(R / p)))
def check(cond, msg):
    global ok
    assert cond, msg
    ok += 1; print("ok", msg)

# Base : grand livre complet (897 tx signées, nonces 0..896) et soldes contrôlés
L = rd("data/base_0xb298_ledger.csv")
own = [r for r in L if r["kind"] == "tx" and r["frm"] == N.B298]
check(len(own) == 897 and sorted(int(r["nonce"]) for r in own) == list(range(897)), "b298 Base : 897 tx signées, nonces 0 à 896 sans trou")
chk = rd("evidence/s11_base_balance_checks.csv")
check(len(chk) >= 40 and all(c["eth_diff"] == "0" and c["usdc_diff"] == "0" for c in chk), f"b298 Base : solde ETH et USDC reconstitué = état archive sur {len(chk)} points")
# F1 : 24 ETH vers le dépôt Coinbase inféré
t = [r for r in L if r["tx"] == "0x52da33cb31aa36ecce1a05774dd7bc69bed8d0a9b555db97e8659771a4a00245"][0]
check(t["to"] == "0x34172888e808debea84bb224bbfa8dcd6d78de7d" and t["raw"] == str(24 * 10 ** 18) and t["ts"] == "2024-11-12T08:57:51", "12/11 08:57:51 : 24 ETH de b298 vers 0x34172888")
cb = rd("data/base_0x3417_ledger.csv")
outs = [r for r in cb if r["dir"] == "out"]; ins = [r for r in cb if r["dir"] == "in"]
check(len(ins) == 5 and {r["frm"] for r in ins} == {N.B298, "0x4b6a508cd730434b4f9a0e32be3646f71b58a8d3"}, "0x34172888 : 5 entrées, de b298 (4) et 0x4b6a508c (1) seulement")
CB = {"0x20fe51a9229eef2cf8ad9e89d91cab9312cf3b7a", "0x1985ea6e9c68e1c272d8209f3b478ac2fdb25c87", "0x40ebc1ac8d4fedd2e144b75fe9c0420be82750c6", "0xb4807865a786e9e9e26e6a9610f2078e7fc507fb", "0x6dcbce46a8b494c885d0e7b6817d2b519df64467"}
check(all(r["to"] in CB for r in outs), "0x34172888 : chaque sortie va à un hot wallet Coinbase étiqueté (Coinbase 14, 31, 41, 42, 55)")
sw = [r for r in outs if r["tx"] == "0x897371dbff83768c73d67a6c85fc59d947fd270cca6474e3f623e891c50f81fa"][0]
check(sw["to"] == "0x20fe51a9229eef2cf8ad9e89d91cab9312cf3b7a" and sw["ts"] == "2024-11-12T08:58:05", "balayage des 24 ETH vers Coinbase 14 en 14 s")
bf = {r["tx"]: r for r in rd("BASE_FLOWS.csv") if r["wallet"] == N.B298}
check(float(bf[t["tx"]]["eth_out_marked_min"]) >= 23.748, "borne basse : au moins 23,748 ETH des 24 viennent de l'USDC de b947")
# F2 : circuit BSC
lk = {r["orderId"]: r for r in rd("CROSSCHAIN_LINKS.csv")}
check(lk["0xc62af9cf7ef4814f579a97750dfbcb8f51a383377fda39423dcd8514957d51d2"]["dst_tx"] == "0x549e4bc55eb2310b903f087d439b16af35c9d4c17624873012443c4eb6730afe", "ordre Ethereum -> BSC relié par orderId")
check(lk["0x5c2e547ffa26cbc17ddc5650d2346cbd23155c8734d0e6d08fb929a84b36285e"]["dst_tx"] == "0xf9b44d3ac32c0ad76280d57f31277844e6b5384ec399b7509b287668e128b3cf", "ordre BSC -> Ethereum relié par orderId")
e = lk["0x801581949a8c0d476a1a188b249642555b3c2d1c88f34cca7ebbdd372719ffa7"]
check(e["dst_tx"].startswith("2w9jzrFEv6") and e["take_amount_raw"] == "445496439103", "ordre Ethereum -> Solana de 445,496439103 SOL relié par orderId")
st = {int(r["block"]): r for r in rd("data/bsc_0xb298_state_changes.csv")}
check(int(st[43950886]["d_native"]) == 157374799465747581520 and int(st[43951101]["d_native"]) == -157467995596656041152, "BSC : +157,3748 BNB puis -157,4680 BNB dans le bloc suivant de b298")
check(int(st[43950886]["native"]) - int(st[43950886]["d_native"]) < 2 * 10 ** 17, "BSC : moins de 0,2 BNB avant l'arrivée")
# F3 : BONK -> GV2w4YvX -> MEXC
T = {r["sig"]: r for r in rd("data/sol_Ei5yGz8d_txs.csv")}
D = json.load(open(R / "data/bsc_0xb298_block_details.json"))
signed = sum(1 for v in D.values() for t in v["txs"] if t["from"].lower() == N.B298)
check(len(D) == 108 and signed == 95 == int(st[max(st)]["nonce"]), "BSC : 108 blocs détaillés, 95 tx signées = nonce final")
B = "DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263"
buy = json.loads(T["4AQCaW4eNyTP1gVNHMVz" + [s for s in T if s.startswith("4AQCaW4eNyTP1gVNHMVz")][0][20:]]["tok"])[B]
X = [x for x in rd("data/sol_Ei5yGz8d_transfers.csv") if x["mint"] == B]
cbin = [x for x in X if x["frm"] == "GJRs4FwHtemZ5ZE9x3FNvJ8TMwitKTh21yxdRPqn7npE"][0]; outb = [x for x in X if x["to"] == "GV2w4YvXeYtEv8LkKFKpFbrqBnvn9HYLesjKgvMyJD5f"][0]
check(buy == 276571548182429 and int(cbin["raw"]) == 225220419214141 and int(outb["raw"]) == buy + int(cbin["raw"]), "Ei5yGz8d : 2 765 715 481,82 BONK achetés + 2 252 204 192,14 reçus de GJRs4FwH = 5 017 919 673,97 envoyés à GV2w4YvX")
G = rd("data/sol_GV2w4YvX_transfers.csv"); g = rd("data/sol_GV2w4YvX_txs.csv")
check(g[0]["signer"] == N.EI5 and int(g[0]["sol"]) == 300000000, "GV2w4YvX : premier SOL = 0,3 SOL d'Ei5yGz8d (wallet vierge)")
usd = [x for x in G if x["mint"] == "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v" and x["frm"] == "GV2w4YvXeYtEv8LkKFKpFbrqBnvn9HYLesjKgvMyJD5f"][0]
check(usd["to"] == "96W8V3toGu55gApT1cNFrZmkcGZwt5YGYotpWaK6fNAm" and usd["raw"] == "182548799464", "GV2w4YvX : 182 548,799464 USDC vers 96W8V3to")
M = rd("data/sol_96W8V3to_transfers.csv")
check(any(x["frm"] == "ASTyfSima4LLAdDgoFGkgqoKowG1LZFDr9fAQrg7iaJZ" and x["asset"] == "SOL" for x in M) and any(x["to"] == "ASTyfSima4LLAdDgoFGkgqoKowG1LZFDr9fAQrg7iaJZ" and x["mint"].startswith("EPjF") for x in M), "96W8V3to : gaz reçu du hot wallet MEXC puis USDC balayé vers lui")
# F4 : boucle 0x2ac17414
Z = rd("data/base_0x2ac1_ledger.csv")
check(Z[0]["frm"] == N.B298 and Z[0]["kind"] == "tx", "0x2ac17414 : premier mouvement = gaz de b298")
f = [r for r in rd("evidence/s12_dln_base.csv") if r["receiverDst"] == "0x2ac17414e34c9a1f70f6eadb6230fa503301e878"]
check(len(f) == 2 and all(r["makerSrc"] == N.EI5 for r in f), "0x2ac17414 : 2 ordres deBridge dont le maker est Ei5yGz8d")
check(any(r["tx"] == "0xe7389f5a4d1065d644104a8920ee5978c8022b82b527eb6cb1553dc5c82ddd57" and r["to"] == N.B298 and r["raw"] == str(16 * 10 ** 16) for r in Z), "0x2ac17414 -> b298 : 0,16 ETH le 27/11 18:40:41")
check(lk["0xd186a2daaad4f179414a33236a6cacdcdac7e85cf386472bb0c8b159de7244c8"]["receiver"] == N.EI5, "b298 -> Ei5yGz8d 8 min plus tard, relié par orderId")
# F5 : deux wallets de vente du 22/07/2024
for w, frm, n, back in [("8kNKNiHKjbCPjaWGjoEEWeQ6X4jkZn2sDV7tz7azfL4t", "HGBiExZRtD2TZdQLWHE9azkTSmE2z7ygKqZMtehJDKYU", 3000000000000, 146627814060),
                        ("BdX9J5pQZ9SoH7PqwDCiiQ2rzaMiT4D9WZ8C1DiwXgyX", "Gcyg2jeLfSY9gxxHf5za5QU74ijtxBb1dB2mdGSPZH3m", 2700000000000, 142401969710)]:
    x = rd(f"data/sol_{w[:8]}_transfers.csv")
    dm = [r for r in x if r["mint"].startswith("7D7BRc") and r["to"] == w]
    gas = [r for r in x if r["asset"] == "SOL" and r["frm"] == N.EI5 and r["to"] == w]
    ret = [r for r in x if r["asset"] == "SOL" and r["frm"] == w and r["to"] == N.EI5]
    check(len(dm) == 1 and dm[0]["frm"] == frm and int(dm[0]["raw"]) == n and len(gas) == 1 and len(ret) == 1 and int(ret[0]["raw"]) == back,
          f"{w[:8]} : {n / 1e6:,.0f} DMAGA de {frm[:8]}, gaz d'Ei5yGz8d, retour de {back / 1e9:.6f} SOL")
# F6 : 43 exécutions vers Ei5yGz8d vérifiées par orderId
S = [r for r in rd("SOLANA_RETURN_FLOWS.csv") if r["kind"] == "fill_from_b298"]
check(len(S) == 43 and round(sum(float(r["sol_in"]) for r in S), 6) == 1959.953482, "43 exécutions b298 -> Ei5yGz8d, 1 959,953482 SOL (dont 1 753,73 depuis Ethereum)")
check(sum(1 for r in rd("CROSSCHAIN_LINKS.csv") if r["level"] == "VERIFIED") == len(rd("CROSSCHAIN_LINKS.csv")) == 88, "88 liens entre chaînes, tous vérifiés par orderId (dont 0x1596c70d, solver tiers, ajouté après audit)")
# Bornes de provenance, corrigées après audit (s15, s16, s17) : soldes archive en cache, chaîne exacte, relais tracé
import s15_relay_bounds as S15, s16_mexc_chain_bound as S16, s17_joint_destinations as S17
J = json.loads((R / "evidence/s15_joint_bound.json").read_text())
check(J["corrected_individual"] == [46.814553, 0.0] and J["under_H_individual"] == [100046.825553, 99981.823743],
      "relais tracé : o1 >= 46,814553 USDC de b947 (sous H : 100 046,825553), o2 >= 0 (sous H : 99 981,823743)")
check(abs(J["joint_min_from_b947"] - 100028.638296) < 1e-6, "borne commune : o1 + o2 portent au moins 100 028,638296 USDC de b947, quelle que soit l'allocation")
m = S16.chain(99981823743); ms = S16.chain(99981823743, strict=True)
check(abs(m["marked_deposit_usdc_min"] - 100027.93) < 0.01 and abs(ms["marked_deposit_usdc_min"] - 99383.28) < 0.01,
      f"hypothèse s51 : dépôt MEXC >= {m['marked_deposit_usdc_min']:,.2f} USDC au prorata, {ms['marked_deposit_usdc_min']:,.2f} en strict (le dépôt privé disait 100 067,30)")
check(S16.chain(0)["marked_deposit_usdc_min"] == 0, "pire cas propre à o2 : borne MEXC nulle")
fr = S17.frontier((0, 100))
check(fr[0]["coinbase_24eth_marked_min_eth"] == 0 and abs(fr[1]["coinbase_24eth_marked_min_eth"] - 23.748588117) < 1e-9
      and abs(fr[0]["mexc_deposit_marked_min_usdc_prorata"] - 100027.93) < 0.01 and fr[1]["mexc_deposit_marked_min_usdc_prorata"] == 0,
      "frontière : Coinbase 0 et MEXC >= 100 027,93 USDC, ou Coinbase >= 23,748588117 ETH et MEXC 0, jamais les deux nulles")
z1, z2 = S17.zero_thresholds()
check(z1 + z2 < round(J["joint_min_from_b947"] * 10 ** 6), f"les deux bornes ne peuvent être nulles ensemble : il faudrait o1 <= {z1 / 1e6:,.2f} et o2 <= {z2 / 1e6:,.2f} USDC, somme < 100 028,64")
print(ok, "assertions passées, réseau coupé")
