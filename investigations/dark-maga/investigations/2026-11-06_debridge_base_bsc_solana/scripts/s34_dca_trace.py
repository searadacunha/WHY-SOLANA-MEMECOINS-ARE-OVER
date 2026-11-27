"""Positions Jupiter DCA d'Ei5yGz8d et de 2aeEoq5n (jup_dca.py), puis le circuit du 17/11/2024 :
exécution deBridge de b298 -> Ei5yGz8d -> DCA SOL -> FvgqHM -> transfert de tout le FvgqHM au wallet neuf 2aeEoq5n -> vente.
Aucun appel réseau : historiques complets dans raw/sol_hist (local ou lecture seule). Sortie : evidence/s34_dca_positions.csv"""
import gzip, json, os, sys, datetime as dt
sys.path.insert(0, os.path.dirname(__file__))
import nt_lib as N
import jup_dca as J

def load(w):
    for d in [N.RAW] + N.RAW_RO:
        p = d / "sol_hist" / f"{w}.jsonl.gz"
        if p.exists(): return [json.loads(l) for l in gzip.open(p, "rt")]
    p = N.ROOT / "evidence" / "fixtures" / "sol" / f"{w}.jsonl"  # repli : fixtures publiées (sous-ensemble)
    return [json.loads(l) for l in open(p)]

def utc(t): return dt.datetime.fromtimestamp(t, dt.timezone.utc).strftime("%Y-%m-%d %H:%M:%S")

def keys_of(t):
    ks = [k["pubkey"] if isinstance(k, dict) else k for k in t["transaction"]["message"]["accountKeys"]]
    la = t["meta"].get("loadedAddresses") or {}
    return ks + la.get("writable", []) + la.get("readonly", [])

def sol_delta(t, w):
    ks = keys_of(t); return t["meta"]["postBalances"][ks.index(w)] - t["meta"]["preBalances"][ks.index(w)] if w in ks else 0

def tok_delta(t, w, mint):
    s = 0
    for side, sg in (("preTokenBalances", -1), ("postTokenBalances", 1)):
        for b in t["meta"].get(side) or []:
            if b.get("owner") == w and b["mint"] == mint: s += sg * int(b["uiTokenAmount"]["amount"])
    return s

W2 = "2aeEoq5n8Cip2raJsiWHBVKuoJL4rid7adepkVYnVzDm"
FVG = "FvgqHMfL9yn39V79huDPy3YUNDoYJpuLWng2JfmQpump"

if __name__ == "__main__":
    rows = []
    for w in (N.EI5, W2):
        for p in J.positions(load(w)).values():
            o, c = p["opened"], p["closed"]
            rows.append(dict(user=w, dca=p["dca"], opened_utc=utc(o["ts"]) if o else "", open_sig=o["sig"] if o else "",
                             input_mint=(o or c or {}).get("input_mint", ""), output_mint=(o or c or {}).get("output_mint", ""),
                             in_deposited=(o or c or {}).get("in_deposited", ""), n_fills=len(p["fills"]), in_filled=p["in_filled"],
                             out_filled=p["out_filled"], unfilled=c["unfilled_amount"] if c else "", closed_utc=utc(c["ts"]) if c else "",
                             close_sig=c["sig"] if c else "", user_closed=c["user_closed"] if c else "", consistent=p["consistent"]))
    N.write_csv(N.ROOT / "evidence/s34_dca_positions.csv", rows)
    bad = [r for r in rows if r["consistent"] is False]
    print(len(rows), "positions DCA ;", len(bad), "incohérentes")
    # le circuit du 17/11/2024
    E = load(N.EI5); A = load(W2)
    g = next(r for r in rows if r["dca"] == "G1fC4VgkodbFbsEwV8k8mzb2cMkngfqpiCNMGRZkCwvU")
    fill = next(t for t in E if t["transaction"]["signatures"][0].startswith("Z4XmFhZ8bUmq"))
    i0 = E.index(fill); opn = next(t for t in E if t["transaction"]["signatures"][0] == g["open_sig"])
    between = E[i0 + 1:E.index(opn)]
    ins = [(t["transaction"]["signatures"][0], sol_delta(t, N.EI5)) for t in between if sol_delta(t, N.EI5) > 0]
    pre = fill["meta"]["preBalances"][keys_of(fill).index(N.EI5)]
    held_before = sum(tok_delta(t, N.EI5, FVG) for t in E[:E.index(opn)])
    xfer = [t for t in E if tok_delta(t, N.EI5, FVG) < 0]
    sale = [t for t in A if tok_delta(t, W2, FVG) < 0]
    first_sol = A[0]
    print("exécution b298 :", fill["transaction"]["signatures"][0][:12], sol_delta(fill, N.EI5), "lamports ; solde avant", pre, "; entrées entre exécution et DCA :", ins)
    print("DCA", g["dca"][:8], "déposé", g["in_deposited"], "exécuté", g["in_filled"], "->", g["out_filled"], "FvgqHM ; FvgqHM détenu avant :", held_before)
    print("sorties de FvgqHM d'Ei5y :", [(t["transaction"]["signatures"][0][:10], utc(t["blockTime"]), tok_delta(t, N.EI5, FVG)) for t in xfer])
    print("2aeEoq5n : premier SOL", utc(first_sol["blockTime"]), sol_delta(first_sol, W2), "de", keys_of(first_sol)[0][:8],
          "; ventes de FvgqHM", [(t["transaction"]["signatures"][0][:10], utc(t["blockTime"]), tok_delta(t, W2, FVG), sol_delta(t, W2)) for t in sale])
