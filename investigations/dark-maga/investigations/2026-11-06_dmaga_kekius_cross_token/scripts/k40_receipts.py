"""Fige les transactions Solana citées dans FINDINGS.md (evidence/receipts/<signature>.json) pour l'autocontrôle hors ligne.

Source : pages Helius déjà collectées (km_curve, xc_curve) ou RPC public (cache) pour les autres."""
import json
from k_lib import EVID
from dmaga.collect import iter_raw
import k16_pubrpc as pub

SIGS = {
    "51W3rg9BpBtWXTTcoRhB3akNPXUpPq9XnkjkDyHV7hCS7wR6MU8U9pnYGUWFW4qBW68iFhSHTxGRCELi8NEcxFsK": "KM : création",
    "BA2V9YnMrWxk1PyF1ty6mNpg4Yu8y244YdH3QbcBBHyyMyniuit5fT8L4vLpjdKwgksxJtLRMxfGMQ8UeSzQJAR": "KM : retrait de migration",
    "62w4TMRQWxJyC975YNETztMC7CNmQSFqjDKiS8RfqCxvDQEN4BfL5XJRccpqXY7XcF37YyLAPdk61GAgZb36myvt": "KM : initialisation Raydium",
    "2xz9tgPBSztVPE6voEL8yKCFv37qUyojVUtEA1Uab4FzeJtDpi6ePPCpsFUzfhKfLTVrPuzpdYFLyk8dojREBq7D": "XC78 : création",
    "5p39GsYPf4zwCMRdLV8iJrqtHjcQw8VtPAP6oYugqCF3oyj98JEFXg7VT78uPpJWhxxKWHDWGsENG1ndDRuAjhST": "XC78 : achat Go5rFkwK au slot de création",
    "5GvjoEMEiPfjqnck7iegRCGuKUrtfe1amJYvvR6D7WxrcPWA19peM163vuEQuorCZDFpYHmknUJ5TDSnPxHfYBxn": "XC78 : vente Go5rFkwK et répartition vers 10 wallets",
    "5wEA4w1XUd987pABFyXYujoCKHJkJ1VSKwaD3bKxgBKy8xeBJ9j4uMvDc6Y5gkDfMfuz2MyhoMwoSjuwsAwPRSiZ": "XC78 : retrait de migration",
    "3hpRnD1mQ9LwfjkdwMFoP7RX2aEp3Z3GJoA9ipriyQGPKrs3v7bdj2bvwLLRNXcfBSwuqG5r55GqMvSNz7tTi5RR": "XC78 : initialisation Raydium",
}


def bundle_sigs():
    out = {}
    for t in iter_raw("xc_curve"):
        s = t["transaction"]["signatures"][0]
        if t["slot"] == 310594130 and not t["meta"]["err"]:
            keys = [k for k in t["transaction"]["message"]["accountKeys"] if k.get("signer")]
            if len(keys) >= 4:
                out[s] = "XC78 : achat co-signé par 4 wallets, slot 310594130"
    return out


if __name__ == "__main__":
    import sys
    extra = dict(a.split("=", 1) for a in sys.argv[1:])
    SIGS.update(bundle_sigs())
    SIGS.update(extra)
    raw = {t["transaction"]["signatures"][0]: t for lab in ("km_curve", "xc_curve") for t in iter_raw(lab)}
    d = EVID / "receipts"
    d.mkdir(parents=True, exist_ok=True)
    index = {}
    for s, why in SIGS.items():
        t = raw.get(s) or pub.tx(s)
        (d / f"{s}.json").write_text(json.dumps(t, separators=(",", ":")))
        index[s] = why
    (d / "INDEX.json").write_text(json.dumps(index, ensure_ascii=False, indent=1))
    print(len(index), "reçus")
