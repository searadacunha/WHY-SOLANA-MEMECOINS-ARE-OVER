#!/usr/bin/env python3
"""Prix SOL/USDT journalier (dernière clôture du jour, en UTC) depuis raw/solusd (fichiers Binance 1 min, déjà sur disque). Sortie work_G/sol_daily.csv."""
import csv, io, os, time, zipfile
D = "/Volumes/VERBATIM HD/Dark-MAGA-Investigation/raw/solusd/"
out = {}
for f in sorted(os.listdir(D)):
    if f.startswith("._") or not f.endswith(".zip"): continue
    z = zipfile.ZipFile(D + f)
    for n in z.namelist():
        for row in csv.reader(io.TextIOWrapper(z.open(n))):
            if not row[0].isdigit(): continue
            t = int(row[0]); t = t // 1000 if t > 1e11 else t
            t = t // 1000 if t > 1e11 else t
            out[time.strftime("%Y-%m-%d", time.gmtime(t))] = row[4]
w = csv.writer(open("audits/2026-11-03/work_G/sol_daily.csv", "w", newline="")); w.writerow(["date", "close"])
for k in sorted(out): w.writerow([k, out[k]])
print(len(out), min(out), max(out))
