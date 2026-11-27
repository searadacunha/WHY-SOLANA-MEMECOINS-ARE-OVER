"""Connexion DuckDB bornée : mémoire limitée, débordement sur le disque USB, base en mémoire."""
import os
import time

import duckdb

from .config import BIG, TMP


def connect(mem="2GB", threads=3):
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
    # une transaction du mint peut aussi toucher le pool : la version pool (ou courbe) fait foi
    con.execute("""CREATE VIEW trades AS SELECT * FROM trades_all WHERE source <> 'mint'
                   UNION ALL BY NAME SELECT * FROM trades_all t WHERE source = 'mint' AND NOT EXISTS
                   (SELECT 1 FROM trades_all p WHERE p.signature = t.signature AND p.source <> 'mint')""")
    con.execute("CREATE VIEW vault AS SELECT DISTINCT * FROM vault_all")
    return con
