#!/usr/bin/env python3
"""Profil d'une adresse depuis son historique téléchargé : expéditeurs, destinations, part vers hot wallets, signataire, frais, délai, programmes, solde.
usage : g21_profile.py addr... ; écrit sur stdout, une fiche par adresse."""
import sys, collections, statistics as st, time, os
sys.path.insert(0, "audits/2026-11-03/work_G")
from g_lib import history, parse, CB, FAM
from dmaga.labels import label
iso = lambda t: time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(t))
TOPN = int(os.environ.get("TOPN", "8"))
def lab(x):
    if x in CB: return CB[x]
    if x in FAM: return "famille CB présumée"
    return (label(x) or "")[:20]
for A in sys.argv[1:]:
    ins = collections.defaultdict(lambda: [0, 0]); outs = collections.defaultdict(lambda: [0, 0]); n = 0; signed = 0; fees = collections.Counter(); progs = collections.Counter()
    first = last = None; dep = []; sw = []; bal_after = []; tok_i = collections.defaultdict(float); tok_o = collections.defaultdict(float); tok_ip = collections.defaultdict(lambda: collections.Counter()); tok_op = collections.defaultdict(lambda: collections.Counter())
    for t in history(A):
        x = parse(t); n += 1; first = first or x["bt"]; last = x["bt"]
        if A in x["signers"]: signed += 1; fees[x["fee"]] += 1
        for p in x["progs"]: progs[p] += 1
        for k, asset, mint, s, d, raw, dec in x["moves"]:
            if asset == "SOL":
                if d == A and s != A: ins[s][0] += 1; ins[s][1] += raw; dep.append((x["bt"], raw))
                if s == A and d != A: outs[d][0] += 1; outs[d][1] += raw; sw.append((x["bt"], raw, d)); bal_after.append(x["post"].get(A, 0))
            elif asset != "other" or True:
                a = asset if asset != "other" else mint[:8]
                f = 10 ** (dec or 0)
                if d == A and s != A: tok_i[a] += raw / f; tok_ip[a][s] += raw / f
                if s == A and d != A: tok_o[a] += raw / f; tok_op[a][d] += raw / f
    print(f"== {A} lab={lab(A)} tx={n} {iso(first) if first else ''} -> {iso(last) if last else ''} signés={signed} frais={fees.most_common(3)} programmes={[(p[:8], c) for p, c in progs.most_common(5)]}")
    ti, to = sum(v[1] for v in ins.values()), sum(v[1] for v in outs.values())
    print(f"  SOL entré {ti/1e9:.3f} de {len(ins)} ; sorti {to/1e9:.3f} vers {len(outs)} ; part vers CB étiqueté {sum(v[1] for k, v in outs.items() if k in CB)/max(to,1):.3f} ; famille présumée {sum(v[1] for k, v in outs.items() if k in FAM)/max(to,1):.3f}")
    for k, v in sorted(ins.items(), key=lambda kv: -kv[1][1])[:TOPN]: print("   IN ", k, lab(k), v[0], round(v[1]/1e9, 4))
    for k, v in sorted(outs.items(), key=lambda kv: -kv[1][1])[:TOPN]: print("   OUT", k, lab(k), v[0], round(v[1]/1e9, 4))
    for a in sorted(set(tok_i) | set(tok_o)):
        if tok_i[a] + tok_o[a] < 1: continue
        print(f"  jeton {a} entré {tok_i[a]:.2f} de {len(tok_ip[a])} sorti {tok_o[a]:.2f} vers {len(tok_op[a])}")
        for k, v in tok_ip[a].most_common(TOPN if a in ("USDC", "USDT", "DMAGA", "WSOL") else 2): print("     in ", k, lab(k), round(v, 2))
        for k, v in tok_op[a].most_common(TOPN if a in ("USDC", "USDT", "DMAGA", "WSOL") else 2): print("     out", k, lab(k), round(v, 2))
    if bal_after: print("  solde après sortie, lamports : médiane", int(st.median(bal_after)), "min", min(bal_after), "max", max(bal_after))
