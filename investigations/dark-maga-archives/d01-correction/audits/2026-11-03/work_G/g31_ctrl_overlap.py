#!/usr/bin/env python3
"""Témoin de recouvrement : dans les 120 dépôts témoins de C (ctrl_deposits), combien d'expéditeurs versent à au moins 2 dépôts, quel est le recouvrement maximal entre deux dépôts,
et quelles destinations reçoivent les balayages (pour tester 94xmX5J9, AafGzY9, 4NyK1A, etc.). Limite : 3 pages par dépôt témoin, SOL seulement. Sortie g31_ctrl_overlap.txt."""
import gzip, json, collections, itertools, sys
NET = "/Volumes/VERBATIM HD/Dark-MAGA-Investigation/audits_work/C/net/"
sys.stdout = open("audits/2026-11-03/work_G/g31_ctrl_overlap.txt", "w")
sen = collections.defaultdict(set); dst = collections.defaultdict(set); dstsol = collections.Counter(); fee = collections.defaultdict(collections.Counter)
for l in gzip.open(NET + "ctrl_deposits.jsonl.gz", "rt"):
    j = json.loads(l); x = j["x"]; t = j["tx"]
    seq = list(t["transaction"]["message"]["instructions"])
    for g in t["meta"].get("innerInstructions") or []: seq += g["instructions"]
    for i in seq:
        p = i.get("parsed")
        if i.get("program") == "system" and isinstance(p, dict) and p.get("type") == "transfer":
            a, b, v = p["info"]["source"], p["info"]["destination"], int(p["info"]["lamports"])
            if b == x and v >= 1_000_000: sen[x].add(a)
            if a == x: dst[b].add(x); dstsol[b] += v; fee[x][t["meta"]["fee"]] += 1
print("dépôts témoins", len(sen), "expéditeurs distincts", len(set().union(*sen.values())))
cnt = collections.Counter(s for v in sen.values() for s in v)
print("expéditeurs versant à au moins 2 dépôts", sum(1 for s, c in cnt.items() if c >= 2), "max", max(cnt.values()))
ov = sorted(((len(sen[a] & sen[b]), a, b, len(sen[a]), len(sen[b])) for a, b in itertools.combinations(sen, 2)), reverse=True)
print("recouvrement maximal entre deux dépôts", ov[:6])
print("paires de dépôts à recouvrement >= 2", sum(1 for o in ov if o[0] >= 2), ">= 5", sum(1 for o in ov if o[0] >= 5), "sur", len(ov))
print("destinations des balayages, dépôts témoins distincts, SOL", [(k, len(v), round(dstsol[k] / 1e9, 1)) for k, v in sorted(dst.items(), key=lambda kv: -len(kv[1]))[:16]])
for a in ("94xmX5J92nZLanLvRstmxhgiS8kN8SVfFQ2zPKYB3Ynb", "AafGzY9eiC5Ud3YFZQwkaKApp48cVBAT2kksGvEjhUvH", "4NyK1AdJBNbgaJ9EsKz3J4rfeHsuYdjkTPg3JaNdLeFw", "9obNtb5GyUegcs3a1CbBkLuc5hEWynWfJC6gjz5uWQkE", "8JUEoHNMbWM4eegcMvx6ZQJt3V3fbo8JNjpWiCtJgxfF", "6hXrioEsSShDPJ6fFzA9YUErimddZUVWYvwiwbffgZLW", "33RuC2ig9ZtdDUHj9YWs3Qbi2pSqQGd4dxs7NuNGemZw"):
    print("  ", a, "balayé par témoins :", len(dst.get(a, ())))
