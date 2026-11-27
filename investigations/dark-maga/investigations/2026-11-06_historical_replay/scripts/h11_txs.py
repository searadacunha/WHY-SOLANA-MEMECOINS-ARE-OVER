"""Transactions complètes (jsonParsed, instructions internes) des signatures réussies d'une adresse, mises en cache par k16.

usage: h11_txs.py <adresse> [--since unix] [--until unix] [--workers N]. Exige sigs_<adresse>.json (h10).
Toute transaction introuvable lève une erreur comptée : jamais de trou muet."""
import argparse
import json
import time
from concurrent.futures import ThreadPoolExecutor
from h_lib import EXT
import k16_pubrpc as pub

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("address")
    ap.add_argument("--since", type=int, default=0)
    ap.add_argument("--until", type=int, default=2**40)
    ap.add_argument("--workers", type=int, default=4)
    a = ap.parse_args()
    d = json.loads((EXT / f"sigs_{a.address}.json").read_text())
    todo = [x["signature"] for x in d["sigs"] if not x.get("err") and a.since <= (x.get("blockTime") or 0) < a.until]
    fails, t0 = [], time.time()

    def job(s):
        try:
            pub.tx(s)
            return True
        except Exception as e:  # signature à refaire : comptée et listée
            fails.append((s, repr(e)[:200]))
            return False

    with ThreadPoolExecutor(a.workers) as ex:
        for i, _ in enumerate(ex.map(job, todo), 1):
            if i % 500 == 0 or i == len(todo):
                print(f"{a.address[:8]} {i}/{len(todo)} échecs={len(fails)} {i / (time.time() - t0):.1f} tx/s", flush=True)
    if fails:
        (EXT / f"txfail_{a.address}.json").write_text(json.dumps(fails))
    print("FIN", a.address[:8], len(todo), "échecs", len(fails), flush=True)
    raise SystemExit(1 if fails else 0)
