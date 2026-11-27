"""Transactions brutes (courbe Pump.fun ou pool Raydium) -> lignes d'échange par propriétaire.

Une ligne = (signature, slot, temps, propriétaire, delta jeton, delta SOL du propriétaire s'il signe, signataires).
Les comptes du lieu d'échange (courbe, autorité Raydium) sont exclus comme propriétaires."""
import csv, gzip, io
from k11_parse import token_deltas, sol_deltas, signers
from dmaga.collect import iter_raw

VENUE_OWNERS = {"5Q544fKrFoe6tsEbD7S8EmxGTJYAKtTVhAW5Q5pge4j1",  # autorité Raydium AMM v4
                "39azUYFWPz3VHgKCf3VChUwbpURdCHRxjWVowf5jUJjg"}  # compte de migration Pump.fun


def rows(label, mint, venue_owner):
    excl = VENUE_OWNERS | {venue_owner}
    for t in iter_raw(label):
        if t["meta"]["err"]:
            continue
        sg = signers(t)
        sd = sol_deltas(t)
        for owner, d in token_deltas(t, mint).items():
            if owner in excl:
                continue
            yield {"sig": t["transaction"]["signatures"][0], "slot": t["slot"], "time": t["blockTime"],
                   "owner": owner, "token_raw": d, "owner_sol_lamports": sd.get(owner, 0) if owner in sg else "",
                   "fee_payer": sg[0], "signers": ";".join(sg)}


def write(path, it):
    buf = io.StringIO()
    w = None
    n = 0
    for r in it:
        if w is None:
            w = csv.DictWriter(buf, fieldnames=list(r))
            w.writeheader()
        w.writerow(r)
        n += 1
    path.write_bytes(gzip.compress(buf.getvalue().encode(), 9))
    return n
