"""Phase 2 : S1 recalculé depuis le parseur de B et depuis les swaps de l'étude ; détail horaire DMAGA autour de Winig ;
M1 ancré sur Winig (EXPLORATOIRE). Sortie : b16_s1.txt."""
import json, sys
from pathlib import Path
import numpy as np, pandas as pd, pyarrow.parquet as pq
sys.path.insert(0, str(Path(__file__).parent))
from b03_metrics import metrics, TOK, HERE, H, LAM
ROOT = HERE.parents[2]
EXT = Path("/Volumes/VERBATIM HD/Dark-MAGA-Investigation")
DM = "CRSwXnfF21yHDXdYBVWwCwQ5Ni2A4QuK3qGYis5k7x7k"
WINIG, AVATAR, CREATED = 1721577749, 1721589800, 1720923331
L = []
def P(*a):
    s = " ".join(str(x) for x in a); L.append(s); print(s)
r = pq.read_table(TOK / f"{DM}.parquet").to_pandas().sort_values(["slot", "idx"])
r["sol"] /= LAM
s = pq.read_table(EXT / "data/controls/swaps" / f"{DM}.parquet").to_pandas().sort_values(["slot", "tx_index"])
P("lignes B", len(r), "lignes étude", len(s), "t max B", r.time.max(), "t max étude", s.t.max())
def s1(t, owner, is_buy, sol, name):
    first = pd.Series(t).groupby(np.asarray(owner)).min()
    fo = pd.Series(np.asarray(owner)).map(first).to_numpy()
    for lab, E in (("winig", WINIG), ("avatar", AVATAR)):
        edges = np.arange(E - 3 * H, CREATED + 96 * H - 1, -3 * H)
        vs = np.array([sol[is_buy & (t >= e) & (t < e + 3 * H)].sum() for e in edges])
        vn = []
        for e in edges:
            m = is_buy & (t >= e) & (t < e + 3 * H) & (fo >= e) & (fo < e + 3 * H)
            vn.append(len(set(np.asarray(owner)[m].tolist())))
        vn = np.array(vn)
        P(f"{name} {lab}: fenêtres passées {len(edges) - 1}, début de la plus ancienne {pd.to_datetime(edges[-1], unit='s')}, SOL {vs[0]:.3f}, médiane passé {np.median(vs[1:]):.3f}, p {(1 + (vs[1:] >= vs[0]).sum()) / len(vs):.4f}, nouveaux {vn[0]}, médiane {np.median(vn[1:])}, p {(1 + (vn[1:] >= vn[0]).sum()) / len(vn):.4f}, 5 plus grandes fenêtres SOL {np.round(np.sort(vs)[::-1][:5], 1)}, p minimal possible {1 / len(vs):.4f}")
s1(r.time.to_numpy(), r.w.to_numpy(), (r.side == 1).to_numpy(), r.sol.to_numpy(), "B")
s1(s.t.to_numpy(), s.owner.to_numpy(), ((s.qty > 0) & (s.sol < 0)).to_numpy(), (-s.sol / 1e9).to_numpy(), "étude")
P("Holm séparé à 4 tests : premier seuil 0,0125, p minimal possible 1/28 = 0,0357 : ne peut pas passer")
P("Chevauchement des fenêtres winig et avatar : fenêtres de avatar qui recoupent [E_winig−3 h, E_winig) : [13:23,16:23) et [10:23,13:23)")
# heure par heure le 21/07
b = r[r.side == 1]
hh = b.groupby(b.time // 3600).agg(sol=("sol", "sum"), n=("sol", "size"), wallets=("w", "nunique"))
hh = hh[hh.index >= 478190]
hh.index = [pd.to_datetime(x * 3600, unit="s").strftime("%d %H:%M") for x in hh.index]
P(hh.round(1).to_string())
w = b[(b.time >= WINIG - 3 * H) & (b.time < WINIG)]
top = w.groupby("w").sol.sum().sort_values(ascending=False)
wallets = (TOK / f"{DM}.wallets.txt").read_text().split("\n")
P("[Winig−3 h, Winig) : SOL", round(w.sol.sum(), 2), "acheteurs", w.w.nunique(), "part du premier", round(top.iloc[0] / top.sum(), 3), "des 5 premiers", round(top.iloc[:5].sum() / top.sum(), 3))
P("Répartition de ces achats dans la fenêtre par tranche de 30 min :", w.groupby((w.time - (WINIG - 3 * H)) // 1800).sol.sum().round(1).to_dict())
P("5 premiers acheteurs :", [(wallets[i], round(v, 2)) for i, v in top.iloc[:5].items()])
# M1 avec S=E_winig (EXPLORATOIRE) : même définition, ancre sur l'événement public
res = pq.read_table(TOK / f"{DM}.res.parquet")
rk = res["slot"].to_numpy() * 100000 + res["idx"].to_numpy(); rpre = res["pre_s"].to_numpy()
rows = r
st = None
for line in open(HERE / "b02_stats.jsonl"):
    x = json.loads(line)
    if x["pool"] == DM: st = x
tok = rows.tok.to_numpy() / 1e6
mm = {}
mt = pd.read_csv(ROOT / "etude_final/derived/metrics.csv"); mt = mt[(mt.variant == "primary") & (mt.pool != DM)]
for name, E in (("S=16:00 UTC", 478216 * 3600), ("E=Winig 16:02:29", WINIG), ("S=19:00 (plan)", 478219 * 3600)):
    m = metrics(E, CREATED, rows.slot.to_numpy(), rows.idx.to_numpy(), rows.time.to_numpy(), rows.side.to_numpy(), rows.w.to_numpy(), rows.sol.to_numpy(), tok, rk, rpre)
    v = {k: round(m[k], 4) for k in ("M1", "M2", "M3", "M4", "M5", "M6", "M7")}
    pv = {k: round((1 + (mt[k] >= m[k]).sum()) / 212, 4) for k in v}
    P(f"EXPLORATOIRE {name}: {v} ; p face aux pairs à leur S : {pv}")
(HERE / "b16_s1.txt").write_text("\n".join(L) + "\n")
