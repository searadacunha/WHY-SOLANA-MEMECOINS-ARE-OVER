"""K12 : adresses complètes de la famille Coinbase non étiquetée, relues dans des sorties complètes, jamais complétées. Écrit evidence/labels/hot_presume.tsv."""
import csv, gzip, json, re, sys
from pathlib import Path
PREF = ["FpwQQhQQ", "D89hHJT5", "DPqsobys", "9obNtb5G", "4NyK1AdJ", "8JUEoHNM", "5g7yNHyG"]
B58 = re.compile(r"[1-9A-HJ-NP-Za-km-z]{32,44}")
found = {p: {} for p in PREF}
srcs = [Path("data/collector.json")] + sorted(Path("audits/2026-11-03/work_D").glob("d[24]*.txt")) + sorted(Path("audits/2026-11-03/work_C").glob("*.csv")) + sorted(Path("audits/2026-11-03/work_C").glob("*.out"))
for f in srcs:
    for a in B58.findall(f.read_text(errors="replace")):
        for p in PREF:
            if a.startswith(p): found[p].setdefault(a, str(f))
net = Path("/Volumes/VERBATIM HD/Dark-MAGA-Investigation/audits_work/C/net/ctrl_deposits.jsonl.gz")
if any(not v for v in found.values()) and net.exists():
    with gzip.open(net, "rt") as fh:
        for l in fh:
            for a in B58.findall(l):
                for p in PREF:
                    if a.startswith(p) and not found[p]: found[p].setdefault(a, str(net))
out = Path("evidence/labels/hot_presume.tsv")
rows = []
for p in PREF:
    ks = [k for k in found[p] if 32 <= len(k) <= 44]
    print(p, found[p])
    assert len(ks) == 1, p
    rows.append((ks[0], found[p][ks[0]]))
with out.open("w", newline="") as f:
    w = csv.writer(f, delimiter="\t")
    w.writerow(["adresse", "lue_dans"])
    w.writerows(rows)
print("écrit", out, len(rows))
