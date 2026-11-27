"""Tokens tronqués au plafond 150 000 signatures : couverture réelle de l'historique, depuis activity.jsonl seul.
Sortie : b08_trunc.csv (un token tronqué par ligne) et b08_trunc.txt (résumé)."""
import csv, json, statistics
from pathlib import Path
EXT = Path("/Volumes/VERBATIM HD/Dark-MAGA-Investigation")
HERE = Path(__file__).parent
pk = {r["pool"]: r for r in csv.DictReader(open(HERE / "b01_peak.csv"))}
rows = []
for line in open(EXT / "data/controls/activity.jsonl"):
    r = json.loads(line)
    if not r["truncated"]:
        continue
    h = r["hist"]
    c = r["created"]
    last_h = max(x[0] for x in h)
    first_h = min(x[0] for x in h)
    cov_days = (last_h * 3600 - c) / 86400
    late = [x for x in h if x[0] * 3600 >= c + 96 * 3600]
    p = pk[r["pool"]]
    status = "S20" if p["S20"] else ("S10_seul" if p["S10"] else "sans_pic")
    rows.append(dict(pool=r["pool"], mint=r["mint"], status=status, created=c, couverture_jours=round(cov_days, 2), total=sum(x[1] for x in h), max_h=max(x[1] for x in h),
                     heures_tardives=len(late), sig_tardives=sum(x[1] for x in late), med_h_tardive=statistics.median([x[1] for x in late]) if late else "", 
                     atteint_96h=int(cov_days >= 4)))
with open(HERE / "b08_trunc.csv", "w", newline="") as fo:
    w = csv.DictWriter(fo, fieldnames=rows[0].keys()); w.writeheader(); w.writerows(rows)
L = [f"tronqués {len(rows)}"]
for st in ["S20", "S10_seul", "sans_pic"]:
    x = [r for r in rows if r["status"] == st]
    cov = sorted(r["couverture_jours"] for r in x)
    L.append(f"{st}: n={len(x)} couverture médiane {statistics.median(cov):.2f} j, min {cov[0]:.2f}, max {cov[-1]:.2f}, n'atteignent pas 96 h : {sum(1 for r in x if not r['atteint_96h'])}, couverture < 7 j : {sum(1 for r in x if r['couverture_jours']<7)}, < 30 j : {sum(1 for r in x if r['couverture_jours']<30)}, max_h médian {statistics.median(r['max_h'] for r in x)}")
(HERE / "b08_trunc.txt").write_text("\n".join(L) + "\n")
print("\n".join(L))
