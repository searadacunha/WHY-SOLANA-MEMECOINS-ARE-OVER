"""Parseur propre commun à work_G : transaction jsonParsed -> virements attribués à leur propriétaire. Test de g_lib en bas (python3 g_lib.py)."""
import gzip, json, os
NETC = "/Volumes/VERBATIM HD/Dark-MAGA-Investigation/audits_work/C/net/"
NETG = "/Volumes/VERBATIM HD/Dark-MAGA-Investigation/audits_work/G/net/"
BASE = {"11111111111111111111111111111111", "ComputeBudget111111111111111111111111111111", "TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA", "TokenzQdBNbLqP5VEhdkAS6EPFLC1PHnBqCXEpPxuEb",
        "ATokenGPvbdGVxr1b2hvZbsiqW5xWH25efTNsLJA8knL", "MemoSq4gqABAXKb96qnH8TysNcWxMyWCqXgDLGmfcHr", "Memo1UhkJRfHyvLMcVucJwxXeuD728EqVDDwQDxFMNo",
        "DeJBGdMFa1uynnnKiwrVioatTuHmNLpyFKnmB5kaFdzQ"}  # enveloppe de virement de portefeuille (725 tx lues : création du compte de jetons puis Transfer), voir g37
MINT = {"So11111111111111111111111111111111111111112": "WSOL", "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v": "USDC", "Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB": "USDT", "7D7BRcBYepfi77vxySapmeqRNN1wsBBxnFPJGbH5pump": "DMAGA"}
# Hot wallets étiquetés Coinbase par Dune, et famille présumée (mêmes balayages que les dépôts témoins de C, sans étiquette publique) : présumée seulement.
CB = {"H8sMJSCQxfKiFTCfDR3DUMLPwcRbM61LGFJ8N4dK3WjS": "Coinbase 1", "2AQdpHJ2JpcEgPiATUXjQxA8QmafFegfQwSLWSprPicm": "Coinbase 2", "GJRs4FwHtemZ5ZE9x3FNvJ8TMwitKTh21yxdRPqn7npE": "Coinbase 3"}
FAM = {"FpwQQhQQoEaVu3WU2qZMfF1hx48YyfwsLoRgXG83E99Q", "D89hHJT5Aqyx1trP6EnGY9jJUB3whgnq3aUvvCqedvzf", "DPqsobysNf5iA9w7zrQM8HLzCKZEDMkZsWbiidsAt1xo", "5g7yNHyGLJ7fiQ9SN9mf47opDnMjc585kqXWt6d7aBWs"}


def history(a):
    """Lignes de l'historique de a : C d'abord, puis G (prolongement ou historique propre), dédupliquées par signature."""
    seen = set()
    for p in (NETC + a + ".jsonl.gz", NETG + a + ".jsonl.gz", NETG + a + ".win.jsonl.gz"):
        if os.path.exists(p):
            for l in gzip.open(p, "rt"):
                t = json.loads(l); s = t["transaction"]["signatures"][0]
                if s not in seen:
                    seen.add(s); yield t


def parse(t, A=None):
    """Retourne dict : sig, bt, signers, payer, fee, pure, progs, nat (delta natif par clé), moves [(kind, asset, mint, src, dst, raw, dec)]."""
    m = t["transaction"]["message"]; meta = t["meta"]; ks = m["accountKeys"]
    keys = [k["pubkey"] for k in ks]; signers = [k["pubkey"] for k in ks if k.get("signer")]
    acct = {}
    for side in ("preTokenBalances", "postTokenBalances"):
        for b in meta.get(side) or []:
            acct[keys[b["accountIndex"]]] = (b.get("owner"), b["mint"], b["uiTokenAmount"]["decimals"])
    seq = list(m["instructions"])
    for g in meta.get("innerInstructions") or []: seq += g["instructions"]
    for i in seq:
        p = i.get("parsed")
        if isinstance(p, dict) and isinstance(p.get("info"), dict):
            inf = p["info"]
            if i.get("program") == "spl-associated-token-account" and inf.get("account") and inf["account"] not in acct: acct[inf["account"]] = (inf.get("wallet"), inf.get("mint"), None)
            if p.get("type", "").startswith("initializeAccount") and inf.get("account") and inf["account"] not in acct: acct[inf["account"]] = (inf.get("owner"), inf.get("mint"), None)
    progs = sorted({i.get("programId") or "" for i in seq})
    moves = []
    for i in seq:
        p = i.get("parsed")
        if not isinstance(p, dict) or not isinstance(p.get("info"), dict): continue
        inf = p["info"]; ty = p.get("type", "")
        if i.get("program") == "system" and ty in ("transfer", "transferWithSeed", "createAccount", "createAccountWithSeed"):
            moves.append(("sys_" + ty, "SOL", "", inf.get("source"), inf.get("destination") or inf.get("newAccount"), int(inf.get("lamports") or 0), 9))
        elif i.get("program") in ("spl-token", "spl-token-2022") and ty in ("transfer", "transferChecked", "transferCheckedWithFee"):
            sa, da = inf.get("source"), inf.get("destination")
            so = acct.get(sa, (None, None, None)); do = acct.get(da, (None, None, None))
            mint = inf.get("mint") or so[1] or do[1]
            raw = int(inf["tokenAmount"]["amount"]) if "tokenAmount" in inf else int(inf.get("amount") or 0)
            dec = inf["tokenAmount"]["decimals"] if "tokenAmount" in inf else (so[2] if so[2] is not None else do[2])
            moves.append(("spl", MINT.get(mint, "other"), mint, so[0] or inf.get("authority") or inf.get("multisigAuthority"), do[0], raw, dec))
    nat = {keys[i]: meta["postBalances"][i] - meta["preBalances"][i] for i in range(len(keys)) if meta["postBalances"][i] != meta["preBalances"][i]}
    d = {}
    for sign, side in ((-1, "preTokenBalances"), (1, "postTokenBalances")):
        for b in meta.get(side) or []:
            k = (b.get("owner"), b["mint"]); d[k] = d.get(k, 0) + sign * int(b["uiTokenAmount"]["amount"])
    return {"sig": t["transaction"]["signatures"][0], "bt": t["blockTime"], "slot": t["slot"], "signers": signers, "payer": keys[0], "fee": meta["fee"], "pure": set(progs) <= BASE,
            "progs": [p for p in progs if p not in BASE], "nat": nat, "tok": {k: v for k, v in d.items() if v}, "moves": moves, "keys": keys, "err": meta.get("err") is not None,
            "pre": dict(zip(keys, meta["preBalances"])), "post": dict(zip(keys, meta["postBalances"]))}


if __name__ == "__main__":  # auto-contrôle sur un fait connu : dépôt de 0,593 SOL du créateur vers 9W9b
    S = "65aNPjoC8nb4yUu3oD5HGzSvyC9DLJZEK1LrkDD8hEXPzdv8Y4FJRgJEXZXXbDuHtYi8UNU7XYdmycKwNi2BS3g2"
    W = "9W9b3zgHH9mCEHDhsdbnbEPHStm9vvXS4aia4DWHBxpL"; C = "8YLEuUtZ4eFMJbf46oNb1CeG6dYFWGyxnQSh9hrgzBzR"
    x = next(parse(t) for t in history(W) if t["transaction"]["signatures"][0] == S)
    assert ("sys_transfer", "SOL", "", C, W, 593000000, 9) in x["moves"] and x["pure"] and x["signers"] == [C], x
    print("g_lib ok")
