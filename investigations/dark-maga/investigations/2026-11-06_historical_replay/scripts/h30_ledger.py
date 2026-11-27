"""Grand livre décodé d'un wallet sur une fenêtre : une ligne par transaction réussie, mouvements instruction par instruction.

usage: h30_ledger.py <wallet> <since> <until> <sortie.csv>. Exige les signatures (h10) et les transactions en cache (h11) :
une transaction absente du cache arrête le script (pas de trou muet). Programmes nommés seulement s'ils sont connus ;
un programme n'identifie jamais une personne."""
import csv
import gzip
import json
import sys
from h_lib import DMAGA, EXT, utc
from h_decode import WSOL, movements, programs, signers, sol_delta, token_delta

NAMES = {"PERPHjGBqRHArX4DySjwM6UJHiR3sWAatqfdBS2qQJu": "jupiter_perps", "6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P": "pumpfun",
         "675kPX9MHTjS2zt1qfr1NYHuzeLXfQM9H24wFSUt1Mp8": "raydium_v4", "JUP6LkbZbjS1jKKwapdHNy74zcZ3tLUZoi5QNyVTaV4": "jupiter_v6",
         "DCA265Vj8a9CEuX1eb1LWRnDT7uK6q1xMipnNyatn23M": "jupiter_dca", "whirLbMiicVdio4qvUfM5KAg6Ct8VwpYzGff3uctyCc": "orca",
         "CAMMCzo5YL8w4VFF8KVHrK22GGUsp5VTaW7grrKgrWqK": "raydium_clmm", "LBUZKhRxPF3XUpBCjp4YzTKgLccjZhTSDM9YuVaPwxo": "meteora_dlmm"}
BORING = {"11111111111111111111111111111111", "ComputeBudget111111111111111111111111111111", "TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA",
          "ATokenGPvbdGVxr1b2hvZbsiqW5xWH25efTNsLJA8knL", "MemoSq4gqABAXKb96qnH8TysNcWxMyWCqXgDLGmfcHr"}


def cached(sig):
    p = EXT / "pub" / sig[:2] / (sig + ".json.gz")
    if not p.exists():
        raise SystemExit(f"transaction absente du cache : {sig} (lancer h11)")
    return json.loads(gzip.decompress(p.read_bytes()))


def rows(wallet, since, until):
    sigs = json.loads((EXT / f"sigs_{wallet}.json").read_text())["sigs"]
    for x in sorted((x for x in sigs if not x.get("err") and since <= x["blockTime"] < until), key=lambda x: (x["slot"], x["signature"])):
        t = cached(x["signature"])
        mv = [m for m in movements(t) if wallet in (m["src"], m["dst"])]
        progs = [NAMES.get(p, p[:8]) for p in programs(t) if p not in BORING]
        yield {"utc": utc(t["blockTime"]), "block_time": t["blockTime"], "slot": t["slot"], "signature": x["signature"],
               "signers": ";".join(signers(t)), "wallet_signed": wallet in signers(t), "programs": ";".join(progs),
               "sol_delta_lamports": sol_delta(t, wallet), "fee_lamports": t["meta"]["fee"] if signers(t)[0] == wallet else 0,
               "wsol_delta_raw": token_delta(t, wallet, WSOL), "dmaga_delta_raw": token_delta(t, wallet, DMAGA),
               "movements": " | ".join(f"{m['path']}:{m['kind']}:{m['src']}>{m['dst']}:{m['amount']}:{m['mint']}" for m in mv)}


if __name__ == "__main__":
    w, a, b, out = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
    rs = list(rows(w, a, b))
    with open(out, "w", newline="") as f:
        wr = csv.DictWriter(f, fieldnames=list(rs[0]))
        wr.writeheader()
        wr.writerows(rs)
    print(out, len(rs), "transactions")
