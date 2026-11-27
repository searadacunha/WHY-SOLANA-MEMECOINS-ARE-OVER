#!/usr/bin/env python3
"""Fiche d'une adresse à partir de flows_all.parquet (traçage existant, sans réseau). usage : g08_addr.py addr1 addr2 ... > sortie.
Pour chaque adresse : flux SOL/USDC/USDT entrants et sortants vus depuis n'importe quel wallet tracé, distincts par signature."""
import duckdb, sys, os
from dmaga.labels import label
G = "/Volumes/VERBATIM HD/Dark-MAGA-Investigation/audits_work/G/"
FL = "/Volumes/VERBATIM HD/Dark-MAGA-Investigation/raw/flows/"; NET = "/Volumes/VERBATIM HD/Dark-MAGA-Investigation/audits_work/C/net/"
con = duckdb.connect(":memory:", config={"memory_limit": "600MB", "threads": 2, "temp_directory": G + "duck", "preserve_insertion_order": False})
con.execute("SET TimeZone='UTC'")
A = f"read_parquet('{G}flows_all.parquet')"
M = {"So11111111111111111111111111111111111111111": "SOL", "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v": "USDC", "Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB": "USDT", "7D7BRcBYepfi77vxySapmeqRNN1wsBBxnFPJGbH5pump": "DMAGA"}
adds = sys.argv[1:]
con.execute("CREATE TABLE q(a VARCHAR)"); con.executemany("INSERT INTO q VALUES (?)", [[a] for a in adds])
con.execute(f"CREATE TABLE d AS SELECT DISTINCT sig,bt,src,dst,mint,raw,ins,inner_ FROM {A} WHERE src IN (SELECT a FROM q) OR dst IN (SELECT a FROM q)")
for a in adds:
    print("==", a, "label", label(a), "net", os.path.exists(NET + a + ".jsonl.gz"), "flows", os.path.isdir(FL + a))
    for dir_, c1, c2 in (("IN", "dst", "src"), ("OUT", "src", "dst")):
        rows = con.execute(f"""SELECT mint,{c2} cp,count(*) n,sum(raw) s,strftime(to_timestamp(min(bt)),'%Y-%m-%d %H:%M') a,strftime(to_timestamp(max(bt)),'%Y-%m-%d') b,min(sig) ex FROM d WHERE {c1}=? GROUP BY 1,2 ORDER BY mint,s DESC""", [a]).fetchall()
        by = {}
        for r in rows: by.setdefault(r[0], []).append(r)
        for mint, L in by.items():
            dec = 1e9 if M.get(mint) == "SOL" else 1e6
            print(f"  {dir_} {M.get(mint, mint[:6])} contreparties {len(L)} total {sum(x[3] for x in L)/dec:.2f} n {sum(x[2] for x in L)}")
            for x in L[:int(os.environ.get('TOPN', '6'))]:
                print("     ", x[1], (label(x[1]) or "-")[:18], x[2], round(x[3] / dec, 3), x[4], x[5], x[6][:14])
