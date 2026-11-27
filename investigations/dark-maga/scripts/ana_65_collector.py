#!/usr/bin/env python3
"""Instruit le collecteur 9W9b3zg : adresse de dépôt d'échange ou wallet ordinaire ? DESCRIPTIF, hors plan gelé.

Mesure sur tout l'historique SOL : part des sorties vers des hot wallets, délai entre entrée et sortie, expéditeurs, et lesquels sont
des wallets de l'enquête. Écrit data/collector.json. Une adresse de dépôt appartient à un client de l'échange, mais n'importe qui
peut y envoyer des fonds : c'est un fort indice de lien, pas une identité.
"""
import json
from collections import Counter, defaultdict

from dmaga.config import BIG, DATA
from dmaga.db import connect
from dmaga.helius import Helius
from dmaga.labels import label

A = "9W9b3zgHH9mCEHDhsdbnbEPHStm9vvXS4aia4DWHBxpL"
NATIVE = "So11111111111111111111111111111111111111111"
h = Helius(rps=4)


def all_rows(direction, cap=60):
    rows, tok = [], None
    for _ in range(cap):
        c = {"direction": direction, "mint": NATIVE, "limit": 100, "sortOrder": "asc", "filters": {"amount": {"gte": 1_000_000}}}
        if tok:
            c["paginationToken"] = tok
        r = h.call("getTransfersByAddress", [A, c])
        rows += r["data"]
        tok = r.get("paginationToken")
        if not tok:
            return rows, False
    return rows, True


inn, t1 = all_rows("in")
out, t2 = all_rows("out")
con = connect()
g = json.loads((DATA / "prevent_groups.json").read_text())[0]
members = set(g["members"])
C = "8YLEuUtZ4eFMJbf46oNb1CeG6dYFWGyxnQSh9hrgzBzR"
pnl = {r[0]: r[1] for r in con.execute(f"SELECT owner, realized_sol FROM read_parquet('{BIG}/wallets.parquet')").fetchall()}
s_in, n_in, first = Counter(), Counter(), {}
for x in inn:
    a = x["fromUserAccount"]
    s_in[a] += float(x["uiAmount"])
    n_in[a] += 1
    first.setdefault(a, (x["blockTime"], x["signature"]))
s_out = Counter()
for x in out:
    s_out[x["toUserAccount"]] += float(x["uiAmount"])
tot_out = sum(s_out.values())
cex = {k: v for k, v in s_out.items() if label(k) and "Coinbase" in label(k)}
times = sorted([(x["blockTime"], "in", float(x["uiAmount"])) for x in inn] + [(x["blockTime"], "out", float(x["uiAmount"])) for x in out])
gaps = []
last_in = None
for t, k, _ in times:
    if k == "in":
        last_in = t
    elif last_in is not None:
        gaps.append(t - last_in)
gaps.sort()
in_group = [{"wallet": a, "sol": s_in[a], "n": n_in[a], "first": first[a][0], "sig": first[a][1], "groupe": a in members, "createur": a == C, "realise_dmaga": pnl.get(a)}
            for a in s_in if a in members or a == C or a in pnl]
in_group.sort(key=lambda r: r["first"])
res = {"address": A, "n_in": len(inn), "n_out": len(out), "tronque": t1 or t2, "expediteurs": len(s_in), "total_in_sol": sum(s_in.values()), "total_out_sol": tot_out,
       "vers_coinbase_sol": sum(cex.values()), "part_coinbase_pct": 100 * sum(cex.values()) / tot_out if tot_out else None,
       "detail_coinbase": cex, "autres_sorties": [(k, label(k), round(v, 2)) for k, v in s_out.most_common(12) if k not in cex],
       "delai_median_s": gaps[len(gaps) // 2] if gaps else None, "premier_t": times[0][0], "dernier_t": times[-1][0], "wallets_de_l_enquete": in_group}
(DATA / "collector.json").write_text(json.dumps(res, indent=1, ensure_ascii=False))
print({k: (round(v, 1) if isinstance(v, float) else v) for k, v in res.items() if k not in ("wallets_de_l_enquete", "detail_coinbase", "autres_sorties")})
print("autres sorties", res["autres_sorties"][:8])
for r in in_group:
    print(r["wallet"][:10], "G" if r["groupe"] else "-", "C" if r["createur"] else "-", round(r["sol"], 3), "n", r["n"], r["first"], "réalisé", round(r["realise_dmaga"] or 0))

# Vérification ligne à ligne des deux salves, et ensemble élargi : groupes d'avant Musk ayant au moins un membre parmi les expéditeurs
BURSTS = [("23/07/2024", 1721700000, 1721702000), ("26/01/2025", 1737907000, 1737912000)]
checked = []
for name, a, b in BURSTS:
    for x in inn:
        if a <= x["blockTime"] <= b:
            t = h.call("getTransaction", [x["signature"], {"encoding": "jsonParsed", "maxSupportedTransactionVersion": 1}])
            sig = [k["pubkey"] for k in t["transaction"]["message"]["accountKeys"] if k.get("signer")]
            progs = sorted({i.get("programId") for i in t["transaction"]["message"]["instructions"]})
            checked.append({"salve": name, "wallet": x["fromUserAccount"], "sol": x["uiAmount"], "t": x["blockTime"], "signature": x["signature"], "signataires": sig,
                            "signe_par_expediteur": x["fromUserAccount"] in sig, "programmes": progs,
                            "groupe": x["fromUserAccount"] in members, "createur": x["fromUserAccount"] == C})
groups = json.loads((DATA / "prevent_groups.json").read_text())
senders = set(s_in)
touched = [g_ for g_ in groups if senders & set(g_["members"])]
res["salves"] = checked
res["groupes_touches"] = [{"n": g_["n"], "held_M": g_["held_before_musk_M"], "realized_sol": g_["realized_sol"], "expediteurs": sorted(senders & set(g_["members"]))} for g_ in touched]
res["ensemble_elargi_held_M"] = sum(g_["held_before_musk_M"] for g_ in touched)
(DATA / "collector.json").write_text(json.dumps(res, indent=1, ensure_ascii=False))
print("salves", [(c["salve"], c["wallet"][:8], c["sol"], c["signe_par_expediteur"], c["groupe"], c["createur"]) for c in checked])
print("groupes touchés", [(g_["n"], round(g_["held_M"], 1), [e[:8] for e in g_["expediteurs"]]) for g_ in res["groupes_touches"]], "élargi M", round(res["ensemble_elargi_held_M"], 1), "délai médian s", res["delai_median_s"])
