"""Vecteurs relus dans les transactions brutes des courbes (797/797 comptes de jetons = ATA dérivée)."""
import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from k12_ata import ata, b58d, b58e, on_curve  # noqa: E402

KM = "HuAncxDEsakCDgZS2Yfo9xJbHmtHXMnxxkT9jqdXnHhm"


class Ata(unittest.TestCase):
    def test_known_atas(self):
        self.assertEqual(ata("4GUgVRftPkeqTNFc7nwZVRjqheBPMVToAhNYdkQVUz3e", KM), "3Eqs5ube7FVNi7R5xkG3oSaDcKgmZv2MhAL2gKtsx8uf")
        self.assertEqual(ata("9xivtNgqpBV1mJ9EVHyqFDvzi1DSSJvZyxaz477qr9s8", KM), "yCzh5N7gDU9xfWuLvGZ7iBJvGaXBnpRLgWYisikaFbs")
        self.assertEqual(ata("92d2PputxVRXp5hLY17EcAr9m1CG2cFG1PoSU2JZdxaH", KM), "GhP3hcWrPHiLygvgry4TD1zeDn8XrmNexPeTgMN5UPoV")

    def test_b58_roundtrip_and_curve(self):
        s = "11111111111111111111111111111111"
        self.assertEqual(b58e(b58d(s)), s)
        self.assertEqual(len(b58d(s)), 32)
        self.assertTrue(on_curve(b58d("4GUgVRftPkeqTNFc7nwZVRjqheBPMVToAhNYdkQVUz3e")))  # une clé de wallet est sur la courbe


if __name__ == "__main__":
    unittest.main()
