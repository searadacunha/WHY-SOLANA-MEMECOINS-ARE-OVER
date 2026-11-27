#!/usr/bin/env python3
"""Reconstruction par wallet depuis l'historique complet telecharge (net/<wallet>.jsonl.gz), sans normalize ni trades.parquet.

Sorties dans work_C :
  members_table.csv : pour chaque wallet du groupe, soldes a T_LOW et T_HIGH et T_HIGH+24 h (post-soldes bruts), achats 1re heure, trades du 21/07,
                      ventes et transferts dans les 24 h apres Musk, premier financeur, completude.
  sol_edges.csv     : tous les virements systeme entre wallets du perimetre (groupe, graines, destinataires G41v, expediteurs 9W9b).
  token_moves.csv   : tous les transferts SPL de DMAGA touchant un membre, avec programmes et signataire.
"""
import csv
import gzip
import json
import time
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[2]
NET = Path("/Volumes/VERBATIM HD/Dark-MAGA-Investigation/audits_work/C/net")
MINT = "7D7BRcBYepfi77vxySapmeqRNN1wsBBxnFPJGbH5pump"
WSOL = "So11111111111111111111111111111111111111112"
USDC = "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"
T0, T_WINIG, T_LOW, T_HIGH = 1720922725, 1721577749, 1721588607, 1721590213
BASE = {"ComputeBudget111111111111111111111111111111", "TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA", "ATokenGPvbdGVxr1b2hvZbsiqW5xWH25efTNsLJA8knL",
        "11111111111111111111111111111111", "MemoSq4gqABAXKb96qnH8TysNcWxMyWCqXgDLGmfcHr", "Memo1UhkJRfHyvLMcVucJwxXeuD728EqVDDwQDxFMNo",
        "TokenzQdBNbLqP5VEhdkAS6EPFLC1PHnBqCXEpPxuEb", "DeJBGdMFa1uynnnKiwrVioatTuHmNLpyFKnmB5kaFdzQ", "HQ2UUt18uJqKaQFJhgV9zaTdQxUZjNrsKFgoEDquBkcx",
        "L2TExMFKdjpN9kozasaurPirfHy9P8sbXoAN1qA3S95"}


def utc(t):
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(t))


g = json.load(open(REPO / "data/prevent_groups.json"))[0]
members = sorted(g["members"])
assert len(members) == 33
perim = set(members)
for f in NET.glob("*.jsonl.gz"):
    if not f.name.startswith(("._", "probe", "ctrl", "absent")):
        perim.add(f.name.split(".")[0])

w_sol = csv.writer(open(ROOT / "sol_edges.csv", "w", newline=""))
w_sol.writerow("utc bt src dst lamports sig signer_src programs".split())
w_mv = csv.writer(open(ROOT / "token_moves.csv", "w", newline=""))
w_mv.writerow("utc bt sig member dir counterparty tokens authority payer nonbase_programs".split())
w_tab = csv.DictWriter(open(ROOT / "members_table.csv", "w", newline=""), fieldnames=
                       "wallet n_tx complete first_tx first_funder first_funder_sol first_funder_t held_T0h held_Tlow held_Thigh held_T24 "
                       "buy1h_tokens buy1h_sol buy1h_n trades_winig_high n_trades_0721 sell24_tokens sell24_sol sell24_usdc xferout24_tokens xferin24_tokens "
                       "buys_total_tokens buys_total_sol sells_total_tokens sells_total_sol xfer_in_total xfer_out_total".split())
w_tab.writeheader()
seen_sol = set()
for wallet in sorted(perim):
    path = NET / f"{wallet}.jsonl.gz"
    if not path.exists():
        continue
    cur = NET / f"{wallet}.cursor.json"
    complete = json.loads(cur.read_text())["complete"] if cur.exists() else None
    rows = [json.loads(l) for l in gzip.open(path, "rt")]
    rows.sort(key=lambda t: (t["slot"], t.get("transactionIndex") or 0))
    bal = {}
    snap = {}
    r = defaultdict(float)
    r["wallet"] = wallet
    first_f = None
    n721 = trades_w = 0
    for tx in rows:
        bt = tx["blockTime"]
        for label_t, tt in (("held_T0h", T0 + 3600), ("held_Tlow", T_LOW), ("held_Thigh", T_HIGH), ("held_T24", T_HIGH + 86400)):
            if label_t not in snap and bt >= tt:
                snap[label_t] = sum(bal.values())
        meta = tx["meta"]
        msg = tx["transaction"]["message"]
        keys = [k["pubkey"] for k in msg["accountKeys"]]
        signers = [k["pubkey"] for k in msg["accountKeys"] if k["signer"]]
        seq = list(msg["instructions"])
        for gr in meta.get("innerInstructions") or []:
            seq += gr["instructions"]
        progs = {i["programId"] for i in seq}
        nonbase = sorted(progs - BASE)
        own, pre, post = {}, {}, {}
        wsol = 0
        usdc = 0
        for side, name in ((-1, "preTokenBalances"), (1, "postTokenBalances")):
            for b in meta.get(name) or []:
                acc = keys[b["accountIndex"]]
                amt = int(b["uiTokenAmount"]["amount"])
                if b["mint"] == MINT:
                    own[acc] = b.get("owner", "")
                    (pre if side == -1 else post)[acc] = amt
                if b.get("owner") == wallet and b["mint"] == WSOL:
                    wsol += side * amt
                if b.get("owner") == wallet and b["mint"] == USDC:
                    usdc += side * amt
        d = 0
        for acc, o in own.items():
            if o == wallet:
                delta = post.get(acc, 0) - pre.get(acc, 0)
                d += delta
                bal[acc] = post.get(acc, 0)
        native = (meta["postBalances"][keys.index(wallet)] - meta["preBalances"][keys.index(wallet)]) if wallet in keys else 0
        fee = meta["fee"] if signers and signers[0] == wallet else 0
        sol_net = native + wsol + fee
        is_swap = bool(nonbase)
        sig = tx["transaction"]["signatures"][0]
        if d and is_swap:
            if d > 0:
                r["buys_total_tokens"] += d / 1e6
                r["buys_total_sol"] += -sol_net / 1e9
                if bt < T0 + 3600:
                    r["buy1h_tokens"] += d / 1e6
                    r["buy1h_sol"] += -sol_net / 1e9
                    r["buy1h_n"] += 1
            else:
                r["sells_total_tokens"] += -d / 1e6
                r["sells_total_sol"] += sol_net / 1e9
                if T_HIGH <= bt < T_HIGH + 86400:
                    r["sell24_tokens"] += -d / 1e6
                    r["sell24_sol"] += sol_net / 1e9
                    r["sell24_usdc"] += usdc / 1e6
            if 1721520000 <= bt < 1721606400:
                n721 += 1
            if T_WINIG <= bt <= T_HIGH:
                trades_w += 1
        for ins in seq:
            p = ins.get("parsed")
            if not isinstance(p, dict):
                continue
            info = p.get("info") if isinstance(p.get("info"), dict) else {}
            if ins.get("program") == "system" and p.get("type") == "transfer":
                s, de, lam = info.get("source"), info.get("destination"), int(info.get("lamports") or 0)
                if de == wallet and lam >= 1_000_000 and first_f is None:
                    first_f = (s, lam / 1e9, bt)
                if s in perim and de in perim and (sig, s, de, lam) not in seen_sol:
                    seen_sol.add((sig, s, de, lam))
                    w_sol.writerow([utc(bt), bt, s, de, lam, sig, s in signers, "|".join(nonbase)])
            if ins.get("program") == "spl-token" and p.get("type") in ("transfer", "transferChecked"):
                so, de = own.get(info.get("source")), own.get(info.get("destination"))
                if so is None and de is None:
                    continue
                amt = int(info.get("amount") or info["tokenAmount"]["amount"])
                if so == wallet and de != wallet:
                    w_mv.writerow([utc(bt), bt, sig, wallet, "out", de or info.get("destination"), amt / 1e6, info.get("authority") or info.get("multisigAuthority"), signers[0], "|".join(nonbase)])
                    if not is_swap:
                        r["xfer_out_total"] += amt / 1e6
                        if T_HIGH <= bt < T_HIGH + 86400:
                            r["xferout24_tokens"] += amt / 1e6
                elif de == wallet and so != wallet:
                    w_mv.writerow([utc(bt), bt, sig, wallet, "in", so or info.get("source"), amt / 1e6, info.get("authority") or info.get("multisigAuthority"), signers[0], "|".join(nonbase)])
                    if not is_swap:
                        r["xfer_in_total"] += amt / 1e6
                        if T_HIGH <= bt < T_HIGH + 86400:
                            r["xferin24_tokens"] += amt / 1e6
    for label_t in ("held_T0h", "held_Tlow", "held_Thigh", "held_T24"):
        r[label_t] = snap.get(label_t, sum(bal.values())) / 1e12
    r.update({"n_tx": len(rows), "complete": complete, "first_tx": utc(rows[0]["blockTime"]) if rows else "", "trades_winig_high": trades_w, "n_trades_0721": n721})
    if first_f:
        r.update({"first_funder": first_f[0], "first_funder_sol": first_f[1], "first_funder_t": utc(first_f[2])})
    w_tab.writerow(dict(r))
print("ok", len(perim))
