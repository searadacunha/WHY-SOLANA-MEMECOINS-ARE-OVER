"""Connexion DuckDB bornée : mémoire limitée, débordement sur le disque USB, base en mémoire."""
import os
import time

import duckdb

from .config import BIG, TMP


def connect(mem="900MB", threads=2):  # plafond bas : sur cette machine, la mémoire devient du swap, donc du disque
    # toute date affichée doit être en UTC : la session héritait de Lisbonne (UTC+1 en juillet)
    os.environ["TZ"] = "UTC"
    time.tzset()
    TMP.mkdir(parents=True, exist_ok=True)
    con = duckdb.connect(":memory:", config={"memory_limit": mem, "threads": threads,
                                             "temp_directory": str(TMP / "duck"), "preserve_insertion_order": False})
    con.execute("SET TimeZone='UTC'")
    for view, sub in (("trades", "trades_shards"), ("vault", "vault_shards")):
        # FAT32 : macOS sème des fichiers ._ que le joker de DuckDB ramasserait
        files = sorted(str(p) for p in (BIG / sub).glob("*.parquet") if not p.name.startswith("._"))
        con.execute(f"CREATE VIEW {view}_all AS SELECT * FROM read_parquet({files!r})")
    final = BIG / "trades.parquet"
    if final.exists():  # table matérialisée par scripts/ana_19_export.py, l'anti-jointure coûte plusieurs minutes
        con.execute(f"""CREATE VIEW trades AS
            SELECT * EXCLUDE (_dedup_rank) FROM (
                SELECT *, row_number() OVER (
                    PARTITION BY signature, kind, owner, venue, token_delta
                    ORDER BY slot, tx_index, source
                ) AS _dedup_rank
                FROM read_parquet('{final}')
            ) WHERE _dedup_rank = 1""")
        con.execute("CREATE VIEW vault AS SELECT DISTINCT * FROM vault_all")
        return con
    # une transaction peut venir de plusieurs historiques : une seule version, tout le parseur voit la même chose
    con.execute("""CREATE VIEW trades AS
        WITH r AS (
            SELECT *, CASE source WHEN 'pool' THEN 0 WHEN 'curve' THEN 1 WHEN 'mint' THEN 2 ELSE 3 END pr
            FROM trades_all
        ), b AS (
            SELECT signature, min(pr) m FROM r GROUP BY signature
        ), preferred AS (
            SELECT r.* FROM r JOIN b ON r.signature = b.signature AND r.pr = b.m
        ), ranked AS (
            SELECT *, row_number() OVER (
                PARTITION BY signature, kind, owner, venue, token_delta
                ORDER BY slot, tx_index, source
            ) AS _dedup_rank FROM preferred
        )
        SELECT * EXCLUDE (pr, _dedup_rank) FROM ranked WHERE _dedup_rank = 1""")
    con.execute("CREATE VIEW vault AS SELECT DISTINCT * FROM vault_all")
    return con
