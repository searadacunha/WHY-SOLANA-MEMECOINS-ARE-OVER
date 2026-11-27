"""100 premiers acheteurs Solana (KM, KEKIUS-XC78) : courbe Pump.fun complète, puis premières transactions Raydium.

Les transactions Raydium viennent du RPC public (cache) d'après la liste des 1 000 premières signatures du pool (Helius,
tri croissant, sauvegardée dans KEKIUS_EXT/pool_first1000_sigs.json). Acheteur = propriétaire dont le solde du jeton monte
dans une tx réussie, hors lieux d'échange. Les co-signataires d'une même tx sont listés : signer ensemble suppose que les
clés étaient réunies au moment de la construction de la tx."""
import csv, json
from k_lib import DATA, EXT, KM, KM_CURVE, XC, XC_CURVE, utc
from k11_parse import token_deltas, sol_deltas, signers
from k15_trades import rows, VENUE_OWNERS
import k16_pubrpc as pub

POOL_AUTH = "5Q544fKrFoe6tsEbD7S8EmxGTJYAKtTVhAW5Q5pge4j1"
heads = json.load(open(EXT / "pool_first1000_sigs.json"))


def pool_rows(key, mint, need):
    n = 0
    for sig, bt, slot, err in heads[key]:
        if err:
            continue
        t = pub.tx(sig)
        if t["meta"]["err"]:
            continue
        sg, sd = signers(t), sol_deltas(t)
        for owner, d in token_deltas(t, mint).items():
            if owner in VENUE_OWNERS or owner == POOL_AUTH:
                continue
            yield {"sig": sig, "slot": t["slot"], "time": t["blockTime"], "owner": owner, "token_raw": d,
                   "owner_sol_lamports": sd.get(owner, 0) if owner in sg else "", "fee_payer": sg[0], "signers": ";".join(sg)}
        n += 1
        if n >= need:
            return


for tk, mint, curve, pool in [("KM", KM, KM_CURVE, "km_pool"), ("XC", XC, XC_CURVE, "xc_pool")]:
    seen, out = set(), []
    allrows = list(rows(f"{tk.lower()}_curve", mint, curve))
    if len({r["owner"] for r in allrows if r["token_raw"] > 0}) < 100:
        allrows += list(pool_rows(pool, mint, 400))
    for r in allrows:
        if r["token_raw"] <= 0 or r["owner"] in seen:
            continue
        seen.add(r["owner"])
        co = [s for s in r["signers"].split(";") if s != r["owner"]]
        out.append([len(out) + 1, r["owner"], utc(r["time"]), r["slot"], r["sig"], round(r["token_raw"] / 1e12, 6),
                    round(-(r["owner_sol_lamports"] or 0) / 1e9, 9) if r["owner_sol_lamports"] != "" else "",
                    r["fee_payer"], ";".join(co), "curve" if r["slot"] <= max(x["slot"] for x in rows(f"{tk.lower()}_curve", mint, curve)) else "raydium"])
        if len(out) == 100:
            break
    with open(DATA / f"sol_first100_buyers_{tk}.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["rank", "owner", "first_buy_utc", "slot", "signature", "tokens_M", "sol_spent_if_signer", "fee_payer", "co_signers", "venue"])
        w.writerows(out)
    print(tk, len(out), "dernier", out[-1][2])
