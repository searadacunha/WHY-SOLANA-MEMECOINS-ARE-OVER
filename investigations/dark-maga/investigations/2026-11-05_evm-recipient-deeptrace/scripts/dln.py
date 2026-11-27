"""Décodeur minimal de l'événement FulfilledOrder de DlnDestination (0xe7351fd7...), sans dépendance. Deux versions, Order = 14 champs :
- v1 : FulfilledOrder(Order order, bytes32 orderId, address sender, address unlockAuthority) ;
- v2 (exécutions de 2026 dans ce dossier) : FulfilledOrder(Order order, bytes32 orderId, uint256, address sender, address unlockAuthority).
Topics = keccak256 de ces signatures (recalculés). La v2 ajoute un uint256 avant sender ; sur les 78 événements v2 du cache, il égale le
takeAmount de l'ordre. Correction du 06/11/2026 : la version initiale ne reconnaissait que la v1, et 74 exécutions vers 2d86 manquaient."""
import re

DLN_DST = "0xe7351fd770a37282b91d153ee690b63579d6dd7f"
FULFILLED = "0xd281ee92bab1446041582480d2c0a9dc91f855386bb27ea295faac1e992f7fe4"  # v1
FULFILLED_V2 = "0xc164aca37b9805a1c9027b6f32260a069723a82926f6e9ece4926e4dd3ea8ecf"  # v2
CREATED_ORDER = "0xfc8703fd57380f9dd234a89dce51333782d49c5902f307b02f03e014d18fe471"  # DlnSource
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

def word(d, i):
    if i < 0 or i % 32 or i + 32 > len(d):
        raise ValueError("Truncated or unaligned ABI word")
    return int.from_bytes(d[i:i + 32], "big")


def raw_order(data_hex, head_words=2):
    """Read a complete ABI Order; an out-of-bounds slice must never become zero."""
    if not isinstance(data_hex, str) or not re.fullmatch(r"0x(?:[0-9a-fA-F]{64})+", data_hex):
        raise ValueError("Invalid ABI event data")
    d = bytes.fromhex(data_hex[2:])
    t = word(d, 0)
    if len(d) < head_words * 32 or t < head_words * 32 or t % 32:
        raise ValueError("Invalid Order tuple offset")
    out = {}
    for k, field in enumerate(FIELDS):
        value = word(d, t + 32 * k)
        if field in DYN:
            if value < 32 * len(FIELDS) or value % 32:
                raise ValueError("Invalid Order bytes offset")
            off = t + value
            size = word(d, off)
            start, end = off + 32, off + 32 + size
            padded_end = start + ((size + 31) // 32) * 32
            if padded_end > len(d) or any(d[end:padded_end]):
                raise ValueError("Truncated or nonzero-padded Order bytes")
            out[field] = d[start:end]
        else:
            out[field] = value
    if out["makerOrderNonce"] >= 1 << 64:
        raise ValueError("Order nonce exceeds uint64")
    return out, "0x" + d[32:64].hex()

def addr_str(chain, b: bytes):
    if not b: return ""
    return b58(b) if chain == 7565164 else "0x" + b.hex()

def _addresses(out):
    g, tk = out["giveChainId"], out["takeChainId"]
    for f in ("makerSrc", "giveTokenAddress", "givePatchAuthoritySrc", "allowedCancelBeneficiarySrc"):
        out[f] = addr_str(g, out[f])
    for f in ("takeTokenAddress", "receiverDst", "orderAuthorityAddressDst", "allowedTakerDst"):
        out[f] = addr_str(tk, out[f])
    out["externalCall"] = out["externalCall"].hex()
    out["giveChain"] = CHAINS.get(g, str(g)); out["takeChain"] = CHAINS.get(tk, str(tk))
    return out


def decode_fulfilled(data_hex: str, version: int = 1) -> dict:
    if version not in (1, 2):
        raise ValueError("Unsupported FulfilledOrder version")
    out, oid = raw_order(data_hex, 3 + version)
    d = bytes.fromhex(data_hex[2:])
    s = 32 * (version - 1)
    for off in (64 + s, 96 + s):
        if word(d, off) >= 1 << 160:
            raise ValueError("Nonzero padding in event address")
    out.update(orderId=oid, sender="0x" + d[76 + s:96 + s].hex(),
               unlockAuthority="0x" + d[108 + s:128 + s].hex(), eventVersion=version)
    if version == 2:
        out["v2Amount"] = word(d, 64)
    return _addresses(out)


def decode_created(data_hex):
    out, oid = raw_order(data_hex, 7)
    d = bytes.fromhex(data_hex[2:])
    out.update(orderId=oid, nativeFixFee=word(d, 96), percentFee=word(d, 128))
    return _addresses(out)

def fulfilled_version(log) -> int:
    """1 ou 2 pour un FulfilledOrder de DlnDestination, 0 sinon."""
    if log["address"].lower() != DLN_DST or not log["topics"]:
        return 0
    return VERSIONS.get(log["topics"][0].lower(), 0)  # full 32-byte topic, never a prefix

def receipt_logs(rcpt):
    """Only successful receipts and unique, non-removed logs can prove execution."""
    if rcpt.get("status") != "0x1":
        return []
    tx = rcpt["transactionHash"]
    if not isinstance(tx, str) or not re.fullmatch(r"0x[0-9a-fA-F]{64}", tx):
        raise ValueError("Invalid receipt transaction hash")
    seen, logs = set(), []
    for log in rcpt["logs"]:
        if log.get("removed"):
            continue
        idx = log["logIndex"]
        if not isinstance(idx, str) or not re.fullmatch(r"0x[0-9a-fA-F]+", idx):
            raise ValueError("Invalid log index")
        idx = int(idx, 16)
        if idx in seen:
            raise ValueError("Duplicate receipt log index")
        seen.add(idx)
        for field in ("transactionHash", "blockHash", "blockNumber"):
            if field in log and field in rcpt and log[field].lower() != rcpt[field].lower():
                raise ValueError(f"Log {field} does not match its receipt")
        logs.append(log)
    return logs


def fills_in_receipt(rcpt) -> list:
    return [dict(decode_fulfilled(l["data"], v), tx=rcpt["transactionHash"], logIndex=int(l["logIndex"], 16))
            for l in receipt_logs(rcpt) if (v := fulfilled_version(l))]

DLN_SRC_EVM = "0xef4fb24ad0916217251f553c0596f8edc630eb66"

def created_in_receipt(rcpt, chain_id=1) -> list:
    """CreatedOrder(Order, bytes32 orderId, bytes affiliateFee, uint256 nativeFixFee, uint256 percentFee, uint32 referralCode, bytes metadata) :
    tête de sept mots ; même tuple Order que FulfilledOrder, sans sender/unlockAuthority."""
    out = []
    for l in receipt_logs(rcpt):
        if (l["address"].lower() != DLN_SRC_EVM or not l.get("topics")
                or l["topics"][0].lower() != CREATED_ORDER):
            continue
        o = decode_created(l["data"])
        if o["giveChainId"] != chain_id:
            continue
        out.append(dict(o, tx=rcpt["transactionHash"], logIndex=int(l["logIndex"], 16), topic0=l["topics"][0]))
    return out
