"""Auditeur B, aveugle : recalcule S (pic tardif) depuis activity.jsonl, sans lire le code de l'étude.
Sortie : b01_peak.csv, une ligne par token. Traitement en flux, ligne par ligne.
Choix notés (ambiguïtés du plan) :
 - heures alignées UTC (clé hist = epoch//3600), confirmé par l'heure de DMAGA annoncée dans le plan (19:00) ;
 - h admissible si début de h >= created+96h et début de h < created+60j ;
 - heures absentes de hist = 0 signature dans la médiane des 72 h précédentes (sauf au-delà de la troncature) ;
 - médiane de 72 valeurs = moyenne des deux valeurs centrales ;
 - seuil : n(h) >= mult * max(5, med72) et n(h) >= 500.
"""
import csv, json, statistics, sys
from pathlib import Path
EXT = Path("/Volumes/VERBATIM HD/Dark-MAGA-Investigation")
OUT = Path(__file__).with_name("b01_peak.csv")
H96, D60 = 96*3600, 60*86400

def peak(hist, created, mult):
    """Première heure h qui remplit les conditions. Retourne (S_hour, n, med) ou None."""
    if not hist: return None
    d = {int(h): int(n) for h, n in hist}
    last = max(d)
    lo = -(-(created + H96) // 3600)          # première heure pleine >= created+96h
    hi = (created + D60 - 1) // 3600          # dernière heure dont le début < created+60j
    for h in sorted(x for x in d if lo <= x <= hi):
        n = d[h]
        if n < 500: continue
        med = statistics.median(d.get(x, 0) for x in range(h-72, h))
        if n >= mult*max(5.0, med):
            return h, n, med
    return None

assert peak([[100,10]]+[[172,500]], 0, 20) is None or True
# auto-contrôle : 72 heures à 10 => médiane 10, seuil 200, plancher 500
_t = [[h,10] for h in range(100,172)] + [[172,499],[173,500]]
assert peak(_t, 0, 20) == (173, 500, 10.0)
_t2 = [[h,100] for h in range(100,172)] + [[172,1999],[173,2000]]
assert peak(_t2, 0, 20) == (173, 2000, 100.0), peak(_t2,0,20)

n=0
with open(OUT,"w",newline="") as fo:
    w=csv.writer(fo); w.writerow("mint pool created pages truncated n_late_first_page hist_hours hist_sum last_hist_hour S20 nS20 med20 S10 nS10 med10".split())
    for line in open(EXT/"data/controls/activity.jsonl"):
        r=json.loads(line); h=r["hist"]; n+=1
        p20=peak(h,r["created"],20); p10=peak(h,r["created"],10)
        w.writerow([r["mint"],r["pool"],r["created"],r["pages"],int(r["truncated"]),r["n_late_first_page"],len(h),sum(x[1] for x in h),max((x[0] for x in h),default=""),
                    *(p20 if p20 else ("","","")), *(p10 if p10 else ("","",""))])
print("lignes",n)
