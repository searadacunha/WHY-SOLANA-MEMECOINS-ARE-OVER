#!/usr/bin/env python3
"""Auditeur D. Teste la série Coinbase et 9W9b depuis les réponses brutes gardées par C (audits_work/C/net) et cb_window.csv.
Aucun appel réseau. Sortie d20_series.txt, d20_senders.csv."""
import csv, gzip, json, os, random, statistics as st, sys, time, calendar, collections, glob
NET = "/Volumes/VERBATIM HD/Dark-MAGA-Investigation/audits_work/C/net/"
ROOT = "audits/2026-11-03/work_C/"; OUT = "audits/2026-11-03/work_D/"
W9 = "9W9b3zgHH9mCEHDhsdbnbEPHStm9vvXS4aia4DWHBxpL"
HOT = {"H8sMJSCQxfKiFTCfDR3DUMLPwcRbM61LGFJ8N4dK3WjS": "CB1", "2AQdpHJ2JpcEgPiATUXjQxA8QmafFegfQwSLWSprPicm": "CB2", "GJRs4FwHtemZ5ZE9x3FNvJ8TMwitKTh21yxdRPqn7npE": "CB3"}
sys.stdout = open(OUT + "d20_series.txt", "w")
ts = lambda u: calendar.timegm(time.strptime(u, "%Y-%m-%dT%H:%M:%SZ"))
iso = lambda t: time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(t))
def transfers(t):
    m = t["transaction"]["message"]; seq = list(m["instructions"])
    for g in t["meta"].get("innerInstructions") or []: seq += g["instructions"]
    for i in seq:
        p = i.get("parsed")
        if i.get("program") == "system" and isinstance(p, dict) and p.get("type") == "transfer":
            yield p["info"]["source"], p["info"]["destination"], int(p["info"]["lamports"])
# 1. historique complet de 9W9b, lu directement
ins, outs = [], []
sigs = set()
for l in gzip.open(NET + W9 + ".jsonl.gz", "rt"):
    t = json.loads(l); s = t["transaction"]["signatures"][0]
    if s in sigs: continue
    sigs.add(s)
    keys = t["transaction"]["message"]["accountKeys"]; signers = [k["pubkey"] for k in keys if k["signer"]]
    for a, b, v in transfers(t):
        if b == W9: ins.append((t["blockTime"], a, v, s, signers))
        if a == W9: outs.append((t["blockTime"], b, v, s, signers, t["meta"]["fee"]))
print("9W9b tx", len(sigs), "entrées", len(ins), "sorties", len(outs), "première", iso(min(x[0] for x in ins)), "dernière", iso(max(x[0] for x in ins + outs)))
real = [x for x in ins if x[2] >= 1_000_000]
send = collections.defaultdict(list)
for x in real: send[x[1]].append(x)
print("expéditeurs >= 0,001 SOL", len(send), "versements", len(real), "SOL", sum(x[2] for x in real) / 1e9)
tot = sum(o[2] for o in outs); cb = sum(o[2] for o in outs if o[1] in HOT)
print("sorties SOL", tot / 1e9, "part 3 hot wallets étiquetés", cb / tot, "destinations", collections.Counter(o[1] for o in outs).most_common(12))
print("frais des sorties", collections.Counter(o[5] for o in outs).most_common(5), "signataire = 9W9b seul", sum(1 for o in outs if o[4] == [W9]), "sur", len(outs))
print("mois des versements", sorted(collections.Counter(iso(x[0])[:7] for x in real).items()))
# solde final et conservation
print("SOL entré total", sum(x[2] for x in ins) / 1e9, "sorti total", tot / 1e9)
# 2. fenêtre de 2 h : qui parmi les destinataires verse ensuite à 9W9b ?
rows = list(csv.DictReader(open(ROOT + "cb_window.csv")))
print("retraits fenêtre", len(rows), "destinataires", len({r["dest"] for r in rows}), "de", rows[0]["utc"], "à", rows[-1]["utc"])
hit = [r for r in rows if r["dest"] in send]
print("retraits vers de futurs expéditeurs de 9W9b", len(hit), "destinataires", len({r["dest"] for r in hit}))
for r in hit: print("  ", r["utc"], r["hot"], r["dest"], r["sol"], "dmaga_tx", r["dmaga_tx"])
T = [ts(r["utc"]) for r in hit]
W = 507  # longueur de la série 01:32:23 -> 01:40:50
t0, t1 = ts(rows[0]["utc"]), ts(rows[-1]["utc"])
best = max(sum(1 for x in T if a <= x <= a + W) for a in T)
print("max de ces destinataires dans une fenêtre glissante de", W, "s :", best)
counts = [sum(1 for x in T if a <= x <= a + W) for a in range(t0, t1 - W, 30)]
print("fenêtres de", W, "s ne contenant aucun de ces destinataires : part", sum(1 for c in counts if c == 0) / len(counts), "max", max(counts))
print("hors [01:32:20,01:40:51] :", [(r["utc"], r["dest"]) for r in hit if not "2024-07-14T01:32:20Z" <= r["utc"] <= "2024-07-14T01:40:51Z"])
# 3. filtre de montant de C
S = [r for r in rows if "2024-07-14T01:32:20Z" <= r["utc"] <= "2024-07-14T01:40:51Z"]
AM = {500000000, 1000000000, 1050000000}
ser = [r for r in S if round(float(r["sol"]) * 1e9) in AM]
print("retraits dans la fenêtre", len(S), "dans le filtre {0,5;1;1,05}", len(ser), "dont futurs expéditeurs", sum(1 for r in ser if r["dest"] in send))
print("hors filtre mais futurs expéditeurs", [(r["utc"], r["sol"]) for r in S if r["dest"] in send and round(float(r["sol"]) * 1e9) not in AM])
print("mêmes montants sur 2 h", {a / 1e9: (sum(1 for r in rows if round(float(r["sol"]) * 1e9) == a), sum(1 for r in rows if round(float(r["sol"]) * 1e9) == a and r["dest"] in send)) for a in AM})
print("autres dates (hors fenêtre) pour 1,05 :", [(r["utc"], r["dest"][:8]) for r in rows if round(float(r["sol"]) * 1e9) == 1050000000 and r not in S])
print("autres 0,5 hors fenêtre", [(r["utc"][11:19], r["dmaga_tx"]) for r in rows if round(float(r["sol"]) * 1e9) == 500000000 and r not in S])
# 4. régularité : écarts sur les seuls futurs expéditeurs, et sur la série de 15
def cv(x): return st.pstdev(x) / st.mean(x)
gaps15 = [ts(b["utc"]) - ts(a["utc"]) for a, b in zip(ser, ser[1:])]
tt = sorted(T); inwin = [x for x in tt if ts("2024-07-14T01:32:20Z") <= x <= ts("2024-07-14T01:40:51Z")]
gaps13 = [b - a for a, b in zip(inwin, inwin[1:])]
print("écarts série 15", gaps15, "CV", round(cv(gaps15), 3), "; écarts 13", gaps13, "CV", round(cv(gaps13), 3))
rng = random.Random(20261103)
def simcv(n, span, N=20000):
    res = []
    for _ in range(N):
        u = sorted(rng.uniform(0, span) for _ in range(n))
        g = [b - a for a, b in zip(u, u[1:])]
        res.append(cv(g))
    return res
for n, g in ((15, gaps15), (len(inwin), gaps13)):
    sim = simcv(n, sum(g))
    print(f"P(CV <= observé) sous arrivées au hasard, n={n}, 20000 tirages : {sum(1 for x in sim if x <= cv(g)) / len(sim):.5f}, min simulé {min(sim):.3f}")
# 5. chronologie du premier retrait Coinbase des 48 expéditeurs, si historique présent
out = csv.writer(open(OUT + "d20_senders.csv", "w", newline=""))
out.writerow("sender n_versements sol_verses premier_versement dernier_versement historique_local premiere_tx premier_financeur premier_financeur_lamports premier_financeur_hot".split())
firstcb = []
for s, v in sorted(send.items(), key=lambda kv: -sum(x[2] for x in kv[1])):
    p = NET + s + ".jsonl.gz"
    ff = ("", "", "", ""); local = os.path.exists(p)
    if local:
        rows2 = []
        for l in gzip.open(p, "rt"):
            t = json.loads(l)
            for a, b, x in transfers(t):
                if b == s and x >= 1_000_000: rows2.append((t["blockTime"], t["slot"], a, x))
        rows2.sort()
        first = None
        if rows2:
            first = rows2[0]
            ff = (iso(first[0]), first[2], first[3], HOT.get(first[2], ""))
            if first[2] in HOT: firstcb.append((first[0], s, first[3], HOT[first[2]]))
    out.writerow([s, len(v), sum(x[2] for x in v) / 1e9, iso(min(x[0] for x in v)), iso(max(x[0] for x in v)), local, *ff])
print("expéditeurs avec historique local", sum(1 for s in send if os.path.exists(NET + s + ".jsonl.gz")))
firstcb.sort()
print("premier financeur = hot Coinbase étiqueté :", len(firstcb))
for x in firstcb: print("  ", iso(x[0]), x[1], x[2] / 1e9, x[3])
# 6. série de wallets : quand reviennent-ils à 9W9b ?
for r in ser:
    d = r["dest"]
    print("  série", r["utc"][11:19], d, r["sol"], "versements 9W9b", [(iso(x[0])[:16], x[2] / 1e9) for x in send.get(d, [])][:8])
# 7. salve du 26/01/2025
b = sorted(x for x in real if "2025-01-26T00" <= iso(x[0]) <= "2025-01-27T00")
print("versements 26/01/2025", len(b), "expéditeurs", len({x[1] for x in b}))
for x in b: print("  ", iso(x[0]), x[1], x[2] / 1e9, x[3])
# 8. rondeur -0,0001 SOL dans les retraits de 2 h : frais standard ?
am = [round(float(r["sol"]) * 1e9) for r in rows]
exact_round = sum(1 for a in am if a % 10_000_000 == 0)
minus = sum(1 for a in am if (a + 100000) % 10_000_000 == 0 and a % 10_000_000)
near = sum(1 for a in am if a % 10_000_000 and any((a + d) % 10_000_000 == 0 for d in range(90000, 110001, 1)))
print("retraits sur 2 h", len(am), "ronds à 0,01 SOL", exact_round, "rond moins exactement 100 000 lamports", minus, "rond moins 90 000 à 110 000 lamports", near)
print("exemples", [a / 1e9 for a in am if (a + 100000) % 10_000_000 == 0 and a % 10_000_000][:20])
