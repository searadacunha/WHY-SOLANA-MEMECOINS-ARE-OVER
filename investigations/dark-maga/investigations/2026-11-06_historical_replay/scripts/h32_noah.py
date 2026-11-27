"""Rejeu des quatre groupes publiés par @Noah_nftn (post 1815372294426124565, 22/07/2024 13:04:17 UTC).

1. Avoirs DMAGA de chaque adresse à l'heure du post (somme des deltas de trades.parquet, toutes natures), comparés à ses
   chiffres : 6,73 % au plus par entité, 20,39 % pour les dix premiers et leurs liés.
2. Arêtes directes à l'intérieur de chaque groupe (virements DMAGA et SOL), avec signature, heure et montant.
3. Contreparties partagées ENTRE groupes, classées : service (plus de 25 wallets DMAGA, ou étiquette d'exchange, de routeur
   ou de pool), poussière (moins de 0,01 SOL par virement), ou candidate à relire. Une candidate n'est pas un lien.
Sorties : data/noah_holdings.csv, data/noah_edges.csv, data/noah_cross_group.csv."""
import csv
import duckdb
from h_lib import DATA, DMAGA_BIG, NOAH, utc

B = str(DMAGA_BIG).replace("/data", "/data_v2")
T_NOAH = 1721653457
SUPPLY = 1_000_000_000
SAT = {"A1UDMqcUC8RkZ8YENAktdueSQ6jxUUBickBK2y61vQ8J": "4+J", "6QFDe4yu9mVhv3cbbaMtkTnakz4bGJLAjLjhwrMn5jqD": "4+J",
       "H4mQu98TuxYTn3VSJone6jCTiDfXpuKcZbNZGHKUJU5y": "4+J"}  # satellites de Jeffro, financés par 7GVC (h31)
HUB = 25


def main():
    grp = {a: str(g) for g, l in NOAH.items() for a in l} | SAT
    q = ",".join(f"'{a}'" for a in grp)
    con = duckdb.connect()
    con.execute(f"create table e as select wallet w, src cp, 'in' dir, sol amt, 'SOL' asset, block_time t, signature sig, src_label lab from '{B}/funding_edges.parquet' "
                f"union all select wallet, dst, 'out', amount, asset, block_time, signature, dst_label from '{B}/exit_flows.parquet'")
    con.execute("create table deg as select cp, count(distinct w) nw from e group by 1")
    # 1. avoirs
    bal = dict(con.execute(f"select owner, sum(token_delta) from '{B}/trades.parquet' where block_time<={T_NOAH} and owner in ({q}) group by 1").fetchall())
    hold, tot = [], {}
    for a, g in grp.items():
        b = (bal.get(a) or 0) / 1e6
        tot[g] = tot.get(g, 0) + b
        hold.append({"group": g, "address": a, "dmaga_at_post": round(b, 6), "pct_supply": round(100 * b / SUPPLY, 4)})
    for g, b in tot.items():
        hold.append({"group": g, "address": "TOTAL", "dmaga_at_post": round(b, 6), "pct_supply": round(100 * b / SUPPLY, 4)})
    with (DATA / "noah_holdings.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(hold[0]))
        w.writeheader()
        w.writerows(hold)
    # 2. arêtes internes et inter-groupes directes
    edges = con.execute(f"""select src, dst, 'DMAGA' asset, qty, block_time, signature, how from '{B}/token_edges.parquet' where src in ({q}) and dst in ({q}) and qty>=1
        union all select src, dst, asset, amount, block_time, signature, type from '{B}/link_edges.parquet' where src in ({q}) and dst in ({q}) and asset<>'DMAGA'
        union all select src, wallet, 'SOL', sol, block_time, signature, 'funding' from '{B}/funding_edges.parquet' where src in ({q}) and wallet in ({q})
        union all select wallet, dst, asset, amount, block_time, signature, 'exit' from '{B}/exit_flows.parquet' where wallet in ({q}) and dst in ({q})""").fetchall()
    seen, rows = set(), []
    for s, d, asset, amt, t, sig, how in sorted(edges, key=lambda x: x[4]):
        if (sig, s, d, asset) in seen:
            continue
        seen.add((sig, s, d, asset))
        rows.append({"utc": utc(t), "src_group": grp[s], "src": s, "dst_group": grp[d], "dst": d, "asset": asset, "amount": amt,
                     "signature": sig, "source_table": how, "same_group": grp[s][0] == grp[d][0]})
    with (DATA / "noah_edges.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    # 3. contreparties partagées entre groupes
    cps = con.execute(f"""select e.cp, d.nw, list(distinct e.w), count(*), sum(case when asset='SOL' then amt end), max(case when asset='SOL' then amt end),
        min(t), max(t), any_value(lab), list(distinct asset), list(distinct dir) from e join deg d using(cp) where e.w in ({q}) and e.cp not in ({q}) group by e.cp, d.nw""").fetchall()
    cross = []
    for cp, nw, ws, n, sol, mx, t0, t1, lab, assets, dirs in cps:
        gs = sorted({grp[w][0] for w in ws})
        if len(gs) < 2:
            continue
        cls = ("service" if (nw > HUB or (lab and lab not in ("None",))) else "poussière" if (mx is not None and mx < 0.01 and assets == ["SOL"]) else "candidate")
        cross.append({"counterparty": cp, "groups": "+".join(gs), "wallets": ";".join(sorted(f"{grp[w]}:{w}" for w in ws)), "dmaga_wallets_touched": nw,
                      "n_transfers": n, "sol_total": round(sol or 0, 6), "max_sol": round(mx or 0, 6), "assets": ";".join(assets), "dirs": ";".join(dirs),
                      "first_utc": utc(t0), "last_utc": utc(t1), "label": lab or "", "class": cls})
    cross.sort(key=lambda r: (r["class"], -r["dmaga_wallets_touched"]))
    with (DATA / "noah_cross_group.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(cross[0]))
        w.writeheader()
        w.writerows(cross)
    print({g: round(100 * b / SUPPLY, 3) for g, b in tot.items()})
    print("arêtes", len(rows), "dont inter-groupes", sum(1 for r in rows if not r["same_group"]))
    print("contreparties partagées", len(cross), {c: sum(1 for r in cross if r["class"] == c) for c in ("service", "poussière", "candidate")})
    for r in cross:
        if r["class"] == "candidate":
            print(" candidate", r["counterparty"], r["groups"], r["dmaga_wallets_touched"], r["sol_total"], r["assets"], r["dirs"], r["first_utc"])


if __name__ == "__main__":
    main()
