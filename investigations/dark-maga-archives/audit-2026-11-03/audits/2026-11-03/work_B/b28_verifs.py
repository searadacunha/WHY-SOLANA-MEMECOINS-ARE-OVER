"""Derniers chiffres cités : rapports de vraisemblance d'un résultat non significatif, fenêtre passée la plus haute de S1 avatar. Sortie : b28_verifs.txt."""
from pathlib import Path
import numpy as np, pandas as pd, pyarrow.parquet as pq
H = Path(__file__).parent; L = []
EXT = Path("/Volumes/VERBATIM HD/Dark-MAGA-Investigation"); DM = "CRSwXnfF21yHDXdYBVWwCwQ5Ni2A4QuK3qGYis5k7x7k"
d = pd.read_csv(H / "b13_scenarios.csv").set_index("scenario"); nul = 5 / 212
for s in ["1R_1w_3h", "2R_1w_3h", "2R_25w_3h_sync", "controle_fort_18w_740SOL_3h_sync"]:
    L.append(f"{s}: détection {d.loc[s, 'taux_verdict_inhabituel']:.4f}, rapport de vraisemblance du non significatif {(1 - d.loc[s, 'taux_verdict_inhabituel']) / (1 - nul):.3f}")
s = pq.read_table(EXT / "data/controls/swaps" / f"{DM}.parquet", columns=["t", "qty", "sol"]).to_pandas()
b = s[(s.qty > 0) & (s.sol < 0)]; E = 1721589800
for i in range(0, 4):
    a = E - 3 * 3600 * (i + 1); v = -b[(b.t >= a) & (b.t < a + 3 * 3600)].sol.sum() / 1e9
    L.append(f"fenêtre avatar {i} : début {pd.to_datetime(a, unit='s')}, SOL {v:.2f}")
(H / "b28_verifs.txt").write_text("\n".join(L) + "\n"); print("\n".join(L))
