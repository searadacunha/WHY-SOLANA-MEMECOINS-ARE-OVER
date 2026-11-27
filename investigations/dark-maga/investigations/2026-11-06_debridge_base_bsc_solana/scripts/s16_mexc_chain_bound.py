"""Borne de provenance de bout en bout, en fractions exactes, pour le circuit du 12-13/11/2024 :
ordre o2 de b298 (Ethereum -> BSC, USDC) -> BNB -> ETH BEP-20 -> ordre BSC -> ETH (Ethereum) -> ordre -> SOL (Ei5yGz8d) -> BONK
-> GV2w4YvX -> vente -> USDC -> dépôt MEXC 96W8V3to. Aucun appel réseau : fixtures publiées (Solana, soldes archive EVM).

Règle à chaque étape (pire cas, sans FIFO) : la sortie étudiée puise d'abord dans tout ce qui n'est pas prouvé marqué
(solde d'avant, part non marquée de l'arrivée) ; une conversion atomique transmet la part marquée de son entrée.
Deux variantes à l'étape BONK, où la vente passe par trois pools à des prix différents :
- prorata : le BONK marqué reçoit le prix moyen de la vente (une seule tx, tout le stock vendu) ;
- strict : le BONK marqué est attribué d'abord aux unités retenues par le routeur, puis aux pools les moins chers.
La part marquée de o2 (USDC venu de b947) est un paramètre : 0 au pire cas propre à o2 (relais tracé, s15), 99 981,823743
sous l'hypothèse de s51 (relais = b947). Facteurs Solana repris de l'audit indépendant (scratchpad audit_sol/s04_bound.py)."""
import json, os, sys
from fractions import Fraction as F
sys.path.insert(0, os.path.dirname(__file__))
import nt_lib as N

FIX = N.ROOT / "evidence" / "fixtures"
GV = "GV2w4YvXeYtEv8LkKFKpFbrqBnvn9HYLesjKgvMyJD5f"
BONK = "DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263"
USDC = "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"

def sol(w): return {json.loads(l)["transaction"]["signatures"][0][:10]: json.loads(l) for l in (FIX / "sol" / f"{w}.jsonl").read_text().splitlines()}
def keys_of(t):
    ks = [k["pubkey"] if isinstance(k, dict) else k for k in t["transaction"]["message"]["accountKeys"]]
    la = t["meta"].get("loadedAddresses") or {}
    return ks + la.get("writable", []) + la.get("readonly", [])
def pre(t, w): return t["meta"]["preBalances"][keys_of(t).index(w)]
def dsol(t, w): i = keys_of(t).index(w); return t["meta"]["postBalances"][i] - t["meta"]["preBalances"][i]
def tok(t, side):  # compte de jeton -> montant brut
    ks = keys_of(t); return {ks[b["accountIndex"]]: int(b["uiTokenAmount"]["amount"]) for b in t["meta"].get(side) or []}
def dtok(t, w, mint):
    s = 0
    for side, sg in (("preTokenBalances", -1), ("postTokenBalances", 1)):
        for b in t["meta"].get(side) or []:
            if b.get("owner") == w and b["mint"] == mint: s += sg * int(b["uiTokenAmount"]["amount"])
    return s
def spl_in(t, auth):  # somme des transferts SPL signés par auth (entrée d'un échange)
    return sum(int(ix["parsed"]["info"]["amount"]) for ii in t["meta"].get("innerInstructions") or [] for ix in ii["instructions"]
               if isinstance(ix.get("parsed"), dict) and ix["parsed"].get("type") == "transfer" and ix.get("program") == "spl-token"
               and ix["parsed"]["info"].get("authority") == auth) + \
           sum(int(ix["parsed"]["info"]["amount"]) for ix in t["transaction"]["message"]["instructions"]
               if isinstance(ix.get("parsed"), dict) and ix["parsed"].get("type") == "transfer" and ix.get("program") == "spl-token"
               and ix["parsed"]["info"].get("authority") == auth)

def rpc_cached(url, method, params):
    N.E.RPC = url; return N.E.rpc(method, params)

def worst(x, before, marked_before):
    """Part marquée minimale d'une sortie x quand tout le non-marqué possible (before - marked_before) passe d'abord dans x."""
    return max(F(0), F(x) - (F(before) - marked_before))

def chain(m2, strict=False):
    x2 = 99989828367                                                     # o2 : USDC donnés par b298 (ordre 0xca823779)
    # BSC : solde avant / arrivée / valeur échangée (archive Tatum ; tx 0x76ffdad7)
    P_bnb = int(rpc_cached("https://bsc-mainnet.gateway.tatum.io", "eth_getBalance", [N.B298, hex(43950885)]), 16)
    after = int(rpc_cached("https://bsc-mainnet.gateway.tatum.io", "eth_getBalance", [N.B298, hex(43950886)]), 16)
    A_bnb = after - P_bnb; V_bnb = 0x88927c24b12aedcc0
    a_bnb = F(A_bnb) * F(m2, x2)
    lo_bnb = worst(V_bnb, after, a_bnb)
    # Ethereum : arrivée de l'ordre BSC, solde avant (archive drpc), ordre vers Ei5yGz8d (valeur de la tx 0x2fa91216)
    E_pre = int(rpc_cached("https://eth.drpc.org", "eth_getBalance", [N.B298, hex(21173223)]), 16)
    E_mid = int(rpc_cached("https://eth.drpc.org", "eth_getBalance", [N.B298, hex(21173224)]), 16)
    E_end = int(rpc_cached("https://eth.drpc.org", "eth_getBalance", [N.B298, hex(21174281)]), 16)
    assert E_mid == E_end, "mouvement d'ETH entre l'arrivée et l'ordre"
    A_eth = 29845089109620802062; V_eth = 29019784588402031094
    assert E_mid - E_pre == A_eth
    lo_eth = worst(V_eth, E_mid, F(A_eth) * lo_bnb / V_bnb)
    # Solana : arrivée sur Ei5yGz8d, achat de BONK
    ei = sol(N.EI5); gv = sol(GV)
    fill, buy, gj, tr = ei["2w9jzrFEv6"], ei["4AQCaW4eNy"], ei["29E3ro5i5T"], ei["5EFJ9CWFdb"]
    A_sol = dsol(fill, N.EI5); S_pre = pre(fill, N.EI5); V_sol = spl_in(buy, N.EI5)
    assert (A_sol, S_pre, V_sol) == (445496439103, 111726858, 445000000000)
    lo_sol = worst(V_sol, S_pre + A_sol, F(A_sol) * lo_eth / V_eth)
    bought = dtok(buy, N.EI5, BONK); cb = dtok(gj, N.EI5, BONK); sent = -dtok(tr, N.EI5, BONK)
    assert sent == bought + cb and dtok(tr, GV, BONK) == sent
    marked_bonk = F(bought) * lo_sol / V_sol
    # GV2w4YvX : vente (trois pools + reste retenu par le routeur), conversion en USDC, dépôt
    sale, conv, dep = gv["5Z5eChWacM"], gv["4wW64PUDwB"], gv["4nFJRpmP8K"]
    sold = -dtok(sale, GV, BONK); p0, p1 = tok(sale, "preTokenBalances"), tok(sale, "postTokenBalances")
    legs = []
    for vt, vs in (("9MSyH6ptUM1a885FUhawyYLd6YfVjDRUhqib4Apqjm3Z", "47BkLC5ReY8tfQF5Web2nk3zA4TKskdk8NARKuMGV8gE"),
                   ("HTsaYAZ5yhpk98Dm3fDKrTueieEDX34ZkUjeacQYoVSV", "EA5NtnGXFe2zVnoov7gAcntreefhMTqXXTGWNerx41Jm"),
                   ("J6vHZDKghn3dbTG7pcBLzHMnXFoqUEiHVaFfZxojMjXs", "DBo9bdufoB8z4FNdNnU8u33SHWNvDa6jFqKcX7NLqTB2")):
        b, s = p1[vt] - p0[vt], p0[vs] - p1[vs]; legs.append((F(s, b), b, s))
    ret = p1["9A1gB614spurtJHiuFJN9gTLCatkevKvGMeMqWBpW7KL"] - p0["9A1gB614spurtJHiuFJN9gTLCatkevKvGMeMqWBpW7KL"]
    gross = sum(l[2] for l in legs); assert sum(l[1] for l in legs) + ret == sold
    if strict:
        rem = marked_bonk - min(marked_bonk, ret); m_sol = F(0)
        for price, b, s in sorted(legs):
            take = min(rem, F(b)); m_sol += price * take; rem -= take
    else:
        m_sol = F(gross) * marked_bonk / sold
    m_sol = max(F(0), m_sol - (gross - dsol(sale, GV)))   # frais de la vente : pris d'abord sur le marqué (pire cas)
    S = spl_in(conv, GV); usdc = dtok(conv, GV, USDC); bal = pre(conv, GV)
    lo_conv = worst(S, bal, m_sol)              # le SOL non issu de la vente (gaz d'Ei5yGz8d, poussière) passe d'abord dans S
    m_usdc = F(usdc) * lo_conv / S
    assert -dtok(dep, GV, USDC) == usdc == 182548799464
    return dict(m2_usdc=float(F(m2, 10 ** 6)), lo_bnb=float(lo_bnb / 10 ** 18), lo_eth=float(lo_eth / 10 ** 18), lo_sol=float(lo_sol / 10 ** 9),
                marked_bonk_share=float(marked_bonk / sold), lo_sale_sol=float(m_sol / 10 ** 9), lo_converted_sol=float(lo_conv / 10 ** 9),
                deposit_usdc=usdc / 10 ** 6, marked_deposit_usdc_min=float(m_usdc / 10 ** 6), share=float(m_usdc / usdc))

if __name__ == "__main__":
    J = json.loads((N.ROOT / "evidence/s15_joint_bound.json").read_text())
    res = {}
    for name, m2 in (("s51_hypothese_relais_pur", 99981823743), ("pire_cas_propre_a_o2", 0), ("allocation_du_minimum_commun", round(J["o2_marked"] * 10 ** 6))):
        for strict in (False, True):
            r = chain(m2, strict); res[f"{name}{'_strict' if strict else '_prorata'}"] = r
            print(f"{name:32s} {'strict ' if strict else 'prorata'} : o2 marqué {r['m2_usdc']:>12,.6f} -> dépôt MEXC marqué >= {r['marked_deposit_usdc_min']:>12,.2f} USDC ({r['share']:.4%})")
    (N.ROOT / "evidence/s16_mexc_chain_bound.json").write_text(json.dumps(res, indent=1) + "\n")
