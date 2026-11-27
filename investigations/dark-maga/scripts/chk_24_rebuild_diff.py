#!/usr/bin/env python3
"""Avant/après de la reconstruction du 07/11/2026 (issue #27) : PnL, composantes, découpe du groupe, fichiers hérités.

Avant : sauvegarde des sorties dérivées (BIG/../data_backup_20261107) et version git `--before-ref` des petits fichiers de data/.
Après : fichiers courants. Les rapports que Helius ne permet plus de régénérer (rep_72, ana_65, chk_63) sont listés avec les valeurs
qu'ils afficheraient, recalculées ici depuis les nouvelles tables : aucun chiffre de Markdown n'est corrigé à la main.
usage: chk_24_rebuild_diff.py [--before-ref REF] [--before-dir NOM] [--out NOM.json]. Défauts : data_backup_20261107,
reports/data_checks/rebuild_20261107.json."""
import json
import subprocess
import sys

from dmaga.config import BIG, DATA, ROOT
from dmaga.db import connect


def git_json(ref, path):
    return json.loads(subprocess.run(["git", "-C", str(ROOT), "show", f"{ref}:{path}"], capture_output=True, text=True, check=True).stdout)


def component_row(c):
    return {"wallets": c["n"], "aretes": c["edges"], "detenu_avant_musk_M": round(c["held_before_musk_M"], 1), "achete_M": round(c["bought_M"], 1),
            "sol_engage": round(c["bought_sol"], 1), "realise_sol": round(c["realized_sol"]), "flux_net_sol": round(c["net_sol"]),
            "pnl_usd": round(c["proceeds_usd"] - c["cost_usd"])}


def leaves(a, b, path=""):
    if isinstance(a, dict) and isinstance(b, dict):
        for k in sorted(set(a) | set(b)):
            if k != "source":
                yield from leaves(a.get(k), b.get(k), f"{path}/{k}")
    elif a != b and not (isinstance(a, list) and isinstance(b, list) and len(a) > 40):
        yield {"chemin": path, "avant": a, "apres": b}


def main():
    arg = lambda k, d: sys.argv[sys.argv.index(k) + 1] if k in sys.argv else d
    ref = arg("--before-ref", "HEAD")
    before = BIG.parent / arg("--before-dir", "data_backup_20261107")
    con = connect(mem="400MB", threads=1)
    old_w, new_w = f"read_parquet('{before / 'wallets.parquet'}')", f"read_parquet('{BIG / 'wallets.parquet'}')"
    tot = lambda w: dict(zip(("wallets", "realise_sol", "achete_sol", "vendu_sol", "residuel_M", "achats", "ventes", "virements"),
                             con.execute(f"SELECT count(*), round(sum(realized_sol),3), round(sum(bought_sol),3), round(sum(sold_sol),3), round(sum(residual_qty)/1e6,3), "
                                         f"sum(n_buys), sum(n_sells), sum(n_transfers) FROM {w}").fetchone()))
    ch = con.execute(f"""SELECT a.owner, round(a.realized_sol,3), round(b.realized_sol,3), a.n_sells, b.n_sells FROM {old_w} a JOIN {new_w} b USING (owner)
                         WHERE abs(b.realized_sol - a.realized_sol) > 0.01 ORDER BY abs(b.realized_sol - a.realized_sol) DESC""").fetchall()
    res = con.execute(f"""SELECT coalesce(a.owner, b.owner), round(coalesce(a.residual_qty, 0)/1e6, 6), round(coalesce(b.residual_qty, 0)/1e6, 6)
                          FROM {old_w} a FULL JOIN {new_w} b USING (owner) WHERE abs(coalesce(b.residual_qty, 0) - coalesce(a.residual_qty, 0)) >= 1
                          ORDER BY abs(coalesce(b.residual_qty, 0) - coalesce(a.residual_qty, 0)) DESC""").fetchall()
    stats = {k: json.loads((p / "trades_stats.json").read_text()) for k, p in (("apres", BIG),)}
    n_dup_old = con.execute(f"""SELECT count(*) FROM (SELECT 1 FROM read_parquet('{before / 'trades.parquet'}')
                                GROUP BY signature, kind, owner, venue, token_delta HAVING count(*) > 1)""").fetchone()[0]
    rows = lambda p: con.execute(f"SELECT count(*) FROM read_parquet('{p}')").fetchone()[0]
    old_pg, new_pg = git_json(ref, "data/prevent_groups.json"), json.loads((DATA / "prevent_groups.json").read_text())
    old_gs, new_gs = git_json(ref, "data/group_split.json"), json.loads((DATA / "group_split.json").read_text())
    out = {
        "avant_ref_git": subprocess.run(["git", "-C", str(ROOT), "rev-parse", ref], capture_output=True, text=True).stdout.strip(),
        "trades_parquet": {"lignes_avant": rows(before / "trades.parquet"), "cles_en_double_avant": n_dup_old,
                           "lignes_apres": rows(BIG / "trades.parquet")},
        "pnl_totaux": {"avant": tot(old_w), "apres": tot(new_w)},
        "pnl_wallets_changes_plus_de_0_01_sol": len(ch),
        "pnl_plus_grands_ecarts": [dict(zip(("owner", "realise_avant", "realise_apres", "ventes_avant", "ventes_apres"), r)) for r in ch[:15]],
        "residuel_wallets_changes_d_au_moins_1_jeton": len(res),
        "residuel_plus_grands_ecarts_M": [dict(zip(("owner", "avant", "apres"), r)) for r in res[:15]],
        "composantes_coordination": {"membres_identiques": all(set(a["members"]) == set(b["members"]) for a, b in zip(old_pg, new_pg)) and len(old_pg) == len(new_pg),
                                     "avant": [component_row(c) for c in old_pg[:6]], "apres": [component_row(c) for c in new_pg[:6]]},
        "group_split_changements": list(leaves(old_gs, new_gs)),
        "heritage_non_regenere": {
            "reports/COORDINATION.md et reports/ATTRIBUTION.md (rep_72)": "lectures Helius getTransfersByAddress ; tableau des composantes : voir composantes_coordination.apres ; ventes du marché en 24 h : group_split_changements",
            "data/collector.json (ana_65)": "lectures Helius de 9W9b3zg ; le réalisé des expéditeurs vient de l'ancien wallets.parquet",
            "reports/data_checks/group_edges_check.json (chk_63)": "relecture Helius des 40 arêtes ; membres et arêtes inchangés, contrôle toujours valable"},
        "trades_stats_apres": stats["apres"],
    }
    p = ROOT / "reports" / "data_checks" / arg("--out", "rebuild_20261107.json")
    p.write_text(json.dumps(out, indent=1, ensure_ascii=False))
    print(json.dumps({k: out[k] for k in ("trades_parquet", "pnl_totaux", "pnl_wallets_changes_plus_de_0_01_sol")}, ensure_ascii=False))
    print(out["composantes_coordination"]["avant"][0], "->", out["composantes_coordination"]["apres"][0])
    print(len(out["group_split_changements"]), "changements dans group_split.json")


if __name__ == "__main__":
    main()
