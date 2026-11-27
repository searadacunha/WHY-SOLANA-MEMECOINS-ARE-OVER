"""Contrôle côté Solana des ordres b298 -> Solana : le receveur a-t-il reçu exactement take_amount, dans les 15 min, par le programme DLN destination ?
Ne relit que les tx du receveur proches de chaque ordre (économie de crédits). Sortie : ../evidence/s22_sol_fills_check.csv"""
import csv, sys, datetime as dt
sys.path.insert(0, ".")
import sol_lib as S
DST = "dst5MGcFPoBeREFAA5E3tU5ij8m5uVYwkzkSAbsLbNo"
O = [r for r in csv.DictReader(open("../evidence/dln_orders_evm.csv")) if r["direction"] == "OUT" and r["take_chain"] == "solana"]
ep = lambda u: int(dt.datetime.strptime(u, "%Y-%m-%d %H:%M:%S").replace(tzinfo=dt.timezone.utc).timestamp())
sigs = {}
for rcv in {r["receiver"] for r in O}:
    sigs[rcv] = S.signatures(rcv)
    # piège des comptes de jetons : une entrée sur un compte existant peut manquer aux signatures du propriétaire
    for mint in {r["take_token"] for r in O if r["receiver"] == rcv and not r["take_token"].startswith("1111")}:
        for v in S.call("getTokenAccountsByOwner", [rcv, {"mint": mint}, {"encoding": "jsonParsed"}])["value"]:
            have = {s["signature"] for s in sigs[rcv]}
            sigs[rcv] += [s for s in S.signatures(v["pubkey"]) if s["signature"] not in have]
out = []
for r in O:
    t0 = ep(r["utc"]); rcv = r["receiver"]; want = int(r["take_amount_raw"]); native = r["take_token"].startswith("1111")
    hit = None
    for s in sigs[rcv]:
        if s["blockTime"] and t0 - 60 <= s["blockTime"] <= t0 + 900 and not s.get("err"):
            t = S.tx(s["signature"]); sol, tok = S.deltas(t, rcv)
            got = sol if native else tok.get(r["take_token"], 0)
            # le receveur peut payer des frais de création de compte : tolérance de 0,01 SOL en natif, exacte en jeton
            if DST in S.programs(t) and (abs(got - want) <= 10_000_000 if native else got == want):
                hit = (s["signature"], s["blockTime"] - t0, got); break
    out.append(dict(utc=r["utc"], evm_tx=r["tx"], orderId=r["orderId"], receiver=rcv, take_token=r["take_token"], take_amount_raw=want,
                    solana_fill_sig=hit[0] if hit else "", delay_s=hit[1] if hit else "", received_raw=hit[2] if hit else "", status="VERIFIED" if hit else "NOT_FOUND"))
    print(r["utc"], rcv[:8], want, "->", out[-1]["status"], out[-1]["delay_s"], flush=True)
with open("../evidence/s22_sol_fills_check.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(out[0])); w.writeheader(); w.writerows(out)
