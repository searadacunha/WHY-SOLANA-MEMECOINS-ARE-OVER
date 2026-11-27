"""Activité complète d'une contrepartie (RPC public) : entrées et sorties SOL/jetons par instruction, pour décider service ou wallet.

usage: h33_counterparty.py <adresse> [--max-pages N]. Sortie : data/counterparty_<adresse>.csv. Une adresse à plus de
--max-pages × 1000 signatures est déclarée service probable sans lecture complète (le dire, pas le cacher)."""
import csv
import sys
from h_lib import DATA, utc
import k16_pubrpc as pub
from h_decode import movements, signers

if __name__ == "__main__":
    a = sys.argv[1]
    cap = int(sys.argv[sys.argv.index("--max-pages") + 1]) if "--max-pages" in sys.argv else 2
    sigs, trunc = pub.sigs(a, max_pages=cap)
    rows = []
    for x in sorted((x for x in sigs if not x.get("err")), key=lambda x: x["slot"]):
        t = pub.tx(x["signature"])
        for m in movements(t):
            if a in (m["src"], m["dst"]) and m["amount"] > 0:
                rows.append({"utc": utc(t["blockTime"]), "slot": t["slot"], "signature": x["signature"], "signers": ";".join(signers(t)),
                             "dir": "out" if m["src"] == a else "in", "counterparty": m["dst"] if m["src"] == a else m["src"],
                             "kind": m["kind"], "mint": m["mint"], "amount_raw": m["amount"]})
    with (DATA / f"counterparty_{a}.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["utc", "slot", "signature", "signers", "dir", "counterparty", "kind", "mint", "amount_raw"])
        w.writeheader()
        w.writerows(rows)
    print(a, "signatures", len(sigs), "tronqué", trunc, "mouvements", len(rows))
