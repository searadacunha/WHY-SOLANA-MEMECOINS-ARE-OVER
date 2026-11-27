"""Phase 2 : R1, R2, R3 recalculés avec les mesures de B, sur les populations de l'étude. Sortie : b26_variants.csv et b26_variants.txt."""
from pathlib import Path
import numpy as np, pandas as pd
H = Path(__file__).parent; ROOT = H.parents[2]
DM = "CRSwXnfF21yHDXdYBVWwCwQ5Ni2A4QuK3qGYis5k7x7k"; MS = ["M1", "M2", "M3", "M4", "M5", "M6", "M7"]
mt = pd.read_csv(ROOT / "etude_final/derived/metrics.csv")
files = {"primary": "b03_main.csv", "R1_10x": "b03_r1.csv", "R2_bande_large": "b03_main.csv", "R3_S_moins_1h": "b03_r3.csv"}
rows = []
for var, fn in files.items():
    a = mt[mt.variant == var].set_index("pool"); b = pd.read_csv(H / fn).set_index("pool").loc[a.index]
    assert (a.S == b.S).all()
    for m in MS:
        ca = a.drop(index=DM)[m].dropna(); cb = b.drop(index=DM)[m].dropna()
        pa_ = (1 + (ca >= a.loc[DM, m]).sum()) / (len(ca) + 1); pb = (1 + (cb >= b.loc[DM, m] - 1e-9).sum()) / (len(cb) + 1)
        rows.append(dict(variante=var, mesure=m, k=len(ca), D_etude=a.loc[DM, m], D_B=b.loc[DM, m], c_etude=int((ca >= a.loc[DM, m]).sum()), c_B=int((cb >= b.loc[DM, m] - 1e-9).sum()), p_etude=pa_, p_B=pb, percentile=float((ca < a.loc[DM, m]).mean())))
d = pd.DataFrame(rows); d.to_csv(H / "b26_variants.csv", index=False)
t = d.pivot(index="mesure", columns="variante", values=["p_etude", "p_B"]).round(4).to_string()
(H / "b26_variants.txt").write_text(t + "\n"); print(t)
print("écarts de c entre étude et B :", int((d.c_etude != d.c_B).sum()), "lignes sur", len(d), d[d.c_etude != d.c_B][["variante", "mesure", "c_etude", "c_B"]].to_dict("records"))
