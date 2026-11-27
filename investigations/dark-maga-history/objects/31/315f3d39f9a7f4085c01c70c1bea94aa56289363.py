"""Frontière entre les deux bornes du 12/11/2024 : dépôt Coinbase de b298 sur Base (24 ETH, via o1) et dépôt MEXC Solana
(via o2). Le relais détient au pire 100 000,011 USDC non marqués (s15) ; on les place en fraction f dans son envoi de 17:40:23
(qui paie o2) et 1 - f dans celui de 01:42:47 (qui paie o1). Pour chaque f, scénario S* de s15 (o1 et o2 puisent d'abord dans
le non-marqué), puis bornes en aval : s60 (Base, 24 ETH) et s16 (chaîne MEXC, prorata et strict). Aucun appel réseau.
Sortie : evidence/s17_joint_destinations.csv"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
import nt_lib as N
import s15_relay_bounds as S15, s16_mexc_chain_bound as S16, s60_positions as P

CB_TX = "0x52da33cb31aa36ecce1a05774dd7bc69bed8d0a9b555db97e8659771a4a00245"   # 24 ETH vers le dépôt Coinbase
FILL1 = "0xf130eea66394f17d0e48bb7cf88926178504a1c9735fc659c673457e1882e996"  # exécution Base de o1

def frontier(steps=(0, 25, 50, 75, 100)):
    R2 = S15.b298_events(); RR = S15.relay_events()
    rep = S15.low(R2, S15.s51_taint)
    rel_taint = lambda r: int(r["amount_raw"]) if r["counterparty"] == N.B947 else (rep.get(r["tx_hash"].lower(), (0, 0))[1] if r["counterparty"] == N.B298 else 0)
    C = sum(int(r["amount_raw"]) - rel_taint(r) for r in RR if r["direction"] == "IN")
    k1 = next(r["tx_hash"].lower() for r in RR if r["tx_hash"].startswith("0x6a7e85b547"))
    k2 = next(r["tx_hash"].lower() for r in RR if r["tx_hash"].startswith("0xd6162abed8"))
    ledger = P.rd(N.ROOT / "data/base_0xb298_ledger.csv"); txs = P.per_tx(ledger, N.B298); taint = P.fill_taint()
    t_first = min(t["ts"] for t in txs if t["tx"] in taint)
    rows = []
    for pct in steps:
        c2 = C * pct // 100; a = {k1: C - c2, k2: c2}
        s = S15.low(R2, S15.relay_split(R2, a), first_clean={S15.O1, S15.O2})
        m1, m2 = s[S15.O1][1], s[S15.O2][1]
        t1 = dict(taint); mn, mx, den, etx = t1[FILL1]; t1[FILL1] = (m1, mx, s[S15.O1][0], etx)
        res, _ = P.run(txs, t1, t_first)
        cb = next(t for t in res if t["tx"] == CB_TX)["res"][P.ETH][1]
        mx_p = S16.chain(m2, strict=False)["marked_deposit_usdc_min"]; mx_s = S16.chain(m2, strict=True)["marked_deposit_usdc_min"]
        rows.append(dict(relay_unmarked_to_o2_pct=pct, o1_marked_usdc=m1 / 1e6, o2_marked_usdc=m2 / 1e6, coinbase_24eth_marked_min_eth=cb / 1e18,
                         mexc_deposit_marked_min_usdc_prorata=round(mx_p, 6), mexc_deposit_marked_min_usdc_strict=round(mx_s, 6)))
    return rows

def zero_thresholds():
    """Plus grand marquage de o1 (resp. o2), en unités brutes, qui laisse nulle la borne Coinbase (resp. MEXC), par dichotomie.
    Si leur somme est inférieure à la borne commune de s15, les deux bornes ne peuvent pas être nulles ensemble."""
    ledger = P.rd(N.ROOT / "data/base_0xb298_ledger.csv"); txs = P.per_tx(ledger, N.B298); taint = P.fill_taint()
    t_first = min(t["ts"] for t in txs if t["tx"] in taint); mn, mx, den, etx = taint[FILL1]
    def cb(m1):
        t1 = dict(taint); t1[FILL1] = (m1, mx, den, etx); res, _ = P.run(txs, t1, t_first)
        return next(t for t in res if t["tx"] == CB_TX)["res"][P.ETH][1]
    def last_zero(f, hi):
        lo = 0
        while hi - lo > 1:
            mid = (lo + hi) // 2
            if f(mid) == 0: lo = mid
            else: hi = mid
        return lo
    z1 = last_zero(cb, den)
    z2 = last_zero(lambda m2: S16.chain(m2, strict=True)["marked_deposit_usdc_min"], 99989828367)
    return z1, z2

if __name__ == "__main__":
    rows = frontier()
    z1, z2 = zero_thresholds(); print(f'seuils de nullité : o1 <= {z1 / 1e6:,.6f}, o2 <= {z2 / 1e6:,.6f} USDC (somme {(z1 + z2) / 1e6:,.6f})')
    N.write_csv(N.ROOT / "evidence/s17_joint_destinations.csv", rows)
    for r in rows:
        print(f"{r['relay_unmarked_to_o2_pct']:3d} % vers o2 : o1 {r['o1_marked_usdc']:>12,.2f} | o2 {r['o2_marked_usdc']:>12,.2f} USDC -> Coinbase >= {r['coinbase_24eth_marked_min_eth']:.4f} ETH ; MEXC >= {r['mexc_deposit_marked_min_usdc_prorata']:>11,.2f} (strict {r['mexc_deposit_marked_min_usdc_strict']:>11,.2f}) USDC")
