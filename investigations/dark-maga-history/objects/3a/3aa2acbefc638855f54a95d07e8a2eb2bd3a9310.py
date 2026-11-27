"""Règle de dmaga.positions (issue #27) : un virement vu seulement par l'API ajoute ses deux jambes ; une arête dont une jambe est
déjà dans trades (jambe de swap ou intermédiaire) n'ajoute rien ; rien après l'instant demandé."""
import tempfile
import unittest
from pathlib import Path

import duckdb

from dmaga.positions import positions


class Positions(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.con = duckdb.connect()
        self.con.execute("CREATE TABLE trades(signature VARCHAR, owner VARCHAR, kind VARCHAR, token_delta BIGINT, block_time BIGINT)")
        self.con.executemany("INSERT INTO trades VALUES (?,?,?,?,?)", [
            ("buy", "A", "swap", 10_000_000, 100),        # A achète 10 jetons
            ("sw2", "C", "swap", 4_000_000, 150),         # C achète via une réserve non listée : arête gtba à une jambe
            ("late", "A", "swap", 1_000_000, 900),        # après l'instant
        ])
        self.edges = Path(self.tmp.name) / "token_edges.parquet"
        self.con.execute(f"""COPY (SELECT * FROM (VALUES
            ('plain', 'A', 'B', 6.0, 120, 'gtba'),          -- Transfer sans mint : aucune jambe dans trades
            ('sw2', 'POOL', 'C', 4.0, 150, 'gtba'),         -- jambe de swap : C déjà dans trades
            ('after', 'A', 'B', 1.0, 950, 'gtba'),          -- après l'instant
            ('multi', 'A', '(multiple)', 1.0, 130, 'gtba')  -- sans destinataire unique : ignoré
            ) t(signature, src, dst, qty, block_time, how)) TO '{self.edges}' (FORMAT parquet)""")

    def tearDown(self):
        self.tmp.cleanup()

    def test_rule(self):
        p = positions(self.con, 500, str(self.edges))
        self.assertEqual(p.get("A"), 4_000_000)
        self.assertEqual(p.get("B"), 6_000_000)
        self.assertEqual(p.get("C"), 4_000_000)
        self.assertNotIn("POOL", p)


if __name__ == "__main__":
    unittest.main()
