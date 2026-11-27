"""Noyau DMAGA (priorités 1 à 8 de la mission) et ses contreparties directes non mutualisées.

Noyau : groupe des 33, gagnants nommés, créateur, Ei5yGz8d et wallets deBridge Solana, pistes B5fC3Dg4 / FKtvVzBS, plus
financeurs directs (funding_edges niveau 0) et destinations de sortie (exit_flows) d'au moins 1 SOL ou 100 USDC/USDT, hors
pools et hors adresses étiquetées. Une contrepartie qui touche plus de 25 wallets DMAGA est traitée comme hub et exclue.
Sortie : data/core_set.csv (address, role, via)."""
import csv
import duckdb
from k_lib import DATA, DMAGA_BIG

NAMED = {
    "8YLEuUtZ4eFMJbf46oNb1CeG6dYFWGyxnQSh9hrgzBzR": "créateur DMAGA",
    "H3QsBrrivimFJmSpTXuvig2n1Bh7JuYxrriRSEszT6cc": "gagnant H3QsBrr",
    "GXZvXsD6hxaLeFvQisWpdAwsayJxga7w9EeafhFZG2Ra": "gagnant GXZvXs",
    "9PrmF8sfoD2YShtWUghrGEYgxwabpnzog8gT1V6LEtdq": "gagnant 9PrmF8",
    "5QhJJcFZu2ashyKyWSTGHcsyo6ZBCbpVuJqeutvQHScd": "gagnant 5QhJJc, lié au créateur",
    "Ei5yGz8dPndr1aCeHZsfqJBcS3VBbz75VHEhxxJKLy3V": "cluster Ei5yGz8d (deBridge)",
    "Hp2BtvnZvw7YxbQvSehqb1LC5jBSX1aLApzHQnDVwf3q": "Hp2BtvnZ (dépôt Coinbase commun avec Ei5)",
    "E72DuqDL2fkCw2Q8tyW2zWXpkRgK1p6FBJys6h6wpgVG": "E72DuqDL (financé par Ei5, payé par b298)",
    "GZXKYzwZPgWH8TwyY9f8dkCQ9EKK6nrPZADGcEwfAg7Y": "GZXKYzwZ (ordre deBridge vers b947)",
    "2aeEoq5n8Cip2raJsiWHBVKuoJL4rid7adepkVYnVzDm": "2aeEoq5n (sortie DCA 393,81 SOL)",
    "C73Yv9iHmTaf8SU2XFnGLt7QXUDqbeWNtUYza9WJhkae": "C73Yv9iH (deBridge vers 2d86)",
    "B5fC3Dg42BRT8GffXg8nPy6ktQtgQ1UL5pHTZ7rnsmmR": "piste B5fC3Dg4",
    "FKtvVzBS8udyxkT4nsrMVEBMTpyUsnSm2CRk7w8j6n31": "piste FKtvVzBS",
    "G41vRrsHShLEvwMj58ruhqJycGfAtWXxtLD56uFExL8E": "G41vRrs (financeur de 10 des 32)",
}
B = str(DMAGA_BIG)
role = dict(NAMED)
for r in csv.DictReader(open(DATA / "dmaga_universe.csv")):
    if "group33" in r["tags"]:
        role.setdefault(r["address"], "groupe des 33")
duckdb.sql("create table core(a varchar)")
duckdb.executemany("insert into core values (?)", [(a,) for a in role])
fan = dict(duckdb.sql(f"select dst, count(distinct wallet) from '{B}/exit_flows.parquet' group by dst").fetchall())
fan_src = dict(duckdb.sql(f"select src, count(distinct wallet) from '{B}/funding_edges.parquet' group by src").fetchall())
rows = [(a, r, "") for a, r in role.items()]
for dst, w in duckdb.sql(f"""select distinct dst, wallet from '{B}/exit_flows.parquet' e join core on e.wallet=core.a
        where not is_pool and dst_label is null and ((asset='SOL' and amount>=1) or (asset in ('USDC','USDT') and amount>=100))""").fetchall():
    if dst not in role and fan.get(dst, 0) <= 25:
        rows.append((dst, "destination de sortie", w))
for src, w in duckdb.sql(f"""select distinct src, wallet from '{B}/funding_edges.parquet' f join core on f.wallet=core.a
        where level=0 and src_label is null and not is_pool and sol>=0.5""").fetchall():
    if src not in role and fan_src.get(src, 0) <= 25:
        rows.append((src, "financeur direct", w))
with open(DATA / "core_set.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(["address", "role", "via"]); w.writerows(rows)
print("noyau", len(role), "lignes", len(rows), "adresses", len({r[0] for r in rows}))
