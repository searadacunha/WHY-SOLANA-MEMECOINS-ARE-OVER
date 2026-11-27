"""Entrées et sorties brutes des dépôts cités, sans filtre, sans étiquette. Une ligne par entrée ou sortie (actif, contrepartie). Sorties : i01_moves.csv, i01_summary.txt.
Contrepartie : les propriétaires qui perdent l'actif dans la même tx. Une tx avec programme hors BASIC est marquée routed=1."""
import csv, sys, datetime as dt
sys.path.insert(0, "audits/2026-11-03/work_I")
from i_lib import *
OUT = "audits/2026-11-03/work_I/"
DEP = {"9W9b": "9W9b3zgHH9mCEHDhsdbnbEPHStm9vvXS4aia4DWHBxpL", "Caw4": "Caw4RrwkmxqtbLSFzgSs6id3XiFxWQxs2t1mrn5a3mME"}
extra = sys.argv[1:]
for a in extra: DEP[a[:4]] = a
w = csv.writer(open(OUT + "i01_moves.csv", "a" if extra else "w"))
if not extra:
    w.writerow("depot utc sig side asset amount cp signer routed nprog err".split())
log = open(OUT + "i01_summary.txt", "a" if extra else "w")
def P(*a):
    print(*a, file=log); print(*a)
for tag, d in DEP.items():
    n = err = 0; first = last = None
    insum = {}; outsum = {}; insend = {}; outdest = {}; sign_by_d = 0; nsig = 0; prog_when_signed = {}
    for t in iter_tx(d):
        n += 1
        ts = t["blockTime"]; first = min(first or ts, ts); last = max(last or ts, ts)
        if not ok(t): err += 1; continue
        sg = t["transaction"]["signatures"][0]; S = signers(t); routed = int(bool(programs(t) - BASIC))
        sd = sol_delta(t); td, dec = tok_delta(t)
        if d in S:
            nsig += 1; sign_by_d += 1
            for p in programs(t): prog_when_signed[p] = prog_when_signed.get(p, 0) + 1
        u = dt.datetime.fromtimestamp(ts, dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        # SOL
        v = sd.get(d, 0)
        if v:
            cps = [k for k, x in sd.items() if (x < 0) == (v > 0) and k != d]
            side = "in" if v > 0 else "out"
            for c in cps or ["?"]:
                w.writerow([tag, u, sg, side, "SOL", abs(v) / 1e9, c, S[0] if S else "", routed, len(programs(t)), ""])
            (insum if v > 0 else outsum).setdefault("SOL", [0])[0] += abs(v)
            for c in cps or ["?"]:
                (insend if v > 0 else outdest).setdefault(("SOL", c), [0, 0])
                (insend if v > 0 else outdest)[("SOL", c)][0] += abs(v) / 1e9
                (insend if v > 0 else outdest)[("SOL", c)][1] += 1
        for (o, m), x in td.items():
            if o != d: continue
            cps = [k[0] for k, y in td.items() if k[1] == m and k[0] != d and (y < 0) == (x > 0)]
            side = "in" if x > 0 else "out"
            a = {USDC: "USDC", USDT: "USDT", WSOL: "WSOL"}.get(m, m)
            amt = abs(x) / 10 ** dec[m]
            for c in cps or ["?"]:
                w.writerow([tag, u, sg, side, a, amt, c, S[0] if S else "", routed, len(programs(t)), ""])
                (insend if x > 0 else outdest).setdefault((a, c), [0, 0])
                (insend if x > 0 else outdest)[(a, c)][0] += amt
                (insend if x > 0 else outdest)[(a, c)][1] += 1
            (insum if x > 0 else outsum).setdefault(a, [0])[0] += amt
    P("==", tag, d, "tx", n, "err", err, dt.datetime.fromtimestamp(first, dt.timezone.utc), dt.datetime.fromtimestamp(last, dt.timezone.utc))
    P(" in", {k: round(v[0] / (1e9 if k == "SOL" else 1), 6) for k, v in insum.items()})
    P(" out", {k: round(v[0] / (1e9 if k == "SOL" else 1), 6) for k, v in outsum.items()})
    P(" signé par le dépôt", nsig, "programmes", prog_when_signed)
    for a in sorted({k[0] for k in insend}):
        snd = {k[1]: v for k, v in insend.items() if k[0] == a}
        P(" expéditeurs", a, len(snd), "dont >=0.01/1:", sum(1 for v in snd.values() if v[0] >= (0.01 if a in ("SOL", "WSOL") else 1)))
    for k, v in sorted(outdest.items(), key=lambda kv: -kv[1][0])[:10]:
        P(" sortie", k, round(v[0], 6), v[1])
