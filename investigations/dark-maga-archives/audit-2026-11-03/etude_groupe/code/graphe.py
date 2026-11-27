"""Fonctions pures de l'étude de groupe : ATA, transferts retenus, mesures. Aucun réseau, aucun fichier."""
import hashlib

ALPHA = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
TOKEN_PROGRAM = "TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA"
ATA_PROGRAM = "ATokenGPvbdGVxr1b2hvZbsiqW5xWH25efTNsLJA8knL"
P = 2**255 - 19
D = (-121665 * pow(121666, P - 2, P)) % P
ONE_M = 10**12  # 1 M de jetons, 6 décimales
SUPPLY = 10**15
LAMPORTS_PUR = 50_000_000  # 0,05 SOL
HUB = 15


def b58d(s: str) -> bytes:
    n = 0
    for c in s:
        n = n * 58 + ALPHA.index(c)
    return b"\0" * (len(s) - len(s.lstrip("1"))) + n.to_bytes((n.bit_length() + 7) // 8, "big")


def b58e(b: bytes) -> str:
    n = int.from_bytes(b, "big")
    out = ""
    while n:
        n, r = divmod(n, 58)
        out = ALPHA[r] + out
    return "1" * (len(b) - len(b.lstrip(b"\0"))) + out


def _on_curve(b: bytes) -> bool:
    y = (int.from_bytes(b, "little") & ((1 << 255) - 1)) % P
    u, v = (y * y - 1) % P, (D * y * y + 1) % P
    x2 = u * pow(v, P - 2, P) % P
    return pow(x2, (P - 1) // 2, P) in (0, 1)


def ata(owner: str, mint: str) -> str:
    seeds = b58d(owner) + b58d(TOKEN_PROGRAM) + b58d(mint)
    prog = b58d(ATA_PROGRAM)
    for bump in range(255, -1, -1):
        h = hashlib.sha256(seeds + bytes([bump]) + prog + b"ProgramDerivedAddress").digest()
        if not _on_curve(h):
            return b58e(h)
    raise ValueError("aucune PDA")


def _by_owner(balances: list, mint: str | None = None, not_mint: str | None = None) -> dict:
    out: dict[str, int] = {}
    for b in balances or []:
        if (mint and b["mint"] != mint) or (not_mint and b["mint"] == not_mint) or not b.get("owner"):
            continue
        out[b["owner"]] = out.get(b["owner"], 0) + int(b["uiTokenAmount"]["amount"])
    return out


def deltas(tx: dict, mint: str) -> dict:
    """Variation de jetons par propriétaire sur ce mint, zéros retirés."""
    pre, post = _by_owner(tx["meta"].get("preTokenBalances"), mint), _by_owner(tx["meta"].get("postTokenBalances"), mint)
    d = {o: post.get(o, 0) - pre.get(o, 0) for o in set(pre) | set(post)}
    return {o: v for o, v in d.items() if v}


def post_balance(tx: dict, mint: str, owner: str) -> int:
    return _by_owner(tx["meta"].get("postTokenBalances"), mint).get(owner, 0)


def transfers(tx: dict, mint: str) -> tuple[list, bool]:
    """(arêtes [expéditeur, receveur, jetons bruts], ambigu). Règle du plan, section « Un transfert retenu »."""
    if tx["meta"].get("err"):
        return [], False
    d = deltas(tx, mint)
    senders = [o for o, v in d.items() if v < 0]
    receivers = {o: v for o, v in d.items() if v > 0}
    big = [o for o, v in receivers.items() if v >= ONE_M]
    if not big:
        return [], False
    if len(senders) != 1:
        return [], True
    sender = senders[0]
    if abs(sum(receivers.values()) + d[sender]) > abs(d[sender]) * 0.01:
        return [], False
    who = {sender, *big}
    pre_o = _by_owner(tx["meta"].get("preTokenBalances"), not_mint=mint)
    post_o = _by_owner(tx["meta"].get("postTokenBalances"), not_mint=mint)
    if any(pre_o.get(o, 0) != post_o.get(o, 0) for o in who):
        return [], False
    keys = [k["pubkey"] if isinstance(k, dict) else k for k in tx["transaction"]["message"]["accountKeys"]]
    for i, k in enumerate(keys):
        if k in who and abs(tx["meta"]["postBalances"][i] - tx["meta"]["preBalances"][i]) >= LAMPORTS_PUR:
            return [], False
    return [[sender, o, receivers[o]] for o in big], False


def measures(edges: list, bal: dict, min_raw: int = ONE_M, hub: int | None = HUB) -> dict:
    """G1, G2, G3 depuis les arêtes [src, dst, brut, ...] et les soldes à S."""
    nb: dict[str, set] = {}
    for e in edges:
        if e[2] >= min_raw and e[0] != e[1]:
            nb.setdefault(e[0], set()).add(e[1])
            nb.setdefault(e[1], set()).add(e[0])
    gone = {o for o, s in nb.items() if hub and len(s) >= hub}
    nb = {o: s - gone for o, s in nb.items() if o not in gone}
    nb = {o: s for o, s in nb.items() if s}
    seen, best = set(), set()
    for o in nb:
        if o in seen:
            continue
        comp, stack = set(), [o]
        while stack:
            x = stack.pop()
            if x not in comp:
                comp.add(x)
                stack += nb[x]
        seen |= comp
        if len(comp) > len(best):
            best = comp
    return {"G1": len(best), "G2": sum(bal.get(o, 0) for o in best) / SUPPLY, "G3": sum(len(s) for s in nb.values()) // 2, "services_retires": len(gone)}
