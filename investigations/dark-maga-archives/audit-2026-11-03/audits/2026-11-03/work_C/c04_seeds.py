#!/usr/bin/env python3
"""Chronologie brute de chaque graine depuis les transactions completes telechargees (audits_work/C/net).
Sorties dans work_C : chrono_<prefixe>.csv (une ligne par transaction) et seeds_summary.txt.
Pour chaque transaction : delta lamports du wallet (post-pre), delta DMAGA par proprietaire, autres jetons,
virements systeme entrants et sortants (externes et internes), transferts SPL de DMAGA avec proprietaires, programmes.
"""
import csv
import gzip
import json
import time
from collections import Counter, defaultdict
from pathlib import Path

MINT = "7D7BRcBYepfi77vxySapmeqRNN1wsBBxnFPJGbH5pump"
WSOL = "So11111111111111111111111111111111111111112"
SEEDS = ["8YLEuUtZ4eFMJbf46oNb1CeG6dYFWGyxnQSh9hrgzBzR", "5QhJJcFZu2ashyKyWSTGHcsyo6ZBCbpVuJqeutvQHScd",
         "G41vRrsHShLEvwMj58ruhqJycGfAtWXxtLD56uFExL8E", "9W9b3zgHH9mCEHDhsdbnbEPHStm9vvXS4aia4DWHBxpL"]
NET = Path("/Volumes/VERBATIM HD/Dark-MAGA-Investigation/audits_work/C/net")
WORK = Path(__file__).resolve().parent
PN = {"675kPX9MHTjS2zt1qfr1NYHuzeLXfQM9H24wFSUt1Mp8": "raydium_v4", "6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P": "pumpfun",
      "JUP6LkbZbjS1jKKwapdHNy74zcZ3tLUZoi5QNyVTaV4": "jup6", "JUP4Fb2cqiRUcaTHdrPC8h2gNsA2ETXiPDD33WcGuJB": "jup4",
      "DCA265Vj8a9CEuX1eb1LWRnDT7uK6q1xMipnNyatn23M": "jup_dca", "jupoNjAxXgZ4rjzxzPMP4oxduvQsQtZzyknqvzYNrNu": "jup_limit",
      "whirLbMiicVdio4qvUfM5KAg6Ct8VwpYzGff3uctyCc": "orca", "LBUZKhRxPF3XUpBCjp4YzTKgLccjZhTSDM9YuVaPwxo": "meteora_dlmm",
      "CAMMCzo5YL8w4VFF8KVHrK22GGUsp5VTaW7grrKgrWqK": "raydium_clmm", "CPMMoo8L3F4NbTegBCKVNunggL7H1ZpdTHKxQB5qKP1C": "raydium_cpmm",
      "Eo7WjKq67rjJQSZxS6z3YkapzY3eMj6Xy8X5EQVn5UaB": "meteora_amm", "pAMMBay6oceH9fJKBRHGP5D4bD4sWpmSwMn52FMfXEA": "pumpswap",
      "TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA": "spl", "ATokenGPvbdGVxr1b2hvZbsiqW5xWH25efTNsLJA8knL": "ata",
      "11111111111111111111111111111111": "system", "ComputeBudget111111111111111111111111111111": "cb",
      "MemoSq4gqABAXKb96qnH8TysNcWxMyWCqXgDLGmfcHr": "memo", "Memo1UhkJRfHyvLMcVucJwxXeuD728EqVDDwQDxFMNo": "memo1",
      "TokenzQdBNbLqP5VEhdkAS6EPFLC1PHnBqCXEpPxuEb": "token2022", "metaqbxxUerdq28cj1RbAWkYQm3ybzjb6a8bt518x1s": "metaplex"}


def utc(t):
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(t))


def walk(tx):
    msg = tx["transaction"]["message"]
    for ins in msg["instructions"]:
        yield ins
    for grp in tx["meta"].get("innerInstructions") or []:
        for ins in grp["instructions"]:
            yield ins


def main():
    fs = open(WORK / "seeds_summary.txt", "w")
    for seed in SEEDS:
        rows = []
        with gzip.open(NET / f"{seed}.jsonl.gz", "rt") as f:
            for line in f:
                rows.append(json.loads(line))
        rows.sort(key=lambda t: (t["slot"], t.get("transactionIndex") or 0))
        out = WORK / f"chrono_{seed[:6]}.csv"
        w = csv.writer(open(out, "w", newline=""))
        w.writerow("utc sig slot txidx payer is_signer sol_delta dmaga_delta_seed other_token_deltas sys_in sys_out dmaga_moves programs".split())
        sys_in, sys_out, n_in, n_out = Counter(), Counter(), Counter(), Counter()
        progs = Counter()
        tot_d = 0
        n_payer = 0
        for tx in rows:
            meta = tx["meta"]
            msg = tx["transaction"]["message"]
            keys = [k["pubkey"] for k in msg["accountKeys"]]
            signers = [k["pubkey"] for k in msg["accountKeys"] if k["signer"]]
            sig = tx["transaction"]["signatures"][0]
            sol = meta["postBalances"][keys.index(seed)] - meta["preBalances"][keys.index(seed)] if seed in keys else 0
            n_payer += signers[0] == seed
            # token : par compte, proprietaire
            own = {}
            bal = defaultdict(lambda: [0, 0])
            for side, name in ((0, "preTokenBalances"), (1, "postTokenBalances")):
                for b in meta.get(name) or []:
                    a = keys[b["accountIndex"]]
                    own[a] = (b.get("owner", ""), b["mint"], b["uiTokenAmount"]["decimals"])
                    bal[a][side] = int(b["uiTokenAmount"]["amount"])
            dm = 0
            oth = Counter()
            for a, (o, m, dec) in own.items():
                d = bal[a][1] - bal[a][0]
                if o == seed:
                    if m == MINT:
                        dm += d
                    elif d:
                        oth[m] += d / 10 ** dec
            tot_d += dm
            s_in, s_out, mv = [], [], []
            pset = []
            for ins in walk(tx):
                pid = ins.get("programId")
                nm = PN.get(pid, pid)
                if nm not in pset:
                    pset.append(nm)
                p = ins.get("parsed")
                if not isinstance(p, dict):
                    continue
                info = p.get("info", {}) if isinstance(p.get("info"), dict) else {}
                if ins.get("program") == "system" and p.get("type") in ("transfer", "transferWithSeed", "createAccount"):
                    src = info.get("source")
                    dst = info.get("destination") or info.get("newAccount")
                    amt = int(info.get("lamports") or 0)
                    if dst == seed:
                        s_in.append(f"{src}:{amt}")
                        sys_in[src] += amt
                        n_in[src] += 1
                    elif src == seed:
                        dst_o = own.get(dst, ("", "", 0))
                        s_out.append(f"{dst}:{amt}" + (f"(ta_de:{dst_o[0]})" if dst_o[0] else ""))
                        if dst_o[0] != seed:
                            sys_out[dst] += amt
                            n_out[dst] += 1
                if ins.get("program") == "spl-token" and p.get("type") in ("transfer", "transferChecked"):
                    s, d = info.get("source"), info.get("destination")
                    so, dso = own.get(s), own.get(d)
                    if (so and so[1] == MINT) or (dso and dso[1] == MINT):
                        amt = int(info.get("amount") or info["tokenAmount"]["amount"])
                        mv.append(f"{so[0] if so else s}>{dso[0] if dso else d}:{amt}")
            for x in pset:
                progs[x] += 1
            w.writerow([utc(tx["blockTime"]), sig, tx["slot"], tx.get("transactionIndex"), signers[0], seed in signers, sol, dm,
                        ";".join(f"{m}:{v:.6f}" for m, v in oth.items()), ";".join(s_in), ";".join(s_out), ";".join(mv), "|".join(pset)])
        fs.write(f"\n=== {seed} n={len(rows)} premier={utc(rows[0]['blockTime'])} dernier={utc(rows[-1]['blockTime'])} payeur={n_payer} delta_dmaga_net={tot_d/1e6:.3f}\n")
        fs.write(f"programmes: {progs.most_common(25)}\n")
        fs.write(f"contreparties SOL entrantes distinctes={len(sys_in)} total={sum(sys_in.values())/1e9:.4f}\n")
        for a, v in sys_in.most_common(25):
            fs.write(f"  IN  {a} {v/1e9:.4f} SOL n={n_in[a]}\n")
        fs.write(f"contreparties SOL sortantes distinctes={len(sys_out)} total={sum(sys_out.values())/1e9:.4f}\n")
        for a, v in sys_out.most_common(25):
            fs.write(f"  OUT {a} {v/1e9:.4f} SOL n={n_out[a]}\n")
    fs.close()


if __name__ == "__main__":
    main()
