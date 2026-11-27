#!/usr/bin/env python3
"""Nature des adresses sondées, depuis leur historique lu (partiel si non complet). Règle écrite : relais si au moins 95 % du SOL sorti va à une seule adresse ; balayé si au moins 90 % va à un hot wallet étiqueté ou à la famille présumée ; sinon wallet actif. Sortie g55.csv, stdout."""
import csv, json, os, sys, time, gzip, collections
sys.path.insert(0, "audits/2026-11-03/work_G")
from g_lib import history, parse, NETG, NETC, CB
from dmaga.labels import label
iso = lambda t: time.strftime("%Y-%m-%d", time.gmtime(t))
FAM = {"FpwQQhQQoEaVu3WU2qZMfF1hx48YyfwsLoRgXG83E99Q", "D89hHJT5Aqyx1trP6EnGY9jJUB3whgnq3aUvvCqedvzf", "DPqsobysNf5iA9w7zrQM8HLzCKZEDMkZsWbiidsAt1xo", "5g7yNHyGLJ7fiQ9SN9mf47opDnMjc585kqXWt6d7aBWs", "9obNtb5GyUegcs3a1CbBkLuc5hEWynWfJC6gjz5uWQkE", "4NyK1AdJBNbgaJ9EsKz3J4rfeHsuYdjkTPg3JaNdLeFw", "8JUEoHNMbWM4eegcMvx6ZQJt3V3fbo8JNjpWiCtJgxfF", "AafGzY9eiC5Ud3YFZQwkaKApp48cVBAT2kksGvEjhUvH"}
A = [l.strip() for f in sys.argv[1:] for l in open(f) if l.strip() and not l.startswith("#")]
w = csv.writer(open("audits/2026-11-03/work_G/g55.csv", "w", newline="")); w.writerow("adresse tx complet debut fin signes sol_in sol_out usd_out top_out part_top label_top part_hot nature".split())
lab = lambda x: CB.get(x) or ("famille présumée" if x in FAM else label(x) or "")
for a in dict.fromkeys(A):
    o = collections.Counter(); u = collections.Counter(); si = 0; n = sg = 0; first = last = None
    for t in history(a):
        x = parse(t); n += 1; first = first or x["bt"]; last = x["bt"]; sg += a in x["signers"]
        for k, as_, m, s, d, r, dc in x["moves"]:
            if as_ == "SOL" and s == a and d != a: o[d] += r
            if as_ == "SOL" and d == a and s != a: si += r
            if as_ in ("USDC", "USDT") and s == a and d != a: u[d] += r
    c = None
    for dd in (NETG, NETC):
        p = dd + a + ".cursor.json"
        if os.path.exists(p): c = json.load(open(p)); break
    tot = sum(o.values()); top = o.most_common(1)[0] if o else ("", 0)
    hot = sum(v for k, v in o.items() if lab(k) and "Jupiter" not in lab(k) and "Raydium" not in lab(k))
    nature = "balayé vers hot wallet" if tot and hot / tot >= .9 else ("relais" if tot and top[1] / tot >= .95 and top[1] > 1e9 else "wallet actif")
    w.writerow([a, n, c.get("complete") if c else "", iso(first) if first else "", iso(last) if last else "", sg, round(si / 1e9, 3), round(tot / 1e9, 3), round(sum(u.values()) / 1e6, 2), top[0], round(top[1] / tot, 3) if tot else "", lab(top[0]), round(hot / tot, 3) if tot else "", nature])
    print(a[:10], "tx", n, "c" if c and c.get("complete") else "p", iso(first) if first else "", iso(last) if last else "", "signé", sg, "in", round(si / 1e9, 1), "out", round(tot / 1e9, 1), "usd", round(sum(u.values()) / 1e6), [(k[:8], lab(k)[:10], round(v / 1e9, 1)) for k, v in o.most_common(4)], nature)
