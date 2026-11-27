"""Phase 2 : cause des écarts B / étude. Compare ligne à ligne les swaps (parquet étude) et les lignes de B sur les tokens les plus éloignés.
Sortie : b17_diff_cause.txt."""
import sys
from pathlib import Path
import numpy as np, pandas as pd, pyarrow.parquet as pq
HERE = Path(__file__).parent
EXT = Path("/Volumes/VERBATIM HD/Dark-MAGA-Investigation")
TOK = EXT / "audits_work/B/tok"
L = []
def P(*a):
    s = " ".join(str(x) for x in a); L.append(s); print(s)
d = pd.read_csv(HERE / "b10_diff_tokens.csv")
pools = []
for m, g in d.groupby("mesure"):
    for p in g.head(1).pool: 
        if p not in pools: pools.append(p)
pools = pools[:7]
for pool in pools:
    s = pq.read_table(EXT / "data/controls/swaps" / f"{pool}.parquet", columns=["t", "slot", "tx_index", "owner", "qty", "sol", "vault_pre"]).to_pandas()
    r = pq.read_table(TOK / f"{pool}.parquet").to_pandas()
    w = (TOK / f"{pool}.wallets.txt").read_text().split("\n")
    r["owner"] = [w[i] for i in r.w]
    r = r.rename(columns={"idx": "tx_index"})
    x = s.merge(r, on=["slot", "tx_index", "owner"], how="outer", indicator=True)
    both = x[x._merge == "both"]
    n_e, n_b = (x._merge == "left_only").sum(), (x._merge == "right_only").sum()
    ds = (both.sol_x.abs() - both.sol_y).abs() / both.sol_y.clip(lower=1)
    dq = (both.qty.abs() - both.tok).abs() / both.tok.clip(lower=1)
    P(f"\n{pool}: lignes étude {len(s)}, B {len(r)}, communes {len(both)}, étude seule {n_e}, B seule {n_b}")
    P(f"  SOL : part des lignes communes qui diffèrent de >0,1 % : {(ds>1e-3).mean():.3f} ; somme étude {both.sol_x.abs().sum()/1e9:.2f}, B {both.sol_y.sum()/1e9:.2f}")
    P(f"  jetons : part qui diffèrent de >0,1 % : {(dq>1e-3).mean():.3f}, parts où |qty étude| > jetons B de plus de 1 % : {(both.qty.abs() > both.tok*1.01).mean():.3f}")
    print_cols = ["slot", "tx_index", "owner", "qty", "sol_x", "tok", "sol_y"]
    if n_e: P("  exemple étude seule :", x[x._merge == "left_only"].head(2)[["slot", "tx_index", "owner", "qty", "sol_x"]].to_dict("records"))
    if n_b: P("  exemple B seule :", x[x._merge == "right_only"].head(2)[["slot", "tx_index", "owner", "tok", "sol_y"]].to_dict("records"))
    big = both.assign(dq=dq).sort_values("dq", ascending=False).head(2)
    P("  plus grand écart jetons :", big[print_cols].to_dict("records"))
    del s, r, x, both
(HERE / "b17_diff_cause.txt").write_text("\n".join(L) + "\n")
