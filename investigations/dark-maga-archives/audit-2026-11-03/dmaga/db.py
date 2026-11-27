"""Connexion DuckDB bornée : mémoire limitée, débordement sur le disque USB, base en mémoire."""
import os
import time

import duckdb

from .config import TMP
from .paths import BIG


def connect(mem="900MB", threads=2, *, use_materialized=True):  # plafond bas : la mémoire devient du swap, donc du disque
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
    if use_materialized and final.exists():  # l'export repart des shards sans supprimer la table encore valide
        con.execute(f"CREATE VIEW trades AS SELECT * FROM read_parquet('{final}')")
        con.execute("CREATE VIEW vault AS SELECT DISTINCT * FROM vault_all")
        return con
    # une transaction peut venir de plusieurs historiques, y compris de la même source (deux venues, deux tranches) : une seule version
    con.execute("""CREATE VIEW trades AS WITH r AS (SELECT *, CASE source WHEN 'pool' THEN 0 WHEN 'curve' THEN 1 WHEN 'mint' THEN 2 ELSE 3 END pr FROM trades_all),
                   b AS (SELECT signature, min(pr) m FROM r GROUP BY 1)
                   SELECT DISTINCT ON (r.signature, r.kind, r.owner, r.venue, r.token_delta) r.* EXCLUDE (pr)
                   FROM r JOIN b ON r.signature = b.signature AND r.pr = b.m""")
    con.execute("CREATE VIEW vault AS SELECT DISTINCT * FROM vault_all")
    return con
