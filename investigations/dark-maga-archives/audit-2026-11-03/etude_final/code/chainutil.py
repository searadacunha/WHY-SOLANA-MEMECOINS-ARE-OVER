"""Copie figée des lectures de transaction utilisées par l'étude, pour que le parseur principal reste modifiable."""


def _keys(tx: dict) -> list[str]:
    keys = tx["transaction"]["message"]["accountKeys"]
    return [k["pubkey"] if isinstance(k, dict) else k for k in keys]


def _signers(tx: dict) -> list[str]:
    keys = tx["transaction"]["message"]["accountKeys"]
    return [k["pubkey"] for k in keys if isinstance(k, dict) and k.get("signer")]


def token_deltas(tx: dict, keys: list[str]) -> list[dict]:
    """Une ligne par (compte de jetons, mint) dont le solde change. Montants entiers bruts."""
    meta = tx["meta"]
    pre = {(b["accountIndex"], b["mint"]): b for b in (meta.get("preTokenBalances") or [])}
    post = {(b["accountIndex"], b["mint"]): b for b in (meta.get("postTokenBalances") or [])}
    out = []
    for k in set(pre) | set(post):
        a, b = pre.get(k), post.get(k)
        va = int(a["uiTokenAmount"]["amount"]) if a else 0
        vb = int(b["uiTokenAmount"]["amount"]) if b else 0
        if va == vb:
            continue
        src = b or a
        owner = (b or {}).get("owner") or (a or {}).get("owner")
        out.append({"index": k[0], "account": keys[k[0]], "mint": k[1], "owner": owner,
                    "delta": vb - va, "post": vb, "pre": va, "decimals": src["uiTokenAmount"]["decimals"]})
    return sorted(out, key=lambda d: d["index"])
