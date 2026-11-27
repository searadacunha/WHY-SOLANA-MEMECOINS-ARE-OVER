"""Complément de k14 : même test ATA, liste parcourue à l'envers via Helius (débit bas), écrit dans data/ata_scan_h.jsonl.
S'arrête dès qu'il rejoint un couple déjà écrit par k14 (relu toutes les 100 requêtes). Les deux fichiers se fusionnent
sans doublon dans k18 (clé owner, token)."""
import csv, json, time
from k_lib import DATA, KM, XC, utc
from k12_ata import ata
from dmaga.helius import Helius

MINTS = {"KM": KM, "XC": XC}
main, out = DATA / "ata_scan.jsonl", DATA / "ata_scan_h.jsonl"


def done_of(p):
    return {(json.loads(l)["owner"], json.loads(l)["token"]) for l in open(p)} if p.exists() else set()


addrs = [r["address"] for r in csv.DictReader(open(DATA / "dmaga_universe.csv"))][::-1]
mine, other = done_of(out), done_of(main)
h = Helius(rps=2, max_tries=20)
k = 0
with open(out, "a") as f:
    for a in addrs:
        for tk in ("XC", "KM"):
            if (a, tk) in mine:
                continue
            if (a, tk) in other:
                print("jonction atteinte", k); raise SystemExit(0)
            acc = ata(a, MINTS[tk])
            for attempt in range(30):  # « max usage reached » intermittent (constaté le 06/11) : pause puis clés réactivées
                try:
                    res = h.txs_page(acc, details="signatures", limit=1000, sort="asc")
                    break
                except Exception as e:
                    if "épuisées" not in str(e) and "max usage" not in str(e):
                        raise
                    h.dead.clear(); time.sleep(30)
            else:
                raise RuntimeError("Helius indisponible après 30 pauses")
            sigs = [[s["signature"], s.get("blockTime"), s.get("err") is not None] for s in res["data"]]
            f.write(json.dumps({"owner": a, "token": tk, "ata": acc, "n": len(sigs), "more": len(sigs) == 1000, "src": "helius-gtfa",
                                "first": utc(sigs[0][1]) if sigs else "", "sigs": sigs}) + "\n")
            f.flush()
            k += 1
            if k % 100 == 0:
                other = done_of(main)
                print(k, dict(h.stats), flush=True)
print("fin", k)
