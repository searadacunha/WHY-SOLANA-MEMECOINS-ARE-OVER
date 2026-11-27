"""Authentification on-chain des contrats cités (KLLARY, RETIREDIO, JOE, ZOOMER) : relecture indépendante, par le RPC public.

Pour KLLARY (Pump.fun), la transaction de création est relue et son événement CreateEvent décodé (nom, symbole, mint,
créateur), immuable. Pour les autres, les métadonnées Metaplex du compte PDA (nom, symbole) sont lues. Les pistes viennent
d'un agent de recherche (sources datées : Reddit 13/07/2024, Wayback CoinGecko 27/05/2024, voir FINDINGS §6) ; rien n'est
repris sans relecture ici. Sortie : data/contracts_verified.json."""
import base64
import json
from h_lib import DATA, utc
import k16_pubrpc as pub
from k12_ata import b58d, pda
from h_decode import bstr, pump_create_event

META = "metaqbxxUerdq28cj1RbAWkYQm3ybzjb6a8bt518x1s"
CAND = {"KLLARY": ("AUS4wtGQZcb6GPQxU4K8FRVqQMwUx2Q8G7K9JKuUpump", "5kGaZNhDcm7PaPFAeYhDYctpQGj5VJ6Y3nEDgxBbR9JZTimHAcFdRVmJkgwvd8VP1wnj6F2rBTgGxjvDo5MK5Chf"),
        "RETIREDIO": ("DyKwrqZMEDVHYAd4gn9V8vFioQQg1bVEgGxqbUr5Mkvo", None),
        "JOE": ("JoeXBUqpCJbaNLMTDxC6o1sLTYHsLef32ga2RDRF89m", None),
        "ZOOMER": ("9MBzpyMRkj2r5nTQZMMnxnCm5j1MAAFSYUtbSKjAF3WU", None)}


def metaplex(mint):
    acc = pda([b"metadata", b58d(META), b58d(mint)], META)
    r = pub.call("getAccountInfo", [acc, {"encoding": "base64"}])["value"]
    if not r:
        return {"metadata_account": acc, "missing": True}
    b = base64.b64decode(r["data"][0])
    name, i = bstr(b, 1 + 32 + 32)
    sym, i = bstr(b, i)
    return {"metadata_account": acc, "name": name, "symbol": sym}


if __name__ == "__main__":
    out = {}
    for tick, (mint, create_sig) in CAND.items():
        d = {"mint": mint, **metaplex(mint)}
        if create_sig:
            t = pub.tx(create_sig)
            ev = pump_create_event(t)
            d.update(create_signature=create_sig, create_slot=t["slot"], create_utc=utc(t["blockTime"]), create_event=ev,
                     event_mint_matches=bool(ev and ev["mint"] == mint))
        out[tick] = d
        print(tick, json.dumps(d, ensure_ascii=False)[:400])
    (DATA / "contracts_verified.json").write_text(json.dumps(out, indent=1, ensure_ascii=False))
