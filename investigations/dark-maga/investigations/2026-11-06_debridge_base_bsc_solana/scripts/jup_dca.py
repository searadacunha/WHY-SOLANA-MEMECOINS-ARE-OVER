"""Décodage des positions Jupiter DCA (programme DCA265Vj8a9CEuX1eb1LWRnDT7uK6q1xMipnNyatn23M) à partir des événements
« self-CPI » Anchor présents dans les instructions internes d'une transaction (Opened, Filled, CollectedFee, Withdraw, Closed).

Structures et discriminants : ceux du décodeur Carbon (sevenlabs-hq/carbon, decoders/jupiter-dca-decoder/src/events/*.rs,
commit bebd1085f7cb7d0bc9d30c7367142ff620086681, licence MIT, généré par Codama depuis l'IDL). Rien n'est copié : les
champs sont relus et le discriminant de chaque événement est recalculé (sha256("event:<Nom>")[:8], contrôlé en fin de
fichier contre les octets publiés par Carbon). Première version écrite par l'audit Solana indépendant du 06/11/2026.

Contrôle de cohérence d'une position fermée : in_deposited = somme des in_amount des Filled + unfilled_amount.
Les exécutants (keepers) qui paient les transactions de remplissage sont un service Jupiter partagé : jamais un lien."""
import hashlib

DCA = "DCA265Vj8a9CEuX1eb1LWRnDT7uK6q1xMipnNyatn23M"
TAG = bytes.fromhex("e445a52e51cb9a1d")  # préfixe des événements émis par CPI (Anchor)
SPEC = {
    "Opened": "user:p dca:p in_deposited:u input_mint:p output_mint:p cycle_frequency:i in_amount_per_cycle:u created_at:i",
    "Filled": "user:p dca:p input_mint:p output_mint:p in_amount:u out_amount:u fee_mint:p fee:u",
    "CollectedFee": "user:p dca:p mint:p amount:u",
    "Withdraw": "dca:p in_amount:u out_amount:u user_withdraw:b",
    "Deposit": "dca:p amount:u",
    "Closed": "user:p dca:p in_deposited:u input_mint:p output_mint:p cycle_frequency:i in_amount_per_cycle:u created_at:i "
              "total_in_withdrawn:u total_out_withdrawn:u unfilled_amount:u user_closed:b",
}
DISC = {hashlib.sha256(("event:" + n).encode()).digest()[:8]: n for n in SPEC}
B58 = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"

def b58d(s):
    n = 0
    for c in s: n = n * 58 + B58.index(c)
    b = n.to_bytes((n.bit_length() + 7) // 8, "big")
    return b"\0" * (len(s) - len(s.lstrip("1"))) + b

def b58e(b):
    n = int.from_bytes(b, "big"); s = ""
    while n: n, r = divmod(n, 58); s = B58[r] + s
    return "1" * (len(b) - len(b.lstrip(b"\0"))) + s

def decode(name, b):
    i, d = 0, {}
    for f in SPEC[name].split():
        k, ty = f.split(":")
        if ty == "p": d[k] = b58e(b[i:i + 32]); i += 32
        elif ty == "b": d[k] = bool(b[i]); i += 1
        else: d[k] = int.from_bytes(b[i:i + 8], "little", signed=(ty == "i")); i += 8
    if i != len(b): raise ValueError(f"{name}: {len(b)} octets, {i} attendus")
    return d

def events(tx):
    """Liste (nom, champs) des événements DCA d'une transaction jsonParsed (meta.innerInstructions)."""
    if tx["meta"].get("err") is not None: return []
    out = []
    for inner in tx["meta"].get("innerInstructions") or []:
        for ix in inner["instructions"]:
            if ix.get("programId") != DCA or "data" not in ix: continue
            b = b58d(ix["data"])
            if b[:8] == TAG and b[8:16] in DISC:
                n = DISC[b[8:16]]; out.append((n, decode(n, b[16:])))
    return out

def positions(txs):
    """Regroupe les événements par compte DCA : ouverture, exécutions, frais, retraits, clôture."""
    pos = {}
    for t in txs:
        for n, d in events(t):
            p = pos.setdefault(d["dca"], dict(dca=d["dca"], opened=None, fills=[], fees=[], withdraws=[], closed=None))
            sig = t["transaction"]["signatures"][0]
            if n == "Opened": p["opened"] = dict(d, sig=sig, ts=t["blockTime"])
            elif n == "Filled": p["fills"].append(dict(d, sig=sig, ts=t["blockTime"]))
            elif n == "CollectedFee": p["fees"].append(dict(d, sig=sig))
            elif n == "Withdraw": p["withdraws"].append(dict(d, sig=sig))
            elif n == "Closed": p["closed"] = dict(d, sig=sig, ts=t["blockTime"])
    for p in pos.values():
        c = p["closed"]
        p["in_filled"] = sum(f["in_amount"] for f in p["fills"]); p["out_filled"] = sum(f["out_amount"] for f in p["fills"])
        p["consistent"] = (c["in_deposited"] == p["in_filled"] + c["unfilled_amount"]) if c else None
    return pos

def _selftest():
    carbon = {"Opened": "a6ac61094d4cbd6d", "Filled": "8604113fdd2db1ad", "Withdraw": "c0f1c9d946965af7",
              "CollectedFee": "2a88d874b5d16db5", "Closed": "321f579b87dcc3ef"}  # octets 8 à 15 des discriminants Carbon
    for n, h in carbon.items():
        assert hashlib.sha256(("event:" + n).encode()).digest()[:8].hex() == h, n
    assert b58e(b58d(DCA)) == DCA and len(b58d(DCA)) == 32
_selftest()
