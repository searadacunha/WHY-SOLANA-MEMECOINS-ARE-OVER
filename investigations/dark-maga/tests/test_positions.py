"""Règle de dmaga.positions (issue #27) : un virement d'une transaction absente de trades ajoute ses deux jambes ; une arête d'une
transaction déjà dans trades (jambe de swap, de passage par un routeur) n'ajoute rien ; rien après l'instant demandé."""
import tempfile
import unittest
from pathlib import Path

import duckdb

from dmaga.positions import gtba_only_transfers_sql, positions


class Positions(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.con = duckdb.connect()
        self.con.execute("CREATE TABLE trades(signature VARCHAR, owner VARCHAR, kind VARCHAR, token_delta BIGINT, block_time BIGINT)")
        self.con.executemany("INSERT INTO trades VALUES (?,?,?,?,?)", [
            ("buy", "A", "swap", 10_000_000, 100),        # A achète 10 jetons
            ("sw2", "C", "swap", 4_000_000, 150),         # C achète via une réserve non listée : arête gtba à une jambe
            ("late", "A", "swap", 1_000_000, 900),        # après l'instant
            ("route", "D", "swap", 8_000_000, 160),       # D achète via un routeur (forme de YQMWMCwa…, 11/2025)
        ])
        self.edges = Path(self.tmp.name) / "token_edges.parquet"
        self.con.execute(f"""COPY (SELECT * FROM (VALUES
            ('plain', 1, 'A', 'B', 6.0, 120, 'gtba'),          -- Transfer sans mint : transaction absente de trades
            ('sw2', 2, 'POOL', 'C', 4.0, 150, 'gtba'),         -- jambe de swap : C déjà dans trades
            ('after', 3, 'A', 'B', 1.0, 950, 'gtba'),          -- après l'instant
            ('multi', 4, 'A', '(multiple)', 1.0, 130, 'gtba'), -- sans destinataire unique : ignoré
            ('route', 5, 'POOL', 'ROUTER', 8.0, 160, 'gtba'),  -- jambe de passage : aucune jambe dans trades, mais transaction lue
            ('route', 5, 'ROUTER', 'D', 8.0, 160, 'gtba')      -- D déjà dans trades
            ) t(signature, slot, src, dst, qty, block_time, how)) TO '{self.edges}' (FORMAT parquet)""")

    def tearDown(self):
        self.tmp.cleanup()

    def test_rule(self):
        p = positions(self.con, 500, str(self.edges))
        self.assertEqual(p.get("A"), 4_000_000)
        self.assertEqual(p.get("B"), 6_000_000)
        self.assertEqual(p.get("C"), 4_000_000)
        self.assertNotIn("POOL", p)
        # transaction déjà lue : le routeur ne reçoit aucun solde fantôme, l'acheteur n'est pas compté deux fois
        self.assertNotIn("ROUTER", p)
        self.assertEqual(p.get("D"), 8_000_000)

    def test_gtba_netting_stays_inside_each_transaction(self):
        edges = Path(self.tmp.name) / "netted.parquet"
        self.con.execute(f"""COPY (SELECT * FROM (VALUES
            ('pass', 1, 'A', 'R', 6.0, 120, 'gtba'),
            ('pass', 1, 'R', 'B', 6.0, 120, 'gtba'),
            ('self', 2, 'A', 'A', 4.0, 125, 'gtba'),
            ('one', 3, 'A', 'R', 2.0, 130, 'gtba'),
            ('two', 4, 'R', 'B', 2.0, 140, 'gtba'),
            ('buy', 5, 'A', 'B', 2.0, 150, 'gtba'),
            ('after_cut', 6, 'A', 'B', 1.0, 500, 'gtba')
            ) t(signature, slot, src, dst, qty, block_time, how)) TO '{edges}' (FORMAT parquet)""")
        query = gtba_only_transfers_sql(str(edges), 500)
        rows = self.con.execute(f"SELECT signature, owner, token_delta FROM ({query}) ORDER BY signature, owner").fetchall()
        self.assertEqual(rows, [
            ("one", "A", -2_000_000), ("one", "R", 2_000_000),
            ("pass", "A", -6_000_000), ("pass", "B", 6_000_000),
            ("two", "B", 2_000_000), ("two", "R", -2_000_000),
        ])
        p = positions(self.con, 500, str(edges))
        self.assertEqual(p["A"], 2_000_000)
        self.assertEqual(p["B"], 8_000_000)
        self.assertEqual(p["R"], 0)


if __name__ == "__main__":
    unittest.main()
