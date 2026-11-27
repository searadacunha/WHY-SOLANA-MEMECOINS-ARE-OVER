"""Collecte l'historique Ethereum complet des 4 receveurs (tx propres, internes, ERC-20, ERC-721, ERC-1155) via Routescan.
Sortie : ../evidence/c01_counts.json (comptes par adresse et action). Les lignes restent dans le cache brut."""
import json, sys
sys.path.insert(0, ".")
import ev_lib as E
A = {"b947": "0xb947bf7f409e998b28f8e218802fc9575c3c8c57", "b298": "0xb29826d809aa04d2ead6f2310d8965a45b87fa67",
     "2d86": "0x2d86499a410a9ac2139833ba8d6942b8a8700a7b", "86f9": "0x86f99097c563e84dd5190f3e85f6a2988f1c47a5"}
ACTIONS = ["txlist", "txlistinternal", "tokentx", "tokennfttx", "token1155tx"]
if __name__ == "__main__":
    counts = {}
    for k, a in A.items():
        for act in ACTIONS:
            rows = E.pull(a, act)
            counts[f"{k}.{act}"] = len(rows)
            print(k, act, len(rows), flush=True)
    json.dump(counts, open("../evidence/c01_counts.json", "w"), indent=1)
