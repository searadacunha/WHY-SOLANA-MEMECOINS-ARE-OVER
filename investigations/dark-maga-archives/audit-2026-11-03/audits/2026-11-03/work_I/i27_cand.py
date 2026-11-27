"""Lignes brutes des destinations partagées à petite population. Sortie i27_cand.txt."""
import csv,json,sys,duckdb,datetime as dt
OUT="audits/2026-11-03/work_I/";W="/Volumes/VERBATIM HD/Dark-MAGA-Investigation/audits_work/I/"
sys.stdout=open(OUT+"i27_cand.txt","w")
rows=list(csv.DictReader(open(OUT+"i25_shared.csv")))
cand=[r["dst"] for r in rows if int(r["nsrc_tous"])<=15 and (not r["label"] or r["label"]=="None")]
EXTRA=["9UsmwVmbV4VwEwv5q5iZh4y3THh6dn2cqjFpEUrGRzZJ","DtDNw24nr4Qx3Kyg4swgewSakMJF4BzV2zmDKfDFKSaY","AxHocY4moH8roYQXMQWqoehtW5piMtTJQYmfL4wQ83D8","ExuV9d3SbtDJj8JmfH7hqFEaRFxBzpy4f8XMmKUPSsLh"]
cand+= [x for x in EXTRA if x not in cand]
con=duckdb.connect(":memory:",config={"memory_limit":"500MB","threads":2,"temp_directory":W+"duck"})
con.execute("SET TimeZone='UTC'")
con.execute(f"CREATE TABLE f AS SELECT DISTINCT src,dst,asset,amount::DOUBLE amt,bt::BIGINT bt,sig FROM read_csv_auto('{W}flows_out.csv.gz',header=true,all_varchar=true) WHERE dst IS NOT NULL AND asset<>'DMAGA' UNION ALL BY NAME SELECT src,dst,asset,amount::DOUBLE amt,bt::BIGINT bt,sig FROM read_csv_auto('{W}net_out.csv.gz',header=true,all_varchar=true) WHERE dst IS NOT NULL AND asset<>'DMAGA'")
P1={list(r.values())[0] for r in csv.DictReader(open("audits/2026-11-03/work_G/g40_p1_wallets.csv"))}
g33=set(json.load(open("data/prevent_groups.json"))[0]["members"])
series={r["wallet"] for r in csv.DictReader(open("audits/2026-11-03/work_C/cb_series.csv"))}
for d in cand:
    print("==",d)
    for r in con.execute("select distinct src,asset,amt,strftime(to_timestamp(bt),'%Y-%m-%d %H:%M:%S'),sig from f where dst=? order by 4",[d]).fetchall():
        print("  ",r[3],r[0],"P1" if r[0] in P1 else "","33" if r[0] in g33 else "","série" if r[0] in series else "",r[1],round(r[2],4),r[4][:16])
