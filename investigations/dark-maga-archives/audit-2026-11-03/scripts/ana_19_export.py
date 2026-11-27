#!/usr/bin/env python3
"""Matérialise data/trades.parquet : une version de chaque transaction (pool ou courbe avant mint), sans ligne doublée, triée (slot, index)."""
import os
import tempfile
from pathlib import Path

from dmaga.db import connect
from dmaga.paths import BIG, exige_v2


def main():
    exige_v2()
    con = connect(mem="700MB", use_materialized=False)
    tmp = None
    try:
        # Même volume que la sortie, nom propre à ce calcul : les sessions ne partagent pas leur fichier temporaire.
        fd, name = tempfile.mkstemp(prefix=".trades-", suffix=".parquet", dir=BIG)
        os.close(fd)
        tmp = Path(name)
        con.execute("COPY (SELECT * FROM trades ORDER BY slot, tx_index) TO ? (FORMAT parquet, COMPRESSION zstd)", [str(tmp)])
        counts = con.execute("SELECT count(*), count(DISTINCT signature) FROM read_parquet(?)", [str(tmp)]).fetchone()
        # Garder l'ancienne table jusqu'à ce que le nouveau fichier soit entièrement écrit et relu.
        tmp.replace(BIG / "trades.parquet")
        print(counts)
    finally:
        try:
            if tmp is not None:
                tmp.unlink(missing_ok=True)
        finally:
            con.close()


if __name__ == "__main__":
    main()
