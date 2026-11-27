"""Adresse de compte de jetons associé (ATA) Solana, sans dépendance : base58, PDA, test « hors courbe » ed25519.

shortcut: seuls les comptes ATA sont couverts ; un bot qui achète avec un compte de jetons non associé échappe à ce test,
d'où la collecte côté pool en complément (k20)."""
import hashlib

B58 = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
P = 2**255 - 19
D = (-121665 * pow(121666, P - 2, P)) % P
TOKEN = "TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA"
ATA_PROGRAM = "ATokenGPvbdGVxr1b2hvZbsiqW5xWH25efTNsLJA8knL"


def b58d(s: str) -> bytes:
    n = 0
    for c in s:
        n = n * 58 + B58.index(c)
    raw = n.to_bytes((n.bit_length() + 7) // 8, "big") if n else b""
    return b"\0" * (len(s) - len(s.lstrip("1"))) + raw


def b58e(b: bytes) -> str:
    n = int.from_bytes(b, "big")
    out = ""
    while n:
        n, r = divmod(n, 58)
        out = B58[r] + out
    return "1" * (len(b) - len(b.lstrip(b"\0"))) + out


def on_curve(b: bytes) -> bool:
    """Même règle que curve25519-dalek decompress : y réduit mod p, valide si (y²-1)/(d·y²+1) est un carré."""
    y = int.from_bytes(b, "little") & ((1 << 255) - 1)
    y %= P
    u = (y * y - 1) % P
    v = (D * y * y + 1) % P
    x2 = u * pow(v, P - 2, P) % P
    return x2 == 0 or pow(x2, (P - 1) // 2, P) == 1


def pda(seeds: list[bytes], program: str) -> str:
    prog = b58d(program)
    for bump in range(255, -1, -1):
        h = hashlib.sha256(b"".join(seeds) + bytes([bump]) + prog + b"ProgramDerivedAddress").digest()
        if not on_curve(h):
            return b58e(h)
    raise ValueError("aucun bump valide")


def ata(owner: str, mint: str, token_program: str = TOKEN) -> str:
    return pda([b58d(owner), b58d(token_program), b58d(mint)], ATA_PROGRAM)


if __name__ == "__main__":
    # Valeurs lues dans la transaction de création de KEKIUS-XC78 (2xz9tgPB…, slot 310594124) : voir tests/
    assert b58e(b58d(TOKEN)) == TOKEN
    print("ok")
