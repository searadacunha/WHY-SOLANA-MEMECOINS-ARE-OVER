"""Relit sur Solana tout l'historique de GZXKYzwZ (signatures du wallet et de ses comptes de jetons) et les variations par tx.
Sortie : ../evidence/s20_gzx_ledger.csv"""
import csv, sys, datetime as dt
sys.path.insert(0, ".")
import sol_lib as S
W = sys.argv[1] if len(sys.argv) > 1 else "GZXKYzwZPgWH8TwyY9f8dkCQ9EKK6nrPZADGcEwfAg7Y"
OUT = sys.argv[2] if len(sys.argv) > 2 else "../evidence/s20_gzx_ledger.csv"
sigs = {s["signature"]: s for s in S.signatures(W)}
txs = {s: S.tx(s) for s in sigs}
# comptes de jetons du wallet vus dans ses tx : leurs signatures peuvent contenir des entrées où le wallet n'apparaît pas
tas = set()
for t in txs.values():
    if not t: continue
    for side in ("preTokenBalances", "postTokenBalances"):
        for b in t["meta"].get(side) or []:
            if b.get("owner") == W:
                tas.add(S.keys_of(t)[b["accountIndex"]])
extra = 0
for ta in sorted(tas):
    for s in S.signatures(ta):
        if s["signature"] not in txs:
            txs[s["signature"]] = S.tx(s["signature"]); sigs[s["signature"]] = s; extra += 1
rows = []
for s, t in txs.items():
    if not t: continue
    sol, tok = S.deltas(t, W)
    ks = S.keys_of(t)
    signers = [k["pubkey"] for k in t["transaction"]["message"]["accountKeys"] if isinstance(k, dict) and k.get("signer")]
    # contreparties : propriétaires dont le solde du même mint bouge en sens inverse
    cps = set()
    for side in ("preTokenBalances", "postTokenBalances"):
        for b in t["meta"].get(side) or []:
            if b.get("owner") and b["owner"] != W and b["mint"] in tok: cps.add(b["owner"][:44])
    for i, k in enumerate(ks[:len(t["meta"]["preBalances"])]):
        d = t["meta"]["postBalances"][i] - t["meta"]["preBalances"][i]
        if k != W and sol and d and (d > 0) != (sol > 0) and abs(d) > 5000: cps.add(k)
    rows.append(dict(utc=dt.datetime.fromtimestamp(t["blockTime"], dt.timezone.utc).strftime("%Y-%m-%d %H:%M:%S"), slot=t["slot"], signature=s,
                     err=bool(t["meta"]["err"]), fee_payer=signers[0] if signers else "", signers="|".join(signers), sol_delta_lamports=sol,
                     dmaga_delta_raw=tok.get(S.DMAGA, 0), usdc_delta_raw=tok.get(S.USDC, 0), wsol_delta_raw=tok.get(S.WSOL, 0),
                     other_tokens="|".join(f"{k}:{v}" for k, v in tok.items() if k not in (S.DMAGA, S.USDC, S.WSOL)),
                     dln_src=S.DLN_SRC in S.programs(t), counterparties="|".join(sorted(cps))[:900]))
rows.sort(key=lambda r: (r["slot"], r["signature"]))
with open(OUT, "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
print(W, "signatures", len(sigs), "dont via comptes de jetons", extra, "comptes de jetons", len(tas), "lignes", len(rows))
