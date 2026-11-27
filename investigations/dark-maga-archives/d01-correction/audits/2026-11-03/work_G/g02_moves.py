#!/usr/bin/env python3
"""Parseur propre de net/<wallet>.jsonl.gz (historiques complets de l'auditeur C), en flux, sans agrégat en mémoire.
Écrit audits_work/G/net_moves.csv.gz (une ligne par virement SOL ou SPL touchant le propriétaire de l'historique)
et audits_work/G/net_txs.csv.gz (une ligne par transaction : deltas du propriétaire et programmes).
Contrôle intégré : pour chaque historique, somme des deltas natifs signés = dernier solde vu moins premier solde pré, à une rupture près comptée."""
import csv, gzip, json, os, sys, time
NET = "/Volumes/VERBATIM HD/Dark-MAGA-Investigation/audits_work/C/net/"
G = "/Volumes/VERBATIM HD/Dark-MAGA-Investigation/audits_work/G/"
BASE = {"11111111111111111111111111111111", "ComputeBudget111111111111111111111111111111", "TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA",
        "TokenzQdBNbLqP5VEhdkAS6EPFLC1PHnBqCXEpPxuEb", "ATokenGPvbdGVxr1b2hvZbsiqW5xWH25efTNsLJA8knL", "MemoSq4gqABAXKb96qnH8TysNcWxMyWCqXgDLGmfcHr",
        "Memo1UhkJRfHyvLMcVucJwxXeuD728EqVDDwQDxFMNo",
        "DeJBGdMFa1uynnnKiwrVioatTuHmNLpyFKnmB5kaFdzQ"}  # enveloppe de virement de portefeuille (725 tx lues : création du compte de jetons puis Transfer), voir g37
MINT = {"So11111111111111111111111111111111111111112": "WSOL", "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v": "USDC",
        "Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB": "USDT", "7D7BRcBYepfi77vxySapmeqRNN1wsBBxnFPJGbH5pump": "DMAGA"}
fm = gzip.open(G + "net_moves.csv.gz", "wt", compresslevel=5, newline=""); wm = csv.writer(fm)
wm.writerow("owner bt slot txidx sig signed payer fee kind asset mint src dst raw decimals src_acct dst_acct pure err".split())
ft = gzip.open(G + "net_txs.csv.gz", "wt", compresslevel=5, newline=""); wt = csv.writer(ft)
wt.writerow("owner bt slot txidx sig signed payer signers fee native_delta wsol_delta usdc_delta usdt_delta dmaga_delta n_other_mints programs pure err".split())
stat = open(G + "net_stats.csv", "w"); print("owner,n_lines,n_tx,first_bt,last_bt,breaks", file=stat)
NETG = G + "net/"
files = [(NET, f) for f in sorted(os.listdir(NET)) if f.endswith(".jsonl.gz") and not f.startswith(("._", "ctrl_", "probe_", "absent_"))] + [(NETG, f) for f in sorted(os.listdir(NETG)) if f.endswith(".jsonl.gz") and not f.endswith(".desc.jsonl.gz") and not f.startswith("._")]
for DIR, fn in files:
    A = fn.split(".")[0]; seen = set(); nl = 0; first = last = None; breaks = 0; prev_post = None
    for line in gzip.open(DIR + fn, "rt"):
        nl += 1
        t = json.loads(line); s = t["transaction"]["signatures"][0]
        if s in seen: continue
        seen.add(s)
        m = t["transaction"]["message"]; meta = t["meta"]; ks = m["accountKeys"]
        keys = [k["pubkey"] for k in ks]; signers = [k["pubkey"] for k in ks if k.get("signer")]
        err = "1" if meta.get("err") else "0"
        bt = t["blockTime"]; first = first or bt; last = bt
        acct = {}  # compte de jetons -> (propriétaire, mint, décimales)
        for side in ("preTokenBalances", "postTokenBalances"):
            for b in meta.get(side) or []:
                acct[keys[b["accountIndex"]]] = (b.get("owner"), b["mint"], b["uiTokenAmount"]["decimals"])
        seq = list(m["instructions"])
        for g in meta.get("innerInstructions") or []: seq += g["instructions"]
        for i in seq:   # comptes créés dans la tx et fermés aussitôt : absents des soldes
            p = i.get("parsed")
            if isinstance(p, dict) and isinstance(p.get("info"), dict):
                inf = p["info"]
                if i.get("program") == "spl-associated-token-account" and inf.get("account") and inf["account"] not in acct:
                    acct[inf["account"]] = (inf.get("wallet"), inf.get("mint"), None)
                if p.get("type", "").startswith("initializeAccount") and inf.get("account") and inf["account"] not in acct:
                    acct[inf["account"]] = (inf.get("owner"), inf.get("mint"), None)
        progs = sorted({i.get("programId") or "" for i in seq})
        pure = "1" if set(progs) <= BASE else "0"
        idx = keys.index(A) if A in keys else None
        nat = (meta["postBalances"][idx] - meta["preBalances"][idx]) if idx is not None else 0
        if idx is not None:
            if prev_post is not None and meta["preBalances"][idx] != prev_post: breaks += 1
            prev_post = meta["postBalances"][idx]
        delta = {}
        for sign, side in ((-1, "preTokenBalances"), (1, "postTokenBalances")):
            for b in meta.get(side) or []:
                if b.get("owner") == A:
                    delta[b["mint"]] = delta.get(b["mint"], 0) + sign * int(b["uiTokenAmount"]["amount"])
        d = lambda k: delta.get(k, 0)
        known = {k for k in MINT}
        wt.writerow([A, bt, t["slot"], t.get("transactionIndex", ""), s, int(A in signers), keys[0], ";".join(signers), meta["fee"], nat,
                     d("So11111111111111111111111111111111111111112"), d("EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"), d("Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB"), d("7D7BRcBYepfi77vxySapmeqRNN1wsBBxnFPJGbH5pump"),
                     sum(1 for k, v in delta.items() if v and k not in known), ";".join(p for p in progs if p not in BASE), pure, err])
        for i in seq:
            p = i.get("parsed")
            if not isinstance(p, dict) or not isinstance(p.get("info"), dict): continue
            inf = p["info"]; ty = p.get("type", "")
            if i.get("program") == "system" and ty in ("transfer", "transferWithSeed", "createAccount", "createAccountWithSeed"):
                a, b = inf.get("source"), inf.get("destination") or inf.get("newAccount")
                if A in (a, b):
                    wm.writerow([A, bt, t["slot"], t.get("transactionIndex", ""), s, int(A in signers), keys[0], meta["fee"], "sys_" + ty, "SOL", "", a, b, int(inf.get("lamports") or 0), 9, "", "", pure, err])
            elif i.get("program") in ("spl-token", "spl-token-2022") and ty in ("transfer", "transferChecked", "transferCheckedWithFee"):
                sa, da = inf.get("source"), inf.get("destination")
                so = acct.get(sa, (None, None, None)); do = acct.get(da, (None, None, None))
                mint = inf.get("mint") or so[1] or do[1]
                auth = inf.get("authority") or inf.get("multisigAuthority")
                src_o = so[0] or auth
                if A in (src_o, do[0], auth):
                    raw = inf["tokenAmount"]["amount"] if "tokenAmount" in inf else inf.get("amount")
                    dec = inf["tokenAmount"]["decimals"] if "tokenAmount" in inf else (so[2] if so[2] is not None else do[2])
                    wm.writerow([A, bt, t["slot"], t.get("transactionIndex", ""), s, int(A in signers), keys[0], meta["fee"], "spl", MINT.get(mint, "other"), mint or "", src_o or "", do[0] or "", raw, dec if dec is not None else "", sa, da, pure, err])
    print(f"{A},{nl},{len(seen)},{first},{last},{breaks}", file=stat)
    print(A[:8], nl, len(seen), "ruptures natives", breaks, flush=True)
fm.close(); ft.close(); stat.close()
