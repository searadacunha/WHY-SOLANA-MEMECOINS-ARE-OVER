"""Grand livre Base de b298 depuis les pages Blockscout brutes (raw/browser_dump), pagination complète exigée.
Une ligne par mouvement de valeur : tx native (valeur + frais), transfert de jeton, transaction interne.
Sortie : data/base_b298_ledger.csv. Usage : python3 -I s10_base_ledger.py [adresse] [chaine]"""
import sys, collections
sys.path.insert(0, __import__("os").path.dirname(__file__))
import nt_lib as N

def h(x): return ((x or {}).get("hash") or "").lower()
def nm(x): return (x or {}).get("name") or ((x or {}).get("metadata") or {}).get("tags", [{}])[0].get("name", "") if x else ""

def ledger(addr, chain="base"):
    addr = addr.lower(); rows = []
    txs, d1, _ = N.dump_pages(chain, addr, "transactions")
    tts, d2, _ = N.dump_pages(chain, addr, "token-transfers")
    its, d3, _ = N.dump_pages(chain, addr, "internal-transactions")
    assert d1 and d2 and d3, f"pagination incomplète pour {addr}: {d1, d2, d3}"
    seen = set()
    for x in txs:
        if x["hash"] in seen: continue
        seen.add(x["hash"])
        rows.append(dict(kind="tx", tx=x["hash"], block=x["block_number"], ts=x["timestamp"][:19], log_index="", frm=h(x["from"]), to=h(x["to"]),
                         to_name=nm(x["to"]), from_name=nm(x["from"]), asset="ETH", token="", raw=int(x["value"] or 0), decimals=18,
                         fee=int((x.get("fee") or {}).get("value") or 0), method=x.get("method") or "", status=x.get("status") or "", nonce=x.get("nonce")))
    seen = set()
    for x in tts:
        k = (x["transaction_hash"], x["log_index"])
        if k in seen: continue
        seen.add(k); t = x["token"] or {}; tot = x.get("total") or {}
        rows.append(dict(kind="token", tx=x["transaction_hash"], block=x["block_number"], ts=x["timestamp"][:19], log_index=x["log_index"],
                         frm=h(x["from"]), to=h(x["to"]), from_name=nm(x["from"]), to_name=nm(x["to"]), asset=t.get("symbol") or "",
                         token=(t.get("address_hash") or t.get("address") or "").lower(), raw=int(tot.get("value") or 0) if "value" in tot else "",
                         decimals=int(tot.get("decimals") or t.get("decimals") or 0), fee="", method=x.get("method") or "", status=x.get("type") or "", nonce=""))
    seen = set()
    for x in its:
        k = (x["transaction_hash"], x.get("index"), h(x["from"]), h(x["to"]), x["value"])
        if k in seen: continue
        seen.add(k)
        if not int(x["value"] or 0): continue
        rows.append(dict(kind="internal", tx=x["transaction_hash"], block=x["block_number"], ts=x["timestamp"][:19], log_index=x.get("index"),
                         frm=h(x["from"]), to=h(x["to"]), from_name=nm(x["from"]), to_name=nm(x["to"]), asset="ETH", token="", raw=int(x["value"]),
                         decimals=18, fee="", method=x.get("type") or "", status="ok" if x.get("success") else "error", nonce=""))
    for r in rows:
        r["dir"] = "out" if r["frm"] == addr else ("in" if r["to"] == addr else "other")
        r["amount"] = (r["raw"] / 10 ** r["decimals"]) if r["raw"] != "" and r["decimals"] is not None else ""
    rows.sort(key=lambda r: (r["block"], str(r["log_index"])))
    return rows

if __name__ == "__main__":
    a = sys.argv[1] if len(sys.argv) > 1 else N.B298; ch = sys.argv[2] if len(sys.argv) > 2 else "base"
    rows = ledger(a, ch)
    out = N.write_csv(N.ROOT / "data" / f"{ch}_{a.lower()[:6]}_ledger.csv", rows,
                      ["ts", "block", "tx", "kind", "dir", "frm", "from_name", "to", "to_name", "asset", "token", "amount", "raw", "decimals", "fee", "method", "status", "nonce", "log_index"])
    c = collections.Counter((r["kind"], r["dir"]) for r in rows)
    print(out, len(rows), dict(c), rows[0]["ts"], rows[-1]["ts"])
    own = [r for r in rows if r["kind"] == "tx" and r["frm"] == a.lower()]
    print("tx signées", len(own), "nonce max", max(int(r["nonce"]) for r in own if r["nonce"] is not None))
