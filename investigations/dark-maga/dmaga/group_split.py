"""Calcul local des achats dans la fenêtre documentaire du changement d'avatar."""


def window_purchases(con, events):
    """Découper la fenêtre en deux intervalles [début, fin), sans chevauchement.

    Les transactions à la borne haute appartiennent aux fenêtres postérieures
    d'ana_50, pas aux achats précédant la première capture du nouvel avatar.
    Les filtres de population restent ceux de l'analyse des sous-groupes.
    """
    bounds = (
        ("borne_basse_a_envoi", events["musk_borne_basse"], events["musk_envoi_image"]),
        ("envoi_a_borne_haute", events["musk_envoi_image"], events["musk_borne_haute"]),
    )
    return {
        name: con.execute(
            """SELECT coalesce(sum(-sol_lamports), 0)/1e9, count(DISTINCT owner)
               FROM trades
               WHERE kind='swap' AND token_delta>0
                 AND block_time>=? AND block_time<?""",
            [start, end],
        ).fetchone()
        for name, start, end in bounds
    }
