#!/usr/bin/env python3
"""Garantie de netting de trades, relue dans le brut (hors ligne, lecture seule du disque USB) : issue #27, 07/11/2026.

Pour chaque arête `gtba` de token_edges dont la transaction est dans trades, la transaction brute (raw/full_*) est décodée par
dmaga.spl. Contrôles :
  1. le mouvement DMAGA source → destination du montant exact existe (chemin d'instruction gardé) ;
  2. un bout absent de trades pour cette signature a un solde net DMAGA nul, ou c'est une venue : un virement réel n'est jamais
     ignoré parce qu'une autre opération du même propriétaire est dans trades ;
  3. pour chaque propriétaire hors venue de la transaction, le net de trades égale le net brut (pre/postTokenBalances).
Les arêtes sans aucune jambe dans trades mais dont la transaction est lue (jambes de passage, ajoutées à tort avant le 07/11)
sont listées avec leurs preuves. Compteurs des cas réels couverts : Token-2022, fermeture de compte, plusieurs mouvements DMAGA.
Sorties : reports/data_checks/netting_raw.json, reports/data_checks/passthrough_edges.csv."""
import csv
import gzip
import json
from collections import Counter, defaultdict

from dmaga import spl
from dmaga.config import BIG, BONDING_CURVE, MINT, RAW, ROOT
from dmaga.db import connect
from dmaga.venues import load as load_venues

AUTH = {"5Q544fKrFoe6tsEbD7S8EmxGTJYAKtTVhAW5Q5pge4j1", "87g44hEXP7R8ZxoAJtz941tsVftpEXC1LqAFTf2ZHtkH",
        "39azUYFWPz3VHgKCf3VChUwbpURdCHRxjWVowf5jUJjg", "PNLCQcVCD26aC7ZWgRyr5ptfaR7bBrWdTFgRWwu2tvF"}


def main():
    venues = set(load_venues()) | AUTH | {BONDING_CURVE}
    con = connect(mem="500MB", threads=1)
    E = str(BIG / "token_edges.parquet")
    con.execute("CREATE TEMP TABLE tn AS SELECT signature, owner, sum(token_delta) n FROM trades WHERE owner IS NOT NULL GROUP BY 1, 2")
    con.execute(f"""CREATE TEMP TABLE ge AS SELECT signature, src, dst, CAST(round(qty*1e6) AS BIGINT) q, block_time FROM read_parquet('{E}')
                    WHERE how='gtba' AND dst<>'(multiple)' AND signature IN (SELECT signature FROM trades)""")
    edges = defaultdict(list)
    for s, a, b, q, t in con.execute("SELECT * FROM ge").fetchall():
        edges[s].append((a, b, q, t))
    tnet = defaultdict(dict)
    for s, o, n in con.execute("SELECT * FROM tn WHERE signature IN (SELECT signature FROM ge)").fetchall():
        tnet[s][o] = n
    con.close()
    c, bad, seen, passthrough = Counter(), defaultdict(list), set(), []
    for src in ("pool", "mint", "curve", "venue"):
        for p in sorted((RAW / f"full_{src}").rglob("p*.jsonl.gz")):
            if p.name.startswith("._"):
                continue
            with gzip.open(p, "rt") as f:
                for line in f:
                    tx = json.loads(line)
                    s = tx["transaction"]["signatures"][0]
                    if s not in edges or s in seen:
                        continue
                    seen.add(s)
                    tr, mvs = tnet[s], spl.movements(tx)
                    mv = [m for m in mvs if m["kind"] == "token" and m["mint"] == MINT]
                    c["tx_token2022"] += any(ix.get("programId") == spl.TOKEN22 for _, ix in spl.instructions(tx))
                    c["tx_fermeture_de_compte"] += any(m["kind"] == "close" for m in mvs)
                    c["tx_plusieurs_mouvements_dmaga"] += len(mv) > 1
                    owners = {b.get("owner") for side in ("preTokenBalances", "postTokenBalances") for b in tx["meta"].get(side) or [] if b["mint"] == MINT}
                    for o in owners - venues - {None}:
                        c["proprietaires_controles"] += 1
                        if spl.token_delta(tx, o, MINT) != tr.get(o, 0):
                            bad["net_de_trades_different_du_brut"].append([s, o, spl.token_delta(tx, o, MINT), tr.get(o)])
                    for a, b, q, t in edges[s]:
                        c["aretes"] += 1
                        hit = [m["path"] for m in mv if m["src"] == a and m["dst"] == b and m["amount"] == q]
                        if not hit:
                            bad["mouvement_absent"].append([s, a, b, q])
                        na, nb = spl.token_delta(tx, a, MINT), spl.token_delta(tx, b, MINT)
                        for x, nx in ((a, na), (b, nb)):
                            if x not in tr and x not in venues and nx != 0:
                                bad["bout_absent_de_trades_a_net_non_nul"].append([s, a, b, q, x, nx])
                        if a not in tr and b not in tr:
                            passthrough.append({"signature": s, "block_time": t, "source_trades": src, "src": a, "dst": b, "montant_brut": q,
                                                "instruction": "+".join(hit), "mint_cite": MINT in spl.keys(tx), "net_src": na, "net_dst": nb,
                                                "src_venue": a in venues, "dst_venue": b in venues})
    c["signatures"], c["signatures_non_trouvees_dans_le_brut"] = len(edges), len(set(edges) - seen)
    out = {"compte": c, "contre_exemples": {k: len(v) for k, v in bad.items()}, "exemples": {k: v[:50] for k, v in bad.items()},
           "jambes_de_passage": {"aretes": len(passthrough), "jetons_M": round(sum(r["montant_brut"] for r in passthrough) / 1e12, 3),
                                 "deux_bouts_a_net_nul_ou_venue": sum((r["net_src"] == 0 or r["src_venue"]) and (r["net_dst"] == 0 or r["dst_venue"]) for r in passthrough)},
           "limite": "les transactions absentes de trades (arêtes ajoutées par ana_20 et dmaga.positions) ne sont pas dans le brut local"}
    d = ROOT / "reports" / "data_checks"
    (d / "netting_raw.json").write_text(json.dumps(out, indent=1, ensure_ascii=False))
    passthrough.sort(key=lambda r: (r["block_time"], r["signature"], r["src"], r["dst"]))
    with (d / "passthrough_edges.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(passthrough[0]))
        w.writeheader()
        w.writerows(passthrough)
    print(json.dumps({k: out[k] for k in ("compte", "contre_exemples", "jambes_de_passage")}, ensure_ascii=False))
    assert not bad and not c["signatures_non_trouvees_dans_le_brut"], "garantie de netting violée : voir netting_raw.json"


if __name__ == "__main__":
    main()
