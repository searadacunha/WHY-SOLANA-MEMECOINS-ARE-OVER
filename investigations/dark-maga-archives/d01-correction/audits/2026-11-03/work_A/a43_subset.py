#!/usr/bin/env python3
"""Auditeur A. Effet des pics faits d'échecs : rangs de DMAGA parmi les comparateurs dont le pic reste le même sur les seules réussies, et parmi ceux qui ont au moins 500 réussies à S. Mesure d'effet, hors protocole. Plus un coup d'oeil aux transactions à un seul vault."""
import csv, gzip, json
from pathlib import Path
ROOT = "REDACTED_HOME/Projects/Dark-MAGA-Investigation"
OUT = ROOT + "/audits/2026-11-03/work_A/out"
RAW = Path("/Volumes/VERBATIM HD/Dark-MAGA-Investigation/raw/ctrl_tx")
C = Path("/Volumes/VERBATIM HD/Dark-MAGA-Investigation/data/controls")
DP = "CRSwXnfF21yHDXdYBVWwCwQ5Ni2A4QuK3qGYis5k7x7k"
sp = {r["pool"]: r for r in csv.DictReader(open(OUT + "/a04_spike_success.csv"))}
rows = [r for r in csv.DictReader(open(ROOT + "/etude_final/derived/metrics.csv")) if r["variant"] == "primary"]
tg = [r for r in rows if r["pool"] == DP][0]
for name, keep in (("pic identique sur réussies", lambda r: sp[r["pool"]]["S_sur_reussies_dans_partie_collectee"] == r["S"]), ("au moins 500 réussies à S", lambda r: int(sp[r["pool"]]["reussies_S"]) >= 500)):
    ct = [r for r in rows if r["pool"] != DP and keep(r)]
    out = {}
    for m in ("M1", "M2", "M3", "M4", "M5", "M6", "M7"):
        v = [float(r[m]) for r in ct if float(r[m]) == float(r[m])]
        out[m] = round((1 + sum(1 for x in v if x >= float(tg[m]))) / (len(v) + 1), 4)
    print(name, "k", len(ct), out)
sel = {}
for x in open(C / "selection.jsonl"):
    r = json.loads(x)
    if r["pool"] == "4GKStivbdSb4ihTiZE2t38cZqQQs8WC8bqd2LQG6hGFD":
        sel = r
vt, vs = sel["vault_token"], sel["vault_sol"]
n = 0
done = False
for p in sorted((RAW / sel["pool"]).glob("p*.jsonl.gz")):
    with gzip.open(p, "rt") as f:
        for line in f:
            t = json.loads(line)
            keys = [k["pubkey"] for k in t["transaction"]["message"]["accountKeys"]]
            bal = {}
            for b in t["meta"].get("preTokenBalances") or []:
                bal[(keys[b["accountIndex"]], b["mint"], b.get("owner"))] = -int(b["uiTokenAmount"]["amount"])
            for b in t["meta"].get("postTokenBalances") or []:
                k = (keys[b["accountIndex"]], b["mint"], b.get("owner"))
                bal[k] = bal.get(k, 0) + int(b["uiTokenAmount"]["amount"])
            dt = sum(v for k, v in bal.items() if k[0] == vt)
            ds = sum(v for k, v in bal.items() if k[0] == vs)
            if (dt != 0) != (ds != 0):
                n += 1
                if n in (1, 500):
                    print("exemple", t["transaction"]["signatures"][0], "dt", dt, "ds", ds, "programmes", sorted({(i.get("programId") or "")[:8] for i in t["transaction"]["message"]["instructions"]}), "deltas", [(k[1][:5], (k[2] or "")[:6], v) for k, v in bal.items() if v][:8])
                if n >= 500:
                    done = True
                    break
    if done:
        break
