"""Sondes Helius bornées, constat 5 (jonction 7Gw3gL8m et 75fXGTvc, HFRc5Nmw) et constat 9 ($PEZI). Budget : 8 appels gtfa à 10 crédits, 3 getAsset à 10 crédits, soit 110 crédits au plus. Réponses brutes dans audits_work/I/net. Compte écrit dans credits.csv."""
import gzip,json,sys,time,os
from dmaga.helius import Helius
W="/Volumes/VERBATIM HD/Dark-MAGA-Investigation/audits_work/I/net/";os.makedirs(W,exist_ok=True)
OUT="audits/2026-11-03/work_I/"
h=Helius(rps=3)
cred=open(OUT+"credits.csv","a")
def page(a,tag,**kw):
    r=h.txs_page(a,limit=100,**kw)
    with gzip.open(f"{W}{a}.{tag}.jsonl.gz","wt") as f:
        for t in r.get("data") or []:f.write(json.dumps(t)+"\n")
    cred.write(f"{time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime())},gtfa_full,{a[:8]}.{tag},10\n");cred.flush()
    return len(r.get("data") or [])
A="7Gw3gL8mq7TSENSe9VZD9DgJiPQF9dHd6Auwk6PRkjhx"
print(page(A,"aout",sort="asc",filters={"blockTime":{"gte":1722650000,"lt":1722900000},"status":"succeeded"}))
print(page(A,"juil25",sort="asc",filters={"blockTime":{"gte":1752960000,"lt":1753200000},"status":"succeeded"}))
print(page(A,"mai24",sort="asc",filters={"blockTime":{"gte":1715700000,"lt":1715900000},"status":"succeeded"}))
print(page(A,"last",sort="desc"))
B="75fXGTvc8BHKBXwNfqriso6dzLe52qMUzvGPu9DV8fog"
print(page(B,"juil24",sort="asc",filters={"blockTime":{"gte":1720900000,"lt":1722400000},"status":"succeeded"}))
print(page(B,"janv25",sort="asc",filters={"blockTime":{"gte":1737800000,"lt":1738000000},"status":"succeeded"}))
for m in ("2dT27TYCxCCvfmtQcF4KeEb91PYcZmjYdUMc9MTeGLss","BbciExji4fhSbqcEWRvqrvNpumJy2y3kCKajc2XGDvLi","AZcjPDj4z1jsxbeof1uUTrgZQ5aDNN2zegjjutSQLohR"):
    r=h.call("getAsset",{"id":m});c=r.get("content",{}).get("metadata",{});print(m,c.get("name"),c.get("symbol"))
    cred.write(f"{time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime())},getAsset,{m[:8]},10\n");cred.flush()
print(dict(h.stats))
