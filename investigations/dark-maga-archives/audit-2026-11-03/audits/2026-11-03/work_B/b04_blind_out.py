"""Auditeur B, aveugle : assemble blind_selection.csv et blind_metrics.csv, calcule les rangs et Holm sur la population de B.
Écrit b04_ranks_blind.csv. N'écrit pas le sceau (fait par b05_seal.py)."""
import csv, os
from pathlib import Path
import numpy as np, pandas as pd
HERE = Path(__file__).parent
EXT = Path("/Volumes/VERBATIM HD/Dark-MAGA-Investigation")
DMAGA = "7D7BRcBYepfi77vxySapmeqRNN1wsBBxnFPJGbH5pump"
pk = pd.read_csv(HERE / "b01_peak.csv")
m = pd.read_csv(HERE / "b03_main.csv")
has_raw = set(x for x in os.listdir(EXT / "raw/ctrl_tx") if not x.startswith("._"))
d = pk.merge(m[["pool", "S", "cap_S1h", "swap_rank_in_last_res", "swap_before_S1_age_s", "rows_96h", "chain_breaks", "chain_breaks_tok", "cursor_complete", "last_res_time", "n_before_S"]], on="pool", how="left")
def status(r):
    if r.hist_hours == 0: return "sans_activite_tardive"
    if pd.isna(r.S20):
        if r.truncated == 1:
            return "tronque_sans_S20" if not pd.isna(r.S10) else "tronque_sans_pic"
        return "sans_pic"
    if r.pool not in has_raw: return "pic_sans_brut"
    if pd.isna(r.cap_S1h): return "sans_swap_avant_S"
    if r.swap_rank_in_last_res > 200: return "sans_swap_avant_S"
    if not (100000 <= r.cap_S1h <= 10000000): return "cap_hors_bande"
    if r.rows_96h < 20: return "moins_20_swaps"
    if r.chain_breaks > 0: return "chaine_rompue"
    if r.cursor_complete is False or str(r.cursor_complete) == "False":
        return "curseur_incomplet"
    return "retenu"
d["status"] = d.apply(status, axis=1)
d.to_csv(HERE / "blind_selection.csv", index=False)
print(d.status.value_counts().to_string())
ret = set(d[d.status == "retenu"].pool)
m["retenu"] = m.pool.isin(ret).astype(int)
m.to_csv(HERE / "blind_metrics.csv", index=False)
D = m[m.mint == DMAGA].iloc[0]
C = m[(m.retenu == 1) & (m.mint != DMAGA)]
print("k population", len(C), "DMAGA retenu", D.retenu)
rows = []
for k in ["M1", "M2", "M3", "M4", "M5", "M6", "M7", "M7b", "M3b", "M6b"]:
    v = C[k].dropna().to_numpy()
    p = (1 + (v >= D[k]).sum()) / (len(v) + 1)
    rows.append(dict(mesure=k, D=D[k], k=len(v), nan=int(C[k].isna().sum()), ge=int((v >= D[k]).sum()), p=p, percentile=float((v < D[k]).mean()), comp_median=float(np.median(v)), comp_max=float(v.max())))
r = pd.DataFrame(rows)
pr = r[r.mesure.isin(["M1", "M2", "M3", "M4", "M5", "M6", "M7"])].sort_values("p")
alpha = 0.05; ok = True; res = {}
for i, (_, x) in enumerate(pr.iterrows()):
    t = alpha / (7 - i)
    ok = ok and x.p <= t
    res[x.mesure] = (t, ok)
r["holm_seuil"] = r.mesure.map(lambda k: res.get(k, (np.nan, False))[0])
r["holm_passe"] = r.mesure.map(lambda k: res.get(k, (np.nan, False))[1])
r.to_csv(HERE / "b04_ranks_blind.csv", index=False)
print(r.to_string())
