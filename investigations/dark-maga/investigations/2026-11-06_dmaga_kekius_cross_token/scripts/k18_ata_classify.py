"""Classe les couples (adresse DMAGA, mint Kekius) actifs du test ATA, puis relit au niveau transaction les candidats.

Classes, dans l'ordre :
- service : étiquette du projet (dmaga.labels) ;
- haute_frequence : plus de 1 000 signatures sur l'ATA, ou plus de 100 dans la fenêtre, ou plus de 50 opérations DMAGA ;
- faible_activite : le reste, sauf si le wallet entier fait au moins 200 tx dans les 24 h avant son premier mouvement Kekius de
  la fenêtre (une page getSignaturesForAddress) : il passe alors en haute_frequence (wallet). Pour les couples restants, chaque transaction de l'ATA jusqu'au 31/01/2025 est relue (RPC public, cache)
  et le mouvement du propriétaire est calculé : achat (jeton +, SOL ou WSOL −), vente, ou entrée et sortie sans contrepartie.
Sorties : data/ata_scan_summary.csv (tous les couples testés, sans signatures) et data/ata_overlap.csv (couples actifs dans
la fenêtre, au format de WALLET_OVERLAP.csv). Option --no-fetch : classement sans relecture."""
import csv, json, sys
import duckdb
from k_lib import DATA, DMAGA_BIG, KM, XC, WSOL, utc
from k11_parse import token_deltas, sol_deltas, signers
from dmaga import labels

T_MUSK, T_END, T_LATE = 1735624921, 1735948800, 1738368000  # 31/12 06:02:01 ; 04/01 ; 01/02/2025
CREATED = {"KM": 1733815740, "XC": 1735490025}
MINT = {"KM": KM, "XC": XC}
fetch = "--no-fetch" not in sys.argv

recs = {}
for f in ("ata_scan.jsonl", "ata_scan_h.jsonl"):
    p = DATA / f
    if p.exists():
        for l in open(p):
            r = json.loads(l)
            recs[(r["owner"], r["token"])] = r
tags = {r["address"]: r["tags"] for r in csv.DictReader(open(DATA / "dmaga_universe.csv"))}
core = {}
for r in csv.DictReader(open(DATA / "core_set.csv")):
    core.setdefault(r["address"], r["role"] + (f" (via {r['via'][:8]}…)" if r["via"] else ""))
ops = dict(((o, n) for o, n in duckdb.sql(f"select owner, n_buys + n_sells from '{DMAGA_BIG}/wallets.parquet'").fetchall()))
first_dmaga = dict(duckdb.sql(f"select owner, first_buy_time from '{DMAGA_BIG}/wallets.parquet'").fetchall())


def moves(owner, tk, sigs):
    import k16_pubrpc as pub
    out = []
    for s, bt, err in sigs:
        if err or bt is None or bt > T_LATE:
            continue
        t = pub.tx(s)
        if t["meta"]["err"]:
            continue
        d = token_deltas(t, MINT[tk]).get(owner, 0)
        if not d:
            continue
        sol = sol_deltas(t).get(owner, 0) if owner in signers(t) else 0
        w = token_deltas(t, WSOL).get(owner, 0)
        kind = "achat" if d > 0 and (sol + w) < -5_000_000 else "vente" if d < 0 and (sol + w) > 0 else "entrée" if d > 0 else "sortie"
        out.append({"sig": s, "t": t["blockTime"], "tok": d, "sol": sol + w, "kind": kind})
    return out


summ, ov = [], []
for (a, tk), r in sorted(recs.items()):
    ok = [x for x in r["sigs"] if not x[2] and x[1]]
    first = min((x[1] for x in ok), default=None)
    win = [x for x in ok if CREATED[tk] <= x[1] < T_END]
    pre = [x for x in ok if CREATED[tk] <= x[1] < T_MUSK]
    lab = labels.label(a)
    cls = ("inactif" if not ok else "service" if lab else
           "haute_frequence" if r["n"] >= 1000 or r.get("more") or len(win) > 100 or ops.get(a, 0) > 50 else "faible_activite")
    summ.append([a, tk, r["ata"], r["n"], utc(first) if first else "", len(win), len(pre), cls, tags.get(a, ""), r.get("src", "helius-gtfa")])
    if not win or cls == "inactif":
        continue
    detail, status, interp = "", "CONFIRMÉ", ""
    if cls == "faible_activite" and fetch:
        import k16_pubrpc as pub
        w0 = min(win, key=lambda x: x[1])
        before = pub.call("getSignaturesForAddress", [a, {"limit": 1000, "before": w0[0]}])
        n24 = sum(1 for x in before if x.get("blockTime") and w0[1] - 86400 <= x["blockTime"] < w0[1])
        if n24 >= 200:
            cls = "haute_frequence"
            summ[-1][7] = "haute_frequence_wallet"
            detail = f"{n24} tx du wallet dans les 24 h avant le premier mouvement Kekius"
    if cls == "faible_activite" and fetch:
        mv = moves(a, tk, r["sigs"])
        b = [m for m in mv if m["kind"] == "achat"]
        bp = [m for m in b if m["t"] < T_MUSK]
        sv = [m for m in mv if m["kind"] == "vente"]
        detail = (f"{len(b)} achats ({len(bp)} avant 06:02:01) pour {-sum(m['sol'] for m in b) / 1e9:.4f} SOL ; "
                  f"{len(sv)} ventes pour {sum(m['sol'] for m in sv) / 1e9:.4f} SOL jusqu'au 31/01/2025 ; "
                  f"{sum(1 for m in mv if m['kind'] in ('entrée', 'sortie'))} entrées ou sorties sans contrepartie")
        sig0 = (bp or b or mv or [{"sig": "", "t": None}])[0]
        interp = "achat avant le changement de profil" if bp else "achat après le changement de profil" if b else "aucun achat relu"
    else:
        sig0 = {"sig": "", "t": first}
        interp = {"service": f"service : {lab}", "haute_frequence": "bot ou trader à haute fréquence, non discriminant"}.get(cls, "non relu")
        status = "REJETÉ" if cls == "service" else "CONFIRMÉ"
    role = core.get(a, "")
    ov.append([tk, "solana", a, a, "A", f"même adresse : ATA {r['ata']} active dans la fenêtre ; DMAGA : {tags.get(a, '')}"
               + (f" ; noyau : {role}" if role else "") + (f" ; 1er achat DMAGA {utc(first_dmaga[a])}" if first_dmaga.get(a) else ""),
               sig0["sig"], utc(sig0["t"]) if sig0.get("t") else "", detail, "historique de l'ATA dérivée (k12, k14)", status,
               f"{cls} : {interp}", "data/ata_scan_summary.csv"])
with open(DATA / "ata_scan_summary.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["address", "token", "ata", "n_signatures", "first_activity_utc", "n_in_window_to_0104", "n_before_0602", "class", "dmaga_tags", "source"])
    w.writerows(summ)
cols = ["token", "chain", "kekius_side_address", "dmaga_side_address", "level", "relation", "tx_or_signature", "utc",
        "asset_amount", "method", "status", "interpretation", "source"]
with open(DATA / "ata_overlap.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(cols); w.writerows(ov)
from collections import Counter
print("couples", len(summ), Counter(x[7] for x in summ), "actifs dans la fenêtre", len(ov))
print("faible activité dans la fenêtre :", sum(1 for x in summ if x[7] == "faible_activite" and x[5] > 0),
      "dont avant 06:02:01 :", sum(1 for x in summ if x[7] == "faible_activite" and x[6] > 0))
