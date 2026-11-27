"""Décodeur minimal de l'événement FulfilledOrder de DlnDestination (0xe7351fd7...), sans dépendance. Deux versions, Order = 14 champs :
- v1 : FulfilledOrder(Order order, bytes32 orderId, address sender, address unlockAuthority) ;
- v2 (exécutions de 2026 dans ce dossier) : FulfilledOrder(Order order, bytes32 orderId, uint256, address sender, address unlockAuthority).
Topics = keccak256 de ces signatures (recalculés). La v2 ajoute un uint256 avant sender ; sur les 78 événements v2 du cache, il égale le
takeAmount de l'ordre. Correction du 06/11/2026 : la version initiale ne reconnaissait que la v1, et 74 exécutions vers 2d86 manquaient."""
DLN_DST = "0xe7351fd770a37282b91d153ee690b63579d6dd7f"
FULFILLED = "0xd281ee92bab14460"     # v1 (préfixe du topic0) ; contrôle positif dans s99
FULFILLED_V2 = "0xc164aca37b9805a1"  # v2
VERSIONS = {FULFILLED: 1, FULFILLED_V2: 2}
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

def decode_fulfilled(data_hex: str, version: int = 1) -> dict:
    d = bytes.fromhex(data_hex[2:])
    t = word(d, 0); s = 32 * (version - 1)  # v2 : un mot de plus avant sender
    out = {"orderId": "0x" + d[32:64].hex(), "sender": "0x" + d[64 + s + 12:96 + s].hex(), "unlockAuthority": "0x" + d[96 + s + 12:128 + s].hex(),
           "eventVersion": version}
    if version == 2:
        out["v2Amount"] = word(d, 64)
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

def fulfilled_version(log) -> int:
    """1 ou 2 pour un FulfilledOrder de DlnDestination, 0 sinon."""
    if log["address"].lower() != DLN_DST or not log["topics"]:
        return 0
    return next((v for p, v in VERSIONS.items() if log["topics"][0].startswith(p)), 0)

def fills_in_receipt(rcpt) -> list:
    return [dict(decode_fulfilled(l["data"], v), tx=rcpt["transactionHash"], logIndex=int(l["logIndex"], 16))
            for l in rcpt["logs"] if (v := fulfilled_version(l))]

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
        o.pop("sender"); o.pop("unlockAuthority"); o.pop("eventVersion")
        o["percentFee"] = word(d, 128); o["nativeFixFee"] = word(d, 96)
        out.append(dict(o, tx=rcpt["transactionHash"], logIndex=int(l["logIndex"], 16), topic0=l["topics"][0]))
    return out
