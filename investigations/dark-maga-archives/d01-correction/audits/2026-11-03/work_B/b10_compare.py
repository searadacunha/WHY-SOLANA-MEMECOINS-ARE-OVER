"""Phase 2 : compare la chaîne aveugle de B à derived/metrics.csv et selection.jsonl, token par token.
Sorties : b10_compare.txt, b10_diff_tokens.csv."""
import json
from pathlib import Path
import numpy as np, pandas as pd
HERE = Path(__file__).parent
ROOT = HERE.parents[2]
EXT = Path("/Volumes/VERBATIM HD/Dark-MAGA-Investigation")
OUT = []
def P(*a):
    s = " ".join(str(x) for x in a); OUT.append(s); print(s)
sel = pd.read_json(EXT / "data/controls/selection.jsonl", lines=True)
pk = pd.read_csv(HERE / "b01_peak.csv")
bs = pd.read_csv(HERE / "blind_selection.csv")
P("selection.jsonl lignes", len(sel), "statuts", sel.status.value_counts().to_dict())
d = sel.merge(pk, on="pool", suffixes=("", "_b"))
P("S20 identiques (aux heures) :", int(((d.S20.fillna(0) / 3600) == d.S20_b.fillna(0)).sum()), "sur", len(d))
P("S10 identiques (aux heures) :", int(((d.S10.fillna(0) / 3600) == d.S10_b.fillna(0)).sum()), "sur", len(d))
dd = d[((d.S20.fillna(0) / 3600) != d.S20_b.fillna(0)) | ((d.S10.fillna(0) / 3600) != d.S10_b.fillna(0))]
P("différences S :", dd[["pool", "S20", "S20_b", "S10", "S10_b", "created"]].to_string() if len(dd) else "aucune")
# population principale : S20 et fdv_s20 dans la bande, sur tout le superset (collecté ou non)
B = (100000, 10000000); W = (10000, 50000000)
main_all = sel[sel.S20.notna() & sel.fdv_s20.between(*B)]
P("S20 et fdv_s20 dans la bande, tous statuts :", len(main_all), main_all.status.value_counts().to_dict())
P("S20 total", int(sel.S20.notna().sum()), "S10 total", int(sel.S10.notna().sum()), "fdv_s20 renseigné", int(sel.fdv_s20.notna().sum()), "fdv_s10 renseigné", int(sel.fdv_s10.notna().sum()))
for c in ["fdv_s20_absent", "fdv_s10_absent"]:
    if c in sel: P(c, sel[c].value_counts(dropna=True).to_dict())
P("tronque_sans_S20 :", int(sel.tronque_sans_S20.sum()), "dont statut", sel[sel.tronque_sans_S20].status.value_counts().to_dict())
# R1 et R2 théoriques sur tout le superset
r1_all = sel[sel.S10.notna() & sel.fdv_s10.between(*B)]
r2_all = sel[sel.S20.notna() & sel.fdv_s20.between(*W)]
P("R1 théorique (S10 et fdv_s10 dans la bande) :", len(r1_all), r1_all.status.value_counts().to_dict())
P("R2 théorique (S20 et fdv_s20 dans la bande large) :", len(r2_all), r2_all.status.value_counts().to_dict())
# métriques
mt = pd.read_csv(ROOT / "etude_final/derived/metrics.csv")
P("metrics.csv", mt.variant.value_counts().to_dict())
for var, f in [("primary", "blind_metrics.csv"), ("R1_10x", "b03_r1.csv"), ("R3_S_moins_1h", "b03_r3.csv")]:
    b = pd.read_csv(HERE / f)
    a = mt[mt.variant == var]
    if var == "primary":
        keep = set(b[b.retenu == 1].pool)
        P("\n== population : B retenu", len(keep), "étude", len(a), "communs", len(keep & set(a.pool)), "B seul", sorted(keep - set(a.pool))[:10], "étude seule", sorted(set(a.pool) - keep)[:10])
    x = a.merge(b, on="pool", suffixes=("", "_B"))
    P(f"\n== {var} : lignes étude {len(a)}, communes {len(x)}, S identique {(x.S == x.S_B).sum()}")
    for m in ["M1", "M2", "M3", "M4", "M5", "M6", "M7"]:
        u, v = x[m].to_numpy(float), x[m + "_B"].to_numpy(float)
        ok = np.isfinite(u) & np.isfinite(v)
        rel = np.abs(u[ok] - v[ok]) / np.maximum(np.abs(u[ok]), 1e-12)
        P(f"{m}: NaN étude {int(np.isnan(u).sum())}, NaN B {int(np.isnan(v).sum())}, écart relatif médian {np.median(rel):.2e}, p95 {np.quantile(rel,.95):.2e}, max {rel.max():.3e}, >1 % : {(rel>0.01).sum()}, >10 % : {(rel>0.1).sum()}, corr rangs {pd.Series(u[ok]).corr(pd.Series(v[ok]), method='spearman'):.5f}")
    if var == "primary":
        rows = []
        for m in ["M1", "M2", "M3", "M4", "M5", "M6", "M7"]:
            rel = (x[m + "_B"] - x[m]).abs() / x[m].abs().clip(lower=1e-12)
            top = x.assign(rel=rel).sort_values("rel", ascending=False).head(10)
            for _, r in top.iterrows():
                rows.append(dict(mesure=m, pool=r.pool, etude=r[m], B=r[m + "_B"], rel=r.rel, n_buyers=r.n_buyers_24h, n_buyers_B=r.n_buyers_24h_B, sol_24h_B=r.sol_24h))
        pd.DataFrame(rows).to_csv(HERE / "b10_diff_tokens.csv", index=False)
        # cap
        y = sel.merge(b[["pool", "cap_S1h", "swap_before_S1_age_s"]], on="pool")
        y = y[y.fdv_s20.notna() & y.cap_S1h.notna() & y.pool.isin(set(a.pool))]
        rel = (y.cap_S1h - y.fdv_s20).abs() / y.fdv_s20
        P("cap B/étude sur le primaire : écart relatif médian", f"{rel.median():.2e}", "max", f"{rel.max():.3e}")
        # DMAGA
        dm = x[x.pool == "CRSwXnfF21yHDXdYBVWwCwQ5Ni2A4QuK3qGYis5k7x7k"].iloc[0]
        for m in ["M1", "M2", "M3", "M4", "M5", "M6", "M7"]:
            P(f"DMAGA {m}: étude {dm[m]:.6f}, B {dm[m+'_B']:.6f}, écart {(dm[m+'_B']-dm[m])/dm[m]*100:+.3f} %")
(HERE / "b10_compare.txt").write_text("\n".join(OUT) + "\n")
