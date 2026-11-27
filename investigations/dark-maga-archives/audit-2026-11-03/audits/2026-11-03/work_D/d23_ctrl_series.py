#!/usr/bin/env python3
"""Auditeur D. Témoin direct du retour au même dépôt, absent de C : même matinée, 4 fenêtres de 507 s hors série, tirées à graine fixe AVANT tout appel, destinataires à montant rond (multiple de 0,05 SOL, définition de C).
Première page (100 tx, ordre croissant) de chaque destinataire, 10 crédits l'unité, plafond 600 crédits. Même troncature appliquée à la série depuis les bruts de C.
Sorties : d23_plan.csv (écrit avant le réseau), d23_ctrl_series.txt, audits_work/D/d23_net.jsonl.gz."""
import csv, gzip, json, os, random, sys, time, calendar, collections
from dmaga.helius import Helius
from dmaga.labels import label
OUT = "audits/2026-11-03/work_D/"; NET = "/Volumes/VERBATIM HD/Dark-MAGA-Investigation/audits_work/C/net/"; D = "/Volumes/VERBATIM HD/Dark-MAGA-Investigation/audits_work/D/"
BUDGET = 600
ts = lambda u: calendar.timegm(time.strptime(u, "%Y-%m-%dT%H:%M:%SZ"))
rows = list(csv.DictReader(open("audits/2026-11-03/work_C/cb_window.csv")))
T = [ts(r["utc"]) for r in rows]; A, Z = min(T), max(T)
SER0, SER1 = ts("2024-07-14T01:32:20Z"), ts("2024-07-14T01:40:51Z")
wins = [(a, a + 507) for a in range(A, Z - 507, 507) if a + 507 < SER0 or a > SER1]
rng = random.Random(20261103); pick = sorted(rng.sample(wins, 4))
plan = []
for w, (a, z) in enumerate(pick):
    seen = set()
    for r in rows:
        t = ts(r["utc"]); lam = round(float(r["sol"]) * 1e9)
        if a <= t < z and lam % 50_000_000 == 0 and lam >= 50_000_000 and r["dest"] not in seen:
            seen.add(r["dest"]); plan.append((w, r["utc"], r["hot"], r["dest"], lam))
plan2 = []
cnt = collections.Counter()
for p in plan:
    if cnt[p[0]] < 15: plan2.append(p); cnt[p[0]] += 1
plan = plan2[: BUDGET // 10]
wr = csv.writer(open(OUT + "d23_plan.csv", "w", newline="")); wr.writerow("fenetre utc hot dest lamports".split()); wr.writerows(plan)
print("fenêtres", [(time.strftime("%H:%M:%S", time.gmtime(a)), time.strftime("%H:%M:%S", time.gmtime(z))) for a, z in pick], "destinataires", dict(cnt), "appels prévus", len(plan), flush=True)
sys.stdout.flush()
out = open(OUT + "d23_ctrl_series.txt", "w")
def P(*a):
    print(*a, file=out, flush=True); print(*a, flush=True)
P("fenêtres", [(time.strftime("%H:%M:%S", time.gmtime(a)), time.strftime("%H:%M:%S", time.gmtime(z))) for a, z in pick], "destinataires", dict(cnt))
h = Helius(rps=3.0); credits = 0; errs = 0
gz = gzip.open(D + "d23_net.jsonl.gz", "wt", compresslevel=6)
hist = {}
for w, u, hot, dest, lam in plan:
    if credits + 10 > BUDGET: break
    try:
        r = h.txs_page(dest, details="full", limit=100, sort="asc", filters={"status": "succeeded"})
    except Exception as e:  # le message peut porter une URL : seul le type est gardé
        errs += 1; P("erreur", type(e).__name__, dest[:8]); credits += 10; continue
    credits += 10
    hist[dest] = r["data"]
    for t in r["data"]: gz.write(json.dumps({"x": dest, "tx": t}, separators=(",", ":")) + "\n")
gz.close()
P("crédits comptés à 10 par page", credits, "erreurs", errs, "stats", {k: v for k, v in h.stats.items()})
def outs(x, txs):
    d = collections.Counter(); first = None
    for t in txs:
        b = t.get("blockTime"); first = b if first is None or (b and b < first) else first
        seq = list(t["transaction"]["message"]["instructions"])
        for g in t["meta"].get("innerInstructions") or []: seq += g["instructions"]
        for i in seq:
            p = i.get("parsed")
            if i.get("program") == "system" and isinstance(p, dict) and p.get("type") == "transfer" and p["info"]["source"] == x and int(p["info"]["lamports"]) >= 1_000_000:
                d[p["info"]["destination"]] += int(p["info"]["lamports"])
    return d, first
def stat(name, members):
    c = collections.Counter(); fresh = 0; n = 0
    for m, u, txs in members:
        if txs is None: continue
        n += 1
        d, first = outs(m, txs)
        fresh += first == ts(u)
        for k in d: c[k] += 1
    top = [(k, v, label(k)) for k, v in c.most_common(6)]
    P(name, "wallets lus", n, "neufs", fresh, "max sur une même destination", top[0][1] if top else 0)
    P("   destinations communes", [(k[:10], v, l) for k, v, l in top])
    return top
for w in range(4):
    stat(f"fenêtre {w}", [(p[3], p[1], hist.get(p[3])) for p in plan if p[0] == w])
# série, même troncature : 100 premières tx, depuis les bruts de C
ser = [r for r in rows if SER0 <= ts(r["utc"]) <= SER1 and round(float(r["sol"]) * 1e9) in (500000000, 1000000000, 1050000000)]
mem = []
for r in ser:
    txs = []
    with gzip.open(NET + r["dest"] + ".jsonl.gz", "rt") as fh:
        for l in fh: txs.append(json.loads(l))
    txs.sort(key=lambda t: (t["slot"], t.get("transactionIndex") or 0))
    mem.append((r["dest"], r["utc"], txs[:100]))
stat("série, 100 premières tx", mem)
mem2 = [(a, u, None) for a, u, _ in mem]
del mem
