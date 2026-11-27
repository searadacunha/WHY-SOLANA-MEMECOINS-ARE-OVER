"""Solde DMAGA de chaque propriétaire avant un instant : trades, plus les virements que seule l'API de transferts a vus.

Règle unique, la même que ana_20_pnl : une arête `gtba` de token_edges dont AUCUNE jambe n'est dans trades (virement SPL
`Transfer` sans compte du mint, issue #27) ajoute ses deux jambes. Une arête dont une jambe est déjà dans trades est une jambe
de swap ou de frais avec une réserve de pool (contrôlé par scripts/chk_22_transfer_coverage.py) : rien n'est ajouté.
Les virements entre deux wallets non suivis restent invisibles : ce solde n'est exact que pour les wallets suivis."""

KINDS = ("swap", "transfer", "fee_share", "swap_other", "lp_add", "lp_remove")


def gtba_only_edges_sql(edges_path: str, t_cut: int) -> str:
    """Arêtes gtba sans aucune jambe dans trades, avant t_cut, quantité en unités brutes."""
    return f"""SELECT e.signature, e.src, e.dst, CAST(round(e.qty * 1e6) AS BIGINT) q FROM read_parquet('{edges_path}') e
               WHERE e.how = 'gtba' AND e.dst <> '(multiple)' AND e.block_time < {t_cut}
               AND NOT EXISTS (SELECT 1 FROM trades t WHERE t.signature = e.signature AND (t.owner = e.src OR t.owner = e.dst))"""


def positions(con, t_cut: int, edges_path: str) -> dict[str, int]:
    """{propriétaire: solde brut} juste avant t_cut."""
    x = gtba_only_edges_sql(edges_path, t_cut)
    return dict(con.execute(f"""
        WITH x AS ({x})
        SELECT owner, sum(d) FROM (
            SELECT owner, token_delta d FROM trades WHERE block_time < {t_cut} AND kind IN {KINDS} AND owner IS NOT NULL
            UNION ALL SELECT src, -q FROM x
            UNION ALL SELECT dst, q FROM x) GROUP BY 1""").fetchall())
