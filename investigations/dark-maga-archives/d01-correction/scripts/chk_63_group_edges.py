#!/usr/bin/env python3
"""Relit sur la chaîne chaque arête du groupe de lancement et le virement au créateur : qui signe, quel programme, swap ou non.

Une arête ne vaut « transfert direct » que si la source signe, sans programme d'échange ni de DCA dans la transaction. Sortie :
reports/data_checks/group_edges_check.json. Un agrégateur ou un exécutant est signalé, l'arête n'est plus une preuve de lien.
"""
import json
from pathlib import Path

from dmaga.config import DATA
from dmaga.helius import Helius

h = Helius(rps=4)
SWAP = {"JUP6LkbZbjS1jKKwapdHNy74zcZ3tLUZoi5QNyVTaV4": "Jupiter", "DCA265Vj8a9CEuX1eb1LWRnDT7uK6q1xMipnNyatn23M": "Jupiter DCA",
        "675kPX9MHTjS2zt1qfr1NYHuzeLXfQM9H24wFSUt1Mp8": "Raydium", "LBUZKhRxPF3XUpBCjp4YzTKgLccjZhTSDM9YuVaPwxo": "Meteora DLMM",
        "whirLbMiicVdio4qvUfM5KAg6Ct8VwpYzGff3uctyCc": "Orca", "CAMMCzo5YL8w4VFF8KVHrK22GGUsp5VTaW7grrKgrWqK": "Raydium CLMM"}


def inspect(sig, src):
    t = h.call("getTransaction", [sig, {"encoding": "jsonParsed", "maxSupportedTransactionVersion": 1}])
    keys = t["transaction"]["message"]["accountKeys"]
    signers = [k["pubkey"] for k in keys if k.get("signer")]
    progs = {i.get("programId") for i in t["transaction"]["message"]["instructions"]}
    for inner in t["meta"].get("innerInstructions") or []:
        progs |= {i.get("programId") for i in inner["instructions"]}
    swaps = sorted(SWAP[p] for p in progs if p in SWAP)
    return {"signers": signers, "source_signe": src in signers, "programmes_echange": swaps, "direct": src in signers and not swaps,
            "programmes": sorted(p for p in progs if p)[:8]}


groups = json.loads((DATA / "prevent_groups.json").read_text())
out = {"group": [], "n": 0, "n_direct": 0}
for e in groups[0]["edges_top"]:
    r = inspect(e["sig"], e["src"])
    out["group"].append({**e, **r})
    out["n"] += 1
    out["n_direct"] += r["direct"]
    if not r["direct"]:
        print("NON DIRECT", e["src"][:8], e["dst"][:8], e["M"], r["signers"][:2], r["programmes_echange"])
C = "8YLEuUtZ4eFMJbf46oNb1CeG6dYFWGyxnQSh9hrgzBzR"
Q = "5QhJJcFZu2ashyKyWSTGHcsyo6ZBCbpVuJqeutvQHScd"
g = h.call("getTransfersByAddress", [C, {"with": Q, "limit": 10, "sortOrder": "asc"}])["data"][0]
out["gaz_vers_createur"] = {"signature": g["signature"], "t": g["blockTime"], "montant": g["uiAmount"], **inspect(g["signature"], Q)}
m = h.call("getTransfersByAddress", [C, {"mint": "7D7BRcBYepfi77vxySapmeqRNN1wsBBxnFPJGbH5pump", "direction": "out", "limit": 1, "sortOrder": "asc"}])["data"][0]
out["deplacement_createur"] = {"signature": m["signature"], "t": m["blockTime"], "montant": m["uiAmount"], **inspect(m["signature"], C)}
Path("reports/data_checks").mkdir(parents=True, exist_ok=True)
Path("reports/data_checks/group_edges_check.json").write_text(json.dumps(out, indent=1))
print(f"arêtes relues {out['n']}, directes {out['n_direct']}")
print("gaz", {k: out["gaz_vers_createur"][k] for k in ("t", "montant", "signers", "direct", "programmes_echange")})
print("déplacement", {k: out["deplacement_createur"][k] for k in ("t", "montant", "signers", "direct", "programmes_echange")})
