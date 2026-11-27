"""BSC_FLOWS.csv : chaque changement d'état de b298 sur BSC (dichotomie s20, complète pour nonce, BNB, USDT, USDC, ETH, WBNB, BUSD),
horodaté, avec les tx et journaux du bloc quand s23 les a lus, et les deux ordres DLN du 12/11/2024 décodés (s21)."""
import csv, json, datetime as dt, sys, os
sys.path.insert(0, os.path.dirname(__file__))
import nt_lib as N
R = N.ROOT; a = N.B298
ch = list(csv.DictReader(open(R / "data/bsc_0xb298_state_changes.csv")))
ts = json.load(open(R / "data/bsc_0xb298_block_ts.json"))
det = json.load(open(R / "data/bsc_0xb298_block_details.json")) if (R / "data/bsc_0xb298_block_details.json").exists() else {}
DLN = {43950886: ("dln_fill_in", "0x549e4bc55eb2310b903f087d439b16af35c9d4c17624873012443c4eb6730afe", "0xc62af9cf7ef4814f579a97750dfbcb8f51a383377fda39423dcd8514957d51d2",
                  "ordre Ethereum 0xca82377984453a77f40592a694c5ad4c8076acce66b64a25e7c43f119f3cf8a4 : 99 949,832436 USDC donnés, 157,374799465747581520 BNB livrés à b298"),
       43951101: ("swap_and_dln_order_out", "0x76ffdad7e00a284fc1041b7c045319741bac650d4fdf7d1767524ddad2204f6c", "0x5c2e547ffa26cbc17ddc5650d2346cbd23155c8734d0e6d08fb929a84b36285e",
                  "BNB échangés en ETH BEP-20 dans la même tx, ordre de 29,869509697174994316 ETH vers b298 sur Ethereum (fill 0xf9b44d3ac32c0ad76280d57f31277844e6b5384ec399b7509b287668e128b3cf, 29,845089109620802062 ETH)")}
rows = []
for r in ch:
    b = int(r["block"]); d = det.get(str(b))
    txs = [t["hash"] for t in (d or {}).get("txs", [])]
    cps = sorted({(t.get("to") if (t.get("from") or "").lower() == a else t.get("from")) or "" for t in (d or {}).get("txs", [])} |
                 {"0x" + l["topics"][1][26:] if l["topics"][2][26:] == a[2:] else "0x" + l["topics"][2][26:] for l in (d or {}).get("logs", []) if len(l["topics"]) > 2})
    cat, tx, oid, note = DLN.get(b, ("", "", "", ""))
    if not cat:
        cat = "tx_signed" if int(r["d_nonce"]) else ("inflow_native" if int(r["d_native"]) > 0 else ("inflow_token" if any(int(r[k]) > 0 for k in r if k.startswith("d_") and k not in ("d_nonce", "d_native")) else "other"))
    rows.append(dict(chain="bsc", wallet=a, utc=dt.datetime.fromtimestamp(ts[str(b)], dt.timezone.utc).strftime("%Y-%m-%d %H:%M:%S"), block=b,
                     period="DMAGA (2024-07 → 2024-12)" if 43000000 <= b <= 45000000 else ("avant DMAGA" if b < 43000000 else "après"),
                     category=cat, nonce_delta=r["d_nonce"], bnb_delta=int(r["d_native"]) / 1e18, usdt_delta=int(r["d_USDT"]) / 1e18, usdc_delta=int(r["d_USDC"]) / 1e18,
                     eth_bep20_delta=int(r["d_ETH"]) / 1e18, wbnb_delta=int(r["d_WBNB"]) / 1e18, busd_delta=int(r["d_BUSD"]) / 1e18,
                     tx=tx or " ".join(txs), dln_orderId=oid, counterparties=" ".join(c for c in cps if c and c.lower() != a),
                     details_read="oui" if d is not None or tx else "non (bloc seul ; voir UNRESOLVED)", note=note))
N.write_csv(R / "BSC_FLOWS.csv", rows)
print(len(rows), "lignes ;", sum(1 for r in rows if r["details_read"] == "oui"), "avec détail ;", sum(1 for r in rows if r["period"].startswith("DMAGA")), "dans la fenêtre DMAGA")
