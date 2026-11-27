"""Recalcul local de l'orderId deBridge DLN : keccak256 de l'encodage compact de l'ordre.

Format repris de la table documentée dans `contracts/libraries/DlnOrderLib.sol` (debridge-finance/dln-contracts, commit
d54e94f2b5102bff89a4df506404bb77f3edc148, licence BUSL-1.1 : aucun code copié, seul le format est réimplémenté) :
nonce (8 o) | len+makerSrc | giveChainId (32) | len+giveToken | giveAmount (32) | takeChainId (32) | len+takeToken | takeAmount (32)
| len+receiverDst | len+givePatchAuthoritySrc | len+orderAuthorityAddressDst | len+allowedTakerDst | len+allowedCancelBeneficiarySrc
| 1 octet (appel externe présent) | keccak256(externalCall) si présent (ou l'empreinte elle-même, variante WithExternalCallHash).

Si l'orderId recalculé à partir des champs décodés égale celui que le contrat a émis, les champs décodés (maker, receveur,
jetons, montants) sont exactement ceux de l'ordre : le contrat lui-même dérive l'orderId de ces champs.
Keccak-256 (pas SHA3-256 : remplissage 0x01) en Python standard, vérifié par des vecteurs connus en fin de fichier."""

_RC = [0x0000000000000001, 0x0000000000008082, 0x800000000000808A, 0x8000000080008000, 0x000000000000808B, 0x0000000080000001,
       0x8000000080008081, 0x8000000000008009, 0x000000000000008A, 0x0000000000000088, 0x0000000080008009, 0x000000008000000A,
       0x000000008000808B, 0x800000000000008B, 0x8000000000008089, 0x8000000000008003, 0x8000000000008002, 0x8000000000000080,
       0x000000000000800A, 0x800000008000000A, 0x8000000080008081, 0x8000000000008080, 0x0000000080000001, 0x8000000080008008]
_ROT = [[0, 36, 3, 41, 18], [1, 44, 10, 45, 2], [62, 6, 43, 15, 61], [28, 55, 25, 21, 56], [27, 20, 39, 8, 14]]
_M = (1 << 64) - 1

def _rol(v, n): return ((v << n) | (v >> (64 - n))) & _M if n else v

def _f(A):
    for rc in _RC:
        C = [A[x][0] ^ A[x][1] ^ A[x][2] ^ A[x][3] ^ A[x][4] for x in range(5)]
        D = [C[(x - 1) % 5] ^ _rol(C[(x + 1) % 5], 1) for x in range(5)]
        A = [[A[x][y] ^ D[x] for y in range(5)] for x in range(5)]
        B = [[0] * 5 for _ in range(5)]
        for x in range(5):
            for y in range(5):
                B[y][(2 * x + 3 * y) % 5] = _rol(A[x][y], _ROT[x][y])
        A = [[B[x][y] ^ ((~B[(x + 1) % 5][y]) & B[(x + 2) % 5][y]) for y in range(5)] for x in range(5)]
        A[0][0] ^= rc
    return A

def keccak256(data: bytes) -> bytes:
    rate = 136
    pad = rate - len(data) % rate
    p = bytearray(data) + (b"\x81" if pad == 1 else b"\x01" + b"\x00" * (pad - 2) + b"\x80")  # un seul octet : 0x01 et 0x80 fusionnent
    A = [[0] * 5 for _ in range(5)]
    for off in range(0, len(p), rate):
        blk = p[off:off + rate]
        for i in range(rate // 8):
            x, y = i % 5, i // 5
            A[x][y] ^= int.from_bytes(blk[8 * i:8 * i + 8], "little")
        A = _f(A)
    return b"".join(A[i % 5][i // 5].to_bytes(8, "little") for i in range(4))

def encode_order(o: dict, external_call_is_hash=False) -> bytes:
    """o : champs bruts, entiers pour nonce/chaînes/montants, bytes pour les adresses et externalCall."""
    def lb(b): return bytes([len(b)]) + b
    u = lambda v: v.to_bytes(32, "big")
    e = o["makerOrderNonce"].to_bytes(8, "big") + lb(o["makerSrc"]) + u(o["giveChainId"]) + lb(o["giveTokenAddress"]) + u(o["giveAmount"])
    e += u(o["takeChainId"]) + lb(o["takeTokenAddress"]) + u(o["takeAmount"]) + lb(o["receiverDst"])
    e += lb(o["givePatchAuthoritySrc"]) + lb(o["orderAuthorityAddressDst"]) + lb(o["allowedTakerDst"]) + lb(o["allowedCancelBeneficiarySrc"])
    ec = o["externalCall"]
    e += b"\x01" if ec else b"\x00"
    if ec:
        e += ec if external_call_is_hash else keccak256(ec)
    return e

def order_id(o: dict) -> str:
    return "0x" + keccak256(encode_order(o)).hex()

FIELDS = ["makerOrderNonce", "makerSrc", "giveChainId", "giveTokenAddress", "giveAmount", "takeChainId", "takeTokenAddress",
          "takeAmount", "receiverDst", "givePatchAuthoritySrc", "orderAuthorityAddressDst", "allowedTakerDst",
          "allowedCancelBeneficiarySrc", "externalCall"]
INT = {"makerOrderNonce", "giveChainId", "giveAmount", "takeChainId", "takeAmount"}

def raw_order(data_hex: str) -> tuple:
    """Champs bruts de l'Order d'un journal CreatedOrder ou FulfilledOrder (même tête : offset de l'Order, puis orderId)."""
    d = bytes.fromhex(data_hex[2:] if data_hex.startswith("0x") else data_hex)
    w = lambda i: int.from_bytes(d[i:i + 32], "big")
    t = w(0); out = {}
    for k, f in enumerate(FIELDS):
        v = w(t + 32 * k)
        if f in INT:
            out[f] = v
        else:
            off = t + v; n = w(off); out[f] = d[off + 32: off + 32 + n]
    return out, "0x" + d[32:64].hex()

def _selftest():
    assert keccak256(b"").hex() == "c5d2460186f7233c927e7db2dcc703c0e500b653ca82273b7bfad8045d85a470"
    assert keccak256(b"abc").hex() == "4e03657aea45a94fc7d47ba826c8d667c0d1e6e33a64a036ec44f58fa12d6c45"
_selftest()
