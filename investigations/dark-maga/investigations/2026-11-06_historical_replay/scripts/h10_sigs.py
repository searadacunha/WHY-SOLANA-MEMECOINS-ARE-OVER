"""Liste complète des signatures d'adresses (RPC public), du plus récent au plus ancien, écrite une fois complète.

usage: h10_sigs.py <adresse> [...] [--max-pages N]. Sortie : HIST_EXT/sigs_<adresse>.json = {"truncated": bool, "sigs": [...]}.
Un fichier existant n'est pas relu sur le réseau ; une liste tronquée le dit."""
import json
import sys
from h_lib import EXT
import k16_pubrpc as pub

if __name__ == "__main__":
    args = sys.argv[1:]
    cap = 200
    if "--max-pages" in args:
        i = args.index("--max-pages")
        cap = int(args[i + 1])
        del args[i:i + 2]
    for a in args:
        p = EXT / f"sigs_{a}.json"
        if p.exists():
            d = json.loads(p.read_text())
        else:
            s, trunc = pub.sigs(a, max_pages=cap)
            d = {"address": a, "truncated": trunc, "n": len(s), "sigs": s}
            tmp = p.with_suffix(".tmp")
            tmp.write_text(json.dumps(d))
            tmp.replace(p)
        ok = [x for x in d["sigs"] if not x.get("err")]
        bt = [x["blockTime"] for x in d["sigs"] if x.get("blockTime")]
        print(a[:8], "n", d["n"], "réussies", len(ok), "tronqué", d["truncated"], "de", min(bt) if bt else None, "à", max(bt) if bt else None, flush=True)
