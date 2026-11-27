"""Vérification sur transactions brutes d'un échantillon des arêtes de reports/data_checks/transfer_coverage.json (issue #27).

Échantillon déterministe (ordre du hachage md5 de la signature) : 40 arêtes `gtba` sans aucune jambe dans trades, 20 arêtes à une
jambe dont la jambe présente est un `transfer`, 20 dont la jambe présente est un swap. Chaque transaction est relue par le RPC
public et décodée par dmaga.spl. Contrôles :
  - sans jambe : un mouvement DMAGA source → destination du montant exact existe ; le compte du mint est-il cité ?
  - une jambe : l'autre bout a un solde net DMAGA nul dans la transaction, ou c'est une venue (dmaga/venues.py, autorités).
Sortie : data/transfer_sample.csv et le décompte."""
import csv
import duckdb
from h_lib import DATA, DMAGA
import k16_pubrpc as pub
from h_decode import keys, movements, token_delta
from dmaga.config import BIG
from dmaga.venues import load as load_venues

AUTH = {"5Q544fKrFoe6tsEbD7S8EmxGTJYAKtTVhAW5Q5pge4j1", "87g44hEXP7R8ZxoAJtz941tsVftpEXC1LqAFTf2ZHtkH",
        "39azUYFWPz3VHgKCf3VChUwbpURdCHRxjWVowf5jUJjg", "PNLCQcVCD26aC7ZWgRyr5ptfaR7bBrWdTFgRWwu2tvF"}


def main():
    con = duckdb.connect(config={"memory_limit": "400MB", "threads": 1})
    con.execute(f"CREATE TABLE tl AS SELECT signature, owner, string_agg(DISTINCT kind, '+') kinds FROM '{BIG}/trades.parquet' WHERE owner IS NOT NULL GROUP BY 1, 2")
    con.execute(f"""CREATE TABLE g AS SELECT e.signature, e.src, e.dst, e.qty, s.kinds sk, d.kinds dk FROM '{BIG}/token_edges.parquet' e
        LEFT JOIN tl s ON s.signature=e.signature AND s.owner=e.src LEFT JOIN tl d ON d.signature=e.signature AND d.owner=e.dst
        WHERE e.how='gtba' AND e.dst<>'(multiple)'""")
    pick = lambda where, n: con.execute(f"SELECT signature, src, dst, qty, sk, dk FROM g WHERE {where} ORDER BY md5(signature), src, dst LIMIT {n}").fetchall()
    one = "(sk IS NULL) <> (dk IS NULL)"
    present = "coalesce(sk, dk)"
    sample = ([("aucune", r) for r in pick("sk IS NULL AND dk IS NULL", 40)] +
              [("une_transfer", r) for r in pick(f"{one} AND {present}='transfer'", 20)] +
              [("une_swap", r) for r in pick(f"{one} AND {present}='swap'", 20)])
    venues = set(load_venues()) | AUTH
    rows = []
    for cat, (sig, src, dst, qty, sk, dk) in sample:
        t = pub.tx(sig)
        q = round(qty * 1e6)
        mv = [m for m in movements(t) if m["kind"] == "token" and m["mint"] == DMAGA]
        exact = any(m["src"] == src and m["dst"] == dst and m["amount"] == q for m in mv)
        absent = None if cat == "aucune" else (dst if sk is not None else src)
        net = token_delta(t, absent, DMAGA) if absent else None
        ok = exact if cat == "aucune" else (net == 0 or absent in venues)
        rows.append({"categorie": cat, "signature": sig, "src": src, "dst": dst, "qty": qty, "err": bool(t["meta"].get("err")),
                     "mouvement_exact": exact, "mint_cite": DMAGA in keys(t), "bout_absent": absent or "", "net_du_bout_absent": net if net is not None else "",
                     "bout_absent_venue": bool(absent and absent in venues), "conforme": ok})
    with (DATA / "transfer_sample.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    for cat in ("aucune", "une_transfer", "une_swap"):
        g = [r for r in rows if r["categorie"] == cat]
        print(cat, "n", len(g), "conformes", sum(r["conforme"] for r in g), "mouvement exact", sum(r["mouvement_exact"] for r in g),
              "mint cité", sum(r["mint_cite"] for r in g), "échouées", sum(r["err"] for r in g))


if __name__ == "__main__":
    main()
