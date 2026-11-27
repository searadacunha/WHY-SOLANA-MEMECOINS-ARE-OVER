"""EXPLORATOIRE, DMAGA seul : remet dans les swaps du test les lignes des 2 owners écartés (5V97uEb4, AD65fgYt), calcule M1 à M7 avec le code gelé,
rang face aux pairs inchangés (asymétrique : les mêmes lignes ne sont pas remises chez les pairs). Sortie : b22_reinstate.txt."""
import sys, json
from pathlib import Path
import numpy as np, pandas as pd, pyarrow.parquet as pq
HERE = Path(__file__).parent; ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / "etude_final/code"))
from metrics import compute, METRICS
EXT = Path("/Volumes/VERBATIM HD/Dark-MAGA-Investigation")
DM = "CRSwXnfF21yHDXdYBVWwCwQ5Ni2A4QuK3qGYis5k7x7k"
S = 478219 * 3600; C = 1720923331
L = []
def P(*a):
    s = " ".join(str(x) for x in a); L.append(s); print(s)
sw = pq.read_table(EXT / "data/controls/swaps" / f"{DM}.parquet").to_pandas()
OW = ["5V97uEb4ZNuXFudphU5nwUapRmt7a2V51TbULQvPJwnx", "AD65fgYti96iSSzSPaNazV9Bs29m7JbNomGjG4Cp5WFS"]
tr = pq.read_table(ROOT / "data/trades.parquet", columns=["signature", "slot", "tx_index", "block_time", "source", "venue", "kind", "owner", "token_delta", "sol_lamports"], filters=[("owner", "in", OW), ("block_time", "<", S)]).to_pandas()
tr = tr[(tr.source == "pool") & (tr.venue == "raydium") & (tr.kind == "swap")]
P("lignes remises", len(tr), tr.groupby("owner").agg(n=("slot", "size"), buy=("sol_lamports", lambda x: -x[x < 0].sum() / 1e9), sell=("sol_lamports", lambda x: x[x > 0].sum() / 1e9), first=("block_time", "min"), last=("block_time", "max"), net=("token_delta", "sum")).to_dict("index"))
res = pq.read_table(EXT / "audits_work/B/tok" / f"{DM}.res.parquet").to_pandas()
tr = tr.merge(res[["slot", "idx", "pre_s"]], left_on=["slot", "tx_index"], right_on=["slot", "idx"], how="left")
assert tr.pre_s.notna().all()
add = pd.DataFrame(dict(t=tr.block_time, slot=tr.slot, tx_index=tr.tx_index, owner=tr.owner, qty=tr.token_delta, sol=tr.sol_lamports, vault_pre=tr.pre_s))
def run(df):
    df = df.sort_values(["slot", "tx_index"], kind="stable")
    uniq = {}; o = np.array([uniq.setdefault(x, len(uniq)) for x in df.owner], dtype=np.int64)
    return compute(df.t.to_numpy(np.int64), df.slot.to_numpy(np.int64), o, df.qty.to_numpy(np.int64), df.sol.to_numpy(np.int64), df.vault_pre.to_numpy(np.int64), S, C)
b = run(sw); a = run(pd.concat([sw[["t", "slot", "tx_index", "owner", "qty", "sol", "vault_pre"]], add]))
mt = pd.read_csv(ROOT / "etude_final/derived/metrics.csv"); mt = mt[(mt.variant == "primary") & (mt.pool != DM)]
for name, r in (("gelé", b), ("avec lignes remises", a)):
    P(name, {m: round(r[m], 4) for m in METRICS}, "p", {m: round((1 + (mt[m] >= r[m]).sum()) / 212, 4) for m in METRICS})
(HERE / "b22_reinstate.txt").write_text("\n".join(L) + "\n")
