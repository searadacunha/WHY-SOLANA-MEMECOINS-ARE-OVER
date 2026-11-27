#!/usr/bin/env python3
"""Graphe aveugle des transferts directs de DMAGA, regles de l'auditeur C, depuis les tables plates du scan.
 1. compte de jetons -> proprietaire (pre/post soldes), comptes a plusieurs proprietaires listes a part.
 2. transferts SPL inter-proprietaires (ix) + lignes dmaga_all des flows absentes du brut.
 3. profil comportemental de chaque proprietaire : tx, tx signees, contreparties, part avec AMM.
 4. exclusion par comportement : jamais signataire + au moins 5 tx, ou etiquette publique de service.
 5. aretes >= 1 M dans des tx sans AMM ni agregateur ; composantes depuis les graines ; sorties CSV.
"""
import csv
import sys
import time
from collections import defaultdict
from pathlib import Path

import duckdb

from dmaga.labels import label

W = "/Volumes/VERBATIM HD/Dark-MAGA-Investigation/audits_work/C"
WORK = Path(__file__).resolve().parent
SEEDS = ["8YLEuUtZ4eFMJbf46oNb1CeG6dYFWGyxnQSh9hrgzBzR", "5QhJJcFZu2ashyKyWSTGHcsyo6ZBCbpVuJqeutvQHScd",
         "G41vRrsHShLEvwMj58ruhqJycGfAtWXxtLD56uFExL8E", "9W9b3zgHH9mCEHDhsdbnbEPHStm9vvXS4aia4DWHBxpL"]
AMM = ["675kPX9MHTjS2zt1qfr1NYHuzeLXfQM9H24wFSUt1Mp8", "CAMMCzo5YL8w4VFF8KVHrK22GGUsp5VTaW7grrKgrWqK", "CPMMoo8L3F4NbTegBCKVNunggL7H1ZpdTHKxQB5qKP1C",
       "LBUZKhRxPF3XUpBCjp4YzTKgLccjZhTSDM9YuVaPwxo", "Eo7WjKq67rjJQSZxS6z3YkapzY3eMj6Xy8X5EQVn5UaB", "whirLbMiicVdio4qvUfM5KAg6Ct8VwpYzGff3uctyCc",
       "PhoeNiXZ8ByJGLkxNfZRnkUfjvmuYqLR89jjFHGqdXY", "FLUXubRmkEi2q6K3Y9kBPg9248ggaZVsoSFhtJHSrm1X", "pAMMBay6oceH9fJKBRHGP5D4bD4sWpmSwMn52FMfXEA",
       "JUP6LkbZbjS1jKKwapdHNy74zcZ3tLUZoi5QNyVTaV4", "JUP4Fb2cqiRUcaTHdrPC8h2gNsA2ETXiPDD33WcGuJB", "DCA265Vj8a9CEuX1eb1LWRnDT7uK6q1xMipnNyatn23M",
       "jupoNjAxXgZ4rjzxzPMP4oxduvQsQtZzyknqvzYNrNu", "6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P", "BSfD6SHZigAfDWSjzD5Q41jw8LmKwtmjskPH9XW1mrRW",
       "DEXYosS6oEGvk8uCDayvwEZz4qEyDJRf9nFgYCaqPMTm", "2wT8Yq49kHgDzXuPxZSaeLaH1qbmGXtEyPy64bL7aD3c", "obriQD1zbpyLz95G5n7nJe6a4DPjpFwa5XYPoNm113y",
       "SoLFiHG9TfgtdUXUjWAxi3LtvYuFyDLVhBWxdMZxyCe", "TessVdML9pBGgG9yGks7o4HewRaXVAMuoVj4x83GLQH", "ZERor4xhbUycZ6gb9ntrhqscUcZmAbQDjEAtCf4hbZY",
       "HyaB3W9q6XdA5xwpU4XnSZV94htfmbmqJXZcEbRaJutt", "H8W3ctz92svYg6mkn1UtGfu2aQr2fnUFHM1RhScEtQDt"]  # DeJBGd retire : instruction sans effet inseree par un portefeuille, verifie sur 5Vn7uLoHkW
THRESH = int(sys.argv[1]) if len(sys.argv) > 1 else 1_000_000_000_000  # 1 M jetons, 6 decimales
RAWDIR = W


def main():
    con = duckdb.connect()
    con.execute(f"SET memory_limit='800MB'; SET threads=2; SET TimeZone='UTC'; SET temp_directory='{W}/tmp'; SET preserve_insertion_order=false;")
    t = time.time()
    con.execute(f"""CREATE TEMP TABLE ta_owner AS
      SELECT token_account, arg_max(owner, n) owner, count(*) n_owners FROM (
        SELECT token_account, owner, count(*) n FROM (
          SELECT token_account, owner_post AS owner FROM '{W}/ta.parquet' WHERE owner_post IS NOT NULL AND owner_post <> ''
          UNION ALL SELECT token_account, owner_pre FROM '{W}/ta.parquet' WHERE owner_pre IS NOT NULL AND owner_pre <> '')
        GROUP BY 1,2) GROUP BY 1""")
    print("comptes de jetons", con.execute("SELECT count(*), sum(n_owners>1) FROM ta_owner").fetchone(), round(time.time() - t), flush=True)
    con.execute(f"COPY (SELECT * FROM '{W}/ta.parquet' t WHERE owner_pre IS NOT NULL AND owner_post IS NOT NULL AND owner_pre<>'' AND owner_post<>'' AND owner_pre<>owner_post) TO '{W}/owner_changes.csv' (HEADER)")
    print("changements de proprietaire", con.execute(f"SELECT count(*) FROM '{W}/owner_changes.csv'").fetchone(), flush=True)
    # transferts inter-proprietaires
    con.execute(f"""COPY (SELECT i.tid, i.kind, i.src_ta, i.dst_ta, a.owner src_o, b.owner dst_o, i.authority, i.amount, i.outer_prog, i.ord
        FROM '{W}/ix.parquet' i LEFT JOIN ta_owner a ON a.token_account=i.src_ta LEFT JOIN ta_owner b ON b.token_account=i.dst_ta
        WHERE i.kind IN ('transfer','transferChecked') AND coalesce(a.owner,'')<>coalesce(b.owner,'')) TO '{W}/xfer.parquet' (FORMAT parquet, COMPRESSION zstd)""")
    print("xfer", con.execute(f"SELECT count(*) FROM '{W}/xfer.parquet'").fetchone(), round(time.time() - t), flush=True)
    # profil par proprietaire : tx ou son solde bouge, tx signees parmi celles-ci
    con.execute(f"""COPY (WITH tm AS (SELECT tid, signers, programs FROM '{W}/tx.parquet'),
        ow AS (SELECT DISTINCT tid, coalesce(nullif(owner_post,''),owner_pre) owner FROM '{W}/ta.parquet')
        SELECT owner, count(*) n_tx, sum(CASE WHEN contains(signers, owner) THEN 1 ELSE 0 END) n_signed
        FROM ow JOIN tm USING(tid) GROUP BY 1) TO '{W}/owner_profile.parquet' (FORMAT parquet)""")
    print("profils", con.execute(f"SELECT count(*), sum(n_signed=0), sum(n_tx>=5 AND n_signed=0) FROM '{W}/owner_profile.parquet'").fetchone(), round(time.time() - t), flush=True)
    # aretes candidates >= seuil : tx detail
    amm_any = "|".join(AMM)
    con.execute(f"""CREATE TEMP TABLE big AS SELECT x.*, t.sig, t.slot, t.txidx, t.bt, t.payer, t.signers, t.programs, t.loc,
           regexp_matches(t.programs, '{amm_any}') has_amm
        FROM '{W}/xfer.parquet' x JOIN '{W}/tx.parquet' t USING(tid) WHERE x.amount >= {THRESH}""")
    print("transferts >= seuil", con.execute("SELECT count(*), sum(has_amm::int) FROM big").fetchone(), round(time.time() - t), flush=True)
    con.execute(f"CREATE TEMP TABLE prof AS SELECT * FROM '{W}/owner_profile.parquet'")
    rows = con.execute("""SELECT b.sig, b.slot, b.txidx, b.bt, b.src_o, b.dst_o, b.amount, b.authority, b.payer, b.signers, b.programs, b.has_amm, b.kind, b.ord, b.outer_prog, b.loc,
         coalesce(p1.n_tx,0), coalesce(p1.n_signed,0), coalesce(p2.n_tx,0), coalesce(p2.n_signed,0)
         FROM big b LEFT JOIN prof p1 ON p1.owner=b.src_o LEFT JOIN prof p2 ON p2.owner=b.dst_o ORDER BY b.slot, b.txidx""").fetchall()
    cols = "sig slot txidx bt src dst amount authority payer signers programs has_amm kind ord outer_prog loc src_ntx src_nsig dst_ntx dst_nsig".split()
    wr = csv.writer(open(WORK / f"cand_edges_{THRESH // 10**12}M.csv", "w", newline=""))
    wr.writerow(cols + ["utc", "src_label", "dst_label"])
    for r in rows:
        wr.writerow(list(r) + [time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(r[3])), label(r[4]) or "", label(r[5]) or ""])
    print("ecrit", len(rows), round(time.time() - t), flush=True)
    # lignes flows hors brut
    n = con.execute(f"""SELECT count(*), count(DISTINCT sig) FROM (SELECT DISTINCT sig, from_u, to_u, amount FROM '{W}/flows_dmaga.parquet' WHERE amount >= {THRESH} AND from_u<>to_u)
         WHERE sig NOT IN (SELECT sig FROM '{W}/tx.parquet')""").fetchone()
    print("flows >= seuil absents du brut (lignes, signatures)", n, flush=True)
    con.execute(f"""COPY (SELECT DISTINCT sig, slot, idx, bt, from_u, to_u, from_ta, to_ta, amount FROM '{W}/flows_dmaga.parquet' WHERE amount >= {THRESH} AND from_u<>to_u AND sig NOT IN (SELECT sig FROM '{W}/tx.parquet') ORDER BY slot, idx) TO '{str(WORK)}/flows_absent_raw_{THRESH // 10**12}M.csv' (HEADER)""")


if __name__ == "__main__":
    main()
