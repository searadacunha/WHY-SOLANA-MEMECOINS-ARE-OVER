"""Correction des bornes USDC de b298 sur Ethereum (s51 du dossier précédent) : le relais 0x4978cd7e n'est pas un conduit pur de b947.

s51 compte toute entrée venue du relais comme 100 % b947. Or b298 renvoie 100 000 USDC au relais le 06/10/2024 19:28:35
(0x6407f6bc…), et s51 donne lui-même 0 comme borne basse de la part b947 de ce renvoi : au pire cas, le relais détient
ensuite 100 000 USDC non marqués, qu'il peut rendre à b298 dans n'importe laquelle de ses sorties suivantes.

Ce script, sans réseau, sur les historiques publiés du dossier précédent (b298_full_history.csv, relay_4978_history.csv) :
1. rejoue la règle H de la première version de s51 (relais = b947) : 31 bornes, 472 143,22 USDC de bornes basses en tout. s51 a été
   corrigé le 06/11 (relais tracé) : ses bornes publiées doivent égaler celles de l'étape 2, calculées ici par un second code ;
2. applique la même règle au relais (entrée de b298 marquée à sa borne basse), puis reporte les bornes du relais sur
   ses envois à b298 : bornes de chaque sortie prise seule (pire cas propre à cette sortie) ;
3. borne commune aux deux ordres du 12/11/2024 (o1 = 0x4b7c7a2f vers Base, o2 = 0xca823779 vers BSC) : scénario S* où o1 et o2
   puisent d'abord dans le non-marqué et toutes les autres sorties d'abord dans le marqué, l'argent non marqué du relais étant
   placé de toutes les façons possibles entre ses sorties (pas de 1 %). Le minimum de marqué(o1) + marqué(o2) est la borne commune.
Sortie : evidence/s15_relay_bounds.csv et evidence/s15_joint_bound.json"""
import csv, json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
import nt_lib as N

USDC = "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48"
B947, RELAY, B298 = N.B947, N.RELAY, N.B298
O1 = "0x4b7c7a2fcda576c58c961dee9d35840fba0151a9156cc0c48a0282c2fb024e16"
O2 = "0xca82377984453a77f40592a694c5ad4c8076acce66b64a25e7c43f119f3cf8a4"
EV = N.PREV / "evidence"

def rd(p): return list(csv.DictReader(open(p)))

def b298_events():
    R = [r for r in rd(EV / "b298_full_history.csv") if r["asset"] == "USDC"
         and (not r["flags"] or (r["flags"] == "lookalike" and r["direction"] == "IN"))]  # même filtre que s51
    R.sort(key=lambda r: (r["timestamp_utc"], int(r["log_index"])))
    return R

def relay_events():
    R = [r for r in rd(EV / "relay_4978_history.csv") if r["kind"] == "erc20" and r["token_contract"].lower() == USDC and int(r["amount_raw"]) > 0]
    R.sort(key=lambda r: (r["timestamp_utc"], int(r["log_index"])))
    return R

def low(R, taint_of, first_clean=()):
    """Scénario bas de s51, généralisé : une entrée porte taint_of(r) unités marquées (borne basse) ; chaque sortie puise d'abord
    dans le marqué, sauf celles de first_clean qui puisent d'abord dans le non-marqué. Rend {tx: (x, borne basse)}."""
    T = C = 0; out = {}
    for r in R:
        x = int(r["amount_raw"])
        if r["direction"] == "IN":
            t = taint_of(r); T += t; C += x - t; continue
        tx = r["tx_hash"].lower()
        if tx in first_clean:
            c = min(x, max(0, C)); C -= c; T -= x - c; out[tx] = (x, x - c)
        else:
            out[tx] = (x, max(0, x - max(0, C)))
            t = min(x, max(0, T)); T -= t; C -= x - t
    return out

def s51_taint(r):
    return int(r["amount_raw"]) if r["counterparty"] in (B947, RELAY) and r["timestamp_utc"] >= "2024-10-01" else 0

def relay_split(R2, clean_by_tx):
    """Entrées du relais dans b298 : marquées = montant - part non marquée attribuée à cette sortie du relais."""
    def f(r):
        if r["counterparty"] == RELAY and r["timestamp_utc"] >= "2024-10-01":
            return int(r["amount_raw"]) - clean_by_tx.get(r["tx_hash"].lower(), 0)
        return s51_taint(r)
    return f

if __name__ == "__main__":
    R2 = b298_events(); RR = relay_events()
    # 1. règle H (première version de s51) ; s51 publie désormais les bornes avec le relais tracé
    pubr = rd(EV / "s51_b298_usdc_bounds.csv")
    pub = {r["tx_hash"].lower(): int(round(float(r["from_b947_min"]) * 10 ** 6)) for r in pubr}
    rep = low(R2, s51_taint)
    assert len(pub) == 31 and sum(rep[tx][1] for tx in pub) == 472143218089, "règle H non reproduite"
    print(f"1. règle H (relais = b947) : {len(pub)} sorties, bornes basses sommées {sum(rep[tx][1] for tx in pub) / 1e6:,.6f} USDC")
    # 2. le relais, même règle : entrées de b947 marquées, renvoi de b298 marqué à sa borne basse s51 (0)
    rel_taint = lambda r: int(r["amount_raw"]) if r["counterparty"] == B947 else (rep.get(r["tx_hash"].lower(), (0, 0))[1] if r["counterparty"] == B298 else 0)
    rel = low(RR, rel_taint)
    ins = [r for r in RR if r["direction"] == "IN"]
    C_relay = sum(int(r["amount_raw"]) - rel_taint(r) for r in ins)
    print(f"2. relais : {len(RR)} transferts USDC réels, non-marqué possible {C_relay / 1e6:,.6f} USDC")
    outs_rel = [r for r in RR if r["direction"] == "OUT"]
    clean_rel = {r["tx_hash"].lower(): int(r["amount_raw"]) - rel[r["tx_hash"].lower()][1] for r in outs_rel}
    corr = low(R2, relay_split(R2, clean_rel))  # chaque envoi du relais à son propre pire cas : bornes individuelles
    diff = [tx for tx, v in pub.items() if abs(corr[tx][1] - v) > 1]
    assert not diff, f"s51 corrigé (dossier précédent) et ce calcul divergent : {diff[:3]}"
    print(f"   s51 corrigé = relais tracé ici : {len(pub)}/{len(pub)} bornes basses (écart <= 1e-6 USDC)")
    rows = []
    for r in outs_rel:
        tx = r["tx_hash"].lower(); x, lo = rel[tx]
        rows.append(dict(utc=r["timestamp_utc"], tx=tx, wallet="relay", amount=x / 1e6, from_b947_min=lo / 1e6, under_H=x / 1e6))
    for tx in (O1, O2):
        x = corr[tx][0]
        rows.append(dict(utc="2024-11-12", tx=tx, wallet="b298", amount=x / 1e6, from_b947_min=corr[tx][1] / 1e6, under_H=rep[tx][1] / 1e6))
    N.write_csv(N.ROOT / "evidence/s15_relay_bounds.csv", rows)
    N.write_csv(N.ROOT / "evidence/s15_s51_corrected.csv", [dict(utc=r["utc"], tx_hash=r["tx_hash"], amount=r["amount"], dln_dest=r["dln_dest"],
                label=r["label"][:40], from_b947_min_under_H=rep[r["tx_hash"].lower()][1] / 1e6, from_b947_min_relay_traced=corr[r["tx_hash"].lower()][1] / 1e6) for r in pubr])
    for r in rows[-2:]: print(f"   ordre {r['tx'][:10]} : {r['amount']:,.6f} USDC, borne basse seule {r['from_b947_min']:,.6f} (sous H : {r['under_H']:,.6f})")
    # 3. borne commune : non-marqué du relais réparti entre ses sorties vers b298, o1 et o2 puisant d'abord dans le non-marqué
    t_in = max(r["timestamp_utc"] for r in ins if r["counterparty"] == B298)   # le non-marqué n'existe qu'après le renvoi de b298
    after = [r for r in outs_rel if r["timestamp_utc"] > t_in]
    T1 = "0x6a7e85b547"; T2 = "0xd6162abed8"
    k1 = next(r["tx_hash"].lower() for r in after if r["tx_hash"].startswith(T1)); k2 = next(r["tx_hash"].lower() for r in after if r["tx_hash"].startswith(T2))
    early = [r["tx_hash"].lower() for r in after if r["timestamp_utc"] < "2024-11-12"]
    caps = {r["tx_hash"].lower(): int(r["amount_raw"]) for r in outs_rel}
    best = None; step = C_relay // 100
    for i in range(101):
        for j in range(101 - i):
            c1, c2 = min(i * step, caps[k1]), min(j * step, caps[k2]); left = C_relay - c1 - c2; a = {k1: c1, k2: c2}
            for e in early:
                t = min(left, caps[e]); a[e] = t; left -= t
            if left > 0: a[k1] += left  # reste (arrondi) : dans la sortie de 01:42, déjà plafonnée à 200 000
            s = low(R2, relay_split(R2, a), first_clean={O1, O2})
            tot = s[O1][1] + s[O2][1]
            if best is None or tot < best[0]: best = (tot, s[O1][1], s[O2][1], {k[:10]: v / 1e6 for k, v in a.items() if v})
    J = dict(orders=[O1, O2], amounts=[corr[O1][0] / 1e6, corr[O2][0] / 1e6], joint_min_from_b947=best[0] / 1e6,
             at_allocation=best[3], o1_marked=best[1] / 1e6, o2_marked=best[2] / 1e6, relay_unmarked_max=C_relay / 1e6,
             under_H_individual=[rep[O1][1] / 1e6, rep[O2][1] / 1e6], corrected_individual=[corr[O1][1] / 1e6, corr[O2][1] / 1e6])
    (N.ROOT / "evidence/s15_joint_bound.json").write_text(json.dumps(J, indent=1) + "\n")
    print(f"3. borne commune : marqué(o1) + marqué(o2) >= {best[0] / 1e6:,.6f} USDC, atteinte avec {best[3]} (o1 {best[1] / 1e6:,.6f}, o2 {best[2] / 1e6:,.6f})")
