"""Décodeur SPL qui préserve le mint, instruction par instruction (issue #27).

Un `Transfer` SPL ordinaire ne cite pas le compte du mint : il échappe à l'historique du mint, d'où sort trades.parquet. Ici, chaque
compte de jetons est rapporté à son propriétaire et à son mint par, dans l'ordre :
  1. les soldes pre/post de la transaction (compte existant avant, ou encore ouvert après) ;
  2. les instructions initializeAccount, initializeAccount2 et initializeAccount3 de la même transaction (compte créé puis fermé
     dans la transaction, absent des soldes).
Un compte jamais résolu reste sous son adresse, avec owner_known=False. Les montants restent des entiers bruts.
Une transaction échouée ne produit aucun mouvement : ses instructions n'ont pas eu d'effet.
Les instructions internes sont lues comme les externes ; chaque mouvement garde son chemin (`o3` = 4e externe, `o3.1` = 2e interne de celle-ci).
Classer un mouvement (virement personnel, jambe de swap, service) n'est pas le rôle de ce module."""

import base64
import struct

WSOL = "So11111111111111111111111111111111111111112"
SYSTEM, TOKEN, TOKEN22 = "11111111111111111111111111111111", "TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA", "TokenzQdBNbLqP5VEhdkAS6EPFLC1PHnBqCXEpPxuEb"


def keys(tx):
    return [k["pubkey"] if isinstance(k, dict) else k for k in tx["transaction"]["message"]["accountKeys"]]


def token_accounts(tx):
    """{compte de jetons: (propriétaire, mint)} d'après les soldes pre/post, puis les initialisations de la transaction."""
    ks, out = keys(tx), {}
    for side in ("preTokenBalances", "postTokenBalances"):
        for b in tx["meta"].get(side) or []:
            out[ks[b["accountIndex"]]] = (b.get("owner"), b["mint"])
    for _, ix in instructions(tx):
        p = ix.get("parsed")
        if ix.get("programId") in (TOKEN, TOKEN22) and isinstance(p, dict) and p.get("type") in ("initializeAccount", "initializeAccount2", "initializeAccount3"):
            info = p.get("info") or {}
            out.setdefault(info.get("account"), (info.get("owner"), info.get("mint")))
    return out


def instructions(tx):
    """(chemin, instruction) pour toutes les instructions, internes comprises, dans l'ordre d'exécution."""
    inner = {g["index"]: g["instructions"] for g in tx["meta"].get("innerInstructions") or []}
    for i, ix in enumerate(tx["transaction"]["message"]["instructions"]):
        yield f"o{i}", ix
        for j, sub in enumerate(inner.get(i, [])):
            yield f"o{i}.{j}", sub


def movements(tx):
    if tx["meta"].get("err"):
        return []
    ks = keys(tx)
    pre = dict(zip(ks, tx["meta"]["preBalances"]))
    ta = token_accounts(tx)
    out = []
    run = dict(pre)  # lamports courants des comptes WSOL : un virement WSOL déplace des lamports, une fermeture rend le total courant
    for path, ix in instructions(tx):
        p = ix.get("parsed")
        if not isinstance(p, dict):
            continue
        t, info = p.get("type"), p.get("info") or {}
        if ix.get("programId") == SYSTEM and t in ("transfer", "transferWithSeed"):
            out.append({"path": path, "kind": "sol", "src": info["source"], "dst": info["destination"], "amount": int(info["lamports"]),
                        "mint": "SOL", "src_owner_known": True, "dst_owner_known": True})
        elif ix.get("programId") == SYSTEM and t in ("createAccount", "createAccountWithSeed"):
            out.append({"path": path, "kind": "sol_create", "src": info["source"], "dst": info["newAccount"], "amount": int(info["lamports"]),
                        "mint": "SOL", "src_owner_known": True, "dst_owner_known": True})
        elif ix.get("programId") in (TOKEN, TOKEN22) and t in ("transfer", "transferChecked"):
            s, d = info["source"], info["destination"]
            mint = info.get("mint") or (ta.get(s) or ta.get(d) or (None, None))[1]
            amt = int(info["tokenAmount"]["amount"]) if "tokenAmount" in info else int(info["amount"])
            so, do = ta.get(s, (None, None))[0], ta.get(d, (None, None))[0]
            if mint == WSOL:
                run[s] = run.get(s, 0) - amt
                run[d] = run.get(d, 0) + amt
            out.append({"path": path, "kind": "token", "src": so or s, "dst": do or d, "amount": amt, "mint": mint, "src_account": s, "dst_account": d,
                        "authority": info.get("authority") or info.get("multisigAuthority"), "src_owner_known": so is not None, "dst_owner_known": do is not None})
        elif ix.get("programId") in (TOKEN, TOKEN22) and t == "closeAccount":
            a = info["account"]
            out.append({"path": path, "kind": "close", "src": (ta.get(a) or (a, None))[0] or a, "dst": info["destination"], "amount": run.get(a, 0),
                        "mint": (ta.get(a) or (None, None))[1], "account": a, "src_owner_known": a in ta, "dst_owner_known": True})
    return out


def sol_delta(tx, addr):
    ks = keys(tx)
    m = tx["meta"]
    return sum(m["postBalances"][i] - m["preBalances"][i] for i, k in enumerate(ks) if k == addr)


def token_delta(tx, owner, mint):
    d = 0
    for side, sgn in (("preTokenBalances", -1), ("postTokenBalances", 1)):
        for b in tx["meta"].get(side) or []:
            if b.get("owner") == owner and b["mint"] == mint:
                d += sgn * int(b["uiTokenAmount"]["amount"])
    return d


def programs(tx):
    return sorted({ix.get("programId") for _, ix in instructions(tx)} - {None})


def signers(tx):
    return [k["pubkey"] for k in tx["transaction"]["message"]["accountKeys"] if isinstance(k, dict) and k.get("signer")]


B58 = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"


def b58e(b):
    n, out = int.from_bytes(b, "big"), ""
    while n:
        n, r = divmod(n, 58)
        out = B58[r] + out
    return "1" * (len(b) - len(b.lstrip(b"\0"))) + out


def bstr(b, i):
    """Chaîne Borsh : longueur u32 little-endian puis octets UTF-8."""
    n = struct.unpack_from("<I", b, i)[0]
    return b[i + 4:i + 4 + n].decode("utf-8", "replace").rstrip("\0"), i + 4 + n


def pump_create_event(tx):
    """CreateEvent de Pump.fun (journal « Program data: ») : nom, symbole, URI, mint, courbe, créateur. Immuable une fois émis."""
    for line in tx["meta"].get("logMessages") or []:
        if line.startswith("Program data: "):
            b = base64.b64decode(line[14:])
            try:
                name, i = bstr(b, 8)
                sym, i = bstr(b, i)
                uri, i = bstr(b, i)
                return {"name": name, "symbol": sym, "uri": uri, "mint": b58e(b[i:i + 32]), "bonding_curve": b58e(b[i + 32:i + 64]), "user": b58e(b[i + 64:i + 96])}
            except (struct.error, UnicodeDecodeError, IndexError):
                continue
    return None
