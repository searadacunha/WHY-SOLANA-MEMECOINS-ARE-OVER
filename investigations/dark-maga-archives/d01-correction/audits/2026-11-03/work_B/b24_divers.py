"""Phase 2 : vérifications restantes. Migrations depuis le brut ; part des pairs dont [S−3 h, S) dépasse leurs 24 fenêtres passées (comme S1) ;
lignes étude seule / B seule sur toute la population ; causes M6 9ny2 et M7 Ew6W ; comparateurs du test financeur. Sortie : b24_divers.txt."""
import gc, gzip, json, os
from pathlib import Path
import numpy as np, pandas as pd, pyarrow as pa, pyarrow.parquet as pq
pa.set_memory_pool(pa.system_memory_pool())
HERE = Path(__file__).parent; ROOT = HERE.parents[2]
EXT = Path("/Volumes/VERBATIM HD/Dark-MAGA-Investigation")
TOK = EXT / "audits_work/B/tok"; SW = EXT / "data/controls/swaps"
DM = "CRSwXnfF21yHDXdYBVWwCwQ5Ni2A4QuK3qGYis5k7x7k"
L = []
def P(*a):
    s = " ".join(str(x) for x in a); L.append(s); print(s, flush=True)
# 1. migrations
d = EXT / "raw/ctrl_migrations"
cur = json.loads((d / "cursor.json").read_text())
P("curseur migrations :", {k: cur[k] for k in ("filters", "n", "page", "complete")})
n = init = 0; pools_seen = 0; ts = []
for fn in sorted(x for x in os.listdir(d) if x.endswith(".jsonl.gz") and not x.startswith("._")):
    with gzip.open(d / fn, "rt") as f:
        for line in f:
            t = json.loads(line); n += 1
            if t["meta"].get("err") is None and any("initialize2" in l for l in (t["meta"].get("logMessages") or [])):
                init += 1
P("tx brutes", n, "avec initialize2", init)
mig = pd.read_json(EXT / "data/controls/migrations.jsonl", lines=True)
P("migrations.jsonl", len(mig), "pools distincts", mig.pool.nunique(), "mints distincts", mig["mint"].nunique(), "created min", pd.to_datetime(mig.created.min(), unit="s"), "max", pd.to_datetime(mig.created.max(), unit="s"))
# 2. réveil avant le pic chez les pairs (comme S1, à E = S)
F = {}
for line in open(HERE / "b12_features.jsonl"):
    r = json.loads(line); F[r["pool"]] = r
pop = pd.read_csv(HERE / "blind_metrics.csv"); pop = pop[pop.retenu == 1]
top = sec = 0; rows = []
for p in pop.pool:
    f = F[p]; w = np.array(f["m1_windows"]); x = f["num3"]
    c = int((w >= x).sum()); rows.append((p, c, x, np.median(w)))
R = pd.DataFrame(rows, columns=["pool", "c", "num3", "med"]); C = R[R.pool != DM]
P(f"Pairs dont [S−3 h, S) dépasse les 24 fenêtres précédentes : {(C.c == 0).sum()}/211 = {(C.c == 0).mean():.3f} ; au plus 1 au-dessus : {(C.c <= 1).sum()}/211 = {(C.c <= 1).mean():.3f} ; DMAGA à S : c = {int(R[R.pool == DM].c.iloc[0])}")
P(f"Pairs avec [S−3 h, S) >= 10 fois la médiane passée : {(C.num3 >= 10 * C.med.clip(lower=.1)).mean():.3f}")
# 3. lignes étude seule et B seule, toute la population
tot = {"etude": 0, "b": 0, "seule_etude": 0, "seule_b": 0, "sol_seule_etude": 0.0, "sol_seule_b": 0.0, "sol_etude": 0.0, "qty_sup": 0, "communes": 0}
worst = []
for p in pop.pool:
    s = pq.read_table(SW / f"{p}.parquet", columns=["slot", "tx_index", "owner", "qty", "sol"], use_threads=False).to_pandas()
    r = pq.read_table(TOK / f"{p}.parquet", columns=["slot", "idx", "w", "sol", "tok"], use_threads=False).to_pandas()
    w = (TOK / f"{p}.wallets.txt").read_text().split("\n")
    r["owner"] = [w[i] for i in r.w]
    x = s.merge(r.rename(columns={"idx": "tx_index"}), on=["slot", "tx_index", "owner"], how="outer", indicator=True)
    a = x[x._merge == "left_only"]; b = x[x._merge == "right_only"]; c = x[x._merge == "both"]
    tot["etude"] += len(s); tot["b"] += len(r); tot["seule_etude"] += len(a); tot["seule_b"] += len(b); tot["sol_seule_etude"] += a.sol_x.abs().sum() / 1e9; tot["sol_seule_b"] += b.sol_y.sum() / 1e9; tot["sol_etude"] += s.sol.abs().sum() / 1e9
    tot["qty_sup"] += int((c.qty.abs() > c.tok * 1.01).sum()); tot["communes"] += len(c)
    if len(a): worst.append((p[:10], len(a), round(a.sol_x.abs().sum() / 1e9, 3), round(a.sol_x.abs().max() / 1e9, 3), a.owner.value_counts().index[0][:12]))
    del s, r, x, a, b, c, w; gc.collect()
P("Lignes population :", tot)
P("Tokens les plus touchés par les lignes étude seule :", sorted(worst, key=lambda z: -z[2])[:6])
# 4. cas M7 et M6
for pool, S_win in (("Ew6WHMMFDkRtqVrVVT7zu9HSt8NLHH7tmcXx9VrLtzRr", None), ("9ny2CD5PcmNgRUvyeLzkFTTXctidJrany4FyQ7Kai7dr", None)):
    S = int(pop[pop.pool == pool].S.iloc[0]); cr = int(pop[pop.pool == pool].created.iloc[0])
    s = pq.read_table(SW / f"{pool}.parquet").to_pandas(); r = pq.read_table(TOK / f"{pool}.parquet").to_pandas()
    wl = (TOK / f"{pool}.wallets.txt").read_text().split("\n"); r["owner"] = [wl[i] for i in r.w]
    sb = s[(s.t >= S - 86400) & (s.t < S) & (s.qty > 0) & (s.sol < 0)].assign(S=lambda z: -z.sol / 1e9).sort_values("S", ascending=False).head(2)
    rb = r[(r.time >= S - 86400) & (r.time < S) & (r.side == 1)].assign(S=lambda z: z.sol / 1e9).sort_values("S", ascending=False).head(2)
    P(pool[:10], "plus gros achats étude", sb[["slot", "tx_index", "owner", "S", "qty", "vault_pre"]].to_dict("records"))
    P(pool[:10], "plus gros achats B", rb[["slot", "idx", "owner", "S", "tok"]].to_dict("records"))
    early_s = s[(s.t < cr + 86400) & (s.qty > 0) & (s.sol < 0)].owner.unique()
    P(pool[:10], "précoces étude", len(early_s), "achats qty étude", s[s.owner.isin(early_s) & (s.t < S) & (s.qty > 0)].groupby("owner").qty.sum().sort_values(ascending=False).head(3).to_dict(), "ventes", s[s.owner.isin(early_s) & (s.t < S) & (s.qty < 0)].groupby("owner").qty.sum().to_dict() if len(early_s) < 6 else "")
    P(pool[:10], "achats tok B", r[r.owner.isin(early_s) & (r.time < S) & (r.side == 1)].groupby("owner").tok.sum().sort_values(ascending=False).head(3).to_dict(), "ventes", r[r.owner.isin(early_s) & (r.time < S) & (r.side == -1)].groupby("owner").tok.sum().to_dict() if len(early_s) < 6 else "")
    del s, r
# 5. financeur
fj = json.load(open(ROOT / "etude_final/tables/funder_share.json"))
v = [c["part"] for c in fj["comparateurs"]]
pp = set(pop.pool)
P("financeur : k", len(v), "p recalculé", (1 + sum(x >= fj["dmaga"]["part"] for x in v)) / (len(v) + 1), "médiane", float(np.median(v)), "non nuls", sum(x > 0 for x in v), "comparateurs hors population principale", [c["pool"][:10] for c in fj["comparateurs"] if c["pool"] not in pp])
(HERE / "b24_divers.txt").write_text("\n".join(L) + "\n")
