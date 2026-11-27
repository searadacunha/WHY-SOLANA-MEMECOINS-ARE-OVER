"""(06/11 : les 7 393 premiers couples via Helius getTransactionsForAddress, tri croissant, 1 000 max, champ « more »
non fiable ; la suite via le RPC public, toutes pages jusqu'à 5 000, champ src = public-rpc.)

Pour chaque adresse de l'univers DMAGA et chaque mint Kekius Solana : historique de signatures de son ATA.

Reprise : les couples déjà écrits dans data/ata_scan.jsonl sont sautés. Une erreur RPC arrête le script (rien n'est
écrit en « vide » à la place d'une panne)."""
import csv, json, sys, time
from k_lib import DATA, KM, XC, utc
from k12_ata import ata
import k16_pubrpc as pub

MINTS = {"KM": KM, "XC": XC}
out = DATA / "ata_scan.jsonl"
done = set()
if out.exists():
    for line in open(out):
        r = json.loads(line)
        done.add((r["owner"], r["token"]))
addrs = [r["address"] for r in csv.DictReader(open(DATA / "dmaga_universe.csv"))]
t0, k = time.time(), 0
with open(out, "a") as f:
    for a in addrs:
        for tk, mint in MINTS.items():
            if (a, tk) in done:
                continue
            acc = ata(a, mint)
            res, trunc = pub.sigs(acc)
            sigs = sorted([[s["signature"], s.get("blockTime"), s.get("err") is not None] for s in res], key=lambda x: x[1] or 0)
            f.write(json.dumps({"owner": a, "token": tk, "ata": acc, "n": len(sigs), "more": trunc, "src": "public-rpc",
                                "first": utc(sigs[0][1]) if sigs else "", "sigs": sigs}) + "\n")
            k += 1
            if k % 500 == 0:
                f.flush()
                print(f"{k} {k/(time.time()-t0):.1f}/s", flush=True)
print("fin", k)
