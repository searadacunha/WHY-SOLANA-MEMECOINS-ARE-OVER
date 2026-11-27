#!/usr/bin/env python3
"""Auditeur A. Relit migrations, activity, selection, swaps_stats, metrics.csv : recalcul propre du pic, comptes, doublons. Sans réseau."""
import csv, json, statistics, collections, os
from pathlib import Path
C = Path("/Volumes/VERBATIM HD/Dark-MAGA-Investigation/data/controls")
ROOT = Path("REDACTED_HOME/Projects/Dark-MAGA-Investigation")
DP = "CRSwXnfF21yHDXdYBVWwCwQ5Ni2A4QuK3qGYis5k7x7k"
H = 3600
mig = [json.loads(x) for x in (C / "migrations.jsonl").read_text().splitlines()]
print("migrations lignes", len(mig), "pools distincts", len({m["pool"] for m in mig}), "mints distincts", len({m["mint"] for m in mig}))
print("créations min/max", min(m["created"] for m in mig), max(m["created"] for m in mig))
pump = sum(m["mint"].endswith("pump") for m in mig)
print("mints finissant par pump", pump)
dm = [m for m in mig if m["pool"] == DP][0]
print("DMAGA migration", dm)
act, bad = [], 0
for x in (C / "activity.jsonl").read_text().splitlines():
    try:
        act.append(json.loads(x))
    except json.JSONDecodeError:
        bad += 1
print("activity lignes", len(act), "pools distincts", len({a["pool"] for a in act}), "invalides", bad)
print("tronqués", sum(a["truncated"] for a in act), "avec n_late>=500", sum(a["n_late_first_page"] >= 500 for a in act),
      "n_late==1000", sum(a["n_late_first_page"] == 1000 for a in act), "pages max", max(a["pages"] for a in act))
print("écart de création migrations/activity", sum(1 for a in act if a["created"] != {m["pool"]: m["created"] for m in mig}.get(a["pool"])) if len(act) < 0 else "voir plus bas")
mc = {m["pool"]: m["created"] for m in mig}
print("écart de création", sum(1 for a in act if a["created"] != mc.get(a["pool"])))


def pic(hist, created, mult=20.0, mn=500):  # écrit depuis le plan, sans metrics.py
    if not hist:
        return None
    lo = (created + 96 * H + H - 1) // H
    hi = (created + 60 * 86400) // H  # h doit commencer avant création + 60 j, et la dernière heure partielle compte selon le plan
    for h in sorted(hist):
        if h < lo or h >= hi + 1:
            continue
        n = hist[h]
        if n < mn:
            continue
        med = statistics.median([hist.get(x, 0) for x in range(h - 72, h)])
        if n >= mult * max(med, 5):
            return h * H
    return None


sel = [json.loads(x) for x in (C / "selection.jsonl").read_text().splitlines()]
print("selection lignes", len(sel), "pools distincts", len({r["pool"] for r in sel}))
print("statuts", collections.Counter(r["status"] for r in sel))
by = {r["pool"]: r for r in sel}
diff20 = diff10 = 0
ex = []
hists = {}
for a in act:
    hist = {int(k): int(v) for k, v in a["hist"]}
    s20, s10 = pic(hist, a["created"], 20.0), pic(hist, a["created"], 10.0)
    r = by.get(a["pool"])
    if r is None:
        ex.append(("absent", a["pool"]))
        continue
    if (r["S20"] or None) != s20:
        diff20 += 1
        ex.append(("S20", a["pool"], r["S20"], s20))
    if (r["S10"] or None) != s10:
        diff10 += 1
        ex.append(("S10", a["pool"], r["S10"], s10))
    if a["pool"] == DP:
        hists[DP] = hist
        print("DMAGA S20", s20, "S10", s10, "sel", r["S20"], r["S10"], "fdv", r.get("fdv_s20"), r.get("fdv_s10"), "tronqué", a["truncated"], "pages", a["pages"], "statut", r["status"])
        for h in range(s20 // H - 6, s20 // H + 2):
            med = statistics.median([hist.get(x, 0) for x in range(h - 72, h)])
            print("  heure", h * H, "n", hist.get(h, 0), "med72", med, "ratio", round(hist.get(h, 0) / max(med, 5), 1))
print("écarts S20", diff20, "S10", diff10, ex[:6])
BAND, WIDE = (1e5, 1e7), (1e4, 5e7)
prim = [r for r in sel if r.get("S20") and r.get("fdv_s20") is not None and BAND[0] <= r["fdv_s20"] <= BAND[1]]
print("S20 dans la bande principale, tous statuts", collections.Counter(r["status"] for r in prim), "total", len(prim))
print("fdv_s20_absent", sum(1 for r in sel if r.get("fdv_s20_absent")), "fdv_s10_absent", sum(1 for r in sel if r.get("fdv_s10_absent")))
st = [json.loads(x) for x in (C / "swaps_stats.jsonl").read_text().splitlines()]
print("swaps_stats lignes", len(st), "pools distincts", len({v["pool"] for v in st}))
sw = [p for p in os.listdir(C / "swaps") if p.endswith(".parquet") and not p.startswith("._")]
print("fichiers swaps", len(sw))
print("retenus sans parquet", sum(1 for r in sel if r["status"] == "retenu_superset" and r["pool"] + ".parquet" not in sw))
print("parquets hors retenus", [p for p in sw if by.get(p[:-8], {}).get("status") != "retenu_superset"][:5])
print("ruptures>0", [(v["pool"], v["ruptures"]) for v in st if v.get("ruptures")])
rows = list(csv.DictReader(open(ROOT / "etude_final/derived/metrics.csv")))
print("metrics lignes", len(rows), collections.Counter(r["variant"] for r in rows))
pr = [r for r in rows if r["variant"] == "primary"]
known = {m["pool"] for m in mig}
print("metrics pools hors migrations", sum(1 for r in rows if r["pool"] not in known), "mints incohérents", sum(1 for r in rows if {m["pool"]: m["mint"] for m in mig}[r["pool"]] != r["mint"]) if False else "")
mm = {m["pool"]: m["mint"] for m in mig}
print("mints incohérents", sum(1 for r in rows if mm[r["pool"]] != r["mint"]), "S incohérents primary", sum(1 for r in pr if int(r["S"]) != by[r["pool"]]["S20"]))
print("primary dans la bande mais absent de metrics", [r["pool"] for r in prim if r["pool"] not in {x["pool"] for x in pr}][:5])
print("primary sans vs avec n_swaps", min(int(r["n_swaps_96h"]) for r in pr), max(int(r["n_swaps_96h"]) for r in pr))
print("DMAGA ligne", [r for r in pr if r["pool"] == DP])
days = {int(r["S"]) // 86400 for r in pr if r["pool"] != DP}
print("jours distincts de pic", len(days), "S min/max", min(int(r["S"]) for r in pr), max(int(r["S"]) for r in pr))
print("tronqués retenus primary", sum(1 for r in pr if by[r["pool"]]["truncated"]))
stp = {v["pool"]: v for v in st}
tot = collections.Counter()
for r in pr:
    v = stp[r["pool"]]
    for k, x in v.items():
        if k != "pool":
            tot[k] += x
print("stats sur primary", dict(tot))
print("DMAGA stats", stp[DP])
for k in ("sans_vault", "non_signataire_deux_cotes", "sans_beneficiaire", "qty_differente_du_vault", "parts_de_frais"):
    v = sorted(stp[r["pool"]].get(k, 0) / max(stp[r["pool"]].get("tx", 1), 1) for r in pr)
    print(k, "part par pool : médiane", round(v[len(v) // 2], 4), "p90", round(v[int(len(v) * .9)], 4), "DMAGA", round(stp[DP].get(k, 0) / stp[DP]["tx"], 4), "rang DMAGA", sum(1 for x in v if x >= stp[DP].get(k, 0) / stp[DP]["tx"]))
