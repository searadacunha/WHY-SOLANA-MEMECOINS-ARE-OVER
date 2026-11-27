#!/usr/bin/env python3
"""Sonde reseau : pour chaque adresse, une page de 1000 signatures et une page de 100 transactions completes (les plus recentes jusqu'a la date demandee).
Mesure : volume, contreparties SOL dans l'echantillon, frequence de signature, solde. Ecrit probe_<etiquette>.csv et conserve le brut en un seul fichier gz.
usage: c11_probe.py <etiquette> <adresse> [<adresse>...]
"""
import csv
import gzip
import json
import sys
import time
from collections import Counter
from pathlib import Path

from dmaga.helius import Helius

WORK = Path(__file__).resolve().parent
NET = Path("/Volumes/VERBATIM HD/Dark-MAGA-Investigation/audits_work/C/net")
CRED = WORK / "credits.csv"


def note(method, addr):
    with open(CRED, "a") as f:
        f.write(f"{time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())},{method},{addr},10\n")


def used():
    return sum(int(l.split(",")[3]) for l in CRED.read_text().splitlines()[1:] if l.strip())


def main():
    tag, addrs = sys.argv[1], sys.argv[2:]
    h = Helius()
    raw = gzip.open(NET / f"probe_{tag}.jsonl.gz", "at", compresslevel=6)
    w = csv.writer(open(WORK / f"probe_{tag}.csv", "a", newline=""))
    w.writerow("addr n_sigs_page more first_bt last_bt n_sample sol_in_ctp sol_out_ctp n_signer top_in top_out".split())
    for a in addrs:
        assert used() + 20 <= 20000, "budget"
        s = h.txs_page(a, details="signatures", limit=1000, sort="desc", filters={"tokenAccounts": "balanceChanged"})
        note("gtfa_signatures", a)
        rows = s["data"]
        r = h.txs_page(a, details="full", limit=100, sort="desc", filters={"tokenAccounts": "balanceChanged", "status": "succeeded"})
        note("gtfa_full", a)
        ctp_in, ctp_out = Counter(), Counter()
        n_sign = 0
        for tx in r["data"]:
            raw.write(json.dumps({"probe": a, "tx": tx}, separators=(",", ":")) + "\n")
            akeys = tx["transaction"]["message"]["accountKeys"]
            n_sign += any(k["pubkey"] == a and k["signer"] for k in akeys)
            seq = list(tx["transaction"]["message"]["instructions"])
            for g in tx["meta"].get("innerInstructions") or []:
                seq += g["instructions"]
            for ins in seq:
                p = ins.get("parsed")
                if ins.get("program") == "system" and isinstance(p, dict) and p.get("type") == "transfer":
                    i = p["info"]
                    if i.get("destination") == a:
                        ctp_in[i["source"]] += int(i["lamports"])
                    if i.get("source") == a:
                        ctp_out[i["destination"]] += int(i["lamports"])
        w.writerow([a, len(rows), bool(s.get("paginationToken")), rows[-1]["blockTime"] if rows else "", rows[0]["blockTime"] if rows else "",
                    len(r["data"]), len(ctp_in), len(ctp_out), n_sign,
                    ";".join(f"{k}:{v/1e9:.3f}" for k, v in ctp_in.most_common(5)), ";".join(f"{k}:{v/1e9:.3f}" for k, v in ctp_out.most_common(5))])
    raw.close()
    print("credits", used(), dict(h.stats))


if __name__ == "__main__":
    main()
