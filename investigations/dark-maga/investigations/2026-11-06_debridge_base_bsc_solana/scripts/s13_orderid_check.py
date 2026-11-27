"""Offline reconciliation of CROSSCHAIN_LINKS against published evidence.

Recompute exact DLN order IDs from successful EVM events, bind both chain and
transaction fields, and replay published Solana executions. A source absent
from Solana fixtures must match the published deBridge index and is reported
as index-only, never as a raw receipt. Default is read-only; --output exports
the recomputed EVM events to a chosen CSV. A failed check exits nonzero.
"""
import argparse, csv, json, sys, os, collections, re
from pathlib import Path
sys.path.insert(0, os.path.dirname(__file__))
import nt_lib as N
import dln as D
import dln_orderid as O
import sol_dln as S

SRC = {"0xef4fb24ad0916217251f553c0596f8edc630eb66"}
DST = {"0xe7351fd770a37282b91d153ee690b63579d6dd7f"}
CHAIN_IDS = {name: number for number, name in D.CHAINS.items()}
HASH = re.compile(r"0x[0-9a-fA-F]{64}\Z")
# This one historical source receipt was not published. Do not silently
# downgrade any of the other raw-receipt checks to index-only coverage.
INDEX_ONLY_SOURCES = {"0xd7d6f9b4b6645aa063fb5578abda7eeb1b696c2ae93bac7d6e5dfc4b54b678b3"}

def require(condition, message):
    if not condition:
        raise ValueError(message)

def read_csv(path):
    with open(path, newline="") as handle:
        return list(csv.DictReader(handle))

def request_chain(request):
    """Network comes from recorded RPC provenance, not just the event's fields."""
    origin = request.split(" ", 1)[0]
    origins = {"base": 8453, "bsc": 56, "ethereum": 1,
               "https://ethereum-rpc.publicnode.com": 1,
               "https://base.drpc.org": 8453, "https://56.rpc.thirdweb.com": 56,
               "https://bsc-mainnet.gateway.tatum.io": 56}
    require(origin in origins, "Missing or unknown chain provenance for cached receipt")
    return origins[origin]

def receipts():
    """Read local caches only; conflicting copies of one receipt are an error."""
    roots = [N.FIXTURES, N.NEW_RAW] + [d for r in N.RAW_RO for d in (r / "cache", r)]
    seen = {}
    for root in roots:
        if not root.is_dir(): continue
        requests = {}
        if root == N.FIXTURES:
            manifest = json.loads((root.parent / "MANIFEST.json").read_text())
            requests = {Path(path).stem: info["request"] for path, info in manifest["cache"].items()}
        else:
            for ledger in (root / "ledger.jsonl", root.parent / "ledger.jsonl"):
                if ledger.is_file():
                    for line in ledger.read_text().splitlines():
                        entry = json.loads(line)
                        requests[entry["key"]] = entry["url"]
        for p in sorted(root.glob("[0-9a-f][0-9a-f]/*.json")):
            d = json.loads(p.read_bytes())
            res = d.get("result") if isinstance(d, dict) else None
            items = [x.get("result") for x in d] if isinstance(d, list) else [res]
            for r in items:
                if isinstance(r, dict) and "logs" in r and "transactionHash" in r:
                    tx = r["transactionHash"].lower()
                    chain = request_chain(requests.get(p.stem, ""))
                    identity = (chain, tx)
                    if identity in seen:
                        for field in ("status", "blockHash", "blockNumber", "logs"):
                            require(seen[identity].get(field) == r.get(field), f"Conflicting cached receipt: {chain}:{tx}")
                    else:
                        # Annotate a copy in memory; archived JSON stays untouched.
                        seen[identity] = dict(r, _evidence_chain_id=chain)
    return seen

def check(rc):
    out = []
    for l in D.receipt_logs(rc):
        a = l["address"].lower()
        topic = (l.get("topics") or [""])[0].lower()
        created = a in SRC and topic == D.CREATED_ORDER
        version = D.fulfilled_version(l) if a in DST else 0
        if not created and not version: continue
        require(len(l["topics"]) == 1, "Unexpected indexed fields in DLN event")
        o, emitted = D.raw_order(l["data"], 7 if created else 3 + version)
        chain = o["giveChainId"] if created else o["takeChainId"]
        require(rc.get("_evidence_chain_id", chain) == chain, "Order event does not match receipt chain provenance")
        ok = O.order_id(o) == emitted
        ok_h = (not ok) and len(o["externalCall"]) == 32 and "0x" + O.keccak256(O.encode_order(o, True)).hex() == emitted
        out.append(dict(tx=rc["transactionHash"].lower(), logIndex=int(l["logIndex"], 16), contract="DlnSource" if created else "DlnDestination",
                        chainId=chain,
                        topic0=topic, orderId=emitted, recomputed_ok=ok or ok_h, external_call_hash_variant=ok_h,
                        makerSrc=D.addr_str(o["giveChainId"], o["makerSrc"]), giveChainId=o["giveChainId"], giveAmount=o["giveAmount"],
                        giveTokenAddress=D.addr_str(o["giveChainId"], o["giveTokenAddress"]),
                        takeTokenAddress=D.addr_str(o["takeChainId"], o["takeTokenAddress"]),
                        takeChainId=o["takeChainId"], takeAmount=o["takeAmount"], receiverDst=D.addr_str(o["takeChainId"], o["receiverDst"]),
                        tx_status=rc.get("status"), block=int(rc["blockNumber"], 16)))
    return out

def solana_receipts():
    out = {}
    for path in sorted((N.ROOT / "evidence/fixtures/sol").glob("*.jsonl")):
        for line in path.read_text().splitlines():
            tx = json.loads(line)
            sig = tx["transaction"]["signatures"][0]
            require(sig not in out or out[sig] == tx, f"Conflicting Solana receipt: {sig}")
            out[sig] = tx
    return out


def same_address(a, b, chain):
    # Solana base58 is case-sensitive; only hexadecimal EVM addresses fold case.
    return a == b if chain == "solana" else a.lower() == b.lower()


def fields_match(link, event):
    return (event["giveChainId"] == CHAIN_IDS.get(link["src_chain"])
            and event["takeChainId"] == CHAIN_IDS.get(link["dst_chain"])
            and same_address(event["makerSrc"], link["maker"], link["src_chain"])
            and same_address(event["receiverDst"], link["receiver"], link["dst_chain"])
            and same_address(event["giveTokenAddress"], link["give_token"], link["src_chain"])
            and same_address(event["takeTokenAddress"], link["take_token"], link["dst_chain"])
            and str(event["giveAmount"]) == link["give_amount_raw"]
            and str(event["takeAmount"]) == link["take_amount_raw"])


def indexed_source(link, index):
    """An index entry binds a missing source signature, not a raw Solana receipt."""
    for row in index:
        if row["order_id"].lower() != link["orderId"].lower():
            continue
        if (row["create_tx"] == link["src_tx"] and row["fulfil_tx"].lower() == link["dst_tx"].lower()
                and row["give_chain"] == str(CHAIN_IDS[link["src_chain"]])
                and row["take_chain"] == str(CHAIN_IDS[link["dst_chain"]])
                and same_address(row["maker"], link["maker"], link["src_chain"])
                and same_address(row["receiver"], link["receiver"], link["dst_chain"])
                and same_address(row["give_token"], link["give_token"], link["src_chain"])
                and same_address(row["take_token"], link["take_token"], link["dst_chain"])
                and row["give_amount"] == link["give_amount_raw"]
                and row["take_amount"] == link["take_amount_raw"]):
            return True
    return False


def solana_amount(tx, wallet, mint):
    meta = tx["meta"]
    keys = [key["pubkey"] if isinstance(key, dict) else key
            for key in tx["transaction"]["message"]["accountKeys"]]
    loaded = meta.get("loadedAddresses") or {}
    keys += loaded.get("writable", []) + loaded.get("readonly", [])
    if mint == "11111111111111111111111111111111":
        require(wallet in keys, "Solana recipient absent from receipt")
        i = keys.index(wallet)
        return meta["postBalances"][i] - meta["preBalances"][i]
    return sum(sign * int(row["uiTokenAmount"]["amount"])
               for field, sign in (("preTokenBalances", -1), ("postTokenBalances", 1))
               for row in meta.get(field) or [] if row.get("owner") == wallet and row["mint"] == mint)


def validate_links(links, events, solana=None, index=None):
    """Validate every supplied assertion; return explicit evidence coverage."""
    require(bool(links), "Empty cross-chain table")
    solana = solana_receipts() if solana is None else solana
    index = read_csv(N.DEB_RECEIVERS) if index is None else index
    by_order, event_ids, seen = collections.defaultdict(list), set(), set()
    for event in events:
        require(event["recomputed_ok"] and event["tx_status"] == "0x1", "Unauthenticated EVM order")
        identity = (event["chainId"], event["tx"], event["logIndex"])
        require(identity not in event_ids, "Duplicate EVM event identity")
        event_ids.add(identity)
        by_order[event["orderId"].lower()].append(event)
    coverage = collections.Counter(links=len(links))
    for link in links:
        oid = link["orderId"].lower()
        require(bool(HASH.fullmatch(oid)), "Invalid orderId")
        require(oid not in seen, f"Duplicate cross-chain order: {oid}")
        seen.add(oid)
        require(link["level"] == "VERIFIED", f"Unverified link: {oid}")
        matched = by_order.get(oid, [])
        require(bool(matched) and all(fields_match(link, event) for event in matched),
                f"Order fields mismatch: {oid}")
        for side, contract, program in (("src", "DlnSource", S.SOURCE), ("dst", "DlnDestination", S.DESTINATION)):
            chain, txid = link[side + "_chain"], link[side + "_tx"]
            if chain != "solana":
                require(bool(HASH.fullmatch(txid)), f"Invalid {side} transaction hash: {oid}")
                hits = [event for event in matched if event["contract"] == contract
                        and event["chainId"] == CHAIN_IDS[chain] and event["tx"] == txid.lower()]
                require(len(hits) == 1, f"Missing or ambiguous {side} EVM event: {oid}")
                coverage[side + "_evm_receipts"] += 1
                continue
            tx = solana.get(txid)
            if tx is None:
                require(side == "src" and oid in INDEX_ONLY_SOURCES and indexed_source(link, index),
                        f"Missing {side} Solana evidence: {oid}")
                coverage["src_solana_index_only"] += 1
                continue
            require(tx["transaction"]["signatures"][0] == txid, f"Wrong {side} Solana receipt: {oid}")
            require(oid in S.order_ids(tx, program), f"Missing successful {side} Solana order event: {oid}")
            if side == "dst":
                require(solana_amount(tx, link["receiver"], link["take_token"]) == int(link["take_amount_raw"]),
                        f"Solana destination amount mismatch: {oid}")
            coverage[side + "_solana_receipts"] += 1
    return dict(coverage)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, help="explicit CSV destination; no file is written by default")
    args = parser.parse_args()
    try:
        cached = receipts()
        events = [event for receipt in cached.values() for event in check(receipt)]
        coverage = validate_links(read_csv(N.ROOT / "CROSSCHAIN_LINKS.csv"), events)
        if args.output:
            N.write_csv(args.output, sorted(events, key=lambda e: (e["chainId"], e["block"], e["tx"], e["logIndex"])))
        print(json.dumps(dict(evm_receipts=len(cached), evm_events=len(events), coverage=coverage), sort_keys=True))
    except (ValueError, KeyError, TypeError, OSError) as error:
        print(f"Validation failed: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
