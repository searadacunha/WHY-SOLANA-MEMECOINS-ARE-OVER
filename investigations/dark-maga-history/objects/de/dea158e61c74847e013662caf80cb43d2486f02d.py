"""Transformation d'une transaction brute (jsonParsed) en lignes de flux DMAGA, tous venues confondus.

Principe : le côté venue fait foi. Le SOL d'un swap est la variation des réserves WSOL (ou USDC) des
venues touchés, ou des lamports de la courbe, jamais une valeur déduite d'un routeur. Un acheteur passé
par Jupiter a donc un coût mesuré à l'entrée dans les pools.

kind :
  swap            échange contre SOL ou USDC, attribué au(x) propriétaire(s) non-venue
  transfer        jetons déplacés entre propriétaires, sans contrepartie côté venue
  lp_add / lp_remove   liquidité déposée ou retirée, y compris à sens unique sur un DLMM
  mint_supply     arrivée de l'offre à la création
  internal        mouvement de venue sans propriétaire final (arbitrage entre pools)
  fee_share       part de jetons sous 5 % du swap versée à un tiers (frais de référent, de bot)
"""
from __future__ import annotations

from .config import BONDING_CURVE, MINT, WSOL

USDC = "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"
FEE_SHARE = 0.05  # mesuré : médiane 0,85 %, p90 1 %, 3 adresses sur 1 931 swaps du 14 au 21/07
RAYDIUM_AUTH = "5Q544fKrFoe6tsEbD7S8EmxGTJYAKtTVhAW5Q5pge4j1"


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


def sol_delta(tx: dict, keys: list[str], addr: str) -> int:
    """Variation native (lamports) d'une adresse dans la transaction, frais inclus."""
    meta = tx["meta"]
    try:
        i = keys.index(addr)
    except ValueError:
        return 0
    return meta["postBalances"][i] - meta["preBalances"][i]


def _is_venue_account(d: dict, ray_dmaga: set, ray_wsol: set, venues: set) -> bool:
    if d["owner"] == RAYDIUM_AUTH:
        # l'autorité Raydium possède les réserves de tous ses pools : seules celles de DMAGA comptent
        return d["account"] in ray_dmaga or d["account"] in ray_wsol or d["mint"] == MINT
    return d["owner"] in venues or d["owner"] == BONDING_CURVE


def parse_tx(row: dict, ray_dmaga: set, ray_wsol: set, source: str, venues: set = frozenset()) -> list[dict]:
    """row = élément de getTransactionsForAddress en mode full. Rend les lignes de flux DMAGA."""
    meta = row.get("meta")
    if meta is None:
        raise ValueError(f"transaction sans meta: {row.get('slot')}")
    if meta.get("err") is not None:
        return []
    keys = _keys(row)
    deltas = token_deltas(row, keys)
    dmaga = [d for d in deltas if d["mint"] == MINT]
    if not dmaga:
        return []

    base = {"signature": row["transaction"]["signatures"][0], "slot": row["slot"],
            "tx_index": row.get("transactionIndex"), "block_time": row.get("blockTime"), "fee_payer": keys[0],
            "signers": ",".join(_signers(row)), "fee": meta.get("fee"), "source": source}

    def make(kind, venue, owner, token_delta, sol=0, usdc=0, pool_token=0, pool_sol=0, n=0):
        return {**base, "kind": kind, "venue": venue, "owner": owner, "token_delta": token_delta,
                "sol_lamports": sol, "usdc_raw": usdc, "pool_token_delta": pool_token, "pool_sol_delta": pool_sol,
                "n_owners": n, "owner_native_delta": sol_delta(row, keys, owner) if owner else 0,
                "owner_wsol_delta": sum(d["delta"] for d in deltas if d["mint"] == WSOL and d["owner"] == owner)}

    venue_d, venue_s, venue_u = 0, 0, 0
    touched = set()
    others: dict[str, int] = {}
    for d in deltas:
        if _is_venue_account(d, ray_dmaga, ray_wsol, venues):
            if d["mint"] == MINT:
                venue_d += d["delta"]
                touched.add(d["owner"])
            elif d["mint"] == WSOL:
                venue_s += d["delta"]
                touched.add(d["owner"])
            elif d["mint"] == USDC:
                venue_u += d["delta"]
                touched.add(d["owner"])
        elif d["mint"] == MINT:
            others[d["owner"]] = others.get(d["owner"], 0) + d["delta"]
    curve_d = sum(d["delta"] for d in dmaga if d["owner"] == BONDING_CURVE)
    if curve_d:
        venue_s += sol_delta(row, keys, BONDING_CURVE)
    others = {o: v for o, v in others.items() if v != 0}
    venue = "pumpfun" if curve_d else ("+".join(sorted(v[:8] for v in touched)) or None)
    if venue and RAYDIUM_AUTH in touched and len(touched) == 1:
        venue = "raydium"

    if curve_d > 0 and venue_s > 0 and any(v > 0 for v in others.values()):
        # création de la courbe : l'offre arrive et le créateur achète dans la même transaction.
        # shortcut: le coût inclut le loyer du compte de courbe (environ 0,0015 SOL), négligeable ici.
        rows = [make("mint_supply", "pumpfun", BONDING_CURVE, curve_d + sum(others.values()))]
        for o, v in others.items():
            rows.append(make("swap", "pumpfun", o, v, sol=-venue_s, pool_token=curve_d, pool_sol=venue_s, n=len(others)))
        return rows

    if not venue_d and not touched:
        # transfert pur entre propriétaires
        return [make("transfer", None, o, v, n=len(others)) for o, v in others.items()]

    if not venue_d:
        # venue touché sans mouvement net de DMAGA : ce qui reste est un transfert (route avec intermédiaire)
        if not others:
            return [make("internal", venue, None, 0, sol=-venue_s, usdc=-venue_u, pool_sol=venue_s)]
        return [make("transfer", venue, o, v, n=len(others)) for o, v in others.items()]

    quote = venue_s if venue_s else venue_u
    same_sign = bool(quote) and (venue_d > 0) == (quote > 0)
    if same_sign or not quote:
        # les deux réserves varient dans le même sens, ou une seule varie : dépôt ou retrait de liquidité
        kind = "lp_add" if venue_d > 0 else "lp_remove"
        same = {o: v for o, v in others.items() if (v > 0) == (venue_d < 0)}
        rows = []
        total = sum(same.values())
        for o, v in same.items():
            share = v / total if total else 0
            rows.append(make(kind, venue, o, v, sol=int(round(-venue_s * share)), usdc=int(round(-venue_u * share)),
                             pool_token=venue_d, pool_sol=venue_s, n=len(same)))
        if not same:
            rows.append(make(kind, venue, keys[0], -venue_d, sol=-venue_s, usdc=-venue_u, pool_token=venue_d,
                             pool_sol=venue_s))
        for o, v in others.items():
            if o not in same:
                rows.append(make("transfer", venue, o, v, n=len(others)))
        return rows

    # swap : le venue perd des jetons, le(s) trader(s) en gagnent, et inversement
    want_pos = venue_d < 0
    same = {o: v for o, v in others.items() if (v > 0) == want_pos}
    rows = []
    full = sum(same.values())
    fees = {o: v for o, v in same.items() if full and abs(v) < FEE_SHARE * abs(full)}
    same = {o: v for o, v in same.items() if o not in fees}
    total = sum(same.values())
    for o, v in fees.items():
        rows.append(make("fee_share", venue, o, v, n=len(same)))
    for o, v in sorted(same.items(), key=lambda kv: -abs(kv[1])):
        # plusieurs bénéficiaires : répartition à la quantité (cas routeur, frais de référent)
        share = v / total if total else 0
        rows.append(make("swap", venue, o, v, sol=int(round(-venue_s * share)), usdc=int(round(-venue_u * share)),
                         pool_token=venue_d, pool_sol=venue_s, n=len(same)))
    for o, v in others.items():
        if o not in same and o not in fees:
            rows.append(make("transfer", venue, o, v, n=len(others)))
    if not same:
        rows.append(make("internal", venue, None, -venue_d, sol=-venue_s, usdc=-venue_u, pool_token=venue_d,
                         pool_sol=venue_s))
    return rows
