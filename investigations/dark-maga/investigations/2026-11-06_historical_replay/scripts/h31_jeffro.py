"""Rejeu des affirmations de @JeffroBTC (post 1815291249102119198, 22/07/2024 07:42:14 UTC) sur 7GVC, 9Sxm et trois satellites.

Sources : grand livre décodé de 7GVC (h30, transactions complètes du RPC public), trades DMAGA de l'enquête d'origine
(data_v2/trades.parquet : courbe, pool et venues complets, Helius), cours SOLUSDT Binance à la minute. Chaque ligne de
data/jeffro_claims.csv cite ses signatures ; h39 fige les reçus. Les abréviations sont résolues parmi les contreparties observées,
jamais complétées à la main."""
import csv
import json
import re
import duckdb
from h_lib import DATA, DMAGA_BIG, EXT, T_CREATE, W7GVC, W9SXM, sol_usd, utc

B = str(DMAGA_BIG).replace("/data", "/data_v2")
LEDGER = DATA / "ledger_7GVC_20240713_20240725.csv"
ABBR = {"A1UD…vQ8J": ("A1UD", "vQ8J", 5), "6QFD…5jqD": ("6QFD", "5jqD", 60), "H4mQ…JU5y": ("H4mQ", "JU5y", 16)}
POST_T, PRICE_AT_POST = 1721634134, 0.0547  # heure du post ; cours cité par Jeffro « à l'édition »


def ledger():
    return list(csv.DictReader(LEDGER.open()))


def sol_moves(rows, src=None, dst=None):
    for r in rows:
        for m in filter(None, r["movements"].split(" | ")):
            path, kind, sd, amt, mint = m.split(":")
            s, d = sd.split(">")
            if kind == "sol" and (src is None or s == src) and (dst is None or d == dst):
                yield r, s, d, int(amt)


def main():
    L = ledger()
    con = duckdb.connect()
    T = lambda q: con.execute(q.replace("{B}", B)).fetchall()
    out, receipts = [], {}

    def claim(cid, text, verdict, observed, sigs, alt):
        out.append({"id": cid, "jeffro_claim": text, "verdict": verdict, "observed": observed, "signatures": ";".join(sigs), "alternatives": alt})
        for s in sigs:
            receipts[s] = f"Jeffro {cid}"

    # C1 : 190 SOL de Jupiter Perpetuals une demi-heure avant l'ouverture
    perps = [r for r in L if "jupiter_perps" in r["programs"] and int(r["block_time"]) < T_CREATE]
    credit = max((r for r in perps if int(r["sol_delta_lamports"]) > 10**9), key=lambda r: int(r["block_time"]))  # dernier crédit Perps avant la création
    own_req = [r for r in perps if r["wallet_signed"] == "True" and int(credit["block_time"]) - 3600 < int(r["block_time"]) < int(credit["block_time"])]
    claim("C1", "7GVC reçoit 190 SOL de Jupiter Perpetuals environ 30 min avant l'ouverture sur Pump.fun",
          "CONFIRMÉ, source requalifiée",
          f"{int(credit['sol_delta_lamports']) / 1e9:.9f} SOL crédités le {credit['utc']} UTC (slot {credit['slot']}), {(T_CREATE - int(credit['block_time'])) // 60} min {(T_CREATE - int(credit['block_time'])) % 60} s avant la création du mint ; "
          f"exécution DecreasePosition3 par le keeper {credit['signers']} ; demandes de clôture signées par 7GVC elle-même ({', '.join(r['utc'][11:] for r in own_req)}). "
          "C'est la clôture de la propre position de 7GVC, pas un virement d'un tiers",
          [credit["signature"]] + [r["signature"] for r in own_req],
          "Le programme Perpetuals de Jupiter rend le collatéral et le gain d'une position : il ne désigne aucun financeur personnel")
    # C2 : achat de 41,2 M à 0,00002721 $
    buys = T(f"select signature, slot, block_time, token_delta, sol_lamports from '{{B}}/trades.parquet' where owner='{W7GVC}' and venue='pumpfun' and kind='swap' and token_delta>0 order by slot, tx_index")
    q = sum(b[3] for b in buys) / 1e6
    usd = sum(-b[4] / 1e9 * sol_usd(b[2]) for b in buys)
    claim("C2", "7GVC achète 41,2 M DMAGA sur Pump.fun au prix moyen de 0,00002721 $", "CONFIRMÉ",
          f"{len(buys)} achats ({', '.join(utc(b[2])[11:] for b in buys)} UTC le 14/07) : {q:,.6f} DMAGA pour {sum(-b[4] for b in buys) / 1e9:.9f} SOL, "
          f"soit {usd / q:.8f} $ par jeton au cours SOLUSDT de chaque minute (écart à 0,00002721 : {100 * (usd / q / 0.00002721 - 1):+.1f} %)",
          [b[0] for b in buys], "Prix en $ sensible à la source du cours SOL ; le SOL compté inclut les frais")
    # C3 : 20 M vers 9Sxm deux minutes plus tard
    tr = T(f"select signature, slot, block_time, qty from '{{B}}/token_edges.parquet' where src='{W7GVC}' and dst='{W9SXM}' and block_time<{T_CREATE + 3600}")
    s, sl, bt, qty = tr[0]
    claim("C3", "2 minutes après l'achat, 20 M DMAGA passent à 9Sxm…HSQS", "CONFIRMÉ pour le montant, FAUX pour le délai",
          f"{qty:,.0f} DMAGA de 7GVC à 9Sxm le {utc(bt)} UTC (slot {sl}), instruction de virement signée par 7GVC ; "
          f"{(bt - buys[-1][2]) // 60} min {(bt - buys[-1][2]) % 60} s après le 2e achat, {(bt - buys[0][2]) // 60} min {(bt - buys[0][2]) % 60} s après le 1er",
          [s], "Un virement direct signé ne dit pas qui tient les clés de 9Sxm")
    # C4 : ventes simultanées vers 02:26
    sells = T(f"select owner, signature, block_time, token_delta, sol_lamports from '{{B}}/trades.parquet' where owner in ('{W7GVC}','{W9SXM}') and kind='swap' and token_delta<0 and block_time<{T_CREATE + 3600} order by slot, tx_index")
    by = {}
    for o, sg, t, d, sol in sells:
        by.setdefault(o, []).append((sg, t, d, sol))
    txt = "; ".join(f"{o[:4]} : {len(v)} ventes de {utc(v[0][1])[11:]} à {utc(v[-1][1])[11:]}, {-sum(x[2] for x in v) / 1e6:,.0f} DMAGA pour {sum(x[3] for x in v) / 1e9:.3f} SOL" for o, v in by.items())
    claim("C4", "Vers 02:26 le 14/07, les deux adresses vendent en même temps (la mèche du graphique)", "PARTIEL", txt + " ; pas simultané",
          [x[0] for v in by.values() for x in v], "Plusieurs gros vendeurs précoces existent ; l'attribution de la mèche à ces seuls deux wallets n'est pas testée ici")
    # C5 : satellites
    cps = {(s, d) for _, s, d, _ in sol_moves(L, src=W7GVC)} | {(s, d) for _, s, d, _ in sol_moves(L, src=W9SXM)}
    sat_rows = []
    for ab, (pre, suf, amount) in ABBR.items():
        cand = sorted({d for s, d in cps if d.startswith(pre) and d.endswith(suf)})
        assert len(cand) == 1, (ab, cand)  # résolution unique parmi les destinations observées, sinon arrêt
        a = cand[0]
        fund = [(r, s, amt) for r, s, d, amt in sol_moves(L, dst=a) if s in (W7GVC, W9SXM)]
        got = sum(x[2] for x in fund) / 1e9
        sb = T(f"select signature, block_time, token_delta, sol_lamports from '{{B}}/trades.parquet' where owner='{a}' and kind='swap' and block_time<{POST_T} order by slot, tx_index")
        bq = sum(x[2] for x in sb if x[2] > 0) / 1e6
        bus = sum(-x[3] / 1e9 * sol_usd(x[1]) for x in sb if x[2] > 0)
        sold = -sum(x[2] for x in sb if x[2] < 0) / 1e6
        bal = T(f"select coalesce(sum(token_delta),0)/1e6 from '{{B}}/trades.parquet' where owner='{a}' and block_time<={POST_T}")[0][0]
        lag = min(x[1] for x in sb if x[2] > 0) - int(fund[0][0]["block_time"])
        sat_rows.append({"abbr": ab, "address": a, "jeffro_sol": amount, "sol_received_from_7GVC_9Sxm": round(got, 9),
                         "funding_utc": ";".join(r["utc"] for r, _, _ in fund), "funding_signatures": ";".join(r["signature"] for r, _, _ in fund),
                         "funder": ";".join(sorted({s for _, s, _ in fund})), "first_buy_lag_s": lag, "dmaga_bought": round(bq, 6),
                         "avg_buy_usd": round(bus / bq, 8), "dmaga_sold_on_venues_before_post": round(sold, 6), "balance_at_post": round(bal, 6),
                         "value_at_0_0547_usd": round(bal * PRICE_AT_POST), "buy_signatures": ";".join(x[0] for x in sb if x[2] > 0)})
        for r, _, _ in fund:
            receipts[r["signature"]] = f"Jeffro C5 financement {ab}"
        receipts[sb[0][0]] = f"Jeffro C5 premier achat {ab}"
    claim("C5", "Distribution de SOL : 5 SOL à A1UD…vQ8J, 60 SOL à 6QFD…5jqD, 16 SOL à H4mQ…JU5y, qui achètent ensuite", "CONFIRMÉ",
          "; ".join(f"{r['abbr']} = {r['address']} : {r['sol_received_from_7GVC_9Sxm']} SOL de {r['funder'][:4]} ({r['funding_utc']}), 1er achat {r['first_buy_lag_s']} s après, "
                    f"{r['dmaga_bought']:,.0f} DMAGA à {r['avg_buy_usd']:.6f} $" for r in sat_rows),
          [], "Résolution par préfixe et suffixe parmi les seules destinations SOL de 7GVC et 9Sxm dans la fenêtre : une seule adresse par abréviation")
    claim("C6", "Gains d'environ 66万, 83万 et 20万 $ (×1012, ×97, ×80)", "REQUALIFIÉ : valorisation, pas gain réalisé",
          "; ".join(f"{r['abbr']} : solde {r['balance_at_post']:,.0f} DMAGA à l'heure du post, {r['dmaga_sold_on_venues_before_post']:,.0f} vendus sur un pool, valeur au cours cité {r['value_at_0_0547_usd']:,} $" for r in sat_rows),
          [], "Les multiples de Jeffro rapportent un cours à un prix d'achat ; aucune vente sur pool avant son post")
    claim("C7", "Les wallets liés avaient une relation avec le token « sombre » KLLARY deux semaines plus tôt", "NON TESTÉ ICI",
          "voir FINDINGS §6 : le test dépend d'un mint KLLARY authentifié", [], "Ticker commun à plusieurs contrats")
    with (DATA / "jeffro_claims.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(out[0]))
        w.writeheader()
        w.writerows(out)
    with (DATA / "jeffro_satellites.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(sat_rows[0]))
        w.writeheader()
        w.writerows(sat_rows)
    (DATA / "receipts_jeffro.json").write_text(json.dumps(receipts, indent=1, ensure_ascii=False))
    for r in out:
        print(r["id"], r["verdict"], "|", r["observed"][:400])


if __name__ == "__main__":
    main()
