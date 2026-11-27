"""DMAGA : part des jetons sortis du vault Raydium v4 face aux autres réserves avant S, depuis raw/full_mint.
Une réserve = owner non signataire dont DMAGA et un autre mint varient en sens opposés dans la transaction.
Sortie : b07_dmaga_venues.csv (par owner et fenêtre) et résumé imprimé."""
import csv, gzip, json, os
from pathlib import Path
EXT = Path("/Volumes/VERBATIM HD/Dark-MAGA-Investigation")
HERE = Path(__file__).parent
MINT = "7D7BRcBYepfi77vxySapmeqRNN1wsBBxnFPJGbH5pump"
WSOL = "So11111111111111111111111111111111111111112"
AUTH = "5Q544fKrFoe6tsEbD7S8EmxGTJYAKtTVhAW5Q5pge4j1"
S = 478219 * 3600
WIN = {"S-24h": (S - 24 * 3600, S), "S-96h": (S - 96 * 3600, S), "E-3h_16h02": (S - 3 * 3600, S), "avant_S": (0, S)}
ag = {w: {} for w in WIN}  # owner -> [tok_sortis, sol_entres, n]  ; peu d'owners réserves
buyers = {w: {} for w in WIN}
d = EXT / "raw/full_mint/t1720922725"
last = 0
n = 0
for fn in sorted(x for x in os.listdir(d) if x.endswith(".jsonl.gz") and not x.startswith("._")):
    with gzip.open(d / fn, "rt") as f:
        for line in f:
            tx = json.loads(line)
            t = tx["blockTime"]
            if t >= S:
                continue
            n += 1
            m = tx["meta"]
            if m.get("err") is not None:
                continue
            keys = tx["transaction"]["message"]["accountKeys"]
            signers = {k["pubkey"] for k in keys if k.get("signer")}
            delta = {}
            for lst, sg in ((m.get("preTokenBalances") or [], -1), (m.get("postTokenBalances") or [], 1)):
                for b in lst:
                    ow = b.get("owner")
                    if ow is None:
                        continue
                    delta[(ow, b["mint"])] = delta.get((ow, b["mint"]), 0) + sg * int(b["uiTokenAmount"]["amount"])
            for (ow, mt), v in delta.items():
                if mt != MINT or v >= 0 or ow in signers:
                    continue
                w = delta.get((ow, WSOL), 0)
                other = any(m2 != MINT and v2 > 0 for (o2, m2), v2 in delta.items() if o2 == ow)
                if not other:
                    continue
                for name, (a, b_) in WIN.items():
                    if a <= t < b_:
                        r = ag[name].setdefault(ow, [0, 0, 0])
                        r[0] += -v
                        r[1] += max(w, 0)
                        r[2] += 1
print("tx lues avant S", n)
with open(HERE / "b07_dmaga_venues.csv", "w", newline="") as fo:
    wr = csv.writer(fo)
    wr.writerow(["fenetre", "owner", "jetons_sortis", "wsol_entres_sol", "n_tx", "part_jetons_fenetre"])
    for name, a in ag.items():
        tot = sum(x[0] for x in a.values()) or 1
        for ow, x in sorted(a.items(), key=lambda kv: -kv[1][0]):
            wr.writerow([name, ow, x[0] / 1e6, x[1] / 1e9, x[2], x[0] / tot])
        ray = a.get(AUTH, [0, 0, 0])
        print(name, "réserves", len(a), "part Raydium authority (jetons sortis)", round(ray[0] / tot, 4), "SOL entrés Raydium", round(ray[1] / 1e9, 1), "SOL entrés autres", round(sum(x[1] for o, x in a.items() if o != AUTH) / 1e9, 1))
