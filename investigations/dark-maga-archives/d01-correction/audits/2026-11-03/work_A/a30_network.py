#!/usr/bin/env python3
"""Auditeur A. Contre-vérification réseau bornée : au plus 300 getTransaction, tirage au hasard, graine 20261103.
Compare le brut au RPC (Helius, pool de recherche via dmaga.helius, jamais ~/Downloads/.env). Essaie aussi un RPC public sur 12 signatures.
Aucune clé ni URL avec clé n'est écrite. Sortie : out/a30_network.json."""
import gzip, json, random, sys, time, urllib.request
from pathlib import Path
sys.path.insert(0, "REDACTED_HOME/Projects/Dark-MAGA-Investigation")
from dmaga.helius import Helius
RAW = Path("/Volumes/VERBATIM HD/Dark-MAGA-Investigation/raw")
OUT = "REDACTED_HOME/Projects/Dark-MAGA-Investigation/audits/2026-11-03/work_A/out/a30_network.json"
SEED = 20261103
rng = random.Random(SEED)
ALLOC = {"full_pool": 110, "full_mint": 45, "full_venue": 20, "full_curve": 5, "ctrl_tx": 60}
sample = []
for src, k in ALLOC.items():
    if src == "full_curve":
        dirs = [RAW / src]
    else:
        dirs = sorted(p for p in (RAW / src).iterdir() if not p.name.startswith("._"))
    pages = []
    for d in dirs:
        pages += sorted(d.glob("p*.jsonl.gz"))
    rng.shuffle(pages)
    for p in pages[:k]:
        with gzip.open(p, "rt") as f:
            lines = f.readlines()
        line = rng.choice(lines)
        sample.append((src, str(p.relative_to(RAW)), json.loads(line)))
        del lines
print("échantillon", len(sample), flush=True)
# échouées : 40 signatures échouées tirées dans sigs_pool
pages = sorted((RAW / "sigs_pool").glob("p*.jsonl.gz"))
rng.shuffle(pages)
failed = []
for p in pages[:60]:
    with gzip.open(p, "rt") as f:
        rows = [json.loads(x) for x in f]
    rows = [r for r in rows if r.get("err") is not None]
    if rows:
        failed.append((str(p.relative_to(RAW)), rng.choice(rows)))
    if len(failed) >= 40:
        break
h = Helius(rps=3)
CFG = {"encoding": "jsonParsed", "maxSupportedTransactionVersion": 1, "commitment": "finalized"}


def cmp(a, b):
    """a = brut, b = réponse RPC. Rend la liste des champs différents."""
    d = []
    if b is None:
        return ["absente"]
    for k in ("slot", "blockTime"):
        if a.get(k) != b.get(k):
            d.append(k)
    if a["transaction"]["signatures"] != b["transaction"]["signatures"]:
        d.append("signatures")
    if [x["pubkey"] for x in a["transaction"]["message"]["accountKeys"]] != [x["pubkey"] for x in b["transaction"]["message"]["accountKeys"]]:
        d.append("accountKeys")
    for k in ("err", "fee", "preBalances", "postBalances", "preTokenBalances", "postTokenBalances"):
        if a["meta"].get(k) != b["meta"].get(k):
            d.append("meta." + k)
    return d


res = {"seed": SEED, "appels": 0, "ecarts": [], "comptes": {}, "failed_ecarts": [], "failed_ok": 0, "public": {}}
for src, page, tx in sample:
    sig = tx["transaction"]["signatures"][0]
    b = h.call("getTransaction", [sig, CFG])
    res["appels"] += 1
    d = cmp(tx, b)
    c = res["comptes"].setdefault(src, {"n": 0, "identiques": 0})
    c["n"] += 1
    if d:
        res["ecarts"].append({"src": src, "page": page, "signature": sig, "champs": d})
    else:
        c["identiques"] += 1
for page, r in failed:
    b = h.call("getTransaction", [r["signature"], CFG])
    res["appels"] += 1
    if b is None or b["meta"].get("err") is None or b.get("slot") != r["slot"] or b.get("blockTime") != r["blockTime"]:
        res["failed_ecarts"].append({"signature": r["signature"], "page": page, "rpc_err": None if b is None else b["meta"].get("err"), "liste_err": r.get("err")})
    else:
        res["failed_ok"] += 1
print("appels Helius", res["appels"], "stats", dict(h.stats), flush=True)
# RPC public, sans clé
PUB = "https://api.mainnet-beta.solana.com"
pub = {"url": PUB, "n": 0, "trouvees": 0, "vides": 0, "identiques": 0, "erreurs": []}
for src, page, tx in sample[:12]:
    body = json.dumps({"jsonrpc": "2.0", "id": 1, "method": "getTransaction", "params": [tx["transaction"]["signatures"][0], CFG]}).encode()
    try:
        with urllib.request.urlopen(urllib.request.Request(PUB, data=body, headers={"content-type": "application/json"}), timeout=30) as r:
            p = json.load(r)
        pub["n"] += 1
        if p.get("error"):
            pub["erreurs"].append(str(p["error"])[:120])
        elif p.get("result") is None:
            pub["vides"] += 1
        else:
            pub["trouvees"] += 1
            pub["identiques"] += not cmp(tx, p["result"])
    except Exception as e:
        pub["erreurs"].append(repr(e)[:120])
    time.sleep(1.5)
res["public"] = pub
json.dump(res, open(OUT, "w"), indent=1)
print(json.dumps({k: v for k, v in res.items() if k != "ecarts"}, indent=0)[:1500])
print("écarts", len(res["ecarts"]), res["ecarts"][:5])
