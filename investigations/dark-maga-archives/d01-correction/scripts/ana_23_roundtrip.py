#!/usr/bin/env python3
"""Allers-retours sous 10 s et étiquette bot_aller_retour. Descriptif, sans réseau, écrit depuis la règle de l'audit (A-04, K06).

Aller-retour : pour un même propriétaire, un achat suivi d'une vente de même quantité à 1 % près sous 10 s.
bot_aller_retour, à partir de 100 SOL achetés : plus de 50 % d'allers-retours, ou jamais signataire avec un programme propre (programme non
générique sur au moins 80 % de ses lignes et vu chez au plus 5 propriétaires non signataires). L'étiquette sert aux classements d'acheteurs.
Elle ne dit rien de l'opérateur et ne touche ni nodes.parquet ni les liens. Sorties : BIG/bots.parquet, DATA/roundtrip.json.
Programme 3GMsedVP (A-16) : non identifié, ses 45 signataires restent hors de l'étiquette tant qu'aucune conclusion n'est possible.
"""
import json
from collections import Counter

import pyarrow as pa
import pyarrow.parquet as pq

from dmaga.db import connect
from dmaga.paths import BIG, DATA, exige_v2

exige_v2()
EV = {e["name"]: e["t"] for e in json.loads((DATA / "events.json").read_text())}
LOW, ENV, HIGH, WIN = EV["musk_borne_basse"], EV["musk_envoi_image"], EV["musk_borne_haute"], EV["winig_visuel"]
S = 1721588400  # pic gelé de DMAGA, 21/07/2024 19:00 UTC (etude_final, tests.json)
FEN = {"fenetre_musk": (LOW, HIGH + 1), "envoi_a_borne_haute": (ENV, HIGH), "24h_apres_musk": (HIGH, HIGH + 86400), "3h_avant_envoi": (ENV - 10800, ENV),
       "3h_avant_winig": (WIN - 10800, WIN), "24h_avant_pic": (S - 86400, S)}
con = connect(mem="600MB")
cur = con.execute("""SELECT owner, block_time, token_delta, CASE WHEN token_delta>0 THEN -sol_lamports ELSE sol_lamports END v,
                     contains(coalesce(signers, ''), owner) sg FROM trades WHERE kind='swap' ORDER BY owner, slot, tx_index""")
rt_owner, buy_owner, sg_owner, n_owner, rt_win, buy_win = Counter(), Counter(), Counter(), Counter(), Counter(), Counter()


def traite(own, lignes):
    ouverts = []  # achats encore appariables
    for t, d, v, sg in lignes:
        n_owner[own] += 1
        sg_owner[own] += bool(sg)
        if d > 0:
            buy_owner[own] += v
            for k, (a, z) in FEN.items():
                if a <= t < z:
                    buy_win[k] += v
            ouverts.append([t, d, v])
        else:
            for b in ouverts:
                if b[1] and t - b[0] <= 10 and abs(-d - b[1]) <= 0.01 * b[1]:
                    rt_owner[own] += b[2]
                    for k, (a, z) in FEN.items():
                        if a <= b[0] < z:
                            rt_win[k] += b[2]
                    b[1] = 0
                    break
            ouverts = [b for b in ouverts if b[1] and t - b[0] <= 10]


own, buf = None, []
while True:
    chunk = cur.fetchmany(20000)
    if not chunk:
        break
    for o, t, d, v, sg in chunk:
        if o != own:
            if own is not None:
                traite(own, buf)
            own, buf = o, []
        buf.append((t, d, v, sg))
if own is not None:
    traite(own, buf)

# programmes propres, sur les seuls wallets assez gros et jamais signataires
grands = [o for o, v in buy_owner.items() if v >= 100e9 and not sg_owner[o]]
con.execute("CREATE TEMP TABLE g(a VARCHAR)")
con.executemany("INSERT INTO g VALUES (?)", [[a] for a in grands])
P = f"read_parquet('{BIG}/owner_programs.parquet')"
propres = {r[0]: r[1] for r in con.execute(f"""WITH uses AS (SELECT program, count(DISTINCT owner) n_own FROM {P} GROUP BY 1),
    parts AS (SELECT p.owner, p.program, count(DISTINCT p.signature) n FROM {P} p WHERE p.owner IN (SELECT a FROM g) GROUP BY 1, 2),
    tot AS (SELECT owner, count(DISTINCT signature) n FROM {P} WHERE owner IN (SELECT a FROM g) GROUP BY 1)
    SELECT parts.owner, arg_max(parts.program, parts.n) FROM parts JOIN tot USING (owner) JOIN uses USING (program)
    WHERE parts.n >= 0.8 * tot.n AND uses.n_own <= 5 GROUP BY 1""").fetchall()}
rows = []
for o, v in buy_owner.items():
    part = rt_owner[o] / v if v else 0.0
    motif = None
    if v >= 100e9 and part > 0.5:
        motif = "plus de 50 % d'allers-retours"
    elif o in propres:
        motif = "jamais signataire, programme propre"
    rows.append({"owner": o, "bought_sol": v / 1e9, "aller_retour_sol": rt_owner[o] / 1e9, "part_aller_retour": part, "lignes": n_owner[o], "lignes_signataire": sg_owner[o],
                 "programme": propres.get(o), "bot_aller_retour": motif is not None, "motif": motif})
pq.write_table(pa.Table.from_pylist(rows), BIG / "bots.parquet", compression="zstd")
tot = sum(buy_owner.values())
bots = [r for r in rows if r["bot_aller_retour"]]
top = sorted(rows, key=lambda r: -r["bought_sol"])[:12]
res = {"achats_sol": tot / 1e9, "allers_retours_sol": sum(rt_owner.values()) / 1e9, "part_pct": 100 * sum(rt_owner.values()) / tot,
       "fenetres": {k: {"achats_sol": buy_win[k] / 1e9, "allers_retours_sol": rt_win[k] / 1e9, "part_pct": 100 * rt_win[k] / buy_win[k] if buy_win[k] else None} for k in FEN},
       "bots": {"n": len(bots), "sol": sum(r["bought_sol"] for r in bots), "plus_de_50": sum(1 for r in bots if r["motif"].startswith("plus")), "programme_propre": sum(1 for r in bots if r["motif"].startswith("jamais"))},
       "plus_de_50_cent_sol": {"n": sum(1 for r in rows if r["bought_sol"] >= 100 and r["part_aller_retour"] > 0.5), "sol": sum(r["bought_sol"] for r in rows if r["bought_sol"] >= 100 and r["part_aller_retour"] > 0.5)},
       "top_acheteurs": top}
(DATA / "roundtrip.json").write_text(json.dumps(res, indent=1, ensure_ascii=False))
print({k: v for k, v in res.items() if k not in ("top_acheteurs",)})
for r in top:
    print(r["owner"], round(r["bought_sol"], 1), round(100 * r["part_aller_retour"], 1), r["lignes_signataire"], r["lignes"], r["bot_aller_retour"], r["motif"], r["programme"])
