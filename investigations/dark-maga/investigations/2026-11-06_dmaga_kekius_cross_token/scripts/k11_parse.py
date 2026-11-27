"""Transactions Solana brutes -> mouvements par propriétaire (jeton étudié, SOL natif du signataire, WSOL).

Règle : delta jeton = post - pre par propriétaire (owner des comptes de jetons) ; delta SOL = lamports du compte
signataire (frais inclus). Aucun montant n'est déduit d'un log : seulement des soldes avant/après."""
from collections import defaultdict


def keys(tx):
    return [k["pubkey"] if isinstance(k, dict) else k for k in tx["transaction"]["message"]["accountKeys"]]


def signers(tx):
    return [k["pubkey"] for k in tx["transaction"]["message"]["accountKeys"] if isinstance(k, dict) and k.get("signer")]


def token_deltas(tx, mint):
    """{owner: delta en unités brutes} pour un mint ; comptes absents d'un côté comptés à 0."""
    m = tx["meta"]
    d = defaultdict(int)
    for side, sgn in (("preTokenBalances", -1), ("postTokenBalances", 1)):
        for b in m.get(side) or []:
            if b["mint"] == mint:
                d[b.get("owner")] += sgn * int(b["uiTokenAmount"]["amount"])
    return {k: v for k, v in d.items() if v}


def sol_deltas(tx):
    m = tx["meta"]
    ks = keys(tx)
    return {ks[i]: m["postBalances"][i] - m["preBalances"][i] for i in range(len(ks)) if m["postBalances"][i] != m["preBalances"][i]}


def ix_names(tx):
    return [l.split("Instruction: ", 1)[1] for l in (tx["meta"].get("logMessages") or []) if "Instruction: " in l]


def programs(tx):
    out = set()
    for ix in tx["transaction"]["message"]["instructions"]:
        out.add(ix.get("programId"))
    for inner in tx["meta"].get("innerInstructions") or []:
        for ix in inner["instructions"]:
            out.add(ix.get("programId"))
    return out
