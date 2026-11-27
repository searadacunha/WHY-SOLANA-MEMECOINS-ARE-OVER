#!/usr/bin/env python3
"""Auditeur D. Amendement 001 : population réelle et maximale de R1 et R2, bornes de p, ordre de collecte. Lecture seule. Sortie d30_amend.txt."""
import csv, json, statistics as st, sys, os, time, math
ROOT = "audits/2026-11-03/work_D/"; C = "/Volumes/VERBATIM HD/Dark-MAGA-Investigation/data/controls/"
sys.stdout = open(ROOT + "d30_amend.txt", "w")
S = [json.loads(l) for l in open(C + "selection.jsonl")]
print("lignes", len(S), {k: sum(1 for x in S if x["status"] == k) for k in {x["status"] for x in S}})
M = ["M1", "M2", "M3", "M4", "M5", "M6", "M7"]
rows = list(csv.DictReader(open("etude_final/derived/metrics.csv")))
var = {}
for r in rows: var.setdefault(r["variant"], []).append(r)
print({k: len(v) for k, v in var.items()})
d = {m: float(next(r for r in var["primary"] if r["is_dmaga"] == "True")[m]) for m in M}
def band(x, lo, hi): return x is not None and lo <= x <= hi
prim = {x["pool"] for x in S if x.get("S20") and band(x.get("fdv_s20"), 1e5, 1e7) and x["status"] in ("retenu_superset", "reporte_budget")}
r1all = {x["pool"] for x in S if x.get("S10") and band(x.get("fdv_s10"), 1e5, 1e7) and x["status"] in ("retenu_superset", "reporte_budget")}
r2all = {x["pool"] for x in S if x.get("S20") and band(x.get("fdv_s20"), 1e4, 5e7) and x["status"] in ("retenu_superset", "reporte_budget")}
coll = {x["pool"] for x in S if x["status"] == "retenu_superset"}
print("principal bande", len(prim), "dont reporté", len(prim - coll))
print("R1 max avec DMAGA", len(r1all), "collectés", len(r1all & coll), "reportés", len(r1all - coll))
print("R2 max avec DMAGA", len(r2all), "collectés", len(r2all & coll), "reportés", len(r2all - coll))
# tronqué sans S20
print("reporté par raison : sans S20", sum(1 for x in S if x["status"] == "reporte_budget" and not x.get("S20")), "tronque_sans_S20 vrai", sum(1 for x in S if x.get("tronque_sans_S20")), "dont statut", {s: sum(1 for x in S if x.get("tronque_sans_S20") and x["status"] == s) for s in {x["status"] for x in S}})
def rank(v, m):
    vals = [float(r[m]) for r in v if r["is_dmaga"] != "True" and r[m] not in ("", "nan")]
    t = float(next(r for r in v if r["is_dmaga"] == "True")[m])
    c = sum(1 for x in vals if x >= t)
    return len(vals), c, (1 + c) / (len(vals) + 1)
kmax = {"R1_10x": len(r1all) - 1, "R2_bande_large": len(r2all) - 1}
for name, v in var.items():
    if name == "R3_S_moins_1h" or name == "primary":
        print(name, "k", len(v) - 1, {m: round(rank(v, m)[2], 4) for m in M}, "meilleur", min((rank(v, m)[2], m) for m in M))
        continue
    res = {}
    for m in M:
        k, c, p = rank(v, m)
        K = kmax[name]
        res[m] = dict(k=k, c=c, p=round(p, 4), p_si_tous_reportes_sous=round((1 + c) / (K + 1), 4), p_si_tous_reportes_au_dessus=round((1 + c + K - k) / (K + 1), 4))
    print(name, "k", len(v) - 1, "kmax", kmax[name]); [print("   ", m, res[m]) for m in M]
    best = min(x["p_si_tous_reportes_sous"] for x in res.values())
    print("   meilleur p possible", best, "seuil Holm 0,00714", "passe" if best <= 0.05 / 7 else "ne passe pas", "; c=32..33 sur M6 exige k >=", math.ceil((1 + res['M6']['c']) / (0.05 / 7) - 1))
primk = {r["pool"] for r in var["primary"]}
for name in ("R1_10x", "R2_bande_large"):
    p = {r["pool"] for r in var[name]}
    print(name, "déjà dans le principal", len(p & primk), "sur", len(p), "ajouts", len(p - primk))
adds = [r for r in var["R2_bande_large"] if r["pool"] not in primk]
sel = {x["pool"]: x for x in S}
print("ajouts R2 : création de", time.strftime("%d/%m", time.gmtime(min(int(r["created"]) for r in adds))), "à", time.strftime("%d/%m", time.gmtime(max(int(r["created"]) for r in adds))), "cap de", min(float(r["fdv_usd"]) for r in adds), "à", max(float(r["fdv_usd"]) for r in adds))
for m in M:
    print("   ", m, "ajouts médiane", round(st.median(float(r[m]) for r in adds), 3), "principal", round(st.median(float(r[m]) for r in var["primary"] if r["is_dmaga"] != "True"), 3))
# ordre de collecte
pos = {x["pool"]: i for i, x in enumerate(S)}
oth = [x for x in S if x["status"] in ("retenu_superset", "reporte_budget") and x["pool"] not in prim]
oth.sort(key=lambda x: pos[x["pool"]])
def spearman(a, b):
    ra = {v: i for i, v in enumerate(sorted(set(a)))}; rb = {v: i for i, v in enumerate(sorted(set(b)))}
    x = [ra[v] for v in a]; y = [rb[v] for v in b]
    mx, my = st.mean(x), st.mean(y)
    return sum((p - mx) * (q - my) for p, q in zip(x, y)) / math.sqrt(sum((p - mx) ** 2 for p in x) * sum((q - my) ** 2 for q in y))
print("hors principal, retenus + reportés", len(oth), "Spearman position/création", round(spearman([pos[x["pool"]] for x in oth], [x["created"] for x in oth]), 4))
act = {}
for l in open(C + "activity.jsonl"):
    j = json.loads(l); act[j.get("pool")] = j
print("clés activité", list(next(iter(act.values())).keys())[:12])
def tot(p):
    j = act.get(p) or {}
    return j.get("n_total") or j.get("total") or j.get("n_sigs") or j.get("listed") or 0
a = [tot(x["pool"]) for x in oth]
print("Spearman position/activité", round(spearman([pos[x["pool"]] for x in oth], a), 4) if any(a) else "activité non lue")
cc = [x for x in oth if x["status"] == "retenu_superset"]; rr = [x for x in oth if x["status"] == "reporte_budget"]
print("hors principal collectés", len(cc), "reportés", len(rr))
fmt = lambda t: time.strftime("%d/%m", time.gmtime(t))
for nm, g in (("collectés", cc), ("reportés", rr)):
    print(nm, "création médiane", fmt(st.median(x["created"] for x in g)), "S20 médian", fmt(st.median(x["S20"] for x in g if x.get("S20"))), "cap médiane", round(st.median(x["fdv_s20"] for x in g if x.get("fdv_s20"))), "activité médiane", st.median(tot(x["pool"]) for x in g))
print("cap > 10 M$ reportés", sum(1 for x in rr if (x.get("fdv_s20") or 0) > 1e7), "collectés", sum(1 for x in cc if (x.get("fdv_s20") or 0) > 1e7))
print("part des hors-principal R2 couverte", round(100 * len(r2all & coll - prim) / max(1, len(r2all - prim)), 1), "%")
# coût d'une collecte complète, ordre de grandeur (signatures listées, 100 tx par page, 10 crédits par page)
print("signatures des reportés", sum(a for a in (tot(x["pool"]) for x in rr)))
