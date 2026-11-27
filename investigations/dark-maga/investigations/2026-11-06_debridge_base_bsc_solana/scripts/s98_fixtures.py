"""Copie dans evidence/fixtures/ l'ensemble minimal de réponses brutes qui permet de rejouer hors ligne les chiffres clés
depuis un clone neuf, et écrit evidence/fixtures/MANIFEST.json (taille et sha256 de chaque fichier, origine de la requête).

- cache/ : réponses RPC brutes, sous leur clé de cache d'origine (sha256 de la requête), lues en premier par nt_lib :
  les reçus EVM des événements DLN des liens de CROSSCHAIN_LINKS.csv, les soldes archive de Base (s11) et d'Ethereum (s14).
- sol/ : transactions Solana complètes (Helius, jsonParsed) : historiques entiers des petits wallets, et pour Ei5yGz8d
  les seules transactions citées par les tests. Une transaction par ligne, telle que reçue.
Usage : DMAGA_NT_RAW_RO=<raw existants> python3 -I s98_fixtures.py"""
import csv, gzip, hashlib, json, os, shutil, sys
sys.path.insert(0, os.path.dirname(__file__))
import nt_lib as N

R = N.ROOT; F = R / "evidence" / "fixtures"
SOL_FULL = ["8kNKNiHKjbCPjaWGjoEEWeQ6X4jkZn2sDV7tz7azfL4t", "BdX9J5pQZ9SoH7PqwDCiiQ2rzaMiT4D9WZ8C1DiwXgyX",
            "GV2w4YvXeYtEv8LkKFKpFbrqBnvn9HYLesjKgvMyJD5f", "96W8V3toGu55gApT1cNFrZmkcGZwt5YGYotpWaK6fNAm",
            "39dTXaMMMy4AV6jhihEmfqdnAkhpwCpYpz9SnvP3y1h7", "Hp2BtvnZvw7YxbQvSehqb1LC5jBSX1aLApzHQnDVwf3q"]
PARTIAL = {N.EI5: R / "evidence" / "fixtures_ei5_signatures.txt",  # listes relues : une signature par ligne
           "2aeEoq5n8Cip2raJsiWHBVKuoJL4rid7adepkVYnVzDm": R / "evidence" / "fixtures_2aeEoq5n_signatures.txt"}

def roots():
    return [N.NEW_RAW] + [d for r in N.RAW_RO for d in (r / "cache", r)]

def find(key):
    for b in roots():
        p = b / key[:2] / (key + ".json")
        if p.exists(): return p

def ledger_index():
    """clé de cache -> requête, d'après les ledger.jsonl de chaque cache."""
    out = {}
    for b in roots():
        p = b / "ledger.jsonl"
        if p.exists():
            for l in open(p):
                try: d = json.loads(l)
                except Exception: continue
                out.setdefault(d["key"], d.get("url", ""))
    return out

def receipt_keys(txs):
    keys = {}
    for b in roots():
        if not b.is_dir(): continue
        for p in b.glob("[0-9a-f][0-9a-f]/*.json"):
            if p.stem in keys.values(): continue
            try: d = json.loads(p.read_bytes())
            except Exception: continue
            items = [x.get("result") for x in d] if isinstance(d, list) else [d.get("result") if isinstance(d, dict) else None]
            for r in items:
                if isinstance(r, dict) and (r.get("transactionHash") or "").lower() in txs:
                    keys[r["transactionHash"].lower()] = p.stem
    return keys

if __name__ == "__main__":
    links = {int(k["orderId"], 16) for k in csv.DictReader(open(R / "CROSSCHAIN_LINKS.csv"))}
    need = {r["tx"] for r in csv.DictReader(open(R / "evidence/s13_orderid_check.csv")) if int(r["orderId"], 16) in links}
    keys = receipt_keys(need)
    miss = need - set(keys)
    assert not miss, f"reçus introuvables : {sorted(miss)[:5]}"
    idx = ledger_index()
    extra = [l.strip() for l in open(R / "evidence/fixtures_cache_keys.txt") if l.strip() and not l.startswith("#")] \
        if (R / "evidence/fixtures_cache_keys.txt").exists() else []
    extra += [k for k, u in idx.items() if u.startswith(("base eth_getBalance", "base eth_call"))]  # soldes archive de s11
    if F.exists(): shutil.rmtree(F)
    man = {"cache": {}, "sol": {}}
    for k in sorted(set(keys.values()) | set(extra)):
        src = find(k); assert src, k
        dst = F / "cache" / k[:2] / (k + ".json"); dst.parent.mkdir(parents=True, exist_ok=True); shutil.copyfile(src, dst)
        b = dst.read_bytes(); man["cache"][f"cache/{k[:2]}/{k}.json"] = dict(bytes=len(b), sha256=hashlib.sha256(b).hexdigest(), request=idx.get(k, "")[:200])
    hist = N.raw_dir("sol_hist")
    (F / "sol").mkdir(parents=True, exist_ok=True)
    for w in SOL_FULL + list(PARTIAL):
        src = hist / f"{w}.jsonl.gz"
        if not src.exists():
            src = next(p for p in [r / "sol_hist" / f"{w}.jsonl.gz" for r in [N.RAW] + N.RAW_RO] if p.exists())
        lines = [l for l in gzip.open(src, "rt")]
        if w in PARTIAL:
            sigs = {l.strip() for l in open(PARTIAL[w]) if l.strip() and not l.startswith("#")}
            lines = [l for l in lines if json.loads(l)["transaction"]["signatures"][0] in sigs]
            got = {json.loads(l)["transaction"]["signatures"][0] for l in lines}
            assert got == sigs, f"signatures absentes de l'historique : {sorted(sigs - got)[:3]}"
        dst = F / "sol" / f"{w}.jsonl"; dst.write_text("".join(lines))
        b = dst.read_bytes()
        man["sol"][f"sol/{w}.jsonl"] = dict(bytes=len(b), sha256=hashlib.sha256(b).hexdigest(), transactions=len(lines),
                                            source_sha256=hashlib.sha256(src.read_bytes()).hexdigest(), complete_history=w in SOL_FULL)
    (F / "MANIFEST.json").write_text(json.dumps(man, indent=1, sort_keys=True) + "\n")
    tot = sum(v["bytes"] for s in man.values() for v in s.values())
    print(len(man["cache"]), "réponses RPC,", len(man["sol"]), "fichiers Solana,", round(tot / 1e6, 2), "Mo")
