"""Contrôle du changement de source du scan ATA : 15 couples avec activité et 15 sans, déjà lus via Helius, relus via le RPC
public. Écrit data/ata_backend_check.json. Un écart de compte de signatures est signalé, pas corrigé."""
import json, random
from k_lib import DATA
import k16_pubrpc as pub

recs = [json.loads(l) for l in open(DATA / "ata_scan.jsonl")]
hel = [r for r in recs if r.get("src") is None]
random.seed(20261106)
sample = random.sample([r for r in hel if 0 < r["n"] < 1000], 15) + random.sample([r for r in hel if r["n"] == 0], 15)
out = []
for r in sample:
    s, tr = pub.sigs(r["ata"])
    hs = {x[0] for x in r["sigs"]}
    ps = {x["signature"] for x in s}
    out.append({"owner": r["owner"], "token": r["token"], "helius_n": r["n"], "public_n": len(ps), "same_set": hs == ps,
                "only_helius": len(hs - ps), "only_public": len(ps - hs)})
json.dump(out, open(DATA / "ata_backend_check.json", "w"), indent=1)
print(sum(o["same_set"] for o in out), "/", len(out), "identiques ;", [o for o in out if not o["same_set"]])
