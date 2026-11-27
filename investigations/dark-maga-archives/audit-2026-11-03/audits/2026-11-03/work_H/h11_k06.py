import duckdb
B = "/Volumes/VERBATIM HD/Dark-MAGA-Investigation/data_v2"
c = duckdb.connect(":memory:", config={"memory_limit": "500MB", "threads": 2, "temp_directory": "/Volumes/VERBATIM HD/Dark-MAGA-Investigation/audits_work/H"})
BT, P = f"read_parquet('{B}/bots.parquet')", f"read_parquet('{B}/owner_programs.parquet')"
c.execute(f"CREATE TEMP TABLE g AS SELECT owner a, bought_sol b, part_aller_retour r FROM {BT} WHERE bought_sol>=100 AND lignes_signataire=0 AND NOT bot_aller_retour")
print(c.execute(f"""WITH u AS (SELECT program, count(DISTINCT owner) n FROM {P} GROUP BY 1), p AS (SELECT owner, program, count(DISTINCT signature) n FROM {P} WHERE owner IN (SELECT a FROM g) GROUP BY 1,2), t AS (SELECT owner, count(DISTINCT signature) n FROM {P} WHERE owner IN (SELECT a FROM g) GROUP BY 1)
SELECT p.owner, g.b, g.r, p.program, u.n, round(p.n*1.0/t.n,3) FROM p JOIN t USING(owner) JOIN u USING(program) JOIN g ON g.a=p.owner WHERE p.n>=0.8*t.n AND u.n<=50 ORDER BY g.b DESC""").fetchall())
