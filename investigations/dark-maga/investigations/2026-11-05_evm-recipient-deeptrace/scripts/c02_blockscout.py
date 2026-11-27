"""Historique Blockscout v2 complet (jetons, tx, internes) des adresses données en argument. Sortie : ../evidence/c02_counts.json (fusionné)."""
import json, sys, os
sys.path.insert(0, ".")
import ev_lib as E
out = "../evidence/c02_counts.json"
counts = json.load(open(out)) if os.path.exists(out) else {}
for a in sys.argv[1:]:
    for kind in ["token-transfers", "transactions", "internal-transactions"]:
        items, complete = E.bs_all(a, kind)
        counts[f"{a}.{kind}"] = {"n": len(items), "complete": complete}
        print(a[:10], kind, len(items), "complet" if complete else "TRONQUÉ", flush=True)
        json.dump(counts, open(out, "w"), indent=1)
