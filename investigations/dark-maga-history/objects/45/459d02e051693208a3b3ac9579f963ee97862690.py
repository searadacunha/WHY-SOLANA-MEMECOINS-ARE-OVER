#!/usr/bin/env python3
"""Couverture des virements DMAGA : chaque arête de token_edges confrontée à trades.parquet (issue #27). Hors ligne.

1. Arêtes `gtba` (API de transferts) classées selon les jambes présentes dans trades : aucune, source seule, destination seule,
   les deux ; et selon la nature des deux bouts (venue de dmaga/venues.py et autorités, puis `kind` de nodes.parquet).
   Attendu : une arête sans jambe dans trades est un virement `Transfer` hors historique du mint, ajouté par ana_20 et
   dmaga.positions ; une arête à une seule jambe est une jambe de swap ou de frais, déjà comptée par la ligne swap du wallet.
   Toute arête à une jambe dont la jambe présente n'est pas un swap, des frais ou un mouvement de liquidité est listée.
2. Doublons : même (signature, source, destination) vue à la fois par les soldes de transaction et par l'API.
3. Positions juste avant la borne basse (19:03:27) : ancienne règle de ana_61 (arêtes token_direct d'au moins 1 M seulement)
   contre dmaga.positions, pour tous les propriétaires et pour la composante de prevent_groups.json.
Sortie : reports/data_checks/transfer_coverage.json."""
import gzip
import json

from dmaga.config import BIG, DATA, RAW, ROOT
from dmaga.db import connect
from dmaga.positions import KINDS, gtba_only_edges_sql, positions
from dmaga.venues import load as load_venues

T_LOW = 1721588607
AUTH = {"5Q544fKrFoe6tsEbD7S8EmxGTJYAKtTVhAW5Q5pge4j1", "87g44hEXP7R8ZxoAJtz941tsVftpEXC1LqAFTf2ZHtkH",
        "39azUYFWPz3VHgKCf3VChUwbpURdCHRxjWVowf5jUJjg", "PNLCQcVCD26aC7ZWgRyr5ptfaR7bBrWdTFgRWwu2tvF"}


def flows_coverage():
    """Historiques DMAGA par wallet (getTransfersByAddress, plafond de 60 pages) : combien sont tronqués."""
    n = trunc = 0
    names = []
    for d in sorted((RAW / "flows").iterdir()):
        f = d / "dmaga_all.json.gz"
        if d.name.startswith("._") or not f.exists():
            continue
        n += 1
        if json.loads(gzip.decompress(f.read_bytes())).get("truncated"):
            trunc += 1
            names.append(d.name)
    return {"wallets": n, "tronques": trunc, "wallets_tronques": names}


def main():
    con = connect(mem="500MB", threads=1)
    E = str(BIG / "token_edges.parquet")
    con.execute("CREATE TEMP TABLE v(a VARCHAR)")
    con.executemany("INSERT INTO v VALUES (?)", [[a] for a in set(load_venues()) | AUTH])
    con.execute(f"CREATE TEMP TABLE nd AS SELECT address, kind FROM read_parquet('{BIG}/nodes.parquet')")
    con.execute("CREATE TEMP TABLE tl AS SELECT signature, owner, string_agg(DISTINCT kind, '+' ORDER BY kind) kinds FROM trades WHERE owner IS NOT NULL GROUP BY 1, 2")
    con.execute(f"""CREATE TEMP TABLE g AS SELECT e.signature, e.src, e.dst, e.qty, e.block_time,
        s.kinds sk, d.kinds dk,
        CASE WHEN e.src IN (SELECT a FROM v) THEN 'venue' ELSE coalesce((SELECT kind FROM nd WHERE address=e.src), 'inconnu') END sc,
        CASE WHEN e.dst IN (SELECT a FROM v) THEN 'venue' ELSE coalesce((SELECT kind FROM nd WHERE address=e.dst), 'inconnu') END dc
        FROM read_parquet('{E}') e LEFT JOIN tl s ON s.signature=e.signature AND s.owner=e.src LEFT JOIN tl d ON d.signature=e.signature AND d.owner=e.dst
        WHERE e.how='gtba' AND e.dst<>'(multiple)'""")
    legs = "CASE WHEN sk IS NULL AND dk IS NULL THEN 'aucune' WHEN dk IS NULL THEN 'source seule' WHEN sk IS NULL THEN 'destination seule' ELSE 'les deux' END"
    by_legs = [dict(zip(("jambes_dans_trades", "aretes", "jetons_M"), r)) for r in con.execute(
        f"SELECT {legs} l, count(*), round(sum(qty)/1e6, 3) FROM g GROUP BY 1 ORDER BY 2 DESC").fetchall()]
    by_class = [dict(zip(("jambes_dans_trades", "bouts", "aretes", "jetons_M"), r)) for r in con.execute(
        f"SELECT {legs} l, sc||'/'||dc, count(*), round(sum(qty)/1e6, 3) FROM g GROUP BY 1, 2 ORDER BY 1, 3 DESC").fetchall()]
    present = f"CASE WHEN sk IS NULL THEN dk ELSE sk END"
    one_leg = [dict(zip(("nature_de_la_jambe_presente", "aretes", "jetons_M"), r)) for r in con.execute(
        f"SELECT {present}, count(*), round(sum(qty)/1e6, 3) FROM g WHERE (sk IS NULL) <> (dk IS NULL) GROUP BY 1 ORDER BY 2 DESC").fetchall()]
    suspect = con.execute(f"""SELECT signature, src, dst, qty, block_time, sk, dk FROM g WHERE (sk IS NULL) <> (dk IS NULL)
        AND NOT regexp_matches({present}, '(swap|fee_share|lp_add|lp_remove)') ORDER BY qty DESC""").fetchall()
    dup = con.execute(f"""SELECT count(*) FROM read_parquet('{E}') a JOIN read_parquet('{E}') b
        ON a.signature=b.signature AND a.src=b.src AND a.dst=b.dst AND a.how='tx_balances' AND b.how='gtba'""").fetchone()[0]
    n_how = dict(con.execute(f"SELECT how, count(*) FROM read_parquet('{E}') GROUP BY 1").fetchall())
    added = con.execute(f"SELECT count(*), round(sum(q)/1e12, 3) FROM ({gtba_only_edges_sql(E, 2**40)})").fetchone()
    # positions : ancienne règle (ana_61) contre la nouvelle
    old = dict(con.execute(f"SELECT owner, sum(token_delta) FROM trades WHERE block_time<{T_LOW} AND kind IN {KINDS} AND owner IS NOT NULL GROUP BY 1").fetchall())
    for a, b, q, s in con.execute(f"""SELECT src, dst, amount, signature FROM read_parquet('{BIG}/link_edges.parquet')
                                      WHERE type='token_direct' AND amount>=1000000 AND block_time<{T_LOW}""").fetchall():
        if not con.execute("SELECT 1 FROM trades WHERE signature=? AND owner=? LIMIT 1", [s, a]).fetchone():
            old[a] = old.get(a, 0) - round(q * 1e6)
            old[b] = old.get(b, 0) + round(q * 1e6)
    new = positions(con, T_LOW, E)
    owners = set(old) | set(new)
    diff = {o: new.get(o, 0) - old.get(o, 0) for o in owners if abs(new.get(o, 0) - old.get(o, 0)) >= 10**6}
    venues = {a for (a,) in con.execute("SELECT a FROM v").fetchall()}
    neg_old = sum(1 for o in owners if old.get(o, 0) < -10**6 and o not in venues)
    neg_new = sum(1 for o in owners if new.get(o, 0) < -10**6 and o not in venues)
    members = set(json.loads((DATA / "prevent_groups.json").read_text())[0]["members"])
    held = lambda p: round(sum(max(p.get(m, 0), 0) for m in members) / 1e12, 3)
    out = {
        "token_edges_par_source": n_how,
        "gtba_par_jambes": by_legs, "gtba_par_jambes_et_bouts": by_class,
        "une_jambe_nature_de_la_jambe_presente": one_leg,
        "une_jambe_hors_swap_frais_liquidite": {"n": len(suspect), "jetons_M": round(sum(r[3] for r in suspect) / 1e6, 3),
                                                "exemples": [dict(zip(("signature", "src", "dst", "qty", "t", "src_kinds", "dst_kinds"), r)) for r in suspect[:20]]},
        "doublons_tx_balances_et_gtba": dup,
        "aretes_ajoutees_par_ana20_et_positions": {"n": added[0], "jetons_M": added[1]},
        "positions_a_la_borne_basse": {
            "proprietaires_changes_de_plus_d_1_jeton": len(diff), "ecart_absolu_total_M": round(sum(abs(v) for v in diff.values()) / 1e12, 3),
            "soldes_negatifs_hors_venues_ancienne_regle": neg_old, "soldes_negatifs_hors_venues_nouvelle_regle": neg_new,
            "composante_prevent_groups": {"membres": len(members), "detenu_M_ancienne_regle": held(old), "detenu_M_nouvelle_regle": held(new)},
            "plus_grands_ecarts": [{"owner": o, "ecart_M": round(v / 1e12, 6), "ancien_M": round(old.get(o, 0) / 1e12, 6), "nouveau_M": round(new.get(o, 0) / 1e12, 6),
                                    "membre": o in members} for o, v in sorted(diff.items(), key=lambda x: -abs(x[1]))[:25]]},
        "garantie_une_jambe": ("dmaga/normalize.py écrit une ligne pour chaque propriétaire hors venue dont le solde net DMAGA change dans une "
                               "transaction lue : une arête à une seule jambe a donc pour autre bout une venue ou un intermédiaire à solde net nul"),
        "historiques_suivis": flows_coverage(),
        "limite": "les virements entre deux wallets non suivis, ou au-delà du plafond de pages d'un historique, ne sont vus ni par trades ni par token_edges",
    }
    p = ROOT / "reports" / "data_checks" / "transfer_coverage.json"
    p.write_text(json.dumps(out, indent=1, ensure_ascii=False))
    print(json.dumps({k: out[k] for k in ("gtba_par_jambes", "une_jambe_nature_de_la_jambe_presente", "doublons_tx_balances_et_gtba",
                                          "aretes_ajoutees_par_ana20_et_positions")}, ensure_ascii=False))
    print(json.dumps({k: v for k, v in out["positions_a_la_borne_basse"].items() if k != "plus_grands_ecarts"}, ensure_ascii=False))
    print("une jambe hors swap/frais/liquidité :", out["une_jambe_hors_swap_frais_liquidite"]["n"])


if __name__ == "__main__":
    main()
