#!/usr/bin/env python3
"""Solidité du groupe d'avant Musk : sensibilité au seuil, sous-ensembles, ventes comparées. DESCRIPTIF, hors plan gelé.

Le groupe de 33 tient par une arête égale au seuil de 1 M. On le découpe en retirant cette arête et le pont de 15 M du 18/07,
puis on regarde ce qui relie encore les morceaux (SOL, financeur). Sortie : data/group_split.json. Réseau : lecture du financeur G41.
"""
import json

import networkx as nx

from dmaga.config import BIG, DATA
from dmaga.db import connect
from dmaga.positions import positions
from dmaga.helius import Helius, RpcError
from dmaga.labels import label

EV = {e["name"]: e["t"] for e in json.loads((DATA / "events.json").read_text())}
T_LOW, T_HIGH, T0 = EV["musk_borne_basse"], EV["musk_borne_haute"], EV["creation_mint"]
con = connect()
W = f"read_parquet('{BIG}/wallets.parquet')"
g = json.loads((DATA / "prevent_groups.json").read_text())[0]
members = set(g["members"])
E = con.execute(f"""SELECT src, dst, amount, block_time, signature FROM read_parquet('{BIG}/link_edges.parquet')
                    WHERE type='token_direct' AND amount>=1000000 AND block_time<{T_LOW}""").fetchall()
E = [e for e in E if e[0] in members and e[1] in members]
# position juste avant la borne basse : trades plus tous les virements vus seulement par l'API de transferts (issue #27).
# L'ancienne correction n'ajoutait que les arêtes token_direct d'au moins 1 M entre wallets du graphe.
pos = {o: v / 1e6 for o, v in positions(con, T_LOW, str(BIG / "token_edges.parquet")).items()}


def held(ws):
    return sum(max(pos.get(m, 0), 0) for m in ws) / 1e6


def comps(edges):
    G = nx.Graph()
    G.add_nodes_from(members)
    G.add_edges_from((a, b) for a, b, *_ in edges)
    return sorted(nx.connected_components(G), key=len, reverse=True)


strict = comps([e for e in E if e[2] > 1_000_000])
at_seuil = [e for e in E if e[2] == 1_000_000]
# ponts : arêtes dont le retrait coupe le groupe
G = nx.Graph()
G.add_edges_from((a, b) for a, b, *_ in E)
weights = {}
for a, b, q, t, s in E:
    weights[frozenset((a, b))] = weights.get(frozenset((a, b)), 0) + q
bridges = [{"a": a, "b": b, "M": weights[frozenset((a, b))] / 1e6} for a, b in nx.bridges(G)]
big_bridge = [br for br in bridges if br["M"] >= 1 and br["a"] in members and br["b"] in members]
# découpe : retrait de l'arête au seuil, puis du pont qui isole le plus petit bloc de jetons d'au moins 4 wallets
cut1 = [e for e in E if e[2] > 1_000_000]
parts = comps(cut1)
main = parts[0]
Gm = nx.Graph()
Gm.add_edges_from((a, b) for a, b, *_ in cut1 if a in main and b in main)
# règle : un pont fait d'une seule transaction, qui isole au moins 3 wallets. Plusieurs transactions sur une paire ne sont pas un pont faible.
n_tx = {}
for x, y, *_ in cut1:
    n_tx[frozenset((x, y))] = n_tx.get(frozenset((x, y)), 0) + 1
cands = []
for a, b in nx.bridges(Gm):
    if n_tx[frozenset((a, b))] != 1:
        continue
    H = Gm.copy()
    H.remove_edge(a, b)
    small = min(nx.connected_components(H), key=len)
    if len(small) >= 3:
        cands.append((held(small), a, b, sorted(small)))
cands.sort(reverse=True)
subsets = [sorted(p) for p in parts[1:] if len(p) >= 2]
if cands:
    _, a, b, small = cands[0]
    subsets += [small, sorted(main - set(small))]
    pont = {"a": a, "b": b, "M": weights[frozenset((a, b))] / 1e6, "autres_candidats": [(round(c[0], 1), len(c[3])) for c in cands[1:]]}
    faibles = [{"held_M": c[0], "a": c[1], "b": c[2], "M": weights[frozenset((c[1], c[2]))] / 1e6, "members": c[3]} for c in cands]
else:
    subsets.append(sorted(main))
    pont = None
    faibles = []
subsets.sort(key=len, reverse=True)
con.execute("CREATE TEMP TABLE g0(a VARCHAR)")
con.executemany("INSERT INTO g0 VALUES (?)", [[m] for m in members])


def describe(ws):
    con.execute("CREATE OR REPLACE TEMP TABLE s(a VARCHAR)")
    con.executemany("INSERT INTO s VALUES (?)", [[m] for m in ws])
    first_hour = con.execute(f"""SELECT count(DISTINCT owner), coalesce(sum(token_delta),0)/1e12, coalesce(sum(-sol_lamports),0)/1e9 FROM trades
        WHERE kind='swap' AND token_delta>0 AND block_time<{T0 + 3600} AND owner IN (SELECT a FROM s)""").fetchone()
    return {"n": len(ws), "members": ws, "held_M": held(ws), "first_hour_buyers": first_hour[0], "first_hour_M": first_hour[1], "first_hour_sol": first_hour[2]}


sub = [describe(s) for s in subsets]
# liens de SOL entre sous-ensembles
idx = {m: i for i, s in enumerate(subsets) for m in s}
sol_between = []
for a, b, q, t, s in con.execute(f"SELECT src, dst, amount, block_time, signature FROM read_parquet('{BIG}/link_edges.parquet') WHERE type='sol_direct' AND block_time<{T_LOW}").fetchall():
    if a in idx and b in idx and idx[a] != idx[b]:
        sol_between.append({"src": a, "dst": b, "sol": q, "t": t, "sig": s})
bought = {r[0] for r in con.execute(f"SELECT owner FROM {W} WHERE n_buys>0").fetchall()}
try:
    h = Helius(rps=4)
    # le financeur commun cité par l'audit, résolu depuis les virements réels
    src = {x["fromUserAccount"] for x in h.call("getTransfersByAddress", ["AW63YBXXsGcLPpsDTSrpBMdQ9QXtxTiHsTbcVkY6UFv5", {"direction": "in", "limit": 20, "sortOrder": "asc",
           "mint": "So11111111111111111111111111111111111111111"}])["data"] if x["fromUserAccount"] and x["fromUserAccount"].startswith("G41vRrsHSh")}
    assert len(src) == 1
    G41 = src.pop()
    out_rows, tok = [], None
    for _ in range(10):
        c = {"direction": "out", "mint": "So11111111111111111111111111111111111111111", "limit": 100, "sortOrder": "asc",
             "filters": {"blockTime": {"gte": T0 - 86400, "lt": T0 + 3600}, "amount": {"gte": 50_000_000}}}
        if tok:
            c["paginationToken"] = tok
        r = h.call("getTransfersByAddress", [G41, c])
        out_rows += r["data"]
        tok = r.get("paginationToken")
        if not tok:
            break
    in_rows = h.call("getTransfersByAddress", [G41, {"direction": "in", "mint": "So11111111111111111111111111111111111111111", "limit": 100, "sortOrder": "desc",
                                                     "filters": {"blockTime": {"lt": T0}, "amount": {"gte": 100_000_000}}}])["data"]
    first = h.txs_page(G41, details="signatures", sort="asc", limit=1)["data"][0]["blockTime"]
    recent = h.txs_page(G41, details="signatures", sort="desc", limit=1000)
    g41 = {"address": G41, "first_tx": first, "recent_page": len(recent["data"]), "more": bool(recent.get("paginationToken")), "label": label(G41),
           "avant_le_mint": [{"dst": x["toUserAccount"], "sol": x["uiAmount"], "t": x["blockTime"], "sig": x["signature"], "dans_le_groupe": x["toUserAccount"] in members,
                              "a_achete_sur_le_marche": x["toUserAccount"] in bought} for x in out_rows],
           "financeurs": [{"src": x["fromUserAccount"], "label": label(x["fromUserAccount"]), "sol": x["uiAmount"], "t": x["blockTime"], "sig": x["signature"]} for x in in_rows[:12]]}
    g41_source = "Helius, lu à cette exécution"
except (RpcError, RuntimeError) as e:  # pool Helius épuisé (06/11) : la lecture réseau du 03/11 est reprise telle quelle, et dite
    g41 = json.loads((DATA / "group_split.json").read_text())["g41"]
    G41 = g41["address"]
    for x in g41["avant_le_mint"]:  # seuls ces deux champs dépendent des tables locales : recalculés
        x["dans_le_groupe"], x["a_achete_sur_le_marche"] = x["dst"] in members, x["dst"] in bought
    g41_source = f"reprise de data/group_split.json (lecture Helius du 03/11), Helius indisponible : {str(e)[:120]}"
g41["source"] = g41_source

# ventes en 24 h : groupe contre marché, et contre les autres détenteurs d'au moins 1 M à la borne basse
end = T_HIGH + 86400
market = con.execute(f"SELECT coalesce(sum(sol_lamports),0)/1e9 FROM trades WHERE kind='swap' AND token_delta<0 AND block_time>={T_HIGH} AND block_time<{end}").fetchone()[0]
gs = con.execute(f"""SELECT coalesce(sum(sol_lamports),0)/1e9, coalesce(sum(-token_delta),0)/1e12 FROM trades WHERE kind='swap' AND token_delta<0
                     AND block_time>={T_HIGH} AND block_time<{end} AND owner IN (SELECT a FROM g0)""").fetchone()
gt = con.execute(f"""SELECT coalesce(sum(qty),0)/1e6 FROM read_parquet('{BIG}/token_edges.parquet') WHERE block_time>={T_HIGH} AND block_time<{end}
                     AND src IN (SELECT a FROM g0) AND dst NOT IN (SELECT a FROM g0) AND dst <> '(multiple)'""").fetchone()[0]
others = [a for a, v in pos.items() if v >= 1e6 and a not in members]
con.execute("CREATE TEMP TABLE o(a VARCHAR, h DOUBLE)")
con.executemany("INSERT INTO o VALUES (?,?)", [[a, pos[a]] for a in others])
venue = {r[0] for r in con.execute(f"SELECT address FROM read_parquet('{BIG}/nodes.parquet') WHERE kind <> 'wallet'").fetchall()}
oth = con.execute(f"""SELECT sum(q), (SELECT sum(h) FROM o WHERE a NOT IN (SELECT unnest(?)))/1e6, count(*) FROM
    (SELECT o.a, coalesce((SELECT sum(-token_delta)/1e12 FROM trades t WHERE t.owner=o.a AND kind='swap' AND token_delta<0 AND block_time>={T_HIGH} AND block_time<{end}),0) q
     FROM o WHERE o.a NOT IN (SELECT unnest(?)))""", [list(venue), list(venue)]).fetchone()
first60 = con.execute(f"""SELECT count(DISTINCT owner), sum(token_delta)/1e12, sum(-sol_lamports)/1e9 FROM trades WHERE kind='swap' AND token_delta>0 AND block_time<{T0 + 60}""").fetchone()
seq = con.execute(f"""SELECT owner, slot, sum(token_delta)/1e12, sum(-sol_lamports)/1e9 FROM trades WHERE kind='swap' AND token_delta>0 AND slot<=277417696 GROUP BY 1,2 ORDER BY 2""").fetchall()
buys = {k: con.execute(f"SELECT coalesce(sum(-sol_lamports),0)/1e9, count(DISTINCT owner) FROM trades WHERE kind='swap' AND token_delta>0 AND block_time>={a} AND block_time<{b}").fetchone()
        for k, a, b in (("borne_basse_a_envoi", T_LOW, EV["musk_envoi_image"]), ("envoi_a_borne_haute", EV["musk_envoi_image"], T_HIGH + 1))}
first_funder = con.execute(f"""SELECT wallet, arg_min(src, block_time) FROM read_parquet('{BIG}/funding_edges.parquet') WHERE wallet IN (SELECT a FROM g0) AND NOT is_pool GROUP BY 1""").fetchall()
in_group = sum(1 for w, f in first_funder if f in members)
by_g41 = sum(1 for w, f in first_funder if f == G41)
day = con.execute(f"SELECT src, dst, qty, block_time, signature FROM read_parquet('{BIG}/token_edges.parquet') WHERE block_time>={T_LOW - 86400} AND block_time<{T_LOW} AND qty>=1000000 AND src IN (SELECT a FROM g0) AND dst IN (SELECT a FROM g0) ORDER BY block_time").fetchall()
res = {"seuil_strict_tailles": [len(c) for c in strict], "seuil_strict_detenu_M": [held(c) for c in strict], "aretes_au_seuil": [{"src": e[0], "dst": e[1], "t": e[3], "sig": e[4]} for e in at_seuil],
       "pont_retire": pont, "ponts_faibles": faibles, "sous_ensembles": sub, "acheteurs_premiere_heure": con.execute(f"SELECT count(DISTINCT owner) FROM trades WHERE kind='swap' AND token_delta>0 AND block_time<{T0 + 3600} AND owner IN (SELECT a FROM g0)").fetchone()[0], "sol_entre_sous_ensembles": sol_between, "g41": g41,
       "ventes_24h": {"groupe_sol": gs[0], "groupe_M": gs[1], "marche_sol": market, "part_pct": 100 * gs[0] / market, "part_du_detenu_pct": 100 * gs[1] / held(members), "transferts_hors_groupe_M": gt,
                      "autres_detenteurs_n": oth[2], "autres_vendu_M": oth[0], "autres_detenu_M": oth[1], "autres_part_pct": 100 * oth[0] / oth[1] if oth[1] else None},
       "premieres_60s": {"acheteurs": first60[0], "M": first60[1], "sol": first60[2]}, "slot_creation_et_suivant": [[r[0], r[1], r[2], r[3]] for r in seq],
       "achats_fenetre": {k: {"sol": v[0], "wallets": v[1]} for k, v in buys.items()}, "premier_financeur": {"dans_le_groupe": in_group, "g41": by_g41, "n": len(first_funder)},
       "gestes_du_jour": [{"src": d[0], "dst": d[1], "M": d[2] / 1e6, "t": d[3], "sig": d[4]} for d in day]}
(DATA / "group_split.json").write_text(json.dumps(res, indent=1, ensure_ascii=False))
print("strict", res["seuil_strict_tailles"], [round(x, 1) for x in res["seuil_strict_detenu_M"]], "pont", pont)
print("sous-ensembles", [(s["n"], round(s["held_M"], 1), s["first_hour_buyers"], round(s["first_hour_M"], 1)) for s in sub])
print("SOL entre sous-ensembles", [(x["src"][:8], x["dst"][:8], round(x["sol"], 2), x["t"]) for x in sol_between][:8])
print("G41", G41, "1re tx", g41["first_tx"], "récentes", g41["recent_page"], g41["more"], "avant mint", len(g41["avant_le_mint"]))
print(" vers", [(x["dst"][:8], x["sol"], x["t"], x["dans_le_groupe"], x["a_achete_sur_le_marche"]) for x in g41["avant_le_mint"]][:22])
print(" financeurs", [(x["src"][:10], x["label"], x["sol"], x["t"]) for x in g41["financeurs"]][:8])
print("ventes", {k: round(v, 1) if isinstance(v, float) else v for k, v in res["ventes_24h"].items()})
print("60 s", res["premieres_60s"], "fenêtres", res["achats_fenetre"], "1er financeur", res["premier_financeur"], "gestes", len(res["gestes_du_jour"]))
