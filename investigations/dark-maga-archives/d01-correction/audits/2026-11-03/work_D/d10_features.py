#!/usr/bin/env python3
"""Auditeur D. Mesures M1-M7 écrites depuis le texte du plan gelé, sur les swaps gelés (lecture seule), pour 212 tokens du principal.
Garde aussi les composantes utiles à l'injection (A3, B3, A24, B24, top5, n acheteurs, paires, réserve). Sortie d10_features.csv.
Contrôle : écart à derived/metrics.csv affiché à la fin (doit être nul)."""
import csv, statistics as st, os, sys
import duckdb
SW = "/Volumes/VERBATIM HD/Dark-MAGA-Investigation/data/controls/swaps/"
ROOT = "audits/2026-11-03/work_D/"
TMP = "/Volumes/VERBATIM HD/Dark-MAGA-Investigation/audits_work/D/duck"
os.makedirs(TMP, exist_ok=True)
con = duckdb.connect(":memory:", config={"memory_limit": "800MB", "threads": 2, "temp_directory": TMP, "preserve_insertion_order": False})
con.execute("SET TimeZone='UTC'")
rows = [r for r in csv.DictReader(open("etude_final/derived/metrics.csv")) if r["variant"] == "primary"]
assert len(rows) == 212
H = 3600
out = csv.writer(open(ROOT + "d10_features.csv", "w", newline=""))
cols = "pool is_dmaga S A3 B3 A24 B24 new24 n24 pairs reserve_S3 m7 top5 early_bought early_held_agg early_held_wallet M1 M2 M3 M4 M5 M6 M7".split()
out.writerow(cols)
maxdiff = {k: 0 for k in "M1 M2 M3 M4 M5 M6 M7".split()}
for i, r in enumerate(rows):
    p, S, cr = r["pool"], int(r["S"]), int(r["created"])
    f = SW + p + ".parquet"
    con.execute(f"CREATE OR REPLACE TEMP VIEW s AS SELECT t,slot,tx_index,owner,qty,sol,vault_pre FROM read_parquet('{f}') WHERE t<{S}")
    A3 = con.execute(f"SELECT coalesce(sum(-sol),0)/1e9 FROM s WHERE qty>0 AND t>={S-3*H}").fetchone()[0]
    w3 = dict(con.execute(f"SELECT (t-{S-75*H})//{3*H} w, sum(-sol)/1e9 FROM s WHERE qty>0 AND t>={S-75*H} AND t<{S-3*H} GROUP BY 1").fetchall())
    B3 = st.median([w3.get(j, 0.0) for j in range(24)])
    A24 = con.execute(f"SELECT coalesce(sum(-sol),0)/1e9 FROM s WHERE qty>0 AND t>={S-24*H}").fetchone()[0]
    w24 = dict(con.execute(f"SELECT (t-{S-96*H})//{24*H} w, sum(-sol)/1e9 FROM s WHERE qty>0 AND t>={S-96*H} AND t<{S-24*H} GROUP BY 1").fetchall())
    B24 = st.median([w24.get(j, 0.0) for j in range(3)])
    new24 = con.execute(f"""SELECT coalesce(sum(-sol),0)/1e9 FROM s WHERE qty>0 AND t>={S-24*H} AND owner NOT IN (SELECT owner FROM s WHERE t<{S-24*H})""").fetchone()[0]
    by = con.execute(f"SELECT owner,sum(-sol)/1e9 v FROM s WHERE qty>0 AND t>={S-24*H} GROUP BY 1 ORDER BY v DESC").fetchall()
    n24 = len(by); top5 = [x[1] for x in by[:5]]
    pairs = con.execute(f"""SELECT coalesce(sum(c*(c-1)/2),0) FROM (SELECT fs,count(*) c FROM (SELECT owner,arg_min(slot,(slot,tx_index)) fs FROM s WHERE qty>0 AND t>={S-24*H} GROUP BY 1) GROUP BY 1)""").fetchone()[0]
    r3 = con.execute(f"SELECT vault_pre FROM s WHERE t<{S-3*H} ORDER BY slot DESC,tx_index DESC LIMIT 1").fetchone()
    res3 = r3[0] / 1e9 if r3 and r3[0] else float("nan")
    m7 = con.execute(f"SELECT max((-sol)*1.0/nullif(vault_pre,0)) FROM s WHERE qty>0 AND t>={S-24*H}").fetchone()[0]
    # M7 : plus gros achat unique, puis rapport à la réserve juste avant lui (lecture stricte du plan)
    m7b = con.execute(f"SELECT (-sol)*1.0/nullif(vault_pre,0) FROM s WHERE qty>0 AND t>={S-24*H} ORDER BY -sol DESC, slot, tx_index LIMIT 1").fetchone()
    m7b = m7b[0] if m7b else None
    e = con.execute(f"""WITH e AS (SELECT DISTINCT owner FROM s WHERE qty>0 AND t<{cr+24*H}),
        a AS (SELECT owner,sum(CASE WHEN qty>0 THEN qty ELSE 0 END) b,sum(CASE WHEN qty<0 THEN -qty ELSE 0 END) d FROM s WHERE owner IN (SELECT owner FROM e) GROUP BY 1)
        SELECT sum(b),sum(greatest(b-d,0)),avg(greatest(b-d,0)*1.0/nullif(b,0)) FROM a""").fetchone()
    eb, eh, ew = e
    M1 = A3 / max(B3, 0.1); M2 = A24 / max(B24, 0.1)
    tot24 = sum(x[1] for x in by)
    M3 = new24 / tot24 if tot24 else None; M4 = sum(top5) / tot24 if tot24 else None
    exp = n24 * (n24 - 1) / 2 / 216000
    M5 = pairs / exp if n24 >= 2 else None
    M6 = eh / eb if eb else None; M7 = m7b
    out.writerow([p, r["is_dmaga"], S, A3, B3, A24, B24, new24, n24, pairs, res3, m7, "|".join(str(x) for x in top5), eb, eh, ew, M1, M2, M3, M4, M5, M6, M7])
    for k, v in zip("M1 M2 M3 M4 M5 M6 M7".split(), [M1, M2, M3, M4, M5, M6, M7]):
        ref = r[k]
        if v is None or ref in ("", "nan"):
            continue
        ref = float(ref)
        d = abs(v - ref) / max(abs(ref), 1e-9)
        maxdiff[k] = max(maxdiff[k], d)
    if i % 50 == 0: print(i, flush=True)
print("écart relatif maximal à metrics.csv", maxdiff, flush=True)
