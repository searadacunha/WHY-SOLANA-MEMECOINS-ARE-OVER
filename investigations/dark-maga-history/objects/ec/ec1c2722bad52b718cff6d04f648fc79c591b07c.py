"""Décodeur minimal de l'ANCIEN événement FulfilledOrder de DlnDestination (0xe7351fd7...), sans dépendance.
Périmètre vérifié dans cette enquête : 2024. La seconde version d'événement (topic0 0xc164aca3..., utilisée notamment en 2026) n'est PAS décodée ici : ne pas inférer l'exhaustivité des fills récents.
Pour les formats et le périmètre élargi, consulter l'audit et les décodeurs de investigations/2026-11-06_debridge_base_bsc_solana/ (PR #16).
FulfilledOrder(Order order, bytes32 orderId, address sender, address unlockAuthority), Order = 14 champs (doc deBridge DLN)."""
DLN_DST = "0xe7351fd770a37282b91d153ee690b63579d6dd7f"
FULFILLED = "0xd281ee92bab14460"  # préfixe du topic0 observé ; validé par le contrôle positif ci-dessous
CHAINS = {7565164: "solana", 1: "ethereum", 56: "bsc", 137: "polygon", 42161: "arbitrum", 8453: "base", 10: "optimism", 43114: "avalanche", 59144: "linea", 100000001: "neon", 100000002: "gnosis", 100000004: "metis", 100000005: "bitrock", 100000014: "sonic", 100000022: "hyperevm"}
B58 = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"

def b58(b: bytes) -> str:
    n = int.from_bytes(b, "big"); s = ""
    while n: n, r = divmod(n, 58); s = B58[r] + s
    return "1" * (len(b) - len(b.lstrip(b"\0"))) + s

FIELDS = ["makerOrderNonce", "makerSrc", "giveChainId", "giveTokenAddress", "giveAmount", "takeChainId", "takeTokenAddress",
          "takeAmount", "receiverDst", "givePatchAuthoritySrc", "orderAuthorityAddressDst", "allowedTakerDst",
          "allowedCancelBeneficiarySrc", "externalCall"]
DYN = {"makerSrc", "giveTokenAddress", "takeTokenAddress", "receiverDst", "givePatchAuthoritySrc", "orderAuthorityAddressDst",
       "allowedTakerDst", "allowedCancelBeneficiarySrc", "externalCall"}

def word(d, i): return int.from_bytes(d[i:i + 32], "big")

def addr_str(chain, b: bytes):
    if not b: return ""
    return b58(b) if chain == 7565164 else "0x" + b.hex()

def decode_fulfilled(data_hex: str) -> dict:
    d = bytes.fromhex(data_hex[2:])
    t = word(d, 0)
    out = {"orderId": "0x" + d[32:64].hex(), "sender": "0x" + d[64 + 12:96].hex(), "unlockAuthority": "0x" + d[96 + 12:128].hex()}
    for k, f in enumerate(FIELDS):
        v = word(d, t + 32 * k)
        if f in DYN:
            off = t + v; n = word(d, off); out[f] = d[off + 32: off + 32 + n]
        else:
            out[f] = v
    g, tk = out["giveChainId"], out["takeChainId"]
    for f in ("makerSrc", "giveTokenAddress", "givePatchAuthoritySrc", "allowedCancelBeneficiarySrc"):
        out[f] = addr_str(g, out[f])
    for f in ("takeTokenAddress", "receiverDst", "orderAuthorityAddressDst", "allowedTakerDst"):
        out[f] = addr_str(tk, out[f])
    out["externalCall"] = out["externalCall"].hex()
    out["giveChain"] = CHAINS.get(g, str(g)); out["takeChain"] = CHAINS.get(tk, str(tk))
    return out

def fills_in_receipt(rcpt) -> list:
    return [dict(decode_fulfilled(l["data"]), tx=rcpt["transactionHash"], logIndex=int(l["logIndex"], 16))
            for l in rcpt["logs"] if l["address"].lower() == DLN_DST and l["topics"][0].startswith(FULFILLED)]

DLN_SRC_EVM = "0xef4fb24ad0916217251f553c0596f8edc630eb66"

def created_in_receipt(rcpt) -> list:
    """CreatedOrder(Order, bytes32 orderId, bytes affiliateFee, uint256 nativeFixFee, uint256 percentFee, uint32 referralCode, bytes metadata) :
    même tête (offset de l'ordre, orderId) que FulfilledOrder, les champs sender/unlockAuthority décodés là n'ont pas de sens et sont retirés."""
    out = []
    for l in rcpt["logs"]:
        if l["address"].lower() != DLN_SRC_EVM or len(l["data"]) < 2 + 64 * 20:
            continue
        try:
            o = decode_fulfilled(l["data"])
        except Exception:
            continue
        if o["giveChainId"] != 1:
            continue
        d = bytes.fromhex(l["data"][2:])
        o.pop("sender"); o.pop("unlockAuthority")
        o["percentFee"] = word(d, 128); o["nativeFixFee"] = word(d, 96)
        out.append(dict(o, tx=rcpt["transactionHash"], logIndex=int(l["logIndex"], 16), topic0=l["topics"][0]))
    return out
