"""Trois tests demandés par l'issue #27 sur les sources de la passe 3 (docs/historical/pass3/DMAGA_PASS3_WALLET_LEADS.csv).

L02 : 9Sxm « 1.8M DMAGA → 17.875 SOL », 15 Jul 2024 09:59, fuseau inconnu. Tous les swaps de vente de 1,5 à 2,1 M
      dans le grand livre décodé (h30) entre le 14/07 19:59 et le 15/07 21:59 UTC (UTC-12 à UTC+14) ; jambe SOL brute
      versée par le pool, lue instruction par instruction.
L01 : 6QFD « 15.3M / 1.53% / $947.9K » (capture postée 22/07 12:56:22 UTC) : solde de l'ATA, transactions de l'ATA du
      21/07 au post de Noah, minutes où solde × prix du pool × SOLUSDT vaut 947,85-947,95 k$.
L03 : BARRON `HmAgiwjj…2nqZ` contre DMAGA : création (compte de métadonnées), créateur, premier financeur, présence dans
      les tables DMAGA, ATA croisées, transactions communes aux deux créateurs.
Sortie : data/pass3_tests.json."""
import csv
import json
import duckdb
from h_lib import DATA, DMAGA, DMAGA_BIG, sol_usd, utc
import k16_pubrpc as pub
from k12_ata import ata
from h_decode import movements, signers, programs
from h50_contracts import metaplex

B = str(DMAGA_BIG).replace("/data", "/data_v2")
W9SXM, W6QFD = "9Sxmf25WG5WVQ5p86ycWeo5hMEwxiWPkFtLdRdTrHSQS", "6QFDe4yu9mVhv3cbbaMtkTnakz4bGJLAjLjhwrMn5jqD"
BARRON = "HmAgiwjjP9CXqK5wQNsHKtjAt2CH3Kv8Q7xH5kGL2nqZ"
DMAGA_CREATOR = "8YLEuUtZ4eFMJbf46oNb1CeG6dYFWGyxnQSh9hrgzBzR"  # docs/CASE_REPORT.md, signature de création fePxr7ER…
RAYDIUM_AUTH = "5Q544fKrFoe6tsEbD7S8EmxGTJYAKtTVhAW5Q5pge4j1"
T_NOAH, T_VIKING = 1721653457, 1721652982


def l02():
    out = []
    for r in csv.DictReader((DATA / "ledger_9Sxm_20240713_20240725.csv").open()):
        d, t = int(r["dmaga_delta_raw"]), int(r["block_time"])
        if d < 0 and 1_500_000 * 10**6 <= -d <= 2_100_000 * 10**6 and 1720987140 <= t <= 1721080740:
            tx = pub.tx(r["signature"])
            gross = sum(m["amount"] for m in movements(tx) if m["kind"] == "token" and m["src"] == RAYDIUM_AUTH and m["mint"].startswith("So111"))
            fee_out = [(m["dst"], m["amount"]) for m in movements(tx) if m["kind"] == "token" and m["mint"].startswith("So111") and m["src"] != RAYDIUM_AUTH and m["dst"] != W9SXM]
            out.append({"signature": r["signature"], "slot": int(r["slot"]), "utc": r["utc"], "dmaga_sold": -d / 1e6, "pool_sol_gross": gross / 1e9,
                        "net_sol_to_wallet": (int(r["sol_delta_lamports"]) + int(r["wsol_delta_raw"])) / 1e9, "wsol_paid_to_third_parties": fee_out,
                        "matches_display": round(gross / 1e9, 3) == 17.875 and round(-d / 1e12, 1) == 1.8})
    return out


def l01():
    acc = ata(W6QFD, DMAGA)
    s, _ = pub.sigs(acc, max_pages=3)
    ok = sorted((x for x in s if not x.get("err")), key=lambda x: x["slot"])
    last = [x for x in ok if x["blockTime"] <= T_NOAH][-1]
    t = pub.tx(last["signature"])
    ks = [k["pubkey"] if isinstance(k, dict) else k for k in t["transaction"]["message"]["accountKeys"]]
    bal = sum(int(b["uiTokenAmount"]["amount"]) for b in t["meta"]["postTokenBalances"] if ks[b["accountIndex"]] == acc)
    from dmaga.db import connect
    con = connect(mem="400MB", threads=1)
    vd, vs = "5HuEsLbebeuottMsFW3hHcXTrKVsu3WUNSQnSr6aX4eL", "3p7DbnWekWjtMQkey6fp1emdwXbAAxecnYuD5eU9ZZPH"
    rows = con.execute(f"""WITH d AS (SELECT slot, tx_index, block_time, post FROM vault WHERE vault='{vd}' AND block_time BETWEEN 1721606400 AND {T_NOAH}),
        s AS (SELECT slot, tx_index, post FROM vault WHERE vault='{vs}' AND block_time BETWEEN 1721606400 AND {T_NOAH})
        SELECT d.block_time, (s.post/1e9)/(d.post/1e6) FROM d JOIN s USING (slot, tx_index) WHERE d.post>0 ORDER BY d.slot, d.tx_index""").fetchall()
    hits = sorted({utc(tt)[11:16] for tt, p in rows if 947_850 <= bal / 1e6 * p * sol_usd(tt) < 947_950})
    return {"ata": acc, "ata_txs_21_07_to_noah": sum(1 for x in ok if 1721520000 <= x["blockTime"] <= T_NOAH), "last_tx_before_noah": last["signature"],
            "last_tx_utc": utc(last["blockTime"]), "balance_raw": bal, "pct_supply": bal / 1e15 * 100,
            "display_15_3M_1_53pct_by_truncation": int(bal / 1e11) == 153 and int(bal / 1e13 * 100) == 153,
            "minutes_22_07_until_noah_where_value_is_947_9K": hits, "swaps_scanned": len(rows)}


def l03():
    meta = metaplex(BARRON)
    s, _ = pub.sigs(meta["metadata_account"], max_pages=2)
    first = min(s, key=lambda x: x["slot"])
    t = pub.tx(first["signature"])
    creator = signers(t)[0]
    cs, ctr = pub.sigs(creator, max_pages=10)
    ds, dtr = pub.sigs(DMAGA_CREATOR, max_pages=10)
    f0 = sorted((x for x in cs if not x.get("err")), key=lambda x: x["slot"])[0]
    funders = [(m["src"], m["amount"]) for m in movements(pub.tx(f0["signature"])) if m["dst"] == creator and m["kind"] == "sol"]
    con = duckdb.connect(config={"memory_limit": "300MB", "threads": 1})
    in_tables = {n: con.execute(q).fetchall()[0][0] for n, q in (
        ("trades", f"select count(*) from '{B}/trades.parquet' where owner='{creator}'"),
        ("funding_edges", f"select count(*) from '{B}/funding_edges.parquet' where src in ('{creator}','{funders[0][0]}') or wallet='{creator}'"),
        ("exit_flows", f"select count(*) from '{B}/exit_flows.parquet' where dst in ('{creator}','{funders[0][0]}') or wallet='{creator}'"),
        ("token_edges", f"select count(*) from '{B}/token_edges.parquet' where src='{creator}' or dst='{creator}'"))}
    common = sorted({x["signature"] for x in cs} & {x["signature"] for x in ds})
    common_moves = []
    for sg in common:
        mv = movements(pub.tx(sg))
        common_moves.append({"signature": sg, "moves_touching_creators": sum(1 for m in mv if {m["src"], m["dst"]} & {creator, DMAGA_CREATOR}),
                             "signers": signers(pub.tx(sg))})
    return {"mint": BARRON, "metadata": meta, "create_signature": first["signature"], "create_utc": utc(t["blockTime"]), "create_programs": programs(t),
            "creator": creator, "creator_signatures": len(cs), "creator_sigs_truncated": ctr, "dmaga_creator_signatures": len(ds),
            "creator_first_funding": {"signature": f0["signature"], "utc": utc(f0["blockTime"]), "funders": funders},
            "creator_and_first_funder_in_dmaga_tables": in_tables,
            "creator_dmaga_ata_sigs": len(pub.sigs(ata(creator, DMAGA), max_pages=1)[0]),
            "dmaga_creator_barron_ata_sigs": len(pub.sigs(ata(DMAGA_CREATOR, BARRON), max_pages=1)[0]),
            "transactions_common_to_both_creators": common_moves}


if __name__ == "__main__":
    res = {"L02_9Sxm_1_8M": l02(), "L01_6QFD": l01(), "L03_BARRON": l03()}
    (DATA / "pass3_tests.json").write_text(json.dumps(res, indent=1, ensure_ascii=False))
    print(json.dumps(res, indent=1, ensure_ascii=False)[:3000])
