"""Lecture des sondes i70 : 7Gw3gL8m et 75fXGTvc. Sortie i71.txt."""
import gzip,json,glob,sys,collections,datetime as dt,csv
sys.path.insert(0,"audits/2026-11-03/work_I")
from i_lib import keys,signers,sol_delta,tok_delta,programs,BASIC,USDC,USDT,WSOL,DMAGA
OUT="audits/2026-11-03/work_I/";W="/Volumes/VERBATIM HD/Dark-MAGA-Investigation/audits_work/I/net/"
sys.stdout=open(OUT+"i71.txt","w")
iso=lambda t:dt.datetime.fromtimestamp(t,dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S")
P1={list(r.values())[0] for r in csv.DictReader(open("audits/2026-11-03/work_G/g40_p1_wallets.csv"))}
g33=set(json.load(open("data/prevent_groups.json"))[0]["members"])
def tag(x):return ("P1" if x in P1 else "")+("33" if x in g33 else "")
for A,tags in (("7Gw3gL8mq7TSENSe9VZD9DgJiPQF9dHd6Auwk6PRkjhx",("aout","juil25","mai24","last")),("75fXGTvc8BHKBXwNfqriso6dzLe52qMUzvGPu9DV8fog",("juil24","janv25"))):
    print("==",A)
    for tg in tags:
        p=f"{W}{A}.{tg}.jsonl.gz";n=0;sg=0;pg=collections.Counter();rows=[]
        for l in gzip.open(p,"rt"):
            t=json.loads(l);n+=1;S=signers(t)
            if A in S:
                sg+=1
                for x in programs(t)-BASIC:pg[x[:10]]+=1
            sd=sol_delta(t);td,dec=tok_delta(t)
            v=sd.get(A,0)/1e9;pure=not(programs(t)-BASIC)
            tok={m[:6]:x/10**dec[m] for (o,m),x in td.items() if o==A}
            other=[o for (o,m),x in td.items() if o!=A and m in tok and False]
            if pure and (abs(v)>=0.05 or tok):
                cp=[k for k,x in sd.items() if k!=A and (x<0)==(v>0) and x!=0]+[o for (o,m),x in td.items() if o!=A]
                rows.append((iso(t["blockTime"]),round(v,4),{k:round(x,3) for k,x in tok.items()},sorted({c for c in cp})[:3],sorted({tag(c) for c in cp if tag(c)})))
            elif DMAGA[:6] in tok:
                rows.append((iso(t["blockTime"]),"swap ou autre",{k:round(x,3) for k,x in tok.items()},S[0][:8]))
        print(tg,"tx",n,"signées",sg,"programmes signés",pg.most_common(6))
        for r in rows[:40]:print("   ",r)
