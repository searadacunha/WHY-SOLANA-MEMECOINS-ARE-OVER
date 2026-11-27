"""Phase 2 : seuils de bascule de DMAGA exprimés en unités du token, intégrité du parseur de B, part de transactions réussies dans l'heure S.
Sortie : b25_seuils.txt."""
import gc, json
from pathlib import Path
import numpy as np, pandas as pd, pyarrow as pa, pyarrow.parquet as pq
pa.set_memory_pool(pa.system_memory_pool())
HERE = Path(__file__).parent; ROOT = HERE.parents[2]
EXT = Path("/Volumes/VERBATIM HD/Dark-MAGA-Investigation"); TOK = EXT / "audits_work/B/tok"
DM = "CRSwXnfF21yHDXdYBVWwCwQ5Ni2A4QuK3qGYis5k7x7k"
L = []
def P(*a):
    s = " ".join(str(x) for x in a); L.append(s); print(s, flush=True)
F = {}
for line in open(HERE / "b12_features.jsonl"):
    r = json.loads(line); F[r["pool"]] = r
mt = pd.read_csv(ROOT / "etude_final/derived/metrics.csv"); mt = mt[(mt.variant == "primary")]
D = mt[mt.pool == DM].iloc[0]; C = mt[mt.pool != DM]; f = F[DM]
den1, den2 = np.median(f["m1_windows"]), np.median(f["m2_windows"])
P(f"M1 : max pairs {C.M1.max():.1f}, il faudrait {C.M1.max()*den1:.0f} SOL sur 3 h (observé {f['num3']:.1f}), facteur {C.M1.max()/D.M1:.1f}")
P(f"M2 : max pairs {C.M2.max():.1f}, il faudrait {C.M2.max()*den2:.0f} SOL sur 24 h (observé {f['num24']:.1f}), facteur {C.M2.max()/D.M2:.1f}")
P(f"M3 : {(C.M3 >= 1 - 1e-12).sum()} pairs à 1,0 : DMAGA ne peut pas faire mieux que p = {(1 + (C.M3 >= 1 - 1e-12).sum()) / 212:.4f}")
P(f"M4 : {(C.M4 >= 1 - 1e-12).sum()} pairs à 1,0 : DMAGA ne peut pas faire mieux que p = {(1 + (C.M4 >= 1 - 1e-12).sum()) / 212:.4f}")
n = f["n_buyers"]; ex = n * (n - 1) / 2 / 216000
P(f"M5 : max pairs {C.M5.max():.1f}, à {n} acheteurs il faudrait {C.M5.max()*ex:.0f} paires dans le même slot (observé {f['pairs']:.0f}), facteur {C.M5.max()/D.M5:.1f}")
P(f"M6 : max pairs {C.M6.max():.4f}, facteur {C.M6.max()/D.M6:.2f}, cotes x{(C.M6.max()/(1-C.M6.max()))/(D.M6/(1-D.M6)):.2f}")
P(f"M7 : max pairs {C.M7.max():.3f}, à la réserve de S−3 h ({f['res_S3h']:.1f} SOL) un achat de {C.M7.max()*f['res_S3h']:.0f} SOL ; observé {f['maxbuy']:.1f} SOL sur {f['maxbuy_res']:.1f}, facteur {C.M7.max()/D.M7:.1f}")
top = {m: C.sort_values(m, ascending=False).iloc[0] for m in ["M1", "M2", "M5", "M7", "M6"]}
for m, r in top.items():
    x = F[r.pool]
    P(f"Plus haut pair {m} : {r.pool} valeur {r[m]:.3f}, acheteurs 24 h {x['n_buyers']}, SOL 24 h {x['num24']:.1f}, dén. M1 {np.median(x['m1_windows']):.2f}, dén. M2 {np.median(x['m2_windows']):.2f}, cap S−1 h {x['cap_S1h']}")
# intégrité B
st = {}
for line in open(HERE / "b02_stats.jsonl"):
    s = json.loads(line); st[s["pool"]] = s
S = list(st.values())
comp = [s for s in S if s["cursor_complete"]]
P("pools", len(S), "complets", len(comp), "ruptures WSOL", sum(s["chain_breaks"] for s in comp), "ruptures vault jeton", sum(s["chain_breaks_tok"] for s in comp), "tokens avec rupture jeton", sum(1 for s in comp if s["chain_breaks_tok"]), "non monotones", sum(s["non_mono"] for s in S), "doublons", sum(s["dups"] for s in S), "lignes = curseur", all(s["lines"] == s["cursor_n"] for s in S), "décimales", sorted({k for s in S for k in s["decimals"]}))
tot = lambda k: sum(s["counts"].get(k, 0) for s in comp)
P("comptes B (245 complets) : tx", tot("tx"), "swap", tot("swap"), "part<5%", tot("part_sous_5pct"), "non signataires deux côtés", tot("nonsign_oppose"), "swaps sans bénéficiaire", tot("swap_sans_beneficiaire"), "parts>1", tot("swap_parts_sup_1"), "multi", tot("swap_multi_benef"))
P("part des swaps sans bénéficiaire : tous", round(tot("swap_sans_beneficiaire") / tot("swap"), 4), "DMAGA", round(st[DM]["counts"]["swap_sans_beneficiaire"] / st[DM]["counts"]["swap"], 4))
# part réussie dans l'heure S
pk = pd.read_csv(HERE / "b01_peak.csv").set_index("pool")
rows = []
for p in mt.pool:
    t = pq.read_table(TOK / f"{p}.res.parquet", columns=["time"], use_threads=False)["time"].to_numpy()
    h = int(pk.loc[p, "S20"]); rows.append((p, int(((t >= h * 3600) & (t < (h + 1) * 3600)).sum()), int(pk.loc[p, "nS20"])))
    del t
R = pd.DataFrame(rows, columns=["pool", "tx_vault", "nS"]); R["ratio"] = R.tx_vault / R.nS
Cc = R[R.pool != DM]; dd = R[R.pool == DM].iloc[0]
P(f"Heure S : tx réussies touchant le vault / signatures : DMAGA {dd.tx_vault}/{dd.nS} = {dd.ratio:.3f} ; pairs médiane {Cc.ratio.median():.3f}, quartiles {Cc.ratio.quantile(.25):.3f} à {Cc.ratio.quantile(.75):.3f}, sous 0,2 : {(Cc.ratio < .2).sum()}, sous 0,1 : {(Cc.ratio < .1).sum()}, sous 0,05 : {(Cc.ratio < .05).sum()} sur {len(Cc)}")
R.to_csv(HERE / "b25_heure_S.csv", index=False)
# pairs à spam probable face aux autres
m2 = mt.merge(R, on="pool"); m2 = m2[m2.pool != DM]
lo = m2[m2.ratio < .2]; hi = m2[m2.ratio >= .2]
P("EXPLORATOIRE, DMAGA face aux pairs dont >= 20 % des signatures de l'heure S sont des tx réussies touchant le vault : k", len(hi), {m: round((1 + (hi[m] >= D[m]).sum()) / (len(hi) + 1), 3) for m in ["M1", "M2", "M3", "M4", "M5", "M6", "M7"]})
P("médianes pairs faible ratio (<0,2) :", lo[["M1", "M2", "M3", "M5", "M6", "M7"]].median().round(3).to_dict(), " ; autres :", hi[["M1", "M2", "M3", "M5", "M6", "M7"]].median().round(3).to_dict())
# variantes M3b, M6b, M7b
r = pd.read_csv(HERE / "b04_ranks_blind.csv")
P("variantes d'ambiguïté :", r[r.mesure.isin(["M3b", "M6b", "M7b"])][["mesure", "D", "ge", "p"]].round(4).to_dict("records"))
(HERE / "b25_seuils.txt").write_text("\n".join(L) + "\n")
