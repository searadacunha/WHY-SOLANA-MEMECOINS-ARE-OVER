"""Phase 2 : reproduit derived/metrics.csv avec le code gelé (metrics.compute) sur les swaps gelés, token par token ; relance parse_swaps gelé sur le brut
de 6 tokens et compare au parquet. Sortie : b23_repro.jsonl (reprise), b23_repro.txt. Rien n'est écrit dans etude_final."""
import gc, gzip, json, os, sys, types
from collections import Counter
from pathlib import Path
import numpy as np, pandas as pd, pyarrow as pa, pyarrow.parquet as pq
HERE = Path(__file__).parent; ROOT = HERE.parents[2]
pa.set_memory_pool(pa.system_memory_pool())
sys.path.insert(0, str(ROOT / "etude_final/code"))
from metrics import compute, METRICS
EXT = Path("/Volumes/VERBATIM HD/Dark-MAGA-Investigation")
SW = EXT / "data/controls/swaps"
OUT = HERE / "b23_repro.jsonl"
mt = pd.read_csv(ROOT / "etude_final/derived/metrics.csv")
done = set()
if OUT.exists():
    done = {json.loads(l)["pool"] for l in open(OUT)}
for pool, g in mt.groupby("pool", sort=False):
    if pool in done: continue
    t = pq.read_table(SW / f"{pool}.parquet", columns=["t", "slot", "tx_index", "owner", "qty", "sol", "vault_pre"], use_threads=False)
    ow = t["owner"].to_pandas()
    o = pd.factorize(ow)[0].astype(np.int64); del ow
    arr = [t[c].to_numpy() for c in ("t", "slot")] + [o] + [t[c].to_numpy() for c in ("qty", "sol", "vault_pre")]
    del t
    worst = 0.0; nv = 0
    for _, r in g.iterrows():
        m = compute(*arr, int(r.S), int(r.created))
        for k in METRICS:
            a, b = m[k], r[k]
            if a != a and b != b: continue
            worst = max(worst, abs(a - b) / max(abs(b), 1e-12)); nv += 1
    with open(OUT, "a") as f:
        f.write(json.dumps({"pool": pool, "rows": len(g), "n": nv, "ecart_max": worst}) + "\n")
    del arr, o; gc.collect()
d = pd.read_json(OUT, lines=True)
L = [f"tokens {len(d)}, lignes {d.rows.sum()}, valeurs comparées {d.n.sum()}, écart relatif max {d.ecart_max.max():.2e}"]
# parse_swaps gelé sur le brut de 6 tokens
stub = types.ModuleType("dmaga.collect")
from chainutil import _keys, _signers, token_deltas  # noqa
sel = {}
want = ["CRSwXnfF21yHDXdYBVWwCwQ5Ni2A4QuK3qGYis5k7x7k", "E1MJhRuLjnjXr24TD5QgcKH9RFb2JbBJx2GqAwmYX1zh", "Ho5k1boxm4sXGpLBfFdd9kBY9gP1QDRB55GRE3T2eTL2", "124TgDq59sdBHBYS7YGp3T5Do88MNHE7ws6X7h6Q6SkA"]
for line in open(EXT / "data/controls/selection.jsonl"):
    r = json.loads(line)
    if r["pool"] in want: sel[r["pool"]] = r
import importlib.util, ast
src = (ROOT / "etude_final/code/col_50_ctrl.py").read_text()
tree = ast.parse(src)
fn = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "parse_swaps")
ns = {"_keys": _keys, "_signers": _signers, "token_deltas": token_deltas, "FEE_SHARE": 0.05, "Counter": Counter}
exec(compile(ast.Module([fn], []), "parse_swaps", "exec"), ns)
parse = ns["parse_swaps"]
for pool in want:
    r = sel[pool]; d_ = EXT / "raw/ctrl_tx" / pool; st = Counter(); out = []
    for fn_ in sorted(x for x in os.listdir(d_) if x.endswith(".jsonl.gz") and not x.startswith("._")):
        with gzip.open(d_ / fn_, "rt") as f:
            for line in f:
                out.extend(parse(json.loads(line), r["mint"], r["vault_token"], r["vault_sol"], st))
    a = pd.DataFrame(out).sort_values(["slot", "tx_index", "owner"]).reset_index(drop=True)
    b = pq.read_table(SW / f"{pool}.parquet").to_pandas().sort_values(["slot", "tx_index", "owner"]).reset_index(drop=True)
    same = len(a) == len(b) and (a.qty.values == b.qty.values).all() and (a.sol.values == b.sol.values).all() and (a.owner.values == b.owner.values).all() and (a.vault_pre.values == b.vault_pre.values).all()
    L.append(f"parse_swaps gelé sur brut {pool[:10]} : lignes {len(a)} contre parquet {len(b)}, identique {bool(same)}, comptes {dict(st)}")
    del a, b, out; gc.collect()
(HERE / "b23_repro.txt").write_text("\n".join(L) + "\n")
print("\n".join(L))
